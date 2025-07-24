##
# @file         dxflips_app_events.py
# @brief        Test to verify Async Flips related features functionality with app running during different app events.
#               Test consists of below scenarios:
#               * Switching between full screen and windowed mode.
#               * Switching between sync and async flips.
#               * Switching between app window and desktop window
#               * Plays FLipAt/TrivFlip/FlipModelD3D12 app and media app in windowed mode.
# @author       Sunaina Ashok
import logging
import os
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips import flip_helper
from Tests.Flips.Dxflips import dxflips_base
from Tests.MPO.mpo_ui_helper import MPOUIHelper

MEDIA_FILE_FOLDER = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO")


##
# @brief    Contains test functions to verify Speedframe functionality with app running during different app events
class DxflipsAppEvents(dxflips_base.DxflipsBase):

    ##
    # @brief        Test function to verify Speedframe after switching between full screen and windowed mode.
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-APPEVENTS') != "FULLSCREEN_WINDOWED",
                     "Skip the test step as the action type is not switch app mode")
    # @endcond
    def test_01_switch_modes(self):

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        ##
        # Open app and play it in maximized mode, by default flip type will be async
        flip_helper.play_app(self.app, True, fps_pattern, fps_pattern2)

        ##
        # The opened app will play for 30 seconds
        time.sleep(30)

        for index in range(0, 4):
            if self.app == "FLIPMODELD3D12":
                winkb_helper.press('F11')
            else:
                winkb_helper.press(' ')
            logging.info("Switched the app mode")

            ##
            # The opened app will play for 30 seconds
            time.sleep(30)

        ##
        # Close the app
        flip_helper.close_app(self.app)

        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Stop ETL Trace
        etl_file = flip_helper.stop_etl_capture("After_app_modeswitch_scenario")

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break

    ##
    # @brief        Test function to verify Speedframe after switching between async and sync flips.
    # @return       None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-APPEVENTS') != "VSYNCSWITCH",
                     "Skip the test step as the action type is not vsync switch")
    # @endcond
    def test_02_switch_vsync(self):

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL Trace
        if flip_helper.start_etl_capture("Before_vsyncswitch_scenario") is False:
            self.fail("Failed to start GfxTrace")

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        ##
        # Open app and play it in maximized mode, by default flip type will be async
        flip_helper.play_app(self.app, True, fps_pattern, fps_pattern2)

        ##
        # Wait for app to stabilize
        time.sleep(5)

        ##
        # For Switching Vsync
        for iteration in range(0, 5):
            flip_helper.toggle_vsync(self.app, iteration)
            time.sleep(10)

        ##
        # Close the app
        flip_helper.close_app(self.app)

        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Stop ETL Trace
        etl_file = flip_helper.stop_etl_capture("After_vsyncswitch_scenario")

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break

    ##
    # @brief    Test function to verify AsyncFlips while app and media is playing in windowed mode
    # @return   None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-APPEVENTS') != "3DAPP_MEDIA",
                     "Skip the test step as the action type is not playing 3D App and Media ")
    # @endcond
    def test_03_windowed_3DApp_Media(self):
        mpo_ui_helper = MPOUIHelper()
        media_file = os.path.join(MEDIA_FILE_FOLDER, "mpo_1920_1080_avc.mp4")

        ##
        # Minimize all windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flip_helper.start_etl_capture("Before_3D_App_Media_scenario") is False:
            self.fail("\tFAIL: Failed to start GfxTrace")

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        ##
        # Open app and play it in maximized mode, by default flip type will be async
        flip_helper.play_app(self.app, False, fps_pattern, fps_pattern2)

        ##
        # Wait for app to stabilize
        time.sleep(5)

        ##
        # Play 3D app in left snap
        winkb_helper.snap_left()

        ##
        # Open Media app
        mpo_ui_helper.play_media(media_file, False)

        ##
        # Play media in right snap
        winkb_helper.snap_right()

        ##
        # App will run for one minute
        time.sleep(60)

        ##
        # Close the media app
        window_helper.close_media_player()

        ##
        # Close the app
        flip_helper.close_app(self.app)

        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Stop ETL Trace
        etl_file = flip_helper.stop_etl_capture("After_3D_App_Media_scenario")

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break

    ##
    # @brief    Test function to verify AsyncFlips while switching between app and desktop window
    # @return   None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-APPEVENTS') != "APP_SWITCH",
                     "Skip the test step as the action type is not app switch")
    # @endcond
    def test_04_app_switch(self):
        from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
        underrun = UnderRunStatus()

        ##
        # Minimize all windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flip_helper.start_etl_capture("Before_app_switch_scenario") is False:
            self.fail("\tFAIL: Failed to start GfxTrace")

        if self.app == "FLIPAT" or self.app == "DOTA":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        ##
        # Open app and play it in maximized mode, by default flip type will be async
        flip_helper.play_app(self.app, True, fps_pattern, fps_pattern2)

        ##
        # Wait for app to stabilize
        time.sleep(5)

        for iteration in range(0, 5):
            logging.info(f"Switch iteration count : {iteration + 1}")

            winkb_helper.press('ALT+TAB')
            logging.info("Switched to desktop window")

            ##
            # Wait for 5 seconds after switching
            time.sleep(5)

            ##
            # Switch window
            winkb_helper.press('ALT+TAB')
            logging.info("Switched to app window")

            ##
            # Wait for 5 seconds after switching
            time.sleep(5)

        ##
        # Close the app
        flip_helper.close_app(self.app)

        logging.info(flip_helper.getStepInfo() + "Closed {0} App".format(self.app))

        ##
        # Stop ETL Trace
        etl_file = flip_helper.stop_etl_capture("After_app_switch_scenario")

        ##
        # Verifying Async flips features
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flip_helper.verify_feature(self.feature, etl_file, panel.pipe) is False:
                    flip_helper.report_to_gdhm(self.feature)
                    self.fail(flip_helper.fail_statements(self.feature))

                if underrun.verify_underrun() is True:
                    flip_helper.report_to_gdhm(self.feature,
                                               "Underrun Found during app switch [Driver Issue]",
                                               driver_bug=True)

                if self.context_args.test.cmd_params.topology == enum.EXTENDED:
                    break


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test Purpose: Test to verify Async flip related features functionality while running the application during different app events")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
