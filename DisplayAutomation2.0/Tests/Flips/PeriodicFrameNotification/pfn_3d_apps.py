########################################################################################################################
# @file         pfn_3d_apps.py
# @brief        Test to verify periodic frame notification when 3d app is running.
#               * Apply display configuration as mentioned in the command line.
#               * Run 3d Application.
#               * Run WHCK tool.
#               * Verify periodic frame notification.
# @author       Ilamparithi Mahendran
########################################################################################################################
import logging
import os
import subprocess
import sys
import time
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips.PeriodicFrameNotification import pfn_base
from Libs.Core.test_env import test_context
from Libs.Core import winkb_helper

##
# @brief    Contains function to check basic periodic frame notification test when 3d app is playing
class PeriodicFrameNotificationBase3DApps(pfn_base.PeriodicFrameNotificationBase):


    ##
    # @brief            To open the ClassicD3D app and run the application
    # @return           void
    def performTest(self):
        self.app = subprocess.Popen(r'TestStore/TestSpecificBin/Flips/ClassicD3D/ClassicD3d.exe darken',
                                    cwd=os.path.join(test_context.TEST_STORE_FOLDER, 'TestSpecificBin', 'Flips',
                                                     'ClassicD3D'))
        time.sleep(3)
        winkb_helper.press('ALT_ENTER')
        time.sleep(3)

        self.run_test_tool()

        self.app.terminate()


    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        for config_list in self.display_config_list:
            if not self.display_config.set_display_configuration_ex(config_list[0], config_list[1]):
                self.fail("Display Configuration failed")

            self.performTest()

            if not self.verify_periodic_frame_notification():
                self.report_to_gdhm_periodic_frame_notification_failure()
                logging.critical("Periodic Frame Notification Test Failed")
                self.fail("Periodic Frame Notification Test Failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
