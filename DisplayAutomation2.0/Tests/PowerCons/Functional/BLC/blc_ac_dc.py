########################################################################################################################
# @file         blc_ac_dc.py
# @brief        Tests for BLC in AC/DC scenario
#
# @author       Ashish Tripathi
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.BLC.blc_base import *


##
# @brief        This class contains Blc tests with AC/DC switch
class BlcAcDc(BlcBase):
    ##
    # @brief        Test function is to verify blc with AC/DC switch
    # @return       None
    def test_blc_ac_dc(self):
        self.setup_and_validate_blc(blc.Scenario.AC_DC_SWITCH)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcAcDc'))
    test_environment.TestEnvironment.cleanup(outcome)
