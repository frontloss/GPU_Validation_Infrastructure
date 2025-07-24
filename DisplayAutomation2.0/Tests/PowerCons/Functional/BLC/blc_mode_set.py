########################################################################################################################
# @file         blc_mode_set.py
# @brief        Test for BLC mode set scenario
#
# @author       Ashish Tripathi
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.BLC.blc_base import *


##
# @brief        This class contains BLC tests with mode set
class BlcModeSet(BlcBase):
    ##
    # @brief        This test verifies BLC with mode set
    # @return       Nones
    def test_blc_mode_set(self):
        self.setup_and_validate_blc(blc.Scenario.MODE_SET)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcModeSet'))
    test_environment.TestEnvironment.cleanup(outcome)

