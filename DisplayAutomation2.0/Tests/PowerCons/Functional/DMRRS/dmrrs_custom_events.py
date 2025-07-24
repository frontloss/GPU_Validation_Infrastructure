########################################################################################################################
# @file         dmrrs_custom_events.py
# @brief        Test for DMRRS verification during custom video/game scenarios
#
# @author       Karthik Kurella
########################################################################################################################
import logging
import time
import unittest

from Libs.Core import enum, display_utility, window_helper, winkb_helper
from Libs.Core import display_power
from Libs.Core.logger import html, gdhm
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DMRRS.dmrrs import VIDEO_FPS_MAPPING
from Tests.PowerCons.Functional.DMRRS.dmrrs_base import DmrrsBase
from Tests.PowerCons.Functional.DMRRS import dmrrs
from Tests.PowerCons.Modules import common, dut, workload
from Tests.PowerCons.Modules.workload import PowerSource
from Tests.VRR import vrr


##
# @brief        This class contains test cases for DMRRS with Custom Video/Game Scenarios
class DmrrsCustomEvents(DmrrsBase):
    test_modes = {}  # {'gfx_0': {'DP_A': []}}

    ##
    # @brief        This class method is the entry point for any DMRRS mode set test case. Helps to initialize few of
    #               the parameters required for DMRRS mode set test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(DmrrsCustomEvents, cls).setUpClass()

        # Prepare the test mode list
        for adapter in dut.adapters.values():
            cls.test_modes[adapter.gfx_index] = {}
            for panel in adapter.panels.values():
                modes_max_rr = common.get_display_mode(panel.target_id, refresh_rate=panel.max_rr, limit=None)
                assert modes_max_rr, "Get display modes failed (Test issue)"
                cls.test_modes[adapter.gfx_index][panel.port] = [modes_max_rr[-1], modes_max_rr[0]]

    ##
    # @brief        This class method is the exit point for any DMRRS custom event test case. Helps to reset few of the
    #               parameters to default to avoid any disruption in test execution.
    # @return       None
    @classmethod
    def tearDownClass(cls):
        super(DmrrsCustomEvents, cls).tearDownClass()
        # Moving back to default zero rotation after test is completed, to avoid any effect on other tests.
        # If left in 90, h_total and v_total are changed leading to division by zero error.
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    continue
                current_mode = cls.display_config_.get_current_mode(panel.target_id)
                if current_mode.rotation != 1:
                    current_mode.rotation = enum.ROTATE_0
                    if cls.display_config_.set_display_mode([current_mode], False) is False:
                        assert False, "FAILED to set display mode"
                    logging.info("\tSuccessfully applied mode")
                else:
                    logging.info(f"HW_Rotation already set to zero")

    ##
    # @brief        This function verifies DMRRS with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PAUSE_VIDEO_S3_PLAY_VIDEO"])
    # @endcond
    def t_11_dmrrs_s3(self):
        # Video playback for 10 seconds -> Pause video -> Invoke S3 power_event -> Resume Video for 30 secs(close video)
        if self.video_with_power_event(display_power.PowerEvent.S3) is False:
            self.fail(f"FAIL: DMRRS feature verification with POWER_EVENT_S3")
        logging.info(f"PASS: DMRRS feature verification with POWER_EVENT_S3")

    ##
    # @brief        This function verifies DMRRS with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PAUSE_VIDEO_CS_PLAY_VIDEO"])
    # @endcond
    def t_12_dmrrs_cs(self):
        # Video playback for 10 seconds -> Pause video -> Invoke CS power_event -> Resume Video for 30 secs(close video)
        if self.video_with_power_event(display_power.PowerEvent.CS) is False:
            self.fail("FAIL: DMRRS feature verification with POWER_EVENT_CS")
        logging.info("PASS: DMRRS feature verification with POWER_EVENT_CS")

    ##
    # @brief        This function verifies DMRRS with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PAUSE_VIDEO_S4_PLAY_VIDEO"])
    # @endcond
    def t_13_dmrrs_s4(self):
        # Video playback for 10 seconds -> Pause video -> Invoke S4 power_event -> Resume Video for 30 secs(close video)
        if self.video_with_power_event(display_power.PowerEvent.S4) is False:
            self.fail("FAIL: DMRRS feature verification with POWER_EVENT_S4")
        logging.info("PASS: DMRRS feature verification with POWER_EVENT_S4")

    ##
    # @brief        This function verifies DMRRS with POWERLINE AC/DC during WORKLOAD
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC_DC"])
    # @endcond
    def t_14_dmrrs_power_source(self):
        # Video playback for 10 seconds -> Enable repeat mode on video player  -> Pause video -> Do AC Switch ->
        # ->Resume the video for 10 secs-> Pause video ->  Do DC Switch-> Resume Video playback for 30 secs ->
        # Do AC Switch -> Resume Video playback for 30 secs -> close video player
        test_status = True
        media_fps = VIDEO_FPS_MAPPING[self.video_file]

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> pause video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, media_fps, 30, True, True, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

                # Change to AC mode
                if workload.change_power_source(PowerSource.AC_MODE) is False:
                    self.fail(f"FAILED to set current power line status to {PowerSource.AC_MODE.name} (Test Issue)")

                logging.info("Waiting for 5 seconds")
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> pause video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, False, media_fps, 30, True, True, True]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps, etl_started_before_video=False)

                # Change to DC mode
                if workload.change_power_source(PowerSource.DC_MODE) is False:
                    self.fail(f"FAILED to set current power line status to {PowerSource.DC_MODE.name} (Test Issue)")

                logging.info("Waiting for 5 seconds")
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> pause video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, False, media_fps, 30, True, True, True]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps, etl_started_before_video=False)

                # Change to AC mode
                if workload.change_power_source(PowerSource.AC_MODE) is False:
                    self.fail(f"FAILED to set current power line status to {PowerSource.AC_MODE.name} (Test Issue)")

                logging.info("Waiting for 5 seconds")
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> close the video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, True, media_fps, 30, True, False, True]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps, etl_started_before_video=False)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with POWERLINE Scenario AC/DC Switch")
        logging.info("PASS: DMRRS feature verification with POWERLINE Scenario AC/DC Switch")

    ##
    # @brief        This function verifies DMRRS with video and game inclusion of power event CS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_CS_GAME_VIDEO"])
    # @endcond
    def t_15_dmrrs_video_game_cs(self):
        # Video verify -> Invoke CS -> Game play -> Video verify
        if self.video_game_with_event(display_power.PowerEvent.CS) is False:
            self.fail("FAIL: DMRRS feature verification VIDEO->GAME->VIDEO with POWER_EVENT_CS")
        logging.info("PASS: DMRRS feature verification VIDEO->GAME->VIDEO with POWER_EVENT_CS")

    ##
    # @brief        This function verifies DMRRS with video and game inclusion of power event S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_S4_GAME_VIDEO"])
    # @endcond
    def t_16_dmrrs_video_game_s4(self):
        # Video verify -> Invoke s4 -> Game play -> Video verify
        if self.video_game_with_event(display_power.PowerEvent.S4) is False:
            self.fail(f"FAIL: DMRRS feature verification VIDEO->GAME->VIDEO with POWER_EVENT_S4")
        logging.info(f"PASS: DMRRS feature verification VIDEO->GAME->VIDEO with POWER_EVENT_S4")

    ##
    # @brief        This function verifies DMRRS with video and game inclusion of power event S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_S3_GAME_VIDEO"])
    # @endcond
    def t_17_dmrrs_video_game_s3(self):
        # Video Verify -> Invoke s3 -> Game play -> Video verify
        if self.video_game_with_event(display_power.PowerEvent.S3) is False:
            self.fail(f"FAIL: DMRRS feature verification VIDEO->GAME->VIDEO with POWER_EVENT_S3")
        logging.info(f"PASS: DMRRS feature verification VIDEO->GAME->VIDEO with POWER_EVENT_S3")

    ##
    # @brief        This function verifies DMRRS with Modeset WORKLOAD VIDEO->GAME->VIDEO
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_RESOLUTION_GAME_VIDEO"])
    # @endcond
    def t_18_dmrrs_video_game_mode_set(self):
        # Video_playback verify -> Invoke Mode Set  -> Game_play verify -> Video_playback verify
        test_status = True
        media_fps = VIDEO_FPS_MAPPING[self.video_file]
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

        test_status &= self.verify_with_mode_set(media_fps)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification VIDEO->GAME->VIDEO with mode_set RESOLUTION")
        logging.info("PASS: DMRRS feature verification VIDEO->GAME->VIDEO with mode_set RESOLUTION")

    ##
    # @brief        This function verifies DMRRS with Rotation Workload
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_ROTATION_GAME_VIDEO"])
    # @endcond
    def t_19_dmrrs_video_game_mode_set(self):
        # Video_playback verify -> Invoke Mode Set  -> Game_play verify -> Video_playback verify
        test_status = True
        media_fps = VIDEO_FPS_MAPPING[self.video_file]
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

        test_status &= self.verify_with_rotation(media_fps, enum.ROTATE_180)
        test_status &= self.verify_with_rotation(media_fps, enum.ROTATE_0)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification VIDEO->GAME->VIDEO with mode_set ROTATION")
        logging.info("PASS: DMRRS feature verification VIDEO->GAME->VIDEO with mode_set ROTATION")

    ##
    # @brief        This function verifies DMRRS with MIN_RR/MAX_RR change during Video Playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["RR_MAX_MIN_MAX"])
    # @endcond
    def t_20_video_rr_change(self):
        test_status = True
        media_fps = VIDEO_FPS_MAPPING[self.video_file]

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                html.step_start(f"Starting Video with {panel.drrs_caps.max_rr} Hz(Max RR) during Video Playback", True)
                html.step_end()
                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> keep the video playing
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, media_fps, 30, True, False, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

                html.step_start(f"Switching to {panel.drrs_caps.min_rr} Hz(Min RR) during Video Playback", True)
                mode = common.get_display_mode(panel.target_id, panel.min_rr)
                if mode is None:
                    self.fail("FAILED to get display mode")
                logging.info(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("\tSuccessfully applied display mode")

                dut.refresh_panel_caps(adapter)
                html.step_end()

                # start tracer-> video is already playing-> play 30 seconds-> stop tracer-> keep the video playing
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, False, media_fps, 30, True, False, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status = dmrrs.verify_dmrrs_with_min_rr(adapter, panel, etl_file)

                # Change to Max RR during video playback
                html.step_start(f"Switching to {panel.drrs_caps.max_rr} Hz(Max RR) during Video Playback", True)
                mode = common.get_display_mode(panel.target_id, panel.max_rr)
                if mode is None:
                    self.fail("FAILED to get display mode")
                logging.info(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("\tSuccessfully applied display mode")

                dut.refresh_panel_caps(adapter)
                html.step_end()

                # let video play after RR switch as OS will not start non-zero duration immediately
                html.step_start("Playing the video for next 30 seconds in Max RR")
                time.sleep(30)

                status, etl_file = workload.etl_tracer_stop_existing_and_start_new("GfxTraceDuringMaxRRSwitch")

                # close media player
                window_helper.close_media_player()
                logging.info("\tClosing video playback")
                html.step_end()

                if status is None:
                    self.fail("FAILED to get ETL during Max RR Switch")
                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with Scenario RR_MAX_MIN_MAX Change")
        logging.info("PASS: DMRRS feature verification with Scenario RR_MAX_MIN_MAX Change")

    ##
    # @brief        This function verifies DMRRS with UNPLUG/PLUG/UNPLUG during Video Playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["UNPLUG_PLUG_UNPLUG"])
    # @endcond
    def t_21_video_unplug_plug_unplug(self):
        lfp_panels = []
        ext_panels = []
        test_status = True
        media_fps = VIDEO_FPS_MAPPING[self.video_file]

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    ext_panels.append(panel.port)
                    continue
                if panel.drrs_caps.is_dmrrs_supported is False:
                    continue
                lfp_panels.append(panel)

        # unplug the external panel before video playback,since DMRRS is not supported.
        if len(ext_panels) == 0:
            self.fail("No External Panel found [Test Issue]")
        for ext_panel in ext_panels:
            logging.info(f"Step: Unplug display {ext_panel}")
            if display_utility.unplug(ext_panel) is False:
                self.fail(f"FAILED to unplug display= {ext_panel}")
            logging.info(f"\tSuccessfully unplugged display= {ext_panel}")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # @Todo Sporadically unplug failure is observed. Can be removed once issue is not observed.
                if panel.is_lfp is False:
                    continue

                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> keep the video playing
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, media_fps, 30, True, False, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

                # plug the external panel
                for ext_panel in ext_panels:
                    logging.info(f"Step: Plug display {ext_panel}")
                    if display_utility.plug(ext_panel) is False:
                        self.fail(f"FAILED to plug display= {ext_panel}")
                    logging.info(f"\tSuccessfully plugged display= {ext_panel}")
                # unplug the external panel
                for ext_panel in ext_panels:
                    logging.info(f"Step: Unplug display= {ext_panel}")
                    if display_utility.unplug(ext_panel) is False:
                        self.fail(f"FAILED to unplug display= {ext_panel}")
                    logging.info(f"\tSuccessfully unplugged display= {ext_panel}")

                dut.refresh_panel_caps(adapter)

                # from Nickel+, maximize the video player
                if dut.WIN_OS_VERSION > dut.WinOsVersion.WIN_COBALT:
                    # WA: after plug/unplug EFP, video player is switched to Mini Player.
                    # Below code will make it Fullscreen
                    winkb_helper.press("ALT_ENTER")
                    time.sleep(2)
                    window_helper.mouse_left_click(400, 400)
                    time.sleep(2)

                # start tracer-> video is already playing-> play 30 seconds-> close the video-> stop tracer
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, True, media_fps, 30, False, False, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps, etl_started_before_video=False)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with Scenario UNPLUG_PLUG_UNPLUG")
        logging.info("PASS: DMRRS feature verification with Scenario UNPLUG_PLUG_UNPLUG")

    ##
    # @brief        This function verifies DMRRS with HW_Rotation 0-180-0 during Video Playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HW_ROTATION_0_180_0"])
    # @endcond
    def t_22_video_Rotation(self):
        test_status = True
        rotation_list = [enum.ROTATE_180, enum.ROTATE_0]
        media_fps = VIDEO_FPS_MAPPING[self.video_file]
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> keep the video playing
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, media_fps, 30, True, False, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

                current_mode = self.display_config_.get_current_mode(panel.target_id)
                for index, rotation in enumerate(rotation_list):
                    current_mode.rotation = rotation
                    logging.info(f"Applying display mode {current_mode.HzRes}x{current_mode.VtRes}"
                                 f"@{current_mode.refreshRate}Hz {current_mode.rotation}")
                    if self.display_config_.set_display_mode([current_mode], False) is False:
                        self.fail("FAILED to set display mode")
                    logging.info("\tSuccessfully applied mode")

                    # During video playback, HW rotation will be done and DMRRS will be verified for each HW rotation.
                    # For last rotation in rotation list, the video playback will be stopped
                    # start tracer-> video is already playing-> play 30 seconds-> stop tracer-> pause/ close video
                    etl_file, _ = workload.run(
                        workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                        [False, True if index == len(rotation_list) - 1 else False, media_fps, 30, False, False, False]
                    )
                    if etl_file is None:
                        self.fail("FAILED to run the workload")

                    test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps, etl_started_before_video=False)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with Scenario HW_ROTATION_0_180_0")
        logging.info("PASS: DMRRS feature verification with Scenario HW_ROTATION_0_180_0")

    ##
    # @brief        This function verifies DMRRS with HW_Rotation 90-270-90 during Video Playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["HW_ROTATION_90_270_90"])
    # @endcond
    def t_23_video_Rotation(self):
        test_status = True
        rotation_list = [enum.ROTATE_270, enum.ROTATE_90]
        media_fps = VIDEO_FPS_MAPPING[self.video_file]
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Starting the test with 90 degree hardware rotation
                current_mode = self.display_config_.get_current_mode(panel.target_id)
                current_mode.rotation = enum.ROTATE_90
                if self.display_config_.set_display_mode([current_mode], False) is False:
                    self.fail("FAILED to set display mode")
                logging.info("\tSuccessfully applied mode")

                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> keep the video playing
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, media_fps, 30, True, False, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

                # During video playback hardware rotation is being done to 270 and then again 90.
                for index, rotation in enumerate(rotation_list):
                    current_mode.rotation = rotation
                    logging.info(f"Applying display mode {current_mode.HzRes}x{current_mode.VtRes}"
                                 f"@{current_mode.refreshRate}Hz {current_mode.rotation}")
                    if self.display_config_.set_display_mode([current_mode], False) is False:
                        self.fail("FAILED to set display mode")
                    logging.info("\tSuccessfully applied mode")

                    # During video playback, HW rotation will be done and DMRRS will be verified for each HW rotation.
                    # For last rotation in rotation list, the video playback will be stopped
                    # start tracer-> video is already playing-> play 30 seconds-> stop tracer-> pause/ close video
                    etl_file, _ = workload.run(
                        workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                        [False, True if index == len(rotation_list) - 1 else False, media_fps, 30, False, False, False]
                    )
                    if etl_file is None:
                        self.fail("FAILED to run the workload")

                    test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps, etl_started_before_video=False)

        if test_status is False:
            self.fail("FAIL: DMRRS feature verification with Scenario HW_ROTATION_90_270_90")
        logging.info("PASS: DMRRS feature verification with Scenario HW_ROTATION_90_270_90")

    ############################
    # Helper Functions
    ############################
    ##
    # @brief        This is a helper function to verify DMRRS with mode set
    # @param[in]    media_fps
    # @return       True if successful, False otherwise
    def verify_with_mode_set(self, media_fps):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if len(self.test_modes[adapter.gfx_index][panel.port]) == 0:
                    self.fail("Test mode list is empty (Test issue)")

                for mode in self.test_modes[adapter.gfx_index][panel.port]:
                    html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                    if self.display_config_.set_display_mode([mode], False) is False:
                        html.step_end()
                        self.fail("FAILED to apply display mode")
                    html.step_end()

                    # gameplay and verify
                    app_config = workload.FlipAtAppConfig()
                    app_config.game_index = 2
                    etl_file, _ = workload.run(
                        workload.GAME_PLAYBACK,
                        [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                    )
                    if vrr.async_flips_present(etl_file) is False:
                        gdhm.report_test_bug_os("[OsFeatures][VRR] OS is NOT sending async flips")
                        html.step_end()
                        self.fail("OS is NOT sending async flips")

                    vrr.verify(adapter, panel, etl_file)
                    # @todo VSDI-34637 enable below verification after HSD-18023132373 is closed. GDHM is inside verify
                    # status &= vrr.verify(adapter, panel, etl_file)

                    # play video for duration seconds and verify feature
                    etl_file, _ = workload.run(
                        workload.VIDEO_PLAYBACK_USING_FILE,
                        [self.video_file, self.duration_in_seconds, False]
                    )
                    if etl_file is None:
                        self.fail("FAILED to run the workload")

                    status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

        return status

    ##
    # @brief        This is a helper function to verify DMRRS with rotation
    # @param[in]    media_fps
    # @param[in]    angle
    # @return       True if successful, False otherwise
    def verify_with_rotation(self, media_fps, angle):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                mode = self.display_config_.get_current_mode(panel.target_id)
                mode.rotation = angle
                html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz {mode.rotation}")
                if self.display_config_.set_display_mode([mode], False) is False:
                    html.step_end()
                    self.fail("FAILED to set display mode")
                html.step_end()

                # gameplay and verify
                app_config = workload.FlipAtAppConfig()
                app_config.game_index = 2
                etl_file, _ = workload.run(
                    workload.GAME_PLAYBACK,
                    [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                )
                if vrr.async_flips_present(etl_file) is False:
                    gdhm.report_test_bug_os("[OsFeatures][VRR] OS is NOT sending async flips")
                    html.step_end()
                    self.fail("OS is NOT sending async flips")
                vrr.verify(adapter, panel, etl_file)
                # @todo VSDI-34637 enable below verification after HSD-18023132373 is closed. GDHM is inside verify()
                # status &= vrr.verify(adapter, panel, etl_file)

                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

        return status

    ##
    # @brief        Helper Function to handle power_event switch for scenario 4
    # @param[in]    power_event
    # @return       True if successful, False otherwise
    def video_game_with_event(self, power_event):
        test_status = True
        is_s3_supported = self.display_power_.is_power_state_supported(display_power.PowerEvent.S3)
        media_fps = VIDEO_FPS_MAPPING[self.video_file]

        if power_event == display_power.PowerEvent.S3 and is_s3_supported is False:
            self.fail("Test needs S3 supported system, but it is S3 not supported (Planning Issue)")

        if power_event == display_power.PowerEvent.CS and is_s3_supported is True:
            self.fail("Test needs CS supported system, but it is S3 supported (Planning Issue)")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

                if invoke_power_event(power_event) is False:
                    self.fail("FAILED to invoke power event")

                app_config = workload.FlipAtAppConfig()
                app_config.game_index = 2
                etl_file, _ = workload.run(
                    workload.GAME_PLAYBACK,
                    [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                )
                if vrr.async_flips_present(etl_file) is False:
                    gdhm.report_test_bug_os("[OsFeatures][VRR] OS is NOT sending async flips")
                    html.step_end()
                    self.fail("OS is NOT sending async flips")
                vrr.verify(adapter, panel, etl_file)
                # @todo VSDI-34637 enable below verification after HSD-18023132373 is closed. GDHM is inside verify()
                # test_status &= vrr.verify(adapter, panel, etl_file)

                # play video for duration seconds and verify feature
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

        return test_status

    ##
    # @brief        Helper Function to handle power_event switch
    # @param[in]    power_event
    # @return       True if successful, False otherwise
    def video_with_power_event(self, power_event):
        test_status = True
        is_s3_supported = self.display_power_.is_power_state_supported(display_power.PowerEvent.S3)
        media_fps = VIDEO_FPS_MAPPING[self.video_file]

        if power_event == display_power.PowerEvent.S3 and is_s3_supported is False:
            self.fail("Test needs S3 supported system, but it is S3 not supported (Planning Issue)")

        if power_event == display_power.PowerEvent.CS and is_s3_supported is True:
            self.fail("Test needs CS supported system, but it is S3 supported (Planning Issue)")

        logging.info("\tInitiating workload with Power Event")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> pause video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, media_fps, 30, True, True, False]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

                if invoke_power_event(power_event) is False:
                    self.fail("FAILED to invoke power event")

                # breather
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> close the video
                etl_file, _ = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, True, media_fps, 30, False, False, True]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= dmrrs.verify(adapter, panel, etl_file, media_fps)

        return test_status


##
# @brief        This is a helper function to verify DMRRS with the provided power event
# @param[in]    event_type enum PowerEvent
# @return       Boolean, True if Successful, False otherwise
def invoke_power_event(event_type):
    display_power_ = display_power.DisplayPower()
    if display_power_.invoke_power_event(event_type, common.POWER_EVENT_DURATION_DEFAULT) is False:
        logging.error("FAILED to invoke PowerEvent (Test Issue)")
        return False
    logging.info(f"\tSuccessfully invoked from PowerEvent {event_type.name}")
    return True


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DmrrsCustomEvents))
    test_environment.TestEnvironment.cleanup(test_result)
