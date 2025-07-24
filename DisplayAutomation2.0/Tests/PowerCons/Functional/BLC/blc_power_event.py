########################################################################################################################
# @file         blc_power_event.py
# @brief        Test for BLC power event (CS/S3/S4) scenario
#
# @author       Ashish Tripathi
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.BLC.blc_base import *


##
# @brief        This class contains BLC tests with various power events
class BlcPowerEvent(BlcBase):
    ##
    # @brief        This test verifies BLC with S3/CS/S4 power event
    # @return       None
    def test_blc_power_event(self):
        if self.cmd_line_param[0]['SELECTIVE'] == ['S3']:
            self.setup_and_validate_blc(blc.Scenario.POWER_EVENT_S3)
        elif self.cmd_line_param[0]['SELECTIVE'] == ['CS']:
            self.setup_and_validate_blc(blc.Scenario.POWER_EVENT_CS)
        elif self.cmd_line_param[0]['SELECTIVE'] == ['S4']:
            self.setup_and_validate_blc(blc.Scenario.POWER_EVENT_S4)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('BlcPowerEvent'))
    test_environment.TestEnvironment.cleanup(outcome)
