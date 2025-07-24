#######################################################################################################################
# @file         drrs.py
# @brief        Contains DRRS enable/disable and verification APIs
#
# @author       Rohit Kumar
#######################################################################################################################

import logging
import sys
from enum import IntEnum
from typing import Union

from DisplayRegs.DisplayOffsets import TimingOffsetValues, VrrOffsetValues, CmtgOffsetValues
from Libs.Core import etl_parser, display_essential
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import gdhm, html
from Libs.Core.vbt import vbt
from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.CMTG import cmtg
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common
from Tests.PowerCons.Modules.dut_context import Adapter, Panel, RrSwitchingMethod
from Tests.VRR import vrr
from Libs.Feature.display_watermark import watermark as wm
from registers.mmioregister import MMIORegister

FPS_TOLERANCE = 0.05
ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.interruptData = 1
ETL_PARSER_CONFIG.functionData = 1


##
# @brief        Exposed enum class for DRRS Type
class DrrsType(IntEnum):
    STATIC_DRRS = 0
    SEAMLESS_DRRS = 2


##
# @brief        Exposed API to enable DRRS
# @param[in]    adapter target adapter object
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
def enable(adapter: Adapter) -> bool:
    assert adapter

    for panel in adapter.panels.values():
        if panel.lrr_caps.rr_switching_method in [RrSwitchingMethod.VTOTAL_HW, RrSwitchingMethod.VTOTAL_SW]:
            if vrr.enable(adapter, True, True) is False:
                logging.error('\tFailed to enable VRR')
                return False
            break

    status = None
    feature_test_control = registry.FeatureTestControl(adapter.gfx_index)
    if feature_test_control.dps_disable != 0:
        feature_test_control.dps_disable = 0
        status = feature_test_control.update(adapter.gfx_index)
        if status is False:
            logging.error(f"\tFAILED to enable DRRS from FeatureTestControl registry on {adapter.name}")
            gdhm.report_test_bug_os(f"[OsFeatures][DRRS]FAILED to enable DRRS from FeatureTestControl registry")
            return False
    logging.info(f"\tPASS: Enabled DRRS from FeatureTestControl registry on {adapter.name}")

    return status


##
# @brief        Exposed API to disable DRRS
# @param[in]    adapter target adapter object
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
def disable(adapter: Adapter) -> bool:
    assert adapter

    status = None
    feature_test_control = registry.FeatureTestControl(adapter.gfx_index)
    if feature_test_control.dps_disable != 1:
        feature_test_control.dps_disable = 1
        status = feature_test_control.update(adapter.gfx_index)
        if status is False:
            logging.error(f"\tFailed to disable DRRS from FeatureTestControl registry on {adapter.name}")
            gdhm.report_test_bug_os(f"[OsFeatures][DRRS]Failed to disable DRRS from FeatureTestControl registry")
            return False
    logging.info(f"\tPASS: Disabled DRRS from FeatureTestControl registry on {adapter.name}")

    return status


##
# @brief        Exposed API to configure DRRS Type in VBT
# @param[in]    adapter object, Adapter object
# @param[in]    panel object, Panel object
# @param[in]    drrs_type DrrsType, flag to use Seamless or Static DRRS
# @return       status, Boolean, True if operation is successful, False otherwise
def configure_drrs_panel_type(adapter: Adapter, panel: Panel, drrs_type: DrrsType) -> bool:
    html.step_start(f"Enabling {DrrsType(drrs_type).name} DRRS for {panel.port} on {adapter.name}")

    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")

    # check that requested DRRS is already enabled
    if getattr(gfx_vbt.block_40, f'DpsPanelType{panel_index}') == drrs_type.value:
        logging.info(f"{DrrsType(drrs_type).name} is already enabled for {panel.port} on PanelIndex= {panel_index}")
        html.step_end()
        return True

    # apply value 0 to enable Static DRRS and 2 for Seamless DRRS
    logging.info(f"\tApplying DpsPanelType{panel_index}= {drrs_type.value}")
    setattr(gfx_vbt.block_40, f'DpsPanelType{panel_index}', drrs_type.value)

    logging.info("\tApplying changes in VBT")
    if gfx_vbt.apply_changes() is False:
        logging.error("\tFAILED to apply changes in VBT")
        html.step_end()
        return False

    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("\tFAILED to restart display driver after VBT update")
        html.step_end()
        return False

    # Verify after restarting the driver
    logging.info("\tReloading VBT data")
    gfx_vbt.reload()

    # check that requested DRRS is enabled
    if getattr(gfx_vbt.block_40, f'DpsPanelType{panel_index}') != drrs_type.value:
        logging.error(f"\tFAILED to enable {DrrsType(drrs_type).name} for {panel.port} on PanelIndex= {panel_index}")
        gdhm.report_test_bug_os(f"[OsFeatures][DRRS]FAILED to enable DRRS", gdhm.ProblemClassification.OTHER,
                                gdhm.Priority.P3,
                                gdhm.Exposure.E3)
        html.step_end()
        return False

    logging.info(f"\tSuccessfully enabled {DrrsType(drrs_type).name} for {panel.port} on {adapter.name}")
    html.step_end()
    return True


##
# @brief        Exposed API to verify DRRS
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    etl_path string path to etl file
# @return       status Boolean, True if verification is successful, False otherwise
def verify(adapter: Adapter, panel: Panel, etl_path: str) -> bool:
    assert adapter
    assert panel
    assert etl_path

    html.step_start(f"Verifying DRRS for {adapter.name}")
    # From ADLP+, pixel clock based RR switching will not be supported on multi-display configuration.
    if adapter.name not in common.PRE_GEN_13_PLATFORMS + ['DG2']:
        logging.info("Step: Checking Multi-display support for Pixel-Clock based RR switch (Not supported from ADLP+)")
        active_display_config = DisplayConfiguration().get_active_display_configuration()
        if active_display_config.numberOfDisplays > 1:
            if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.CLOCK:
                logging.error("From ADLP+, Pixel Clock based RR Switching is NOT supported in Multi-display config")
                return False
        logging.info("Pixel Clock based RR Switching is supported (Active display is 1)")

    # If PSR2 is disabled, RR switching method should be VTOTAL_HW
    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_SW:
        if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is False:
            logging.info("\tPSR2 is disabled. Changing RR_SWITCH METHOD from VTOTAL_SW to VTOTAL_HW")
            panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW

    status = True

    logging.info(f"Step: Verifying DRRS for {panel.port}")
    logging.info(f"\tGenerating EtlParser Report for {etl_path}")
    if etl_parser.generate_report(etl_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        return False

    logging.info("\tSuccessfully generated ETL Parser report")

    vbi_enabled_regions, vbi_disabled_regions = get_vsync_enable_disable_regions(etl_parser.Ddi.DDI_CONTROLINTERRUPT2)
    if vbi_disabled_regions is None:
        gdhm.report_driver_bug_os("[OsFeatures][DRRS] No CRTC_VSYNC DISABLE interrupt found in ETL")
        logging.error("\tFAIL: No CRTC_VSYNC DISABLE interrupt found (VBI is not getting disabled)")
        return False

    logging.info(f"\tNumber of VBI disabling interrupts= {len(vbi_disabled_regions)}")
    vbi_disabled_duration = 0
    display_timings = DisplayConfiguration().get_display_timings(panel.display_info.DisplayAndAdapterInfo)
    active_mode_refreshRate = round(display_timings.targetPixelRate / (display_timings.hTotal * display_timings.vTotal))
    for (start, end) in vbi_disabled_regions:
        if end == sys.maxsize:
            # To avoid a scenario where VBI got disabled just before stopping the ETL traces
            continue

        vbi_disabled_duration += (end - start)
        logging.debug(f"\tVBI Disabled Region: Start={start}, End={end}")

        # If VBI is disabled for more than 3 frames, make sure DRRS is getting triggered
        frame_duration = (1000 / active_mode_refreshRate) * 3
        if (end - start) > frame_duration:
            status &= verify_clock_programming(adapter, panel, panel.drrs_caps.min_rr, start, end)

    status &= verify_clock_programming(adapter, panel, panel.drrs_caps.min_rr)

    if vbi_enabled_regions is None:
        return status

    logging.info(f"\tNumber of VBI enabling interrupts= {len(vbi_disabled_regions)}")
    vbi_enabled_duration = 0
    for (start, end) in vbi_enabled_regions:
        # It is possible that LinkM write happened before ETL tracing if VBI was enabled in the beginning.
        # Skipping the first region.
        if start == 0:
            continue

        if end == sys.maxsize:
            # To avoid a scenario where VBI got enabled just before (few ms) stopping the ETL traces
            continue

        vbi_enabled_duration += (end - start)
        logging.debug("\tVBI Enabled Region: Start= {0}, End= {1}".format(start, end))
        frame_duration = (1000 / active_mode_refreshRate) * 3
        if (end - start) > frame_duration:
            status &= verify_clock_programming(adapter, panel, active_mode_refreshRate, start, end)

    status &= verify_clock_programming(adapter, panel, active_mode_refreshRate)
    logging.info("\tVBI duration, ENABLED= {0:.3f} ms, DISABLED= {1:.3f} ms".format(
        vbi_enabled_duration, vbi_disabled_duration))

    if vbi_disabled_duration < vbi_enabled_duration:
        logging.warning("\tVBI enabled duration is longer than expected")

    status &= verify_psr_exit_time(adapter, panel)

    return status


##
# @brief        Exposed API to verify clock programming for any given panel
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    expected_rr float
# @param[in]    start_timestamp timestamp in ETL from where verification should be started
# @param[in]    end_timestamp
# @return       status Boolean, True if verification is successful, False otherwise
def verify_clock_programming(adapter: Adapter, panel: Panel, expected_rr: float,
                             start_timestamp=None, end_timestamp=None) -> bool:
    assert adapter
    assert panel
    assert expected_rr

    actual_rr_list = []
    disable_event_data = []
    clock_vtotal_sw_verification_status = False

    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.CLOCK:
        actual_rr_list = get_clock_based_rr(adapter, panel, start_timestamp, end_timestamp)
    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_HW:
        # In case of VRR H/W based DRRS, driver will not program VRR Vmax for max_rr, instead it will disable VRR
        # Check for VRR disable event in such case
        if expected_rr == panel.drrs_caps.max_rr and not panel.vrr_caps.is_always_vrr_mode:
            vrr_disable_events = etl_parser.get_event_data(
                etl_parser.Events.RR_SWITCH_INFO, start_timestamp, end_timestamp)

            if vrr_disable_events is None:
                logging.error(f"No VRR disable events found in ETL")
                return False

            for disable_event in vrr_disable_events:
                if disable_event.TargetId == panel.target_id and disable_event.RrMode != "DD_REFRESH_RATE_MODE_VARIABLE":
                    disable_event_data.append(disable_event)

            if disable_event_data is None:
                if start_timestamp is not None and end_timestamp is not None:
                    logging.error("\t\tFAIL: VRR H/W is not getting disabled on CRTC_VSYNC ENABLE [{0} - {1}]".format(
                        start_timestamp, end_timestamp))
                else:
                    logging.error("\t\tFAIL: VRR H/W is not getting disabled on CRTC_VSYNC ENABLE")
                gdhm.report_driver_bug_os(f"[OsFeatures][DRRS]VRR H/W is not getting disabled on CRTC_VSYNC ENABLE")
                return False

            if start_timestamp is not None and end_timestamp is not None:
                for event in disable_event_data:
                    logging.debug("\t\t{0}".format(event))
                logging.info("\t\tPASS: VRR H/W is getting disabled on CRTC_VSYNC ENABLE [{0} - {1}]".format(
                    start_timestamp, end_timestamp))
            else:
                logging.info("\t\tPASS: VRR H/W is getting disabled on CRTC_VSYNC ENABLE")
            return True

        actual_rr_list = get_vtotal_hw_rr(adapter, panel, start_timestamp, end_timestamp)

    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_SW:
        actual_rr_list = get_vtotal_sw_rr(adapter, panel, start_timestamp, end_timestamp)
    logging.info(f"Actual Clock RR list= {actual_rr_list}")
    # comparing with actual_max_rr as driver considers the pixel clock value in DTD to calculate the LinkM for max_rr
    for actual_rr in actual_rr_list:
        # compare with tolerance using actual_max_rr when expected_rr is max_rr, else it will be false positive
        # even if there is no RR change happening. Reason: difference between the max_rr and actual_max_rr
        # may be less than FPS_TOLERANCE
        if common.compare_with_tolerance(actual_rr, expected_rr, FPS_TOLERANCE) or \
                (
                        round(expected_rr) == round(panel.max_rr) and
                        common.compare_with_tolerance(actual_rr, panel.drrs_caps.actual_max_rr, FPS_TOLERANCE)
                ) or \
                (
                        round(expected_rr) == round(panel.min_rr) and
                        common.compare_with_tolerance(actual_rr, panel.drrs_caps.actual_min_rr, FPS_TOLERANCE)
                ):
            if start_timestamp is not None and end_timestamp is not None:
                logging.info(f"\t\tPASS: {panel.lrr_caps.rr_switching_method} based RR Expected= {expected_rr}, "
                             f"Actual= {actual_rr} ({start_timestamp} - {end_timestamp})")
            else:
                logging.info(f"\t\tPASS: {panel.lrr_caps.rr_switching_method} based RR "
                             f"Expected= {expected_rr}, Actual= {actual_rr}")
            clock_vtotal_sw_verification_status = True

    if panel.psr_caps.is_psr2_supported and panel.lrr_caps.is_lrr_supported is False:
        logging.info("Panel is PSR2 and LRR is disabled via reg-key. There will be no RR change (Expected)")
        clock_vtotal_sw_verification_status = True

    cmtg_verification_status = True
    # Verify CMTG only if the RR switching method is Vtotal S/W based or Clock based and platform (ADLP + Gen14+)
    if ((adapter.name not in common.PRE_GEN_13_PLATFORMS + ['DG2']) and (
            panel.lrr_caps.rr_switching_method in [RrSwitchingMethod.VTOTAL_SW, RrSwitchingMethod.CLOCK]) and
            adapter.name not in common.GEN_16_PLATFORMS):
        cmtg_verification_status &= verify_cmtg_rr_change(adapter, panel, expected_rr, start_timestamp, end_timestamp)
        logging.info(f"CMTG Verification Status= {cmtg_verification_status} "
                     f"during: [{start_timestamp} - {end_timestamp}]")
    else:
        if adapter.name in (common.PRE_GEN_13_PLATFORMS + ['DG2']):
            logging.info(f"CMTG Verification Skipped as CMTG is not supported on {adapter.name}")
        else:
            logging.info(f"CMTG Verification Skipped as panel's RR switching method is VTOTAL_HW/UNSUPPORTED")
    if not clock_vtotal_sw_verification_status:
        if start_timestamp is not None and end_timestamp is not None:
            logging.error(f"\t\tFAIL: {panel.lrr_caps.rr_switching_method} based RR "
                          f"Expected= {expected_rr}, Actual= {actual_rr_list} ({start_timestamp} - {end_timestamp})")
        else:
            logging.error(f"\t\tFAIL: {panel.lrr_caps.rr_switching_method} based RR "
                          f"Expected= {expected_rr}, Actual= {actual_rr_list}")
        gdhm.report_test_bug_os(f"[OsFeatures][DRRS]Clock verification failed.")
        return False
    if not cmtg_verification_status:
        gdhm.report_driver_bug_os(f"[OsFeatures][DRRS]Invalid RR programming found in CMTG")
        return False
    return True


##
# @brief        Exposed API to verify CMTG
# @param[in]    adapter object, Adapter from dut_context
# @param[in]    panel object, Panel from dut_context
# @param[in]    expected_rr
# @param[in]    start_timestamp optional, timestamp in ETL from where verification should be started
# @param[in]    end_timestamp optional, timestamp in ETL till where verification should be completed
# @return       timestamp_list, list
# @return       boolean True if CMTG verification passes, False otherwise
def verify_cmtg_rr_change(adapter: Adapter, panel: Panel, expected_rr, start_timestamp=None, end_timestamp=None):
    # Get the CMTG List of RR's during the timestamp
    actual_rr_list_cmtg = []
    actual_rr_list_trans = []
    if adapter.name in common.PRE_GEN_13_PLATFORMS:
        logging.error(f"CMTG is not supported on {adapter.name}")
        return False

    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.CLOCK:
        actual_rr_list_cmtg = get_cmtg_clock_based_rr(adapter, panel, start_timestamp, end_timestamp)
        actual_rr_list_trans = get_clock_based_rr(adapter, panel, start_timestamp, end_timestamp,
                                                  get_rr_with_timestamp=True)

    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_SW:
        actual_rr_list_cmtg = get_cmtg_vtotal_sw_rr(adapter, panel, start_timestamp, end_timestamp)
        actual_rr_list_trans = get_vtotal_sw_rr(adapter, panel, start_timestamp, end_timestamp,
                                                get_rr_with_timestamp=True)

    # Check if CMTG was enabled
    timestamp_list_cmtg = get_cmtg_ctl_ddi_status(adapter, panel, start_timestamp, end_timestamp, False)

    # Check if the transcoder is slave to the CMTG
    time_stamp_list_ddi_cmtg = get_cmtg_ctl_ddi_status(adapter, panel, start_timestamp, end_timestamp, True)

    logging.info(f"CMTG RR list= {actual_rr_list_cmtg}")
    logging.info(f"Transcoder RR List= {actual_rr_list_trans}")
    logging.info(f"CMTG Enabled= {timestamp_list_cmtg}")
    logging.info(f"Transcoder slave= {time_stamp_list_ddi_cmtg}")

    if len(timestamp_list_cmtg) > 0:
        if len(time_stamp_list_ddi_cmtg) > 0:
            # Compare RR lists of CMTG and Transcoder
            if len(actual_rr_list_cmtg) > 0 and len(actual_rr_list_trans) > 0:

                # Check if both the list have same number of entries
                if len(actual_rr_list_cmtg) != len(actual_rr_list_trans):
                    logging.error("Transcoder and CMTG Refresh rate entries do not match")
                    logging.error(f"CMTG RR changes= {actual_rr_list_cmtg}")
                    logging.error(f"Transcoder RR changes= {actual_rr_list_trans}")
                    gdhm.report_driver_bug_os(
                        f"[OsFeatures][DRRS]Transcoder and CMTG Refresh rate entries do not match")
                    return False

                rr_match = True
                for cmtg_trl, trans_trl in zip(actual_rr_list_cmtg, actual_rr_list_trans):
                    # compare RR
                    if cmtg_trl[1] != trans_trl[1]:
                        logging.error("The CMTG and Transcoder RR do not match")
                        logging.error(f"CMTG: Timestamp= {cmtg_trl[0]} \t RR= {cmtg_trl[1]} ")
                        rr_match = False
                    # check for time gap between transcoder and CMTG register changes Threshold is 1 second
                    if (trans_trl[0] - cmtg_trl[0]) > 1000:
                        logging.error("Time Gap between transcoder and CMTG RR change greater than 1 second")
                        rr_match = False
                if rr_match:
                    logging.info("PASS: CMTG Verification Passed")
                    return True
                else:
                    logging.error("FAIL: CMTG Verification Failed. RR switch mismatch found on CMTG, Transcoder")
                    gdhm.report_driver_bug_os(
                        f"[OsFeatures][DRRS]CMTG Verification Failed. RR switch mismatch found on CMTG, Transcoder")
                    return False
            logging.warning("No RR change detected in CMTG and Transcoder during workload")

        logging.error(f"CMTG is enabled, but Slave bit is not set in the Transcoder_{panel.transcoder_type}"
                      f"\t FAIL: CMTG Actual RR List:{actual_rr_list_cmtg} Expected: {expected_rr}")
        return False

    logging.warning(f"\tCMTG is NOT enabled CMTG. Actual RR List= {actual_rr_list_cmtg}, Expected= {expected_rr}")
    return True


##
# @brief        Exposed API to get CMTG control status and to get DDI function control CMTG slave status.
# @param[in]    adapter object, Adapter from dut_context
# @param[in]    panel object, Panel from dut_context
# @param[in]    start_timestamp optional, timestamp in ETL from where verification should be started
# @param[in]    end_timestamp optional, timestamp in ETL till where verification should be completed
# @param[in]    cmtg_ddi: Boolean variable to decide whether to get CMTG control or DDI function control
#                                                                                                 CMTG slave bit status.
# @return       Returns timestamp list of all DDI CMTG slave status entries when input cmtg_ddi is set,
#                                                                             otherwise will return CMTG control status.
def get_cmtg_ctl_ddi_status(adapter: Adapter, panel: Panel, start_timestamp=None, end_timestamp=None,
                            cmtg_ddi: bool = False):
    if cmtg_ddi:
        cmtg_ddi_offsets = adapter.regs.get_cmtg_offsets(panel.transcoder_type)
        mmio_output = etl_parser.get_mmio_data(cmtg_ddi_offsets.DdiFunctionControlReg, start_time=start_timestamp,
                                               end_time=end_timestamp)
    else:
        cmtg_ddi_offsets = adapter.regs.get_cmtg_offsets(panel.transcoder_type)
        mmio_output = etl_parser.get_mmio_data(cmtg_ddi_offsets.CmtgControlReg, start_time=start_timestamp,
                                               end_time=end_timestamp)
    timestamp_list = set()

    if mmio_output is None:
        return list(timestamp_list)

    for cmtg_ddi_value in mmio_output:
        if cmtg_ddi:
            cmtg_ddi_info = adapter.regs.get_cmtg_info(panel.transcoder_type,
                                                       CmtgOffsetValues(DdiFunctionControlReg=cmtg_ddi_value.Data))
            if cmtg_ddi_info.DdiFnCtrlCmtgSlave:
                timestamp_list.add(cmtg_ddi_value.TimeStamp)
        else:
            cmtg_ddi_info = adapter.regs.get_cmtg_info(panel.transcoder_type,
                                                       CmtgOffsetValues(CmtgControlReg=cmtg_ddi_value.Data))
            if cmtg_ddi_info.CmtgEnable:
                timestamp_list.add(cmtg_ddi_value.TimeStamp)

    return list(timestamp_list)


##
# @brief        Exposed API to get clock based RR
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    start_timestamp optional, starting point in ETL for fetching clock based RR change
# @param[in]    end_timestamp optional, ending point in ETL for fetching clock based RR change
# @param[in]    get_rr_with_timestamp bool, True if rr list with timestamp required
# @return       rr_list list
def get_clock_based_rr(adapter: Adapter, panel: Panel, start_timestamp=None, end_timestamp=None,
                       get_rr_with_timestamp=False):
    timing_offsets = adapter.regs.get_timing_offsets(panel.transcoder_type)
    mmio_output = etl_parser.get_mmio_data(timing_offsets.LinkM, start_time=start_timestamp, end_time=end_timestamp)
    if mmio_output is None:
        return [panel.max_rr]
    rr_list = set()
    previous_link_m = None
    # Declare a list which will be of format [(TimeStamp1, RefreshRate1), (TimeStamp2, RefreshRate2)]
    rr_list_with_timestamp = []  # used for CMTG verification
    for link_m_value in mmio_output:
        timing_info = adapter.regs.get_timing_info(panel.transcoder_type, TimingOffsetValues(LinkM=link_m_value.Data))
        rr = link_m_to_hz(adapter, panel, timing_info.LinkM)
        logging.info(f"Calculated RR value= {rr}")

        if previous_link_m is None:
            previous_link_m = link_m_value
            logging.info(f"\t\tCLOCK based RR= {rr} [START - {link_m_value.TimeStamp}]")
        else:
            timing_info_p = adapter.regs.get_timing_info(panel.transcoder_type,
                                                         TimingOffsetValues(LinkM=previous_link_m.Data))
            previous_rr = link_m_to_hz(adapter, panel, timing_info_p.LinkM)
            if previous_rr != rr:
                logging.info(
                    f"\t\tCLOCK based RR= {previous_rr} [{previous_link_m.TimeStamp} - {link_m_value.TimeStamp}]")
                previous_link_m = link_m_value

        rr_list.add(rr)
        # Get the timestamp when there is a write operation to the LinkM register.
        if get_rr_with_timestamp and link_m_value.IsWrite:
            rr_list_with_timestamp.append((link_m_value.TimeStamp, rr))
    if previous_link_m is not None:
        timing_info_p = adapter.regs.get_timing_info(
            panel.transcoder_type, TimingOffsetValues(LinkM=previous_link_m.Data))
        logging.info(f"\t\tCLOCK based RR= {link_m_to_hz(adapter, panel, timing_info_p.LinkM)} "
                     f"[{previous_link_m.TimeStamp} - END]")

    return rr_list_with_timestamp if get_rr_with_timestamp else list(rr_list)


##
# @brief        Exposed API to get list of refresh rates for a  given time range by reading the CMTG LINKM values
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    start_timestamp optional, starting point in ETL for fetching cmtg clock based RR change
# @param[in]    end_timestamp optional, ending point in ETL for fetching cmtg clock based RR change
# @return       rr_list list
def get_cmtg_clock_based_rr(adapter: Adapter, panel: Panel, start_timestamp=None, end_timestamp=None):
    timing_offsets = adapter.regs.get_cmtg_offsets(panel.transcoder_type)
    mmio_output = etl_parser.get_mmio_data(timing_offsets.CmtgLinkMReg, start_time=start_timestamp,
                                           end_time=end_timestamp)
    rr_list_with_timestamp = []
    if mmio_output is None:
        logging.info(f"No Values found in ETL for {timing_offsets.CmtgLinkMReg} ")
        return rr_list_with_timestamp

    previous_link_m = None
    for link_m_value in mmio_output:
        timing_info = adapter.regs.get_cmtg_info(panel.transcoder_type,
                                                 CmtgOffsetValues(CmtgLinkMReg=link_m_value.Data))
        rr = link_m_to_hz(adapter, panel, timing_info.CmtgLinkM)
        if link_m_value.IsWrite:
            rr_list_with_timestamp.append((link_m_value.TimeStamp, rr))
        if previous_link_m is None:
            previous_link_m = link_m_value
            logging.info(f"\t\t CMTG CLOCK based RR= {rr} [START - {link_m_value.TimeStamp}]")
        else:
            timing_info_p = adapter.regs.get_cmtg_info(panel.transcoder_type,
                                                       CmtgOffsetValues(CmtgLinkMReg=previous_link_m.Data))
            previous_rr = link_m_to_hz(adapter, panel, timing_info_p.CmtgLinkM)
            # Log only if previous rr is not equal to present RR
            if previous_rr != rr:
                logging.info(
                    f"\t\t CMTG CLOCK based RR= {previous_rr} [{previous_link_m.TimeStamp} - {link_m_value.TimeStamp}]")
                previous_link_m = link_m_value

    # Handle the last RR
    if previous_link_m is not None:
        timing_info_p = adapter.regs.get_cmtg_info(
            panel.transcoder_type, CmtgOffsetValues(CmtgLinkMReg=previous_link_m.Data))
        logging.info(
            f"\t\t CMTG CLOCK based RR= {link_m_to_hz(adapter, panel, timing_info_p.CmtgLinkM)}"
            f"[{previous_link_m.TimeStamp}-END]")

    return rr_list_with_timestamp


##
# @brief        Exposed API to get VRR/ VTotal based RR
# @param[in]    adapter Adapter, object
# @param[in]    panel Panel, object
# @param[in]    start_timestamp optional, starting point in ETL for fetching vtotal hw based RR change
# @param[in]    end_timestamp optional, ending point in ETL for fetching vtotal hw based RR change
# @param[in]    get_rr_with_timestamp bool, True if rr list with timestamp required
# @return       rr_list list
def get_vtotal_hw_rr(adapter: Adapter, panel: Panel, start_timestamp=None, end_timestamp=None,
                     get_rr_with_timestamp=False):
    vrr_enable_event_output = []
    vrr_offsets = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    timing_info = adapter.regs.get_timing_info(panel.transcoder_type)
    h_total = timing_info.HTotal

    if panel.mso_caps.is_mso_supported:
        logging.info(f"This panel is MSO supported so multiplying HTotal with number of segments"
                     f" {panel.mso_caps.no_of_segments}")
        h_total = panel.mso_caps.no_of_segments * h_total

    vrr_enable_events = etl_parser.get_event_data(etl_parser.Events.RR_SWITCH_INFO, start_timestamp, end_timestamp)
    # Filter out enable event data for targeted display
    if vrr_enable_events is not None:
        for event in vrr_enable_events:
            if event.TargetId == panel.target_id and (
                    (event.RrMode == "DD_REFRESH_RATE_MODE_VARIABLE") and event.IsCurrent):
                vrr_enable_event_output.append(event)
    if vrr_enable_event_output is not None:
        if start_timestamp is not None and end_timestamp is not None:
            for event in vrr_enable_event_output:
                logging.debug(f"\t\t{event}")

    mmio_output = etl_parser.get_mmio_data(vrr_offsets.VrrVmaxReg, start_time=start_timestamp, end_time=end_timestamp)
    if mmio_output is None:
        return [panel.vrr_caps.max_rr]

    rr_list = set()
    previous_vrr_vmax = None
    rr_list_with_timestamp = []
    for mmio_data in mmio_output:
        vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrVmaxReg=mmio_data.Data))
        # Current RR = PixelClockInHz/(HTotal*VTotal)
        rr = round(
            float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (vrr_info.VrrVmax + 1)), 3)
        logging.info(f"Htotal: {h_total}, VrrVmax:{vrr_info.VrrVmax}, "
                     f"Native_ModePixelClock: {panel.native_mode.pixelClock_Hz} RR : {rr}")

        if previous_vrr_vmax is None:
            previous_vrr_vmax = mmio_data
            logging.info(f"\t\tVTotal HW based RR= {rr} [START - {mmio_data.TimeStamp}]")
        else:
            vrr_info_p = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                   VrrOffsetValues(VrrVmaxReg=previous_vrr_vmax.Data))
            previous_rr = round(
                float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (vrr_info_p.VrrVmax + 1)), 3)
            if previous_rr != rr:
                logging.info(
                    f"\t\tVTotal HW based RR= {previous_rr} [{previous_vrr_vmax.TimeStamp} - {mmio_data.TimeStamp}]")
                previous_vrr_vmax = mmio_data

        rr_list.add(rr)
        # Get the timestamp when there is a write operation to the register.
        if get_rr_with_timestamp and mmio_data.IsWrite:
            rr_list_with_timestamp.append((mmio_data.TimeStamp, rr))

    if previous_vrr_vmax is not None:
        vrr_info_p = adapter.regs.get_vrr_info(
            panel.transcoder_type, VrrOffsetValues(VrrVmaxReg=previous_vrr_vmax.Data))
        previous_rr = round(
            float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (vrr_info_p.VrrVmax + 1)), 3)
        logging.info(f"\t\tVTotal HW based RR= {previous_rr} [{previous_vrr_vmax.TimeStamp} - END]")

    return rr_list_with_timestamp if get_rr_with_timestamp else list(rr_list)


##
# @brief        Exposed API to get VTotal S/W based RR
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    start_timestamp optional, starting point in ETL for fetching vtotal sw based RR change
# @param[in]    end_timestamp optional, ending point in ETL for fetching vtotal sw based RR change
# @param[in]    get_rr_with_timestamp bool, True if rr list with timestamp required
# @return       rr_list list
def get_vtotal_sw_rr(adapter: Adapter, panel: Panel, start_timestamp=None, end_timestamp=None,
                     get_rr_with_timestamp=False):
    timing_info = adapter.regs.get_timing_info(panel.transcoder_type)
    h_total = timing_info.HTotal

    if panel.mso_caps.is_mso_supported:
        logging.info(f"This panel is MSO supported so multiplying HTotal with number of segments"
                     f" {panel.mso_caps.no_of_segments}")
        h_total = panel.mso_caps.no_of_segments * h_total

    timing_offsets = adapter.regs.get_timing_offsets(panel.transcoder_type)
    mmio_output = etl_parser.get_mmio_data(timing_offsets.VTotal, start_time=start_timestamp, end_time=end_timestamp)
    if mmio_output is None:
        return [panel.vrr_caps.max_rr]

    rr_list = set()
    # Declare a list which will be of format [(TimeStamp1, RefreshRate1), (TimeStamp2, RefreshRate2)]
    timestamp_rr_list = []  # used for CMTG verification
    previous_v_total = None
    previous_write_rr = None
    for mmio_data in mmio_output:
        timing_info = adapter.regs.get_timing_info(panel.transcoder_type, TimingOffsetValues(VTotal=mmio_data.Data))
        rr = round(float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (timing_info.VTotal + 1)), 3)
        logging.info(f"Htotal: {h_total}, VTotal:{timing_info.VTotal}, "
                     f"Native_ModePixelClock: {panel.native_mode.pixelClock_Hz} RR : {rr}")
        if previous_v_total is None:
            previous_v_total = mmio_data
            logging.info(f"\t\tVTotal SW based RR= {rr} [START - {mmio_data.TimeStamp}]")
        else:
            timing_info_p = adapter.regs.get_timing_info(panel.transcoder_type,
                                                         TimingOffsetValues(VTotal=previous_v_total.Data))
            previous_rr = round(
                float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (timing_info_p.VTotal + 1)), 3)
            if previous_rr != rr:
                logging.info(
                    f"\t\tVTotal SW based RR= {previous_rr} [{previous_v_total.TimeStamp} - {mmio_data.TimeStamp}]")
                previous_v_total = mmio_data

        rr_list.add(rr)
        # Get the timestamp when there is a write operation to the VTotal register.
        if get_rr_with_timestamp and mmio_data.IsWrite:
            if previous_write_rr != rr:
                previous_write_rr = rr
                timestamp_rr_list.append((mmio_data.TimeStamp, rr))

    if previous_v_total is not None:
        timing_info_p = adapter.regs.get_timing_info(
            panel.transcoder_type, TimingOffsetValues(VTotal=previous_v_total.Data))
        previous_rr = round(float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (timing_info_p.VTotal + 1)), 3)
        logging.info(f"\t\tVTotal SW based RR= {previous_rr} [{previous_v_total.TimeStamp} - END]")

    return timestamp_rr_list if get_rr_with_timestamp else list(rr_list)


##
# @brief        Exposed API to get VTotal S/W based RR
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    start_timestamp optional, starting point in ETL for fetching cmtg vtotal sw based RR change
# @param[in]    end_timestamp optional, ending point in ETL for fetching cmtg vtotal sw based RR change
# @return       rr_list list
def get_cmtg_vtotal_sw_rr(adapter: Adapter, panel: Panel, start_timestamp=None, end_timestamp=None):
    timing_info = adapter.regs.get_cmtg_info(panel.transcoder_type)
    h_total = timing_info.CmtgHTotal

    if panel.mso_caps.is_mso_supported:
        # if panel supports MSO, Htotal is multipled with number of segments.
        h_total = panel.mso_caps.no_of_segments * h_total
    timing_offsets = adapter.regs.get_cmtg_offsets(panel.transcoder_type)
    mmio_output = etl_parser.get_mmio_data(timing_offsets.CmtgVTotalReg, start_time=start_timestamp,
                                           end_time=end_timestamp)
    timestamp_rr_list = []
    if mmio_output is None:
        logging.info(f"No Values found MMIO for register CMTG VTotal register {timing_offsets.CmtgVTotalReg}")
        return timestamp_rr_list
    previous_v_total = None
    for v_total in mmio_output:
        timing_info = adapter.regs.get_cmtg_info(panel.transcoder_type, CmtgOffsetValues(CmtgVTotalReg=v_total.Data))
        rr = round(float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (timing_info.CmtgVTotal + 1)), 3)
        if v_total.IsWrite:
            timestamp_rr_list.append((v_total.TimeStamp, rr))
        if previous_v_total is None:
            previous_v_total = v_total
            logging.info(f"\t\t CMTG VTotal SW based RR= {rr} [START - {v_total.TimeStamp}]")
        else:
            timing_info_p = adapter.regs.get_cmtg_info(panel.transcoder_type,
                                                       CmtgOffsetValues(CmtgVTotalReg=previous_v_total.Data))
            previous_rr = round(
                float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (timing_info_p.CmtgVTotal + 1)), 3)
            if previous_rr != rr:
                logging.info(
                    f"\t\t CMTG VTotal SW based RR= {previous_rr} [{previous_v_total.TimeStamp} - {v_total.TimeStamp}]")
                previous_v_total = v_total

    # for printing the last rr entry
    if previous_v_total is not None:
        timing_info_p = adapter.regs.get_cmtg_info(
            panel.transcoder_type, CmtgOffsetValues(CmtgVTotalReg=previous_v_total.Data))
        previous_rr = round(
            float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (timing_info_p.CmtgVTotal + 1)), 3)
        logging.info(f"\t\t CMTG VTotal SW based RR= {previous_rr} [{previous_v_total.TimeStamp} - END]")
    return timestamp_rr_list


##
# @brief        Exposed API to verify PSR exit time
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @return       status bool True if PSR2 exit time verification passed successfully, False otherwise
def verify_psr_exit_time(adapter: Adapter, panel: Panel):
    function = "Gen11TranscoderPsr2Disable"
    if adapter.name in common.GEN_12_PLATFORMS:
        function = "Gen12TranscoderPsr2Disable"
    elif adapter.name in common.GEN_13_PLATFORMS:
        function = "Gen13TranscoderPsr2Disable"
    elif adapter.name in common.GEN_14_PLATFORMS:
        function = "Gen14TranscoderPsr2Disable"
    elif adapter.name in common.GEN_15_PLATFORMS:
        function = "Gen15TranscoderPsr2Disable"

    logging.info(f"\tVerifying PSR2 exit time using function Data of {function}()")
    function_data = etl_parser.get_function_data(function)
    if function_data is None:
        logging.info("\t\tNo PSR2 disable call found")
        return True

    active_mode = DisplayConfiguration().get_current_mode(panel.target_id)

    # As per bspec we need to wait for the worst case total of ( > 7.5ms + 1000 / Refresh Rate)
    # https://gfxspecs.intel.com/Predator/Home/Index/4289
    # one full frame time(1/refresh rate)+SRD exit training time(max of 6 ms)+SRD aux channel handshake(max of 1.5 ms)
    start_time = 0
    status = True
    expected_wait_time = 7.5 + 1000 / active_mode.refreshRate
    report_to_gdhm = False
    for data in function_data:
        if data.Stage == 0:
            start_time = data.TimeStamp
        if data.Stage == 1:
            logging.info(f"\t\tMax wait time to disable PSR2. "
                         f"Expected= {expected_wait_time:.3f} ms, Actual= {(data.TimeStamp - start_time):.3f} ms")
            if data.ErrorCode != 0:
                logging.error(f"\t\tFAIL: Driver failed to disable PSR2 at TimeStamp= {data.TimeStamp}")
                report_to_gdhm = True
                status = False

    if report_to_gdhm:
        gdhm.report_driver_bug_os(f"[OsFeatures][DRRS] Driver failed to disable PSR2 in {function}()")

    if status:
        logging.info("\t\tPASS: PSR2 exit time verification")
    else:
        logging.error("\t\tFAIL: PSR2 exit time verification")

    return status


##
# @brief        Helper API to get VBI enabled and disabled regions from ETL
# @param[in]    interrupt ControlInterrupt1/2/3
# @return       (enabled, disabled), tuple, a tuple of lists having enabling and disabling timestamps
def get_vsync_enable_disable_regions(interrupt):
    disabled = []
    enabled = []
    interrupt_data = etl_parser.get_interrupt_data(interrupt, etl_parser.InterruptType.CRTC_VSYNC)
    if interrupt_data is None:
        return None, None

    start_disabled = None
    start_enabled = None
    is_first_region = True
    for interrupt in interrupt_data:
        if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.ENABLE]:
            if start_enabled is None:
                start_enabled = interrupt.TimeStamp

            if start_disabled is not None:
                disabled.append((start_disabled, interrupt.TimeStamp))
                start_disabled = None

        if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.DISABLE_NO_PHASE]:
            if start_enabled is not None:
                # In first enabled region, existing DRRS state is unknown.
                # This can result in both, clock programming to high/low or no programming at all. Skipping.
                if is_first_region:
                    is_first_region = False
                else:
                    enabled.append((start_enabled, interrupt.TimeStamp))
                start_enabled = None
            else:
                enabled.append((0, interrupt.TimeStamp))

            if start_disabled is None:
                start_disabled = interrupt.TimeStamp

    if start_enabled is not None:
        enabled.append((start_enabled, sys.maxsize))
    if start_disabled is not None:
        disabled.append((start_disabled, sys.maxsize))

    if len(disabled) == 0:
        disabled = None
    if len(enabled) == 0:
        enabled = None

    return enabled, disabled


##
# @brief        Helper function to check if RR change is happening or not
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    etl_file string indicating the path of etl file
# @param[in]    start_timestamp timestamp in ETL from where verification should be started
# @param[in]    end_timestamp  timestamp in ETL from where verification should end
# @return       status bool True if RR change is detected, None if report generation Failed, False otherwise
def is_rr_changing(adapter: Adapter, panel: Panel, etl_file: str, start_timestamp=None,
                   end_timestamp=None) -> Union[None, bool]:
    status = False
    config = etl_parser.EtlParserConfig()
    config.mmioData = 1
    config.commonData = 1
    logging.info(f"\tGenerating EtlParser Report for {etl_file}")
    if etl_parser.generate_report(etl_file, config) is False:
        logging.error("\tFAILED to generate ETL report")
        return None
    logging.info("\tSuccessfully generated ETL report")

    timing_info = adapter.regs.get_timing_info(panel.transcoder_type)
    h_total = timing_info.HTotal
    if panel.mso_caps.is_mso_supported:
        logging.info(f"This panel is MSO supported so multiplying HTotal with number of segments"
                     f" {panel.mso_caps.no_of_segments}")
        h_total = panel.mso_caps.no_of_segments * h_total
    timing_offsets = adapter.regs.get_timing_offsets(panel.transcoder_type)

    # LinkM1
    mmio_output = etl_parser.get_mmio_data(timing_offsets.LinkM, start_time=start_timestamp, end_time=end_timestamp)
    if mmio_output is not None:
        rr_list = set()
        for link_m_value in mmio_output:
            timing_info = adapter.regs.get_timing_info(panel.transcoder_type,
                                                       TimingOffsetValues(LinkM=link_m_value.Data))
            rr_list.add(link_m_to_hz(adapter, panel, timing_info.LinkM))

        if len(rr_list) > 1:
            logging.info(f"\tRefresh rate change detected with LinkM1 {rr_list}")
            status = True

    vrr_active_region = vrr.get_vrr_active_period(adapter, panel, start_timestamp, end_timestamp)
    if vrr_active_region is None:
        # NO VRR active region found. Skipping further check as MMIO value in VrrVmax and VTotal would be invalid
        return status

    pixel_clock = panel.current_mode.pixelClock_Hz
    vrr_offsets = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    for start, end in vrr_active_region:
        # VrrVmax
        mmio_output = etl_parser.get_mmio_data(vrr_offsets.VrrVmaxReg, start_time=start, end_time=end)
        if mmio_output is not None:
            rr_list = set()
            for data in mmio_output:
                vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrVmaxReg=data.Data))
                rr = round(float(pixel_clock) / ((h_total + 1) * (vrr_info.VrrVmax + 1)), 3)
                rr_list.add(rr)
                logging.debug(f"\tVrrVMax ({hex(data.Offset)})= {vrr_info.VrrVmax} at {data.TimeStamp} ms")
                logging.debug(f"\tPixel Clock= {pixel_clock}Hz, HTotal= {h_total}, RR= {rr}Hz")
            if len(rr_list) > 1:
                logging.info(f"\tRefresh rate change detected with VrrVmax {rr_list}")
                status = True

        # VTotal
        mmio_output = etl_parser.get_mmio_data(timing_offsets.VTotal, start_time=start, end_time=end)
        if mmio_output is not None:
            rr_list = set()
            for data in mmio_output:
                timing_info = adapter.regs.get_timing_info(panel.transcoder_type, TimingOffsetValues(VTotal=data.Data))
                rr = round(float(pixel_clock) / ((h_total + 1) * (timing_info.VTotal + 1)), 3)
                rr_list.add(rr)
                logging.debug(f"\tVTotal ({hex(data.Offset)})= {timing_info.VTotal} at {data.TimeStamp} ms")
                logging.debug(f"\tPixel Clock= {pixel_clock}Hz, HTotal= {h_total}, RR= {rr}Hz")
            if len(rr_list) > 1:
                logging.info(f"\tRefresh rate change detected with VTotal {rr_list}")
                status = True

    return status


##
# @brief        Exposed API to get DRRS is enabled or not in VBT
# @param[in]    adapter Adapter target adapter object
# @param[in]    panel Panel
# @return       True if DRRS enable in VBT, False otherwise
def is_enable_in_vbt(adapter: Adapter, panel: Panel):
    # Check Default VBT configuration first.
    gfx_vbt = vbt.Vbt(adapter.gfx_index)

    # Skip VBT check for unsupported VBT version
    if gfx_vbt.version < 228:
        logging.info("\tDRRS option is not present in VBT version < 228")
        return False

    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")

    if (gfx_vbt.block_44.DRRSEnable[0] & (1 << panel_index)) != (1 << panel_index):
        logging.warning(f"\tDRRS is not enabled in VBT for {panel.port}")
        return False
    logging.info(f"\tDRRS is enabled in VBT for {panel.port}")
    return True


##
# @brief        Exposed API to enable/disable DRRS for any panel in VBT
# @param[in]    adapter target adapter object
# @param[in]    panel object of the targeted display
# @param[in]    enable_drrs bool
# @return       status bool True if drrs is set in VBT, False otherwise
def set_drrs_in_vbt(adapter: Adapter, panel: Panel, enable_drrs: bool) -> bool:
    expected_value = 1 if enable_drrs else 0
    status_str = "Enable" if enable_drrs else "Disable"
    html.step_start(f"Updating VBT to {status_str} DRRS for {panel.port}")

    gfx_vbt = vbt.Vbt(adapter.gfx_index)

    # Skip VBT update for unsupported VBT version
    if gfx_vbt.version < 228 or panel.is_lfp is False:
        logging.info("\tDRRS option is not present in VBT version < 228")
        return True

    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")

    drrs_status = (gfx_vbt.block_44.DRRSEnable[0] & (1 << panel_index)) >> panel_index
    if drrs_status == expected_value:
        logging.info(f"\tDRRS is already {status_str} in VBT")
        html.step_end()
        return True

    if enable_drrs:
        gfx_vbt.block_44.DRRSEnable[0] |= (1 << panel_index)
    else:
        gfx_vbt.block_44.DRRSEnable[0] &= (0 << panel_index)

    if gfx_vbt.apply_changes() is False:
        logging.error("\tFAILED to apply changes in VBT")
        html.step_end()
        return False
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("\tFAILED to restart display driver after VBT update")
        html.step_end()
        return False

    # Verify after restarting the driver
    gfx_vbt.reload(adapter.gfx_index)
    drrs_status = (gfx_vbt.block_44.DRRSEnable[0] & (1 << panel_index)) >> panel_index
    if drrs_status != expected_value:
        logging.error(f"\tFAILED to {status_str} DRRS in VBT")
        html.step_end()
        return False

    logging.info(f"\tSuccessfully {status_str} DRRS in VBT")
    html.step_end()
    return True


##
# @brief        Helper function to verify watermark during DRRS verification
# @param[in]    gfx_index string, gfx adapter instance
# @return       bool, True if Pass, False otherwise
def verify_watermark_drrs(gfx_index):
    html.step_start(f"Watermark Verification started for {gfx_index}")
    watermark = wm.DisplayWatermark()
    if watermark.verify_watermarks(is_48hz_test=True, gfx_index=gfx_index) is False:
        logging.error("FAIL: Watermark verification with DRRS")
        gdhm.report_driver_bug_os(f"[OsFeatures][DRRS]Watermark verification failed with DRRS")
        html.step_end()
        return False
    logging.info("PASS: Watermark verification with DRRS")
    html.step_end()
    return True


##
# @brief        Helper function to verify watermark update during refresh rate switch
# @param[in]    adapter Adapter object
# @param[in]    panel Panel object
# @param[in]    etl_path string path to etl file
# @return       bool, True if Pass, False otherwise
def verify_watermark_during_rr_switch(adapter: Adapter, panel: Panel, etl_path: str):
    if common.PLATFORM_NAME in common.PRE_GEN_15_PLATFORMS:
        logging.info("Skipping verify_watermark_during_rr_switch verification due to HSD-18040160949")
        return True
    else:
        html.step_start(f"Verifying Watermark during RR switch for {panel.port} on {adapter.gfx_index}")
        logging.info(f"\tGenerating EtlParser Report for {etl_path}")
        if etl_parser.generate_report(etl_path, ETL_PARSER_CONFIG) is False:
            logging.error("\tFAILED to generate ETL report")
            return False
        logging.info("\tSuccessfully generated ETL report")

        # WM programming depends on pixel clock hence check only for Clock based panel
        if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.CLOCK:
            rr_list_with_timestamp = get_clock_based_rr(adapter, panel, get_rr_with_timestamp=True)
        else:
            logging.info("\tRR Switching method is not Clock based. Skipping...")
            return True

        if len(rr_list_with_timestamp) <= 1:
            logging.info("\tThere was no RR switch so WM programming will not be done. Skipping...")
            return True

        rr_list = set()
        for values in rr_list_with_timestamp:
            rr_list.add(values[1])

        if len(rr_list) <= 1:
            logging.info("\tThere was no RR switch so WM programming will not be done. Skipping...")
            return True

        logging.debug(f"\tRR List with TimeStamp= {rr_list_with_timestamp}")
        status = True

        frame_ctr_offset = adapter.regs.get_pipe_frame_ctr_offsets(panel.pipe).pipe_frm_cntr_offset
        if common.PLATFORM_NAME not in common.PRE_GEN_13_PLATFORMS + ['DG2']:
            if cmtg.verify_cmtg_status(adapter):
                frame_ctr_offset = MMIORegister.get_instance(
                    "PIPEDMC_FRAMECOUNT_REGISTER", "PIPEDMC_FRAMECOUNT_CMTG_" + panel.pipe, adapter.name).offset

        logging.debug(f"FrameCounter Offset= {hex(frame_ctr_offset)}")
        for current_timestamp, refresh_rate in rr_list_with_timestamp:
            logging.info(f"\tRefresh rate changed to {refresh_rate} Hz at {current_timestamp} ms")
            mmio_output = etl_parser.get_mmio_data(frame_ctr_offset, end_time=current_timestamp)
            if mmio_output is None:
                logging.warning(f"\tNO MMIO data for FrameCounter({hex(frame_ctr_offset)}) till {current_timestamp} ms")
                # Sometimes no frame counter data in the starting of ETL. Keeping threshold to avoid for 500 ms
                if current_timestamp < 500:
                    logging.warning(f"\tTimestamp {current_timestamp} is less than 500 ms. Skipping current iteration")
                    continue
                status &= False
                continue
            # logging.debug(f"MMIO Output Data for Frame CTR before WM - {mmio_output}")
            # Get Frame Counter when RR change happened
            frame_counter_before_rr_change = mmio_output[-1].Data
            logging.info(f"\tFrame counter value= {frame_counter_before_rr_change} before RR changed to {refresh_rate} "
                         f"Hz")

            # Get TimeStamp when WM programming happened
            line_time_offset = MMIORegister.get_instance(
                "WM_LINETIME_REGISTER", "WM_LINETIME_" + panel.pipe, adapter.name).offset
            mmio_output = etl_parser.get_mmio_data(line_time_offset, is_write=True, start_time=current_timestamp)
            if mmio_output is None:
                # We are always getting values for above WM_LINETIME register.Below plane 1 register is just a safety
                # net
                logging.warning(f"NO MMIO data found for WM Line Time{hex(line_time_offset)}. Trying with Plane 1 "
                                f"register")
                wm_plane_1_offset = MMIORegister.get_instance(
                    "PLANE_WM_REGISTER", "PLANE_WM_1_" + panel.pipe, adapter.name).offset
                mmio_output = etl_parser.get_mmio_data(wm_plane_1_offset, is_write=True, start_time=current_timestamp)
                if mmio_output is None:
                    logging.error(f"\t\tNO MMIO data found for PLANE_WM_1_{panel.pipe}({hex(wm_plane_1_offset)})")
                    status &= False
                    continue

            # logging.debug(f"MMIO Output Data for WM - {mmio_output}")
            # Get FrameCounter when WM programming happened
            timestamp_after_wm_update = mmio_output[0].TimeStamp
            mmio_output = etl_parser.get_mmio_data(frame_ctr_offset, end_time=timestamp_after_wm_update)
            frame_counter_after_wm_update = mmio_output[-1].Data

            logging.info(f"\t\tFrame counter value = {frame_counter_after_wm_update} when WM programming is done")
            # logging.debug(f"MMIO Output Data for Frame CTR after WM - {mmio_output}")
            if frame_counter_before_rr_change == frame_counter_after_wm_update:
                logging.info(f"\t\tWM update and RR switch is done in same frame with FrameCounter= {mmio_output[-1].Data}")
            else:
                logging.error("Different FrameCounter for RR and WM programming. "
                              f"RR= {frame_counter_before_rr_change}, WM= {frame_counter_after_wm_update}")
                status &= False

        return status


##
# @brief        Exposed API to verify static DRRS
# @param[in]    expected_rr int value to be expected during SET_TIMING. If no SET_TIMING expected keep it 0
# @return       bool, True if Pass, False otherwise
def verify_static_drrs(expected_rr: int):
    html.step_start(f"Verifying Static DRRS with Expected RR= {'NO Change' if expected_rr == 0 else expected_rr}")
    set_timing_event_output = etl_parser.get_event_data(etl_parser.Events.SET_TIMING)
    if set_timing_event_output is None:
        logging.warning("No Event found for SET_TIMING in ETL")
        if expected_rr == 0:
            logging.info("No RR change happened (Expected)")
            html.step_end()
            return True

        logging.error("No RR change happened (Unexpected)")
        html.step_end()
        return False

    if len(set_timing_event_output) > 1:
        logging.error("\tMore than one SetTiming event entry found (Unexpected)")
        html.step_end()
        return False

    actual_rr = set_timing_event_output[0].RR

    if expected_rr != actual_rr:
        logging.error(f"RR is NOT switched to desired value. Expected= {expected_rr} Hz, Actual= {actual_rr} Hz")
        html.step_end()
        return False

    logging.info(f"RR is switched to desired value. Expected= {expected_rr} Hz, Actual= {actual_rr} Hz")
    html.step_end()
    return True


##
# @brief        Helper API to convert LinkM value to Hz
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    link_m_value int, link M values which needs to be converted to Hz
# @return       Hz float, converted value from linkm
def link_m_to_hz(adapter, panel, link_m_value):
    assert panel
    assert adapter

    timing_info = adapter.regs.get_timing_info(panel.transcoder_type)
    h_total = timing_info.HTotal + 1
    v_total = timing_info.VTotal + 1

    logging.debug(f"Link Rate= {panel.link_rate}, LinkM Value= {link_m_value}, HTotal: {h_total}, VTotal: {v_total}")

    # Old way of RR calculation from linkM: Current RR = (LinkM * MaxRr) / MaxRrLinkM
    # Issue was observed with above method on SINK_EDP108, refer HSD-18017375306
    # New way of getting RR from link_m register value:
    #                   PixelClock100Hz = (LinkM * LinkSymbolClock100Hz * 100000000) / (LinkN * 10000)
    #                   RR = (PixelClock100Hz * 100)/ (HTotal * VTotal)
    link_symbol_clock_100_hz = (panel.link_rate * 1000 * 1000) / 10000
    link_n = 0x80000  # LinkN is a constant for details refer DpProtocolComputeMNTU() in driver code
    pixel_clock_100_hz = round((link_m_value * link_symbol_clock_100_hz * 100000000) / (link_n * 10000))
    pixel_clock = pixel_clock_100_hz * 100
    logging.debug(f"Calculated Pixel Clock= {pixel_clock}")

    return round(pixel_clock / (h_total * v_total), 3)
