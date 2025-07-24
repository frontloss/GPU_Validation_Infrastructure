########################################################################################################################
# @file        power_event.py
# @brief      This file implements power event scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.EventValidation.Basic.event_validation_base import *


##
# @brief        This class contains tests for events with different power events
class PowerEvent(EventValidationBase):
    ##
    # @brief        This function verifies events with different power events
    # @return       None
    def test_power_event(self):

        for power_line_state in [display_power.PowerSource.AC, display_power.PowerSource.DC]:
            if self.display_power_.set_current_powerline_status(power_line_state) is False:
                self.fail("Failed to set current power line status to {0} (Test Issue)".format(
                    power_line_state.name))
            time.sleep(2)  # Delay before next event

        power_event = display_power.PowerEvent[self.power_event_type.upper()]
        if self.display_power_.invoke_power_event(power_event) is False:
            self.fail("Failed to initiate and resume from {0} (Test Issue)".format(self.power_event_type))

        logging.info("Waiting for 30 seconds..")
        time.sleep(30)

        self.check_validators()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
