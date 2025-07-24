########################################################################################################################
# @file         pfn_basic.py
# @brief        Basic test to verify periodic frame notification.
#               * Apply display configuration as mentioned in the command line.
#               * Run WHCK tool
#               * Verify periodic frame notification
# @author       Ilamparithi Mahendran
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips.PeriodicFrameNotification import pfn_base

##
# @brief    Contains function to check basic periodic frame notification test
class PeriodicFrameNotificationBaseBasic(pfn_base.PeriodicFrameNotificationBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        for config_list in self.display_config_list:
            if not self.display_config.set_display_configuration_ex(config_list[0], config_list[1]):
                self.fail("Display Configuration failed")

            self.run_test_tool()

            if not self.verify_periodic_frame_notification():
                self.report_to_gdhm_periodic_frame_notification_failure()
                logging.critical("Periodic Frame Notification Test Failed")
                self.fail("Periodic Frame Notification Test Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
