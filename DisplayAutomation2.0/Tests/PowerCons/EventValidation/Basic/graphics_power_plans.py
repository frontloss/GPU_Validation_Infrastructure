########################################################################################################################
# @file         graphics_power_plans.py
# @brief        This file implements graphics power plans scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.PowerCons.EventValidation.Basic.event_validation_base import *


##
# @brief        This class contains tests for events with graphics power plans scenario
class GraphicsPowerPlans(EventValidationBase):

    ##
    # @brief        This function verifies the features with setting of a power scheme
    # @return       None
    def test_graphics_power_plans(self):

        for power_line_state in [display_power.PowerSource.DC, display_power.PowerSource.AC]:
            if self.display_power_.set_current_powerline_status(power_line_state) is False:
                self.fail("Failed t set current power line status to {0} (Test Issue)".format(
                    power_line_state.name))

            for power_scheme in [display_power.PowerScheme.POWER_SAVER,
                                 display_power.PowerScheme.HIGH_PERFORMANCE,
                                 display_power.PowerScheme.BALANCED]:
                # WA for legacy platform - 14010392021
                if common.PLATFORM_NAME in common.PRE_GEN_11_PLATFORMS and self.panel_config == "SEAMLESS_DRRS":
                    power_scheme = display_power.PowerScheme.POWER_SAVER
                logging.info("Setting current power scheme to {0}".format(power_scheme.name))
                if self.display_power_.set_current_power_scheme(power_scheme) is False:
                    self.fail("Failed to set current power scheme to {0}(Test Issue)".format(
                        power_scheme.name))
                logging.info("\tSet current power scheme successfully")

                logging.info("Waiting for 5 seconds..")
                time.sleep(5)

        if self.display_power_.set_current_powerline_status(display_power.PowerSource.DC) is False:
            self.fail("Failed to set current power line status to DC (Test Issue)")

        logging.info("Waiting for 5 seconds..")
        time.sleep(5)

        self.check_validators()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
