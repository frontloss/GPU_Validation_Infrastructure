########################################################################################################################
# @file         dmrrs.py
# @brief        Contains APIs to enable and verify DMRRS
#
# @author       Vinod D S, Rohit Kumar
########################################################################################################################

import logging
import sys

from DisplayRegs.DisplayOffsets import TimingOffsetValues, VrrOffsetValues
from Libs.Core import etl_parser, registry_access, display_essential
from Libs.Core.logger import gdhm, html
from Libs.Core.vbt import vbt
from Libs.Feature.powercons import registry
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, dut
from Tests.PowerCons.Modules.dut_context import Adapter, Panel, RrSwitchingMethod
from Libs.Core.display_config import display_config

FRACTIONAL_RR_FACTOR = 0.999  # 99.9% of RR is fractional RR
VBLANK_MAX_DURATION = 0xFFFFFFFF

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1
ETL_PARSER_CONFIG.flipData = 1
ETL_PARSER_CONFIG.mmioData = 1
ETL_PARSER_CONFIG.displayDiagnosticsData = 1
ETL_PARSER_CONFIG.interruptData = 1
ETL_PARSER_CONFIG.vbiData = 1


##
# @brief        Exposed object for different media FPS
class MediaFps:
    FPS_23_976 = 23.976
    FPS_24_000 = 24.000
    FPS_25_000 = 25.000
    FPS_29_970 = 29.970
    FPS_30_000 = 30.000
    FPS_59_940 = 59.940
    FPS_60_000 = 60.000


VIDEO_FILE_MAPPING = {
    '24': '24.000.mp4',
    '25': '25.000.mp4',
    '30': '30.000.mp4',
    '23_976': '23.976.mp4',
    '29_970': '29.970.mp4',
    '59_940': '59.940.mp4'
}

VIDEO_FPS_MAPPING = {
    '24.000.mp4': 24.000,
    '25.000.mp4': 25.000,
    '30.000.mp4': 30.000,
    '23.976.mp4': 23.976,
    '29.970.mp4': 29.970,
    '59.940.mp4': 59.940
}


##
# @brief        Exposed API to enable DMRRS
# @param[in]    adapter Adapter
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise
@html.step("Enabling DMRRS using reg-key")
def enable(adapter: Adapter) -> bool:
    assert adapter

    logging.info(f"\tEnabling DMRRS on {adapter.gfx_index}")
    # Enable DMRRS from internal reg-key
    dmrrs_int_status = configure_dmrrs_internal_reg_key(adapter, enable_dmrrs=True)
    if dmrrs_int_status is False:
        return False
    # Enable DMRRS from exposed reg-key for LFP
    dmrrs_ex_lfp_status = configure_dmrrs_exposed_reg_key(adapter, enable_dmrrs=True, is_lfp=False)
    if dmrrs_ex_lfp_status is False:
        return False
    # Enable DMRRS from exposed reg-key for EFP
    dmrrs_ex_efp_status = configure_dmrrs_exposed_reg_key(adapter, enable_dmrrs=True, is_lfp=True)
    if dmrrs_ex_efp_status is False:
        return False

    return dmrrs_int_status or dmrrs_ex_lfp_status or dmrrs_ex_efp_status


##
# @brief        Exposed API to disable DMRRS
# @param[in]    adapter Adapter
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise
@html.step("Disabling DMRRS using reg-key")
def disable(adapter: Adapter) -> bool:
    assert adapter

    logging.info(f"\tDisabling DMRRS on {adapter.gfx_index}")
    # Disable DMRRS from internal reg-key
    dmrrs_int_status = configure_dmrrs_internal_reg_key(adapter, enable_dmrrs=False)
    if dmrrs_int_status is False:
        return False
    # Disable DMRRS from exposed reg-key for LFP
    dmrrs_ex_lfp_status = configure_dmrrs_exposed_reg_key(adapter, enable_dmrrs=False, is_lfp=True)
    if dmrrs_ex_lfp_status is False:
        return False
    # Disable DMRRS from exposed reg-key for EFP
    dmrrs_ex_efp_status = configure_dmrrs_exposed_reg_key(adapter, enable_dmrrs=False, is_lfp=False)
    if dmrrs_ex_efp_status is False:
        return False

    return dmrrs_int_status or dmrrs_ex_lfp_status or dmrrs_ex_efp_status


##
# @brief        Exposed API to enable or disable DMRRS in internal(debug) reg key
# @param[in]    adapter object, Adapter
# @param[in]    enable_dmrrs Boolean, True for enabling & False for disabling
# @return       status Boolean, True updated & restart required, None updated & no restart required, False otherwise
@html.step("Configuring DMRRS using internal (debug) reg-key")
def configure_dmrrs_internal_reg_key(adapter: Adapter, enable_dmrrs: bool) -> bool:
    assert adapter

    reg_key = registry.RegKeys.DRRS.MEDIA_REFRESH_RATE_SUPPORT
    value = registry.RegValues.DRRS.MDRRS_ENABLE if enable_dmrrs else registry.RegValues.DRRS.MDRRS_DISABLE

    logging.info(f"\t{'Enabling' if enable_dmrrs else 'Disabling'} DMRRS on {adapter.gfx_index} with {reg_key}")
    dmrrs_status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, value)
    if dmrrs_status is False:
        logging.error(f"\tFailed to update {reg_key} registry key")
        return False
    logging.info("\tPASS: {0:35} Expected= {1}, Actual= {1}".format(reg_key, hex(value)))
    return dmrrs_status


##
# @brief        Exposed API to enable or disable DMRRS in exposed reg key
# @param[in]    adapter object, Adapter
# @param[in]    enable_dmrrs Boolean, True for enabling & False for disabling
# @param[in]    is_lfp Boolean, True if LFP else False
# @return       status Boolean, True updated & restart required, None updated & no restart required, False otherwise
@html.step("Configuring DMRRS using exposed reg-key")
def configure_dmrrs_exposed_reg_key(adapter: Adapter, enable_dmrrs: bool, is_lfp: bool):
    assert adapter

    reg_key = registry.RegKeys.PC.FEATURE_CONTROL
    reg_value = registry.read(adapter.gfx_index, reg_key)
    logging.info(f"DisplayPcFeatureControl reg-key value= {hex(reg_value)}")

    if is_lfp:
        lfp_expected_value = 0 if enable_dmrrs else registry.RegValues.DRRS.DMRRS_DISABLE_INTERNAL_PANEL_PC_FTR_CTL
        if (reg_value & registry.RegValues.DRRS.DMRRS_DISABLE_INTERNAL_PANEL_PC_FTR_CTL) == lfp_expected_value:
            logging.info(f"DMRRS already {'enabled' if enable_dmrrs else 'disabled'} for LFP on {adapter.gfx_index}")
            return None
        if enable_dmrrs:
            reg_value = reg_value & registry.RegValues.DRRS.DMRRS_ENABLE_INTERNAL_PANEL_PC_FTR_CTL
        else:
            reg_value = reg_value | registry.RegValues.DRRS.DMRRS_DISABLE_INTERNAL_PANEL_PC_FTR_CTL
    else:
        efp_expected_value = 0 if enable_dmrrs else registry.RegValues.DRRS.DMRRS_DISABLE_EXTERNAL_PANEL_PC_FTR_CTL
        if (reg_value & registry.RegValues.DRRS.DMRRS_DISABLE_EXTERNAL_PANEL_PC_FTR_CTL) == efp_expected_value:
            logging.info(f"DMRRS already {'enabled' if enable_dmrrs else 'disabled'} for EFP on {adapter.gfx_index}")
            return None
        if enable_dmrrs:
            reg_value = reg_value & registry.RegValues.DRRS.DMRRS_ENABLE_EXTERNAL_PANEL_PC_FTR_CTL
        else:
            reg_value = reg_value | registry.RegValues.DRRS.DMRRS_DISABLE_EXTERNAL_PANEL_PC_FTR_CTL

    dmrrs_status = registry.write(adapter.gfx_index, reg_key, registry_access.RegDataType.DWORD, reg_value)

    if dmrrs_status is False:
        logging.error(f"\tFailed to update {reg_key} registry key")
        return False

    logging.info(f"Successfully updated regkey {reg_key}= {reg_value}")
    return dmrrs_status


##
# @brief        Exposed API to verify DMRRS
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @param[in]    etl_path String path to etl file
# @param[in]    media_fps Float
# @param[in]    etl_started_before_video bool, True, if ETL trace started before video,
#                                            False, if video is already playing and new ETL has started
# @return       status Boolean, True if verification is successful, False otherwise
def verify(adapter: Adapter, panel: Panel, etl_path: str, media_fps: float, etl_started_before_video=True) -> bool:
    assert adapter
    assert panel
    assert etl_path
    assert media_fps

    present_duration_timestamps = []
    last_flip_timestamp = None
    status = True
    flips_without_duration = 0
    zero_duration_time = 0
    non_zero_duration_time = 0

    html.step_start(f"Verifying DMRRS with {media_fps} FPS")
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
    # If ETL started before video launch, check present duration should be there
    # If ETL started when video is already playing, check present duration would have already happened
    if etl_started_before_video:
        status = __verify_check_present_duration(panel, media_fps)

    logging.info("\tStep: Verifying VBI notification calls during video playback")
    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                   etl_parser.InterruptType.CRTC_VSYNC)
    if interrupt_data is None:
        logging.info("\t\tNo VBI notification found during video playback")
    else:
        logging.warning("\t\tVBI notification data found during video playback")
        for interrupt in interrupt_data:
            logging.info(f"\t\t{interrupt}")

    flip_data = etl_parser.get_flip_data('PIPE_' + panel.pipe)
    if flip_data is None:
        logging.warning(f"\tNo flip data found for PIPE_{panel.pipe}")
    else:
        logging.info(f"\tIncoming flips on PIPE_{panel.pipe}: {len(flip_data)}")
        durations = {}
        previous_duration_flip = None
        last_flip_timestamp = None
        for flip in flip_data:
            # Skip the flips with plane disable call, these flips might have unexpected data.
            is_plane_disable_call = False
            for plane_info in flip.PlaneInfoList:
                if plane_info.Flags == "":
                    is_plane_disable_call = True
                    logging.info("\tSkipping: Flip found with plane disable call (it might have unexpected data)")
                    break

            if is_plane_disable_call:
                logging.debug(f"\tSkipped plane disable flip for duration calculation")
                logging.debug(f"\t{flip}")
                continue

            if flip.Duration is not None:
                if 0 < flip.Duration < VBLANK_MAX_DURATION:
                    present_duration_timestamps.append(flip.TimeStamp)

                if flip.Duration == 0:
                    flips_without_duration += 1

                if flip.Duration in durations.keys():
                    durations[flip.Duration] += 1
                else:
                    durations[flip.Duration] = 1

                if previous_duration_flip is None:
                    last_flip_timestamp = flip.TimeStamp
                    previous_duration_flip = flip
                    logging.info(f"\t\tFlip Duration= {flip.Duration} [START - {last_flip_timestamp}]")
                    zero_start_duration = last_flip_timestamp
                    continue

                if previous_duration_flip.Duration != flip.Duration:
                    new_duration_start = last_flip_timestamp
                    logging.info(f"\t\tFlip Duration= {previous_duration_flip.Duration} "
                                 f"[{last_flip_timestamp} - {previous_duration_flip.TimeStamp}]")
                    last_flip_timestamp = flip.TimeStamp

                    if previous_duration_flip.Duration == 0:
                        zero_duration_time += previous_duration_flip.TimeStamp - new_duration_start
                    else:
                        non_zero_duration_time += previous_duration_flip.TimeStamp - new_duration_start

                if previous_duration_flip.Duration != 0:
                    # When BFR is enabled, OS will send non-zero duration without VPB, hence added this check
                    # for BFR supported panel
                    if round(common.duration_to_hz(previous_duration_flip.Duration)) != panel.current_mode.refreshRate:
                        interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                                       etl_parser.InterruptType.CRTC_VSYNC)
                        if interrupt_data is not None:
                            for interrupt in interrupt_data:
                                if previous_duration_flip.Duration <= interrupt.TimeStamp <= flip.TimeStamp:
                                    if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.DISABLE_NO_PHASE]:
                                        logging.error(
                                            f"\t\tVBI disable notification received during video playback "
                                            f"{interrupt.TimeStamp}")
                                        gdhm.report_driver_bug_os("[OsFeatures][DMRRS] VBI disable notification "
                                                                  "received during video playback")
                                        status = False

                previous_duration_flip = flip

        if last_flip_timestamp is not None:
            logging.info(
                f"\t\tFlip Duration= {previous_duration_flip.Duration} [{last_flip_timestamp} - END]")
            zero_duration_time += previous_duration_flip.TimeStamp - last_flip_timestamp

        # Check Non-zero duration during video playback
        is_non_zero_duration_present = False
        if bool(durations):
            for duration in durations.keys():
                logging.info(f"\t\tFlips with duration {duration}({common.duration_to_hz(duration)}Hz)=\
                            {durations[duration]}")
                if duration != 0:
                    is_non_zero_duration_present = True
            if is_non_zero_duration_present is False:

                expected_rr = media_fps
                while round(expected_rr) < panel.drrs_caps.min_rr:
                    expected_rr += media_fps

                expected_rr = min(panel.drrs_caps.max_rr, expected_rr)  # Limit expected RR to max RR
                expected_rr = max(round(panel.drrs_caps.min_rr / 1.001, 3), expected_rr)  # Limit expected RR to min RR

                # If expected RR is applied RR, then OS might not send non-zero flip duration.
                if expected_rr in [panel.current_mode.refreshRate, round(panel.current_mode.refreshRate/1.001, 3)]:
                    logging.info(f"\tPASS: Flip Verification skipped as Expected RR {expected_rr} == "
                                 f"Applied RR ({panel.current_mode.refreshRate}) or "
                                 f"{round(panel.current_mode.refreshRate/1.001,3)}")
                else:
                    if media_fps in [MediaFps.FPS_59_940, MediaFps.FPS_60_000]:
                        logging.info(f"\tPASS: Flip Verification skipped as OS is not sending Flip for "
                                     f"{MediaFps.FPS_60_000} or {MediaFps.FPS_59_940} Media FPS")
                    else:
                        logging.error(
                            f"FAIL: Non-zero duration flips not found during video playback of {media_fps} FPS,"
                            f"Applied RR ({panel.current_mode.refreshRate}) or "
                            f"{round(panel.current_mode.refreshRate / 1.001, 3)} or {panel.drrs_caps.min_rr}"
                            f"or {panel.drrs_caps.max_rr}")
                        gdhm.report_driver_bug_os("[OsFeatures][DMRRS] Non-zero duration flips not found during video "
                                                  "playback")
                        return False

        # Check if OS is sending flips with MAX_DURATION during video playback
        if VBLANK_MAX_DURATION in durations.keys():
            logging.warning('\tOS is sending flips with VBLANK_MAX_DURATION during video playback')
            gdhm.report_driver_bug_os("[OsFeatures][DMRRS] OS is sending flips with MAX_DURATION during video playback")

        # Check if DMRRS was enabled most of the time during video playback
        if len(present_duration_timestamps) > 0:
            logging.info("\tStep: Verifying DMRRS was enabled most of the time during video playback")
            logging.info(f"Total Zero duration time: {zero_duration_time}, Total non-zero duration time: {non_zero_duration_time}")
            if non_zero_duration_time < zero_duration_time:
                logging.warning("\t\tDMRRS active period is lower than expected")
                gdhm.report_driver_bug_os("[OsFeatures][DMRRS] DMRRS active period is lower than expected")
            html.step_end()

        if len(present_duration_timestamps) > 0:
            # Check for any mouse move event after DMRRS got enabled
            logging.info("\tStep: Verifying DMRRS status before/ after cursor movement during video playback")
            ddi_data = etl_parser.get_ddi_data(
                etl_parser.Ddi.DDI_SETPOINTERPOSITION, start_time=present_duration_timestamps[0])
            if ddi_data is None:
                logging.info('\t\tNo mouse pointer movement detected during video playback')
            else:
                index = 0
                while index < len(ddi_data):
                    ddi = ddi_data[index]
                    logging.info(f"\t\t{ddi}")

                    # Check if multiple mouse moves happened within 10 seconds
                    is_subsequent_mouse_moves = False
                    if index < (len(ddi_data) - 1):
                        if (ddi_data[index + 1].StartTime - ddi.StartTime) < 10000:
                            is_subsequent_mouse_moves = True

                    dmrrs_got_enabled_back = False
                    # Calculate time taken by OS to turn DMRRS back ON
                    for timestamp in present_duration_timestamps:
                        if timestamp > ddi.StartTime:
                            logging.info("\t\t\tPASS: DMRRS got enabled back after {0} ms ({1})".format(
                                (timestamp - ddi.StartTime), timestamp))

                            # Fail if DMRRS enabling is taking more than 10 seconds after mouse move
                            # After moving mouse over full screen video playback window, control panel comes up.
                            # OS takes around 7 seconds to hide control panel. DMRRS should kick in after that.
                            # if is_subsequent_mouse_moves is False:
                            #     if (timestamp - ddi.StartTime) > 10000:
                            #         status = False

                            dmrrs_got_enabled_back = True
                            break

                    # Skip the failure reporting for subsequent mouse moves
                    if is_subsequent_mouse_moves:
                        index += 1
                        continue

                    # if dmrrs_got_enabled_back is False:
                    #     # Skip the failure reporting for last 10 seconds for video playback
                    #     if (last_flip_timestamp - ddi.StartTime) > 10000:
                    #         logging.error(
                    #             "\t\tDMRRS is not getting enabled after mouse pointer movement during video playback")
                    #         gdhm.report_bug(
                    #             title="[PowerCons][DMRRS] DMRRS is not getting enabled after mouse pointer movement",
                    #             problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    #             component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                    #             priority=gdhm.Priority.P2,
                    #             exposure=gdhm.Exposure.E2
                    #         )
                    #         status = False

                    index += 1
            html.step_end()

    # Check for VBI when VSYNC_DISABLE call is coming from OS (consider zero duration region).
    if check_no_vbi_during_vsync_disable(panel) is False:
        logging.error(f"FAIL: VBI data found during VSYNC_DISABLE call for {panel.port}[Reported via GDHM]")
        # @Todo This will be sporadic behavior, we will analyze GDHM for few weeks and if issue is not seen we
        # @Todo will uncomment this code
        # status = False

    # If PSR2 is disabled, RR switching method should be VTOTAL_HW
    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_SW:
        if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_2) is False:
            logging.info("\tPSR2 is disabled. Changing RR_SWITCH METHOD from VTOTAL_SW to VTOTAL_HW")
            panel.lrr_caps.rr_switching_method = RrSwitchingMethod.VTOTAL_HW

    # Check to verify always VRR.
    if check_always_vrr(adapter, panel) is False:
        logging.error(f"FAIL: Always VRR check failed for panel at {panel.port}")
        status = False

    status &= verify_clock_programming(adapter, panel, media_fps)

    if status:
        logging.info(f"\tDMRRS is functional with media FPS= {media_fps}")
    else:
        logging.error(f"\tDMRRS is NOT functional with media FPS= {media_fps}")

    return status


##
# @brief        Helper API to verify clock programming
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @param[in]    media_fps float
# @param[in]    is_hrr_enabled Boolean, True if HRR is enabled, False otherwise.
# @return       status Boolean, True if operation is successful, False otherwise
def verify_clock_programming(adapter: Adapter, panel: Panel, media_fps: float, is_hrr_enabled=False) -> bool:
    assert adapter
    assert panel
    assert media_fps

    # Todo: uncomment the below code and remove the line "expected_rr = 60.0 if media_fps == 59.940 else media_fps",
    #   if MSFT agrees to send duration for 59.940fps video playback
    #   Refer HSD-18018642354 (OS is not issuing non-zero duration for 59.940 fps video)
    # expected_rr = media_fps
    # If OS starts issuing duration for 59.940fps videos then RR will be switched as the trigger for RR switch is
    # non-zero duration in the flips

    expected_rr = media_fps

    # handling HRR
    if is_hrr_enabled:
        # find the first multiple in half refresh rate range.
        half_min_rr = round((panel.drrs_caps.min_rr / 2), 3)
        while round(expected_rr) < half_min_rr:
            expected_rr += media_fps
        # If it does not fall in the actual panel refresh rate range, double it.
        # expected_rr is always in actual panel range
        if round(expected_rr) < panel.drrs_caps.min_rr:
            expected_rr *= 2

        # if round(expected_rr) > panel.max_rr - Fail the test
        # Ex: On any 60-90Hz panel. HRR will not work
        # Reason: Consider 24fps video playback. HRR range will be (30Hz - 90Hz)
        # First multiple of 24 is 48 in (30-90)Hz range.
        # Actual RR that needs to be programmed is 96Hz which is not possible as max_rr of the panel is 90Hz.
        # So HRR will not be enabled.
        if round(expected_rr) > round(panel.drrs_caps.max_rr):
            logging.error(f"There will be no HRR on panels with ExpectedRR= {expected_rr} > \
                            MaxRR= {panel.drrs_caps.max_rr}")
            return False
    else:
        while round(expected_rr) < panel.drrs_caps.min_rr:
            expected_rr += media_fps

    expected_rr = min(panel.drrs_caps.max_rr, expected_rr)  # Limit expected RR to max RR
    expected_rr = max(round(panel.drrs_caps.min_rr / 1.001, 3), expected_rr)  # Limit expected RR to min RR

    # If expected RR is applied RR, skip the clock verification as duration will come as 0, and DMRRS path will not be
    # triggered from driver side. There will be no LINKM MMIO entries in ETL.
    # If expected RR is max RR, driver will not follow VRR path
    if expected_rr in [panel.current_mode.refreshRate, round(panel.current_mode.refreshRate/1.001, 3),
                       panel.drrs_caps.max_rr]:
        logging.info(f"\tPASS: Clock verification skipped as Expected RR({expected_rr}) == "
                     f"applied RR [{panel.current_mode.refreshRate}, {round(panel.current_mode.refreshRate/1.001, 3)}]"
                     f"or Max RR {panel.drrs_caps.max_rr}")
        return True
    if media_fps in [MediaFps.FPS_60_000, MediaFps.FPS_59_940]:
        logging.info(f"\tPASS: Clock verification skipped as OS not sending Non Zero Duration for "
                     f"{MediaFps.FPS_60_000} or {MediaFps.FPS_59_940} media FPS")
        return True
    return drrs.verify_clock_programming(adapter, panel, expected_rr)


##
# @brief        Helper API to verify DMRRS exit
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @return       status Boolean, True if operation is successful, False otherwise
def verify_dmrrs_exit(adapter: Adapter, panel: Panel) -> bool:
    assert adapter
    assert panel
    status = False

    html.step_start("Verifying DMRRS exit after media playback")

    timing_info = adapter.regs.get_timing_info(panel.transcoder_type)
    current_mode_rr = round(
        float(panel.current_mode.pixelClock_Hz) / ((timing_info.HTotal + 1) * (timing_info.VTotal + 1)), 3)
    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.CLOCK:
        rr = drrs.link_m_to_hz(adapter, panel, timing_info.LinkM)

        # Keeping 0.02 as precision tolerance
        if common.compare_with_tolerance(rr, panel.drrs_caps.max_rr, drrs.FPS_TOLERANCE) or \
                common.compare_with_tolerance(rr, panel.drrs_caps.min_rr, drrs.FPS_TOLERANCE) or \
                common.compare_with_tolerance(rr, current_mode_rr, drrs.FPS_TOLERANCE):
            logging.info(
                "\tPASS: CLOCK based RR after media playback Actual= {0}, Expected= {1}".format(
                    rr, [panel.drrs_caps.min_rr, panel.drrs_caps.max_rr, current_mode_rr]))
            status = True
        # Comparing with the actual max RR, actual min RR as the driver considers the clock value in DTD for max RR
        elif common.compare_with_tolerance(rr, panel.actual_max_rr, drrs.FPS_TOLERANCE) or \
                common.compare_with_tolerance(rr, panel.drrs_caps.actual_min_rr, drrs.FPS_TOLERANCE):
            logging.info("\tPASS: CLOCK based RR after media playback Actual= {0}, Expected= {1}".format(
                rr, [panel.drrs_caps.actual_min_rr, panel.actual_max_rr]))
            status = True
        else:
            logging.error("\tFAIL: CLOCK based RR after media playback Actual= {0}, Expected= {1}".format(
                rr, [panel.drrs_caps.min_rr, panel.drrs_caps.max_rr, current_mode_rr]))
            logging.error("\tRR is NOT changing back after media playback")
            gdhm.report_driver_bug_os("[OsFeatures][DMRRS] Clock based RR is not changing back after media playback")

    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_HW:
        # In case of VRR way, VRR should get disabled after closing the media
        vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type)
        if vrr_info.VrrEnable:
            # If VRR is still enabled, check if it is a DRRS scenario
            if adapter.name in common.GEN_16_PLATFORMS and panel.panel_type == "DP" and panel.is_lfp == False:
                rr = round(
                    float(panel.native_mode.pixelClock_Hz) / ((timing_info.HTotal + 1) * (vrr_info.VrrDcbVmax + 1)), 3)
                logging.info(f"DCB: RR - {rr}, VrrDcbVmax - {vrr_info.VrrDcbVmax}")
                logging.info(f"DCB: adapter.name = {adapter.name}, panel_type = {panel.panel_type}")
            else:
                rr = round(
                    float(panel.native_mode.pixelClock_Hz) / ((timing_info.HTotal + 1) * (vrr_info.VrrVmax + 1)), 3)
                logging.info(f"RR - {rr}, VrrVmax - {vrr_info.VrrVmax}")
                logging.info(f"adapter.name = {adapter.name}, panel_type = {panel.panel_type}")

            if common.compare_with_tolerance(rr, panel.drrs_caps.max_rr, drrs.FPS_TOLERANCE) or \
                    common.compare_with_tolerance(rr, panel.drrs_caps.min_rr, drrs.FPS_TOLERANCE) or \
                    common.compare_with_tolerance(rr,current_mode_rr, drrs.FPS_TOLERANCE):
                logging.info(
                    "\tPASS: VTOTAL_HW based RR after media playback Actual= {0:.2f}, Expected= {1}".format(
                        rr, [panel.drrs_caps.min_rr, panel.drrs_caps.max_rr, current_mode_rr]))
                status = True
            # When BFR mode is applied the RR can return to the half of the panel rr
            elif is_dynamic_mode_enabled(panel) and common.compare_with_tolerance(rr, panel.current_mode.refreshRate,
                                                                                  drrs.FPS_TOLERANCE):
                logging.info(
                    "\tPASS: VTOTAL_SW based RR after media playback Actual= {0:.2f}, Expected= {1}".format(
                        rr, [panel.current_mode.refreshRate]))
                status = True
            else:
                logging.error(
                    "\tFAIL: VTOTAL_HW based RR after media playback Actual= {0:.2f}, Expected= {1}".format(
                        rr, [panel.drrs_caps.min_rr, panel.drrs_caps.max_rr, current_mode_rr]))
                logging.error("\tRR is NOT changing back after media playback")
                gdhm.report_driver_bug_os("[OsFeatures][DMRRS] VTOTAL_HW based RR is not changing back after "
                                          "media playback")
        else:
            logging.info("\tPASS: VRR got disabled after closing media")
            status = True

    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.VTOTAL_SW:
        rr = float(panel.native_mode.pixelClock_Hz) / ((timing_info.HTotal + 1) * (timing_info.VTotal + 1))

        if common.compare_with_tolerance(rr, panel.drrs_caps.max_rr, drrs.FPS_TOLERANCE) or \
                common.compare_with_tolerance(rr, panel.drrs_caps.min_rr, drrs.FPS_TOLERANCE) or \
                    common.compare_with_tolerance(rr,current_mode_rr, drrs.FPS_TOLERANCE):
            logging.info(
                "\tPASS: VTOTAL_SW based RR after media playback Actual= {0:.2f}, Expected= {1}".format(
                    rr, [panel.drrs_caps.min_rr, panel.drrs_caps.max_rr, current_mode_rr]))
            status = True
        # When BFR mode is applied the RR can return to the half of the panel rr
        elif is_dynamic_mode_enabled(panel) and common.compare_with_tolerance(rr, panel.current_mode.refreshRate,
                                                                              drrs.FPS_TOLERANCE):
            logging.info(
                "\tPASS: VTOTAL_SW based RR after media playback Actual= {0:.2f}, Expected= {1}".format(
                    rr, [panel.current_mode.refreshRate]))
            status = True
        else:
            logging.error(
                "\tFAIL: VTOTAL_SW based RR after media playback Actual= {0:.2f}, Expected= {1}".format(
                    rr, [panel.drrs_caps.min_rr, panel.drrs_caps.max_rr, current_mode_rr]))
            logging.error("\tRR is NOT changing back after media playback")
            gdhm.report_driver_bug_os("[OsFeatures][DMRRS] VTOTAL_SW based RR is not changing back after"
                                      " media playback")

    html.step_end()
    return status


##
# @brief        Exposed API to get DMRRS enabled or not in VBT
# @param[in]    adapter Adapter target adapter object
# @param[in]    panel Panel
# @return       True if DMRRS enable in VBT, False otherwise
def is_enabled_in_vbt(adapter: Adapter, panel: Panel):
    # Check Default VBT configuration first.
    gfx_vbt = vbt.Vbt(adapter.gfx_index)

    # Skip VBT check for unsupported VBT version
    if gfx_vbt.version < 228:
        logging.info("\tDMRRS option is not present in VBT version < 228")
        return False

    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
    logging.debug(f"\tPanel Index for {panel.port}= {panel_index}")

    if (gfx_vbt.block_44.DmrrsEnable[0] & (1 << panel_index)) != (1 << panel_index):
        logging.warning(f"\tDMRRS is not enabled in VBT for {panel.port}")
        return False
    logging.info(f"\tDMRRS is enabled in VBT for {panel.port}")
    return True


##
# @brief        Exposed API to enable/disable DMRRS for any panel in VBT
# @param[in]    adapter Adapter
# @param[in]    panel Panel
# @param[in]    enable_dmrrs bool
# @return       status bool
def set_dmrrs_in_vbt(adapter: Adapter, panel: Panel, enable_dmrrs: bool) -> bool:
    expected_value = 1 if enable_dmrrs else 0

    gfx_vbt = vbt.Vbt(adapter.gfx_index)

    # Skip VBT update for unsupported VBT version
    if gfx_vbt.version < 228 or panel.is_lfp is False:
        logging.info("\tDMRRS option is not present in VBT version < 228")
        return True

    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)

    logging.info(f"\tPanel Index for {panel.port}= {panel_index}")
    logging.debug(f"VBT block44 DMRRSEnable before changing:  {gfx_vbt.block_44.DmrrsEnable[0]}")

    if (gfx_vbt.block_44.DmrrsEnable[0] & (1 << panel_index)) == expected_value:
        logging.info(f"\tPASS: DMRRS is already {'enabled' if enable_dmrrs else 'disabled'} in VBT for {panel.port}")
        return True

    if enable_dmrrs:
        gfx_vbt.block_44.DmrrsEnable[0] |= (1 << panel_index)
    else:
        gfx_vbt.block_44.DmrrsEnable[0] &= ~(1 << panel_index)

    if gfx_vbt.apply_changes() is False:
        logging.error("\tFailed to apply changes to VBT")
        return False

    logging.info(f"VBT block44 DMRRSEnable after applying changes: {gfx_vbt.block_44.DmrrsEnable[0]}")

    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("\tFailed to restart display driver after VBT update")
        return False
    logging.info("Driver restarted successfully")

    gfx_vbt.reload(adapter.gfx_index)
    logging.info("Reloaded VBT context and verifying applied VBT block44 DMRRSEnable value")
    if enable_dmrrs:
        if (gfx_vbt.block_44.DmrrsEnable[0] & (1 << panel_index)) != (1 << panel_index):
            logging.error(f"\tFailed to enable DMRRS in VBT on {panel.port}")
            return False
    else:
        if (gfx_vbt.block_44.DmrrsEnable[0] & (1 << panel_index)) != 0:
            logging.error(f"\tFailed to disable DMRRS in VBT {panel.port}")
            return False
    logging.info(f"\tPASS: {'Enabled' if enable_dmrrs else 'Disabled'} DMRRS in VBT successfully {panel.port}")
    return True


##
# @brief        Exposed API to check if there a RR change due to DMRRS
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @param[in]    etl_path string, path to ETL file
# @param[in]    media_fps float, fps of the media
# @return       status bool True if rr changed due to DMRRS, False otherwise
def is_dmrrs_changing_rr(adapter: Adapter, panel: Panel, etl_path: str, media_fps: float) -> bool:
    logging.info(f"\tGenerating EtlParser Report for {etl_path}")
    if etl_parser.generate_report(etl_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        return False
    logging.info("\tSuccessfully generated ETL Parser report")
    rr_timestamp_list = []
    timing_offsets = adapter.regs.get_timing_offsets(panel.transcoder_type)

    if panel.lrr_caps.rr_switching_method == RrSwitchingMethod.CLOCK:
        logging.info("Checking LinkM changes")
        mmio_output = etl_parser.get_mmio_data(timing_offsets.LinkM, is_write=True)
        if mmio_output is None:
            logging.warning("No LinkM change found in ETL")
            return False
        for link_m_value in mmio_output:
            timing_info = adapter.regs.get_timing_info(panel.transcoder_type,
                                                       TimingOffsetValues(LinkM=link_m_value.Data))
            rr_timestamp_list.append((drrs.link_m_to_hz(adapter, panel, timing_info.LinkM), link_m_value.TimeStamp))

    if panel.lrr_caps.rr_switching_method in [RrSwitchingMethod.VTOTAL_SW, RrSwitchingMethod.VTOTAL_HW]:
        logging.info("Checking VrrVmax/VrrDcbVmax changes")
        timing_info = adapter.regs.get_timing_info(panel.transcoder_type)
        h_total = timing_info.HTotal
        if panel.mso_caps.is_mso_supported:
            logging.info(f"This panel is MSO supported so multiplying HTotal with number of segments"
                         f" {panel.mso_caps.no_of_segments}")
            h_total = panel.mso_caps.no_of_segments * h_total
        vrr_offsets = adapter.regs.get_vrr_offsets(panel.transcoder_type)
        if adapter.name in common.GEN_16_PLATFORMS and panel.panel_type == "DP":
            mmio_output = etl_parser.get_mmio_data(vrr_offsets.VrrDcbVmaxReg, is_write=True)
            logging.debug(f"MMIO Output for VrrDcbVmaxReg - {mmio_output}")
        else:
            mmio_output = etl_parser.get_mmio_data(vrr_offsets.VrrVmaxReg, is_write=True)
            logging.debug(f"MMIO Output for VrrVmaxReg - {mmio_output}")
        if mmio_output is None:
            logging.warning("No VrrVmax/VrrDcbVmax change found in ETL")
            return False
        for mmio_data in mmio_output:
            vrr_info = adapter.regs.get_vrr_info(panel.transcoder_type, VrrOffsetValues(VrrVmaxReg=mmio_data.Data))
            if adapter.name in common.GEN_16_PLATFORMS and panel.panel_type == "DP":
                rr = round(float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (vrr_info.VrrDcbVmax + 1)), 3)
                logging.info(f"RR - {rr}, VrrDcbVmax - {vrr_info.VrrDcbVmax}")
            else:
                rr = round(float(panel.native_mode.pixelClock_Hz) / ((h_total + 1) * (vrr_info.VrrVmax + 1)), 3)
                logging.info(f"RR - {rr}, VrrVmax - {vrr_info.VrrVmax}")
            rr_timestamp_list.append((rr, mmio_data.TimeStamp))

    logging.debug(f"RR Timestamp list: {rr_timestamp_list}")

    for rr, timestamp in rr_timestamp_list:
        if (panel.drrs_caps.max_rr - 0.05) <= rr <= (panel.drrs_caps.max_rr + 0.5):
            # DMRRS will not kick in if multiple of the media_fps == max_rr
            continue
        # RR not expected to be found in ETL:
        #   1. Multiple of media_fps
        #   2. not in actual panel rr range(min-max)
        media_fps_multiples = []
        for i in range(1, 6):
            if panel.drrs_caps.min_rr <= (media_fps * i) <= min(60, panel.drrs_caps.max_rr):
                media_fps_multiples.append(media_fps * i)
        logging.info(f"Media fps not expected in ETL : {media_fps_multiples}")

        for fps in media_fps_multiples:
            if (fps - 0.05) < rr < (fps + 0.05):
                # If that is near to the multiple of the media_fps
                #   Check if the most recent DDIInterrupt call is enable
                #       if yes, return True else continue
                interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                               etl_parser.InterruptType.CRTC_VSYNC,
                                                               end_timestamp=timestamp)
                if interrupt_data is None:
                    continue
                if interrupt_data[-1].CrtVsyncState in [etl_parser.CrtcVsyncState.ENABLE,
                                                        etl_parser.CrtcVsyncState.DISABLE_KEEP_PHASE]:
                    logging.error(f"RR switch(DMRRS way) after VSync Enable Not Expected")
                    return True
    return False


##
# @brief        Exposed API to check if is a flip with non-zero duration is present in the ETL
# @param[in]    panel object, Panel
# @param[in]    etl_path string, path to ETL file
# @return       True if non-zero duration is present in the ETL, False otherwise
def is_non_zero_duration_flip_present(panel: Panel, etl_path) -> bool:
    # Generate ETL report
    if etl_parser.generate_report(etl_path, ETL_PARSER_CONFIG) is False:
        logging.error("Failed to generate ETL report")
        return False
    logging.info("ETL report is generated successfully")

    # Get the flip data and check if the flip has a duration
    flip_data = etl_parser.get_flip_data('PIPE_' + panel.pipe)
    if flip_data is None:
        logging.warning(f"\tNo flip data found for PIPE_{panel.pipe}")
        return False

    logging.info(f"\tIncoming flips on PIPE_{panel.pipe}: {len(flip_data)}")
    for flip in flip_data:
        # Skip the flips with plane disable call, these flips might have unexpected data.
        is_plane_disable_call = False
        for plane_info in flip.PlaneInfoList:
            if plane_info.Flags == "":
                is_plane_disable_call = True
                logging.info("\tSkipping: Flip found with plane disable call (it might have unexpected data)")
                break
        if is_plane_disable_call:
            logging.debug(f"\tSkipped plane disable flip for duration calculation")
            logging.debug(f"\t\t{flip}")
            continue

        if flip.Duration != 0 and flip.Duration != VBLANK_MAX_DURATION:
            logging.error(f"Non-zero duration flip found at {flip.TimeStamp}")
            return True
    logging.info(f"No non-zero duration flips found for {panel.port}")
    return False


##
# @brief        Exposed API to check if the current mode is Dynamic Refresh Rate mode
# @param[in]    panel object, Panel
# @return       True, if current mode is Dynamic refresh rate mode, False otherwise
def is_dynamic_mode_enabled(panel: Panel):
    display_config_ = display_config.DisplayConfiguration()
    current_mode = display_config_.get_current_mode(panel.target_id)
    if current_mode.rrMode == 1:
        return True
    return False


##
# @brief        Exposed API to check with and without always VRR
# @param[in]    adapter object, Adapter
# @param[in]    panel object, Panel
# @return       True, if check is passed else, False
def check_always_vrr(adapter, panel):
    html.step_start(f"Verifying Always VRR behaviour for {panel.port}")
    # get duration regions (zero duration and non zero durations in ETL)
    duration_regions = get_flip_duration_regions(panel.pipe)
    if duration_regions is None:
        logging.warning("\tNo duration region found")
        html.step_end()
        return True
    zero_duration_regions = duration_regions[0] if 0 in duration_regions.keys() else None
    if zero_duration_regions is None:
        logging.warning("\tNo zero duration region found")
        html.step_end()
        return True

    vrr_regs = adapter.regs.get_vrr_offsets(panel.transcoder_type)
    status = True
    interrupt_data = etl_parser.get_interrupt_data(etl_parser.Ddi.DDI_CONTROLINTERRUPT2,
                                                   etl_parser.InterruptType.CRTC_VSYNC)
    if interrupt_data is None:
        logging.warning("\tInterrupt data not found")
        html.step_end()
        return status

    expect_always_vrr = panel.vrr_caps.is_always_vrr_mode | panel.vrr_caps.is_always_vrr_mode_on_non_vrr_panel
    for start_time, end_time in zero_duration_regions:
        skip_current_iteration = False
        # Even though always VRR is not expected, there could be VRR programming due to ControlInterrupt2
        if expect_always_vrr is False:
            # if VSYNC disable call came between start_time & end_time, then skip further verification
            for interrupt in interrupt_data:
                if interrupt.CrtVsyncState in [etl_parser.CrtcVsyncState.DISABLE_NO_PHASE]:
                    if start_time <= interrupt.TimeStamp <= end_time:
                        logging.info(f"Skip always VRR verification for panel from [{start_time} - {end_time}] ms")
                        skip_current_iteration = True
                        break

        if skip_current_iteration:
            continue

        vrr_enabled = False
        # Check mmio-data for VRR_CTL for each zero duration region
        vrr_ctl_data = etl_parser.get_mmio_data(vrr_regs.VrrControl, start_time=start_time + 0.2, end_time=end_time)
        if vrr_ctl_data is None:
            logging.warning("No mmio data found for VRR_CTL")
            vrr_enabled = expect_always_vrr
        else:
            logging.debug(f"VRR_CTL_{panel.transcoder} Data from [{start_time} - {end_time}]= {vrr_ctl_data}")
            for mmio_data in vrr_ctl_data:
                vrr_ctl_info = adapter.regs.get_vrr_info(panel.transcoder_type,
                                                         VrrOffsetValues(VrrControl=mmio_data.Data))
                logging.info(f"VRR CTL {hex(mmio_data.Offset)}= {hex(mmio_data.Data)} at {mmio_data.TimeStamp} ms")
                vrr_enabled = vrr_ctl_info.VrrEnable
                logging_message = f"\tVRR CTL 31st bit Expected= {int(expect_always_vrr)}, Actual= {int(vrr_enabled)}"
                if (expect_always_vrr and vrr_enabled) or (expect_always_vrr is False and vrr_enabled is False):
                    logging.info(logging_message)
                else:
                    logging.error(logging_message)

        if expect_always_vrr ^ vrr_enabled:
            status = False
    html.step_end()
    return status


##
# @brief        Exposed API to get zero and non-zero duration regions
# @param[in]    pipe Object, pipe
# @param[in]    start_time int, start time of the etl
# @param[in]    end_time int, end time of the etl
# @return       duration_regions, dictionary, {duration: (start, end)}
def get_flip_duration_regions(pipe, start_time=None, end_time=None):
    flip_data = etl_parser.get_flip_data('PIPE_' + pipe, start_time=start_time, end_time=end_time)
    if flip_data is None:
        logging.warning(f"\tNo flip data found for PIPE_{pipe}")
        return None

    # Get the start and end time of flips with duration.
    duration_regions = {}  # Dictionary to contain the start and end time of regions with non-zero duration flips
    previous_flip = None
    same_flip = None
    for flip in flip_data:
        # Skip the flips with plane disable call, these flips might have unexpected data.
        is_plane_disable_call = False
        for plane_info in flip.PlaneInfoList:
            if plane_info.Flags == "":
                is_plane_disable_call = True
                break

        if is_plane_disable_call:
            logging.debug(f"\tSkipped plane disable flip for duration calculation")
            logging.debug(f"\t{flip}")
            continue

        if flip.Duration is not None:
            # Whenever a changed duration is found add it to the list
            # List format = {duration1: [(start1, end1), (start2, end2),...], duration2 = [(start1, end1),...]}
            if flip.Duration not in duration_regions.keys():
                duration_regions[flip.Duration] = []

            # If previous flip is None
            if previous_flip is None:
                previous_flip = flip
                if start_time is None:
                    logging.info(f"Flip Duration(first entry)= {flip.Duration}, [Start - {flip.TimeStamp}]")
                    duration_regions[flip.Duration].append((0, flip.TimeStamp))
                else:
                    start_time = start_time if start_time < flip.TimeStamp else flip.TimeStamp
                    logging.info(f"Flip Duration(first entry)= {flip.Duration}, [{start_time} - {flip.TimeStamp}]")
                    duration_regions[flip.Duration].append((start_time, flip.TimeStamp))

            if previous_flip.Duration == flip.Duration:
                same_flip = flip
                continue
            if same_flip is None:
                logging.info(
                    f"Flip Duration: {previous_flip.Duration}, [{previous_flip.TimeStamp} - {previous_flip.TimeStamp}]")
                duration_regions[previous_flip.Duration].append((previous_flip.TimeStamp, previous_flip.TimeStamp))
            else:
                logging.info(
                    f"Flip Duration: {previous_flip.Duration}, [{previous_flip.TimeStamp} - {same_flip.TimeStamp}]")
                duration_regions[previous_flip.Duration].append((previous_flip.TimeStamp, same_flip.TimeStamp))
            previous_flip = flip

    if end_time is None:
        # Add last flip to the duration region
        logging.info(f"Flip Duration(last entry): {previous_flip.Duration}, [{previous_flip.TimeStamp} - END]")
        duration_regions[previous_flip.Duration].append((previous_flip.TimeStamp, sys.maxsize))
    else:
        # Add last flip to the duration region
        logging.info(f"Flip Duration(last entry): {previous_flip.Duration}, [{previous_flip.TimeStamp} - {end_time}]")
        duration_regions[previous_flip.Duration].append((previous_flip.TimeStamp, end_time))
    logging.info(f"Duration Regions: {duration_regions}")
    return duration_regions


##
# @brief        Exposed API to check VBI during VSYNC_DISABLE call
# @param[in]    panel Object, panel
# @return       duration_regions, dictionary, {duration: (start, end)}
def check_no_vbi_during_vsync_disable(panel):
    html.step_start("Verifying VBI during VSYNC_DISABLE call")
    _, vsync_disabled = drrs.get_vsync_enable_disable_regions(etl_parser.Ddi.DDI_CONTROLINTERRUPT2)
    logging.debug(f"Vsync Disable Regions= {vsync_disabled}")
    if vsync_disabled is None:
        logging.warning("No Vsync Disabled region found, VBI check not required")
        return True
    status = True
    for vsync_disabled_start, vsync_disabled_end in vsync_disabled:
        logging.info(f"Checking VBI during Vsync disabled call from {vsync_disabled_start} - {vsync_disabled_end}")
        vbi_data = etl_parser.get_vbi_data(panel.pipe, start_time=vsync_disabled_start, end_time=vsync_disabled_end)
        if vbi_data is None:
            logging.info(f"VBI data not found during VSYNC_DISABLE call")
        else:
            status = False
            logging.error(f"FAIL: VBI data found during VSYNC_DISABLE call (Unexpected)")
    if status is False:
        gdhm.report_driver_bug_os("[OS_FEATURES] VBI data found during VSYNC_DISABLE")
    html.step_end()
    return status


def __verify_check_present_duration(panel: Panel, media_fps):
    status = True
    html.step_start("Verifying GfxCheckPresentDurationSupport data")
    check_present_duration_output = etl_parser.get_event_data(etl_parser.Events.CHECK_PRESENT_DURATION_SUPPORT)
    if check_present_duration_output is None:
        # Check Present Duration is expected on Non-BFR panels (Clock based panel + VRR panels without BFR support)
        # There is no CheckPresentDuration when the media fps is 59.940fps on non-BFR panels
        # @todo as per HSD-18018642354, it is not concluded to expect non-zero on 59.940 video playback hence keeping
        #          the check "(media_fps != 59.940)" in the below condition. It can be removed if MSFT agrees to send
        #           non-zero duration for 59.940fps Video playback.
        if (panel.bfr_caps.is_bfr_supported is False) and (media_fps != MediaFps.FPS_59_940):
            logging.error("\tNo data found for GfxCheckPresentDurationSupport on Non-BFR panel")
            gdhm.report_driver_bug_os("[OsFeatures][DMRRS] No data found for GfxCheckPresentDurationSupport on "
                                      "Non-BFR panel")
            status &= False
    else:
        # Fail if CheckPresentDuration entries are found on BFR supported panel
        if panel.bfr_caps.is_bfr_supported:
            logging.error(f"\tCheckPresentDuration DDI is not expected on a BFR supported panel")
            gdhm.report_driver_bug_os("[OsFeatures][DMRRS] GfxCheckPresentDurationSupport DDI found on BFR "
                                      "supported panel")
            status &= False
        for event_data in check_present_duration_output:
            if event_data.IsDataProvided is False:
                logging.error(f"\t{event_data}")
                logging.error("\tUnserviced GfxCheckPresentDurationSupport call found")
                gdhm.report_driver_bug_os("[OsFeatures][DMRRS] Unserviced GfxCheckPresentDurationSupport call found")
            else:
                requested_duration = None
                if event_data.DesiredPresentDuration is not None:
                    requested_duration = common.duration_to_hz(event_data.DesiredPresentDuration)
                supported_duration_smaller = None
                if event_data.ClosestSmallerDuration is not None:
                    supported_duration_smaller = common.duration_to_hz(event_data.ClosestSmallerDuration)
                supported_duration_larger = None
                if event_data.ClosestLargerDuration is not None:
                    supported_duration_larger = common.duration_to_hz(event_data.ClosestLargerDuration)

                logging.info("\tTimeStamp= {0}: Requested RR= {1}, Reported RR Range({2}, {3})".format(
                    event_data.TimeStamp, requested_duration, supported_duration_larger, supported_duration_smaller))
    html.step_end()
    return status


##
# @brief        Exposed API to verify DMRRS behavior in Min RR of the panel
# @param[in]    adapter Object, Adapter
# @param[in]    panel Object, panel
# @param[in]    etl_path string, path to ETL file
# @return       duration_regions, dictionary, {duration: (start, end)}
def verify_dmrrs_with_min_rr(adapter: Adapter, panel: Panel, etl_path: str):
    html.step_start(f"Verifying duration flips for {panel.port} in Min RR")
    # Till Cobalt OS, MPO3 flips with 0 duration will be received in Min RR of the panel
    if dut.WIN_OS_VERSION < dut.WinOsVersion.WIN_NICKEL:
        if is_non_zero_duration_flip_present(panel, etl_path) is False:
            logging.info(f"\tNon-zero duration flip is NOT present with Min RR for {panel.port}")
            html.step_end()
            return True
        logging.error(f"\tNon-zero duration flip present with Min RR for {panel.port}")
        gdhm.report_driver_bug_os("[OsFeatures][DMRRS] Non-zero duration flip present in Min RR")
        html.step_end()
        return False

    # From Nickel OS, MPO3 flips can be received as per Min RR of the panel
    logging.info(f"\tGenerating EtlParser Report for {etl_path}")
    if etl_parser.generate_report(etl_path, ETL_PARSER_CONFIG) is False:
        logging.error("\tFAILED to generate ETL Parser report")
        html.step_end()
        return False
    logging.info("\tSuccessfully generated ETL Parser report")

    non_zero_duration_region = get_flip_duration_regions(panel.pipe)
    if bool(non_zero_duration_region) is False:
        gdhm.report_driver_bug_os("[OsFeatures][DMRRS] No duration flips found during VPB in Min RR")
        logging.error(f"NO duration Flips found during VPB for {panel.pipe}")
        html.step_end()
        return False

    status = True
    for duration, region in non_zero_duration_region.items():
        duration = common.duration_to_hz(duration)
        title = f"{duration}Hz flips found during {region} when mode RR is {panel.drrs_caps.min_rr}"
        if duration in [0, panel.drrs_caps.min_rr, panel.drrs_caps.min_rr*1000/1001]:
            logging.info(f"\t{title} (Expected)")
        else:
            logging.error(f"\t{title} (Unexpected)")

    html.step_start(f"Verifying No RR change happened for {panel.port} in Min RR")
    rr_change_status = drrs.is_rr_changing(adapter, panel, etl_path)
    if rr_change_status is None:
        logging.error("\tETL report generation FAILED")
        status = False
    elif rr_change_status is False:
        logging.info("\tRefresh rate is NOT changing during workload")
    else:
        gdhm.report_driver_bug_os("[OsFeatures][DMRRS] Refresh rate is changing in Min RR")
        logging.error("\tRefresh rate is changing during workload")
        status = False

    html.step_end()
    return status
