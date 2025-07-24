##
# @file         flipq_media_basic.py
# @brief        Basic test to verify FlipQ functionality during windowed/fullscreen video playback.
#                   * Play media content using Movies & Tv.
#                   * Verify the ETL's for flip time and queuing.
# @author       Anjali Shetty

import logging
import sys
import time
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.FlipQ import flipq_base
from Tests.FlipQ import flipq_helper


##
# @brief    FlipQ media basic test
class FlipQMediaBasic(flipq_base.FlipQBase):

    ##
    # @brief        test_01_basic Basic test to verify FlipQ functionality during windowed video playback
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "BASIC",
                     "Skip the  test step as the action type is not basic")
    def test_01_basic(self):
        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_windowed_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Play media in windowed mode
        flipq_helper.play_close_media(True, False)

        ##
        # Wait for a minute during video playback
        time.sleep(60)

        ##
        # Close media player
        flipq_helper.play_close_media(False)

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_windowed_scenario")

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
    # @brief        test_02_basic Basic test to verify FlipQ functionality during fullscreen video playback
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "BASIC",
                     "Skip the  test step as the action type is not basic")
    def test_02_basic(self):
        ##
        # Play media in fullscreen mode
        flipq_helper.play_close_media(True, True)

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_fullscreen_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Wait for a minute during video playback
        time.sleep(60)

        ##
        # Close media player
        flipq_helper.play_close_media(False)

        ##
        # Stop ETL capture
        etl_file = flipq_helper.stop_etl_capture("After_fullscreen_scenario")

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
    logging.info("Test Purpose: Basic test to verify FlipQ functionality during video playback")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
