########################################################################################################################
# @file         hrr.py
# @brief        Contains APIs to enable, disable and verify HRR
#
# @author       Rohit Kumar
########################################################################################################################

import logging
from typing import List, Union

import Libs.Core.flip as flip
from DisplayRegs.DisplayOffsets import PsrOffsetValues
from Libs.Core import etl_parser
from Libs.Core.logger import gdhm, html
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Modules import common, dut
from Tests.PowerCons.Modules.dut_context import Adapter, Panel
from registers.mmioregister import MMIORegister

__DMC_EVT_CTL_1_DISABLED = 0x0
__DMC_EVT_HTP_1_DISABLED = 0x0
__DMC_EVT_CTL_1_ENABLED = 0xC0033200
__DMC_EVT_HTP_1_ENABLED = 0x312C3100
__DMC_RAM_HALF_RATE_CURRENT_STATE_DISABLED = 0x0
__DMC_CHICKEN_HRR_ENABLED_MASK = 0x80000000
__DMC_CHICKEN_BUSY_BIT_ENABLED_MASK = 0x40000000
__PIPE_DMC_CHICKEN_2_EXECUTING_HRR = 0x1

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.vbiData = 1
ETL_PARSER_CONFIG.interruptData = 1
VBLANK_MAX_DURATION = 0xFFFFFFFF
mpo_flipq = flip.MPO()


##
# @brief        This class contains Gen11 Hrr Regs
class Gen11HrrRegs:
    DMC_CHICKEN = 0x8F080
    DMC_EVT_CTL_1 = 0x8F038
    DMC_EVT_HTP_1 = 0x8F008
    DMC_RAM_HALF_RATE_CURRENT_STATE = 0x80058
    QUEUE_PLANE_SURF_1_A = 0x80054
    QUEUE_PLANE_SURF_6_A = 0x80050


##
# @brief        This class contains Gen12 Hrr Regs
class Gen12HrrRegs(Gen11HrrRegs):
    DMC_RAM_HALF_RATE_CURRENT_STATE = 0x800C4
    QUEUE_PLANE_SURF_1_A = 0x800CC
    QUEUE_PLANE_SURF_6_A = 0x800C8


##
# @brief        This class contains Gen13 Hrr Regs
class Gen13HrrRegs(Gen11HrrRegs):
    ##
    # @brief        Initializes the data members of Gen13HrrRegs
    # @param[in]    pipe string, pipe of the panel
    def __init__(self, pipe):
        if pipe == 'A':
            self.DMC_CHICKEN = 0x5f080
            self.PIPE_DMC_CHICKEN_2 = 0x5f084
        elif pipe == 'B':
            self.DMC_CHICKEN = 0x5f480
            self.PIPE_DMC_CHICKEN_2 = 0x5f484
        elif pipe == 'C':
            self.DMC_CHICKEN = 0x5f880
            self.PIPE_DMC_CHICKEN_2 = 0x5f884
        elif pipe == 'D':
            self.DMC_CHICKEN = 0x5fc80
            self.PIPE_DMC_CHICKEN_2 = 0x5fc84


##
# @brief        Exposed API to enable HRR
# @param[in]    adapter String, gfx adapter index
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
def enable(adapter: Adapter) -> bool:
    assert adapter

    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        logging.info(f"HRR is not supported on {adapter.name}")
        return True

    html.step_start(f"Disabling OS FlipQ on {adapter.name}")
    mpo_flipq.enable_disble_os_flipq(True, adapter.gfx_index)

    display_feature_control = registry.DisplayFeatureControl(adapter.gfx_index)
    if display_feature_control.disable_hrr != 0:
        display_feature_control.disable_hrr = 0
        status = display_feature_control.update(adapter.gfx_index)
        if status is False:
            logging.error(f"\tFAILED to enable HRR from DisplayFeatureControl registry on {adapter.name}")
            html.step_end()
            return False

    logging.info(f"\tPASS: Enabled HRR from DisplayFeatureControl registry on {adapter.name}")
    html.step_end()
    return True


##
# @brief        Exposed API to disable HRR
# @param[in]    adapter String, gfx adapter index
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
def disable(adapter: Adapter) -> bool:
    assert adapter

    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        logging.info(f"HRR is not supported on {adapter.name}")
        return True

    display_feature_control = registry.DisplayFeatureControl(adapter.gfx_index)
    if display_feature_control.disable_hrr != 1:
        display_feature_control.disable_hrr = 1
        status = display_feature_control.update(adapter.gfx_index)
        if status is False:
            logging.error(f"\tFailed to disable HRR from DisplayFeatureControl registry on {adapter.name}")
            return False
    logging.info(f"\tPASS: Disabled HRR from DisplayFeatureControl registry on {adapter.name}")

    html.step_start(f"Enabling OS FlipQ back on {adapter.name}")
    mpo_flipq.enable_disble_os_flipq(False, adapter.gfx_index)
    html.step_end()
    return True


##
# @brief        Exposed API to enable D13 HRR
# @param[in]    adapter String, gfx adapter index
# @return       status Boolean, True if successful and restart needed, None no action required, False otherwise
def enable_d13_hrr(adapter: Adapter):
    return __configure_d13_hrr_status(adapter, enable_hrr=True)


##
# @brief        Exposed API to disable D13 HRR
# @param[in]    adapter String, gfx adapter index
# @return       status Boolean, True if successful and restart needed, None no action required, False otherwise
def disable_d13_hrr(adapter: Adapter):
    return __configure_d13_hrr_status(adapter, enable_hrr=False)


##
# @brief        Private API to configure status of D13 HRR
# @param[in]    adapter String, gfx adapter index
# @param[in]    enable_hrr bool, True to enable HRR and False to disable HRR
# @return       status Boolean, True if successful and restart needed, None no action required, False otherwise
def __configure_d13_hrr_status(adapter: Adapter, enable_hrr: bool):
    sku_name = SystemInfo().get_sku_name(adapter.gfx_index)
    if adapter.name not in ['ADLP'] or sku_name in ['ADLN', 'RPLP']:
        logging.info(f"HRR in D13 way is not supported for {adapter.name} (SKU= {sku_name})")
        return None
    status_str = "Enable" if enable_hrr else "Disable"
    html.step_start(f"{status_str} HRR on ADLP (Temp Approach for MSFT) on {adapter.name}")
    reg_key = registry.RegKeys.HRR.FORCE_ENABLE_D13_HRR
    value = registry.RegValues.ENABLE if enable_hrr else registry.RegValues.DISABLE
    status = registry.write(adapter.gfx_index, reg_key, registry.registry_access.RegDataType.DWORD, value)
    if status is False:
        logging.error(f"\tFAILED to {status_str} HRR from registry {reg_key}= {value} on {adapter.name}")
        html.step_end()
        return False

    if status is True:
        logging.info(f"\tSuccessfully {status_str} HRR from registry {reg_key}= {value} on {adapter.name}")
    else:
        logging.info(f"\tHRR registry is already {reg_key}= {value} on {adapter.name}")

    html.step_end()
    return status


##
# @brief        Exposed API to verify HRR
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @param[in]    etl_path String path to etl file
# @param[in]    media_fps float
# @param[in]    etl_started_before_video bool, True, if ETL trace started before video,
#                                            False, if video is already playing and new ETL has started
# @return       status Boolean True if operation is successful, False otherwise
def verify(adapter: Adapter, panel: Panel, etl_path: str, media_fps: float, etl_started_before_video=True) -> bool:
    assert adapter
    assert panel
    assert etl_path
    assert media_fps

    status = True
    html.step_start(f"Verifying HRR for {media_fps}fps on {panel.port}")

    logging.info(f"\tGenerating EtlParser Report for {etl_path}")
    if etl_parser.generate_report(etl_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        html.step_end()
        return False
    logging.info("\tSuccessfully generated ETL Parser report")
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
    # if video is already playing, CheckPresentDuration will not happen
    if etl_started_before_video:
        status &= __verify_present_duration(panel, media_fps)

    hrr_active_regions = __get_hrr_active_region(adapter, panel)
    logging.info(f"HRR Active Region: {hrr_active_regions}")

    # HRR should not get enabled if FPS is in supported RR range
    if (panel.drrs_caps.min_rr * dmrrs.FRACTIONAL_RR_FACTOR) <= media_fps <= panel.drrs_caps.max_rr:
        if hrr_active_regions is not None:
            logging.error("\tFAIL: HRR is getting enabled for {0}fps in {1}Hz-{2}Hz panel".format(
                media_fps, panel.drrs_caps.min_rr, panel.drrs_caps.max_rr))
            gdhm.report_driver_bug_os("[OsFeatures][HRR] HRR is getting enabled for {0}fps in {1}Hz-{2}Hz panel".format(
                media_fps, panel.drrs_caps.min_rr, panel.drrs_caps.max_rr))
            html.step_end()
            return False
        logging.info("\tPASS: HRR is not getting enabled for {0}fps in {1}Hz-{2}Hz panel".format(
            media_fps, panel.drrs_caps.min_rr, panel.drrs_caps.max_rr))
        html.step_end()
        return True

    # For positive HRR case, make sure at least one HRR active region is present in ETL
    if hrr_active_regions is None:
        logging.error("\tFAIL: No HRR active region found in ETL")
        gdhm.report_driver_bug_os("[OsFeatures][HRR] HRR is not getting enabled")
        html.step_end()
        return False

    status &= __verify_hrr_switch_with_duration_flip(adapter, panel)
    status &= __verify_mmio_programming(adapter, panel)
    status &= dmrrs.verify_clock_programming(adapter, panel, media_fps, is_hrr_enabled=True)
    status &= __check_deep_sleep_disable(adapter, panel)

    for (start, end) in hrr_active_regions:
        # Skipping verification if HRR active region is less then 5 flips
        if (end - start) / 1000 < (5 * 1 / media_fps):
            continue
        status &= __verify_incoming_flips(panel, start, end, media_fps)
        status &= __verify_vbi(adapter, panel, start, end, media_fps)
    html.step_end()
    return status


##
# @brief        Helper API to verify HRR MMIO programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @return       status Boolean, True if verification is successful, False otherwise
def __verify_mmio_programming(adapter: Adapter, panel: Panel):
    html.step_start(f"Verifying MMIO programming for {panel.port}")
    status = True
    regs = Gen11HrrRegs()
    if adapter.name in common.GEN_12_PLATFORMS:
        regs = Gen12HrrRegs()
    elif adapter.name in common.GEN_13_PLATFORMS + common.GEN_14_PLATFORMS:
        regs = Gen13HrrRegs(panel.pipe)

    # EVT_CTL and EVT_HTP are not programmed from Gen12+
    if adapter.name in common.PRE_GEN_12_PLATFORMS:
        dmc_evt_htp_1 = etl_parser.get_mmio_data(regs.DMC_EVT_HTP_1, is_write=True)
        if dmc_evt_htp_1 is None:
            logging.error("No write event for DMC_EVT_HTP_1 register found in ETL")
            gdhm.report_driver_bug_os("[OsFeatures][HRR] No write event for DMC_EVT_HTP_1 register found in ETL")
            html.step_end()
            return False

        sub_status = False
        for mmio_data in dmc_evt_htp_1:
            if mmio_data.Data == __DMC_EVT_HTP_1_ENABLED:
                logging.info("\tPASS: DMC_EVT_HTP_1 Expected= {0}, Actual= {0}".format(hex(__DMC_EVT_HTP_1_ENABLED)))
                sub_status = True
                break

        if sub_status is False:
            logging.error("\tDMC_EVT_HTP_1 is not getting enabled")
            gdhm.report_driver_bug_os("[OsFeatures][HRR] DMC_EVT_HTP_1 is not getting enabled")

        status &= sub_status

        dmc_evt_ctl_1 = etl_parser.get_mmio_data(regs.DMC_EVT_CTL_1, is_write=True)
        if dmc_evt_ctl_1 is None:
            logging.error("No write event for DMC_EVT_CTL_1 register found in ETL")
            gdhm.report_driver_bug_os("[OsFeatures][HRR] No write event for DMC_EVT_CTL_1 register found in ETL")
            html.step_end()
            return False

        sub_status = False
        for mmio_data in dmc_evt_ctl_1:
            if mmio_data.Data == __DMC_EVT_CTL_1_ENABLED:
                logging.info("\tPASS: DMC_EVT_CTL_1 Expected= {0}, Actual= {0}".format(hex(__DMC_EVT_CTL_1_ENABLED)))
                sub_status = True
                break

        if sub_status is False:
            logging.error("DMC_EVT_CTL_1 is not getting enabled")
            gdhm.report_driver_bug_os("[OsFeatures][HRR] DMC_EVT_CTL_1 is not getting enabled")

        status &= sub_status

    # check HRR is not enabled when DMC is executing HRR (DMC has separate register from gen13+)
    sub_status = True
    if adapter.name in common.PRE_GEN_13_PLATFORMS:
        dmc_chicken = etl_parser.get_mmio_data(regs.DMC_CHICKEN, is_write=True)
        if dmc_chicken is None:
            logging.error("No write event for DMC_CHICKEN register found in ETL")
            gdhm.report_driver_bug_os("[OsFeatures][HRR] No write event for DMC_CHICKEN register found in ETL")
            html.step_end()
            return False
        for mmio_data in dmc_chicken:
            if mmio_data.Data & __DMC_CHICKEN_BUSY_BIT_ENABLED_MASK == __DMC_CHICKEN_BUSY_BIT_ENABLED_MASK:
                sub_status = False
                break
    else:
        hrr_active_regions = __get_hrr_active_region(adapter, panel)
        for (start, end) in hrr_active_regions:
            pipe_dmc_output = etl_parser.get_mmio_data(regs.PIPE_DMC_CHICKEN_2, None, start, end)
            if pipe_dmc_output is None:
                logging.warning(f"No event for PIPEDMC_CHICKEN_2_{panel.pipe} register found in ETL")
            else:
                # check only at HRR exit because busy bit can be set in between when HRR is enabled
                if pipe_dmc_output[-1].Data & __PIPE_DMC_CHICKEN_2_EXECUTING_HRR == __PIPE_DMC_CHICKEN_2_EXECUTING_HRR:
                    # Bit 0 of register PIPEDMC_CHICKEN_2
                    logging.info(f"\tOffset= {hex(pipe_dmc_output[-1].Offset)}, "
                                 f"Value= {hex(pipe_dmc_output[-1].Data)} at {pipe_dmc_output[-1].TimeStamp}")
                    logging.error(f"\tHRR got disabled by driver when PIPEDMC_CHICKEN_2 is Executing HRR (Unexpected)")
                    sub_status = False
                    break

    if sub_status is True:
        logging.info("\tPASS: No DMC_CHICKEN register write detected when DMC is executing HRR")
    else:
        logging.error("\tFAIL: DMC_CHICKEN register write detected when DMC is executing HRR")
        gdhm.report_driver_bug_os("[OsFeatures][HRR] DMC_CHICKEN register write detected when DMC is executing HRR")

    status &= sub_status
    html.step_end()
    return status


##
# @brief        Helper API to verify GfxCheckPresentDurationSupport DDI calls
# @param[in]    panel Panel
# @param[in]    media_fps float
# @return       status Boolean, True if operation is successful, False otherwise
def __verify_present_duration(panel: Panel, media_fps: float) -> bool:
    status = True
    # With HRR, 30-60 panel can report 15-60 as supported duration
    min_rr = (panel.drrs_caps.min_rr * dmrrs.FRACTIONAL_RR_FACTOR) / 2

    # Consider fractional RR, (min rr * 0.999)
    supported_min_rr = min_rr * dmrrs.FRACTIONAL_RR_FACTOR

    supported_max_rr = panel.drrs_caps.max_rr

    expected_incoming_fps = media_fps
    while expected_incoming_fps < min_rr:
        expected_incoming_fps += media_fps

    logging.info("\tVerifying GfxCheckPresentDurationSupport data")
    check_present_duration_output = etl_parser.get_event_data(etl_parser.Events.CHECK_PRESENT_DURATION_SUPPORT)
    if check_present_duration_output is None:
        if panel.bfr_caps.is_bfr_supported or media_fps == dmrrs.MediaFps.FPS_59_940:
            logging.info("No data found for GfxCheckPresentDurationSupport for BFR panel or media FPS 59.940")
            return True
        gdhm.report_driver_bug_os(
            "[OsFeatures][HRR] No data found for GfxCheckPresentDurationSupport for Non-BFR panel")
        logging.error("No data found for GfxCheckPresentDurationSupport for Non-BFR panel")
        return False

    for event_data in check_present_duration_output:
        if event_data.IsDataProvided is False:
            logging.error("\t\t{0}".format(event_data))
            logging.error("\t\tUnserviced GfxCheckPresentDurationSupport call found")
            gdhm.report_driver_bug_os("[OsFeatures][HRR] Unserviced GfxCheckPresentDurationSupport call found")
            status = False

        requested_duration = common.duration_to_hz(event_data.DesiredPresentDuration)
        supported_duration_smaller = common.duration_to_hz(event_data.ClosestSmallerDuration)
        supported_duration_larger = common.duration_to_hz(event_data.ClosestLargerDuration)

        logging.info(
            "\t\tTimeStamp= {0}: Requested RR= {1}, Reported RR Range({2}, {3})".format(
                event_data.TimeStamp, requested_duration, supported_duration_larger, supported_duration_smaller))

        # Make sure reported duration is within supported range
        if supported_duration_larger < supported_min_rr or supported_duration_smaller > supported_max_rr:
            logging.error("\t\tDriver is reporting duration outside of supporting range")
            gdhm.report_driver_bug_os("[OsFeatures][HRR] Driver is reporting duration outside of supporting range")
            status = False

    return status


##
# @brief        Helper API to verify incoming flips
# @param[in]    panel object, Panel
# @param[in]    start float, start timestamp of HRR active region
# @param[in]    end float
# @param[in]    fps int
# @return       status, Boolean, True if verification is successful, False otherwise
def __verify_incoming_flips(panel: Panel, start: float, end: float, fps: float):
    html.step_start(f"Verifying incoming flips from OS with HRR active region during [{start} - {end}]")
    expected_incoming_fps = fps
    while expected_incoming_fps < (panel.drrs_caps.min_rr * dmrrs.FRACTIONAL_RR_FACTOR) / 2:
        expected_incoming_fps += fps

    flip_data = etl_parser.get_flip_data(f"PIPE_{panel.pipe}", start_time=start, end_time=end)
    if flip_data is None:
        logging.error("\tFAIL: No Flip Data found in HRR active region")
        html.step_end()
        return False
    logging.info(f"\tNumber of incoming flips= {len(flip_data)}")
    durations = {}
    for flip in flip_data:
        if flip.Duration is not None:
            if flip.Duration in durations.keys():
                durations[flip.Duration] += 1
            else:
                durations[flip.Duration] = 1

    if bool(durations):
        logging.info(f"\tMPO3 Flip Duration= {durations}")

    incoming_fps = set()
    for duration in durations.keys():
        if duration == 0:
            continue
        d_to_fps = common.duration_to_hz(duration)
        incoming_fps.add(d_to_fps)
        if expected_incoming_fps - drrs.FPS_TOLERANCE <= d_to_fps <= expected_incoming_fps + drrs.FPS_TOLERANCE:
            logging.info(f"\tIncoming FPS Expected= {expected_incoming_fps}, Actual= {d_to_fps}")
            html.step_end()
            return True

    gdhm.report_driver_bug_os("[OsFeatures][HRR] Incoming FPS is not as expected with HRR enabled")
    logging.error(f"\tIncoming FPS Expected= {expected_incoming_fps}, Actual= {incoming_fps}")
    html.step_end()
    return False


##
# @brief        Helper API to verify VBI
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    start float
# @param[in]    end float
# @param[in]    fps float
# @return       status Boolean, True if verification is successful, False otherwise
def __verify_vbi(adapter: Adapter, panel: Panel, start: float, end: float, fps: float) -> bool:
    html.step_start(f"Verifying VBI rate with in HRR active region during [{start} - {end}]")
    expected_fps = fps

    while expected_fps < (panel.drrs_caps.min_rr * dmrrs.FRACTIONAL_RR_FACTOR) / 2:
        expected_fps += fps

    is_psr2_expected = False
    psr2_offsets = adapter.regs.get_psr_offsets(panel.transcoder_type)
    offset = psr2_offsets.Psr2CtrlReg
    if adapter.name not in common.PRE_GEN_14_PLATFORMS:
        offset = 0x60902
        if panel.transcoder == 'B':
            offset = 0x61902
    psr2_ctl_data = etl_parser.get_mmio_data(offset)
    if psr2_ctl_data is not None:
        for data in psr2_ctl_data:
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                data = data.Data
            else:
                data = data.Data << 16
            psr2_ctl = adapter.regs.get_psr_info(panel.transcoder_type, PsrOffsetValues(Psr2CtrlReg=data))
            if psr2_ctl.Psr2Enable == 1:
                is_psr2_expected = True
                break

    # if psr2 is enabled, then for end boundary region there would be glitch due to Hw which is expected
    # below logic will update the region till non-zero duration is there from OS.
    if is_psr2_expected:
        flip_data = etl_parser.get_flip_data('PIPE_' + panel.pipe, start_time=start, end_time=end)
        previous_flip = None
        for flip in flip_data:
            # first iteration with non-zero duration
            if previous_flip is None:
                previous_flip = flip
                continue

            # when there is change in duration, update end time stamp and break the loop
            if flip.Duration != previous_flip.Duration:
                end = previous_flip.TimeStamp
                break
            previous_flip = flip
    # adding CTL interrupt check as seen sporadically got disable keep phase call.
    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                   etl_parser.InterruptType.CRTC_VSYNC, start_timestamp=start,
                                                   end_timestamp=end)
    if interrupt_data is not None:
        for interrupt in interrupt_data:
            if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.DISABLE_KEEP_PHASE]:
                end = interrupt.TimeStamp
                break

    logging.info(f"\tFetching VBI data from {start} to {end}")
    vbi_data = etl_parser.get_vbi_data(f"PIPE_{panel.pipe}", start, end)
    if vbi_data is None:
        logging.error("\tFAIL: No VBI Data found in HRR region")
        gdhm.report_driver_bug_os("[OsFeatures][HRR] No VBI data found in HRR region")
        html.step_end()
        return False

    report_to_gdhm = set()
    actual_fps_list = []
    final_status = True
    total_vbi = len(vbi_data)
    prev_vbi = None
    logging.info(f"\tNumber of VBIs reported to OS= {total_vbi}")
    for vbi in vbi_data:
        # handle first vbi
        if prev_vbi is None:
            prev_vbi = vbi
            continue
        logging.debug(f"\tCalculating VBI rate between two consecutive VBIs [{prev_vbi.TimeStamp} to {vbi.TimeStamp}]")
        actual_fps = round(1000.0 / float(vbi.TimeStamp - prev_vbi.TimeStamp), 3)
        logging.debug(f"\t\tVBI rate Expected= {expected_fps}, Actual= {actual_fps}")
        actual_fps_list.append(actual_fps)
        prev_vbi = vbi

    # The average of 3 actual FPS must be taken for calculation of actual FPS
    average_fps = [sum(actual_fps_list[i:i + 3]) / len(actual_fps_list[i:i + 3]) for i in
                   range(0, len(actual_fps_list))]
    for each_average_fps in average_fps:
        # tolerance is kept 1.0 ms(same as DiAna NotifyVSyncInterval) because RR is calculated from VBI interval
        vbi_status = common.compare_with_tolerance(each_average_fps, expected_fps, 1.0)
        if not vbi_status:
            logging.error(f"\t\tVBI rate Expected= {expected_fps}, Actual_After_Average= {round(each_average_fps, 3)}")
            report_to_gdhm.add(f"[OsFeatures][HRR] Incorrect VBI rate found")
            final_status = False
        else:
            logging.info(f"\t\tVBI rate Expected= {expected_fps}, Actual_After_Average= {round(each_average_fps, 3)}")

    for report in report_to_gdhm:
        gdhm.report_driver_bug_os(report)
    html.step_end()
    return final_status


##
# @brief        Helper API to get HRR active region
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @return       output, list, list of tuples having HRR start/end time
def __get_hrr_active_region(adapter: Adapter, panel: Panel) -> Union[None, List]:
    regs = Gen11HrrRegs()
    if adapter.name in common.GEN_12_PLATFORMS:
        regs = Gen12HrrRegs()
    if adapter.name in common.GEN_13_PLATFORMS + common.GEN_14_PLATFORMS:
        regs = Gen13HrrRegs(panel.pipe)

    dmc_chicken = etl_parser.get_mmio_data(regs.DMC_CHICKEN, is_write=True)
    if dmc_chicken is None:
        return None

    start_time = None
    output = []
    for index, mmio_data in enumerate(dmc_chicken):
        if mmio_data.Data & __DMC_CHICKEN_HRR_ENABLED_MASK == __DMC_CHICKEN_HRR_ENABLED_MASK:
            start_time = mmio_data.TimeStamp
        else:
            # if HRR is already enabled then start time will be None, make it 0.0 for start of ETL
            if start_time is None:
                start_time = 0.0
            output.append((start_time, mmio_data.TimeStamp))
            start_time = None

        # if ETL is having duration flips till the end, then HRR will be enabled
        # In this case, test will consider end_time till end of the ETL which is required for further verification
        if (index == len(dmc_chicken) - 1) and (start_time is not None):
            etl_end_time = etl_parser.get_event_data(etl_parser.Events.ETL_DETAILS)[0].EndTime
            output.append((start_time, etl_end_time))

    return None if len(output) == 0 else output


##
# @brief        Helper API to verify PSR2 Entry/Exit sequence in HRR
# @param[in]    adapter Adapter
# @param[in]    panel
# @return       status
def __verify_hrr_entry_exit_sequence(adapter, panel):
    offset = 0x60902
    psr_regs = adapter.regs.get_psr_offsets(panel.transcoder_type)
    psr2_ctl_offset = psr_regs.Psr2CtrlReg
    psr2_ctl = MMIORegister.get_instance("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name)
    previous_time = 0
    psr2_val, psr2_mmio_ctl = 0, 0
    output = __get_hrr_active_region(adapter, panel)
    for duration_index in range(0, len(output)):
        time1 = output[duration_index][0]
        time2 = output[duration_index][1]

        # To check PSR sequence at HRR Entry, suppose (x,y), (x1,y1) and (x2,y2) are the HRR active regions, the first
        # entry sequence will be check in region (0 to x) and second entry sequence will be checked in region (y to x1)
        # then (y1 to x2) and so on. That is why, previous_time is initialized with value 0, and is further incremented.
        psr2_mmio_ctl_output_hrr_entry = etl_parser.get_mmio_data(psr2_ctl.offset, is_write=True,
                                                                  start_time=previous_time, end_time=time1)
        if adapter.name not in common.PRE_GEN_14_PLATFORMS:
            if panel.transcoder == 'B':
                offset = 0x61902
            # from GEN14+, Driver will write first 16 bits & last 16 bit's separately to avoid synchronization issues
            psr2_mmio_ctl = etl_parser.get_mmio_data(offset, is_write=True, start_time=previous_time, end_time=time1)
        previous_time = time2
        if (duration_index + 1) == len(output):
            time1 = None
        else:
            time1 = output[duration_index + 1][0]

        # To check PSR sequence at HRR Exit, suppose (x,y), (x1,y1) and (x2,y2) are the HRR active regions, the first
        # exit sequence will be checked in the region (y to x1) then (y1 to x2) and so on , but the last exit sequence
        # will be checked in (y1 to None). That is why, when len(active_region) is achieved time1 is set as None.
        psr2_mmio_ctl_output_hrr_exit = etl_parser.get_mmio_data(psr2_ctl.offset, is_write=True, start_time=time2,
                                                                 end_time=time1)
        if adapter.name not in common.PRE_GEN_14_PLATFORMS:
            psr2_val = etl_parser.get_mmio_data(offset, is_write=True, start_time=time2, end_time=time1)

        if psr2_mmio_ctl_output_hrr_entry is None:
            logging.warning(f"No MMIO output found for PSR2_STATUS_{panel.transcoder}")
            continue
        if psr2_mmio_ctl_output_hrr_exit is None:
            logging.warning(f"No MMIO output found for PSR2_STATUS_{panel.transcoder}")
            continue

        html.step_start(f"Verification for HRR Entry Sequence for {panel.port} on {adapter.gfx_index}")
        hrr_entry_count = 0
        mmio_len = len(psr2_mmio_ctl_output_hrr_entry)
        for index, mmio_data in (enumerate(psr2_mmio_ctl_output_hrr_entry)):
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                psr2_ctl.asUint = mmio_data.Data
            else:
                psr2_ctl.asUint = mmio_data.Data + (psr2_val[index].Data << 16)
            if psr2_ctl.asUint is None:
                continue
            if index == (mmio_len - 2) and psr2_ctl.psr2_enable == 0:
                logging.info(
                    f"PSR2 is disabled, Offset= {hex(mmio_data.Offset)} Value= {hex(mmio_data.Data)} at "
                    f"{mmio_data.TimeStamp}")
                hrr_entry_count += 1
            if index == (mmio_len - 1) and psr2_ctl.psr2_enable == 1 and psr2_ctl.idle_frame == 0:
                logging.info(
                    f"PSR2 Deep sleep is disabled,Offset= {hex(mmio_data.Offset)} Value= {hex(mmio_data.Data)} at "
                    f"{mmio_data.TimeStamp}")
                logging.info(
                    f"PSR2 is enabled, Offset={hex(mmio_data.Offset)}, Value= {hex(mmio_data.Data)} at "
                    f"{mmio_data.TimeStamp}")
                hrr_entry_count += 1
        if hrr_entry_count == 2:
            logging.info("HRR Entry Sequence Successful")
        else:
            logging.error("FAIL: HRR Entry Sequence Failed")

        html.step_start(f"Verification for HRR Exit Sequence for {panel.port} on {adapter.gfx_index}")
        hrr_exit_count = 0
        for index, mmio_data in enumerate(psr2_mmio_ctl_output_hrr_exit):
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                psr2_ctl.asUint = mmio_data.Data
            else:
                psr2_ctl.asUint = mmio_data.Data + (psr2_mmio_ctl[index] << 16)
            if psr2_ctl.asUint is None:
                continue
            if index == 0 and psr2_ctl.psr2_enable == 0:
                logging.info(
                    f"PSR2 is disabled, Offset= {hex(mmio_data.Offset)}, Value= {hex(mmio_data.Data)} at "
                    f"{mmio_data.TimeStamp}")
                hrr_exit_count += 1
            if index == 1 and psr2_ctl.idle_frame == 4 and psr2_ctl.psr2_enable == 1:
                logging.info(
                    f"PSR2 Deep sleep Idle frame enabled, Offset= {hex(mmio_data.Offset)}, Value= {hex(mmio_data.Data)}"
                    f" at {mmio_data.TimeStamp}")
                logging.info(
                    f"PSR2 is enabled, Offset= {hex(mmio_data.Offset)}, Value= {hex(mmio_data.Data)} at "
                    f"{mmio_data.TimeStamp}")
                hrr_exit_count += 1
        if hrr_exit_count == 2:
            logging.info("HRR Exit Sequence Successful")
        else:
            logging.error("FAIL: HRR Exit Sequence Failed")
            return False
        html.step_end()
    return True


##
# @brief        Helper API to check deep sleep is disabled in HRR active regions
# @param[in]    adapter Adapter, object
# @param[in]    panel Panel, object
# @return       status
def __check_deep_sleep_disable(adapter, panel):
    psr2_reg_data = None
    html.step_start("Verifying Deep Sleep is DISABLED in HRR Active regions")
    active_regions = __get_hrr_active_region(adapter, panel)
    if active_regions is None:
        html.step_end()
        return True

    psr2_ctl_offset = adapter.regs.get_psr_offsets(panel.transcoder_type).Psr2CtrlReg
    status = True
    for start, end in active_regions:
        logging.info(f"Checking Idle Frame counter for HRR active region from [{start} - {end}] ms")
        psr2_ctl_data = etl_parser.get_mmio_data(psr2_ctl_offset, start_time=start, end_time=end)
        if adapter.name not in common.PRE_GEN_14_PLATFORMS:
            psr2_reg_data = etl_parser.get_mmio_data(psr2_ctl_offset, start_time=start, end_time=end)
            offset = 0x60902
            if panel.transcoder == 'B':
                offset = 0x61902
            psr2_ctl_data = etl_parser.get_mmio_data(offset, start_time=start, end_time=end)
        if psr2_ctl_data is None and psr2_reg_data is None:
            logging.info(f"\tNo MMIO output found for PSR2_CTL_{panel.transcoder} ({hex(psr2_ctl_offset)})")
            continue

        is_deep_sleep_disabled = True
        for data in psr2_ctl_data:
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                val = data.Data
            else:
                val = (data.Data << 16) + psr2_reg_data[-1].Data
            psr2_ctl = adapter.regs.get_psr_info(panel.transcoder_type, PsrOffsetValues(Psr2CtrlReg=val))
            # if PSR2 CTL is disabled, IDLE frame update has no impact to driver behavior
            # IDLE frame has direct trigger based on ControlInterrupt. Driver will not check the CTL status
            # avoid deep sleep check if PSR2 CTL is disabled
            if psr2_ctl.Psr2Enable is False:
                continue
            if psr2_ctl.IdleFrames == 0:
                logging.debug(f"\tPSR2 CTL Offset= {hex(data.Offset)}, Value= {hex(data.Data)} at {data.TimeStamp} ms")
                logging.debug(f"\t\tPSR2 DeepSleep is disabled. IDLE FRAME Counter= {psr2_ctl.IdleFrames}")
            else:
                logging.info(f"\tPSR2 CTL Offset= {hex(data.Offset)}, Value= {hex(data.Data)} at {data.TimeStamp} ms")
                logging.error(f"\t\tPSR2 DeepSleep is NOT disabled. IDLE FRAME Counter= {psr2_ctl.IdleFrames}")
                is_deep_sleep_disabled = False

        if is_deep_sleep_disabled:
            logging.info("\tDeep Sleep is disabled in HRR active region")
        else:
            logging.error("\tDeep Sleep is NOT disabled in HRR active region")
            status = False

    if status is False:
        gdhm.report_driver_bug_os("[OsFeatures][HRR] Deep Sleep is NOT disabled in HRR active region", gdhm.Priority.P1)

    html.step_end()
    return status


##
# @brief        Helper API to check DMC chicken register is programmed immediately when duration is different
#               from prev Mpo3Flip to current Mpo3Flip for Non-PSR2 and sequence maintained for PSR2
# @note         This function will be called only when HRR is possible. So, whenever duration of current flip is
#               different from previous flip, HRR should get toggled(enable/disable).
#               Hence, only check if any write(hrr enable/ disable) happened in DMC register.
#               Proper RR verification in HRR region will be done separately
# @param[in]    adapter Adapter, object
# @param[in]    panel Panel, object
# @return       status
def __verify_hrr_switch_with_duration_flip(adapter: Adapter, panel: Panel):
    html.step_start("Verifying HRR switch happening exactly after duration flip is received from OS")
    is_psr2_expected = False

    psr2_regs = adapter.regs.get_psr_offsets(panel.transcoder_type)
    psr2_ctl_data = etl_parser.get_mmio_data(psr2_regs.Psr2CtrlReg)
    if adapter.name not in common.PRE_GEN_14_PLATFORMS:
        psr_offset = 0x60902
        if panel.transcoder == 'B':
            psr_offset = 0x61902
        psr2_ctl_data = etl_parser.get_mmio_data(psr_offset)
    else:
        psr_offset = psr2_regs.Psr2CtrlReg
    if psr2_ctl_data is not None:
        for data in psr2_ctl_data:
            if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                data = data.Data << 16
            else:
                data = data.Data
            psr2_ctl = adapter.regs.get_psr_info(panel.transcoder_type, PsrOffsetValues(Psr2CtrlReg=data))
            if psr2_ctl.Psr2Enable == 1:
                is_psr2_expected = True
                break

    flip_data = etl_parser.get_flip_data('PIPE_' + panel.pipe)
    if flip_data is None:
        logging.warning(f"\tNo flip data found for PIPE_{panel.pipe}")
        html.step_end()
        return None

    regs = Gen11HrrRegs()
    if adapter.name in common.GEN_12_PLATFORMS:
        regs = Gen12HrrRegs()
    if adapter.name in common.GEN_13_PLATFORMS + common.GEN_14_PLATFORMS:
        regs = Gen13HrrRegs(panel.pipe)

    previous_flip = None
    status = True
    for index, flip in enumerate(flip_data):
        expected_sequence = ['HrrSwitch']
        if is_psr2_expected:
            expected_sequence = ['Psr2CtlDisable', 'Psr2StatusIdle', 'HrrSwitch', 'Psr2CtlEnable']
            # in case of LRR2.0 panel. HRR will use VRR HW block. once we enable VRR HW block PSR should disable.
            # Gen14+ LRR2.0 not supported and Fixed RR can enable with PSR.
            if panel.lrr_caps.is_lrr_2_0_supported and adapter.name in common.PRE_GEN_14_PLATFORMS:
                expected_sequence = ['Psr2CtlDisable', 'Psr2StatusIdle', 'HrrSwitch']

        actual_sequence = []
        # first iteration
        if flip.Duration is not None and previous_flip is None:
            previous_flip = flip
            continue

        # when no change in duration, skip that iteration and go for next
        if flip.Duration == previous_flip.Duration:
            previous_flip = flip
            continue

        # when duration change from 0 -> Max and Max -> 0, skip that iteration and go for next
        if (flip.Duration == VBLANK_MAX_DURATION and previous_flip.Duration == 0) or \
                (flip.Duration == 0 and previous_flip.Duration == VBLANK_MAX_DURATION):
            previous_flip = flip
            continue
        # when duration change from non_zero -> Max skip that iteration and go for next
        if flip.Duration == VBLANK_MAX_DURATION and previous_flip.Duration != 0:
            previous_flip = flip
            continue
        # skip when flip duration change from 0--> min rr or min rr --> 0 duration.
        if (common.duration_to_hz(flip.Duration) == panel.min_rr and previous_flip.Duration == 0) or (
                flip.Duration == 0 and common.duration_to_hz(previous_flip.Duration) == panel.min_rr):
            previous_flip = flip
            continue

        # skip if no consecutive 10 flip with non-zero duration.
        no_consecutive_flip = False
        for ind in range(10):
            if flip_data[index + ind].Duration != flip.Duration:
                no_consecutive_flip = True
                break
        if no_consecutive_flip:
            continue

        logging.info(f"Current FlipDuration= {flip.Duration} at {flip.TimeStamp} ms, "
                     f"Previous FlipDuration= {previous_flip.Duration} at {previous_flip.TimeStamp} ms")
        is_sequence_followed = False
        for data in flip.MmioDataList:
            if is_sequence_followed:
                logging.debug("Sequence verified with change in duration, breaking loop of mmio for flip")
                break
            # ignore all offset except PSR2 and HRR
            if data.Offset not in [psr_offset, psr2_regs.Psr2StatusReg, regs.DMC_CHICKEN]:
                continue
            mmio_read_write = "Write" if data.IsWrite else "Read"
            logging.info(f"\tMMIO {mmio_read_write}: Offset= {hex(data.Offset)}= {hex(data.Data)} at {data.TimeStamp}")
            is_hrr_switch_valid = False
            if is_psr2_expected is False:
                if data.IsWrite is False:
                    continue
                if data.Offset == regs.DMC_CHICKEN:
                    actual_sequence.append("HrrSwitch")
            else:
                # HRR disable sequence in LRR 2.0 panel  HrrSwitch->Psr2CtlEnable
                if panel.lrr_caps.is_lrr_2_0_supported and previous_flip.Duration != 0 and flip.Duration == 0:
                    expected_sequence = ['HrrSwitch', 'Psr2CtlEnable']
                    # ignore all mmio except DMC chicken
                    if data.Offset != regs.DMC_CHICKEN:
                        continue
                    actual_sequence.append("HrrSwitch")
                    # With upcoming flips, Psr2CtlEnable (Threshold is within next 3 flips)
                    flip_count = index
                    threshold_flip_count = index + 6
                    while flip_count <= threshold_flip_count:
                        for mmio in flip_data[flip_count].MmioDataList:
                            # ignore all MMIOs except PSR2
                            if mmio.Offset not in [psr_offset]:
                                continue
                            if mmio.Offset == psr_offset and ["HrrSwitch"] == actual_sequence and \
                                    mmio.IsWrite is True:
                                mmio_data = mmio.Data
                                if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                                    mmio_data = mmio.Data << 16
                                psr2_ctl = adapter.regs.get_psr_info(
                                    panel.transcoder_type, PsrOffsetValues(Psr2CtrlReg=mmio_data))
                                if psr2_ctl.Psr2Enable:
                                    actual_sequence.append("Psr2CtlEnable")
                                    break  # this is the last sequence. Break the loop once PSr2CtlEnable is done
                        flip_count += 1
                else:
                    # Psr2CtlDisable -> Psr2IdleState -> HrrSwitch -> Psr2CtlEnable
                    if data.Offset != psr_offset:
                        continue
                    mmio_data = data.Data
                    if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                        mmio_data = data.Data << 16
                    psr2_ctl = adapter.regs.get_psr_info(panel.transcoder_type, PsrOffsetValues(Psr2CtrlReg=mmio_data))

                    # proceed further only when PSR2 CTL is disabled
                    # There would be case where PSR2 CTL is already disabled so just check Psr2Ctl is disabled
                    if psr2_ctl.Psr2Enable:
                        continue
                    actual_sequence.append("Psr2CtlDisable")
                    # With upcoming flips, Psr2IdleState -> HRR switch -> Psr2CtlEnable (Threshold is within next 3
                    # flips)
                    flip_count = index
                    threshold_flip_count = index + 6
                    while flip_count <= threshold_flip_count:
                        for mmio in flip_data[flip_count].MmioDataList:
                            # ignore all MMIOs except PSR2 or HRR
                            if mmio.Offset not in [psr_offset, psr2_regs.Psr2StatusReg, regs.DMC_CHICKEN]:
                                continue

                            # ignore all read calls except Psr2Status
                            if mmio.IsWrite is False and mmio.Offset != psr2_regs.Psr2StatusReg:
                                continue
                            mmio_read_write = "Write" if data.IsWrite else "Read"
                            logging.info(f"\tMMIO {mmio_read_write}: Offset= {hex(mmio.Offset)}= {hex(mmio.Data)} at "
                                         f"{mmio.TimeStamp}")
                            # check for IDLE state after Psr2CtlDisable because it can be idle any time
                            if mmio.Offset == psr2_regs.Psr2StatusReg and ["Psr2CtlDisable"] == actual_sequence:
                                psr2_status = adapter.regs.get_psr_info(
                                    panel.transcoder_type, PsrOffsetValues(Psr2StatusReg=mmio.Data))
                                if psr2_status.Psr2StateIdle:
                                    actual_sequence.append("Psr2StatusIdle")
                                else:
                                    logging.debug("\tPsr2Status is not yet Idle, continue..")
                                    continue
                            # in case of gen13 HRR enable as part of Flip path, GEn14+ HRR enable on scanline interrupt
                            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                                # consider only when Write is there and psr2Status is Idle
                                if mmio.Offset == regs.DMC_CHICKEN and ["Psr2CtlDisable",
                                                                        "Psr2StatusIdle"] == actual_sequence \
                                        and mmio.IsWrite is True:
                                    actual_sequence.append("HrrSwitch")
                                    if panel.lrr_caps.is_lrr_2_0_supported:
                                        logging.debug("\tbreaking loop for LRR 2_0 panel")
                                        break
                            else:
                                if ["Psr2CtlDisable", "Psr2StatusIdle"] == actual_sequence:
                                    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_SCANLINEINTERRUPT,
                                                                                   start_timestamp=mmio.TimeStamp)
                                    if interrupt_data is None:
                                        logging.error("\tFAIL: No scanline interrupt data found")
                                        html.step_end()
                                        return False
                                    vbi_data = etl_parser.get_vbi_data(f"PIPE_{panel.pipe}",
                                                                       start_time=interrupt_data[0].TimeStamp, limit=1)
                                    if vbi_data is None:
                                        logging.error("\tFAIL: No VBI Data found after enabling HRR ")
                                        html.step_end()
                                        return False
                                    mmio_output = etl_parser.get_mmio_data(regs.DMC_CHICKEN, is_write=True,
                                                                           start_time=interrupt_data[0].TimeStamp,
                                                                           end_time=vbi_data[0].TimeStamp)
                                    if mmio_output is None:
                                        logging.error(f"No HRR register transaction happen between "
                                                      f"{interrupt_data[0].TimeStamp} to {vbi_data[0].TimeStamp}")
                                        gdhm.report_driver_bug_os("No HRR register transaction happen between first "
                                                                  "scanline interrupt to VBlank interrupt.")
                                        return False
                                    actual_sequence.append("HrrSwitch")

                            if mmio.Offset == psr_offset and \
                                    ["Psr2CtlDisable", "Psr2StatusIdle", "HrrSwitch"] == actual_sequence:
                                mmio_data = mmio.Data
                                if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                                    mmio_data = mmio.Data << 16
                                psr2_ctl = adapter.regs.get_psr_info(
                                    panel.transcoder_type, PsrOffsetValues(Psr2CtrlReg=mmio_data))
                                if psr2_ctl.Psr2Enable:
                                    actual_sequence.append("Psr2CtlEnable")
                                    break  # this is the last sequence. Break the loop once PSr2CtlEnable is done
                        flip_count += 1
            if actual_sequence == expected_sequence:
                logging.info(f"\tSequence Actual= {actual_sequence}, Expected= {expected_sequence}")
                is_hrr_switch_valid = True
                is_sequence_followed = True
            else:
                logging.error(f"\tSequence Actual= {actual_sequence}, Expected= {expected_sequence}")

            actual_sequence = []
            if is_hrr_switch_valid is False:
                logging.error("\tNO HRR switch is done as soon as Non-Zero duration Flip")
                status &= is_hrr_switch_valid
        previous_flip = flip

    if status is False:
        gdhm.report_test_bug_os("[OsFeatures][HRR] HRR programming didn't happened before Mpo3Flip End")
    html.step_end()
    return status
