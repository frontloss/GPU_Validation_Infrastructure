########################################################################################################################
# @file         display_off.py
# @details      @ref display_off.py <br>
#               This file implements display off scenario for all display pc feature testing.
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment

from Tests.PowerCons.EventValidation.Basic.event_validation_base import *


##
# @brief        This class contains tests for events with display off scenarios
class DisplayOff(EventValidationBase):
    ##
    # @brief        This function verifies the setting of display time-out
    # @return       None
    def test_display_off(self):

        logging.info(" SCENARIO: {0} ".format(self.cmd_test_name.upper()).center(common.MAX_LINE_WIDTH, "*"))

        # Setting the display time-out to 1 minute
        logging.info("Setting display time-out to 1 minute")
        if desktop_controls.set_time_out(desktop_controls.TimeOut.TIME_OUT_DISPLAY, 1) is False:
            self.fail("Failed to set display time-out to 1 minute (Test Issue)")
        logging.info("\tSet display time-out to 1 minute successfully")

        logging.info("Waiting for 120 seconds..")
        time.sleep(120)

        self.check_validators()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
