########################################################################################################################
# @file         blc_monitor_timeout.py
# @brief        Test for BLC Monitor Time out scenario
#
# @author       Ashish Tripathi
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.BLC.blc_base import *


##
# @brief        This class contains BLC tests with monitor timeout
class BlcTimeOut(BlcBase):
    ##
    # @brief        This test verifies BLC with monitor timeout
    # @return       None
    def test_blc_monitor_time_out(self):
        self.setup_and_validate_blc(blc.Scenario.MONITOR_TIME_OUT)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcTimeOut'))
    test_environment.TestEnvironment.cleanup(outcome)

