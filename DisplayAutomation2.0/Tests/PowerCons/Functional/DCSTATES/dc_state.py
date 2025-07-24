########################################################################################################################
# @file         dc_state.py
# @brief        Contains APIs to verify DC STATES - DC6, DC6v & DC9
#
# @author       Vinod D S
########################################################################################################################

import logging
import math
import os
import time

from DisplayRegs.DisplayOffsets import DCStateOffsetsValues
from Libs.Core import etl_parser, window_helper, app_controls
from Libs.Core import winkb_helper as kb
from Libs.Core.display_power import DisplayPower, PowerEvent
from Libs.Core.logger import gdhm, etl_tracer
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env import test_context
from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.CMTG import cmtg
from Tests.PowerCons.Functional.PSR import psr_util, psr, pr
from Tests.PowerCons.Modules import common, polling, workload
from Tests.PowerCons.Modules.dut_context import Adapter
from registers.mmioregister import MMIORegister


__PRE_SI_FRAME_COUNTER_UPDATE_TIMEOUT = 100  # 30 times
__PRE_SI_POLLING_DELAY = 30  # 30 seconds
__PRE_SI_FRAME_UPDATE_MAX = 8  # Wait for 8 frames before closing the psr util app
DC6V_UPPER_GB_OFFSET = 0x456A4
DC6V_EARLY_GB_OFFSET = 0x455B0

DMC_COUNTERS = {
    'TGL': {
        'DC5': 0x8012C,
        'DC6': 0x80130
    },
    'DG1': {
        'DC5': 0x8012C
    },
    'DG2': {
        'DC5': 0x8F054,
        'DC6': 0x8F054
    },
    'ADLS': {
        'DC5': 0x8012C,
        'DC6': 0x80130
    },
    'ADLP': {
        'DC5': 0x8F054,
        'DC6': 0x8F058,
        'DC6V': 0x101098
    },
    'MTL': {
        'DC5': 0x134154,
        'DC6': 0x8F058,
        'DC6V': 0x101098
    },
    'LNL': {
        'DC5': 0x134154,
        'DC6': 0x8F058,
        'DC6V': 0x101098
    },
    'PTL': {
        'DC5': 0x134154,
        'DC6': 0x8F058,
        'DC6V': 0x101098
    }
}

DC_STATE_MAP = {
    'DC0': 'DC_PWR_STATE_SET_NONE',
    'DC6': 'DC_PWR_STATE_SET_UPTO_DC6',
    'DC5': 'DC_PWR_STATE_SET_UPTO_DC5',
    'DC6V': 'DC_PWR_STATE_SET_UPTO_DC6V',
    'DC9': 'DC_PWR_STATE_SET_UPTO_DC9',
}

driver_interface_ = driver_interface.DriverInterface()


##
# @brief        This is a helper function to enable dc6v
# @param[in]    adapter - adapter object
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
def enable_dc6v(adapter):
    display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
    status = None
    if display_pc.DisableDC6v == 0:
        logging.info("\tDC6v is already enabled via DisplayPcFeatureControl registry")
        return status
    display_pc.DisableDC6v = 0
    status = display_pc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to enable DC6v via DisplayPcFeatureControl registry")
    else:
        logging.info("\tSuccessfully enabled DC6v via DisplayPcFeatureControl registry")
    return status


##
# @brief        This is a helper function to disable dc6v
# @param[in]    adapter - adapter object
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
def disable_dc6v(adapter):
    display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
    status = None
    if display_pc.DisableDC6v == 1:
        logging.info("\tDC6v is already disabled via DisplayPcFeatureControl registry")
        return status
    display_pc.DisableDC6v = 1
    status = display_pc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to disable DC6v via DisplayPcFeatureControl registry")
    else:
        logging.info("\tSuccessfully disabled DC6v via DisplayPcFeatureControl registry")
    return status


##
# @brief        This is a helper function to enable dc6
# @param[in]    adapter - adapter object
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
def enable_dc6(adapter):
    display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
    status = None
    if display_pc.DisableDC6 == 0:
        logging.info("\tDC6 is already enabled via DisplayPcFeatureControl registry")
        return status
    display_pc.DisableDC6 = 0
    status = display_pc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to enable DC6 via DisplayPcFeatureControl registry")
    else:
        logging.info("\tSuccessfully enabled DC6 via DisplayPcFeatureControl registry")
    return status


##
# @brief        This is a helper function to disable dc6
# @param[in]    adapter - adapter object
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
def disable_dc6(adapter):
    display_pc = registry.DisplayPcFeatureControl(adapter.gfx_index)
    status = None
    if display_pc.DisableDC6 == 1:
        logging.info("\tDC6 is already disabled via DisplayPcFeatureControl registry")
        return status
    display_pc.DisableDC6 = 1
    status = display_pc.update(adapter.gfx_index)
    if status is False:
        logging.error("\tFAILED to disable DC6 via DisplayPcFeatureControl registry")
    else:
        logging.info("\tSuccessfully disabled DC6 via DisplayPcFeatureControl registry")
    return status


##
# @brief        Verify DC5/DC6 functionality as below
#               1. Polling
#               2. Entry/exit with ETL parsing.
#               3. DMC Counter verification
# @param[in]    adapter Adapter Object
# @param[in]    method APP - to get PSR entry exit
#               Video - to get DC6v entry exit in 24fps video.
#               IDLE - to get DC5/DC6 state in IDLE scenario.
# @return       True if supported else False
def verify_dc5_dc6(adapter, method):
    if method == 'APP':
        dc_state, status = verify_sw_dc5_dc6_state(adapter, method)
    else:
        dc_state, status = verify_sw_dc_state_polling(adapter, 'DC6', method)
    if status is False:
        gdhm.report_driver_bug_pc("[PowerCons][DC6] SW DC5/6 verification failed")
        logging.error("\tSW DC5/DC6 verification is failed")
        return False
    logging.info("\tSW {0} verification is successful".format(dc_state))
    return True


##
# @brief        Verify DC5/DC6 with ETL parsing
# @param[in]    adapter Adapter Object
# @param[in]    method APP - to get PSR entry exit
#               Video - to get DC6v entry exit in 24fps video.
#               IDLE - to get DC5/DC6 state in IDLE scenario.
# @param[in]    duration [optional]  duration of workload in ms
# @return       SW dc state, True if supported else False
def verify_sw_dc5_dc6_state(adapter, method, duration=30):
    psr2_enabled = False
    initial_dc6_counter, final_dc6_counter = 0, 0
    for panel in adapter.panels.values():
        if panel.psr_caps.is_psr2_supported is True:
            if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is False:
                for i in range(5):
                    if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is True:
                        psr2_enabled = True
                        break
                if not psr2_enabled:
                    logging.warning("PSR2 not enabled in driver")
        elif panel.psr_caps.is_psr_supported is True:
            if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1) is False:
                logging.warning("PSR1 not enabled in driver")
    # DC6 & DC6V counters are not valid from MTL+ onwards
    initial_dc5_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name]['DC5'], adapter.gfx_index)
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        initial_dc6_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name]['DC6'], adapter.gfx_index)
    etl_file = get_etl_trace(method, duration)
    final_dc5_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name]['DC5'], adapter.gfx_index)
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        final_dc6_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name]['DC6'], adapter.gfx_index)

    sw_dc6_status = verify_dc6_vbi(etl_file)
    sw_dc6v_status = True
    # @TODO: Remove after enabling DC6V in driver.
    # if adapter.name == 'ADLP':
    #     sw_dc6v_status = verify_dc6v_vbi(adapter,etl_file)
    
    if sw_dc6_status is True and sw_dc6v_status is True:
        logging.info(f"\tPass: DC state SW verification successful")
        if adapter.name in common.PRE_GEN_13_PLATFORMS + ['ADLP']:
            if initial_dc6_counter != final_dc6_counter:
                logging.info("\tDC6 DMC counter verification is successful")
                return 'DC6', True
            logging.error("\tDC6 DMC counter verification failed")
            return 'DC0', False
        else:
            # For DG2, only DC5 is the max low power state
            # From GEN14+ only DC5 counter will be toggled
            if initial_dc5_counter != final_dc5_counter:
                logging.info("\tDC5 DMC counter verification is successful")
                return 'DC5', True
            logging.error("\tDC5 DMC counter verification failed")
            return 'DC0', False
    return 'DC0', False


##
# @brief        Get ETL trace with scenario
#
# @param[in]    method - APP to get PSR entry exit
#               Video to get DC6v entry exit in 24fps video.
#               IDLE to get DC5/DC6 state in IDLE scenario.
# @param[in]    duration for workload in ms
# @return       ETL file
def get_etl_trace(method, duration=30):
    if method == 'IDLE':
        etl_file, _ = workload.run(workload.IDLE_DESKTOP, [duration])
        return etl_file
    elif method == 'VIDEO':
        etl_file, _ = workload.run(workload.VIDEO_PLAYBACK, [24, duration])
        return etl_file
    elif method == 'APP':
        monitors = app_controls.get_enumerated_display_monitors()
        monitor_ids = [_[0] for _ in monitors]
        etl_file, _ = workload.run(workload.SCREEN_UPDATE, [monitor_ids])
        return etl_file


##
# @brief        Verify DC State with polling
# @param[in]    adapter - Adapter object
# @param[in]    state - DC5, DC6, DC6v
# @param[in]    method - APP to get PSR entry exit
#               Video  to get DC6v entry exit in 24fps video.
#               IDLE  to get DC5/DC6 state in IDLE scenario.
# @param[in]    fps - video duration in fps
# @return       SW dc state, True if supported else False
def verify_sw_dc_state_polling(adapter, state, method=None, fps=24.000):
    monitor_ids = []
    pr_alpm_registers = []
    dc5_state_counter = 0
    dc6_state_counter = 0
    dc6v_state_counter = 0
    counter = 0
    initial_dc6_counter, final_dc6_counter = 0, 0
    alpm_check = False
    panels = adapter.panels.values()
    for panel in panels:
        if panel.is_lfp is False:
            continue
        monitor_ids.append(panel.monitor_id)
        if panel.pr_caps.is_pr_supported:
            if pr.is_enabled_in_driver(adapter, panel) is False:
                logging.warning(f"PR not enabled in driver")
        elif panel.psr_caps.is_psr2_supported is True:
            if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is False:
                logging.warning("PSR2 not enabled in driver")
        elif panel.psr_caps.is_psr_supported is True:
            if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1) is False:
                logging.warning("PSR1 not enabled in driver")
        if adapter.name not in common.PRE_GEN_15_PLATFORMS and panel.pr_caps.is_pr_supported:
            pr_alpm_registers.append(MMIORegister.get_instance(
                'PR_ALPM_CTL_REGISTER', 'PR_ALPM_CTL_' + panel.transcoder, adapter.name).offset)
    dc_state_en = MMIORegister.get_instance("DC_STATE_EN_REGISTER", "DC_STATE_EN", adapter.name)

    initial_dc5_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name]['DC5'], adapter.gfx_index)
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        initial_dc6_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name]['DC6'], adapter.gfx_index)
    offsets = [dc_state_en.offset]
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        offsets = offsets + pr_alpm_registers
    polling.start(offsets, 0.01)
    if method == 'IDLE':
        time.sleep(30)
    elif method == 'VIDEO':
        kb.press('WIN+M')
        app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, "{0:.3f}.mp4".format(fps)))
        logging.info("\tLaunching video playback of {0:.3f}.mp4 is successful".format(fps))
        time.sleep(30)

    # Stop the polling and get the timeline
    polling_timeline, time_stamps = polling.stop()
    if method == 'VIDEO':
        window_helper.close_media_player()

    final_dc5_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name]['DC5'], adapter.gfx_index)
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        final_dc6_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name]['DC6'], adapter.gfx_index)

    dc_state = MMIORegister.get_instance("DC_STATE_EN_REGISTER", "DC_STATE_EN", adapter.name)
    for time_stamp in time_stamps:
        if time_stamp in time_stamps:
            mmio_value = polling_timeline[dc_state_en.offset][time_stamps.index(time_stamp)]
            if mmio_value is None:
                continue
            dc_state.asUint = mmio_value
            if state in ['DC6V']:
                if dc_state.dc_state_enable == 3:
                    dc6v_state_counter += 1
            else:
                if dc_state.dc_state_enable == 1:
                    dc5_state_counter += 1
                elif dc_state.dc_state_enable == 2:
                    dc6_state_counter += 1
            logging.debug("\tDC state value={0} (TimeStamp={1})".format(dc_state.asUint, time_stamp))
            if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                pr_alpm_ctl_a = MMIORegister.get_instance('PR_ALPM_CTL_REGISTER', 'PR_ALPM_CTL_A', adapter.name)
                pr_alpm_ctl_b = MMIORegister.get_instance('PR_ALPM_CTL_REGISTER', 'PR_ALPM_CTL_B', adapter.name)
                for offset in pr_alpm_registers:
                    alpm_val = polling_timeline[offset][time_stamps.index(time_stamp)]
                    if alpm_val is None:
                        continue
                    if pr_alpm_ctl_a.offset == offset:
                        pr_alpm_ctl_a.asUint = alpm_val
                        if pr_alpm_ctl_a.as_sdp_transmission_disabled_in_active == 0x1:
                            logging.info(f"Driver disabled AS SDP during VBI disable")
                            alpm_check = True
                    else:
                        pr_alpm_ctl_b.asUint = alpm_val
                        if pr_alpm_ctl_b.as_sdp_transmission_disabled_in_active == 0x1:
                            logging.info(f"Driver disabled AS SDP during VBI disable")
                            alpm_check = True

    if state == 'DC6V':
        counter = dc6v_state_counter
        state = 'DC6V'
    elif state in ['DC5', 'DC6']:
        if dc6_state_counter != 0:
            counter = dc6_state_counter
            state = 'DC6'
        if dc5_state_counter != 0:
            counter = dc5_state_counter
            state = 'DC5'
    else:
        return None, False

    if adapter.name not in common.PRE_GEN_15_PLATFORMS and alpm_check is False and pr_alpm_registers:
        logging.error("driver did not disable AS SDP during VBI disable")
        return state, False
    if counter > 0:
        logging.info(f"\tPass: DC state SW verification successful={state} counter={counter}")
        if adapter.name in common.PRE_GEN_13_PLATFORMS + ['ADLP']:
            if initial_dc6_counter != final_dc6_counter:
                logging.info("\tDC6 DMC counter verification is successful")
                return 'DC6', True
            logging.error("\tDC6 DMC counter verification failed")
            return 'DC0', False
        else:
            # For DG2, only DC5 is the max low power state
            # From GEN14+ only DC5 counter will be toggled
            if initial_dc5_counter != final_dc5_counter:
                logging.info("\tDC5 DMC counter verification is successful")
                return 'DC5', True
            logging.error("\tDC5 DMC counter verification failed")
            return 'DC0', False
    else:
        gdhm.report_driver_bug_pc(f"[PowerCons][{state}] {state} state verification failed")
        logging.error(f"\tFAIL: DC state verification failed={state} counter={counter}")
        return state, False


##
# @brief        Verify DC State in Hw
# @param[in]    dc_state string indicating DC States
# @param[in]    adapter Adpater object
# @param[in]    method - APP to get PSR entry exit
#               Video  to get DC6v entry exit in 24fps video.
#               IDLE  to get DC6v state in IDLE scenario.
# @param[in]    fps - video duration in fps
# @return       True if success else False
def verify_hw_dc_state(dc_state, adapter, method, fps=24.000):
    monitor_ids = []
    panels = adapter.panels.values()

    for panel in panels:
        if panel.psr_caps.is_psr2_supported is True:
            if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is False:
                logging.warning("PSR2 not enabled in driver")
        elif panel.psr_caps.is_psr_supported is True:
            if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1) is False:
                logging.warning("PSR1 not enabled in driver")
    if adapter.name not in common.PRE_GEN_14_PLATFORMS and dc_state in ['DC6V', 'DC6']:
        dc_state = 'DC5'
    initial_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name][dc_state], adapter.gfx_index)

    time.sleep(4)
    # minimizing to desktop
    if window_helper.minimize_all_windows():
        logging.info("\tSuccessfully minimized to Desktop")
    else:
        logging.error("\tFAILED to Minimize Desktop")
    if method == 'APP':
        for panel in panels:
            monitor_ids.append(panel.monitor_id)
        psr_util.run(monitor_ids)
    elif method == 'IDLE':
        time.sleep(30)
    elif method == 'VIDEO':
        kb.press('WIN+M')
        app_controls.launch_video(os.path.join(common.TEST_VIDEOS_PATH, "{0:.3f}.mp4".format(fps)))
        logging.info("\tLaunching video playback of {0:.3f}.mp4 is successful".format(fps))
        time.sleep(30)
    final_counter = driver_interface_.mmio_read(DMC_COUNTERS[adapter.name][dc_state], adapter.gfx_index)
    if method == 'VIDEO':
        window_helper.close_media_player()
    if initial_counter != final_counter:
        logging.info(
            "\t{0}: Initial counter={1} Final counter={2}".format(dc_state, initial_counter, final_counter))
        return True
    gdhm.report_driver_bug_pc(f"[PowerCons][{dc_state}] HW {dc_state} counter verification failed")
    logging.info(f"\t{dc_state}: Initial counter={initial_counter} Final counter={final_counter}")
    return False


##
# @brief        Verify DC6v functionality as below
#               1. Polling
#               2. Entry/exit with ETL parsing.
#               3. DMC Counter verification
# @param[in]    adapter - adapter object
# @param[in]    method APP to get DC6v entry exit
#               Video to get DC6V entry exit in 24fps video.
# @param[in]    fps - video duration in fps
# @return       True if supported else False
def verify_dc6v(adapter, method, fps=24.000):
    status = False

    if method == "VIDEO":
        etl_file, _ = workload.run(workload.VIDEO_PLAYBACK, [fps, 60])
        if verify_dc6v_vbi(adapter, method, etl_file):
            status = True
    else:
        status = verify_sw_dc6v_state(adapter, method)

    if status is True:
        logging.info("\tSW DC6v verification is successful")
        if verify_hw_dc_state('DC6V', adapter, method, fps):
            logging.info("\tHW DC6v verification is successful")
            return True
        gdhm.report_driver_bug_pc("[PowerCons][DC6v] HW DC6v verification failed")
        logging.error("\tHW DC6v verification is failed")
        return False
    logging.error("\tSW DC6v verification is failed")
    return False


##
# @brief        Verify DC6v with ETL parsing
#
# @param[in]    adapter - adapter object
# @param[in]    method - APP to get PSR entry exit
#               Video - to get DC6v entry exit in 24fps video.
#               IDLE - to get DC6v state in IDLE scenario.
# @return       True if supported else False
def verify_sw_dc6v_state(adapter, method):
    duration = 30
    psr2_pr_enabled = False
    for panel in adapter.panels.values():
        if panel.psr_caps.is_psr2_supported is True:
            if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is False:
                for i in range(5):
                    if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is True:
                        psr2_pr_enabled = True
                        break
                if not psr2_pr_enabled:
                    logging.error("PSR2 not enabled in driver")
                    return False
        elif panel.pr_caps.is_pr_supported:
            for i in range(5):
                if pr.is_enabled_in_driver(adapter, panel):
                    psr2_pr_enabled = True
                    break
            if not psr2_pr_enabled:
                logging.error("PR not enabled in driver")
                return False

    if verify_cmtg_programming(adapter) is False:
        return False
    etl_file = get_etl_trace(method, duration)
    return verify_dc6v_vbi(adapter, method, etl_file)


##
# @brief        This is a helper function to check CMTG status before verifying DC6v
# @param[in]    adapter - adapter object
# @return       True if success else False
def verify_cmtg_programming(adapter):
    if cmtg.verify_cmtg_status(adapter) is False:
        gdhm.report_driver_bug_pc("[PowerCons][DC6v] DC6v verification failed CMTG status Expected=True Actual=False")
        logging.error("\tDC6v verification failed CMTG status Expected=True Actual=False")
        return False

    status, slaved_panel = cmtg.verify_cmtg_slave_status(adapter, adapter.panels.values())
    if status is False:
        logging.error("DC6v verification failed {0} is not slave to CMTG".format(adapter.panels.values))
        return False

    return True


##
# @brief        This function verifies dc6v programming
# @param[in]    method  - APP/VIDEO
# @param[in]    adapter - adapter object
# @return       True if success else False
def verify_dc6v_programming(method: str, adapter: Adapter):
    logging.debug(f"Verifying DC6v programming in method {method}")
    panels = adapter.panels.values()
    status, slaved_panel = cmtg.verify_cmtg_slave_status(adapter, panels)
    if status is False:
        logging.error("Panel is not slaved to CMTG. Aborting DC6v verification")
        return False
    if slaved_panel.vrr_caps.is_always_vrr_mode:
        return verify_dc6v_guardband_programming_on_vrr_panel(adapter, slaved_panel)

    # verify Legacy dc6v programming in VRR disable case
    # expected_scan_line_val, expected_upper_gb = 0, 0
    driver_interface_inst = driver_interface.DriverInterface()
    actual_upper_gb = driver_interface_inst.mmio_read(DC6V_UPPER_GB_OFFSET, adapter.gfx_index)
    if adapter.name in common.PRE_GEN_15_PLATFORMS:
        htotal = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_CMTG", adapter.name)
        vblank = MMIORegister.read("TRANS_VBLANK_REGISTER", "TRANS_VBLANK_CMTG", adapter.name)
    else:
        # use CMTG0 for LNL+, CMTG1 check is not needed because DC6v cannot be enabled in Dual LFP without PortSync
        htotal = MMIORegister.read("TRANS_HTOTAL_REGISTER", "TRANS_HTOTAL_CMTG0", adapter.name)
        vblank = MMIORegister.read("TRANS_VBLANK_REGISTER", "TRANS_VBLANK_CMTG0", adapter.name)
    dmc_scanline_cmp_lower_reg = MMIORegister.read(
        "PIPE_DMC_SCANLINE_CMP_LOWER_REGISTER", "PIPE_DMC_SCANLINE_CMP_LOWER_" + slaved_panel.transcoder, adapter.name)
    dmc_scanline_cmp_upper_reg = MMIORegister.read(
        "PIPE_DMC_SCANLINE_CMP_UPPER_REGISTER", "PIPE_DMC_SCANLINE_CMP_UPPER_" + slaved_panel.transcoder, adapter.name)

    # line time in micro secs = H total / Pixel clock in MHZ
    line_time_micro_sec = math.floor(
        (8 * (htotal.horizontal_total + 1)) / float(slaved_panel.native_mode.pixelClock_Hz / (1000 * 1000)))
    line_time_us = math.ceil(
        (8 * (htotal.horizontal_total + 1)) / float(slaved_panel.native_mode.pixelClock_Hz / (1000 * 1000)))
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        # From LNL+, All GB's calculation will be done with FlipQ GB
        logging.info(
            f"DMC scanline upper = {dmc_scanline_cmp_upper_reg.scanline_upper} "
            f"Lower = {dmc_scanline_cmp_lower_reg.scanline_lower}")
        line_time = line_time_us / 8
        expected_upper_gb = dmc_scanline_cmp_lower_reg.scanline_lower - math.ceil(600 / line_time)
        expected_lower_gb = expected_upper_gb - 8
        expected_dc6v_restore_time = math.ceil(
            (dmc_scanline_cmp_upper_reg.scanline_upper - expected_lower_gb) * line_time) + 50
        expected_early_entry_gb = expected_lower_gb - math.ceil(600 / line_time)  # DC5_TO_DC3_EXIT_LATENCY = 600 us
    else:
        line_time = int(line_time_us / 8)
        expected_upper_gb = math.ceil(vblank.vertical_blank_start + 1) - math.ceil(1000 / line_time)
        expected_lower_gb = expected_upper_gb - 8
        expected_early_entry_gb = expected_lower_gb
        expected_dc6v_restore_time = ((vblank.vertical_blank_start + 1) - expected_lower_gb) * line_time + 50
    logging.info(f"line time/8 = {line_time}, line_time_us = {line_time_us}, line time floored ={line_time_micro_sec}")
    expected_line_time_dc6v = line_time_micro_sec
    # compare all
    dc6v_reg_data = adapter.regs.get_dc6v_info()

    logging.info(f"LowerGB Expected:{expected_lower_gb} Actual:{dc6v_reg_data.LowerGuardBand}")
    logging.info(f"UpperGB Expected:{expected_upper_gb} Actual:{actual_upper_gb}")
    logging.info(f"Dc6v_line_time Expected:{expected_line_time_dc6v} Actual:{dc6v_reg_data.LineTimeDc6v}")
    logging.info(f"Dc6vRestoreTime Expected:{expected_dc6v_restore_time} Actual:{dc6v_reg_data.RestoreProgrammingTime}")
    if expected_lower_gb not in [dc6v_reg_data.LowerGuardBand - 1, dc6v_reg_data.LowerGuardBand,
                                 dc6v_reg_data.LowerGuardBand + 1]:
        logging.error(f"LowerGB Expected:{expected_lower_gb} Actual:{dc6v_reg_data.LowerGuardBand}")
        status = False
    if expected_upper_gb not in [actual_upper_gb - 1, actual_upper_gb, actual_upper_gb + 1]:
        logging.error(f"UpperGB Expected:{expected_upper_gb} Actual:{actual_upper_gb}")
        status = False
    if expected_line_time_dc6v != dc6v_reg_data.LineTimeDc6v:
        logging.error(f"Dc6v_line_time Expected:{expected_line_time_dc6v} Actual:{dc6v_reg_data.LineTimeDc6v}")
        status = False
    if expected_dc6v_restore_time != dc6v_reg_data.RestoreProgrammingTime:
        logging.error(
            f"Dc6vRestoreTime Expected:{expected_dc6v_restore_time} Actual:{dc6v_reg_data.RestoreProgrammingTime}")
        status = False
    actual_value = driver_interface_inst.mmio_read(DC6V_EARLY_GB_OFFSET, adapter.gfx_index)
    actual_value = actual_value & 0x000FFFFF
    if expected_early_entry_gb not in [actual_value - 1, actual_value, actual_value + 1]:
        logging.error(f"Dc6v_early entry GB Expected:{expected_early_entry_gb} Actual:{actual_value & 0x000FFFFF}")
        status = False
    if status is False:
        gdhm.report_driver_bug_pc("[PowerCons][DC6v] Legacy dc6v programming verification failed")
    return status


##
# @brief        Verify DC9 state with CS/S3
# @param[in]    adapter - adapter object
# @return       True if DC9 enters else False
def verify_dc9(adapter):
    display_power_ = DisplayPower()
    duration = 10
    power_event = PowerEvent.CS
    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return False

    if display_power_.is_power_state_supported(power_event) is False:
        power_event = PowerEvent.S3
    if display_power_.invoke_power_event(power_event, duration) is False:
        return False

    if etl_tracer.stop_etl_tracer() is False:
        logging.error("Failed to stop ETL Tracer")
        return False

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to start ETL Tracer")
        return False

    file_name = "GfxTrace_dc9_" + str(time.time()) + ".etl"
    etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
    os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_parser.generate_report(etl_file_path) is False:
        logging.error("\tFailed to generate EtlParser report")
        return False

    dcstate_data = etl_parser.get_event_data(etl_parser.Events.DC_STATE_DATA)
    if dcstate_data is None:
        logging.error("No DC state data found in ETL")
        return False

    for entry in range(len(dcstate_data)):
        logging.debug(f"DC state requested {dcstate_data[entry].DcStateRequested}")
        logging.debug(f"DC state restriction {dcstate_data[entry].DcStateRestriction}")
        if dcstate_data[entry].DcStateRequested in ['DC9', 'DC_PWR_STATE_SET_UPTO_DC9']:
            logging.info("DC9 state requested")
            if common.PLATFORM_NAME == 'MTL':
                if verify_phylatch_during_dc9_entry(adapter, etl_file_path) and \
                        verify_phylatch_during_dc9_exit(adapter, etl_file_path):
                    logging.info("phylatch programming during DC9 is successful")
                    return True
                logging.error("phylatch programming verification failed during DC9")
                return False
            return True
    logging.error("DC9 state not requested by driver")
    return False


##
# @brief        Verify phylatch set status during DC9 entry
# @param[in]    adapter - adapter object
# @param[in]    etl_file_path - etl file
# @return       True if state found else false
def verify_phylatch_during_dc9_entry(adapter, etl_file_path):
    phyclk_status = False
    phy_status = False
    if etl_parser.generate_report(etl_file_path) is False:
        logging.error("\tFailed to generate EtlParser report")
        return False

    dcstate_offsets = adapter.regs.get_dcstate_offsets()
    dcstate_mmio_data = etl_parser.get_mmio_data(dcstate_offsets.DcStateEnable, is_write=True, start_time=None,
                                                 end_time=None)

    for data in dcstate_mmio_data:
        dc_state_val = adapter.regs.get_dcstate_info(DCStateOffsetsValues(data.Data))
        if dc_state_val.PhyClkreqPg1Latch == 1:
            logging.info("PhyClkreqPg1Latch set during DC9 entry")
            phyclk_status = True
        if dc_state_val.PhyPg1Latch == 1:
            phy_status = True
            logging.info("PhyPg1Latch set during DC9 entry")

    return phy_status & phyclk_status


##
# @brief        Verify phylatch reset status during DC9 exit
# @param[in]    adapter - adapter object
# @param[in]    etl_file_path - etl file
# @return       True if state found else false
def verify_phylatch_during_dc9_exit(adapter, etl_file_path):
    phyclk_status = False
    phy_status = False
    if etl_parser.generate_report(etl_file_path) is False:
        logging.error("\tFailed to generate EtlParser report")
        return False
    dcstate_offsets = adapter.regs.get_dcstate_offsets()
    dcstate_mmio_data = etl_parser.get_mmio_data(dcstate_offsets.DcStateEnable, is_write=True, start_time=None,
                                                 end_time=None)
    for data in dcstate_mmio_data[::-1]:
        dc_state_val = adapter.regs.get_dcstate_info(DCStateOffsetsValues(data.Data))
        if dc_state_val.PhyClkreqPg1Latch == 0:
            logging.info("PhyClkreqPg1Latch reset during DC9 exit")
            phyclk_status = True
        if dc_state_val.PhyPg1Latch == 0:
            phy_status = True
            logging.info("PhyPg1Latch reset during DC9 exit")
    return phy_status & phyclk_status


##
# @brief        Verify DC state in given ETL file
# @param[in]    adapter - adapter object
# @param[in]    requested_state - expected DC states DC6/DC9/DC6v
# @param[in]    etl_file - etl file
# @return       True if state found else false
def verify_dc_state(adapter, requested_state, etl_file):
    if etl_parser.generate_report(etl_file) is False:
        logging.error("\tFailed to generate EtlParser report")
        return False

    dcstate_data = etl_parser.get_event_data(etl_parser.Events.DC_STATE_DATA)
    if dcstate_data is None:
        logging.error("No DC state data found in ETL")
        return False
    if adapter.name == 'DG2' and requested_state in ['DC6', 'DC_PWR_STATE_SET_UPTO_DC6']:
        requested_state = ['DC5', 'DC_PWR_STATE_SET_UPTO_DC5']
    else:
        requested_state = DC_STATE_MAP[requested_state]

    for entry in range(len(dcstate_data)):
        logging.debug(f"DC state requested {dcstate_data[entry].DcStateRequested}")
        logging.debug(f"DC state restriction {dcstate_data[entry].DcStateRestriction}")
        if dcstate_data[entry].DcStateRequested in requested_state:
            logging.info(f"{requested_state} state requested")
            return True

    logging.error(f"{requested_state} state not requested by driver")
    return False


##
# @brief        Verify DC state in given ETL file
# @param[in]    method  - APP/VIDEO
# @param[in]    adapter - adapter object
# @param[in]    etl_file - etl file
# @param[in] is_basic - True for Basic verification
# @return       True if state found else false
def verify_dc6v_vbi(adapter, method, etl_file, is_basic=False):
    status = True
    vbi_enable_data = []
    logging.info(f"\tGenerating EtlParser Report for {etl_file}")
    if etl_parser.generate_report(etl_file) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        return False
    logging.info("\tSuccessfully generated ETL Parser report")
    if cmtg.verify_cmtg_status(adapter) is False:
        logging.error(f"CMTG is disabled. aborting DC6v verification")
        return False
    if is_basic is False:
        if verify_dc6v_programming(method, adapter) is False:
            logging.error(f"DC6v programming verification failed")
            return False

    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                   etl_parser.InterruptType.CRTC_VSYNC)

    if interrupt_data is None:
        logging.warning("\tFAIL: No VBI enable data present in ETL file")
        return False

    for index in range(1, len(interrupt_data) - 1):
        if interrupt_data[index].CrtVsyncState == etl_parser.CrtcVsyncState.ENABLE and \
                interrupt_data[index - 1].CrtVsyncState == etl_parser.CrtcVsyncState.DISABLE_NO_PHASE:
            vbi_enable_data.append(interrupt_data[index])

    for index in range(0, len(vbi_enable_data) - 2):
        dc_state_data = etl_parser.get_event_data(etl_parser.Events.DC_STATE_DATA,
                                                  start_time=vbi_enable_data[index].TimeStamp,
                                                  end_time=vbi_enable_data[index + 1].TimeStamp)

        if dc_state_data is None:
            logging.error(f"No DC data present at {vbi_enable_data[index].TimeStamp}")

        dc6v_enabled_in_vbi = False
        for dcstate in dc_state_data:
            if dcstate.DcStateRequested in ['DC6V', 'DC_PWR_STATE_SET_UPTO_DC6V']:
                logging.info(f"DC6V enabled after VBI Enable {vbi_enable_data[index].TimeStamp}")
                dc6v_enabled_in_vbi = True
                break
        if dc6v_enabled_in_vbi is False:
            logging.error(f"DC6V disabled after VBI Enable {vbi_enable_data[index].TimeStamp}")
            status &= False
    return status


##
# @brief        Exposed API to verify DC6 in given ETL file
# @param[in]    etl_file string, etl file
# @param[in]    psr_disable_expected bool, True/False
# @return       status bool, True if state found else false
def verify_dc6_vbi(etl_file, psr_disable_expected=False):
    dcstate = ['DC6', 'DC_PWR_STATE_SET_UPTO_DC6']
    if common.PLATFORM_NAME == 'DG2':
        dcstate = ['DC5', 'DC_PWR_STATE_SET_UPTO_DC5']
    status = True
    vbi_disable_data = []
    if etl_parser.generate_report(etl_file) is False:
        logging.error("\tFailed to generate report for {0}".format(etl_file))
        return False
    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                   etl_parser.InterruptType.CRTC_VSYNC)
    logging.debug(f"Interrupt Data: {interrupt_data}")
    if interrupt_data is None:
        gdhm.report_driver_bug_pc("[PowerCons][DC6] DDI ControlInterrupt2 data not Found in ETL")
        logging.warning("\tFAIL: No VBI data present in ETL file")
        return False

    for index in range(1, len(interrupt_data) - 1):
        if interrupt_data[index].CrtVsyncState == etl_parser.CrtcVsyncState.DISABLE_NO_PHASE and \
                interrupt_data[index - 2].CrtVsyncState == etl_parser.CrtcVsyncState.ENABLE:
            vbi_disable_data.append(interrupt_data[index])
    logging.debug(f"Vbi Disable Data: {vbi_disable_data}")

    for index in range(0, len(vbi_disable_data) - 1):
        dc_state_data = etl_parser.get_event_data(etl_parser.Events.DC_STATE_DATA,
                                                  start_time=vbi_disable_data[index].TimeStamp,
                                                  end_time=vbi_disable_data[index + 1].TimeStamp)
        # In LRR panels PSR2 will be toggled during RR_switch, during this time DC state data won't be available in ETL
        if dc_state_data is None:
            if psr_disable_expected:
                continue
            gdhm.report_driver_bug_pc("[PowerCons][DC6] DC state event data not Found in ETL")
            logging.error(f"No DC data present at {vbi_disable_data[index].TimeStamp}")
            status &= False
            return status
        dc6_enabled_in_vbi = False
        for dc_state in dc_state_data:
            if dc_state.DcStateRequested in dcstate:
                logging.info(f"DC6 enabled after VBI Disable {vbi_disable_data[index].TimeStamp}")
                dc6_enabled_in_vbi = True
                break
        if (dc6_enabled_in_vbi is False) and (psr_disable_expected is False):
            logging.error(f"DC6 disabled after VBI Disable {vbi_disable_data[index].TimeStamp}")
            gdhm.report_driver_bug_pc("[PowerCons][DC6] DC6 disabled after VBI disable")
            status &= False
    return status


##
# @brief        Exposed API to verify DMC unload in given ETL file
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    etl_file string, etl file
# @return       status bool, True if state found else false
def verify_dmc_unload(adapter, panel, etl_file):
    etl_parser.generate_report(etl_file)
    ##
    # This is called by OS to stop the device, release all resources
    #  and transfer the display ownership to OS
    driver_disable = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_STOP_DEVICE_AND_RELEASE_POST_DISPLAY_OWNERSHIP)
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        dmc_ctl = MMIORegister.get_instance("PIPE_DMC_CONTROL_REGISTER", "PIPE_DMC_CONTROL_" + panel.pipe, adapter.name)
    else:
        dmc_ctl = MMIORegister.get_instance("PIPE_DMC_CONTROL_REGISTER", "PIPE_DMC_CONTROL", adapter.name)

    dmc_val = etl_parser.get_mmio_data(dmc_ctl.offset, is_write=True, start_time=driver_disable[0].StartTime)
    if driver_disable:
        for val in dmc_val:
            dmc_ctl.asUint = val.Data
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                if dmc_ctl.pipe_dmc_enable == 0:
                    logging.info(f"PIPE_{panel.pipe} DMC unloaded during driver disable at {val.TimeStamp}")
                    return True
            else:
                if panel.pipe == 'A' and dmc_ctl.pipe_dmc_enable_a == 0:
                    logging.info(f"PIPE_A DMC unloaded during driver disable at {val.TimeStamp}")
                    return True
                elif panel.pipe == 'B' and dmc_ctl.pipe_dmc_enable_b == 0:
                    logging.info(f"PIPE_B DMC unloaded during driver disable at {val.TimeStamp}")
                    return True
    else:
        logging.error("DDI STOP DEVICE call not found in ETL")
    return False


##
# @brief        Exposed API to verify DMC enable in given ETL file
# @param[in]    adapter object
# @param[in]    panel object
# @param[in]    etl_file string, etl file
# @return       status bool, True if state found else false
def verify_dmc_load(adapter, panel, etl_file):
    etl_parser.generate_report(etl_file)
    driver_enable = etl_parser.get_ddi_data(etl_parser.Ddi.DDI_START_DEVICE)
    if adapter.name in common.PRE_GEN_14_PLATFORMS:
        dmc_ctl = MMIORegister.get_instance("PIPE_DMC_CONTROL_REGISTER", "PIPE_DMC_CONTROL_" + panel.pipe, adapter.name)
    else:
        dmc_ctl = MMIORegister.get_instance("PIPE_DMC_CONTROL_REGISTER", "PIPE_DMC_CONTROL", adapter.name)

    dmc_val = etl_parser.get_mmio_data(dmc_ctl.offset, is_write=True, start_time=driver_enable[0].StartTime)
    if driver_enable:
        for val in dmc_val:
            dmc_ctl.asUint = val.Data
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                if dmc_ctl.pipe_dmc_enable == 1:
                    logging.info(f"PIPE_{panel.pipe} DMC loaded during driver enable at {val.TimeStamp}")
                    return True
            else:
                if panel.pipe == 'A' and dmc_ctl.pipe_dmc_enable_a == 1:
                    logging.info(f"PIPE_A DMC loaded during driver enable at {val.TimeStamp}")
                    return True
                elif panel.pipe == 'B' and dmc_ctl.pipe_dmc_enable_b == 1:
                    logging.info(f"PIPE_B DMC loaded during driver enable at {val.TimeStamp}")
                    return True
    else:
        logging.error("DDI START DEVICE call not found in ETL")
    return False


##
# @brief        Verify DC6v programming with VRR fixed RR mode
# @param[in]    adapter - adapter object
# @param[in]    panel - panel object
# @return       True if successful else False
def verify_dc6v_guardband_programming_on_vrr_panel(adapter, panel):
    dc6v_regs = adapter.regs.get_dc6v_offsets()
    wm_line_time_reg = MMIORegister.get_instance("WM_LINETIME_REGISTER", "WM_LINETIME_" + panel.pipe, adapter.name)
    dmc_scanline_cmp_lower_reg = MMIORegister.get_instance(
        "PIPE_DMC_SCANLINE_CMP_LOWER_REGISTER", "PIPE_DMC_SCANLINE_CMP_LOWER_" + panel.transcoder, adapter.name)
    dmc_scanline_cmp_upper_reg = MMIORegister.get_instance(
        "PIPE_DMC_SCANLINE_CMP_UPPER_REGISTER", "PIPE_DMC_SCANLINE_CMP_UPPER_" + panel.transcoder, adapter.name)

    # Get actual data from ETL
    line_time_data = etl_parser.get_mmio_data(dc6v_regs.LineTimeDc6v, is_write=True)
    if line_time_data is None:
        logging.error(f"{dc6v_regs.LineTimeDc6v} mmio write data not found in ETL")

    upper_gb_data = etl_parser.get_mmio_data(DC6V_UPPER_GB_OFFSET, is_write=True)
    if upper_gb_data is None:
        logging.error(f"{DC6V_UPPER_GB_OFFSET} mmio write data not found in ETL")
    lower_gb_data = etl_parser.get_mmio_data(dc6v_regs.GuardBand, is_write=True)
    if lower_gb_data is None:
        logging.error(f"{dc6v_regs.GuardBand} mmio write data not found in ETL")
    early_entry_gb_data = etl_parser.get_mmio_data(DC6V_EARLY_GB_OFFSET, is_write=True)
    if early_entry_gb_data is None:
        logging.error(f"{DC6V_EARLY_GB_OFFSET} mmio write data not found in ETL")
    restore_time_data = etl_parser.get_mmio_data(dc6v_regs.RestoreProgrammingTime)
    if restore_time_data is None:
        logging.error(f"{dc6v_regs.RestoreProgrammingTime} mmio write data not found in ETL")

    wm_line_time_data = etl_parser.get_mmio_data(wm_line_time_reg.offset)
    if wm_line_time_data is None:
        logging.error(f"{wm_line_time_reg.offset} mmio data not found in ETL")
    else:
        wm_line_time_reg.asUint = wm_line_time_data[-1].Data

    scanline_cmp_low = etl_parser.get_mmio_data(dmc_scanline_cmp_lower_reg.offset, is_write=True)
    if scanline_cmp_low is None:
        logging.error(f"{dmc_scanline_cmp_lower_reg.offset} mmio write data not found in ETL")
    else:
        dmc_scanline_cmp_lower_reg.asUint = scanline_cmp_low[-1].Data

    scanline_cmp_up = etl_parser.get_mmio_data(dmc_scanline_cmp_upper_reg.offset, is_write=True)
    if scanline_cmp_up is None:
        logging.error(f"{dmc_scanline_cmp_upper_reg.offset} mmio write data not found in ETL")
    else:
        dmc_scanline_cmp_upper_reg.asUint = scanline_cmp_up[-1].Data

    if None in (line_time_data, upper_gb_data, lower_gb_data, early_entry_gb_data, restore_time_data,
                wm_line_time_data, scanline_cmp_low, scanline_cmp_up):
        gdhm.report_driver_bug_pc("[PowerCons][DC6v] DC6v MMIO entries not found in ETL")
        return False

    # verify dc6v programming with fixed RR mode, Bspec - https://gfxspecs.intel.com/Predator/Home/Index/55255
    dc5_to_dc3_exit_latency_us = 600

    # WM line time & DC6v line time
    line_time_actual = line_time_data[-1].Data
    line_time_expected = wm_line_time_reg.line_time - 1  # Always use round-down value for Dc6v line time
    if line_time_actual != line_time_expected:
        logging.error(f"Dc6v_line_time Actual:{line_time_actual} Expected:{line_time_expected}")
        gdhm.report_driver_bug_pc("[PowerCons][DC6v] Line time programming mismatch between WM & DC6v registers")
        return False
    logging.info(f"Dc6v_line_time Actual:{line_time_actual} Expected:{line_time_expected}")

    # line_time_data will be in units of 0.125us.
    line_time_ns = math.ceil(wm_line_time_reg.line_time * 125)  # (line_time / 8) * 1000

    status = True
    # DC6v upper GB
    upper_gb_actual = upper_gb_data[-1].Data
    upper_gb_expected = dmc_scanline_cmp_lower_reg.scanline_lower - math.ceil(
        dc5_to_dc3_exit_latency_us * 1000 / line_time_ns)
    if upper_gb_actual not in (upper_gb_expected - 1, upper_gb_expected, upper_gb_expected + 1):
        logging.error(f"Dc6vUpperGB Actual:{upper_gb_actual} Expected:{upper_gb_expected}")
        status = False
    else:
        logging.info(f"Dc6vUpperGB Actual:{upper_gb_actual} Expected:{upper_gb_expected}")

    # DC6v lower GB
    lower_gb_actual = lower_gb_data[-1].Data
    lower_gb_expected = (upper_gb_expected - 8)
    if lower_gb_actual not in (lower_gb_expected - 1, lower_gb_expected, lower_gb_expected + 1):
        logging.error(f"DC6vLowerGB Actual:{lower_gb_actual} Expected:{lower_gb_expected}")
        status = False
    else:
        logging.info(f"DC6vLowerGB Actual:{lower_gb_actual} Expected:{lower_gb_expected}")

    # DC6v early entry GB (0-19 bits)
    early_entry_gb_actual = early_entry_gb_data[-1].Data & 0x000FFFFF
    early_entry_gb_expected = lower_gb_expected - math.ceil(dc5_to_dc3_exit_latency_us * 1000 / line_time_ns)
    if early_entry_gb_actual != early_entry_gb_expected:
        logging.error(f"Dc6vEarlyEntryGB Actual:{early_entry_gb_actual} Expected:{early_entry_gb_expected}")
        status = False
    else:
        logging.info(f"Dc6vEarlyEntryGB Actual:{early_entry_gb_actual} Expected:{early_entry_gb_expected}")

    # DC6v restore time (0-15 bits)
    restore_time_actual = restore_time_data[-1].Data & 0x0000FFFF
    restore_time_expected = (dmc_scanline_cmp_upper_reg.scanline_upper - lower_gb_expected) * line_time_ns
    restore_time_expected = math.ceil(restore_time_expected / 1000) + 50
    if restore_time_actual != restore_time_expected:
        logging.error(f"Dc6vRestoreTime Actual:{restore_time_actual} Expected:{restore_time_expected}")
        status = False
    else:
        logging.info(f"Dc6vRestoreTime Actual:{restore_time_actual} Expected:{restore_time_expected}")

    if status is False:
        logging.error("Dc6v Guardband programming on VRR panel verification failed")
        gdhm.report_driver_bug_pc("[PowerCons][DC6v] Dc6v Guardband programming on VRR panel verification failed")
    else:
        logging.info("Dc6v Guardband programming on VRR panel verification passed")
    return status
