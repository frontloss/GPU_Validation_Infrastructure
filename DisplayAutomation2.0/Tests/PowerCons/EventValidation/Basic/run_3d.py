########################################################################################################################
# @file         run_3d.py
# @details      @ref run_3d.py <br>
#               This file implements run 3d scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################

import subprocess

from Libs.Core.test_env import test_environment
from Tests.PowerCons.EventValidation.Basic.event_validation_base import *


##
# @brief        This class contains tests for events with run 3d
class Run3d(EventValidationBase):
    ##
    # @brief        This function verifies events with multi-animation app
    # @return       None
    def test_run_3d(self):

        if os.path.exists(MULTI_ANIMATION_EXE) is False:
            self.fail("File does NOT exist = {0} (Test Issue)".format(MULTI_ANIMATION_EXE))

        app_arguments = [
            MULTI_ANIMATION_EXE,
            '-forcevsync:0' if self.app_flip_type == 'async' else '-forcevsync:1',
            '-fullscreen' if self.app_window_state == 'fullscreen' else ''
        ]

        # Launch the DirectX app with the arguments
        logging.info("Step: Opening MultiAnimation app with FlipType= {0} in {1} mode".format(
            self.app_flip_type, self.app_window_state))
        try:
            self.app_handle = subprocess.Popen(app_arguments)
        except Exception as e:
            logging.error(e)
            self.fail("Failed to launch MultiAnimation.exe (Test Issue)")
        logging.info("\tLaunched MultiAnimation.exe successfully")

        logging.info("Waiting for 60 seconds..")
        time.sleep(60)

        logging.info("Closing MultiAnimation app..")
        self.app_handle.terminate()
        self.app_handle = None

        self.check_validators()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
