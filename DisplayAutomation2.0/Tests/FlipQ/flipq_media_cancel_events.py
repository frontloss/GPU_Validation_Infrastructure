##
# @file         flipq_media_cancel_events.py
# @brief        Test to verify FlipQ cancel functionality with video playback.
#               Test consists of below scenarios:
#                   * Maximize and minimize video playback window
#                   * Close and open video playback window
#                   * Switch between windowed and fullscreen mode
#                   * Play and pause video
#                   * Resize of video playback window
#                   * Move video playback window
#               Verification includes queue cancellation and queue recreation
# @author       Anjali Shetty

import logging
import sys
import time
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.FlipQ import flipq_base
from Tests.FlipQ import flipq_helper


##
# @brief    FlipQ tests to verify FlipQ cancel functionality with video playback
class FlipQMediaCancelEvents(flipq_base.FlipQBase):
    flip_base = flipq_base.FlipQBase()

    ##
    # @brief        test_01_media_cancel_queue Test to verify FlipQ functionality during video playback and
    #                                          exercising below scenarios
    #                                          * Maximize and minimize window
    #                                          * Open and close window
    #                                          * Switch to fullscreen and windowed mode
    #                                          * Play and pause video
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "CANCEL_QUEUE",
                     "Skip the test step as the action type is not cancel queue")
    def test_01_media_cancel_queue(self):
        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_cancel_queue_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        flipq_helper.play_close_media(True, False)

        ##
        # Perform cancel event
        flipq_helper.perform_media_cancel_event(self.action)

        ##
        # Close media player
        flipq_helper.play_close_media(False)

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_cancel_queue_scenario")

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
    # @brief        test_02_media_cancel_queue_resize Test to verify FlipQ functionality
    #               while resizing video application
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-ACTION') != "RESIZE",
                     "Skip the test step as the action type is not cancel queue and resize")
    def test_02_media_cancel_queue_resize(self):
        ##
        # Get current display configuration.
        current_config = self.config.get_current_display_configuration()

        ##
        # Get current applied mode.
        current_mode = self.config.get_current_mode(current_config.displayPathInfo[0].targetId)

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_resize_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        media_handle = flipq_helper.play_close_media(True, False)

        width = 400
        height = 400
        media_handle.set_position(0, 0, width, height)

        ##
        # Resize media window
        while width + 40 < current_mode.HzRes and height + 40 < current_mode.VtRes:
            width = width + 40
            height = height + 40

            ##
            # Resize
            media_handle.set_position(0, 0, width, height)

            ##
            # Wait for 2 seconds for app to stabilize after resize
            time.sleep(2)

        ##
        # Close media player
        flipq_helper.play_close_media(False)

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
    # @brief        test_03_media_cancel_queue_move_window Test to verify FlipQ functionality while
    #                                                       dragging video application.
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-ACTION') != "MOVE_WINDOW",
                     "Skip the test step as the action type is not cancel queue and move window")
    def test_03_media_cancel_queue_move_window(self):
        ##
        # Get current display configuration.
        current_config = self.config.get_current_display_configuration()

        ##
        # Get current applied mode.
        current_mode = self.config.get_current_mode(current_config.displayPathInfo[0].targetId)

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_move_window_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        media_handle = flipq_helper.play_close_media(True, False)

        left, top, right, bottom = 0, 0, 400, 400
        media_handle.set_position(left, top, right, bottom)

        ##
        # Move video playback window
        while right + 40 < current_mode.HzRes and bottom + 40 < current_mode.VtRes:
            left = left + 40
            top = top + 40
            right = right + 40
            bottom = bottom + 40

            ##
            # Move window
            media_handle.set_position(left, top, right, bottom)

            ##
            # Wait for 2 seconds for app to stabilize after move window
            time.sleep(2)

        ##
        # Close media player
        flipq_helper.play_close_media(False)

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
    logging.info("Test Purpose: Basic test to verify FlipQ cancel functionality with video playback")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)