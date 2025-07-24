#######################################################################################################################
# @file         vrr.py
# @brief        APIs to enable, disable and verify VRR
#
# @author       Rohit Kumar, Gopikrishnan R
#######################################################################################################################

import ctypes
import logging
import math
import os
import time

from Libs.Core.wrapper import control_api_wrapper, control_api_args
from Libs.Core.wrapper.driver_escape_args import VrrArgs, VrrOperation

from DisplayRegs.DisplayOffsets import VrrOffsetValues, CmtgOffsetValues, InterruptOffsetValues, EmpOffsetValues, \
    PsrOffsetValues
from Libs.Core import etl_parser, driver_escape, registry_access, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm, html
from Libs.Core.sw_sim.driver_interface import DriverInterface
from Libs.Core.test_env import test_context
from Libs.Core.vbt import vbt
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.hdmi.emp_block import HdmiEmpDataBlock
from Libs.Feature.powercons import registry
from Tests.BFR import bfr
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, dut
from Tests.PowerCons.Modules import dpcd
from Tests.PowerCons.Modules.dut_context import Adapter, Panel
from Tests.PowerCons.Modules.dut_context import PRE_GEN_13_PLATFORMS, PRE_GEN_14_PLATFORMS, PRE_GEN_15_PLATFORMS, \
                                                 GEN_14_PLATFORMS, GEN_15_PLATFORMS, GEN_16_PLATFORMS, \
                                                PRE_GEN_16_PLATFORMS
from registers.mmioregister import MMIORegister

VBI_DELTA_TIME_TOLERANCE = 1
VRR_ADAP_BAL_PREDICTION_ERROR_MAX_VALUE_IN_MICRO_SEC = 5000
ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.displayDiagnosticsData = 1
ETL_PARSER_CONFIG.dpcdData = 1
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.vbiData = 1
ETL_PARSER_CONFIG.interruptData = 1
FLIP_ONLY_PARSER_CONFIG = etl_parser.EtlParserConfig()
FLIP_ONLY_PARSER_CONFIG.flipData = 1
MAX_H_ACTIVE_SUPPORTED = 5120
MAX_V_ACTIVE_SUPPORTED = 4320
VBLANK_MAX_DURATION = 0xFFFFFFFF
LATENCY_SAGV = 0x4578C

ARC_SYNC_PROFILE = control_api_args.ctl_intel_arc_sync_profile_v

__display_config = display_config.DisplayConfiguration()

panel_adapter_active_duration = {}

lnl_cdclock_ctl_freq_dict = dict([
    (153.6, 985),
    (172.8, 875),
    (192, 788),
    (211.2, 716),
    (230.4, 657),
    (249.6, 606),
    (268.8, 563),
    (288, 525),
    (307.2, 493),
    (330, 459),
    (360, 420),
    (390, 388),
    (420, 360),
    (450, 336),
    (480, 315),
    (487.2, 311),
    (522, 290),
    (556.8, 272),
    (571.2, 265),
    (612, 248),
    (652.8, 232)
])

ptl_cdclock_ctl_freq_dict = dict([
    (153.6, 421.875),
    (172.8, 375),
    (192, 337.5),
    (211.2, 306.81),
    (230.4, 281.25),
    (249.6, 259.61),
    (268.8, 241.07),
    (288, 225),
    (307.2, 210.93),
    (326.4, 198.52),
    (345.6, 187.5),
    (364.8, 177.63),
    (384, 168.75),
    (403.2, 160.71),
    (422.4, 153.41),
    (441.6, 146.74),
    (460.8, 140.625),
    (480, 135),
    (499.2, 129.81),
    (518.4, 125),
    (537.6, 120.53),
    (556.8, 116.37),
    (576, 112.5),
    (595.2, 108.87),
    (614.4, 105.46),
    (633.6, 102.27),
    (652.8, 99.26),
    (672, 96.42),
    (691.2, 93.75)
])


##
# @brief        Helper function to report bug to GDHM in case of VRR escape call failure
def __report_to_gdhm():
    gdhm.report_test_bug_os(
        title="[OsFeatures][VRR] Failed to change VRR settings with escape calls",
        priority=gdhm.Priority.P3,
        exposure=gdhm.Exposure.E3
    )


##
# @brief        Exposed API to enable VRR
# @param[in]    adapter Adapter target adapter object
# @param[in]    is_low_fps [optional] to enable/disable LOW FPS solution with VRR
# @param[in]    is_high_fps [optional] to enable/disable HIGH FPS solution with VRR
# @return       True if operation is successful, False otherwise
def enable(adapter: Adapter, is_low_fps=False, is_high_fps=False):
    # Make sure VRR is enabled in VBT
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    if gfx_vbt.version >= 233:
        for port, panel in adapter.panels.items():
            if panel.is_lfp is False:
                continue
            panel_index = gfx_vbt.get_lfp_panel_type(port)
            logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")
            if (gfx_vbt.block_44.VRR[0] & (1 << panel_index)) >> panel_index == 0:
                logging.warning("\tVRR was disabled in VBT")
                gfx_vbt.block_44.VRR[0] |= (1 << panel_index)
                if gfx_vbt.apply_changes() is False:
                    logging.error("\tFailed to apply changes to VBT")
                    return False
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    logging.error("\tFailed to restart display driver after VBT update")
                    return False
                # Verify after restarting the driver
                gfx_vbt.reload()
                if (gfx_vbt.block_44.VRR[0] & (1 << panel_index)) >> panel_index == 0:
                    logging.error("\tFailed to enable VRR in VBT")
                    return False
                logging.info(f"\tPASS: Enabled VRR in VBT successfully {port}")
            else:
                logging.info(f"\tPASS: VRR is enabled in VBT for {port}")

    # Make sure VRR is enabled from registry key
    status = registry.write(adapter.gfx_index, registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_ENABLE,
                            registry_access.RegDataType.DWORD, registry.RegValues.ENABLE)
    if status is False:
        logging.error(f"\tFAIL: Failed to update registry key {registry.RegKeys.VRR.VRR_ADAPTIVE_VSYNC_ENABLE}")
        return False

    if status is None:
        logging.info("\tPASS: VRR is enabled in registry")

    if status:
        logging.warning("\tVRR was disabled in registry key")
        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            logging.error("\tFailed to restart display driver after registry update")
            return False
        logging.info("\tPASS: Enabled VRR in registry successfully")

    # Get the current VRR configuration
    vrr_args = VrrArgs()
    vrr_args.operation = VrrOperation.GET_INFO.value
    vrr_flag, vrr_args = driver_escape.get_set_vrr(adapter.gfx_index, vrr_args)
    if not vrr_flag:
        logging.error(f"Escape call failed to get VRR for {adapter.gfx_index}")

    # Enable VRR if not enabled
    if vrr_args.vrrEnabled is False:
        vrr_args.operation = VrrOperation.ENABLE.value
        vrr_flag, vrr_args = driver_escape.get_set_vrr(adapter.gfx_index, vrr_args)
        if not vrr_flag:
            logging.error(f"Escape call failed to set VRR for {adapter.gfx_index}")
        vrr_args = VrrArgs()
        vrr_args.operation = VrrOperation.GET_INFO.value
        vrr_flag, vrr_args = driver_escape.get_set_vrr(adapter.gfx_index, vrr_args)
        if not vrr_flag:
            logging.error(f"Escape call failed to get VRR for {adapter.gfx_index}")
        if vrr_args.vrrEnabled is False:
            __report_to_gdhm()
            logging.error("\tFailed to enable VRR")
            return False

    logging.info(f"\tPASS: {'VRR Status':<40} Expected= ENABLED, Actual= ENABLED")

    # Handle Low FPS solution setting
    if is_low_fps != vrr_args.vrrLowFpsSolnEnabled:
        vrr_args.operation = VrrOperation.LOW_FPS_DISABLE.value
        if is_low_fps:
            vrr_args.operation = VrrOperation.LOW_FPS_ENABLE.value
        vrr_flag, vrr_args = driver_escape.get_set_vrr(adapter.gfx_index, vrr_args)
        if not vrr_flag:
            logging.error(f"Escape call failed to set VRR for {adapter.gfx_index}")
        vrr_args = VrrArgs()
        vrr_args.operation = VrrOperation.GET_INFO.value
        vrr_flag, vrr_args = driver_escape.get_set_vrr(adapter.gfx_index, vrr_args)
        if not vrr_flag:
            logging.error(f"Escape call failed to get VRR for {adapter.gfx_index}")
        if is_low_fps != vrr_args.vrrLowFpsSolnEnabled:
            __report_to_gdhm()
            logging.error("\tFailed to {0} VRR Low FPS Solution".format("enabled" if is_low_fps else "disabled"))
            return False

    status = "ENABLED" if is_low_fps else "DISABLED"
    logging.info(f"\tPASS: {'VRR Low FPS Solution':<40} Expected= {status}, Actual= {status}")

    # Handle High FPS solution setting
    if is_high_fps != vrr_args.vrrHighFpsSolnEnabled:
        vrr_args.operation = VrrOperation.HIGH_FPS_DISABLE.value
        if is_high_fps:
            vrr_args.operation = VrrOperation.HIGH_FPS_ENABLE.value
        vrr_flag, vrr_args = driver_escape.get_set_vrr(adapter.gfx_index, vrr_args)
        if not vrr_flag:
            logging.error(f"Escape call failed to set VRR for {adapter.gfx_index}")
        vrr_args = VrrArgs()
        vrr_args.operation = VrrOperation.GET_INFO.value
        vrr_flag, vrr_args = driver_escape.get_set_vrr(adapter.gfx_index, vrr_args)
        if not vrr_flag:
            logging.error(f"Escape call failed to get VRR for {adapter.gfx_index}")
        if is_high_fps != vrr_args.vrrHighFpsSolnEnabled:
            __report_to_gdhm()
            logging.error("\tFailed to {0} VRR High FPS Solution".format("enabled" if is_high_fps else "disabled"))
            return False

    status = "ENABLED" if is_high_fps else "DISABLED"
    logging.info(f"\tPASS: {'VRR High FPS Solution':<40} Expected= {status}, Actual= {status}")

    if adapter.name not in PRE_GEN_13_PLATFORMS:
        if update_sdp_support(adapter, True) is False:
            return False
    return True


##
# @brief        Exposed API to check VRR enabled in VBT or not
# @param[in]    adapter Adapter target adapter object
# @param[in]    panel Panel
# @return       True if VRR enable in VBT, False otherwise
def is_enable_in_vbt(adapter: Adapter, panel: Panel):
    # Check Default VBT configuration first.
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    if gfx_vbt.version < 233:
        logging.info("\tVRR option is not present in VBT version < 233")
        return False
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")
    if (gfx_vbt.block_44.VRR[0] & (1 << panel_index)) >> panel_index == 0:
        logging.warning(f"\tVRR is not enabled in VBT for {panel.port}")
        return False
    # return True in case enable
    logging.info(f"\tVRR is enabled in VBT for {panel.port}")
    return True


##
# @brief        Exposed API to enable/disable VRR SDP support
# @param[in]    adapter Adapter target adapter object
# @param[in]    enable [optional], to enable/disable sdp support with VRR
# @return       True if operation is successful, False otherwise
def update_sdp_support(adapter: Adapter, enable=True):
    display_feature_control = registry.DisplayFeatureControl(adapter.gfx_index)
    val = 0x0 if enable else 0x1

    if display_feature_control.disable_adaptive_sync_sdp != val:
        display_feature_control.disable_adaptive_sync_sdp = val
        status = display_feature_control.update(adapter.gfx_index)
        if status is False:
            logging.error("\tFAILED to update VRR SDP support for enable= {0}".format(enable))
            return False
        logging.info("\tSuccessfully updated VRR SDP support for enable= {0}".format(enable))
        if status:
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                return False
    else:
        logging.info("\tVRR SDP support is already enable= {0}".format(enable))
    return True


##
# @brief        Exposed API to disable VRR
# @param[in]    adapter Adapter target adapter object
# @return       True if operation is successful, False otherwise
def disable(adapter=None):
    gfx_index = 'gfx_0'
    if adapter is not None:
        gfx_index = adapter.gfx_index

    logging.info("STEP: Disabling VRR on {0}".format(gfx_index))
    # Get the current VRR configuration
    vrr_args = VrrArgs()
    vrr_args.operation = VrrOperation.GET_INFO.value
    vrr_flag, vrr_args = driver_escape.get_set_vrr(gfx_index, vrr_args)
    if not vrr_flag:
        logging.error(f"Escape call failed to get VRR for {gfx_index}")

    # Disable VRR if not disabled
    if vrr_args.vrrEnabled:
        vrr_args.operation = VrrOperation.DISABLE.value
        vrr_flag, vrr_args = driver_escape.get_set_vrr(gfx_index, vrr_args)
        if not vrr_flag:
            logging.error(f"Escape call failed to set VRR for {gfx_index}")

        vrr_args = VrrArgs()
        vrr_args.operation = VrrOperation.GET_INFO.value
        vrr_flag, vrr_args = driver_escape.get_set_vrr(gfx_index, vrr_args)
        if not vrr_flag:
            logging.error(f"Escape call failed to get VRR for {gfx_index}")

        if vrr_args.vrrEnabled:
            logging.error("\tFAIL: VRR Status Expected= DISABLED, Actual= ENABLED")
            __report_to_gdhm()
            return False

    logging.info("\tPASS: VRR Status Expected= DISABLED, Actual= DISABLED")

    return True


##
# @brief        Helper function to get VRR active period time stamps from ETL
# @param[in]    adapter - Adapter target adapter object
# @param[in]    panel Panel
# @param[in]    start optional, start time
# @param[in]    end optional, end time
# @param[in]    consider_iscurrent - True if iscurent consider for disable event , false by default.
# @return       a list of tuples (vrr_active_start_time_stamp, vrr_active_end_time_stamp) if VRR enable/disable
#               trace events are present in ETL, None otherwise
def get_vrr_active_period(adapter: Adapter, panel: Panel, start=None, end=None, consider_iscurrent=False):
    # If we have request cached with same params then return the cached data
    if start is None and end is None and consider_iscurrent is False:
        keyToCheck = adapter.name + str(panel.target_id)
        if keyToCheck in panel_adapter_active_duration:
            return panel_adapter_active_duration[keyToCheck]

    output = []

    vrr_enable_disable_event_output = etl_parser.get_event_data(etl_parser.Events.RR_SWITCH_INFO, start, end)
    # Filter out enable event data for targeted display
    vrr_enable_event_output = [
        _ for _ in vrr_enable_disable_event_output
        if _.TargetId == panel.target_id and ((_.RrMode == "DD_REFRESH_RATE_MODE_VARIABLE") and _.IsCurrent)]

    if vrr_enable_event_output is None:
        logging.error(f"No VRR enable events found in ETL")
        return None

    vrr_disable_event_output = []
    if consider_iscurrent:
        # Filter out event data for targeted display
        vrr_disable_event_output = [_ for _ in vrr_enable_disable_event_output if _.TargetId == panel.target_id and
                                    (_.RrMode != "DD_REFRESH_RATE_MODE_VARIABLE") and _.IsCurrent]
    else:
        # Filter out event data for targeted display
        vrr_disable_event_output = [_ for _ in vrr_enable_disable_event_output if _.TargetId == panel.target_id and
                                    (_.RrMode != "DD_REFRESH_RATE_MODE_VARIABLE")]
    if vrr_disable_event_output is None:
        logging.error(f"No VRR disable events found in ETL")
        return None

    for entry_index in range(len(vrr_enable_event_output)):
        time_stamp = None
        for exit_entry in vrr_disable_event_output:
            if entry_index < len(vrr_enable_event_output) - 1:
                if vrr_enable_event_output[entry_index].TimeStamp < exit_entry.TimeStamp < \
                        vrr_enable_event_output[entry_index + 1].TimeStamp:
                    if time_stamp is None:
                        time_stamp = exit_entry.TimeStamp
                    break
            else:
                if vrr_enable_event_output[entry_index].TimeStamp < exit_entry.TimeStamp:
                    if time_stamp is None:
                        time_stamp = exit_entry.TimeStamp
                    break

        if time_stamp is not None:
            output.append((vrr_enable_event_output[entry_index].TimeStamp, time_stamp))

    final_output = []
    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    for vrr_active_start, vrr_active_end in output:
        # reading status register and update start time based on Vrr enable live status
        vrr_status_output = etl_parser.get_mmio_data(vrr_regs.VrrStatus,
                                                     start_time=vrr_active_start, end_time=vrr_active_end)
        if vrr_status_output is None:
            logging.error(
                "\t\tNo MMIO operation found for TRANS_VRR_STATUS_REGISTER for VRR active period "
                "({0}, {1})".format(vrr_active_start, vrr_active_end))
            gdhm.report_driver_bug_os("[OsFeatures][VRR] No MMIO operation found for TRANS_VRR_STATUS_REGISTER for "
                                      "VRR active period")
        else:
            for mmio_data in vrr_status_output:
                vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrStatus=mmio_data.Data))
                if vrr_info.VrrEnableLive is True:
                    final_output.append((mmio_data.TimeStamp, vrr_active_end))
                    break

    if len(final_output) == 0:
        return None

    # Cache the output as we receive multiple request with same params
    if start is None and end is None:
        keyToSet = adapter.name + str(panel.target_id)
        panel_adapter_active_duration[keyToSet] = final_output

    return final_output


##
# @brief        Helper function to check flip size greater then max plane size.
# @param[in]    left, SourceLeft value of requested flip
# @param[in]    top, SourceTop value of requested flip
# @param[in]    right, SourceRight value of requested flip
# @param[in]    bottom, SourceBottom value of requested flip
# @return       Boolean, True if plane size greater then max plane size, else False
def __is_flip_on_dual_pipe(left, top, right, bottom):
    h_size = right - left
    v_size = bottom - top
    return h_size >= MAX_H_ACTIVE_SUPPORTED or v_size >= MAX_V_ACTIVE_SUPPORTED


##
# @brief        Helper function to check async flip requests from OS for given display
# @details
#               ***** Win RS5 or before *****
#               Async Flip -> SyncInterval= 0, TearingFlag= FlipImmediate
#               Sync Flip  -> SyncInterval= 1, TearingFlag= FlipOnNextVSync
#               VRR Trigger -> Async Flips
#               VRR Enabled:
#                   * Sync flips will always be submitted as Sync
#                   * If Low/High FPS solutions are disabled
#                       * Async flips will be converted to Sync flips
#                   * If Low/High FPS solutions are enabled
#                       * Async flips below MaxRR will be converted to Sync
#                       * Async flips above MaxRR will be submitted as Async
#               VRR Disabled:
#                   * No change
#
#
#               ***** Win 19H1 onwards *****
#               Async Flip -> SyncInterval= 0, TearingFlag= FlipImmediate
#               Sync Flip  -> SyncInterval= 1, TearingFlag= FlipOnNextVSync
#               VRR Flip   -> SyncInterval= 0, TearingFlag= FlipImmediateNoTearing, Duration= The length of time,
#                             in units of 100 nanoseconds, between when the current present operation flips to the
#                             screen and the next VBI occurs. If zero, the refresh rate should be the default rate
#                             based on the current mode.
#               VRR Trigger -> Duration= DURATION_MAX
#               VRR Enabled:
#                   * Sync flips will always be submitted as Sync
#                   * VRR flips will always be submitted as Sync
#                   * Async flips will always be submitted as Async
#               VRR Disabled:
#                   * No change
#
#
# @param[in]    panel, Panel, panel object of the targeted display
# @param[in]    expected_vrr, Boolean indicating if vrr is expected
# @param[in]    is_high_fps, Boolean, True if test is meant for HIGH_FPS setting
# @param[in]    is_os_aware_vrr, Boolean, True for 19H1 or latest
# @param[in]    is_negative_test, Boolean
# @return       status, True if async flip happened on given display for VRR enabled case, False otherwise
def __check_async_flip(panel, expected_vrr, is_high_fps, is_os_aware_vrr, is_negative_test):
    pipe = 'PIPE_' + panel.pipe
    status = True

    # Get flip data from EtlParser for given source ID
    flip_data = etl_parser.get_flip_data(sourceid=panel.source_id)

    if flip_data is None:
        logging.warning("\tNo flip data found for {0} in EtlParser Report".format(panel.source_id))
        if expected_vrr is False:
            return True
        return False

    flip_in_async_count = 0
    flip_in_sync_count = 0
    flip_in_vrr_count = 0
    flip_out_async_count = 0
    flip_out_sync_count = 0
    flip_on_master_pipe = 0
    flip_on_slave_pipe = 0
    is_flipon_dualpipe = False
    durations = {}
    for flip in flip_data:
        if flip.Duration is not None:
            if flip.Duration in durations.keys():
                durations[flip.Duration] += 1
            else:
                durations[flip.Duration] = 1

        for plane_info in flip.PlaneInfoList:
            if "FlipImmediateNoTearing" in plane_info.Flags:
                flip_in_vrr_count += 1
            elif "FlipImmediate" in plane_info.Flags:
                flip_in_async_count += 1
            else:
                flip_in_sync_count += 1

        for plane_details in flip.PlaneDetailsList:
            if (panel.pipe_joiner_tiled_caps.is_pipe_joiner_require is True) or \
                    (panel.pipe_joiner_tiled_caps.is_tiled_panel is True):
                is_flipon_dualpipe = __is_flip_on_dual_pipe(plane_details.SrcLeft, plane_details.SrcTop,
                                                            plane_details.SrcRight, plane_details.SrcBottom)
            break

        if flip.IsAddressOnly:
            for flip_address_only in flip.FlipAddressList:
                if flip_address_only.Async:
                    flip_out_async_count += 1
                else:
                    flip_out_sync_count += 1
                    # collecting details of output/submitted flip on master and slave pipe in case of pipe joiner
                    if ((panel.pipe_joiner_tiled_caps.is_pipe_joiner_require is True) or
                        (panel.pipe_joiner_tiled_caps.is_tiled_panel is True)) and is_flipon_dualpipe:
                        if flip_address_only.Pipe == panel.pipe_joiner_tiled_caps.master_pipe:
                            flip_on_master_pipe += 1
                        elif flip_address_only.Pipe == panel.pipe_joiner_tiled_caps.slave_pipe:
                            flip_on_slave_pipe += 1
        else:
            flip_out_sync_count += 1
            for flip_all_param in flip.FlipAllParamList:
                if ((panel.pipe_joiner_tiled_caps.is_pipe_joiner_require is True) or
                    (panel.pipe_joiner_tiled_caps.is_tiled_panel is True)) and is_flipon_dualpipe:
                    if flip_all_param.Pipe == panel.pipe_joiner_tiled_caps.master_pipe:
                        flip_on_master_pipe += 1
                    elif flip_all_param.Pipe == panel.pipe_joiner_tiled_caps.slave_pipe:
                        flip_on_slave_pipe += 1

    if is_os_aware_vrr:
        logging.info(
            "\tFlips on {0}: INCOMING -> [Sync= {1}, Async= {2}, Vrr= {3}], SUBMITTED -> [Sync= {4}, Async= {5}]"
            "".format(
                pipe, flip_in_sync_count, flip_in_async_count, flip_in_vrr_count, flip_out_sync_count,
                flip_out_async_count))
    else:
        logging.info(
            "\tFlips on {0}: INCOMING -> [Sync= {1}, Async= {2}], SUBMITTED -> [Sync= {3}, Async= {4}]".format(
                pipe, flip_in_sync_count, flip_in_async_count, flip_out_sync_count, flip_out_async_count))

    incoming_flips = flip_in_sync_count + flip_in_async_count + flip_in_vrr_count
    outgoing_flips = flip_out_sync_count + flip_out_async_count

    logging.info(
        f"\tDifference between incoming and submitted flips= "
        f"{abs(outgoing_flips - incoming_flips)} "
        f"({round((abs(outgoing_flips - incoming_flips) * 100) / incoming_flips, 2)}%)")

    if bool(durations):
        logging.info("\tDuration on {0}: {1}".format(pipe, durations))

    # With VRR disabled, there should not be any change in flip type
    if not expected_vrr:
        # Incoming async flips should be submitted as Async
        if flip_in_async_count > 0:
            if flip_out_async_count == 0:
                logging.error("\tFAIL: Expected submitted Async Flips= {0}, Actual= 0".format(flip_in_async_count))
                status = False
            else:
                logging.info("\tPASS: Expected submitted Async Flips= {0}, Actual= {1}".format(
                    flip_in_async_count, flip_out_async_count))
        else:
            # No incoming async flip. No flip should be submitted as ASync.
            if flip_out_async_count != 0:
                logging.error("\tFAIL: Expected submitted Async Flips= 0, Actual= {0}".format(flip_out_async_count))
                status = False
            else:
                logging.info("\tPASS: Expected submitted Async Flips= 0, Actual= 0")

    else:
        # In NO_LOW_HIGH_FPS and LOW_FPS settings, number of submitted async flips should be zero
        # if there is no incoming FlipImmediate flip
        if (is_high_fps is False) and (0 == flip_in_async_count):
            if flip_out_async_count != 0:
                logging.error("\tFAIL: HIGH_FPS DISABLED: Expected submitted Async flips= 0, Actual= {0}".format(
                    flip_out_async_count))
                status = False
            else:
                logging.info("\tPASS: HIGH_FPS DISABLED: Expected submitted Async flips= 0, Actual= 0")

        # In HIGH_FPS and LOW_HIGH_FPS settings, number of submitted async flips should be non-zero if FPS is
        # higher than max RR. Also, Async flips should not be converted to sync flips.
        if is_high_fps is True:
            if flip_out_async_count == 0:
                logging.warning("\tHIGH_FPS ENABLED: Expected submitted Async flips > 0, Actual= 0")
            else:
                logging.info("\tPASS: HIGH_FPS ENABLED: Expected submitted Async flips > 0, Actual= {0}".format(
                    flip_out_async_count))

        # In Pipe joiner case , Sync flip submitted on both pipe for one incoming flip. checking count for both pipe
        # should be same.
        if (panel.pipe_joiner_tiled_caps.is_pipe_joiner_require is True) or \
                (panel.pipe_joiner_tiled_caps.is_tiled_panel is True):
            if flip_on_master_pipe == flip_on_slave_pipe:
                logging.info("\tPASS: Sync Flips on PIPE_{} = {} and PIPE_{} = {} are Same ".
                             format(panel.pipe_joiner_tiled_caps.master_pipe, flip_on_master_pipe,
                                    panel.pipe_joiner_tiled_caps.slave_pipe, flip_on_slave_pipe))
            else:
                # logging GDHM and not failing test case as we are seeing sporadic failure.
                logging.error("\tFAIL: Sync Flips on PIPE_{} = {} and PIPE_{} = {} are not Same".
                              format(panel.pipe_joiner_tiled_caps.master_pipe, flip_on_master_pipe,
                                     panel.pipe_joiner_tiled_caps.slave_pipe, flip_on_slave_pipe))
                logging.info(
                    f"\tDifference between incoming and submitted flips= "
                    f"{abs(flip_on_master_pipe - flip_on_slave_pipe)} ")

                if abs(flip_on_master_pipe - flip_on_slave_pipe) > 5:
                    gdhm.report_driver_bug_os(
                        title="Flips on Master and slave pipes are not same  in case of pipe joiner",
                        priority=gdhm.Priority.P3,
                        exposure=gdhm.Exposure.E3
                    )

    # If VRR is expected to be enabled, incoming async flip count is not expected to be 0
    if expected_vrr and (flip_in_async_count == 0 and flip_in_vrr_count == 0):
        if is_negative_test is False:
            gdhm.report_test_bug_os(
                title="[OsFeatures][VRR] OS is not sending async flips during VRR game playback",
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
        logging.error("\tOS is not sending Async flips")
        status = False

    return status


##
# @brief        Verifies all VRR register programming for the display supplied
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @param[in]    v_min expected VRR v_min value
# @param[in]    v_max expected VRR v_max value
# @param[in]    drrs_v_max expected DRRS V_MAX value
# @param[in]    dc_balance_event_expected boolean, True DC balance event expected, False DC balance disable.
# @param[in]    vmax_flipline_for_each_flip, True if vmax for each flip verification require.
# @return       status, True if verification is successful, False otherwise
def __check_vmin_vmax(adapter: Adapter, panel: Panel, v_min, v_max, drrs_v_max, dc_balance_event_expected,
                      vmax_flipline_for_each_flip):
    status = True

    # Verify VRR V_MIN
    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    vrr_active_period = get_vrr_active_period(adapter, panel)
    if vrr_active_period is None:
        logging.error("\t\tNo VRR active period found")
        return False
    for vrr_active_start, vrr_active_end in vrr_active_period:
        min_vrr_active_period = 5 * math.floor(1000.0 / panel.min_rr)
        # Skip if VRR active period is too short  less then 5 flips
        if (vrr_active_end - vrr_active_start) <= min_vrr_active_period:
            logging.debug(f"\t\tVrr active periods is short = {vrr_active_start} to {vrr_active_end} time - skipping it")
            continue
        # Get all the write operations on given offset
        mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrVminReg, is_write=True,
                                               start_time=vrr_active_start,
                                               end_time=vrr_active_end)

        if mmio_output is None:
            logging.warning("\tNo MMIO entry found for register TRANS_VRR_V_MIN_" + panel.transcoder)
        else:
            previous_trans_vrr_v_min = None
            for mmio_data in mmio_output:
                vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrVminReg=mmio_data.Data))

                if v_min <= vrr_info.VrrVmin <= v_max:
                    if previous_trans_vrr_v_min is None or previous_trans_vrr_v_min != v_min:
                        logging.info('\tPASS: TRANS_VRR_V_MIN_%s: V_MIN Expected= [%d, %d], Actual= %d' % (
                            panel.transcoder, v_min, v_max, vrr_info.VrrVmin))
                        previous_trans_vrr_v_min = vrr_info.VrrVmin
                else:
                    logging.error(
                        '\tFAIL: TRANS_VRR_V_MIN_%s: V_MIN Expected= [%d, %d], Actual= %d (TimeStamp = %d)' % (
                            panel.transcoder, v_min, v_max, vrr_info.VrrVmin, mmio_data.TimeStamp))
                    status = False
        # from Gen 16 onwards, HW DC balance use except HDMI 2.1 TMDS.
        # @todo need to remove below tmds check post PTL B0 PO
        if adapter.name in PRE_GEN_16_PLATFORMS or (adapter.name in GEN_16_PLATFORMS and
                                                    panel.hdmi_2_1_caps.is_hdmi_2_1_tmds):
            # Verify VRR V_MAX
            # Get all the write operations on given offset
            mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrVmaxReg, is_write=True,
                                                   start_time=vrr_active_start,
                                                   end_time=vrr_active_end)
            if mmio_output is None:
                # fail test case in case of DC balance enable, Vmax and flipline need to program for each scanline/Flip
                if dc_balance_event_expected:
                    logging.error("\tFAIL: No MMIO entry found for register TRANS_VRR_V_MAX_" + panel.transcoder)
                    status = False
                else:
                    logging.warning("\tNo MMIO entry found for register TRANS_VRR_V_MAX_" + panel.transcoder)
            else:
                previous_trans_vrr_v_max = None
                reduced_v_max_count = 0
                for mmio_data in mmio_output:
                    vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                         VrrOffsetValues(VrrVmaxReg=mmio_data.Data))
                    if v_min <= vrr_info.VrrVmax <= v_max + 1 or drrs_v_max <= vrr_info.VrrVmax <= drrs_v_max + 1:
                        if vrr_info.VrrVmin < v_max:
                            reduced_v_max_count += 1
                        if previous_trans_vrr_v_max is None or \
                                previous_trans_vrr_v_max != vrr_info.VrrVmax:
                            previous_trans_vrr_v_max = vrr_info.VrrVmax
                    else:
                        logging.error('\tFAIL: TRANS_VRR_V_MAX_%s: V_MAX Expected= [%d, %d], Actual= %d '
                                      '(TimeStamp= %d)' % (panel.transcoder, v_min, v_max + 1, vrr_info.VrrVmax,
                                                           mmio_data.TimeStamp))
                        status = False

                reduced_v_max_percent = round((reduced_v_max_count * 100) / len(mmio_output), 2)
                logging.info(
                    f"\tTotal VMax Updates= {len(mmio_output)}, "
                    f"Reduced(<{v_max})= {reduced_v_max_count}({reduced_v_max_percent} %)")

                if dc_balance_event_expected and vmax_flipline_for_each_flip:
                    # Vmax should get program for each flip if panel is not in AlwaysInVRRMode.
                    if panel.vrr_caps.is_always_vrr_mode is False:
                        flip_data = etl_parser.get_flip_data(async_flip=True, vrr_flip=True,
                                                             start_time=vrr_active_start,
                                                             end_time=vrr_active_end,
                                                             sourceid=panel.source_id)
                        # Check for flip length if active duration is very small observed issue as denominator is small
                        if len(flip_data) > 300:
                            vmax_for_each_flip = round(len(mmio_output)*100/len(flip_data), 2)
                            if int(vmax_for_each_flip) < 60:
                                logging.error(f"\t\t Vmax register not program for each flip, actual program for "
                                              f"{vmax_for_each_flip}% of flip")
                                status = False
                            else:
                                logging.info(f"\t\t Vmax register program for {vmax_for_each_flip}% of flip")
                    # Vmax should ger program for each scanline interrupt during VRR active for AlwaysInVRRMode
                    else:
                        # check for each scanline interrupt.
                        interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_SCANLINEINTERRUPT,
                                                                       start_timestamp=vrr_active_start,
                                                                       end_timestamp=vrr_active_end)

                        # Driver should program Vmax register for each scanline interrupt during vrr active
                        vmax_for_each_scanline = round(len(mmio_output) * 100 / len(interrupt_data), 2)
                        if int(vmax_for_each_scanline) < 100:
                            logging.error(f"\t\t Vmax register not program for each scanline interrupt, actual program"
                                          f"for {vmax_for_each_scanline}% of scanline interrupt")
                        else:
                            logging.info(f"\t\t Vmax register program for {vmax_for_each_scanline}% of interrupt")
        # HW DCB register need to program in case of Gen16 (Xe3) onwards.
        else:
            # Verify VRR V_MAX_DCB
            # Get all the write operations on given offset
            mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrDcbVmaxReg, is_write=True,
                                                   start_time=vrr_active_start,
                                                   end_time=vrr_active_end)
            if mmio_output is None:
                # fail test case in case of DC balance enable, Vmax_dcb and flipline_dcb need to program for each flip
                if dc_balance_event_expected:
                    logging.error(f"\tFAIL: No MMIO entry found for register TRANS_VRR_V_MAX_DCB_{panel.transcoder} "
                                  f"between {vrr_active_start} to {vrr_active_end}" )
                    status = False
                else:
                    logging.warning("\tNo MMIO entry found for register TRANS_VRR_V_MAX_DCB" + panel.transcoder)
            else:
                previous_trans_vrr_v_max = None
                reduced_v_max_count = 0
                for mmio_data in mmio_output:
                    vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                         VrrOffsetValues(VrrDcbVmaxReg=mmio_data.Data))
                    if v_min <= vrr_info.VrrDcbVmax <= v_max + 1 or drrs_v_max <= vrr_info.VrrDcbVmax <= drrs_v_max + 1:
                        if vrr_info.VrrDcbVmax < v_max:
                            reduced_v_max_count += 1
                        if previous_trans_vrr_v_max is None or \
                                previous_trans_vrr_v_max != vrr_info.VrrDcbVmax:
                            previous_trans_vrr_v_max = vrr_info.VrrDcbVmax
                    else:
                        logging.error('\tFAIL: TRANS_VRR_V_MAX_DCB_%s: V_MAX Expected= [%d, %d], Actual= %d '
                                      '(TimeStamp= %d)' % (panel.transcoder, v_min, v_max + 1, vrr_info.VrrDcbVmax,
                                                           mmio_data.TimeStamp))
                        status = False

                reduced_v_max_percent = round((reduced_v_max_count * 100) / len(mmio_output), 2)
                logging.info(
                    f"\tTotal VMax Updates= {len(mmio_output)}, "
                    f"Reduced(<{v_max})= {reduced_v_max_count}({reduced_v_max_percent} %)")

                # failing currently, need to enable post driver issue fix
                '''if dc_balance_event_expected:
                    # Vmax should ger program for each scanline interrupt during VRR active for AlwaysInVRRMode
                    # check for each scanline interrupt.
                    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_SCANLINEINTERRUPT,
                                                                   start_timestamp=vrr_active_start,
                                                                   end_timestamp=vrr_active_end)

                    # Driver should program Vmax register for each scanline interrupt during vrr active
                    vmax_for_each_scanline = round(len(mmio_output) * 100 / len(interrupt_data), 2)
                    if int(vmax_for_each_scanline) <= 90:
                        logging.error(f"\t\t VmaxDCB register not program for each scanline interrupt, actual program"
                                      f"for {vmax_for_each_scanline}% of scanline interrupt")
                    else:
                        logging.info(f"\t\t VmaxDCB register program for {vmax_for_each_scanline}% of interrupt")'''

    return status


##
# @brief        Verifies all VRR register programming for the display supplied
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @param[in]    v_min expected VRR v_min value
# @param[in]    drrs_v_max expeced VRR drrs_v_max value
# @return       status, True if verification is successful, False otherwise
def __check_vmin_vmax_modeset(adapter: Adapter, panel: Panel, v_min, drrs_v_max):
    status = True
    gdhm_error = set()
    is_write_or_read = True  # true for Write and False for read
    # return in case of pre gen13 platforms and LFP panel ( not in Always VRR mode)
    if not panel.vrr_caps.is_always_vrr_mode:
        logging.info("not in Always VRR mode returning early")
        return status
    ctl_interrupt_found = False
    # getting CTL interrupt data
    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                   etl_parser.InterruptType.CRTC_VSYNC)
    if interrupt_data is not None:
        for interrupt in interrupt_data:
            if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.DISABLE_NO_PHASE]:
                ctl_interrupt_found = True
                break
    # Get the first mode set happened after opening the app if any
    set_timing_data = etl_parser.get_event_data(etl_parser.Events.SET_TIMING)
    if set_timing_data is None:
        logging.info("No physical modeset, virtual modeset happen, considering read value")
        is_write_or_read = False  # update value to false as no physcial modeset
    # Verify VRR V_MIN
    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    # Get all the write operations on given offset
    mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrVminReg, is_write=is_write_or_read)

    if mmio_output is None:
        logging.warning("\tNo MMIO entry found for register TRANS_VRR_V_MIN_" + panel.transcoder)
        status &= False
    else:
        for mmio_data in mmio_output:
            vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrVminReg=mmio_data.Data))

            if v_min == vrr_info.VrrVmin:
                logging.info('\tPASS: TRANS_VRR_V_MIN_%s: V_MIN Expected= %d, Actual= %d' % (
                    panel.transcoder, v_min, vrr_info.VrrVmin))
            else:
                logging.error(
                    '\tFAIL: TRANS_VRR_V_MIN_%s: V_MIN Expected= %d, Actual= %d (TimeStamp = %d)' % (
                        panel.transcoder, v_min, vrr_info.VrrVmin, mmio_data.TimeStamp))
                # add into gdhm_error set for vmin failure
                gdhm_error.add("TRANS_VRR_V_MIN: register verification failed during modeset")
                status = False

    # Verify VRR V_MAX
    # Get all the write operations on given offset
    mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrVmaxReg, is_write=is_write_or_read)
    if mmio_output is None:
        logging.warning("\tNo MMIO entry found for register TRANS_VRR_V_MAX_" + panel.transcoder)
        status = False
    else:
        for mmio_data in mmio_output:
            vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrVmaxReg=mmio_data.Data))
            # Sporadically vsync disable called received due to which enter into DRRS
            if vrr_info.VrrVmax == v_min or (ctl_interrupt_found and vrr_info.VrrVmax == drrs_v_max):
                logging.info('\tPASS: TRANS_VRR_V_MAX_%s: V_MAX Expected= %d or %d, Actual= %d' % (
                    panel.transcoder, v_min, drrs_v_max, vrr_info.VrrVmax))
            else:
                logging.error('\tFAIL: TRANS_VRR_V_MAX_%s: V_MAX Expected= %d or %d, Actual= %d (TimeStamp= %d)' % (
                    panel.transcoder, v_min, drrs_v_max, vrr_info.VrrVmax, mmio_data.TimeStamp))
                # add into gdhm_error set for vmax failure
                gdhm_error.add("TRANS_VRR_V_MAX: V_MAX register verification failed during modeset")
                status = False

    # Verify VRR V_Flipline
    # Get all the write operations on given offset
    mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrFlipLine, is_write=is_write_or_read)
    if mmio_output is None:
        logging.warning("\tNo MMIO entry found for register TRANS_VRR_V_FLIPLINE_" + panel.transcoder)
        status = False
    else:
        for mmio_data in mmio_output:
            vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrFlipLine=mmio_data.Data))
            if vrr_info.VrrFlipLine == v_min or (ctl_interrupt_found and vrr_info.VrrFlipLine == drrs_v_max):
                logging.info('\tPASS: TRANS_VRR_V_FLIPLINE_%s: V_FLIPLINE Expected= %d or %d, Actual= %d' % (
                    panel.transcoder, v_min, drrs_v_max, vrr_info.VrrFlipLine))
            else:
                logging.error('\tFAIL: TRANS_VRR_V_FLIPLINE_%s: V_FLIPLINE Expected= %d or %d, '
                              'Actual= %d (TimeStamp= %d)' % (panel.transcoder, v_min, drrs_v_max, vrr_info.VrrFlipLine,
                                                              mmio_data.TimeStamp))
                # add into gdhm_error set for vflipline failure
                gdhm_error.add("TRANS_VRR_FLIP_LINE: Flipline register verification failed during modeset")
                status = False

    # check for gdhm_report set and update GDHM for failure.
    for error in gdhm_error:
        gdhm.report_driver_bug_os(title=f"[OsFeatures][VRR] {error}")
    return status


##
# @brief        Helper API to verify FLIP_LINE register based on v_min and v_max values
#               Flip Line value must be greater than or equal to v_min and less than or equal to v_max
# @param[in]    adapter, Adapter
# @param[in]    panel, Panel, panel object of the targeted display
# @param[in]    v_min VRR v_min value
# @param[in]    v_max VRR v_max value
# @param[in]    dc_balance_event_expected boolean, True DC balance event expected, False DC balance disable.
# @param[in]    vmax_flipline_for_each_flip, True if vmax for each flip verification require.
# @return       status, True if verification is successful, False otherwise
def __check_flip_line(adapter: Adapter, panel: Panel, v_min, v_max, dc_balance_event_expected,
                      vmax_flipline_for_each_flip):
    status = True

    # Verify VRR V_MIN
    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    vrr_active_period = get_vrr_active_period(adapter, panel)
    if vrr_active_period is None:
        logging.error("\t\tNo VRR active period found")
        return False
    # from Gen 16 onwards, HW DC balance use except HDMI 2.1 TMDS.
    # @todo need to remove below tmds check post PTL B0 PO
    if adapter.name in PRE_GEN_16_PLATFORMS or (adapter.name in GEN_16_PLATFORMS and
                                                panel.hdmi_2_1_caps.is_hdmi_2_1_tmds):
        for vrr_active_start, vrr_active_end in vrr_active_period:
            mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrFlipLine, is_write=True,
                                                   start_time=vrr_active_start,
                                                   end_time=vrr_active_end)
            if mmio_output is None:
                # fail test case in case of DC balance enable, Vmax and flipline need to program for each scanline/Flip
                if dc_balance_event_expected:
                    logging.error("\tFAIL: No MMIO entry found for register TRANS_VRR_V_FLIPLINE_" + panel.transcoder)
                    status = False
                else:
                    logging.warning("\tNo MMIO entry found for register TRANS_VRR_FLIPLINE_" + panel.transcoder)
            else:
                log_gdhm = False
                previous_data = None
                for mmio_data in mmio_output:
                    vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrFlipLine=mmio_data.Data))
                    if adapter.name in PRE_GEN_13_PLATFORMS:
                        # HW restriction: FlipLine should always be greater than Vmin for Pre gen13+ platform
                        if v_min < vrr_info.VrrFlipLine <= v_max:
                            if previous_data is None or previous_data != vrr_info.VrrFlipLine:
                                logging.info(
                                    '\tPASS: TRANS_VRR_FLIP_LINE_{0}: FLIP_LINE Expected= range[{1}, {2}], '
                                    'Actual= {3}'.format(
                                        panel.transcoder, v_min, v_max, vrr_info.VrrFlipLine))
                                previous_data = vrr_info.VrrFlipLine
                        else:
                            logging.error(
                                '\tFAIL: TRANS_VRR_FLIP_LINE_{0}: FLIP_LINE Expected= range[{1}, {2}], Actual= {3} '
                                'at{4}'.format(
                                    panel.transcoder, v_min, v_max, vrr_info.VrrFlipLine, mmio_data.TimeStamp))
                            log_gdhm = True
                            status = False
                    else:
                        if v_min <= vrr_info.VrrFlipLine <= v_max:
                            if previous_data is None or previous_data != vrr_info.VrrFlipLine:
                                logging.info(
                                    '\tPASS: TRANS_VRR_FLIP_LINE_{0}: FLIP_LINE Expected= range[{1}, {2}], '
                                    'Actual= {3}'.format(
                                        panel.transcoder, v_min, v_max, vrr_info.VrrFlipLine))
                                previous_data = vrr_info.VrrFlipLine
                        else:
                            logging.error(
                                '\tFAIL: TRANS_VRR_FLIP_LINE_{0}: FLIP_LINE Expected= range[{1}, {2}], '
                                'Actual= {3}'.format(panel.transcoder, v_min, v_max, vrr_info.VrrFlipLine))
                            log_gdhm = True
                            status = False
                if dc_balance_event_expected and vmax_flipline_for_each_flip:
                    # Vflipline should get program for each flip if panel is not in AlwaysInVRRMode.
                    if panel.vrr_caps.is_always_vrr_mode is False:
                        flip_data = etl_parser.get_flip_data(async_flip=True, vrr_flip=True,
                                                             start_time=vrr_active_start,
                                                             end_time=vrr_active_end,
                                                             sourceid=panel.source_id)
                        # Check for flip length if active duration is very small observed issue as denominator is small
                        if len(flip_data) < 300:
                            vflipline_for_each_flip = round(len(mmio_output)*100/len(flip_data), 2)
                            if int(vflipline_for_each_flip) < 60:
                                logging.error(f"\t\t Vflipline register not program for each flip, actual program for "
                                              f"{vflipline_for_each_flip}% of flip")
                                status = False
                            else:
                                logging.info(f"\t\t Vflipline register program for {vflipline_for_each_flip}% of flip")
                    # Vmax should ger program for each scanline interrupt during VRR active for AlwaysInVRRMode
                    else:
                        # check for each scanline interrupt.
                        interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_SCANLINEINTERRUPT,
                                                                       start_timestamp=vrr_active_start,
                                                                       end_timestamp=vrr_active_end)

                        # Driver should program Vmax register for each scanline interrupt during vrr active
                        vflipline_for_each_scanline = round(len(mmio_output) * 100 / len(interrupt_data), 2)
                        if int(vflipline_for_each_scanline) < 100:
                            logging.error(f"\t\t Vmax register not program for each scanline interrupt, actual program"
                                          f"for {vflipline_for_each_scanline}% of scanline interrupt")
                        else:
                            logging.info(f"\t\t Vmax register program for {vflipline_for_each_scanline}% of interrupt")
                if log_gdhm:
                    gdhm.report_driver_bug_os(
                        f"[OsFeatures][VRR] TRANS_VRR_FLIP_LINE: Flipline register verification failed")
    # HW DCB register need to program in case of Gen16 (Xe3) onwards.
    else:
        for vrr_active_start, vrr_active_end in vrr_active_period:
            mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrDcbFlipLine, is_write=True,
                                                   start_time=vrr_active_start,
                                                   end_time=vrr_active_end)
            if mmio_output is None:
                # fail test case in case of DC balance enable, Vmax and flipline need to program for each scanline/Flip
                if dc_balance_event_expected:
                    logging.error("\tFAIL: No MMIO entry found for register TRANS_VRR_V_FLIPLINE_DCB_" + panel.transcoder)
                    status = False
                else:
                    logging.warning("\tNo MMIO entry found for register TRANS_VRR_FLIPLINE_DCB" + panel.transcoder)
            else:
                log_gdhm = False
                previous_data = None
                for mmio_data in mmio_output:
                    vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                         VrrOffsetValues(VrrDcbFlipLine=mmio_data.Data))

                    if v_min <= vrr_info.VrrDcbFlipLine <= v_max:
                        if previous_data is None or previous_data != vrr_info.VrrDcbFlipLine:
                            logging.info(
                                '\tPASS: TRANS_VRR_FLIP_LINE_DCB_{0}: FLIP_LINE Expected= range[{1}, {2}], '
                                'Actual= {3}'.format(
                                    panel.transcoder, v_min, v_max, vrr_info.VrrDcbFlipLine))
                            previous_data = vrr_info.VrrDcbFlipLine
                    else:
                        logging.error(
                            '\tFAIL: TRANS_VRR_FLIP_LINE_DCB_{0}: FLIP_LINE Expected= range[{1}, {2}], '
                            'Actual= {3}'.format(panel.transcoder, v_min, v_max, vrr_info.VrrDcbFlipLine))
                        log_gdhm = True
                        status = False
                # failing - need to unblock once issue fixed.
                '''if dc_balance_event_expected:
                    # Vflipline should get program for each flip if panel is not in AlwaysInVRRMode.
                    if panel.vrr_caps.is_always_vrr_mode is False:
                        flip_data = etl_parser.get_flip_data(async_flip=True, vrr_flip=True,
                                                             start_time=vrr_active_start,
                                                             end_time=vrr_active_end,
                                                             sourceid=panel.source_id)
                        vflipline_for_each_flip = round(len(mmio_output) * 100 / len(flip_data), 2)
                        if int(vflipline_for_each_flip) <= 90:
                            logging.error(f"\t\t Vflipline register not program for each flip, actual program for "
                                          f"{vflipline_for_each_flip}% of flip")
                            status = False
                        else:
                            logging.info(f"\t\t Vflipline register program for {vflipline_for_each_flip}% of flip")
                    # Vmax should ger program for each scanline interrupt during VRR active for AlwaysInVRRMode
                    else:
                        # check for each scanline interrupt.
                        interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_SCANLINEINTERRUPT,
                                                                       start_timestamp=vrr_active_start,
                                                                       end_timestamp=vrr_active_end)

                        # Driver should program Vmax register for each scanline interrupt during vrr active
                        vflipline_for_each_scanline = round(len(mmio_output) * 100 / len(interrupt_data), 2)
                        if int(vflipline_for_each_scanline) <= 100:
                            logging.error(f"\t\t Vmax register not program for each scanline interrupt, actual program"
                                          f"for {vflipline_for_each_scanline}% of scanline interrupt")
                        else:
                            logging.info(f"\t\t Vmax register program for {vflipline_for_each_scanline}% of interrupt")'''
                if log_gdhm:
                    gdhm.report_driver_bug_os(
                        f"[OsFeatures][VRR] TRANS_VRR_FLIP_LINE: Flipline register verification failed")

    return status


##
# @brief        Helper API to verify FLIP_LINE register based on v_min and v_max values
#               Flip Line value must be greater than or equal to v_min and less than or equal to v_max
# @param[in]    adapter, Adapter
# @param[in]    panel, Panel, panel object of the targeted display
# @param[in]    v_min VRR v_min value
# @param[in]    v_max VRR v_min value
# @return       status, True if verification is successful, False otherwise
def __check_flip_line_modeset(adapter: Adapter, panel: Panel, v_min, v_max):
    status = True

    # Verify VRR V_MIN
    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)

    mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrFlipLine, is_write=True)
    if mmio_output is None:
        logging.warning("\tNo MMIO entry found for register TRANS_VRR_FLIPLINE_" + panel.transcoder)
    else:
        log_gdhm = False
        previous_data = None
        for mmio_data in mmio_output:
            vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrFlipLine=mmio_data.Data))
            if adapter.name in PRE_GEN_13_PLATFORMS:
                # HW restriction: FlipLine should always be greater than Vmin for Pre gen13+ platform
                if v_min < vrr_info.VrrFlipLine <= v_max:
                    if previous_data is None or previous_data != vrr_info.VrrFlipLine:
                        logging.info(
                            '\tPASS: TRANS_VRR_FLIP_LINE_{0}: FLIP_LINE Expected= range[{1}, {2}], Actual= {3}'.format(
                                panel.transcoder, v_min, v_max, vrr_info.VrrFlipLine))
                        previous_data = vrr_info.VrrFlipLine
                else:
                    logging.error(
                        '\tFAIL: TRANS_VRR_FLIP_LINE_{0}: FLIP_LINE Expected= range[{1}, {2}], Actual= {3} '
                        'at{4}'.format(
                            panel.transcoder, v_min, v_max, vrr_info.VrrFlipLine, mmio_data.TimeStamp))
                    log_gdhm = True
                    status = False
            else:
                if v_min <= vrr_info.VrrFlipLine <= v_max:
                    if previous_data is None or previous_data != vrr_info.VrrFlipLine:
                        logging.info(
                            '\tPASS: TRANS_VRR_FLIP_LINE_{0}: FLIP_LINE Expected= range[{1}, {2}], Actual= {3}'.format(
                                panel.transcoder, v_min, v_max, vrr_info.VrrFlipLine))
                        previous_data = vrr_info.VrrFlipLine
                else:
                    logging.error(
                        '\tFAIL: TRANS_VRR_FLIP_LINE_{0}: FLIP_LINE Expected= range[{1}, {2}], Actual= {3}'.format(
                            panel.transcoder, v_min, v_max, vrr_info.VrrFlipLine))
                    log_gdhm = True
                    status = False
        if log_gdhm:
            gdhm.report_driver_bug_os(f"[OsFeatures][VRR] TRANS_VRR_FLIP_LINE: Flipline register verification failed")
    return status


##
# @brief        Helper API to verify VRR Enable/Disable trace events
# @description  ETL capturing is started before opening the App, hence it should contain VRR Enable trace events
#               Similarly ETL capturing is stopped after closing the App, hence it should contain VRR disable trace
#               trace events also. Apart from these two scenarios, ETL should contain any intermediate VRR enable/
#               disable switch.
# @param[in]    panel Panel, panel object of the targeted display
# @param[in]    enabled, Boolean, True if VRR is expected to be enabled, False otherwise
# @param[in]    v_min Number, expected Vmin value
# @param[in]    v_max Number, expected Vmax value
# @param[in]    drrs_v_max Number, expected DRRS Vmax value
# @param[in]    BFR_v_max Number, expected BFR_Vmax value
# @param[in]    check_status Boolean, True if need to check Status info event else false.
# @return       status Boolean, True if verification is successful, False otherwise
def __check_vrr_enable_disable(adaper: Adapter, panel: Panel, enabled, v_min=None, v_max=None, drrs_v_max=None,
                               bfr_v_max=None):
    status = True
    vrr_enable_count = 0
    vrr_disable_count = 0
    pipe = 'PIPE_' + panel.pipe
    port = 'PORT_' + panel.pipe

    logging.info("\tVerifying VRR Enable/Disable events")
    vrr_enable_disable_event_output = etl_parser.get_event_data(etl_parser.Events.RR_SWITCH_INFO)
    # Filter out enable event data for targeted display
    enable_event_data = [_ for _ in vrr_enable_disable_event_output if _.TargetId == panel.target_id and _.RrMode ==
                         "DD_REFRESH_RATE_MODE_VARIABLE" and _.IsCurrent]
    if not enabled:
        if vrr_enable_disable_event_output is None:
            logging.info("\t\tNo VRR enable trace event found")
        else:
            if len(enable_event_data) == 0:
                logging.info(f"\t\tNo VRR enable trace event found for {pipe} (Expected)")
            else:
                logging.error(f"\t\tVRR Enable trace event found for {pipe} (Unexpected)")
                gdhm.report_driver_bug_os(f"\t\tVRR Enable trace event found for {pipe} (Unexpected)")
                status = False
    else:
        if vrr_enable_disable_event_output is None:
            logging.error("\t\tNo VRR Enable trace event found")
            gdhm.report_driver_bug_os("\t\tNo VRR Enable trace event found")
            status = False
        else:
            gdhm_error = set()
            if len(enable_event_data) == 0:
                logging.error(f"\t\tNo VRR Enable trace event found for {pipe}")
                gdhm.report_driver_bug_os(f"No VRR Enable trace event found")
                status = False
            else:
                if v_min is not None and v_max is not None and adaper.name in PRE_GEN_13_PLATFORMS:
                    v_min += 1
                rr_program_output = etl_parser.get_event_data(etl_parser.Events.RR_SWITCH_PROGRAM)
                rr_prog_data = [_ for _ in rr_program_output if _.Port == port and _.VrrEnable and not
                (_.VrrVmax == _.VrrFlipLine)]
                for event_data in rr_prog_data:
                    logging.info("\t\tVRR Enabled(Time= {0}): {1}".format(event_data.TimeStamp, event_data))

                    if v_min is not None and v_max is not None:
                        # compare vmin with calculated Vmin or drrs_vmax - 2 in case of drrs panel or
                        # bfr_vmax -2 in case of bfr supported panel with bfr mode enable
                        if not ((event_data.VrrVmin - 1) == v_min or  # Vmin for Vrr
                                (panel.drrs_caps.is_drrs_supported and
                                 ((event_data.VrrVmin - 1) == drrs_v_max))  # Vmin with DRRS supported panel
                                or (panel.bfr_caps.is_bfr_supported and bfr.is_dynamic_rr(panel) and
                                    (event_data.VrrVmin - 1) == bfr_v_max)):
                            logging.error(
                                f"\tFAIL: TRANS_VRR_V_MIN_{panel.transcoder}: V_MIN Expected= {v_min} or "
                                f"{drrs_v_max}(Drrs_Vmax) or {bfr_v_max}(BFR_Vmax),"
                                f"Actual= {event_data.VrrVmin - 1}")
                            # add into gdhm_error set for vmin failure
                            gdhm_error.add("TRANS_VRR_V_MIN: register verification failed")
                            status = False
                        else:
                            logging.info(
                                f"\tPASS: TRANS_VRR_V_MIN_{panel.transcoder}: V_MIN Expected= {v_min} or "
                                f"{drrs_v_max}(Drrs_Vmax) or {bfr_v_max}(BFR_Vmax),"
                                f"Actual= {event_data.VrrVmin - 1}")
                            # compare vmax with calculated Vmax or drrs_vmax in case of drrs panel or
                            # bfr_vmax in case of bfr supported panel with bfr mode enable
                        if not ((v_max <= (event_data.VrrVmax - 1) <= v_max + 1) or
                                (panel.drrs_caps.is_drrs_supported and
                                 drrs_v_max <= (event_data.VrrVmax - 1) <= drrs_v_max + 1)
                                or (panel.bfr_caps.is_bfr_supported and bfr.is_dynamic_rr(panel) and
                                    bfr_v_max <= (event_data.VrrVmax - 1) <= bfr_v_max + 1)):
                            logging.error(
                                f"\tFAIL: TRANS_VRR_V_MAX_{panel.transcoder}: V_MAX Expected= {v_max + 1}"
                                f"or {drrs_v_max}(Drrs_Vmax), or {bfr_v_max}(BFR_Vmax), "
                                f"Actual= {event_data.VrrVmax - 1}")
                            # add into gdhm_error set for vmax failure
                            gdhm_error.add("TRANS_VRR_V_MAX: V_MAX register verification failed")
                            status = False
                        else:
                            logging.info(
                                f"\tPASS: TRANS_VRR_V_MAX_{panel.transcoder}: V_MAX Expected= {v_max + 1} "
                                f"or {drrs_v_max}(Drrs_Vmax), or {bfr_v_max}(BFR_Vmax), "
                                f"Actual= {event_data.VrrVmax - 1}")
                            # compare vmax with calculated Vmax or drrs_vmax in case of drrs panel or
                            # bfr_vmax in case of bfr supported panel with bfr mode enable
                        if not ((event_data.VrrFlipLine == event_data.VrrVmin) or
                                (
                                        panel.drrs_caps.is_drrs_supported and event_data.VrrFlipLine == drrs_v_max +
                                        1) or
                                (panel.bfr_caps.is_bfr_supported and bfr.is_dynamic_rr(panel) and
                                 event_data.VrrFlipLine == bfr_v_max + 1)):
                            logging.error(f"\tFAIL: TRANS_VRR_FLIP_LINE_{panel.transcoder}: Flipline Expected= "
                                          f"%{v_min}(Vmin) or {drrs_v_max}(Drrs_Vmax),or {bfr_v_max}(BFR_Vmax), "
                                          f"Actual= {event_data.VrrFlipLine - 1}")
                            # add into gdhm_error set for vflipline failure
                            gdhm_error.add("TRANS_VRR_FLIP_LINE: Flipline register verification failed")
                            status = False
                        else:
                            logging.info(f"\tPASS: TRANS_VRR_FLIP_LINE_{panel.transcoder}: Flipline Expected= "
                                         f"{v_min}(Vmin) or {drrs_v_max}(Drrs_Vmax),or {bfr_v_max}(BFR_Vmax), "
                                         f"Actual= {event_data.VrrFlipLine - 1}")
                vrr_enable_count += 1
            # check for gdhm_report set and update GDHM for failure.
            for error in gdhm_error:
                gdhm.report_driver_bug_os(f"[OsFeatures][VRR] {error}")

    # Filter out event data for targeted display
    disable_event_data = [_ for _ in vrr_enable_disable_event_output if _.TargetId == panel.target_id and
                          (_.RrMode != "DD_REFRESH_RATE_MODE_VARIABLE")]
    if enabled:
        if disable_event_data is None:
            logging.error("\t\tNo VRR Disable trace event found")
            status = False
        else:
            if len(disable_event_data) == 0:
                logging.error("\t\tNo VRR Disable trace event found for {0}".format(pipe))
                gdhm.report_driver_bug_os(f"[OsFeatures][VRR] No VRR Disable trace event found (Unexpected)")
                status = False
            else:
                for event_data in disable_event_data:
                    logging.info("\t\tVRR Disabled(Time= {0}): {1}".format(event_data.TimeStamp, event_data))
                    vrr_disable_count += 1

    if enabled:
        logging.info("\t\tVRR enable/disable count: Enabled= {0} times, Disabled= {1} times".format(
            vrr_enable_count, vrr_disable_count))
    return status


##
# @brief        Helper API to verify VBI
# @param[in]    adapter, Adapter
# @param[in]    panel - Panel, panel object of the targeted display
# @param[in]    is_power_event indicates if a power event occurred
# @param[in]    rr_min number, min rr value
# @param[in]    is_negative_test, Boolean indicates if it is a negative test
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_vbi(adapter: Adapter, panel: Panel, power_event, rr_min, is_negative_test):
    status = True
    pipe = 'PIPE_' + panel.pipe
    min_vrr_active_period = 5 * math.floor(1000.0 / rr_min)

    # Get VRR enable events to select last mode set entry before VRR got enabled
    logging.info("\tVerifying VBI")
    vrr_active_period = get_vrr_active_period(adapter, panel)
    if vrr_active_period is None:
        logging.error("\t\tNo VRR active period found")
        return False

    for vrr_active_start, vrr_active_end in vrr_active_period:
        # Skip if VRR active period is too short
        if (vrr_active_end - vrr_active_start) <= min_vrr_active_period:
            continue
        vbi_output = etl_parser.get_vbi_data(pipe, start_time=vrr_active_start, end_time=vrr_active_end)
        if vbi_output is None:
            logging.error("\t\tNo VBI data found for VRR active period({0}, {1})".format(
                vrr_active_start, vrr_active_end))
            status = False
            return status

        # Check interval between two VBIs is changing during VRR active period
        previous_vbi_data = None
        previous_vbi_delta = None
        is_vbi_changing = False
        for vbi_data in vbi_output:
            if previous_vbi_data is None:
                previous_vbi_data = vbi_data
                continue
            if previous_vbi_delta is None:
                previous_vbi_delta = vbi_data.TimeStamp - previous_vbi_data.TimeStamp
                continue
            current_vbi_delta = vbi_data.TimeStamp - previous_vbi_data.TimeStamp
            if (previous_vbi_delta + VBI_DELTA_TIME_TOLERANCE) <= current_vbi_delta <= \
                    (previous_vbi_delta + VBI_DELTA_TIME_TOLERANCE):
                # No change
                pass
            else:
                # VBI interval is changing
                is_vbi_changing = True
            previous_vbi_data = vbi_data

        if is_vbi_changing:
            logging.info("\t\tPASS: VBI interval change detected during VRR active period ({0}, {1})".format(
                vrr_active_start, vrr_active_end))
        elif power_event is None:
            logging.error("\t\tFAIL: No VBI interval change detected during VRR active period ({0}, {1})".format(
                vrr_active_start, vrr_active_end))
            status = False
        status &= is_vbi_changing

    if status is False and is_negative_test is False:
        gdhm.report_driver_bug_os("[OsFeatures][VRR] VBI interval is not changing during VRR game playback")

    return status


##
# @brief        Helper API to verify VRR_CTL programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @param[in]    is_negative_test, Boolean indicates if it is a negative test
# @return       status Boolean, True if verification is successful, False otherwise
def __check_vrr_ctl_programming(adapter: Adapter, panel: Panel, is_negative_test):
    status = True
    logging.info("\tVerifying TRANS_VRR_CTL_REGISTER programming")

    # read MMIO value from etl
    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    vrr_ctl_output = etl_parser.get_mmio_data(vrr_regs.VrrControl)
    is_fixed_rr_supported = panel.vrr_caps.is_always_vrr_mode  # fixed support will be true for AlwaysInVRR support
    # panel
    # Fixed RR not support if panel is not LRR supported from DPCD.
    if panel.is_lfp and adapter not in common.PRE_GEN_15_PLATFORMS and panel.psr_caps.is_psr2_supported:
        is_fixed_rr_supported &= panel.lrr_caps.is_lrr_2_5_supported

    # VRR_CTL register program may not happen in case of non vrr panel.
    if vrr_ctl_output is None:
        # VRR_CTL register program may not happen in case of non vrr panel or VRR panel with negative scenario
        if not panel.vrr_caps.is_vrr_supported or (panel.vrr_caps.is_vrr_supported and is_negative_test):
            logging.info("\t\tNo MMIO operation found for TRANS_VRR_CTL_REGISTER for Non-VRR panel")
            return True
        logging.error("\t\tNo MMIO operation found for TRANS_VRR_CTL_REGISTER for VRR panel")
        gdhm.report_driver_bug_os("[OsFeatures][VRR] No MMIO operation found for TRANS_VRR_CTL_REGISTER for VRR panel")
        return False
    # VRR_CTL register enable bit check in case of non vrr panel.
    if not panel.vrr_caps.is_vrr_supported:
        for mmio_data in vrr_ctl_output:
            vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrControl=mmio_data.Data))
            # for always in VRR mode for non VRR panel, VRR enable bit should be set
            if panel.vrr_caps.is_always_vrr_mode_on_non_vrr_panel:
                # failing in case VRR Enable bit not set
                if vrr_info.VrrEnable is False:
                    logging.error(
                        f"\t\tTRANS_VRR_CTL_REGISTER(bit:31) got disable during (TimeStamp= {mmio_data.TimeStamp}"
                        f"expected: enable, actual: disable")
                    gdhm.report_driver_bug_os(f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:31) was disable on "
                                              f"Non-VRR panel")
                    status = False
                if vrr_info.FlipLineEnable is False:
                    logging.error(
                        f"\t\tTRANS_VRR_CTL_REGISTER(bit:29) got disable during (TimeStamp={mmio_data.TimeStamp}"
                        f"expected: enable, actual: disable")
                    gdhm.report_driver_bug_os(f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:29) was disable on "
                                              f"Non-VRR panel")
                    status = False
            # for not in always VRR mode for non VRR panel, VRR enable bit should be disabled
            else:
                # failing in case VRR Enable bit set for non-vrr panel
                if vrr_info.VrrEnable is True:
                    logging.error(
                        f"\t\tTRANS_VRR_CTL_REGISTER(bit:31) got enable during (TimeStamp= {mmio_data.TimeStamp}"
                        f"expected: disable, actual: enable")
                    gdhm.report_driver_bug_os(f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:31) was enabled on "
                                              f"Non-VRR panel")
                    status = False
                if vrr_info.FlipLineEnable is True:
                    logging.error(
                        f"\t\tTRANS_VRR_CTL_REGISTER(bit:29) got enable during (TimeStamp={mmio_data.TimeStamp}"
                        f"expected: disable, actual: enable")
                    gdhm.report_driver_bug_os(f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:29) was enabled on Non-VRR"
                                              f" panel ")
                    status = False
        if not status:
            logging.error(f"\t\tFAIL: TRANS_VRR_CTL_REGISTER(bit:31 & 29) verification failed for {panel.port}")
            return False
        logging.info(f"\t\tPASS: TRANS_VRR_CTL_REGISTER(bit:31 & 29) verification passed for {panel.port}")
        return True
    # checking in case of VRR_CTL register program happen for VRR panel
    else:
        # Always in VRR mode enable - VRR_CTL enable bit should always enable with below condition
        # VRR supported panel and gen13+ platform for EFP and Gen14+ for LFP( Always VRR enable check)
        if panel.vrr_caps.is_always_vrr_mode:
            set_timing_event_output = etl_parser.get_event_data(etl_parser.Events.SET_TIMING, event_filter='DISABLE')
            if set_timing_event_output is not None:
                set_timing_event_output = [_ for _ in set_timing_event_output if _.Port == panel.port]

            for mmio_data in vrr_ctl_output:
                vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrControl=mmio_data.Data))
                # VRR can disable for panel during any set-timing or power event during game playback
                if vrr_info.VrrEnable is False and set_timing_event_output is None:
                    logging.error(
                        f"\t\tTRANS_VRR_CTL_REGISTER(bit:31) got disable during (TimeStamp= {mmio_data.TimeStamp}"
                        f"expected: enable, actual: disable")
                    gdhm.report_driver_bug_os(
                        f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:31) was disabled")
                    status &= False
                if vrr_info.FlipLineEnable is False and set_timing_event_output is None:
                    logging.error(
                        f"\t\tTRANS_VRR_CTL_REGISTER(bit:29) got disable during (TimeStamp={mmio_data.TimeStamp}"
                        f"expected: enable, actual: disable")
                    gdhm.report_driver_bug_os(
                        f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:29) was disabled")
                    status &= False
            if not status:
                logging.error(f"\t\tFAIL: TRANS_VRR_CTL_REGISTER(bit:31 & 29) was disabled for {panel.port}")
                return False
            logging.info(f"\t\tPASS: TRANS_VRR_CTL_REGISTER(bit:31 & 29) was enabled for {panel.port}")
            return True
        # not always in VRR on VRR panel - LFP for PRE_gen14 platform and EFP for pre_gen13 platform.
        else:
            # VRR_CTL enable bit check for negative scenario
            # negative + not always in VRR + Fixed RR not support - disable CTL bit
            # negative + not always in VRR + fixed RR support - enable CTL bit
            if is_negative_test and not panel.vrr_caps.is_always_vrr_mode:
                for mmio_data in vrr_ctl_output:
                    vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                         VrrOffsetValues(VrrControl=mmio_data.Data))
                    if vrr_info.VrrEnable is True:
                        # VRR enable to support fixed RR.
                        if not is_fixed_rr_supported:
                            logging.error(
                                f"\t\tTRANS_VRR_CTL_REGISTER(bit:31) got enable during (TimeStamp= "
                                f"{mmio_data.TimeStamp}"
                                f"expected: disable, actual: enable")
                            gdhm.report_driver_bug_os(
                                f"[OsFeatures][VRR][Negative] TRANS_VRR_CTL_REGISTER(bit:31) was enabled")
                            status &= False
                    if vrr_info.FlipLineEnable is True:
                        # VRR enable to support fixed RR.
                        if not is_fixed_rr_supported:
                            logging.error(
                                f"\t\tTRANS_VRR_CTL_REGISTER(bit:29) got enable during (TimeStamp={mmio_data.TimeStamp}"
                                f"expected: disable, actual: enable")
                            gdhm.report_driver_bug_os(
                                f"[OsFeatures][VRR][Negative] TRANS_VRR_CTL_REGISTER(bit:29) was enabled")
                            status &= False
                if not status:
                    logging.error(f"\t\tFAIL: TRANS_VRR_CTL_REGISTER(bit:31 & 29) was enabled for {panel.port}")
                    return False
                logging.info(f"\t\tPASS: TRANS_VRR_CTL_REGISTER(bit:31 & 29) was disabled for {panel.port}")
                return True

            # VRR_CTL enable bit should enable during VRR active periods ( not always in VRR and positive scenario)
            else:
                vrr_active_period = get_vrr_active_period(adapter, panel)
                if vrr_active_period is None:
                    logging.error("\t\tNo VRR active period found")
                    gdhm.report_driver_bug_os(f"[OsFeatures][VRR] No VRR active period found")
                    return False

                for vrr_active_start, vrr_active_end in vrr_active_period:
                    vrr_ctl_output = etl_parser.get_mmio_data(
                        vrr_regs.VrrControl, start_time=vrr_active_start, end_time=vrr_active_end)
                    if vrr_ctl_output is None:
                        logging.error(
                            "\t\tNo MMIO operation found for TRANS_VRR_CTL_REGISTER for VRR active period "
                            "({0}, {1})".format(vrr_active_start, vrr_active_end))
                        gdhm.report_driver_bug_os(
                            f"[OsFeatures][VRR] No MMIO operation found for TRANS_VRR_CTL_REGISTER for VRR active "
                            f"period")
                        return False
                    for mmio_data in vrr_ctl_output:
                        vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                             VrrOffsetValues(VrrControl=mmio_data.Data))

                        if vrr_info.VrrEnable is False:
                            if (vrr_active_start + 50) > mmio_data.TimeStamp < (vrr_active_end - 50):
                                logging.error(
                                    "\t\tTRANS_VRR_CTL_REGISTER(bit:31) got disabled during (TimeStamp= {0}) VRR "
                                    "active "
                                    "period ({1}, {2})".format(mmio_data.TimeStamp, vrr_active_start, vrr_active_end))
                                gdhm.report_driver_bug_os(
                                    f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:31) was disabled")
                                status &= False

                        if vrr_info.FlipLineEnable is False:
                            if (vrr_active_start + 50) > mmio_data.TimeStamp < (vrr_active_end - 50):
                                logging.error(
                                    "\t\tTRANS_VRR_CTL_REGISTER(bit:29) got disabled during (TimeStamp={0}) VRR active "
                                    "period ({1}, {2})".format(mmio_data.TimeStamp, vrr_active_start, vrr_active_end))
                                gdhm.report_driver_bug_os(
                                    f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:29) was disabled")
                                status &= False

                    if not status:
                        logging.error(f"\t\tFAIL: TRANS_VRR_CTL_REGISTER(bit:31 & 29) was disabled for {panel.port}")
                        return False
                    logging.info(
                        "\t\tPASS: TRANS_VRR_CTL_REGISTER(bit:31) was enabled during VRR active period({0}, {1})"
                        "".format(vrr_active_start, vrr_active_end))
    return status


##
# @brief        Helper API to verify VRR_CTL programming during modeset
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @param[in]    is_negative_test, Boolean indicates if it is a negative test
# @return       status Boolean, True if verification is successful, False otherwise
def __check_vrr_ctl_programming_modeset(adapter: Adapter, panel: Panel, is_negative_test):
    status = True
    logging.info("\tVerifying TRANS_VRR_CTL_REGISTER programming during mode-set")
    if not panel.vrr_caps.is_always_vrr_mode:
        logging.info("not in Always VRR mode returning early")
        return status
    # Get the first mode set happened after opening the app if any
    set_timing_data = etl_parser.get_event_data(etl_parser.Events.SET_TIMING)

    # if there is only virtual modeset, then need to check VRR CTL already enable or not
    if set_timing_data is None:
        # read MMIO value from etl
        vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
        vrr_ctl_output = etl_parser.get_mmio_data(vrr_regs.VrrControl, is_write=False)
    # in case of physical modeset - Driver should write and enable VRR CTL
    else:
        # read MMIO value from etl
        vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
        vrr_ctl_output = etl_parser.get_mmio_data(vrr_regs.VrrControl, is_write=True)

    # Check for VRR CTL mmio register.
    if vrr_ctl_output is None:
        logging.error(f"\t\tNo MMIO operation found for TRANS_VRR_CTL_REGISTER for {panel.port}")
        gdhm.report_driver_bug_os("[OsFeatures][VRR] No MMIO operation found for TRANS_VRR_CTL_REGISTER for VRR panel "
                                  "during mode-set")
        return False
    # VRR_CTL register enable bit should be set in last read or write base on mode set.
    mmio_data = vrr_ctl_output[-1]
    vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrControl=mmio_data.Data))
    # if panel is vrr supported or always in VRR mode for non VRR panel than it should set VRR Enable bit
    if panel.vrr_caps.is_vrr_supported or (not panel.vrr_caps.is_vrr_supported and
                                           panel.vrr_caps.is_always_vrr_mode_on_non_vrr_panel):
        # failing in case VRR Enable bit not set
        if vrr_info.VrrEnable is False:
            logging.error(
                f"\t\tTRANS_VRR_CTL_REGISTER(bit:31) got disable during (TimeStamp= {mmio_data.TimeStamp}"
                f"expected: enable, actual: disable")
            gdhm.report_driver_bug_os(f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:31) was disable on Non-VRR panel")
            status &= False
        if vrr_info.FlipLineEnable is False:
            logging.error(
                f"\t\tTRANS_VRR_CTL_REGISTER(bit:29) got disable during (TimeStamp={mmio_data.TimeStamp}"
                f"expected: enable, actual: disable")
            gdhm.report_driver_bug_os(f"[OsFeatures][VRR] TRANS_VRR_CTL_REGISTER(bit:29) was disable on Non-VRR panel")
            status &= False
    if not status:
        logging.error(f"\t\tFAIL: TRANS_VRR_CTL_REGISTER(bit:31 & 29) verification failed for {panel.port}")
        return False
    logging.info(f"\t\tPASS: TRANS_VRR_CTL_REGISTER(bit:31 & 29) verification passed for {panel.port}")
    return status


##
# @brief        Check OS FlipQ status in OsFtrTable
# @param[in]    etl_file : Data from FeatureControl event
# @return       status   : True if OS FlipQ is enabled in OSFtrTable else False
def os_flipq_status_in_os_ftr_table():
    # Generate ETL report
    feature_control_info = etl_parser.get_event_data(etl_parser.Events.FEATURE_CONTROL)
    if feature_control_info is None:
        logging.error("No Data found for FeatureControl")
        assert False, "No Data found for FeatureControl"
    if feature_control_info[0].OsFtrTable[0] & 0x1 == 0x1:
        logging.info("OS FlipQ is enabled in OsFtrTable")
        return True
    logging.info("OS FlipQ is disabled in OsFtrTable")
    return False


##
# @brief        Helper API to verify VRR GuardBand programming
# @param[in]    adapter Adapter
# @param[in]    panel, Panel, panel object of the targeted display
# @param[in]    v_min VRR v_min value
# @param[in]    v_active VActive
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_vrr_guard_band_programming(adapter: Adapter, panel: Panel, v_min, v_active):
    status = True
    guardband = 0
    window2 = 0
    if not panel.vrr_caps.is_always_vrr_mode:
        logging.info("Always in VRR mode not enable returning early")
        return status
    ##
    # Feature is valid from Gen13 onwards (DG2 A0 has an issue, so skipping the check)
    if adapter.name in PRE_GEN_13_PLATFORMS or \
            (adapter.name in ['DG2'] and adapter.cpu_stepping == 0):
        return status

    set_timing_data = etl_parser.get_event_data(etl_parser.Events.SET_TIMING)

    # if there is only virtual modeset, then No write into CTL and scanline upper register.
    if set_timing_data is None:
        return status
    logging.info("\tVerifying VRR GuardBand programming")
    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    # Get all the write operations on given offset
    mmio_output = etl_parser.get_mmio_data(vrr_regs.VrrControl, is_write=True)
    timings_info = adapter.regs.get_timing_info(panel.transcoder_type)
    current_mode = __display_config.get_current_mode(panel.display_info.DisplayAndAdapterInfo)
    if mmio_output is None:
        logging.error("\tNo MMIO entry found for register TRANS_VRR_CTL_" + panel.transcoder)
        status = False
    else:
        for mmio_data in mmio_output:
            vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrControl=mmio_data.Data))
            # skipping Guardband check when VRR Enable bit is not set.
            if vrr_info.VrrEnable is False:
                logging.info("\t\tSkipping Guardband check as VRR enable bit is not set")
                continue
            guardband = v_min - timings_info.VBlankStart
            if vrr_info.VrrGuardband != (v_min - timings_info.VBlankStart):
                logging.error(
                    "\t\tTRANS_VRR_CTL_REG programming for VRR GuardBand expected= {0}, actual= {1} during "
                    "(TimeStamp= {2})".format((v_min - timings_info.VBlankStart),
                                              vrr_info.VrrGuardband, mmio_data.TimeStamp))
                status = False
            else:
                logging.info("\t\tTRANS_VRR_CTL_REG programming for VRR GuardBand expected= {0}, actual= {1} during "
                             "(TimeStamp= {2})".format((v_min - timings_info.VBlankStart),
                                                       vrr_info.VrrGuardband, mmio_data.TimeStamp))
    logging.info("\tVerifying ScanLine upper programming")
    display_fc2 = registry.DisplayFeatureControl2(adapter.gfx_index)
    if (adapter.name not in PRE_GEN_14_PLATFORMS and (os_flipq_status_in_os_ftr_table() is True or
                                                     display_fc2.EnableOsUnawareFlipQ) and not
    panel.pipe_joiner_tiled_caps.is_pipe_joiner_require):
        # Get the first mode set happened after opening the app if any
        set_timing_data = etl_parser.get_event_data(etl_parser.Events.SET_TIMING)
        if set_timing_data is None:
            status &= True
        else:
            # Get all the write operations on given offset
            mmio_output = etl_parser.get_mmio_data(vrr_regs.PipeDmcScanlineUpper, is_write=True,
                                                   start_time=set_timing_data[0].TimeStamp - 10)

            if mmio_output is None:
                logging.error("\tNo MMIO entry found for register PIPE_DMC_SCANLINE_CMP_UPPER_" + panel.transcoder)
                status = False
            else:
                vrr_info_2 = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                       VrrOffsetValues(PipeDmcScanlineUpper=mmio_output[0].Data))
                window2 = MMIORegister.read('TRANS_SET_CONTEXT_LATENCY_REGISTER',
                                            'TRANS_SET_CONTEXT_LATENCY_' + panel.transcoder,
                                            adapter.name, gfx_index=adapter.gfx_index).context_latency
                scanline_upper = v_min - guardband - window2
                if adapter.name not in PRE_GEN_15_PLATFORMS:
                    current_cd_clock = DisplayClock().get_current_cd_clock(adapter.gfx_index)

                    if adapter.name in GEN_15_PLATFORMS:
                        dmctimeoutbasedoncdclockapplied = lnl_cdclock_ctl_freq_dict[current_cd_clock]
                    if adapter.name in GEN_16_PLATFORMS:
                        dmctimeoutbasedoncdclockapplied = ptl_cdclock_ctl_freq_dict[current_cd_clock]

                    logging.debug(f"dmctimeoutbasedoncdclockapplied: {dmctimeoutbasedoncdclockapplied}")
                    data = DriverInterface().mmio_read(LATENCY_SAGV, adapter.gfx_index)
                    sagvblocktime = data & 0x00001FFF
                    logging.debug(f"sagvblocktime {sagvblocktime}")
                    time_req_in_us_to_execute_flipq = dmctimeoutbasedoncdclockapplied + 100 + sagvblocktime
                    logging.debug(f"time_req_in_us_to_execute_flipq {time_req_in_us_to_execute_flipq}")
                    line_time_offset = 'WM_LINETIME_' + panel.pipe
                    linetime_instance = MMIORegister.get_instance('WM_LINETIME_REGISTER', line_time_offset,
                                                                  adapter.name)
                    linetime_offset = linetime_instance.offset
                    linetime = math.floor(DriverInterface().mmio_read(linetime_offset, adapter.gfx_index) / 8)
                    logging.debug(f"linetime{linetime}")
                    lines_required_for_dmc = time_req_in_us_to_execute_flipq / linetime
                    logging.debug(f"lines_required_for_dmc {lines_required_for_dmc}")
                    scanline_upper -= lines_required_for_dmc
                    scanline_upper = int(scanline_upper + 2)
                if vrr_info_2.PipeDmcScanlineUpper != scanline_upper:
                    logging.error(
                        "\t\tREG_PIPE_DMC_SCANLINE_CMP_UPPER programming for scanline upper expected= {0}, "
                        "actual= {1} during (TimeStamp= {2})".format(scanline_upper,
                                                                     vrr_info_2.PipeDmcScanlineUpper,
                                                                     mmio_output[0].TimeStamp))
                    status = False
                else:
                    logging.info(
                        "\t\tREG_PIPE_DMC_SCANLINE_CMP_UPPER programming for scanline upper expected= {0}, "
                        "actual= {1} during (TimeStamp= {2})".format(scanline_upper,
                                                                     vrr_info_2.PipeDmcScanlineUpper,
                                                                     mmio_output[0].TimeStamp))

    if status:
        logging.info("\t\tPASS: TRANS_VRR_CTL_REG and PIPE_DMC_SCANLINE_CMP_UPPER_REG programmed properly for "
                     "VRR GuardBand and Scanline cmp upper")
    return status


##
# @brief        Helper API to verify VRR GuardBand programming
# @param[in]    adapter Adapter
# @param[in]    panel, Panel, panel object of the targeted display
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_sdp_programming(adapter: Adapter, panel: Panel):
    status = True
    # ignoring verification for native HDMI 2.1 panel
    if panel.hdmi_2_1_caps.is_hdmi_2_1_native:
        logging.info("\tSkipping verification for SDP programming")
        return status
    ##
    # Feature is valid from Gen13 onwards (DG2 A0 has an issue, so skipping the check)
    if adapter.name in PRE_GEN_13_PLATFORMS or panel.vrr_caps.is_vrr_sdp_supported is False \
            or (adapter.name in ['DG2'] and adapter.cpu_stepping == 0):
        return status

    logging.info("\tVerifying SDP  programming")
    adaptive_sync_capability = dpcd.AdaptiveSyncCapability(panel.target_id)  # address 0x2214
    sdp_one_line_earlier = dpcd.AdaptiveSyncSdpTransmissionTimingConfig(panel.target_id)  # address 0x11B
    # checking if SDP pck sent one line before or not
    if adaptive_sync_capability.as_sdp_first_half_line == 0x1 and panel.vrr_caps.is_vrr_sdp_supported is True \
            and sdp_one_line_earlier.as_sdp_one_line_earlier_enable == 0x01:
        logging.info("\tPASS, SDP one line earlier enable correctly")
    else:
        logging.error("\tFAIL, SDP one line earlier not enable incorrectly")
        status = False
    return status


##
# @brief        Helper API to verify EMP AS SDP Transmission line
# @param[in]    adapter Adapter
# @param[in]    panel, Panel, panel object of the targeted display
# @param[in]    is_modeset optional, Whether verifying during modeset
# @param[in]    start optional, start time
# @param[in]    end optional, end time
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_emp_as_sdp_tl_programming(adapter: Adapter, panel: Panel, is_modeset=False, start=None, end=None):
    status = True
    ##
    # Feature is valid from Gen15 onwards (Also supported for BMG and ARL - TBD)
    if adapter.name in (PRE_GEN_14_PLATFORMS + ['MTL']):
        logging.info("\tSkipping EmpAsSdpTl verification for Pre Gen14 and MTL platforms.")
        return status
    if panel.vrr_caps.is_vrr_sdp_supported:
        logging.info("SDP supported")
    else:
        logging.info("SDP not supported")

    # ignoring verification for displays other than native HDMI 2.1 panel
    if panel.panel_type == "HDMI" and not panel.hdmi_2_1_caps.is_hdmi_2_1_native:
        logging.info("\tSkipping EmpAsSdpTl verification for displays other than native HDMI 2.1 panel.")
        return status
    elif panel.panel_type == "DP" and (not panel.vrr_caps.is_vrr_sdp_supported or is_modeset):
        logging.info("\tSkipping EmpAsSdpTl verification for eDP or DP panels without SDP or during modeset.")
        return status

    logging.info("\tVerifying EMP AS SDP TL programming")
    emp_regs = adapter.regs.get_emp_offsets(panel.transcoder_type)
    emp_as_sdp_tl_output = etl_parser.get_mmio_data(emp_regs.EmpAsSdpTl, is_write=True, start_time=start, end_time=end)
    if emp_as_sdp_tl_output is None:
        logging.error(
            "\t\tNo MMIO operation found for EMP_AS_SDP_TL_REGISTER.")
        gdhm.report_driver_bug_os("[OsFeatures][VRR] No MMIO operation found for EMP_AS_SDP_TL_REGISTER")
        status = False
        return status

    timings_info = adapter.regs.get_timing_info(panel.transcoder_type)
    if panel.panel_type == "HDMI":
        expected_emp_as_sdp_tl = timings_info.VTotal - timings_info.VActive - 1

    else:
        expected_emp_as_sdp_tl = timings_info.VTotal - timings_info.VSyncStart

        adaptive_sync_capability = dpcd.AdaptiveSyncCapability(panel.target_id)  # address 0x2214
        # checking if support for SDP pck sent one line before or not
        if adaptive_sync_capability.as_sdp_first_half_line == 0x1:
            expected_emp_as_sdp_tl += 1

    emp_info = adapter.regs.get_emp_info(panel.transcoder_type, EmpOffsetValues(EmpAsSdpTl=emp_as_sdp_tl_output[
        -1].Data))

    if emp_info.EmpAsSdpTl != expected_emp_as_sdp_tl:
        logging.error(f"\t\tEMP AS SDP TL not set correctly for panel : {panel.port}, "
                      f"expected: {expected_emp_as_sdp_tl}, Observed: {emp_info.EmpAsSdpTl}")

        gdhm.report_driver_bug_os(f"[OsFeatures][VRR] EMP AS SDP TL not set correctly for panel:  {panel.port}")
        status = False
    else:
        logging.info(
            f"\t\tEMP AS SDP TL set correctly for panel: {panel.port} at TimeStamp: "
            f"{emp_as_sdp_tl_output[-1].TimeStamp}")

    return status


##
# @brief        Helper API to verify VRR VTEM programming during modeset
# @param[in]    adapter Adapter
# @param[in]    panel, Panel, panel object of the targeted display
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_vtem_programming_during_modeset(adapter: Adapter, panel: Panel):
    status = True

    ##
    # Feature is valid from Gen14 onwards for HDMI 2.1 native panel only
    if adapter.name in PRE_GEN_14_PLATFORMS or panel.hdmi_2_1_caps.is_hdmi_2_1_native is False:
        logging.info(f"\tHDMI 2.1 native not supported on {adapter.name} or {panel.port}")
        return status
    logging.info(f"\tVerifying VTEM  programming during Mode Set")
    status = __check_vtem_programming(adapter, panel)
    return status


def __check_vtem_programming(adapter: Adapter, panel: Panel, start=None, end=None):
    status = True
    payload_byte = 11  # 11bype payload PB0 to PB10
    zero_padding_byte = 17  # remaining zero pading for 7Dword
    total_byte = payload_byte + zero_padding_byte
    byte_in_one_packet = 28  # as per bspec its 24 confirm with

    logging.debug("\t\tVerifying EMP CTL register")
    emp_regs = adapter.regs.get_emp_offsets(panel.transcoder_type)
    emp_control_output = etl_parser.get_mmio_data(emp_regs.EmpControl, is_write=True, start_time=start,
                                                  end_time=end)
    if emp_control_output is None:
        logging.error(
            "\t\tNo MMIO operation found for HDMI_EMP_CTL_REGISTER for HDMI 2.1 VRR panel")
        gdhm.report_driver_bug_os("[OsFeatures][VRR] No MMIO operation found for HDMI_EMP_CTL_REGISTER"
                                  " for HDMI 2.1 VRR panel")
        status = False
    else:
        for emp_control in emp_control_output:
            emp_ctl = adapter.regs.get_emp_info(panel.transcoder_type,
                                                EmpOffsetValues(EmpControl=emp_control.Data))

            # for HDMI 2.1 VRR supported panel it should be 1 (VTEM packet type)
            if emp_ctl.EmpType != 1:
                logging.error(f"\t\tEMP Type not set to VTEM for panel : {panel.port}")
                gdhm.report_driver_bug_os("[OsFeatures][VRR] EMP Type not set to VTEM")
                status = False
            else:
                logging.info(
                    f"\t\tEMP Type set to VTEM for panel: {panel.port} at TimeStemp: {emp_control.TimeStamp}")

    logging.debug("\t\tVerifying EMP HEADER register")
    emp_header_output = etl_parser.get_mmio_data(emp_regs.EmpHeader, is_write=True, start_time=start,
                                                 end_time=end)
    if emp_header_output is None:
        logging.error(
            "\t\tNo MMIO operation found for HDMI_EMP_HEADER_REGISTER for HDMI 2.1 VRR panel")
        gdhm.report_driver_bug_os(
            "[OsFeatures][VRR] No MMIO operation found for HDMI_EMP_HEADER_REGISTER during "
            "open and close game workload for HDMI 2.1 VRR panel")
        status = False
    else:
        for emp_header in emp_header_output:
            emp_header_value = adapter.regs.get_emp_info(panel.transcoder_type,
                                                         EmpOffsetValues(EmpHeader=emp_header.Data))
            # for HDMI 2.1 VRR supported panel hb0_spare should be 0x7f
            if emp_header_value.Hb0Spare != 0x7f:
                logging.error(f"\t\tEMP HB0 Spare not set to '0x7f' for panel : {panel.port}")
                gdhm.report_driver_bug_os("[OsFeatures][VRR] EMP HB0 Spare not set to '0x7f' for panel")
                status = False
            else:
                logging.info(f"\t\tEMP HB0 spare set to '0x7f' for panel:{panel.port} at "
                             f"TimeStemp:{emp_header.TimeStamp}")

            # Data Set Type value should be 0
            if emp_header_value.DsType != 0:
                logging.error(f"\t\tEMP DsType not set to '0' for panel : {panel.port}")
                gdhm.report_driver_bug_os("[OsFeatures][VRR] EMP DsType not set to '0'")
                status = False
            else:
                logging.info(
                    f"\t\tEMP DsType set to '0' for panel: {panel.port} at TimeStemp: {emp_header.TimeStamp}")
            cal_number_of_packets = total_byte / byte_in_one_packet if total_byte % byte_in_one_packet == 0 else \
                (total_byte / byte_in_one_packet) + 1

            if emp_header_value.NumOfPackets != cal_number_of_packets:
                logging.error(f"\t\tNumber of packets not matching, Expected {cal_number_of_packets}, "
                              f"actual{emp_header_value.NumOfPackets}")
                gdhm.report_driver_bug_os("[OsFeatures][VRR] Number of packets not matching in EMP header")
                status = False
            else:
                logging.info(f"\t\tNumber of packets matching, Expected {cal_number_of_packets}, "
                             f"actual{emp_header_value.NumOfPackets}")

            if emp_header_value.End != 0:
                logging.error(f"\t\tinform End of packet in header, Expected: 0, "
                              f"actual {emp_header_value.End}")
                gdhm.report_driver_bug_os("[OsFeatures][VRR]  informed End of packet in header")
                status = False
            else:
                logging.info(f"\t\tinform End of packet in header, Expected: 0, "
                             f"actual{emp_header_value.End}")

    logging.debug("\t\tVerifying EMP DATA register")
    data_status = True
    expected_payload_dir = {"PB0": 132, "PB1": 0, "PB2": 1, "PB3": 0, "PB4": 1, "PB5": 0, "PB6": 4}
    expected_vrr_en = True
    expected_m_const = False
    expected_fva_factor = 0
    expected_base_refreshrate = [0]
    expected_base_vfront = [0]

    # vfront value
    timings_info = adapter.regs.get_timing_info(panel.transcoder_type)
    expected_base_vfront.append(abs(timings_info.VSyncStart - timings_info.VBlankStart))

    # base refreshrate calculation
    current_mode = __display_config.get_current_mode(panel.display_info.DisplayAndAdapterInfo)
    if current_mode is None:
        logging.error("\t\tAPI get_current_mode() Failed (Test Issue)")
        gdhm.report_test_bug_di("API get_current_mode() Failed (Test Issue)")
        return False

    expected_base_refreshrate.append(round(
        float(current_mode.pixelClock_Hz) / ((timings_info.HTotal + 1) * (timings_info.VTotal + 1))))

    emp_data_output = etl_parser.get_mmio_data(emp_regs.EmpData, start_time=start, end_time=end)
    if emp_data_output is None:
        logging.error(
            f"\t\tNo MMIO operation found for HDMI_EMP_DATA_REGISTER for HDMI 2.1 VRR panel")
        gdhm.report_driver_bug_os("[OsFeatures][VRR] No MMIO operation found for HDMI_EMP_DATA_REGISTER"
                                  " for HDMI 2.1 VRR panel")
        data_status = False
    else:
        # collect all emp_data program to emp_data register and make into list
        emp_data_list = []
        for emp_data in emp_data_output:
            emp_data_value = adapter.regs.get_emp_info(panel.transcoder_type,
                                                       EmpOffsetValues(EmpData=emp_data.Data))
            emp_data_list.append(emp_data_value.EmpData)

        # parse emp_data value and verify payload
        emp_parser = HdmiEmpDataBlock()
        emp_parser.parse_hdmi_emp_data_block(emp_data_list)
        if emp_parser.get_pb0 != expected_payload_dir["PB0"]:
            logging.error(f"""\t\tPB0 value is not matching, expected {expected_payload_dir["PB0"]}, actual: 
                                      {emp_parser.get_pb0}""")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] PB0 value is not matching in EMP data packet")
            data_status = False

        if emp_parser.get_pb1 != expected_payload_dir["PB1"]:
            logging.error(f"""\t\tPB1 value is not matching, expected {expected_payload_dir["PB1"]}, actual: 
                                      {emp_parser.get_pb1}""")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] PB1 value is not matching in EMP data packet")
            data_status = False

        if emp_parser.get_pb2 != expected_payload_dir["PB2"]:
            logging.error(f"""\t\tPB2 value is not matching, expected {expected_payload_dir["PB2"]}, actual: 
                                      {emp_parser.get_pb2}""")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] PB2 value is not matching in EMP data packet")
            data_status = False

        if emp_parser.get_pb3 != expected_payload_dir["PB3"]:
            logging.error(f"""\t\tPB3 value is not matching, expected {expected_payload_dir["PB3"]}, actual: 
                                      {emp_parser.get_pb3}""")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] PB3 value is not matching in EMP data packet")
            data_status = False

        if emp_parser.get_pb4 != expected_payload_dir["PB4"]:
            logging.error(f"""\t\tPB4 value is not matching, expected {expected_payload_dir["PB4"]}, actual: 
                                      {emp_parser.get_pb4}""")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] PB4 value is not matching in EMP data packet")
            data_status = False

        if emp_parser.get_pb5 != expected_payload_dir["PB5"]:
            logging.error(f"""\t\tPB5 value is not matching, expected {expected_payload_dir["PB5"]}, actual: 
                                      {emp_parser.get_pb5}""")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] PB5 value is not matching in EMP data packet")
            data_status = False

        if emp_parser.get_pb6 != expected_payload_dir["PB6"]:
            logging.error(f"""\t\tPB6 value is not matching, expected {expected_payload_dir["PB6"]}, actual: 
                                      {emp_parser.get_pb6}""")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] PB6 value is not matching in EMP data packet")
            data_status = False

        if emp_parser.vrr_en != expected_vrr_en:
            logging.error(f"\t\tVRR en bit is not set, expected {expected_vrr_en}, actual: {emp_parser.vrr_en}")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] VRR en bit is not set in EMP data packet")
            data_status = False

        if emp_parser.m_const != expected_m_const:
            logging.error(
                f"\t\tM_const is not matching, expected {expected_m_const}, actual: {emp_parser.m_const}")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] M_const is not matching in EMP data packet")
            data_status = False

        if emp_parser.fva_factor_m1 != expected_fva_factor:
            logging.error(f"\t\tFVA factor is not matching, expected {expected_fva_factor}, actual: "
                          f"{emp_parser.fva_factor_m1}")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] FVA factor is not matching in EMP data packet")
            data_status = False

        if emp_parser.base_vfront not in expected_base_vfront:
            logging.error(f"\t\tBase Vfront is not matching, expected {expected_base_vfront}, actual: "
                          f"{emp_parser.base_vfront}")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] Base Vfront is not matching in EMP data packet")
            data_status = False

        if emp_parser.base_refresh_rate not in expected_base_refreshrate:
            logging.error(
                f"\t\tBase refresh-rate  is not matching, expected {expected_base_refreshrate}, actual: "
                f"{emp_parser.base_refresh_rate}")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] Base refresh-rate  is not matching in EMP data packet")
            data_status = False

    if data_status:
        logging.info("\t\tPASS: VTEM Data register verification successful ")
    status &= data_status
    return status


##
# @brief        Helper API to verify VRR VTEM programming during game playback
# @param[in]    adapter Adapter
# @param[in]    panel, Panel, panel object of the targeted display
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_vtem_prgm_during_game_play(adapter: Adapter, panel: Panel):
    status = True

    ##
    # Feature is valid from Gen14 onwards for HDMI 2.1 native panel only
    if adapter.name in PRE_GEN_14_PLATFORMS or panel.hdmi_2_1_caps.is_hdmi_2_1_native is False:
        logging.info(f"\tHDMI 2.1 native not supported on {adapter.name} or {panel.port}")
        return status

    rrswitch_info = etl_parser.get_event_data(etl_parser.Events.RR_SWITCH_INFO)
    enable_gaming_vrr_list = []
    # loop through event
    start_event_timestemp = None
    for info_event in rrswitch_info:
        # ignore event for other target id
        if info_event.TargetId != panel.target_id:
            continue
        # ignore event other than Variable mode and VRR method.
        if info_event.RrSwitchMethod == "DD_RR_SWITCH_METHOD_VRR" and info_event.RrMode == \
                "DD_REFRESH_RATE_MODE_VARIABLE":
            if not info_event.IsCurrent:
                start_event_timestemp = info_event.TimeStamp
            if info_event.IsCurrent and start_event_timestemp is not None:
                enable_gaming_vrr_list.append((start_event_timestemp, info_event.TimeStamp))
                start_event_timestemp = None
        else:
            logging.debug(f"ignoring event at {info_event.TimeStamp} for game launch")

    # loop through enable_gaming_vrr_list for VTEM packet verification during gaming VRR enable
    for start_t, end_t in enable_gaming_vrr_list:
        logging.info(f"\tVerifying VTEM  programming during Game launch from [{start_t} to {end_t}]")
        status &= __check_vtem_programming(adapter, panel, start=start_t, end=end_t)
    # todo currently driver is nor programming header to update end of packet , enable below code once enable
    disable_gaming_vrr_list = []
    # loop through event
    start_event_timestemp = None
    for info_event in rrswitch_info:
        # ignore event for other target id
        if info_event.TargetId != panel.target_id:
            continue
        # ignore event other than Variable mode and VRR method.
        if info_event.RrSwitchMethod == "DD_RR_SWITCH_METHOD_VRR" and \
                info_event.RrMode == "DD_REFRESH_RATE_MODE_FIXED":
            if not info_event.IsCurrent:
                start_event_timestemp = info_event.TimeStamp

            if info_event.IsCurrent and start_event_timestemp is not None:
                disable_gaming_vrr_list.append((start_event_timestemp, info_event.TimeStamp))
                start_event_timestemp = None
        else:
            logging.debug(f"\t\tignoring event at {info_event.TimeStamp} for close game")
    # loop through disable_gaming_vrr_list for VTEM packet verification during gaming VRR disable
    for start_t, end_t in disable_gaming_vrr_list:
        logging.info(f"\tVerifying VTEM  programming during Game close from [{start_t} to {end_t}]")
        status &= __check_vtem_programming(adapter, panel, start_t, end_t)
    return status


##
# @brief        Helper API to verify VRR_STATUS programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_vrr_status_programming(adapter: Adapter, panel: Panel):
    status = True
    logging.info("\tVerifying TRANS_VRR_STATUS_REGISTER programming")

    vrr_active_period = get_vrr_active_period(adapter, panel)
    if vrr_active_period is None:
        logging.error("\t\tNo VRR active period found")
        return False

    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    for vrr_active_start, vrr_active_end in vrr_active_period:
        vrr_status_output = etl_parser.get_mmio_data(
            vrr_regs.VrrStatus, start_time=vrr_active_start, end_time=vrr_active_end)
        if vrr_status_output is None:
            logging.error(
                "\t\tNo MMIO operation found for TRANS_VRR_STATUS_REGISTER for VRR active period "
                "({0}, {1})".format(vrr_active_start, vrr_active_end))
            status = False
        else:
            for mmio_data in vrr_status_output:
                vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrStatus=mmio_data.Data))
                if vrr_info.VrrEnableLive is False:
                    if (vrr_active_start + 50) < mmio_data.TimeStamp < (vrr_active_end - 50):
                        logging.error(
                            "\t\tTRANS_VRR_STATUS_REGISTER(bit:27) got disabled during (TimeStamp= {0}) VRR active "
                            "period ({1}, {2})".format(mmio_data.TimeStamp, vrr_active_start, vrr_active_end))
                        status = False
            if status:
                logging.info(
                    "\t\tPASS: TRANS_VRR_STATUS_REGISTER(bit:27) was enabled during VRR active period"
                    "({0}, {1})".format(vrr_active_start, vrr_active_end))
    return status


##
# @brief        Helper API to verify VRR_STATUS programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_vrr_status_programming_modeset(adapter: Adapter, panel: Panel):
    status = True
    logging.info("\tVerifying TRANS_VRR_STATUS_REGISTER programming")
    if not panel.vrr_caps.is_always_vrr_mode:
        logging.info("Always in VRR mode not enable returning early")
        return status

    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)

    vrr_status_output = etl_parser.get_mmio_data(vrr_regs.VrrStatus)
    if vrr_status_output is None:
        # for non vrr panel if always vrr mode not enable then status register will not program.
        if not panel.vrr_caps.is_always_vrr_mode_on_non_vrr_panel:
            logging.info("\t\tMMIO operation not found for TRANS_VRR_STATUS_REGISTER during modeset for Non VRR panel")
            return status
        # failing in case for always vrr enable for both VRR and non VRR panel
        logging.error(
            "\t\tNo MMIO operation not found for TRANS_VRR_STATUS_REGISTER during modeset")
        status = False
    else:
        for mmio_data in vrr_status_output:
            vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrStatus=mmio_data.Data))
            if vrr_info.VrrEnableLive is False:
                logging.error(f"\t\tTRANS_VRR_STATUS_REGISTER(bit:27) got disabled during mode-set"
                              f"(TimeStamp= {mmio_data.TimeStamp})")
                gdhm.report_driver_bug_os(f"[OsFeatures][VRR] TRANS_VRR_STATUS_REGISTER(bit:27) got disabled during "
                                          f"mode-set")
                status = False
        if status:
            logging.info("\t\tPASS: TRANS_VRR_STATUS_REGISTER(bit:27) was enabled during Mode-set")
    return status


##
# @brief        Helper API to verify VRR_STATUS register to see VmaxReached bit is set as expected
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @param[in]    flag_set_expected - True - bit is expected to be 1 False otherwise
# @return       status, Boolean, True if verification is successful, False otherwise
def check_vrr_status_vmax_reached(adapter: Adapter, panel: Panel, flag_set_expected=False):
    html.step_start("Verifying vmaxReachedFlag in VrrStatus Register")
    status = True
    vrr_active_region = get_vrr_active_period(adapter, panel)
    for start, stop in vrr_active_region:
        event_data = etl_parser.get_event_data(etl_parser.Events.VRR_ADAPTIVE_BALANCE_APPLY, start_time=start,
                                               end_time=stop)
        if len(event_data) < 3:
            logging.error("Adaptive balance was not kicked in")
            continue
        adaptive_balance_start, adaptive_balance_stop = event_data[1].TimeStamp, event_data[-1].TimeStamp
        vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
        vrr_status_output = etl_parser.get_mmio_data(vrr_regs.VrrStatus, start_time=adaptive_balance_start,
                                                     end_time=adaptive_balance_stop)
        if vrr_status_output is None:
            logging.error(
                "\t\tNo MMIO operation found for TRANS_VRR_STATUS_REGISTER for Adaptive balance active period "
                "({0}, {1})".format(adaptive_balance_start, adaptive_balance_stop))
            gdhm.report_driver_bug_os(
                "[OsFeatures][VRR]No MMIO operation found for TRANS_VRR_STATUS_REGISTER for Adaptive "
                "balance active period ")
            status = False
        else:
            bit31 = lambda x: ((x & (1 << 31)) >> 31)
            for mmio_data in vrr_status_output:
                vmax_reached = bit31(mmio_data.Data)
                fail_count = 0
                # (VmaxReached, flag_set_expected) : Result
                result_dict = {
                    (0, False): "Bit not set as expected",
                    (0, True): "Bit was expected to be set",
                    (1, False): "Bit was not expected to be set",
                    (1, True): "Bit set as expected"
                }
                result = bool(vmax_reached) == flag_set_expected
                logger = logging.debug if result else logging.warning
                logger(f"\t\tTRANS_VRR_STATUS_REGISTER(bit:31) {result_dict[(vmax_reached, flag_set_expected)]} "
                       f"(TimeStamp= {mmio_data.TimeStamp}) Adaptive balance"
                       f" active period ({adaptive_balance_start}, {adaptive_balance_stop})")
                status &= result
                if not status:
                    logging.error("TRANS_VRR_STATUS_REGISTER(bit:31) bit programming not as expected")
                    gdhm.report_driver_bug_os(
                        "[OSFeatures][VRR] TRANS_VRR_STATUS_REGISTER(bit:31) bit programming not as expected")

    html.step_end()
    return status


##
# @brief        Helper API to verify TRANS_PUSH programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @return       status Boolean, True if verification is successful, False otherwise
def __check_trans_push_programming(adapter: Adapter, panel: Panel):
    status = True
    logging.info("\tVerifying TRANS_PUSH_REGISTER programming")

    vrr_active_period = get_vrr_active_period(adapter, panel)
    if vrr_active_period is None:
        logging.error("\t\tNo VRR active period found")
        return False

    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    for vrr_active_start, vrr_active_end in vrr_active_period:
        vrr_status_output = etl_parser.get_mmio_data(
            vrr_regs.VrrPush, start_time=vrr_active_start, end_time=vrr_active_end, is_write=True)
        if vrr_status_output is None:
            logging.info(
                "\t\tNo MMIO operation found for TRANS_PUSH_REGISTER for VRR active period "
                "({0}, {1})".format(vrr_active_start, vrr_active_end))
        else:
            push_enable_count = 0
            push_disable_count = 0
            send_push_count = 0
            for mmio_data in vrr_status_output:
                vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrPush=mmio_data.Data))
                if vrr_info.PushEnable:
                    push_enable_count += 1
                else:
                    push_disable_count += 1

                if vrr_info.SendPush:
                    send_push_count += 1
            logging.info("\t\tPUSH_ENABLE= {0}, PUSH_DISABLE= {1}, SEND_PUSH= {2}".format(
                push_enable_count, push_disable_count, send_push_count))
    return status


##
# @brief        Helper API to verify TRANS_PUSH programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @return       status Boolean, True if verification is successful, False otherwise
def __check_trans_push_programming_modeset(adapter: Adapter, panel: Panel):
    status = True
    logging.info("\tVerifying TRANS_PUSH_REGISTER programming")
    if not panel.vrr_caps.is_always_vrr_mode:
        logging.info("Always in VRR mode not enable returning early")
        return status

    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    vrr_status_output = etl_parser.get_mmio_data(vrr_regs.VrrPush, is_write=True)
    if vrr_status_output is None:
        # for non vrr panel if always vrr mode not enable then status register will not program.
        if not panel.vrr_caps.is_always_vrr_mode_on_non_vrr_panel:
            logging.info("\t\tMMIO operation not found for TRANS_VRR_STATUS_REGISTER during modeset for Non VRR panel")
            return status
        # failing in case for always vrr enable for both VRR and non VRR panel
        logging.error("\t\tNo MMIO operation found for TRANS_PUSH_REGISTER during mode-set")
        gdhm.report_driver_bug_os("[OsFeatures][VRR] No MMIO operation found for TRANS_PUSH_REGISTER during mode-set")
        status = False
    else:
        push_enable_count = 0
        push_disable_count = 0
        send_push_count = 0
        for mmio_data in vrr_status_output:
            vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrPush=mmio_data.Data))
            if vrr_info.PushEnable:
                push_enable_count += 1
            else:
                push_disable_count += 1
            if vrr_info.SendPush:
                send_push_count += 1
        # for non vrr panel no push enable event if always in vrr mode not enable
        if push_enable_count < 0:
            if not panel.vrr_caps.is_always_vrr_mode_on_non_vrr_panel:
                logging.info("Push enable not set for non VRR panel")
            else:
                logging.error("Push enable not set for non VRR panel expected: Enable, actual: Disable")
                gdhm.report_driver_bug_os("[OsFeatures][VRR] Push enable not set for non VRR panel expected: Enable, "
                                          "actual: Disable")
                status = False
        else:
            logging.info(f"\t\tPUSH_ENABLE= {push_enable_count} during mode-set")
        # Change is due to VRR MSA WA issue on PTL
        if adapter.name in common.GEN_16_PLATFORMS and panel.panel_type == "DP" and panel.is_lfp == False:
            if send_push_count != 1:
                logging.error(f"\t\tSEND_PUSH= {send_push_count} during mode-set,expected: 1")
                gdhm.report_driver_bug_os("[OsFeatures][VRR] SEND_PUSH during mode-set, expected: 1")
                status = False
        else:
            if send_push_count > 0:
                logging.error(f"\t\tSEND_PUSH= {send_push_count} during mode-set,expected: 0")
                gdhm.report_driver_bug_os("[OsFeatures][VRR] SEND_PUSH during mode-set, expected: 0")
                status = False
    return status


##
# @brief        Helper API to verify MSA_TIMING_PAR_IGNORED_EN DPCD programming
#               if panel supports VRR we need to set MsaTimingParIgnoreEnable of DPCD 107 at sink
# @param[in]    panel Panel, panel object of the targeted display
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_msa_timing_dpcd(panel: Panel):
    status = True
    if panel.hdmi_2_1_caps.is_hdmi_2_1_native:
        logging.info("\tSkipping verification for MSA_TIMING programming")
        return status
    logging.info("\tVerifying DOWN_SPREAD_CTL:MSA_TIMING programming")
    down_spread_ctl = dpcd.DownSpreadCtl(panel.target_id)
    active_mode = __display_config.get_current_mode(panel.target_id)
    is_fixed_rr_supported = panel.vrr_caps.is_always_vrr_mode  # by default enable considering all panel support
    # fixed RR.
    if panel.is_lfp:
        is_fixed_rr_supported &= panel.lrr_caps.is_lrr_2_5_supported
    if panel.vrr_caps.is_vrr_supported and (active_mode.refreshRate > panel.vrr_caps.vrr_min_rr):
        # check for EDP/DP/ HDMI 2.1 PCON MSA ignore bit should enable even Gaming VRR disable to support fixed RR
        if not panel.hdmi_2_1_caps.is_hdmi_2_1_native:
            if down_spread_ctl.msa_timing_par_ignored_en == 0x1:
                logging.info("\t\tPASS: DOWN_SPREAD_CTL:MSA_TIMING_PAR_IGNORED_EN Expected= 0x1, Actual= 0x1")
            else:
                if not is_fixed_rr_supported:
                    logging.info("\t\tPASS: DOWN_SPREAD_CTL:MSA_TIMING_PAR_IGNORED_EN Expected= 0x0, Actual= 0x0")
                else:
                    logging.error("\t\tFAIL: DOWN_SPREAD_CTL:MSA_TIMING_PAR_IGNORED_EN Expected= 0x1, Actual= 0x0")
                    gdhm.report_driver_bug_os("[OsFeatures][VRR] DOWN_SPREAD_CTL:MSA_TIMING_PAR_IGNORED_EN "
                                              "Expected= 0x1, Actual= 0x0")
                    status = False
    else:
        if down_spread_ctl.msa_timing_par_ignored_en == 0x1:
            logging.error("\t\tFAIL: DOWN_SPREAD_CTL:MSA_TIMING_PAR_IGNORED_EN Expected= 0x0, Actual= 0x1")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] DOWN_SPREAD_CTL:MSA_TIMING_PAR_IGNORED_EN Expected= 0x0, "
                                      "Actual= 0x1")
            status = False
        else:
            logging.info("\t\tPASS: DOWN_SPREAD_CTL:MSA_TIMING_PAR_IGNORED_EN Expected= 0x0, Actual= 0x0")

    return status


##
# @brief        Helper function to calculate expected v_min and v_max
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @return       v_min expected VRR V_MIN value
#               v_max expected VRR V_MAX value
#               v_active expected VRR V_MIN value
#               drrs_v_max expected DRRS V_MAX value
#               dfr_v_max expected BFR V_MAX value
#               intel Arc sync profile - tuple for profile with min, max and time for scane line in us
# @note         App can do a mode set at the time of launch based on current resolution and refresh rate, and revert
#               back to original mode before closing. Relying on the current mode to calculate v_min and v_max is
#               not correct. Track any in-between mode set and calculate the expected v_min and v_max value based on
#               the set timing parameters.
def __get_expected_v_min_max(adapter: Adapter, panel: Panel):
    current_mode = __display_config.get_current_mode(panel.display_info.DisplayAndAdapterInfo)
    assert current_mode is not None, "API get_current_mode() Failed (Test Issue)"
    current_profile = False
    if adapter.name not in PRE_GEN_13_PLATFORMS:
        current_profile = get_current_profile(panel)

    # Get the first mode set happened after opening the app if any
    set_timing_data = etl_parser.get_event_data(etl_parser.Events.SET_TIMING)

    # Get VRR enable events to select last mode set entry before VRR got enabled
    vrr_enable_event_output = etl_parser.get_event_data(etl_parser.Events.RR_SWITCH_INFO)
    vrr_enable_event = [
        _ for _ in vrr_enable_event_output
        if _.TargetId == panel.target_id and ((_.RrMode == "DD_REFRESH_RATE_MODE_VARIABLE") and _.IsCurrent)]

    intermediate_mode_set = None
    if set_timing_data is not None:
        for mode_set_entry in set_timing_data:
            logging.info("\tIntermediate ModeSet: {0}".format(mode_set_entry))
            if mode_set_entry.Port != ('PORT_' + panel.port[-1]):
                continue
            if mode_set_entry.RR is None or mode_set_entry.RR == 0:
                continue
            if mode_set_entry.HTotal is None or mode_set_entry.HTotal == 0:
                continue
            if mode_set_entry.HActive is None or mode_set_entry.HActive == 0:
                continue
            if mode_set_entry.VTotal is None or mode_set_entry.VTotal == 0:
                continue
            if mode_set_entry.VActive is None or mode_set_entry.VActive == 0:
                continue
            if mode_set_entry.DotClock is None or mode_set_entry.DotClock == 0:
                continue
            # Discard the mode set entries happened after VRR got enabled
            if len(vrr_enable_event) != 0 and mode_set_entry.TimeStamp > vrr_enable_event[0].TimeStamp:
                continue
            intermediate_mode_set = mode_set_entry

            if intermediate_mode_set is not None:
                logging.info("\tSelected Intermediate ModeSet: {0}".format(intermediate_mode_set))

    if intermediate_mode_set is not None:
        h_total = intermediate_mode_set.HTotal
        v_total = intermediate_mode_set.VTotal
        v_active = intermediate_mode_set.VActive
        pixel_clock = intermediate_mode_set.DotClock
        rr = intermediate_mode_set.RR
    else:
        # If there is no intermediate mode set detected, read the HTotal and VTotal values from registers
        logging.debug("\tNo intermediate mode set detected, reading HTotal and VTotal values from timing")
        timings_info = adapter.regs.get_timing_info(panel.transcoder_type)
        # as per Bpec, programmed to the number of pixels desired minus one. so adding plus 1.
        h_total = timings_info.HTotal + 1

        #  VTotal register is double buffered in Gen12+ platforms. Value of this register can be changed
        #  dynamically in LRR2.5 cases. VrrVmin value depends on VTotal value. Reading the register after
        #  closing the VRR app can give wrong value.
        #  Making it generic for all platform, not to read value from register for VTotal and vActive.
        display_timings = __display_config.get_display_timings(panel.display_info.DisplayAndAdapterInfo)
        v_total = display_timings.vTotal
        v_active = display_timings.vActive

        pixel_clock = current_mode.pixelClock_Hz
        rr = current_mode.refreshRate

    # incase current applied RR is greater than max MRL range, then consider MAX MRL for vmin calculate
    if current_mode.refreshRate > panel.vrr_caps.vrr_max_rr:
        logging.debug(
            f"Current applied RR= {current_mode.refreshRate} greater then max MRL={panel.vrr_caps.vrr_max_rr}, "
            f"Consider MAX MRL for vmin")
        if pixel_clock % (h_total * panel.vrr_caps.vrr_max_rr) == 0:
            v_total = pixel_clock // (h_total * panel.vrr_caps.vrr_max_rr)
        else:
            v_total = (pixel_clock // (h_total * panel.vrr_caps.vrr_max_rr)) + 1

    # @note for preGen13, HW restriction: Flipline should always be greater than Vmin (so, decrement Vmin value by 1)
    # other decrement value by 1 due to 0 based address.
    # for Gen13+, Flipline HW restriction has been removed.
    decrement_by = 2 if adapter.name in PRE_GEN_13_PLATFORMS else 1
    v_min = v_total - decrement_by

    # Vmax is register is 0 based , so doing -1 to set under 0 based
    v_max = ((pixel_clock * 1001) // (h_total * panel.vrr_caps.vrr_min_rr * 1000)) - 1

    # calculate bfr_v_max in case current mode is dynamic mode enable for bfr.
    bfr_v_max = 0
    if current_mode.rrMode:
        bfr_v_max = int((pixel_clock + (h_total * rr) / 2) / (h_total * rr)) - 1

    # Vmax is register is 0 based , so doing -1 to set under 0 based
    # In case of DMRRS/DRRS scenario, Vmax value calculated not based on floating point.
    drrs_v_max = int((pixel_clock + (h_total * panel.vrr_caps.min_rr) / 2) / (h_total * panel.vrr_caps.min_rr)) - 1

    # Vmin/Vmax values after considering active IntelArcSync profile
    intel_arc_sync_v_min = None
    intel_arc_sync_v_max = None
    time_for_scanline_in_us = None
    if current_profile is not False and current_profile.IntelArcSyncProfile.value != ARC_SYNC_PROFILE.INVALID.value:
        if h_total and current_profile.MinRefreshRateInHz and current_profile.MaxRefreshRateInHz:
            intel_arc_sync_v_min = v_min
            calculated_rr = math.ceil(round(pixel_clock / (h_total * v_total)))
            logging.info(f"rr: {calculated_rr}, profile MaxRR: {current_profile.MaxRefreshRateInHz}")
            if calculated_rr != int(current_profile.MaxRefreshRateInHz):
                intel_arc_sync_v_min = pixel_clock // (h_total * current_profile.MaxRefreshRateInHz)
            intel_arc_sync_v_max = ((pixel_clock * 1001) // (h_total * current_profile.MinRefreshRateInHz * 1000)) - 1
            time_for_scanline_in_us = round(((10 ** 6 * h_total) / pixel_clock), 3)
    if current_profile is not False and current_profile.IntelArcSyncProfile.value == ARC_SYNC_PROFILE.OFF.value \
            and current_profile.MaxRefreshRateInHz == current_profile.MinRefreshRateInHz:
        intel_arc_sync_v_max = intel_arc_sync_v_min + 1

    return v_min, v_max, v_active, drrs_v_max, bfr_v_max, (intel_arc_sync_v_min, intel_arc_sync_v_max,
                                                           time_for_scanline_in_us)


##
# @brief        Helper function to verify Adaptive DC Balancing
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @param[in]    v_min, Number, v_min of the panel
# @param[in]    v_max, Number, v_max of the panel
# @param[in]    dc_balance_event_expected, Bool, True if DC balance event expecting else False
# @param[in]    is_workload_already_running, Bool, True if workload already running else False
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_vrr_adaptive_dc_balancing(adapter: Adapter, panel: Panel, v_min: int, v_max: int,
                                      dc_balance_event_expected, is_workload_already_running):
    dc_balance_event_count_vrr_active_region = 0
    correction_sensitivity = 50
    guard_band = int((v_max * correction_sensitivity) / 100)
    logging.info("\tVerifying Adaptive DC Balancing programming")
    logging.info(f"\t\tGuardBand Value = {guard_band}")

    # Make sure DC balance is not exceeding the guard band value by too much
    dc_balance_balance_events = etl_parser.get_event_data(etl_parser.Events.VRR_ADAPTIVE_BALANCE_BALANCE)
    # DC balance event not present and Expected DC balance algorithm trigger ( Fail cond for Gen12+)
    if dc_balance_balance_events is None and dc_balance_event_expected:
        # Get flip data from EtlParser for given source ID
        flip_data = etl_parser.get_flip_data(async_flip=True, vrr_flip=True, sourceid=panel.source_id)
        if flip_data is None:
            logging.info(f"\t\tNo Vrr Flip present in etl, so no DC balance event in etl ")
            return True
        if len(flip_data) > 10:
            logging.error("\t\tNo VrrAdaptiveBalance/Balance event found")
            gdhm.report_driver_bug_os("No VrrAdaptiveBalance/Balance event found")
            return False
        # DC balance algo will not enable if number of flips are very less.
        logging.info("\t\tPASS: DC balance algo will not enable if number of flips are very less")
        return True
    # DC balance event present and Expected DC balance algorithm not trigger (fail cond for Gen11, Gen11.5 and DG1)
    if dc_balance_balance_events is not None and not dc_balance_event_expected:
        logging.error("\t\tVrrAdaptiveBalance/Balance event found")
        gdhm.report_driver_bug_os(
            title="VrrAdaptiveBalance/Balance event found",
            priority=gdhm.Priority.P3,
            exposure=gdhm.Exposure.E3
        )
        return False
    # DC balance event not present and Expected DC balance algorithm not trigger (pass cond for Gen11, Gen11.5 and DG1)
    if dc_balance_balance_events is None and not dc_balance_event_expected:
        logging.info("\t\tNo VrrAdaptiveBalance/Balance event found")
        return True

    balance_below_guard_band_count = 0
    balance_above_guard_band_count = 0
    balance_above_2_guard_band_count = 0
    min_balance = math.inf
    avg_balance = 0
    max_balance = -math.inf
    # Balance need to clear with in 10 frame. consider with v_max.
    max_allowed_balance = 10 * v_max
    balance_above_max_allow_limit = 0
    for dc_balance in dc_balance_balance_events:
        if abs(dc_balance.Balance) <= guard_band:
            balance_below_guard_band_count += 1
        else:
            balance_above_guard_band_count += 1

        if abs(dc_balance.Balance) > max_allowed_balance:
            balance_above_max_allow_limit += 1

        if abs(dc_balance.Balance) > (2 * guard_band):
            balance_above_2_guard_band_count += 1

        if min_balance > dc_balance.Balance:
            min_balance = dc_balance.Balance

        if max_balance < dc_balance.Balance:
            max_balance = dc_balance.Balance

        avg_balance += abs(dc_balance.Balance)

    avg_balance /= len(dc_balance_balance_events)

    logging.info(
        f"\t\tTotal Balance Updates= {len(dc_balance_balance_events)}, "
        f"Below GuardBand= {balance_below_guard_band_count}, "
        f"Above GuardBand= {balance_above_guard_band_count}, "
        f"Above 2* GuardBand= {balance_above_2_guard_band_count}, "
        f"Min Balance= {min_balance}, "
        f"Max Balance= {max_balance}, "
        f"Avg Balance= {int(avg_balance)}"
    )
    if balance_above_max_allow_limit > 0:
        logging.error(f"Balance above max allow limit: {max_allowed_balance} happen "
                      f"{balance_above_max_allow_limit} times")
        gdhm.report_driver_bug_os(
            title="Balance value above max allow limit of (10 * v_max)",
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E3
        )

    # Check for DC balancing algo running during VRR active periods
    vrr_active_period = get_vrr_active_period(adapter, panel, consider_iscurrent=True)
    if vrr_active_period is None:
        logging.error("\t\tNo VRR active period found")
        return False
    for vrr_start, vrr_stop in vrr_active_period:
        # skip DC balance check if no VRR flips. VRR can enable for BFR , DRRS , DMRRS and for that no DC balance
        # Get flip data from EtlParser for given source ID
        flip_data = etl_parser.get_flip_data(async_flip=True, vrr_flip=True, start_time=vrr_start, end_time=vrr_stop,
                                             sourceid=panel.source_id)
        if flip_data is None:
            logging.info(f"\t\tNo Async or Vrr Flip during {vrr_start} to {vrr_stop} time")
            flip_data = []

        dc_balance_bal_data = etl_parser.get_event_data(etl_parser.Events.VRR_ADAPTIVE_BALANCE_BALANCE,
                                                        start_time=vrr_start, end_time=vrr_stop)
        # DC balance event not present and Expected DC balance algorithm trigger ( Fail cond for Gen12+ )
        # DC balance event will trigger if we get min 3-5 VRR flips
        if dc_balance_bal_data is None and dc_balance_event_expected:
            min_vrr_active_period = 5 * math.floor(1000.0 / panel.min_rr)
            # Skip if VRR active period is too short  less then 5 flips
            if (vrr_stop - vrr_start) <= min_vrr_active_period:
                logging.debug(f"\t\tVrr active periods is short = {vrr_start} to {vrr_stop} time - skipping it")
                continue
            if len(flip_data) > 5:
                logging.error("\t\tNo VrrAdaptiveBalance/Balance event found")
                gdhm.report_driver_bug_os(
                    title="No VrrAdaptiveBalance/Balance event found",
                    priority=gdhm.Priority.P3,
                    exposure=gdhm.Exposure.E3
                )
                return False
            # continue to next active region in case of less flips
            logging.debug(f"\t\t continue to next active region, {vrr_start} to {vrr_stop} has less flips")
            continue
        # DC balance event present and Expected DC balance algorithm not trigger (fail cond for Gen11, Gen11.5 and DG1)
        if dc_balance_bal_data is not None and not dc_balance_event_expected:
            logging.error("\t\tVrrAdaptiveBalance/Balance event found")
            gdhm.report_driver_bug_os(
                title="VrrAdaptiveBalance/Balance event found",
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            return False
        # DC balance event present and Expected DC balance algorithm not trigger (pass cond for Gen11, Gen11.5 and DG1)
        if dc_balance_bal_data is None and not dc_balance_event_expected:
            logging.info("\t\tNo VrrAdaptiveBalance/Balance event found")
            return True
        logging.debug(f"\t\tLooking in VRR Active Period {vrr_start} : {vrr_stop}")
        if len(flip_data) > 15 and len(dc_balance_bal_data) < 3:
            logging.error(f"\t\tAdaptive balance was not kicked in for active period {vrr_start}:{vrr_stop}")
            return False
        dc_balance_event_count_vrr_active_region += len(dc_balance_bal_data)
        # check for DC balancing active periods only if we have more than 5 VRR flips during vrr active time.
        if len(flip_data) > 15:
            dc_balance_start, dc_balance_stop = dc_balance_bal_data[1].TimeStamp, dc_balance_bal_data[-1].TimeStamp
            # checking if DC balancing algorithm trigger at-least for 70% of VRR active periods.
            # so checking if DC balancing active periods less than 30 then it is issue. need to investigate further.
            if round((dc_balance_stop - dc_balance_start) * 100 / (vrr_stop - vrr_start), 2) < 30:
                logging.error(
                    f"\t\tDC balancing algorithm has run only "
                    f"({round((dc_balance_stop - dc_balance_start) * 100 / (vrr_stop - vrr_start), 2)}%)"
                    f"during VRR active periods {vrr_start} : {vrr_stop}")
                gdhm.report_driver_bug_os(
                    title="DC Balancing algorithm has ran only for short duration",
                    priority=gdhm.Priority.P3,
                    exposure=gdhm.Exposure.E3
                )
                return False
            logging.info(
                f"\t\tDC balancing algorithm has run during {dc_balance_start} : {dc_balance_stop} "
                f"({round((dc_balance_stop - dc_balance_start) * 100 / (vrr_stop - vrr_start), 2)}%)"
                f"during VRR active periods {vrr_start} : {vrr_stop}")

            # checking Previous VTotal value in balance event.
            for dc_balance in dc_balance_bal_data:
                if dc_balance.PreviousVtotal < v_min + 1 or dc_balance.PreviousVtotal > v_max + 1:
                    if dc_balance.PreviousVtotal != v_max:
                        logging.error(f"\t\tDC balance Previous Vtotal Expected= [{v_min + 1}, {v_max + 1}]"
                                      f", Actual= {dc_balance.PreviousVtotal}")
                        return False
            logging.info(f"\t\tDC balance Previous Vtotal in range= [{v_min + 1}, {v_max + 1}]")

    # Make sure DC balance is not running after game playback with check total dc balance event in full etl and
    # dc balance event during vrr active periods.
    if dc_balance_event_count_vrr_active_region != len(dc_balance_balance_events) and not is_workload_already_running:
        panel_adapter_active_duration.clear()
        logging.error(
            f"\t\tError: DC balancing algorithm kicked in after vrr active period."
            f"DC balance event total: {len(dc_balance_balance_events)}, "
            f"active region {dc_balance_event_count_vrr_active_region} are not same")
        gdhm.report_driver_bug_os(
            title="DC balancing algorithm has kicked in after vrr active period",
            priority=gdhm.Priority.P3,
            exposure=gdhm.Exposure.E3
        )
        return False
    logging.info(
        f"\t\tDC balance event total: {len(dc_balance_balance_events)}, "
        f"active region {dc_balance_event_count_vrr_active_region} are same")
    panel_adapter_active_duration.clear()
    return True


# calculate:
#   num_frames: the total number of frames expected for this prediction
#   earlier_vtotal : the desired flip time of each frame earlier than the final one. Ie, the first (num_frames-1) frames
#   final : the desired frame time of the last frame, informational
#   initial_flipline : the minimum frame time for the first frame
#   final_vtotal : the maximum frame time allowed for the final frame.
#   delta : total change predicted, informational
#   Set flipline = intitial_vtotmin    for the first frame.
#   Set flipline = vmin                for all other num_frames.
#   Set vtotal = earlier_vtotal     for the first (num_frames-1) frames.
#   Set vtotal = final_vtotal       for all other num_frames.
# @param[in]    monitor_v_min
# @param[in]    monitor_v_max
# @param[in]    balance
# @param[in]    next_direction
# @param[in]    prediction
# @param[in]    blank_percent
# @param[in]    correction_sensitivity, GuardBandPercent (50)
# @param[in]    guard_band_slope_factor, GBSlopeFactor
# @param[in]    v_max_adjust,
# @param[in]    prediction_error,   Average Prediction Error in micro seconds
# @return       num_adaptive_bal_frames, first_v_min, n_minus_1_v_max, final_v_max, high_prediction_error
def __adaptive_dc_balancing_algo(monitor_v_min, monitor_v_max, balance, next_direction, prediction,
                                 blank_percent, guard_band_percent, guard_band_slope_factor, v_max_adjust,
                                 prediction_error):
    adaptive_balance_v_min = monitor_v_min * 1000
    adaptive_balance_v_max = monitor_v_max * 1000

    # This is the time of an active frame.
    v_min = min(max(monitor_v_min, adaptive_balance_v_min / 1000), monitor_v_max)

    # This is the maximum time the display can handle between active frames.
    v_max = max(adaptive_balance_v_max / 1000, v_min)

    if prediction_error > VRR_ADAP_BAL_PREDICTION_ERROR_MAX_VALUE_IN_MICRO_SEC:
        # If the prediction error is large, then there is little point using the predicted numbers.
        # Switch to fixed max refresh rate instead.
        return 1, v_min, v_min, v_min, True

    # Number of scan-lines of blanking to allow after the predicted time before starting a new active on the final frame
    # This limits the maximum balance that can be generated by the frame on a mis-prediction.
    targeted_blank = math.floor((blank_percent * (v_max - v_min)) / 100)

    # GuardBands for starting to apply corrections. The ideal minimum guard band is typically about v_max/2.
    # Values below this can be used, but the tend to add more frame latency
    guard_band = math.floor((v_max * guard_band_percent) / 100)

    # The adjustments being made are absolute, this can cause the calculation to go below the active time. However,
    # its highly desirable to have a small bit of blank after any active whenever we
    # split a frame into multiples. This is to ensure that we don't force an artificial FPS limit where the final
    # active blocks the GPU from running faster and hence the prediction gets stuck. This
    # sets a minimum final frame time of the active plus the specified percentage of the time between active and final
    # prediction pre-adjustment.
    v_min_min_percent = 25

    # Calculate the minimum number of frames that could be used
    num_frames = int(prediction / v_max) + 1

    # Increase the num frames until the first case that's lower than the blank target.
    while (prediction / (num_frames + 1) > v_min) and ((prediction / num_frames) - v_min) > targeted_blank:
        num_frames = num_frames + 1

    # calculate the desired final frame time
    final_frame_time = max(math.floor(prediction / num_frames), v_min)

    first_v_min = v_min

    # For simplicity, always assume first frame is positive when calculating
    modified_balance = balance * next_direction

    # Calculate the worst extreme of balance, first frame is always positive, so just need to check this case
    if num_frames > 1 and modified_balance > (-final_frame_time / 2):
        modified_balance = modified_balance + final_frame_time

    # Calculate the size of the adjustment to apply to this frame
    # adjustment will be zero below the GuardBand and then some number of milliseconds relative to the distance beyond
    # the GuardBand.
    adjust = max(0, (abs(modified_balance) - guard_band))
    adjust = (adjust * guard_band_slope_factor) / guard_band

    # calculate how to adjust the final to alter the balance
    if modified_balance < 0:
        # negative
        if num_frames % 2 == 1:
            final_frame_time = min(final_frame_time + adjust, v_max)
        else:
            final_frame_time = max(final_frame_time - adjust,
                                   v_min + math.floor(v_min_min_percent * (final_frame_time - v_min) / 100))
    else:
        # positive
        if num_frames % 2 == 1:
            final_frame_time = max(final_frame_time - adjust,
                                   v_min + math.floor(v_min_min_percent * (final_frame_time - v_min) / 100))
        else:
            final_frame_time = min(final_frame_time + adjust, v_max)

    if num_frames == 1:
        # single frames cases need some adjustments as there is no capability to adjust the middle frame
        if modified_balance < -guard_band:
            # single frame and negative GuardBand frames need to be extended to create convergence.
            first_v_min = final_frame_time
        else:
            # Cannot shorten a single frame case.
            final_frame_time = max(final_frame_time, prediction)

    # calculate the desired time of any earlier frames
    if num_frames > 1:
        n_minus_1_v_max = max((prediction - final_frame_time) / (num_frames - 1), v_min)
    else:
        n_minus_1_v_max = 0

    # Calculate the final VTotal. Reduce the allowance when GuardBand is exceeded
    final_v_max = min(final_frame_time + max(v_max_adjust - adjust, 0), v_max)

    return num_frames, n_minus_1_v_max, first_v_min, final_v_max, False


##
# @brief        Helper API to verify CMTG programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @return       status Boolean, True if verification is successful, False otherwise
def __check_cmtg_disable(adapter: Adapter, panel: Panel):
    status = True
    # Return early if platform not support CMTG.
    if adapter.name in PRE_GEN_13_PLATFORMS or adapter.name in ['DG2']:
        logging.info(f"\t\tCMTG not supported on {adapter.name}")
        return status
    # CMTG is supported only on eDP panels, so skipping CMTG verification for external panels
    if not panel.is_lfp:
        logging.info(f"\t CMTG not supported on external panels. Skipping CMTG verification")
        return status
    logging.info("\tVerifying CMTG Disable during VRR active ")
    vrr_active_period = get_vrr_active_period(adapter, panel)
    if vrr_active_period is None:
        logging.error("\t\tNo VRR active period found")
        return False
    for vrr_active_start, vrr_active_end in vrr_active_period:

        # Verify CMTG disable during VRR active time.
        cmtg_offsets = adapter.regs.get_cmtg_offsets(panel.transcoder_type)
        cmtg_during_game = etl_parser.get_mmio_data(cmtg_offsets.CmtgControlReg, start_time=vrr_active_start,
                                                    end_time=vrr_active_end)
        if cmtg_during_game is None:
            logging.info("\t\tPASS: CMTG enable/disable event not present during VRR active period"
                         "({0}, {1})".format(vrr_active_start, vrr_active_end))
            status &= True
        else:
            for mmio_data in cmtg_during_game:
                cmtg_val = adapter.regs.get_cmtg_info(panel.transcoder_type,
                                                      CmtgOffsetValues(CmtgControlReg=mmio_data.Data))
                if cmtg_val.CmtgEnable == 1:
                    logging.error(f"\t\tCMTG enable during workload {mmio_data.Data} Timestamp {mmio_data.TimeStamp}")
                    status &= False
                else:
                    logging.info(f"\t\tPASS: CMTG disable during workload {mmio_data.Data} Timestamp "
                                 f"{mmio_data.TimeStamp}")
                    status &= True

        # Verify CMTG interrupt during VRR active time.
        interrupt_offsets = adapter.regs.get_interrupt_offsets()
        interrupt_data = etl_parser.get_mmio_data(interrupt_offsets.InterruptIIR, start_time=vrr_active_start,
                                                  end_time=vrr_active_end)
        if interrupt_data is None:
            logging.info("\t\tPASS: No data found for CMTG Vblank interrupt during VRR active period"
                         "({0}, {1})".format(vrr_active_start, vrr_active_end))
            status &= True
        else:
            for data in interrupt_data:
                int_val = adapter.regs.get_interrupt_info(InterruptOffsetValues(InterruptIIR=data.Data))
                if int_val.InterruptIIR_CmtgVblank == 1:
                    logging.error(f"\t\tCMTG Vblank interrupt is enabled {hex(data.Offset)} - {data.Data} at "
                                  f"{data.TimeStamp}")
                    status &= False
                else:
                    logging.info(f"\t\tPASS: CMTG Vblank interrupt is disabled {hex(data.Offset)} - {data.Data} at "
                                 f"{data.TimeStamp}")
                    status &= True
    return status


##
# @brief        Helper API to verify CMTG programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @return       status Boolean, True if verification is successful, False otherwise
def __check_cmtg_post_modeset(adapter: Adapter, panel: Panel):
    status = True
    # Return early if platform not support CMTG.
    if adapter.name in PRE_GEN_14_PLATFORMS:
        logging.info(f"\t\tCMTG not supported during modeset on {adapter.name} platform")
        return status
    # CMTG is supported only on eDP panels, so skipping CMTG verification for external panels
    if not panel.is_lfp:
        logging.info(f"\t CMTG not supported on external panels. Skipping CMTG verification")
        return status
    if not panel.psr_caps.is_psr_supported or panel.psr_caps.psr_version != 0x02:
        logging.info(f"\t CMTG not supported on non PSR2 panels. Skipping CMTG verification")
        return status
    feature_support = psr.verify_psr_restrictions(adapter, panel, psr.UserRequestedFeature.PSR_2)
    if feature_support == psr.UserRequestedFeature.PSR_NONE or feature_support == psr.UserRequestedFeature.PSR_1:
        logging.info(f"\t Skipping CMTG verification as panel fall back to PSR1 or non PSR due to timing restriction")
        return status

    # Verify CMTG enable post modeset.
    cmtg_offsets = adapter.regs.get_cmtg_offsets(panel.transcoder_type)
    cmtg_during_modeset = etl_parser.get_mmio_data(cmtg_offsets.CmtgControlReg)
    if cmtg_during_modeset is None:
        logging.error("\t\tFAIL: CMTG enable/disable event not present post mode set")
        gdhm.report_driver_bug_os(title="[OsFeatures][VRR] CMTG enable/disable event not present post mode set")
        status &= False
    else:
        cmtg_val = adapter.regs.get_cmtg_info(panel.transcoder_type,
                                              CmtgOffsetValues(CmtgControlReg=cmtg_during_modeset[-1].Data))
        if cmtg_val.CmtgEnable == 1:
            logging.info(f"\t\tPASS: CMTG enable post Modeset {cmtg_during_modeset[-1].Data} Timestamp "
                         f"{cmtg_during_modeset[-1].TimeStamp}")
            status &= True
        else:
            logging.error(f"\t\tCMTG Disable post Modeset {cmtg_during_modeset[-1].Data} "
                          f"Timestamp {cmtg_during_modeset[-1].TimeStamp}")
            gdhm.report_driver_bug_os(title="[OsFeatures][VRR] CMTG Disable post Mode-set expected enable")
            status &= False
    return status


##
# @brief        Helper API to verify Prev_vtotal programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @param[in]    profile_v_min applied profile VRR v_min value
# @param[in]    profile_v_max applied profile VRR v_max value
# @param[in]    is_prev_vtotal_check_require, Bool True for check require else False
# @return       status Boolean, True if verification is successful, False otherwise
def __check_vrr_prev_vtotal(adapter: Adapter, panel: Panel, profile_v_min, profile_v_max,
                            check_varying_vtotal):
    status = True
    logging.info("\tVerifying Prev_Vtotal programming")

    vrr_active_period = get_vrr_active_period(adapter, panel)
    if vrr_active_period is None:
        logging.error("\t\tNo VRR active period found")
        return False

    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    for vrr_active_start, vrr_active_end in vrr_active_period:
        vrr_prev_vtotal_output = etl_parser.get_mmio_data(
            vrr_regs.VrrVTotal, start_time=vrr_active_start + 10, end_time=vrr_active_end, is_write=False)
        if vrr_prev_vtotal_output is None:
            logging.warning(
                f"\t\tNo MMIO Read operation found for TRANS_VRR_VTOTAL_PREV_{panel.transcoder_type} for "
                f"VRR active period ({vrr_active_start}, {vrr_active_end})")
        else:
            vtotal_full = [((vrr_prev_vtotal.Data & 0xFFFFF), vrr_prev_vtotal.TimeStamp) for vrr_prev_vtotal in
                           vrr_prev_vtotal_output]
            for val, ts in vtotal_full:
                if val < profile_v_min or val > profile_v_max:
                    logging.error(f"\t\tUnexpected VTotal value ({val}) detected at {ts / 1000}s")
                    status = False
            if not status:
                logging.error(f"\t\tFAIL: Previous Vtotal value exceed from =[{profile_v_min}, {profile_v_max}]")
                gdhm.report_driver_bug_os(
                    title="[OsFeatures][VRR] Previous Vtotal value exceed from vmin-Vmax range "
                )
            else:
                logging.info(f"\t\tPASS: Previous Vtotal value not exceed than =[{profile_v_min}, {profile_v_max}]")

            # if current profile is off , then Previous Vtotal won't change as vmin = vmax = flipline
            if adapter.name not in PRE_GEN_13_PLATFORMS:
                current_profile = get_current_profile(panel)
                if (current_profile is not False and
                        current_profile.IntelArcSyncProfile.value == ARC_SYNC_PROFILE.OFF.value):
                    check_varying_vtotal = False
            # Prev_Vtotal value changing verification require or not
            if check_varying_vtotal:
                vtotal_value_set = set()
                for vtotal_value, ts in vtotal_full:
                    vtotal_value_set.add(vtotal_value)
                if len(vtotal_value_set) < 2:
                    # previous Vtotal value might not change if duration is very short for prediction.
                    if (vrr_active_end - vrr_active_start) <= 500:
                        logging.info(
                            f"\t\tVrr_Previous_Vtotal register value not changing {len(vtotal_value_set)} "
                            f"due to short duration during "
                            f"{vrr_active_start} to {vrr_active_end}")
                    elif (vrr_active_end - vrr_active_start) > 500:
                        logging.error(
                            f"\t\t Vrr_Previous_Vtotal register value not changing for duration start:"
                            f"{vrr_active_start}, end:{vrr_active_end}")
                        gdhm.report_driver_bug_os(
                            title="[OsFeatures][VRR] Previous Vtotal value not changing as per FPS "
                        )
                        status = False
                else:
                    logging.info(
                        f"\t\tVrr_Previous_Vtotal register value changing {len(vtotal_value_set)} times during "
                        f"{vrr_active_start} to {vrr_active_end}")
    return status


##
# @brief        Helper function to perform VRR verification.
# @param[in]    adapter                     : Adapter
# @param[in]    panel                       : panel object of the targeted display
# @param[in]    etl_file                    : String, path to ETL file
# @param[in]    power_event                 : PowerEvent
# @param[in]    negative                    : Boolean
# @param[in]    os_aware_vrr                : Boolean
# @param[in]    expected_vrr                : Boolean, True if VRR is expected to be enabled, False otherwise.
# @param[in]    is_workload_already_running : Boolean, True if workload is already running, False otherwise.
# @param[in]    is_prev_vtotal_check_require: Boolean, True if previous VTotal check required, False otherwise.
# @param[in]    vmax_flipline_for_each_flip : Boolean, True if vmax_flipline for each flip require, False otherwise
# @return       status                      : Boolean, True if all VRR verification functions passed, False otherwise
def verify(adapter, panel, etl_file, power_event=None, negative=False, os_aware_vrr=True, expected_vrr=True,
           is_workload_already_running=False, is_prev_vtotal_check_require=False, vmax_flipline_for_each_flip=True):
    status = True
    dc_balancing_status = True
    dc_balance_event_expected = False
    intel_arc_sync_data = (None, None, None)
    panel_adapter_active_duration.clear()
    html.step_start(f"Verify VRR on {panel.port} ({adapter.name})")
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("\tFailed to generate EtlParser report(Test Issue)")
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

    # Get the current VRR configuration
    vrr_args = VrrArgs()
    vrr_args.operation = VrrOperation.GET_INFO.value
    vrr_flag, vrr_args = driver_escape.get_set_vrr(adapter.gfx_index, vrr_args)
    if not vrr_flag:
        logging.error(f"Escape call failed to get VRR for {adapter.gfx_index}")

    # Verify Sink programming (MSA Timing DPCD)
    # With VRR possible, MSA Timing --> 0x1
    # With VRR not possible, MSA Timing --> 0x0
    status &= __check_msa_timing_dpcd(panel)

    # Before verifying VRR registers, make sure driver is getting ASync flips from OS
    flip_status = __check_async_flip(panel, expected_vrr, vrr_args.vrrHighFpsSolnEnabled, os_aware_vrr, negative)
    status &= flip_status

    if panel.vrr_caps.is_dc_balancing_enabled is False:
        # Check VRR enable/disable events
        status &= __check_vrr_enable_disable(adapter, panel, expected_vrr)

    if negative:
        # Check VRR_CTL programming for negative test
        status &= __check_vrr_ctl_programming(adapter, panel, negative)

    if expected_vrr:
        # DC balance enable for Gen12+ except DG1
        if panel.vrr_caps.is_dc_balancing_enabled:
            # not in Always VRR mode ( Pre gen13 or LFP panel)
            v_min, v_max, v_active, drrs_v_max, bfr_v_max, intel_arc_sync_data = __get_expected_v_min_max(
                adapter,
                panel)
            status &= __check_vrr_enable_disable(adapter, panel, expected_vrr, intel_arc_sync_data[0],
                                                 intel_arc_sync_data[1], drrs_v_max,
                                                 bfr_v_max)
        # in case of DC balancing is false for Gen11, Gen11p5, gen12(Dg1)
        else:
            # Get expected v_min and v_max
            v_min, v_max, v_active, drrs_v_max, bfr_v_max, intel_arc_sync_data = __get_expected_v_min_max(adapter,
                                                                                                          panel)
        # update profile min and max as v_min and v_max as IGCL support from Gen13 onwards.
        if adapter.name in PRE_GEN_13_PLATFORMS:
            intel_arc_sync_data = (v_min, v_max, None)
        # Check VBI while VRR is enabled
        status &= __check_vbi(adapter, panel, power_event, panel.min_rr, negative)

        # check if LOW_FPS solution enable or not. DC balance not trigger in-case of LOW_FPS solution disable.
        if vrr_args.vrrLowFpsSolnEnabled and panel.vrr_caps.is_dc_balancing_enabled:
            dc_balance_event_expected = True

        # Check v_min_v_max programming
        register_programming_status = __check_vmin_vmax(adapter, panel, intel_arc_sync_data[0],
                                                        intel_arc_sync_data[1], drrs_v_max, dc_balance_event_expected,
                                                        vmax_flipline_for_each_flip)

        # Check if PSR is disabled during VRR active time frame
        register_programming_status &= __check_psr_status(adapter, panel)

        # check arc sync vmin , vmax and vtotal with SFDIT and SFDDT if low FPS solution enable.
        if vrr_args.vrrLowFpsSolnEnabled:
            # Check arc sync
            # JIRA: VSDI-31817 [IntelArcSync] Enable Intel Arc Sync profile verification tests
            register_programming_status &= __check_arc_sync_vmin_vmax(adapter, panel, intel_arc_sync_data[0],
                                                                      intel_arc_sync_data[1], intel_arc_sync_data[2])

        # Check flip line programming
        register_programming_status &= __check_flip_line(adapter, panel, intel_arc_sync_data[0], intel_arc_sync_data[1],
                                                         dc_balance_event_expected, vmax_flipline_for_each_flip)

        # Check VRR_CTL programming during VRR active period
        register_programming_status &= __check_vrr_ctl_programming(adapter, panel, negative)

        # Check VRR_STATUS programming during VRR active period
        register_programming_status &= __check_vrr_status_programming(adapter, panel)

        # Check TRANS_PUSH programming during VRR active period
        register_programming_status &= __check_trans_push_programming(adapter, panel)

        # Check SDP programming
        register_programming_status &= __check_sdp_programming(adapter, panel)

        # Check EMP AS SDP TL programming
        register_programming_status &= __check_emp_as_sdp_tl_programming(adapter, panel)

        if adapter.name not in common.GEN_16_PLATFORMS:
            # Check CMTG disable during VRR enable
            register_programming_status &= __check_cmtg_disable(adapter, panel)

        # check Prev_Vtotal programming during VRR active period
        register_programming_status &= __check_vrr_prev_vtotal(adapter, panel, intel_arc_sync_data[0],
                                                               intel_arc_sync_data[1], is_prev_vtotal_check_require)

        # check VTEM packet programming during Game workload launch and close
        register_programming_status &= __check_vtem_prgm_during_game_play(adapter, panel)

        if register_programming_status is False and negative is False:
            gdhm.report_driver_bug_os(
                title="[OsFeatures][VRR] Invalid VRR register programming found"
            )

        status &= register_programming_status

        # Check VRR Adaptive DC Balance
        dc_balancing_status = __check_vrr_adaptive_dc_balancing(adapter, panel, intel_arc_sync_data[0],
                                                                intel_arc_sync_data[1], dc_balance_event_expected,
                                                                is_workload_already_running)

        status &= dc_balancing_status

    html.step_end()
    return status


##
# @brief        Helper function to perform VRR verification.
# @param[in]    adapter                 : Adapter
# @param[in]    panel Panel             : panel object of the targeted display
# @param[in]    etl_file String         : path to ETL file
# @param[in]    negative                : Boolean
# @return       status                  : True if all VRR verification functions passed, False otherwise
def verify_modeset(adapter, panel, etl_file, negative=False):
    status = True

    html.step_start(f"Verify VRR on {panel.port} ({adapter.name}) during modeset")
    if etl_parser.generate_report(etl_file, ETL_PARSER_CONFIG) is False:
        logging.error("\tFailed to generate EtlParser report(Test Issue)")
        return False
    if not panel.vrr_caps.is_always_vrr_mode:
        logging.info("Always in VRR mode not enable returning early")
        return status

    # Get expected v_min and v_max
    v_min, v_max, v_active, drrs_v_max, bfr_v_max, intel_arc_sync_data = __get_expected_v_min_max(adapter, panel)

    # Check v_min_v_max programming
    register_programming_status = __check_vmin_vmax_modeset(adapter, panel, v_min, drrs_v_max)

    # Check flip line programming
    register_programming_status &= __check_flip_line_modeset(adapter, panel, v_min, v_max)

    # Check VRR_CTL programming during VRR active period
    register_programming_status &= __check_vrr_ctl_programming_modeset(adapter, panel, negative)

    # Check TRANS_PUSH programming during VRR active period
    register_programming_status &= __check_trans_push_programming_modeset(adapter, panel)

    # Check VRR GuardBand programming
    register_programming_status &= __check_vrr_guard_band_programming(adapter, panel, v_min, v_active)

    # Check VTEM programming for HDMI 2.1 Native
    register_programming_status &= __check_vtem_programming_during_modeset(adapter, panel)

    # Check EMP AS SDP TL programming
    register_programming_status &= __check_emp_as_sdp_tl_programming(adapter, panel, is_modeset=True)

    if adapter.name not in common.GEN_16_PLATFORMS:
        # Check CMTG disable during VRR enable
        register_programming_status &= __check_cmtg_post_modeset(adapter, panel)

    # Check if PSR is disabled during VRR active time frame
    register_programming_status &= __check_psr_status_post_mode_set(adapter, panel)

    if register_programming_status is False and negative is False:
        logging.error("\t[OsFeatures][VRR] Invalid VRR register programming found during modeset")
        gdhm.report_driver_bug_os(
            title="[OsFeatures][VRR] Invalid VRR register programming found during modeset")

    status &= register_programming_status
    html.step_end()
    return status


##
# @brief        Exposed API to verify Optical Sensor data for DC balance flickering
# @param[in]    sensor_data : list
# @return       status
@html.step("Verifying Optical Sensor Data")
def verify_optical_sensor_data(sensor_data):
    status = True
    try:
        import matplotlib.pyplot as plt
        f = plt.figure()
        plt.plot(list(range(len(sensor_data))), sensor_data)
        plt.ylabel('Normalized Voltage')
        plt.xlabel('Time in milliseconds')
        file_name = 'OpticalSensorDataPlot.' + str(time.time()) + '.pdf'
        f.savefig(os.path.join(test_context.LOG_FOLDER, file_name), bbox_inches='tight')
        logging.info(f"\tSaved optical sensor data in {file_name} file.")
    except Exception as e:
        logging.error(e)
    return status


##
# @brief        Exposed API to check if any given ETL file contains async flips or not
# @param[in]    etl_file String path to ETL file
# @return       True if flip data can be obtained from the etl file, False otherwise
def async_flips_present(etl_file):
    if etl_parser.generate_report(etl_file, FLIP_ONLY_PARSER_CONFIG) is False:
        logging.error("\tFailed to generate EtlParser report(Test Issue)")
        return False

    if etl_parser.get_flip_data(async_flip=True, vrr_flip=True) is not None:
        return True
    return False


##
# @brief        Exposed API to update VRR setting in VBT
# @param[in]    adapter Adapter
# @param[in]    port Port name for which the panel name has to be retrieved.
# @param[in]    enable_vrr boolean to indicate if vrr has to be enabled
# @return       True if VRR is enabled in VBT, False otherwise
def update_vbt(adapter: Adapter, port: str, enable_vrr: bool):
    expected_value = 1 if enable_vrr else 0
    # Make sure VRR is enabled in VBT
    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    if gfx_vbt.version >= 233:
        panel_index = gfx_vbt.get_lfp_panel_type(port)
        logging.debug(f"\tPanel Index for {port}= {panel_index}")
        vbt_vrr_status = (gfx_vbt.block_44.VRR[0] & (1 << panel_index)) >> panel_index
        if vbt_vrr_status != expected_value:
            if enable_vrr:
                gfx_vbt.block_44.VRR[0] |= (1 << panel_index)
            else:
                gfx_vbt.block_44.VRR[0] &= (0 << panel_index)

            if gfx_vbt.apply_changes() is False:
                logging.error("\tFailed to apply changes to VBT")
                return False
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                logging.error("\tFailed to restart display driver after VBT update")
                return False

            # Verify after restarting the driver
            gfx_vbt.reload()
            vbt_vrr_status = (gfx_vbt.block_44.VRR[0] & (1 << panel_index)) >> panel_index
            if vbt_vrr_status != expected_value:
                logging.error(f"\tFailed to {'enable' if enable_vrr else 'disable'} VRR in VBT")
                return False
            logging.info(f"\tPASS: {'Enabled' if enable_vrr else 'Disabled'} VRR in VBT successfully {port}")
        else:
            logging.info(f"\tPASS: VRR is {'enabled' if enable_vrr else 'disabled'} in VBT for {port}")

    return True


##
# @brief        Non-exposed function to Get the current Vmin and Vmax value
#               as per the min and Max RR from set Profile
# @param[in]    adapter
# @param[in]    panel
# @return       vmin, vmax
def __get_current_vmin_vmax(adapter, panel):
    current_profile = get_current_profile(panel)
    timing_info = adapter.regs.get_timing_info(panel.transcoder_type)
    h_total = timing_info.HTotal
    rr_reg_convert = lambda x: int(panel.native_mode.pixelClock_Hz / ((h_total + 1) * x)) - 1

    vmin = rr_reg_convert(current_profile.MaxRefreshRateInHz)
    vmax = rr_reg_convert(current_profile.MinRefreshRateInHz)
    return vmin, vmax


##
# @brief        Non-exposed function to verify arc sync related verification
#               on the ETL.
# @param[in]    adapter
# @param[in]    panel
# @param[in]    v_min  Profile v_min value
# @param[in]    v_max  profile v_max value
# @param[in]    scanline_time_in_us
# @return       status
def __check_arc_sync_vmin_vmax(adapter, panel, v_min, v_max, scanline_time_in_us):
    # not applicable for PRE_GEN_13_PLATFORMS
    if adapter.name in PRE_GEN_13_PLATFORMS:
        return True

    assert v_min, f"Invalid {v_min=} value passed"
    assert v_max, f"Invalid {v_max=} value passed"

    # do the control library Call and get min and max values
    # Get the current VRR configuration
    current_profile = get_current_profile(panel)
    status = True
    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    logging.info(f"Checking previous Vtotal")
    logging.info(
        f"\tExpected values: {current_profile.MinRefreshRateInHz=} {v_max=} {current_profile.MaxRefreshRateInHz=} "
        f"{v_min=}")
    vrr_active_region = get_vrr_active_period(adapter, panel)
    if vrr_active_region is None:
        logging.error("\t\tNo VRR active period found")
        return False
    for start, stop in vrr_active_region:
        event_data = etl_parser.get_event_data(etl_parser.Events.VRR_ADAPTIVE_BALANCE_APPLY, start_time=start,
                                               end_time=stop)

        logging.info(f"\tLooking in VRR Active Period {start} : {stop}")
        if event_data is None or len(event_data) < 3:
            logging.info(f"\t\tAdaptive balance was not kicked in for active period {start} : {stop}")
            continue

        start, stop = event_data[1].TimeStamp, event_data[-1].TimeStamp
        logging.debug(f"\t\tLooking for Vtotal in VRR Active Period wrt VRR ADAPTIVE BALANCE APPLY {start} : {stop}")
        register_data = etl_parser.get_mmio_data(vrr_regs.VrrVTotal, is_write=False, start_time=start, end_time=stop)
        if register_data is None:
            logging.error("\t\tVTotal register data was not found during vrr_active period")
            continue

        # Ignoring the first value
        vtotal_full = [((i.Data & 0xFFFFF), i.TimeStamp) for i in register_data[1:]]
        vtotal_values = [i for i, j in vtotal_full]

        if max(vtotal_values) > v_max:
            logging.error(f"\t\tFAIL: Max expected VTotal={v_max}, Actual={max(vtotal_values)}")
            for val, ts in vtotal_full:
                if val > v_max:
                    logging.error(f"\t\tUnexpected VTotal value ({val}) detected at {ts / 1000}s")
            status = False
        else:
            logging.info(f"\t\tPASS: Max expected VTotal={v_max}, Actual={max(vtotal_values)}")

        if min(vtotal_values) < v_min:
            logging.error(f"\t\tFAIL: Min expected VTotal={v_min}, Actual={min(vtotal_values)}")
            status = False
            for val, ts in vtotal_full:
                if val < v_min:
                    logging.error(f"\t\tUnexpected VTotal value ({val}) detected at {ts / 1000}s")
        else:
            logging.info(f"\t\tPASS: Min expected VTotal={v_min}, Actual={min(vtotal_values)}")
        delta_values = [vtotal_values[i + 1] - vtotal_values[i] for i in range(len(vtotal_values) - 1)]
        time_differences_in_us = [(scanline_time_in_us * i) for i in delta_values]
        # consider less VRR active time and no Vtotal read happen from driver.
        if time_differences_in_us is None:
            continue
        # SFDIT value can be 0 for some profiles (EXCELLENT). Skip the verification for such cases.
        if 0 != current_profile.MaxFrameTimeIncreaseInUs:
            # Difference between max frame time increase and maxFrameTimeIncrease from IGCL shouldn't be more than the
            # tolerance value (1 of scanline time)
            if max(time_differences_in_us, default=0) > (
                    current_profile.MaxFrameTimeIncreaseInUs + scanline_time_in_us):
                logging.warning(
                    f"\t\tFAIL: Max expected SFDIT value= "
                    f"{current_profile.MaxFrameTimeIncreaseInUs + scanline_time_in_us}, "
                    f"Actual= {max(time_differences_in_us, default=0)}")
                gdhm.report_driver_bug_os(title="[OsFeatures][VRR] SFDIT value exceed expected value")
            else:
                logging.info(
                    f"\t\tPASS: Max expected SFDIT value= {current_profile.MaxFrameTimeIncreaseInUs}, "
                    f"Actual= {max(time_differences_in_us, default=0)}")
        else:
            logging.info(f"\t\tSFDIT is 0. Verification is skipped.")

        # SFDDT value can be 0 for some profiles (EXCELLENT). Skip the verification for such cases.
        if 0 != current_profile.MaxFrameTimeDecreaseInUs:
            # Difference between max frame time decrease and maxFrameTimeDecrease from IGCL shouldn't be less than the
            # tolerance value (1 of scanline time)
            if abs(min(time_differences_in_us, default=0)) > (
                    current_profile.MaxFrameTimeDecreaseInUs + scanline_time_in_us):
                logging.warning(
                    f"\t\tFAIL: Max expected SFDDT value= "
                    f"{current_profile.MaxFrameTimeDecreaseInUs + scanline_time_in_us}, "
                    f"Actual= {abs(min(time_differences_in_us, default=0))}")
                gdhm.report_driver_bug_os(title="[OsFeatures][VRR] SFDDT value exceed expected value")
            else:
                logging.info(
                    f"\t\tPASS: Max expected SFDDT value= {current_profile.MaxFrameTimeDecreaseInUs}, "
                    f"Actual= {abs(min(time_differences_in_us, default=0))}")
        else:
            logging.info(f"\t\tSFDDT is 0. Verification is skipped.")

    return status


##
# @brief        get_fps_pattern, based on max RR and min RR
# @param[in]    refresh_rate - Panel refresh rate
# @param[in]    high_fps - True if high FPS false otherwise
# @return       fpspattern - FPS Pattern
def get_fps_pattern(refresh_rate, high_fps=True):
    fpspattern = []
    if high_fps:
        x = ((1 / refresh_rate) * pow(10, 3)) - ((1 / refresh_rate) * pow(10, 3)) / 2
        y = ((1 / refresh_rate) * pow(10, 3)) - ((1 / refresh_rate) * pow(10, 3)) / 3
        fpspattern = [round(x, 3), 1, round(y, 3), 1, 100]
    else:
        x = ((1 / refresh_rate) * pow(10, 3)) + ((1 / refresh_rate) * pow(10, 3)) / 2
        y = ((1 / refresh_rate) * pow(10, 3)) + ((1 / refresh_rate) * pow(10, 3)) / 3
        fpspattern = [round(x, 3), 1, round(y, 3), 1, 100]
    return fpspattern


##
# @brief        Exposed Function to if the expected profile has been applied as current
# @param[in]    panel
# @param[in]    expected_profile : expected profile
# @return       profile - profile of them monitor
def is_profile_applied(panel, expected_profile):
    profile_params = get_current_profile(panel)
    if not profile_params:
        logging.error("Fail: Get profile in Control Library")
    elif (profile_params.IntelArcSyncProfile.value == expected_profile.value or
          profile_params.IntelArcSyncProfile.value == ARC_SYNC_PROFILE.RECOMMENDED):
        return True
    else:
        logging.error("Fail: Current profile is not same as expected Profile")
    return False


##
# @brief        get current profile of the panel
# @param[in]    panel
# @param[in]    expected_fail True if expected fail else Default False
# @return       status
def get_current_profile(panel, expected_fail=False):
    profile_params = control_api_args.ctl_intel_arc_sync_profile_params_t()
    profile_params.Size = ctypes.sizeof(profile_params)
    profile_params.Version = 0
    if control_api_wrapper.get_current_intel_arc_sync_profile(profile_params, panel.display_info.DisplayAndAdapterInfo):
        logging.info(f"\tCurrent IntelArcSync profile: {profile_params.IntelArcSyncProfile}, "
                     f"max: {profile_params.MaxRefreshRateInHz}, MInRR: {profile_params.MinRefreshRateInHz}"
                     f"SFDIT: {profile_params.MaxFrameTimeIncreaseInUs}, "
                     f"SFDDT:{profile_params.MaxFrameTimeDecreaseInUs}")
        return profile_params
    if not expected_fail:
        logging.error("\t[OsFeatures][VRR] Failed to get IntelArcSync profile using IGCL")
        gdhm.report_driver_bug_os(
            title="[OsFeatures][VRR] Failed to get IntelArcSync profile using IGCL"
        )
    return False


##
# @brief        set specified arc sync profile on the panel
# @param[in]    panel : panel info
# @param[in]    profile : profile name
# @param[in]    minrr : profile name
# @param[in]    maxrr : profile name
# @param[in]    maxframeincreaseinus : Max Frame time increase
# @param[in]    maxframedecreaseinus : Max Frame time decrease
# @param[in]    expected_fail true if expected to fail profile set call
# @return       status
def set_profile(panel, profile=None, minrr=None, maxrr=None, maxframeincreaseinus=None, maxframedecreaseinus=None,
                expected_fail=False):
    status = True
    profile_params = control_api_args.ctl_intel_arc_sync_profile_params_t()
    profile_params.Size = ctypes.sizeof(profile_params)
    profile_params.Version = 0
    if minrr or maxrr or maxframeincreaseinus or maxframedecreaseinus:
        profile_params = get_current_profile(panel)
        profile_params.IntelArcSyncProfile = control_api_args.ctl_intel_arc_sync_profile_v.CUSTOM
        profile_params.MinRefreshRateInHz = minrr if minrr is not None else profile_params.MinRefreshRateInHz
        profile_params.MaxRefreshRateInHz = maxrr if maxrr is not None else profile_params.MaxRefreshRateInHz
        profile_params.MaxFrameTimeDecreaseInUs = maxframeincreaseinus if maxframeincreaseinus is not None else \
            profile_params.MaxFrameTimeDecreaseInUs
        profile_params.MaxFrameTimeIncreaseInUs = maxframedecreaseinus if maxframedecreaseinus is not None else \
            profile_params.MaxFrameTimeIncreaseInUs
    else:
        if profile is None:
            logging.error("Profile value not set : Either profile / Parameters have to be set")
            return False
        profile_params.IntelArcSyncProfile = profile
    html.step_start(f"Setting Profile {profile.name}")
    if control_api_wrapper.set_intel_arc_sync_profile(profile_params, panel.display_info.DisplayAndAdapterInfo):
        logging.info(f"Profile set successfully to {profile.name}")
    else:
        status = False
        if not expected_fail:
            logging.error("Fail: Set profile in Control Library")
            gdhm.report_driver_bug_os("[OsFeatures][VRR] Fail: Set profile in Control Library")
    html.step_end()
    return status


##
# @brief        get arc sync support for panel
# @param[in]    panel : panel info
# @return       panel parameters
def get_arc_sync_config(panel):
    arc_sync_params = control_api_args.ctl_intel_arc_sync_monitor_params_t()
    arc_sync_params.Size = ctypes.sizeof(arc_sync_params)
    arc_sync_params.Version = 0
    if control_api_wrapper.get_intel_arc_sync_info(arc_sync_params,
                                                   panel.display_info.DisplayAndAdapterInfo):
        return arc_sync_params
    logging.error("Fail: Get Arc sync config in Control Library")
    gdhm.report_driver_bug_os("[OsFeatures][VRR] Fail to Get Arc sync config in Control Library")
    return False


##
# @brief        Helper API to verify PSR status during VRR active period
# @param[in]    adapter, Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_psr_status(adapter, panel):
    status = True
    logging.info("\tVerifying PSR status")
    if not panel.psr_caps.is_psr_supported:
        logging.info(f"PSR is not supported by the panel")
        return status
    vrr_active_period = get_vrr_active_period(adapter, panel)
    if vrr_active_period is None:
        logging.error("\t\tNo VRR active period found")
        return False

    for vrr_active_start, vrr_active_end in vrr_active_period:
        psr_regs = adapter.regs.get_psr_offsets(panel.transcoder_type)

        # Check if PSR1 is disabled for PSR1 supported panel
        if panel.psr_caps.psr_version == 1:
            # get the mmio offsets for PSR1 SRD CTL register
            psr_mmio_ctl_output = etl_parser.get_mmio_data(psr_regs.SrdCtlReg, start_time=vrr_active_start,
                                                           end_time=vrr_active_end)
            if psr_mmio_ctl_output is None:
                logging.info(f"No MMIO output found for SRD_CTL_{panel.transcoder}")
            else:
                for mmio_data in psr_mmio_ctl_output:
                    psr_info = adapter.regs.get_psr_info(panel.transcoder_type,
                                                         PsrOffsetValues(SrdCtlReg=mmio_data.Data))
                    if psr_info.SrdEnable:
                        logging.error(f"SRD_CTL_{panel.transcoder}= {mmio_data.Data} at {mmio_data.TimeStamp}"
                                      f" 31st bit Expected= Disabled, Actual= Enabled")
                        gdhm.report_driver_bug_os(f"[OsFeatures][VRR] PSR1 status:Expected= Disabled, Actual= Enabled")
                        status = False

        # Check if PSR2 is disabled if panel is PSR2 supported panel
        if panel.psr_caps.psr_version == 2:
            # get the mmio offsets for PSR2 CTL register
            psr2_mmio_ctl_output = etl_parser.get_mmio_data(psr_regs.Psr2CtrlReg, start_time=vrr_active_start,
                                                            end_time=vrr_active_end)
            if psr2_mmio_ctl_output is None:
                logging.info(f"No MMIO output found for PSR2_CTL_{panel.transcoder}")
            else:
                for mmio_data in psr2_mmio_ctl_output:
                    psr2_info = adapter.regs.get_psr_info(panel.transcoder_type,
                                                          PsrOffsetValues(Psr2CtrlReg=mmio_data.Data))
                    if psr2_info.Psr2Enable:
                        logging.error(f"PSR2 CTL {panel.transcoder}= {mmio_data} at {mmio_data.TimeStamp}"
                                      f" 31st bit Expected= Disabled, Actual= Enabled")
                        gdhm.report_driver_bug_os(f"[OsFeatures][VRR] PSR2 status:Expected= Disabled, Actual= Enabled")
                        status = False
    return status


##
# @brief        Helper API to verify PSR status post modeset
# @param[in]    adapter, Adapter
# @param[in]    panel Panel, panel object of the targeted display
# @return       status, Boolean, True if verification is successful, False otherwise
def __check_psr_status_post_mode_set(adapter, panel):
    status = True
    logging.info("\tVerifying PSR status")
    if adapter.name in PRE_GEN_14_PLATFORMS:
        logging.info(f"\t\tPSR not enable during modeset for {adapter.name} platform, skipping verification")
        return status
    if not panel.psr_caps.is_psr_supported:
        logging.info(f"\t\tPSR is not supported by the panel")
        return status
    if panel.psr_caps.psr_version == 1:
        feature_supported = psr.verify_psr_restrictions(adapter, panel, psr.UserRequestedFeature.PSR_1)
    else:
        feature_supported = psr.verify_psr_restrictions(adapter, panel, psr.UserRequestedFeature.PSR_2)

    if feature_supported == psr.UserRequestedFeature.PSR_NONE:
        logging.info(f"\t\tPSR is not supported by the panel due to timing restriction, Skipping PSR verification")
        return status
    psr_regs = adapter.regs.get_psr_offsets(panel.transcoder_type)

    # Check if PSR1 is enabled for PSR1 supported panel
    if feature_supported == psr.UserRequestedFeature.PSR_1:
        # get the mmio offsets for PSR1 SRD CTL register
        psr_mmio_ctl_output = etl_parser.get_mmio_data(psr_regs.SrdCtlReg)
        if psr_mmio_ctl_output is None:
            logging.error(f"No MMIO output found for SRD_CTL_{panel.transcoder}")
            status = False
        else:
            psr_info = adapter.regs.get_psr_info(panel.transcoder_type,
                                                 PsrOffsetValues(SrdCtlReg=psr_mmio_ctl_output[-1].Data))
            if psr_info.SrdEnable is False:
                logging.error(f"SRD_CTL_{panel.transcoder}= {psr_mmio_ctl_output[-1].Data} at "
                              f"{psr_mmio_ctl_output[-1].TimeStamp} 31st bit Expected= Enabled, Actual= Disabled")
                gdhm.report_driver_bug_os(f"[OsFeatures][VRR] PSR1 status:Expected= Enabled, Actual= Disabled")
                status = False
            else:
                logging.info("PSR1 enable post mode set, Expected= Enable, Actual= Enabled")

    # Check if PSR2 is disabled if panel is PSR2 supported panel
    if feature_supported == psr.UserRequestedFeature.PSR_2:
        # get the mmio offsets for PSR2 CTL register
        offset = psr_regs.Psr2CtrlReg
        if adapter.name not in common.PRE_GEN_14_PLATFORMS:
            offset = 0x60902  # 16-bit address
            if panel.transcoder == 'B':
                offset = 0x61902
        psr2_mmio_ctl_output = etl_parser.get_mmio_data(offset)
        if psr2_mmio_ctl_output is None:
            logging.error(f"No MMIO output found for PSR2_CTL_{panel.transcoder}")
        else:
            data = psr2_mmio_ctl_output[-1].Data
            if adapter.name not in common.PRE_GEN_14_PLATFORMS:
                data = data << 16
            psr2_info = adapter.regs.get_psr_info(panel.transcoder_type, PsrOffsetValues(Psr2CtrlReg=data))
            if psr2_info.Psr2Enable is False:
                logging.error(f"PSR2 CTL {panel.transcoder}= {data} at {psr2_mmio_ctl_output[-1].TimeStamp} 31st bit "
                              f"Expected= Enabled, Actual= Disabled")
                gdhm.report_driver_bug_os(f"[OsFeatures][VRR] PSR2 status:Expected= Enabled, Actual= Disabled")
                status = False
            else:
                logging.info("PSR2 enable post mode set, Expected= Enable, Actual= Enabled")
    return status


##
# @brief        This method enables/disables Adaptive Sync Plus in IGCC
# @param[in]    gfx_index: Graphics Adapter Index
# @param[in]    enable: bool
# @return       vrr_flag: bool. True is operation is successful, otherwise False
def enable_disable_adaptive_sync_plus(gfx_index, enable=True):
    vrr_args = VrrArgs()
    vrr_args.operation = VrrOperation.GET_INFO.value
    vrr_flag, vrr_args = driver_escape.get_set_vrr(gfx_index, vrr_args)
    if not vrr_flag:
        logging.error(f"Escape call failed to get VRR for {gfx_index}")
        return vrr_flag
    if enable:
        vrr_args.operation = VrrOperation.LOW_FPS_ENABLE.value
    else:
        vrr_args.operation = VrrOperation.LOW_FPS_DISABLE.value

    vrr_flag, vrr_args = driver_escape.get_set_vrr(gfx_index, vrr_args)
    if not vrr_flag:
        logging.error(f"Escape call failed to set VRR for {gfx_index}")
        return vrr_flag

    return vrr_flag
