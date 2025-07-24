#######################################################################################################################
# @file         bfr.py
# @brief        APIs to verify bfr and parse etl
#
# @author       Gopikrishnan R
#######################################################################################################################

import logging
import os
import time
import math

from DisplayRegs.DisplayOffsets import TimingOffsetValues

from DisplayRegs.DisplayOffsets import VrrOffsetValues
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Tests.PowerCons.Modules.dut_context import Adapter, Panel, RrSwitchingMethod
from Tests.PowerCons.Modules import common, dut
from Libs.Core.display_config import display_config
from Libs.Core.logger import html, etl_tracer, gdhm
from Libs.Core.test_env import test_context
from Libs.Core import etl_parser, registry_access, display_essential
from Tests.PowerCons.Modules.dut_context import PRE_GEN_13_PLATFORMS

VBI_DELTA_TIME_TOLERANCE = 1
VRR_ADAP_BAL_PREDICTION_ERROR_MAX_VALUE_IN_MICRO_SEC = 5000
ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.displayDiagnosticsData = 1
ETL_PARSER_CONFIG.dpcdData = 1
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.vbiData = 1
FLIP_ONLY_PARSER_CONFIG = etl_parser.EtlParserConfig()
FLIP_ONLY_PARSER_CONFIG.flipData = 1

VRR_VMAX = "VRR_VMAX"
VTOTAL = "VTOTAL"
tstamp = lambda x: round((x / 1000), 2)

__display_config = display_config.DisplayConfiguration()


#
##
# @brief        Helper function to check if RR change is happening or not
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    etl_file string indicating the path of etl file
# @param[in]    power_event Power event
# @param[in]    negative Negative
# @param[in]    start_timestamp timestamp in ETL from where verification should start
# @param[in]    end_timestamp  timestamp in ETL from where verification should end
# @return       status bool True if RR change is detected, False otherwise
def verify(adapter: Adapter, panel: Panel, etl_file: str, power_event=None, negative=False,
           start_timestamp=None,
           end_timestamp=None) -> bool:
    bfr_config = etl_parser.EtlParserConfig()
    bfr_config.mmioData = 1
    bfr_config.vbiData = 1
    bfr_config.flipData = 1
    bfr_config.commonData = 1

    rr_list = set()
    if etl_parser.generate_report(etl_file, bfr_config) is False:
        logging.error("\tFailed to generate ETL report")
        return False

    # update BFR and HRR caps based on FLIPQ Event into ETL
    feature_control_info = etl_parser.get_event_data(etl_parser.Events.FEATURE_CONTROL)
    if feature_control_info is None:
        logging.error("No Data found for FeatureControl")
        assert False, "No Data found for FeatureControl"
    if feature_control_info[0].OsFtrTable[0] & 0x1 == 0x1:
        logging.info("OS FlipQ is enabled in OsFtrTable")
        os_aware_flipq_enable = True
    else:
        logging.info("OS FlipQ is disabled in OsFtrTable")
        os_aware_flipq_enable = False
    dut.update_bfr_hrr_caps(adapter, os_aware_flipq_enable)

    # logic for verifying rr change in flip
    flip_data = etl_parser.get_flip_data(sourceid=panel.source_id)
    if flip_data is None:
        logging.error(f"\tNo flip data found for pipe {panel.pipe}")
        return False
    rr_flip_list = []
    flip_rrs = set()
    previous_rr = 0
    total_flip_count = len(flip_data)
    for i in range(total_flip_count):
        flip = flip_data[i]
        if flip.Duration > 0:
            rr = (10 ** 7) / flip.Duration
            if (previous_rr != rr) and ((i + 2) < total_flip_count):
                # add a check to see if the next two flips are also with the changed duration, then only consider it
                # as a change.
                if flip.Duration == flip_data[i + 1].Duration == flip_data[i + 2].Duration:
                    # keeping track of timestamp at which flip duration changed, also the next two flips
                    rr_flip_list.append(
                        (flip.TimeStamp, flip_data[i + 1].TimeStamp, flip_data[i + 2].TimeStamp, round(rr, 2)))
                else:
                    logging.warning(f"\tInconsistent rate of change of RR in os flip at \
                    {flip.TimeStamp, flip_data[i + 1].TimeStamp, flip_data[i + 2].TimeStamp} seconds, Skipping")
            previous_rr = rr
            flip_rrs.add(round(rr, 2))
    if negative:
        if len(rr_flip_list) > 1:
            logging.error("OS Flip duration change wasn't expected")
            gdhm.report_driver_bug_os("[OsFeatures][BFR] OS Flip duration change wasn't expected")
            return False
        else:
            logging.info("OS Flip duration change wasn't seen as expected")
            return True
    elif len(rr_flip_list) <= 1:
        logging.error(f"\tRefresh rate not detected in os flip call")
        gdhm.report_driver_bug_os("[OsFeatures][BFR] Refresh rate not detected in os flip call")
        return False
    logging.info(f"\tRefresh rate change detected in OS flip Call {[(ts, rr) for (ts, ts1, ts2, rr) in rr_flip_list]}")
    # popping the first element of the list, as we it is the rr change we are interested in
    rr_flip_list.pop(0)
    status = True

    for ts, ats1, ats2, rr in rr_flip_list:
        duration_rr = int(math.floor(rr))
        html.step_start(
            f"Verifying register programming for os duration change for rr {rr}Hz detected at {tstamp(ts)}s")
        latency = (1/rr)*1000*3  # programming latency till next 3 frames as per RR.
        logging.info(f"Flip with duration change : {tstamp(ts)} 2nd Flip : {tstamp(ats1)} 3rd Flip: {tstamp(ats2)}")
        rr_change_list = get_rr_register_data(adapter, panel, etl_file, ts, ts + latency)
        rr_change_list2 = get_rr_register_data(adapter, panel, etl_file, ats1,
                                               ats1 + latency)
        rr_change_list3 = get_rr_register_data(adapter, panel, etl_file, ats2,
                                               ats2 + latency)
        detected_rr = None
        # Skipping the duration check of modeset RR
        modeset_rr = round(__get_modeset_rr(adapter, panel))
        logging.debug(f"\tduration RR is {duration_rr} \t modeset RR is {modeset_rr}")
        if duration_rr == int(math.floor(modeset_rr)):
            if (len(rr_change_list) == 0) and (len(rr_change_list2) == 0) and (len(rr_change_list3) == 0):
                logging.info(
                    f"Expected: RR programming of {rr} not detected after all three duration changes{tstamp(ats2)}s")
                continue
        if len(rr_change_list) == 0:
            logging.warning(
                f"RR programming of {rr} not detected after the first flip with duration change{tstamp(ts)}s")
            if len(rr_change_list2) == 0:
                logging.warning(
                    f"RR programming of {rr} not detected after the first flip after the second duration change{tstamp(ats1)}s")
                if len(rr_change_list3) == 0:
                    logging.error(
                        f"RR programming of {rr} not detected after the first flip after the third duration change{tstamp(ats2)}s")
                    status = False
        else:
            if len(rr_change_list) > 1:
                logging.warning(
                    f"Multiple RR change detected wrt {panel.lrr_caps.rr_switching_method} : {rr_change_list}")
            flag = False
            for mmio_ts, detected_rr in rr_change_list:
                if abs(detected_rr - rr) <= 1:
                    logging.info(
                        f"RR change detected wrt {panel.lrr_caps.rr_switching_method} : {detected_rr} is a per the flip1")
                    flag = True

            if not flag and len(rr_change_list2) > 0:
                logging.warning(
                    f"RR change detected wrt {panel.lrr_caps.rr_switching_method} : {rr_change_list} is not as per "
                    f"the flip rr {rr}Hz after Flip1, checking with next Flip")
                for mmio_ts, detected_rr in rr_change_list2:
                    if abs(detected_rr - rr) <= 1:
                        logging.info(
                            f"RR change detected wrt {panel.lrr_caps.rr_switching_method} : {detected_rr} is a per the flip2")
                        flag = True

            if not flag and len(rr_change_list3) > 0:
                logging.warning(
                    f"RR change detected wrt {panel.lrr_caps.rr_switching_method} : {rr_change_list} is not as per "
                    f"the flip rr {rr}Hz after Flip1, checking with next Flip")
                for mmio_ts, detected_rr in rr_change_list3:
                    if abs(detected_rr - rr) <= 1:
                        logging.info(
                            f"RR change detected wrt {panel.lrr_caps.rr_switching_method} : {detected_rr} is a per the flip3")
                        flag = True

            if not flag:
                logging.error(
                    f"RR change not detected wrt {panel.lrr_caps.rr_switching_method} : {rr_change_list} is not as per "
                    f"the flip rr {rr}Hz")
                status = False
            html.step_end()

    logging.info(f"All RR info programmed as per {panel.lrr_caps.rr_switching_method}")
    if not status:
        logging.error("RR programming not detected wrt OS Flip Duration change")
        gdhm.report_driver_bug_os("[OsFeatures][BFR] RR programming change not detected")

    return status


#
##
# @brief        get_rr_register_data : get rr programming data from ETL
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    etl_file string indicating the path of etl file
# @param[in]    start_timestamp timestamp in ETL from where verification should start
# @param[in]    end_timestamp  timestamp in ETL from where verification should end
# @return       rr_change_list
def get_rr_register_data(adapter, panel, etl_file, start_timestamp, end_timestamp):
    logging.debug(f"start_timestamp is {start_timestamp}, end_timestamp is {end_timestamp}")
    timing_info = adapter.regs.get_timing_info(panel.transcoder_type)
    h_total = timing_info.HTotal
    if panel.mso_caps.is_mso_supported:
        logging.info(f"This panel is MSO supported so multiplying HTotal with number of segments"
                     f" {panel.mso_caps.no_of_segments}")
        h_total = panel.mso_caps.no_of_segments * h_total
    timing_offsets = adapter.regs.get_timing_offsets(panel.transcoder_type)
    current_mode = __display_config.get_current_mode(panel.display_info.DisplayAndAdapterInfo)
    rr_change_list = []
    # VrrVmax / VrrDcbVmax (For PTL platform on DP panel due to MSA issue)
    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_HW:
        if adapter.name in common.GEN_16_PLATFORMS and panel.panel_type == "DP" and panel.is_lfp == False:
            vrr_offsets = adapter.regs.get_vrr_offsets(panel.transcoder_type)
            mmio_output = etl_parser.get_mmio_data(vrr_offsets.VrrDcbVmaxReg, is_write=True, start_time=start_timestamp,
                                                   end_time=end_timestamp)
            logging.info(f"Reading info from VrrDcbVmax reg Addr:0x%X" % vrr_offsets.VrrDcbVmaxReg)
        else:
            vrr_offsets = adapter.regs.get_vrr_offsets(panel.transcoder_type)

            mmio_output = etl_parser.get_mmio_data(vrr_offsets.VrrVmaxReg, is_write=True, start_time=start_timestamp,
                                                   end_time=end_timestamp)
            logging.info(f"Reading info from VrrVmax reg Addr:0x%X" % vrr_offsets.VrrVmaxReg)
        if mmio_output is not None:
            rr_list_vrrvmax = set()
            previous_rr = 0
            for mmio_data in mmio_output:
                if adapter.name in common.GEN_16_PLATFORMS and panel.panel_type == "DP" and panel.is_lfp == False:
                    vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                         VrrOffsetValues(VrrDcbVmaxReg=mmio_data.Data))
                    logging.debug(
                        f"pixel clock:{current_mode.pixelClock_Hz}, H_total:{h_total}, DcbVmax: {vrr_info.VrrDcbVmax}")
                    rr = round(float(current_mode.pixelClock_Hz) / ((h_total + 1) * (vrr_info.VrrDcbVmax + 1)), 3)
                    logging.info(
                        f"pixel clock:{current_mode.pixelClock_Hz}, H_total:{h_total}, DcbVmax: {vrr_info.VrrDcbVmax}")
                else:
                    vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                         VrrOffsetValues(VrrVmaxReg=mmio_data.Data))
                    logging.debug(
                        f"pixel clock:{current_mode.pixelClock_Hz}, H_total:{h_total}, VrrVmax: {vrr_info.VrrVmax}")
                    rr = round(float(current_mode.pixelClock_Hz) / ((h_total + 1) * (vrr_info.VrrVmax + 1)), 3)
                    logging.info(
                        f"pixel clock:{current_mode.pixelClock_Hz}, H_total:{h_total}, Vmax: {vrr_info.VrrVmax}")
                rr_list_vrrvmax.add(rr)
                logging.debug(
                    f"vrr_vmax reg value: {vrr_info.VrrVmax} rr : {rr} time:{tstamp(mmio_data.TimeStamp)}s")
                if previous_rr != rr:
                    rr_change_list.append((mmio_data.TimeStamp, round(rr, 2)))
                    logging.info(f"RR programming of {rr}Hz detected on VrrVmax at {mmio_data.TimeStamp}s")
                previous_rr = rr

    elif panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_SW:
        rr_list_vtotal = set()
        # VTotal
        mmio_output = etl_parser.get_mmio_data(timing_offsets.VTotal, is_write=True, start_time=start_timestamp,
                                               end_time=end_timestamp)
        logging.info(f"Reading info from Vtotal reg Addr:0x%X" % timing_offsets.VTotal)
        if mmio_output is not None:
            previous_rr = 0
            for mmio_data in mmio_output:
                timing_info = adapter.regs.get_timing_info(panel.transcoder_type,
                                                           TimingOffsetValues(VTotal=mmio_data.Data))
                rr = round(float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (timing_info.VTotal + 1)), 3)
                rr_list_vtotal.add(rr)
                logging.debug(
                    f"vtotal reg value: {timing_info.VTotal} calculated rr : {rr} time:{tstamp(mmio_data.TimeStamp)}s")
                if previous_rr != rr:
                    rr_change_list.append((mmio_data.TimeStamp, round(rr, 2)))
                    logging.info(f"RR programming of {rr}Hz detected on Vtotal at {mmio_data.TimeStamp}s")
                previous_rr = rr

    else:
        logging.error("Panel rr switch method is neither VTOTAL HW or VTOTAL SW")
        gdhm.report_driver_bug_os("[OsFeatures][BFR] Panel rr switch method is neither VTOTAL HW or VTOTAL SW")

    return rr_change_list


##
# @brief        Function to enable dynamic RR in the panel
# @param[in]    panel object of the targeted display
# @return       None
def set_dynamic_rr(panel: Panel):
    display_config_ = display_config.DisplayConfiguration()
    native_mode = common.get_display_mode(panel.target_id)
    native_mode.refreshRate = panel.max_rr // 2
    DYNAMIC_RR = 1
    native_mode.rrMode = DYNAMIC_RR
    if not display_config_.set_mode(native_mode):
        logging.info(f"Unable to set to Dynamic RR mode with RR {native_mode.refreshRate}")
        # @todo Trying to set virtual rr to maxRR/2-1 to check if the failure is becasue the panel max RR is a
        #  floating point number for eg. if panel maxRR is 239.5Hz, panel.maxRR will be rounded to 240 and setting to
        #  120 in virtualRR will fail.
        native_mode.refreshRate = panel.max_rr // 2 - 1
        if not display_config_.set_mode(native_mode):
            logging.error("Unable to set to Dynamic RR mode")
            gdhm.report_driver_bug_os("[OsFeatures][BFR] Unable to set to Dynamic RR mode")
            return False
    logging.info(f"Successfully Applied Dynamic RR with RR {native_mode.refreshRate}")
    return True


##
# @brief        Function to check bfr support from enumerated driver modes
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    negative True if negative test, False otherwise
# @return       None
def check_bfr_mode_enumeration(adapter, panel, negative=False):
    if not etl_tracer.stop_etl_tracer():
        logging.error("Failed to stop ETL capture")
        return False
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(
            test_context.LOG_FOLDER, 'GfxTraceBeforeDriverRestart.' + str(time.time()) + '.etl')
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return False
    time.sleep(2)

    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("\tFailed to restart display driver")
        return False
    logging.info("Driver restarted successfully")

    if etl_tracer.stop_etl_tracer() is False:
        logging.error("Failed to stop ETL Tracer")
        return False
    logging.info("ETL capture stopped successfully")

    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        file_name = 'GfxTraceDuringDriverRestart-' + str(time.time()) + '.etl'
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    bfr_config = etl_parser.EtlParserConfig()
    bfr_config.commonData = True

    if etl_parser.generate_report(etl_file_path, bfr_config) is False:
        logging.error("\tFailed to generate ETL report")
        return False

    reported_modes = etl_parser.get_event_data(etl_parser.Events.TRANSLATED_OS_MODE)
    rrswitch_fixed_caps = etl_parser.get_event_data(etl_parser.Events.RR_SWITCH_CAPS_FIXED_RXCAPS)
    if rrswitch_fixed_caps is None:
        logging.error("No event found with RR Switch caps fixed")
        gdhm.report_driver_bug_os("[OsFeatures][BFR] No event found with RR Switch caps fixed")
        return False
    vbi_masking_factor = 1
    for caps in rrswitch_fixed_caps:
        # Port will have value like DP_A, DP_B
        # SinkType will have value like eDP, DP
        # Transcoder will have value like A, B
        if(((panel.is_lfp and caps.SinkType[1:] == panel.port.split('_')[0]) or (caps.SinkType == panel.port.split('_')[0])) and caps.Port.split('_')[1] == panel.transcoder):
            if caps.VbiMasking:
                vbi_masking_factor = caps.VbiMaskingFactor
                break

    virtual_rr_support = False
    for i, mode in enumerate(reported_modes):
        if int(mode.TargetId) != panel.target_id:
            continue
        rr = round((mode.DotClock / (mode.HTotal*mode.VTotal)), 2)
        min_rr = round(mode.VSyncMinRR/1000, 2)
        logging.debug(f"Mode {i+1} : {mode.HActive}x{mode.VActive}@{rr} VsyncMinRR: {min_rr}, VirtualRRSupport:{mode.IsVirtualRRSupported}")
        logging.debug(f"Mode = {mode}")
        if not virtual_rr_support and mode.IsPreferred:
            virtual_rr_support = mode.IsVirtualRRSupported
            logging.info(f"Virtual RR supported Mode {i+1} : {mode.HActive}x{mode.VActive}@{rr} MinRR: {min_rr}, "
                         f"VirtualRRSupport:{mode.IsVirtualRRSupported}")
        if mode.IsVirtualRRSupported:
            expected_vsync_minRR = panel.vrr_caps.vrr_min_rr/vbi_masking_factor
            if abs(expected_vsync_minRR-min_rr) > 1:
                logging.error(f"Reported minRR is different from expected, Reported{min_rr} expected:{expected_vsync_minRR}")
                gdhm.report_driver_bug_os(f"[OsFeatures][BFR] Reported minRR is different from expected")
                return False
    if not virtual_rr_support and negative is False:
        logging.error("VirtualRRSupport not reported for any mode by OS")
        gdhm.report_driver_bug_os("[OsFeatures][BFR] VirtualRRSupport not reported for any mode by OS")
        return False
    if virtual_rr_support and negative:
        logging.error("VirtualRRSupport reported for any mode by driver for negative panel")
        gdhm.report_driver_bug_os("[OsFeatures][BFR] VirtualRRSupport reported for any mode by driver for negative panel")
        return False
    return True


##
# @brief        Function to enable native mode static RR in the panel
# @param[in]    panel Panel
# @return       None
def set_static_rr(panel: Panel):
    display_config_ = display_config.DisplayConfiguration()
    native_mode = display_config_.get_native_mode(panel.target_id)
    if native_mode is None:
        logging.error(f"Failed to get native mode for {panel.target_id}")
        return False
    static_mode = display_config_.get_current_mode(panel.target_id)
    static_mode.refreshRate = native_mode.refreshRate
    STATIC_RR = 0
    static_mode.rrMode = STATIC_RR
    if not display_config_.set_mode(static_mode):
        logging.error("Unable to set to Static RR mode")
        gdhm.report_driver_bug_os("[OsFeatures][BFR] Unable to set to Static RR mode")
        return False
    logging.info("Successfully Applied Static RR")
    return True


##
# @brief        Function to see if the current mode is dynamic RR in the panel
# @param[in]    panel Panel
# @return       None
def is_dynamic_rr(panel: Panel):
    display_config_ = display_config.DisplayConfiguration()
    current_mode = display_config_.get_current_mode(panel.target_id)
    DYNAMIC_RR = 1
    if current_mode.rrMode == DYNAMIC_RR:
        return True
    return False


##
# @brief        Function to enable BFR in external panel
# @return       status : Boolean
def enable():
    html.step_start(f"Enabling BFR for external panel")
    reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                             reg_path=r"SYSTEM\CurrentControlSet\Control")
    if registry_access.write(args=reg_args, reg_name="EnableVirtualRefreshRateOnExternalMonitor",
                             reg_type=registry_access.RegDataType.DWORD,
                             reg_value=1,
                             sub_key=r"GraphicsDrivers\DMM") is False:
        logging.error("\tFailed to update EnableVirtualRefreshRateOnExternalMonitor registry")
        gdhm.report_driver_bug_os("[OsFeatures][BFR] Failed to update EnableVirtualRefreshRateOnExternalMonitor registry")
        return False
    for adapter in dut.adapters.values():
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error("\tFailed to restart display driver after enabling BFR in external panel")
            return False
    logging.info("Enabled BFR in external panel using Regkey")
    return True

##
# @brief        Function to get the modeset RR using IGCL
# @param[in]    target_id : Target ID of the panel
# @return       Modeset RR
def __get_modeset_rr(adapter: Adapter, panel: Panel):
    # Fetching the current modeset from IGCL instead of QDC call as driver will consider the max RR as modeset RR.
    # For eg: If panel RR is 60-165 and we apply dynamic RR of 82-164, the modeset RR from driver will be 165 whereas
    # QDC call would return 164.
    if adapter.name not in PRE_GEN_13_PLATFORMS:
        displayProperties = control_api_args.ctl_display_properties_t()
        if control_api_wrapper.get_display_properties(displayProperties, panel.target_id):
            logging.info(f"Modeset RR: {displayProperties.Display_Timing_Info.RefreshRate}")
        return displayProperties.Display_Timing_Info.RefreshRate
    else:
        current_mode = __display_config.get_current_mode(panel.display_info.DisplayAndAdapterInfo)
        assert current_mode is not None, "API get_current_mode() Failed (Test Issue)"
        return current_mode.refreshRate*2

