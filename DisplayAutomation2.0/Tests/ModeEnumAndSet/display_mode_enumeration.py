#######################################################################################################################
# @file         display_mode_enumeration.py
# @brief        This file contains validation of different mode enumarations for given DP/HDMI display
# @details      display_mode_enumeration.py applies different modes and verify DE for each of them.
#
# @author       Golwala Ami
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.ModeEnumAndSet.display_mode_enumeration_base import *

##
# @brief        A class which has test method to apply modeset.
class ModeEnumAndSet(ModeEnumAndSetBase):

    ##
    # @brief        Unit-test runTest function.
    # @return       None
    def runTest(self):
        ##
        # Apply and verify mode set.
        self.verify_mode_enum_and_modeset()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)