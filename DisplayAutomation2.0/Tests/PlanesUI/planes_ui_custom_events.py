########################################################################################################################
# @file         planes_ui_custom_events.py
# @brief        Test for Planes UI tests to have required feature verification during
#               custom events of Video/ Game scenarios
#
# @author       Ashish Tripathi
########################################################################################################################
import logging
import time
import math
import unittest

from Libs.Core import display_essential, enum, registry_access
import Libs.Core.flip as flip
from Libs.Core.display_power import DisplayPower, PowerEvent
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_environment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.PlanesUI.Common import planes_ui_helper, planes_ui_verification
from Tests.PlanesUI.planes_ui_base import PlanesUIBase
from Tests.PowerCons.Functional.DMRRS import dmrrs, hrr
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import dpcd, common, dut, workload


##
# @brief        This class contains test cases for Custom Events of Video/Game Scenarios
class PlanesUiCustomEvents(PlanesUIBase):
    flipq = flip.MPO()

    ##
    # @brief        This class method is the entry point for current PlanesUI test case. Helps to initialize few of
    #               the parameters required for test execution.
    # @return       None
    def setUp(self):
        super(PlanesUiCustomEvents, self).setUp()
        available_videos = [member.name for member in workload.VideoFile]
        assert self.media_type in available_videos, f"{self.media_type} video is invalid/ unavailable"
        self.video_path = str(workload.VideoFile[self.media_type].value)
        self.media_fps = float(self.fps)
        dut.prepare()
        # disable PSR if panel is not supporting 314 DCPD value
        for adapter in dut.adapters.values():
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                continue
            for panel in adapter.panels.values():
                caps = dpcd.LrrUbrrCaps(panel.target_id)
                if caps.source_v_total_based:
                    continue
                else:
                    logging.info(f"Disabling PSR on {adapter.name} due to 314 DPCD not supported")
                    psr_status = psr.disable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                    if psr_status is False:
                        self.fail(f"FAILED to disable PSR on {adapter.name}")
                    logging.info(f"Disabled PSR on {adapter.name}")

        for adapter in dut.adapters.values():
            # refreshing panel caps as we have update pane caps above.
            dut.refresh_panel_caps(adapter)
            for panel in adapter.panels.values():
                logging.info("\t{0}".format(panel))
                logging.info("\t\t{0}".format(panel.psr_caps))
                logging.info("\t\t{0}".format(panel.drrs_caps))
                logging.info("\t\t{0}".format(panel.vrr_caps))
                logging.info("\t\t{0}".format(panel.lrr_caps))
                logging.info("\t\t{0}".format(panel.bfr_caps))

        status, etl = workload.etl_tracer_stop_existing_and_start_new("BeforeTestStart")
        if status:
            for adapter in dut.adapters.values():
                # In cases where FlipQ is enabled by the OS, we can disable the OS FlipQ using registry key. This
                # will continue HRR verification without any issue
                if planes_ui_verification.os_flipq_status_in_os_ftr_table(etl) is True:
                    self.flipq.enable_disble_os_flipq(True, adapter.gfx_index)
                hrr.enable(adapter)
                dut.refresh_panel_caps(adapter)

                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    logging.error("Failed to disable-enable display driver")
                    return False

    ##
    # @brief        This class method is the exit point for current PlanesUI test case. Helps to reset few of the
    #               parameters to default to avoid any disruption in test execution.
    # @return       None
    def tearDown(self):
        super(PlanesUiCustomEvents, self).tearDown()
        # disable PSR if panel is not supporting 314 DCPD value
        for adapter in dut.adapters.values():
            if adapter.name in common.PRE_GEN_14_PLATFORMS:
                continue
            for panel in adapter.panels.values():
                caps = dpcd.LrrUbrrCaps(panel.target_id)
                if caps.source_v_total_based:
                    continue
                else:
                    logging.info(f"Enabling PSR on {adapter.name} due to 314 DPCD not supported")
                    psr_status = psr.enable(adapter.gfx_index, psr.UserRequestedFeature.PSR_1)
                    if psr_status is False:
                        logging.error(f"FAILED to disable PSR on {adapter.name}")
                    logging.info(f"Enabled PSR on {adapter.name}")
        for adapter in dut.adapters.values():
            self.flipq.enable_disble_os_flipq(False, adapter.gfx_index)
            hrr.disable(adapter)
            dut.refresh_panel_caps(adapter)
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                logging.error("Failed to disable-enable display driver")
                return False
        dut.reset()

    ##
    # @brief        This function verifies feature with S3 power event
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'PAUSE_VIDEO_S3_PLAY_VIDEO',
                     "Skipping the test step as the scenario type is not PAUSE_VIDEO_S3_PLAY_VIDEO")
    # @endcond
    def t_11_pause_video_s3_play_video(self):
        if DisplayPower().is_power_state_supported(PowerEvent.S3) is False:
            self.fail("Test needs S3 supported system, but it is NOT S3 supported (Planning Issue)")
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> pause video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, self.media_fps, 30, True, True, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, True)
                if self.feature == "FLIPQ_HRR":
                    test_status &= planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                                   platform=adapter.name)

                if invoke_power_event(PowerEvent.S3) is False:
                    self.fail("FAILED to invoke power event(S3)")

                # breather
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> close the video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, True, self.fps, 30, False, False, True]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, False)
                if self.feature == "FLIPQ_HRR":
                    test_status &= planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                                   platform=adapter.name)
        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWER_EVENT_S3")
        logging.info(f"PASS: Feature verification with POWER_EVENT_S3")

    ##
    # @brief        This function verifies feature with CS power event
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'PAUSE_VIDEO_CS_PLAY_VIDEO',
                     "Skipping the test step as the scenario type is not PAUSE_VIDEO_CS_PLAY_VIDEO")
    # @endcond
    def t_12_pause_video_cs_play_video(self):
        test_status = True
        if DisplayPower().is_power_state_supported(PowerEvent.CS) is False:
            self.fail("Test needs CS supported system, but it is NOT CS supported (Planning Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> pause video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, self.media_fps, 30, True, True, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, True)
                if self.feature == "FLIPQ_HRR":
                    test_status &= planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                                   platform=adapter.name)

                if invoke_power_event(PowerEvent.CS) is False:
                    self.fail("FAILED to invoke power event(CS)")

                # breather
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> close the video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, True, self.fps, 30, False, False, True]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, False)
                if self.feature == "FLIPQ_HRR":
                    test_status &= planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                                   platform=adapter.name)
        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWER_EVENT_CS")
        logging.info(f"PASS: Feature verification with POWER_EVENT_CS")

    ##
    # @brief        This function verifies feature with S4 power event
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'PAUSE_VIDEO_S4_PLAY_VIDEO',
                     "Skipping the test step as the scenario type is not PAUSE_VIDEO_S4_PLAY_VIDEO")
    # @endcond
    def t_13_pause_video_s4_play_video(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> pause video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, self.media_fps, 30, True, True, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, True)
                if self.feature == "FLIPQ_HRR":
                    test_status &= planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                                   platform=adapter.name)

                if invoke_power_event(PowerEvent.S4) is False:
                    self.fail("FAILED to invoke power event(S4)")

                # breather
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> close the video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, True, self.fps, 30, False, False, True]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, False)
                if self.feature == "FLIPQ_HRR":
                    test_status &= planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                                   platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWER_EVENT_S4")
        logging.info(f"PASS: Feature verification with POWER_EVENT_S4")

    ##
    # @brief        This function verifies feature with POWERLINE AC/DC during WORKLOAD
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'AC_DC',
                     "Skipping the test step as the scenario type is not AC_DC")
    # @endcond
    def t_14_toggle_ac_dc(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds-> stop tracer-> pause video
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInDcMode"),
                        workload.Video(workload.Video.PAUSE),

                        # Switch to AC mode
                        workload.SwitchPowerSource(workload.SwitchPowerSource.AC),
                        workload.Wait(delay=5),

                        # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> pause video
                        workload.Video(workload.Video.UN_PAUSE),
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInAcMode"),
                        workload.Video(workload.Video.PAUSE),

                        # Switch to DC mode
                        workload.SwitchPowerSource(workload.SwitchPowerSource.DC),
                        workload.Wait(delay=5),

                        # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> pause video
                        workload.Video(workload.Video.UN_PAUSE),
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInDcMode"),
                        workload.Video(workload.Video.PAUSE),

                        # Switch to AC mode
                        workload.SwitchPowerSource(workload.SwitchPowerSource.AC),
                        workload.Wait(delay=5),

                        # unpause existing video-> start tracer-> play 30 seconds-> close video -> stop tracer
                        workload.Video(workload.Video.UN_PAUSE),
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInAcMode")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWERLINE Scenario AC/DC Switch")
        logging.info(f"PASS: Feature verification with POWERLINE Scenario AC/DC Switch")

    ##
    # @brief        This function verifies feature with MIN_RR/MAX_RR change during Video Playback
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'RR_MAX_MIN_MAX',
                     "Skipping the test step as the scenario type is not RR_MAX_MIN_MAX")
    # @endcond
    def t_15_video_rr_change(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds-> stop tracer-> keep the video playing
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Video(workload.Video.ENABLE_LOOP_VIDEO),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInMaxRr"),

                        # Min RR
                        workload.Mode(workload.Mode.REFRESH_RATE_MIN, adapter, panel),

                        # start tracer-> video already playing-> play 30 seconds-> stop tracer-> keep the video playing
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInMinRr"),

                        # Max RR
                        workload.Mode(workload.Mode.REFRESH_RATE_MAX, adapter, panel),

                        # let video play after RR switch as OS will not start non-zero duration immediately
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInMaxRr")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for adapter in dut.adapters.values():
                    for panel in adapter.panels.values():
                        for etl in etl_files[workload.Etl.STOP]:
                            if "WorkloadTraceInMinRr" in etl:
                                if dmrrs.is_dmrrs_changing_rr(adapter, panel, etl, self.media_fps) is True:
                                    test_status = False

                            else:
                                test_status &= hrr.verify(adapter, panel, etl, self.media_fps)
                            if self.feature == "FLIPQ_HRR":
                                test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe,
                                                                               panel.target_id,
                                                                               platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with Scenario RR_MAX_MIN_MAX Change")
        logging.info(f"PASS: Feature verification with Scenario RR_MAX_MIN_MAX Change")

    ##
    # @brief        This function verifies feature with Window toggle during Video Playback
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'FULLSCREEN_WINDOWED_FULLSCREEN',
                     "Skipping the test step as the scenario type is not FULLSCREEN_WINDOWED_FULLSCREEN")
    # @endcond
    def t_16_video_window_toggle(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds-> stop tracer-> pause video
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInFullscreenMode"),

                        # Switch to Windowed mode
                        workload.Video(workload.Video.SWITCH_TO_WINDOWED_MODE),

                        # start tracer-> play 30 seconds-> stop tracer-> pause video
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInWindowedMode"),

                        # Switch to Fullscreen mode
                        workload.Video(workload.Video.SWITCH_TO_FULLSCREEN_MODE),

                        # start tracer-> play 30 seconds-> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceInFullscreenMode")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    if "WorkloadTraceInFullscreenMode" in etl:
                        test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    else:
                        rr_change_status = drrs.is_rr_changing(adapter, panel, etl)
                        if rr_change_status is None:
                            logging.error("\tETL report generation FAILED")
                            test_status = False
                        elif rr_change_status is False:
                            logging.info("\tRefresh rate is NOT changing during Windowed Mode Video Playback")
                        else:
                            error_msg = "Refresh rate is changing during Windowed VPB"
                            gdhm.report_driver_bug_pc(f"[PowerCons][DMRRS] {error_msg}")
                            logging.error(f"\t{error_msg}")
                            test_status = False
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail("FAIL: Feature verification with VPB FULLSCREEN_WINDOWED_FULLSCREEN")
        logging.info("PASS: Feature verification with VPB FULLSCREEN_WINDOWED_FULLSCREEN")

    ##
    # @brief        This function verifies feature with Switching between Video and game workload
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_GAME_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_GAME_VIDEO")
    # @endcond
    def t_17_video_game_video(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds-> stop tracer-> close video
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbBeforeGame"),

                        # Close any pop up notification before opening the app
                        # Pressing WIN+A twice will open and close the notification center, which will close all notification toasts
                        workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_A),
                        workload.Wait(delay=1),
                        workload.KeyBoardPress(keyboard_action=workload.KeyBoardPress.WIN_A),
                        workload.Wait(delay=1),

                        workload.Etl(workload.Etl.START),
                        workload.Game(workload.Game.LAUNCH_IN_FULLSCREEN, workload.Apps.FlipAt),
                        workload.KeyBoardPress(workload.KeyBoardPress.ALT_TAB),
                        workload.Wait(delay=15),
                        workload.Game(workload.Game.CLOSE, self.app),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceDuringGamePlayback"),

                        # start tracer-> play 30 seconds-> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.KeyBoardPress(workload.KeyBoardPress.ALT_TAB),
                        workload.Video(workload.Video.UN_PAUSE),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterGame"),
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    if "WorkloadTraceDuringGamePlayback" in etl:
                        continue
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWERLINE Scenario VIDEO_GAME_VIDEO")
        logging.info(f"PASS: Feature verification with POWERLINE Scenario VIDEO_GAME_VIDEO")

    ##
    # @brief        This function verifies feature with S3 power event
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_S3_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_S3_VIDEO")
    # @endcond
    def t_18_video_s3_video(self):
        if DisplayPower().is_power_state_supported(PowerEvent.S3) is False:
            self.fail("Test needs S3 supported system, but it is NOT S3 supported (Planning Issue)")
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds-> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbBeforeS3"),

                        # Invoke S3
                        workload.InvokePowerEvent(workload.InvokePowerEvent.S3),

                        # start tracer-> play 30 seconds-> close video-> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterS3")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWER_EVENT_S3")
        logging.info(f"PASS: Feature verification with POWER_EVENT_S3")

    ##
    # @brief        This function verifies feature with CS power event
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_CS_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_CS_VIDEO")
    # @endcond
    def t_19_video_cs_video(self):
        test_status = True
        if DisplayPower().is_power_state_supported(PowerEvent.CS) is False:
            self.fail("Test needs CS supported system, but it is NOT CS supported (Planning Issue)")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds-> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbBeforeCS"),

                        # Invoke CS
                        workload.InvokePowerEvent(workload.InvokePowerEvent.CS),

                        # start tracer-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterCS")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWER_EVENT_CS")
        logging.info(f"PASS: Feature verification with POWER_EVENT_CS")

    ##
    # @brief        This function verifies feature with S4 power event
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_S4_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_S4_VIDEO")
    # @endcond
    def t_20_video_s4_video(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbBeforeS4"),

                        # Invoke S4
                        workload.InvokePowerEvent(workload.InvokePowerEvent.S4),

                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterS4")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWER_EVENT_S4")
        logging.info(f"PASS: Feature verification with POWER_EVENT_S4")

    ##
    # @brief        This function verifies feature with video play pause play
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_PLAY_PAUSE_PLAY',
                     "Skipping the test step as the scenario type is not VIDEO_PLAY_PAUSE_PLAY")
    # @endcond
    def t_21_video_play_pause_play(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds-> stop tracer-> Pause Video
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbBeforePause"),
                        workload.Video(workload.Video.PAUSE),

                        # wait for 10 sec after pause video
                        workload.Wait(delay=10),

                        # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> pause video
                        workload.Video(workload.Video.UN_PAUSE),
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterUnpause")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with VIDEO_PLAY_PAUSE_PLAY")
        logging.info(f"PASS: Feature verification with VIDEO_PLAY_PAUSE_PLAY")

    ##
    # @brief        This function verifies feature with VPB minimized maximized
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_MINIMIZED_MAXIMIZED',
                     "Skipping the test step as the scenario type is not VIDEO_MINIMIZED_MAXIMIZED")
    # @endcond
    def t_22_video_minmized_maximized(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbBeforeMinimize"),

                        # Minimize video playback window
                        workload.KeyBoardPress(workload.KeyBoardPress.WIN_D),

                        # Wait for 10 seconds after minimize
                        workload.Wait(delay=10),

                        # Maximize video playback window
                        workload.KeyBoardPress(workload.KeyBoardPress.WIN_D),

                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterMaximized")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with VPB Minimize_Maximize")
        logging.info(f"PASS: Feature verification with VPB Minimize_Maximize")

    ##
    # @brief        This function verifies feature with Rotation
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_ROTATION_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_ROTATION_VIDEO")
    # @endcond
    def t_23_video_rotation_video(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbBefore90Rotation"),

                        # Invoke Rotation to 90
                        workload.Mode(action=workload.Mode.ROTATE_SCREEN_TO_90, adapter=adapter, panel=panel),

                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfter90Rotation"),

                        # Invoke Rotation to 180
                        workload.Mode(action=workload.Mode.ROTATE_SCREEN_TO_180, adapter=adapter, panel=panel),

                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfter180Rotation"),

                        # Invoke Rotation to 270
                        workload.Mode(action=workload.Mode.ROTATE_SCREEN_TO_270, adapter=adapter, panel=panel),

                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfter270Rotation"),

                        # Invoke Rotation to 0
                        workload.Mode(action=workload.Mode.ROTATE_SCREEN_TO_0, adapter=adapter, panel=panel),

                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterZeroRotation")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, True)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with VIDEO_ROTATION_VIDEO")
        logging.info(f"PASS: Feature verification with VIDEO_ROTATION_VIDEO")

    ##
    # @brief        This function verifies feature with resolution change
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_RESOLUTION_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_RESOLUTION_VIDEO")
    # @endcond
    def t_24_video_resolution_change_video(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbBeforeResolutionChange"),

                        # Invoke resolution change
                        workload.Mode(action=workload.Mode.RESOLUTION_MIN, adapter=adapter, panel=panel),

                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterResolutionChangeToMin"),

                        # Invoke resolution change
                        workload.Mode(action=workload.Mode.RESOLUTION_MAX, adapter=adapter, panel=panel),

                        # start tracer-> launch new video-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterResolutionChangeToMax")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with VIDEO_RESOLUTION_VIDEO")
        logging.info(f"PASS: Feature verification with VIDEO_RESOLUTION_VIDEO")

    ##
    # @brief        This function verifies feature with TDR
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_TDR_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_TDR_VIDEO")
    # @endcond
    def t_25_video_tdr_video(self):
        test_status = True
        VerifierCfg.tdr = Verify.SKIP
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video-> play 30 seconds -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbBeforeTDR"),

                        # start tracer-> play 10 seconds-> TDR-> play 30 seconds -> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Wait(delay=10),
                        # Invoke TDR
                        workload.Tdr(workload.Tdr.GENERATE, adapter.gfx_index),

                        # Detect TDR
                        workload.Tdr(workload.Tdr.DETECT, adapter.gfx_index),

                        # clear TDR
                        workload.Tdr(workload.Tdr.CLEAR, adapter.gfx_index),

                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceVpbAfterTDR")
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    test_status &= hrr.verify(adapter, panel, etl, self.media_fps, index == 0)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with TDR")
        logging.info(f"PASS: Feature verification with TDR")

    ##
    # @brief        This function verifies feature with Switching between Video - S3 - Game - Video workload
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_S3_GAME_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_S3_GAME_VIDEO")
    # @endcond
    def t_26_video_s3_game_video(self):
        if DisplayPower().is_power_state_supported(PowerEvent.S3) is False:
            self.fail("Test needs S3 supported system, but it is NOT S3 supported (Planning Issue)")
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(workload.VIDEO_PLAYBACK,
                                           [self.media_fps, 30, False, False, None, None, True, False])
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, True)

                if invoke_power_event(PowerEvent.S3) is False:
                    self.fail("FAILED to invoke power event(S3)")

                # breather
                time.sleep(5)

                app_config = workload.FlipAtAppConfig()
                app_config.game_index = 2
                etl_file, _ = workload.run(
                    workload.GAME_PLAYBACK,
                    [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                )

                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(workload.VIDEO_PLAYBACK,
                                           [self.media_fps, 30, False, False, None, None, True, False])
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, True)
                if self.feature == "FLIPQ_HRR":
                    test_status &= planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                                   platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWERLINE Scenario Video_S3_Game_Video")
        logging.info(f"PASS: Feature verification with POWERLINE Scenario Video_S3_Game_Video")

    ##
    # @brief        This function verifies feature with Switching between Video - S4 - Game - Video workload
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_S4_GAME_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_S4_GAME_VIDEO")
    # @endcond
    def t_27_video_s4_game_video(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(workload.VIDEO_PLAYBACK,
                                           [self.media_fps, 30, False, False, None, None, True, False])
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, True)

                if invoke_power_event(PowerEvent.S4) is False:
                    self.fail("FAILED to invoke power event(S4)")

                # breather
                time.sleep(5)

                app_config = workload.FlipAtAppConfig()
                app_config.game_index = 2
                etl_file, _ = workload.run(
                    workload.GAME_PLAYBACK,
                    [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                )

                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(workload.VIDEO_PLAYBACK,
                                           [self.media_fps, 30, False, False, None, None, True, False])
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, True)
                if self.feature == "FLIPQ_HRR":
                    test_status &= planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                                   platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWERLINE Scenario Video_S4_Game_Video")
        logging.info(f"PASS: Feature verification with POWERLINE Scenario Video_S4_Game_Video")

    ##
    # @brief        This function verifies feature with Switching between Video - CS - Game - Video workload
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'VIDEO_CS_GAME_VIDEO',
                     "Skipping the test step as the scenario type is not VIDEO_CS_GAME_VIDEO")
    # @endcond
    def t_28_video_cs_game_video(self):
        if DisplayPower().is_power_state_supported(PowerEvent.CS) is False:
            self.fail("Test needs CS supported system, but it is NOT CS supported (Planning Issue)")
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(workload.VIDEO_PLAYBACK,
                                           [self.media_fps, 30, False, False, None, None, True, False])
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, True)

                if invoke_power_event(PowerEvent.CS) is False:
                    self.fail("FAILED to invoke power event(CS)")

                # breather
                time.sleep(5)

                app_config = workload.FlipAtAppConfig()
                app_config.game_index = 2
                etl_file, _ = workload.run(
                    workload.GAME_PLAYBACK,
                    [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                )

                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(workload.VIDEO_PLAYBACK,
                                           [self.media_fps, 30, False, False, None, None, True, False])
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= hrr.verify(adapter, panel, etl_file, self.media_fps, True)
                if self.feature == "FLIPQ_HRR":
                    test_status &= planes_ui_helper.verify_feature(self.feature, etl_file, panel.pipe, panel.target_id,
                                                                   platform=adapter.name)
        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWERLINE Scenario VIDEO_CS_GAME_VIDEO")
        logging.info(f"PASS: Feature verification with POWERLINE Scenario VIDEO_CS_GAME_VIDEO")

    ##
    # @brief        This function verifies feature with Switching between Video - CS - Game - Video workload
    # @return       None
    # @cond
    @unittest.skipIf(planes_ui_helper.get_config_type('-SCENARIO') != 'HRR_DMRRS_HRR',
                     "Skipping the test step as the scenario type is not HRR_DMRRS_HRR")
    # @endcond
    def t_29_hrr_dmrrs_hrr(self):
        test_status = True
        dmrrs_fps = 30.000
        self.dmrrs_video_path = str(workload.VideoFile['FPS_30'].value)
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.min_rr > 30:
                    dmrrs_fps = 59.940
                    self.dmrrs_video_path = str(workload.VideoFile['FPS_59_940'].value)
                status, etl_files = workload.execute(
                    [
                        # start tracer-> launch new video HRR video-> play 30 seconds-> stop tracer-> close video
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Video(workload.Video.CLOSE),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceHRRVpb"),

                        # start tracer-> play 30 seconds DMRRS video-> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.dmrrs_video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceDMRRSVpb"),
                        workload.Video(workload.Video.CLOSE),

                        # start tracer-> play 30 seconds HRR video-> close video -> stop tracer
                        workload.Etl(workload.Etl.START),
                        workload.Video(workload.Video.LAUNCH_IN_FULLSCREEN, path=self.video_path),
                        workload.Wait(delay=30),
                        workload.Etl(workload.Etl.STOP, file_name="WorkloadTraceHrrVpbAfterDmrrs"),
                        workload.Video(workload.Video.CLOSE),
                    ]
                )

                if status is False or bool(etl_files[workload.Etl.STOP]) is False:
                    self.fail("FAILED to run the workload")

                for index, etl in enumerate(etl_files[workload.Etl.STOP]):
                    if "WorkloadTraceDMRRSVpb" in etl:
                        test_status &= dmrrs.verify(adapter, panel, etl, dmrrs_fps, True)
                    else:
                        test_status &= hrr.verify(adapter, panel, etl, self.media_fps, True)
                    if self.feature == "FLIPQ_HRR":
                        test_status &= planes_ui_helper.verify_feature(self.feature, etl, panel.pipe, panel.target_id,
                                                                       platform=adapter.name)

        if test_status is False:
            self.fail(f"FAIL: Feature verification with POWERLINE Scenario HRR_DMRRS_HRR")
        logging.info(f"PASS: Feature verification with POWERLINE Scenario HRR_DMRRS_HRR")


##
# @brief        This is a helper function to verify DMRRS with the provided power event
# @param[in]    event_type enum PowerEvent
# @return       Boolean, True if Successful, False otherwise
def invoke_power_event(event_type):
    display_power_ = DisplayPower()
    if display_power_.invoke_power_event(event_type, common.POWER_EVENT_DURATION_DEFAULT) is False:
        logging.error("FAILED to invoke PowerEvent (Test Issue)")
        return False
    logging.info(f"\tSuccessfully invoked from PowerEvent {event_type.name}")
    return True

if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PlanesUiCustomEvents))
    test_environment.TestEnvironment.cleanup(test_result)
