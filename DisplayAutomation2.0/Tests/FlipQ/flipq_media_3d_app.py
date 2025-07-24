##
# @file         flipq_media_3d_app.py
# @brief        Test to verify FlipQ functionality with video playback and 3D application.
#               Test consists of below scenarios:
#                   * Video playback and 3D application running in snapmode
#                   * Resize 3D application/media content
# @author       Anjali Shetty

import logging
import subprocess
import sys
import time
import unittest

from Libs.Core import window_helper, winkb_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import dll_logger
from Tests.FlipQ import flipq_base
from Tests.FlipQ import flipq_helper
from Tests.FlipQ.flipq_base import flip_base


##
# @brief    FlipQ tests to verify FlipQ functionality with video playback and 3D application
class FlipQMedia3DApp(flipq_base.FlipQBase):
    flip_base = flipq_base.FlipQBase()

    ##
    # @brief        test_01_media_3d_app_snapmode Test to verify FlipQ functionality during video playback and
    #                                              3D application running in snapmode.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "SNAP_MODE",
                     "Skip the test step as the action type is not snapmode")
    def test_01_media_3d_app_snapmode(self):
        ##
        # Verify that interval and buffer data is not None
        if flip_base.interval is None or flip_base.buffer is None:
            self.fail("Incorrect command line argument")

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_media_3d_app_snapmode_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        flipq_helper.play_close_media(True, True)

        ##
        # Open 3D Application
        self.app = \
            subprocess.Popen('TestStore/TestSpecificBin/Flips/ClassicD3D/ClassicD3D.exe interval:'
                             + flip_base.interval + 'buffers:' + flip_base.buffer)
        if self.app is not None:
            logging.info("Successfully launched 3D application")
        else:
            flipq_helper.report_to_gdhm("Failed to launch 3D application", driver_bug=False)
            self.fail("Failed to launch 3D application")

        ##
        # Wait for app to stabilize
        time.sleep(2)

        ##
        # Play 3D app in right snap
        winkb_helper.snap_right()

        ##
        # Wait for 2 seconds after playing 3D app in snap mode to stabilize
        time.sleep(2)

        ##
        # Play media in left snap
        winkb_helper.press('ENTER')

        ##
        # Wait for a minute while media and 3D app is running in snapmode
        time.sleep(60)

        ##
        # Close media
        flipq_helper.play_close_media(False)

        ##
        # Close 3D application
        self.app.terminate()

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_media_3d_app_snapmode_scenario")

        ##
        # Verify FlipQ
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flipq_helper.verify_flipq(etl_file, panel.pipe, adapter.platform):
                    logging.info("FlipQ verification passed")
                else:
                    flipq_helper.report_to_gdhm()
                    self.fail("FlipQ verification failed")

    ##
    # @brief        test_02_media_3d_app_resize Test to verify FlipQ functionality during video playback and
    #                                           resize of 3D application.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-ACTION') != "RESIZE",
                     "Skip the test step as the action type is not resize")
    def test_02_media_3d_app_resize(self):
        ##
        # Get current display configuration.
        current_config = self.config.get_current_display_configuration()

        ##
        # Get current applied mode.
        current_mode = self.config.get_current_mode(current_config.displayPathInfo[0].targetId)

        ##
        # Verify that interval and buffer data is not None
        if flip_base.interval is None or flip_base.buffer is None:
            self.fail("Incorrect command line argument")

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_media_3d_app_snapmode_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        media_handle = flipq_helper.play_close_media(True, False)

        left, top, right, bottom = 0, 0, 400, 400
        media_handle.set_position(left, top, right, bottom)

        time.sleep(2)

        ##
        # Open 3D Application
        self.app = \
            subprocess.Popen('TestStore/TestSpecificBin/Flips/ClassicD3D/ClassicD3D.exe interval:'
                             + flip_base.interval + 'buffers:' + flip_base.buffer)
        if self.app is not None:
            logging.info("Successfully launched 3D application")
        else:
            flipq_helper.report_to_gdhm("Failed to launch 3D application", driver_bug=False)
            self.fail("Failed to launch 3D application")

        ##
        # Wait for app to stabilize
        time.sleep(2)

        ##
        # Get 3D App window handle
        app_window_handle = window_helper.get_window('ClassicD3D: Window 0', True)

        left, top, right, bottom = 400, 400, 800, 800

        app_window_handle.set_position(left, top, right, bottom)

        while right + 40 < current_mode.HzRes and bottom + 40 < current_mode.VtRes:
            right = right + 40
            bottom = bottom + 40

            ##
            # Resize 3D app window
            app_window_handle.set_position(0, 0, right, bottom)

            ##
            # Wait for 2 seconds after resize
            time.sleep(2)

        ##
        # Resetting right and bottom to resize media
        right, bottom = 400, 400

        while right + 40 < current_mode.HzRes and bottom + 40 < current_mode.VtRes:
            right = right + 40
            bottom = bottom + 40

            ##
            # Resize media window
            media_handle.set_position(left, top, right, bottom)

            ##
            # Wait for 2 seconds after resize
            time.sleep(2)

        ##
        # Close media
        flipq_helper.play_close_media(False)

        ##
        # Close 3D application
        self.app.terminate()

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_cancel_scenario")

        ##
        # Verify FlipQ
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if flipq_helper.verify_flipq(etl_file, panel.pipe, adapter.platform):
                    logging.info("FlipQ verification passed")
                else:
                    flipq_helper.report_to_gdhm()
                    self.fail("FlipQ verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Test to verify FlipQ functionality with video playback and 3D application")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)