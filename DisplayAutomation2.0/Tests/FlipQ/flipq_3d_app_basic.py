##
# @file         flipq_3d_app_basic.py
# @brief        Basic test to verify FlipQ functionality while running 3D application in windowed/fullscreen mode.
#                   * Run ClassicD3D Application.
#                   * Verify the ETL's for flip time and queuing.
# @author       Anjali Shetty

import logging
import subprocess
import sys
import time
import unittest

from Libs.Core import winkb_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.FlipQ import flipq_base
from Tests.FlipQ import flipq_helper
from Tests.FlipQ.flipq_base import flip_base


##
# @brief    FlipQ 3D App basic test
class FlipQ3DAppBasic(flipq_base.FlipQBase):

    ##
    # @brief        test_01_basic Basic test to verify FlipQ functionality while running 3D application in
    #                             windowed mode
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "BASIC",
                     "Skip the  test step as the action type is not basic")
    def test_01_basic(self):
        ##
        # Verify that interval and buffer data is not None
        if flip_base.interval is None or flip_base.buffer is None:
            self.fail("Incorrect command line argument")

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_windowed_scenario") is False:
            self.fail("Failed to start ETL capture")

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
        # Wait for a minute while 3D app is running
        time.sleep(60)

        ##
        # Close 3D application
        self.app.terminate()
        logging.info("Closed 3D application")

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
    # @brief        test_02_basic Basic test to verify FlipQ functionality while running 3D application in
    #                             fullscreen mode
    # @param[in]    self
    # @return       None
    @unittest.skipIf(flipq_helper.get_action_type('-SCENARIO') != "BASIC",
                     "Skip the  test step as the action type is not basic")
    def test_02_basic(self):
        ##
        # Verify that interval and buffer data is not None
        if flip_base.interval is None or flip_base.buffer is None:
            self.fail("Incorrect command line argument")

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

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
        # Time for application to stabilize
        time.sleep(5)

        ##
        # Start ETL capture
        if flipq_helper.start_etl_capture("Before_fullscreen_scenario") is False:
            self.fail("Failed to start ETL capture")

        ##
        # Switch to fullscreen
        winkb_helper.press('F5')

        ##
        # Wait for a minute while 3D app is running
        time.sleep(60)

        ##
        # Close 3D application
        self.app.terminate()
        logging.info("Closed 3D application")

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
    logging.info("Test Purpose: Basic test to verify FlipQ functionality while running 3D application")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
