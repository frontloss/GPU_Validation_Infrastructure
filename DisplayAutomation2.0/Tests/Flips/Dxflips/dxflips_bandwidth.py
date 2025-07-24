##
# @file         dxflips_bandwidth.py
# @brief        This test script verifies for power saving.
#               Test consists of below scenarios:
#               * Plays Dxapp and verifies for bandwidth saving with endurance gaming.
# @author       Anjali Shetty

import logging
import sys
import time
import unittest

from Libs.Core import winkb_helper
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips import flip_helper
from Tests.Flips.Dxflips import dxflips_base


##
# @brief    Contains test functions that are used to determine power saving
class DxflipsBandwidth(dxflips_base.DxflipsBase):
    ##
    # @brief     Helper function to exercise the scenario
    # @return    IO bandwidth value
    def __execute_scenario(self):
        if self.app == "FLIPAT":
            fps_pattern, fps_pattern2 = flip_helper.setFps(self.fps)
        else:
            fps_pattern = None
            fps_pattern2 = None

        ##
        # Open any app
        flip_helper.play_app(self.app, bfullscreen=True, fps_pattern=fps_pattern, fps_pattern2=fps_pattern2)

        ##
        # Wait for 2 seconds for app to stabilize
        time.sleep(2)

        bandwidth = flip_helper.get_io_bandwidth_using_socwatch()
        if not bandwidth:
            flip_helper.report_to_gdhm(self.feature, "Failed to fetch bandwidth details", driver_bug=False)
            self.fail("Failed to fetch bandwidth details")

        ##
        # Close the application
        flip_helper.close_app(self.app)

        logging.info("Closed {0} App".format(self.app))

        return bandwidth

    ##
    # @brief    Test function to verify bandwidth saving with endurance gaming
    # @return   None
    # @cond
    @unittest.skipIf(flip_helper.get_action_type('-SCENARIO') != "ENDURANCE_BW",
                     "Skip the test step as the action type is not endurance bandwidth")
    # @endcond
    def test_01_endurance_gaming_io_bandwidth(self):
        ##
        # Minimize all windows
        winkb_helper.press('WIN+M')

        ##
        # Set DC mode
        result = flip_helper.ac_dc_switch(True)
        self.assertEquals(result, True, "Aborting the test as setting the power line status to DC failed")

        ##
        # Get bandwidth info with feature enabled
        bw_feature_enabled = self.__execute_scenario()

        ##
        # Disable the feature: To do post escape changes

        ##
        # Get bandwidth info with feature disabled
        bw_feature_disabled = self.__execute_scenario()

        ##
        # Set AC mode (Restore back)
        result = flip_helper.ac_dc_switch(False)
        self.assertEquals(result, True, "Aborting the test as setting the power line status to AC failed")

        if bw_feature_enabled > bw_feature_disabled:
            flip_helper.report_to_gdhm(self.feature, "No expected bandwidth saving with feature enabled",
                                       driver_bug=False)
            self.fail("There is no expected bandwidth saving with feature enabled")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose:Test to verify bandwidth saving while running any async application")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
