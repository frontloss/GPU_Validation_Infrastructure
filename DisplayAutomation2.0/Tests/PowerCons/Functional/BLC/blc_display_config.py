########################################################################################################################
# @file         blc_display_config.py
# @brief        Test for BLC display config scenario
#
# @author       Ashish Tripathi
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.BLC.blc_base import *


##
# @brief        This class contains BLC tests with display config
class BlcDisplayConfig(BlcBase):

    ##
    # @brief        This test verifies Blc with display config
    # @return       None
    def test_blc_display_config(self):
        self.setup_and_validate_blc(blc.Scenario.DISPLAY_CONFIG)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcDisplayConfig'))
    test_environment.TestEnvironment.cleanup(outcome)

