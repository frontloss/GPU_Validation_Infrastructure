########################################################################################################################
# @file         display_shift_basic.py
# @brief        Test calls for Control Library of display shift and verifies return status of the API.
#                   * Enumerate Display API.
#                   * Mux Properties/Display shift API.
# @author       Nivetha.B
########################################################################################################################

import sys
import unittest
import logging

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Shift import display_shift_base


##
# @brief       Verifies Basic display shift between Integrated and Discrete
class DisplayShiftBasic(display_shift_base.DisplayShiftBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Display shift Basic")
        for cycle_no in range(0, self.iterations):
            if self.iterations > 1:
                logging.info("--------------Test cycle {0}-----------------".format(cycle_no + 1))

            # Display shift from Integrated to Discrete
            self.verify_display_shift()
            # Display shift from Discrete to Integrated
            self.verify_display_shift()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Display Shift basic Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
