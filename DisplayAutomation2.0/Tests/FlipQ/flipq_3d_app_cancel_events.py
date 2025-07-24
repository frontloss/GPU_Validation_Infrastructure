##
# @file         flipq_3d_app_cancel_events.py
# @brief        Test to verify FlipQ cancel functionality with 3D application.
#               Test consists of below scenarios:
#                   * Maximize and minimize 3D application window
#                   * Close and open 3D application window
#                   * Switch between windowed and fullscreen mode
#                   * Resize of 3D application
#                   * Move 3D application window
#               Verification includes queue cancellation and queue recreation
# @author       Anjali Shetty

import logging
import subprocess
import sys
import time
import unittest

from Libs.Core import window_helper, winkb_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.FlipQ import flipq_base
from Tests.FlipQ import flipq_helper
from Tests.FlipQ.flipq_base import flip_base


##
# @brief    FlipQ tests to verify FlipQ cancel functionality with 3D application
class FlipQ3DAppCancelEvents(flipq_base.FlipQBase):

    ##
    # @brief        test_01_3d_app_cancel_queue Test to verify FlipQ functionality while running 3D application and
    #                                           exercising below scenarios
    #                                           * Maximize and minimize window
    #                                           * Open and close window
    #                                           * Switch to fullscreen and windowed mode
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "CANCEL_QUEUE",
                     "Skip the test step as the action type is not cancel queue")
    def test_01_3d_app_cancel_queue(self):
        ##
        # Verify that interval and buffer data is not None
        if flip_base.interval is None or flip_base.buffer is None:
            self.fail("Incorrect command line argument")

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_cancel_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Open 3D Application
        self.app = \
            subprocess.Popen('TestStore/TestSpecificBin/Flips/ClassicD3D/ClassicD3D.exe interval:' + flip_base.interval
                             + 'buffers:' + flip_base.buffer)
        if self.app is not None:
            logging.info("Successfully launched 3D application")
        else:
            flipq_helper.report_to_gdhm("Failed to launch 3D application", driver_bug=False)
            self.fail("Failed to launch 3D application")

        ##
        # Wait for a minute while 3D app is running
        time.sleep(60)

        ##
        # Perform cancel event
        flipq_helper.perform_3d_app_cancel_event(self.action)(self.app)

        ##
        # Close 3D application
        self.app.terminate()
        logging.info("Closed 3D application")

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

    ##
    # @brief        test_02_3d_app_cancel_queue_resize Test to verify FlipQ functionality while resizing 3D application
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-ACTION') != "RESIZE",
                     "Skip the test step as the action type is not cancel queue and resize")
    def test_02_3d_app_cancel_queue_resize(self):
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
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_resize_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Open 3D Application
        self.app = \
            subprocess.Popen('TestStore/TestSpecificBin/Flips/ClassicD3D/ClassicD3D.exe interval:' + flip_base.interval
                             + 'buffers:' + flip_base.buffer)
        if self.app is not None:
            logging.info("Successfully launched 3D application")
        else:
            flipq_helper.report_to_gdhm("Failed to launch 3D application", driver_bug=False)
            self.fail("Failed to launch 3D application")

        ##
        # Wait for a minute while 3D app is running
        time.sleep(60)

        ##
        # Width and Height values for first flip
        width = 400
        height = 400

        ##
        # Get 3D App window handle
        app_window_handle = window_helper.get_window('ClassicD3D: Window 0', True)

        ##
        # Resize the window
        app_window_handle.set_position(0, 0, width, height)

        while width + 40 < current_mode.HzRes and height + 40 < current_mode.VtRes:
            width = width + 40
            height = height + 40

            ##
            # Resize window
            app_window_handle.set_position(0, 0, width, height)

            ##
            # Wait for 2 seconds after resize
            time.sleep(2)

        ##
        # Close 3D application
        self.app.terminate()
        logging.info("Closed 3D application")

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_resize_scenario")

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
    # @brief        test_02_3d_app_cancel_queue_move_window Test to verify FlipQ functionality while
    #                                                       dragging 3D application.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-ACTION') != "MOVE_WINDOW",
                     "Skip the test step as the action type is not cancel queue and move window")
    def test_03_3d_app_cancel_queue_move_window(self):
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
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_move_window_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Open 3D Application
        self.app = \
            subprocess.Popen('TestStore/TestSpecificBin/Flips/ClassicD3D/ClassicD3D.exe interval:' + flip_base.interval
                             + 'buffers:' + flip_base.buffer)
        if self.app is not None:
            logging.info("Successfully launched 3D application")
        else:
            flipq_helper.report_to_gdhm("Failed to launch 3D application", driver_bug=False)
            self.fail("Failed to launch 3D application")

        ##
        # Wait for a minute while 3D app is running
        time.sleep(60)

        ##
        # left, top, right and bottom values
        left, top, right, bottom = 0, 0, 400, 400

        ##
        # Get 3D App window handle
        app_window_handle = window_helper.get_window('ClassicD3D: Window 0', True)

        ##
        # Move 3D App window
        app_window_handle.set_position(left, top, right, bottom)

        while right + 40 < current_mode.HzRes and bottom + 40 < current_mode.VtRes:
            left = left + 40
            top = top + 40
            right = right + 40
            bottom = bottom + 40

            ##
            # Move 3D App window
            app_window_handle.set_position(left, top, right, bottom)

        ##
        # Close 3D application
        self.app.terminate()
        logging.info("Closed 3D application")

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_move_window_scenario")

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
    logging.info("Test Purpose: FlipQ tests to verify FlipQ cancel functionality with 3D application")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
