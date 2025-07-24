########################################################################################################################
# @file         lrr_custom_events.py
# @brief        Test for LRR verification during custom video/game scenarios
#
# @author       Karthik Kurella
########################################################################################################################
import time

from Libs.Core import enum
from Libs.Core import display_power
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LRR.lrr import VIDEO_FPS_MAPPING
from Libs.Core.display_config import display_config

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common, dut, workload
from Tests.PowerCons.Modules.workload import PowerSource
from Tests.VRR import vrr


##
# @brief        This class contains test cases for LRR with Video Playback
class LrrCustomEvents(LrrBase):
    display_power_ = display_power.DisplayPower()
    display_config_ = display_config.DisplayConfiguration()
    test_modes = {}  # {'gfx_0': {'DP_A': []}}

    ##
    # @brief        This class method is the entry point for any LRR mode set test case. Helps to initialize few of
    #               the parameters required for LRR mode set test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(LrrCustomEvents, cls).setUpClass()

        # Prepare the test mode list
        for adapter in dut.adapters.values():
            cls.test_modes[adapter.gfx_index] = {}
            for panel in adapter.panels.values():
                modes_max_rr = common.get_display_mode(panel.target_id, refresh_rate=panel.max_rr, limit=None)
                assert modes_max_rr, "Get display modes failed (Test issue)"
                cls.test_modes[adapter.gfx_index][panel.port] = [modes_max_rr[-1], modes_max_rr[0]]

    ##
    # @brief        This function verifies LRR with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PAUSE_VIDEO_S3_PLAY_VIDEO"])
    # @endcond
    def t_11_lrr_s3(self):
        # Video playback for 10 seconds -> Pause video -> Invoke S3 power_event -> Resume Video for 30 secs(close video)
        if self.video_with_power_event(display_power.PowerEvent.S3) is False:
            self.fail(f"FAIL: LRR feature verification with POWER_EVENT_S3")
        logging.info(f"PASS: LRR feature verification with POWER_EVENT_S3")

    ##
    # @brief        This function verifies LRR with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PAUSE_VIDEO_CS_PLAY_VIDEO"])
    # @endcond
    def t_12_lrr_cs(self):
        # Video playback for 10 seconds -> Pause video -> Invoke CS power_event -> Resume Video for 30 secs(close video)
        if self.video_with_power_event(display_power.PowerEvent.CS) is False:
            self.fail(f"FAIL: LRR feature verification with POWER_EVENT_CS")
        logging.info(f"PASS: LRR feature verification with POWER_EVENT_CS")

    ##
    # @brief        This function verifies LRR with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["PAUSE_VIDEO_S4_PLAY_VIDEO"])
    # @endcond
    def t_13_lrr_s4(self):
        # Video playback for 10 seconds -> Pause video -> Invoke S4 power_event -> Resume Video for 30 secs(close video)
        if self.video_with_power_event(display_power.PowerEvent.S4) is False:
            self.fail(f"FAIL: LRR feature verification with POWER_EVENT_S4")
        logging.info(f"PASS: LRR feature verification with POWER_EVENT_S4")

    ##
    # @brief        This function verifies LRR with POWERLINE AC/DC during WORKLOAD
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC_DC"])
    # @endcond
    def t_14_lrr_power_source(self):
        # Video playback for 10 seconds -> Enable repeat mode on video player  -> Pause video -> Do AC Switch ->
        # ->Resume the video for 10 secs-> Pause video ->  Do DC Switch-> Resume Video playback for 30 secs ->
        # Do AC Switch -> Resume Video playback for 30 secs -> close video player
        test_status = True
        media_fps = VIDEO_FPS_MAPPING[self.video_file]

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> pause video
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, media_fps, 30, True, True, False],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

                # Change to AC mode
                if workload.change_power_source(PowerSource.AC_MODE) is False:
                    self.fail(f"FAILED to set current power line status to {PowerSource.AC_MODE.name} (Test Issue)")

                # wait for 5 secs
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> pause video
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, False, media_fps, 30, True, True, True],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

                # Change to DC mode
                if workload.change_power_source(PowerSource.DC_MODE) is False:
                    self.fail(f"FAILED to set current power line status to {PowerSource.DC_MODE.name} (Test Issue)")

                # wait for 5 secs
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> pause video
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, False, media_fps, 30, True, True, True],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

                # Change to AC mode
                if workload.change_power_source(PowerSource.AC_MODE) is False:
                    self.fail(f"FAILED to set current power line status to {PowerSource.AC_MODE.name} (Test Issue)")

                # wait for 5 secs
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> close the video
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, True, media_fps, 30, True, False, True],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

        if test_status is False:
            self.fail("FAIL: LRR feature verification with POWERLINE Scenario AC/DC Switch")
        logging.info("PASS: LRR feature verification with POWERLINE Scenario AC/DC Switch")

    ##
    # @brief        This function verifies LRR with video and game inclusion of power event CS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_CS_GAME_VIDEO"])
    # @endcond
    def t_15_lrr_video_game_cs(self):
        # Video playback & verify feature -> Power_event CS -> Play game & verify VRR -> Video playback & verify feature
        if self.video_game_with_event(display_power.PowerEvent.CS) is False:
            self.fail("FAIL: LRR feature verification VIDEO->GAME->VIDEO with POWER_EVENT_CS")
        logging.info("PASS: LRR feature verification VIDEO->GAME->VIDEO with POWER_EVENT_CS")

    ##
    # @brief        This function verifies lrr with video and game inclusion of power event S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_S4_GAME_VIDEO"])
    # @endcond
    def t_16_lrr_video_game_s4(self):
        # Video playback & verify feature -> Power_event S4 -> Play game & verify VRR -> Video playback & verify feature
        if self.video_game_with_event(display_power.PowerEvent.S4) is False:
            self.fail("FAIL: LRR feature verification VIDEO->GAME->VIDEO with POWER_EVENT_S4")
        logging.info("PASS: LRR feature verification VIDEO->GAME->VIDEO with POWER_EVENT_S4")

    ##
    # @brief        This function verifies LRR with video and game inclusion of power event S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_S3_GAME_VIDEO"])
    # @endcond
    def t_17_lrr_video_game_s4(self):
        # Video playback & verify feature -> Power_event S3 -> Play game & verify VRR -> Video playback & verify feature
        if self.video_game_with_event(display_power.PowerEvent.S3) is False:
            self.fail("FAIL: LRR feature verification VIDEO->GAME->VIDEO with POWER_EVENT_S3")
        logging.info("PASS: LRR feature verification VIDEO->GAME->VIDEO with POWER_EVENT_S3")

    ##
    # @brief        This function verifies LRR with Modeset WORKLOAD
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_RESOLUTION_GAME_VIDEO"])
    # @endcond
    def t_18_lrr_video_game_mode_set(self):
        # Video_playback verify -> Invoke Mode Set -> Game_play verify -> Video_playback verify
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # video playback and verify feature
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

        test_status &= self.verify_with_mode_set()

        if test_status is False:
            self.fail("FAIL: LRR feature verification VIDEO->GAME->VIDEO with mode_set RESOLUTION")
        logging.info("PASS: LRR feature verification VIDEO->GAME->VIDEO with mode_set RESOLUTION")

    ##
    # @brief        This function verifies LRR with Rotation Workload
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["VIDEO_ROTATION_GAME_VIDEO"])
    # @endcond
    def t_19_lrr_video_game_mode_set(self):
        # Video_playback verify -> Invoke Mode Set -> Game_play verify -> Video_playback verify
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # video playback and verify feature
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

        test_status &= self.verify_with_rotation(enum.ROTATE_180)
        test_status &= self.verify_with_rotation(enum.ROTATE_0)

        if test_status is False:
            self.fail("FAIL: LRR feature verification VIDEO->GAME->VIDEO with mode_set ROTATION")
        logging.info("PASS: LRR feature verification VIDEO->GAME->VIDEO with mode_set ROTATION")

    ############################
    # Helper Function
    ############################
    ##
    # @brief        This is a helper function to verify LRR with mode set
    # @return       True if successful, False otherwise
    def verify_with_mode_set(self):
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
                    etl_file_path, _ = workload.run(
                        workload.GAME_PLAYBACK,
                        [workload.Apps.MovingRectangleApp, 30, True]
                    )
                    # Failures were seen sporadically when MovingRectangleApp was used,
                    # as async flips were not issued by OS sometimes
                    # The workload with MovingRectangleApp is used as latest to ensure async flip from OS[double check].
                    # Ensure async flips
                    if vrr.async_flips_present(etl_file_path) is False:
                        logging.info("OS is not sending async flips with MovingRectangle.. Retrying with FlipAt")
                        app_config = workload.FlipAtAppConfig()
                        app_config.game_index = 2
                        etl_file_path, _ = workload.run(
                            workload.GAME_PLAYBACK,
                            [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None,
                             app_config]
                        )
                        if vrr.async_flips_present(etl_file_path) is False:
                            self.fail("OS is NOT sending async flips")
                    status &= vrr.verify(adapter, panel, etl_file_path, vmax_flipline_for_each_flip=False)

                    # play video for duration seconds and verify feature
                    etl_file, polling_data = workload.run(
                        workload.VIDEO_PLAYBACK_USING_FILE,
                        [self.video_file, self.duration_in_seconds, False],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )
                    if etl_file is None:
                        self.fail("FAILED to run the workload")

                    status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                         pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

        return status

    ##
    # @brief        This is a helper function to verify LRR with rotation
    # @param[in]    angle
    # @return       True if successful, False otherwise
    def verify_with_rotation(self, angle):
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
                etl_file_path, _ = workload.run(
                    workload.GAME_PLAYBACK,
                    [workload.Apps.MovingRectangleApp, 30, True]
                )
                # Failures were seen sporadically when MovingRectangleApp was used,
                # as async flips were not issued by OS sometimes
                # The workload with MovingRectangleApp is used as latest to ensure async flip from OS[double check].
                # Ensure async flips
                if vrr.async_flips_present(etl_file_path) is False:
                    logging.info("OS is not sending async flips with MovingRectangle.. Retrying with FlipAt")
                    # gameplay and verify
                    app_config = workload.FlipAtAppConfig()
                    app_config.game_index = 2
                    etl_file_path, _ = workload.run(
                        workload.GAME_PLAYBACK,
                        [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                    )
                    if vrr.async_flips_present(etl_file_path) is False:
                        self.fail("OS is NOT sending async flips")
                status &= vrr.verify(adapter, panel, etl_file_path, vmax_flipline_for_each_flip=False)

                # play video for duration seconds and verify feature
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                     pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

        return status

    ##
    # @brief        Helper Function to handle power_event switch for scenario
    # @param[in]    power_event
    # @return       True if successful, False otherwise
    def video_game_with_event(self, power_event):
        test_status = True
        is_s3_supported = self.display_power_.is_power_state_supported(display_power.PowerEvent.S3)

        if power_event == display_power.PowerEvent.S3 and is_s3_supported is False:
            self.fail("Test needs S3 supported system, but it is S3 not supported (Planning Issue)")

        if power_event == display_power.PowerEvent.CS and is_s3_supported is True:
            self.fail("Test needs CS supported system, but it is S3 supported (Planning Issue)")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # play video for duration seconds and verify feature
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

                if invoke_power_event(power_event) is False:
                    self.fail("FAILED to invoke power event")

                # gameplay and verify
                etl_file_path, _ = workload.run(
                    workload.GAME_PLAYBACK,
                    [workload.Apps.MovingRectangleApp, 30, True]
                )
                # Failures were seen sporadically when MovingRectangleApp was used,
                # as async flips were not issued by OS sometimes
                # The workload with MovingRectangleApp is used as latest to ensure async flip from OS[double check].
                # Ensure async flips
                if vrr.async_flips_present(etl_file_path) is False:
                    logging.info("OS is not sending async flips with MovingRectangle.. Retrying with FlipAT")
                    app_config = workload.FlipAtAppConfig()
                    app_config.game_index = 2
                    etl_file_path, _ = workload.run(
                        workload.GAME_PLAYBACK,
                        [workload.Apps.FlipAt, workload.DEFAULT_GAME_PLAYBACK_DURATION, True, None, None, app_config]
                    )
                    if vrr.async_flips_present(etl_file_path) is False:
                        self.fail("OS is NOT sending async flips")
                test_status &= vrr.verify(adapter, panel, etl_file_path, vmax_flipline_for_each_flip=False)

                # play video for duration seconds and verify feature
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds, False],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

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

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():

                # start tracer-> launch new video-> play 30 seconds-> stop tracer-> pause video
                logging.info(f"\tPlaying {media_fps} video for 30s ")
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [True, False, media_fps, 30, False, True, False],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

                if invoke_power_event(power_event) is False:
                    self.fail("FAILED to invoke power event")

                # breather
                time.sleep(5)

                # unpause existing video-> start tracer-> play 30 seconds-> stop tracer-> close the video
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_WITH_CUSTOM_EVENTS,
                    [False, True, media_fps, 30, False, False, True],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )
                if etl_file is None:
                    self.fail("FAILED to run the workload")

                test_status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                          pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

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
    test_result = runner.run(common.get_test_suite(LrrCustomEvents))
    test_environment.TestEnvironment.cleanup(test_result)
