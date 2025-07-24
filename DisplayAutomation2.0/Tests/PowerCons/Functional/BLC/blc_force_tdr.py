########################################################################################################################
# @file         blc_force_tdr.py
# @brief        Test for BLC force tdr scenario
#
# @author       Ashish Tripathi
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.BLC.blc_base import *


##
# @brief        This class contains BLC tests with force TDR
class BlcForceTdr(BlcBase):
    ##
    # @brief        This test verifies Blc with force TDR
    # @return       None
    def test_blc_force_tdr(self):
        self.setup_and_validate_blc(blc.Scenario.DISPLAY_TDR)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcForceTdr'))
    test_environment.TestEnvironment.cleanup(outcome)
