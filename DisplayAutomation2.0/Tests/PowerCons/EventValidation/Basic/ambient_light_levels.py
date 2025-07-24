########################################################################################################################
# @file         ambient_light_levels.py
# @details      @ref ambient_light_levels.py <br>
#               This file implements ambient light levels scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment

from Tests.PowerCons.EventValidation.Basic.event_validation_base import *


##
# @brief        This class contains tests to verify ambient light levels scenario
class AmbientLightLevels(EventValidationBase):

    ##
    # @brief        This is a test function to test ambient light levels and then check validators.
    # @return       None
    def test_ambient_light_levels(self):

        als_override_enable_lux_values = [0, 100, 450, 501, 1000, 1499, 10000, 14999, 20000, 2000, 450]

        logging.info("Applying various lux values - {0}".format(', '.join(map(str, als_override_enable_lux_values))))
        for lux in als_override_enable_lux_values:
            # Applying lux with als override
            logging.info("Step: Applying lux= {0}, override= True".format(lux))
            if powercons_escapes.als_override(True, lux) is not True:
                self.fail("Failed to apply lux= {0} (Test Issue)".format(lux))
            logging.info("\tApplied lux successfully")

            logging.info("Waiting for 5 seconds..")
            time.sleep(5)

        self.check_validators()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
