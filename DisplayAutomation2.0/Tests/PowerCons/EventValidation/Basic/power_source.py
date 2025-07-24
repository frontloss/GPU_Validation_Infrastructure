########################################################################################################################
# @file         power_source.py
# @brief        This file implements power source scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.EventValidation.Basic.event_validation_base import *


##
# @brief        This class contains tests for events with power source
class PowerSource(EventValidationBase):
    ##
    # @brief        This function verifies events with different power sources
    # @return       None
    def test_power_source(self):

        for i in range(5):
            for power_line_state in [display_power.PowerSource.AC, display_power.PowerSource.DC]:
                if self.display_power_.set_current_powerline_status(power_line_state) is False:
                    self.fail("Failed to set current power line status to {0} (Test Issue)".format(power_line_state.name))

                logging.info("Waiting for 5 seconds..")
                time.sleep(5)

        self.check_validators()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
