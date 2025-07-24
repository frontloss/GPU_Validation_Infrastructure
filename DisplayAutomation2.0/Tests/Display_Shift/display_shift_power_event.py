########################################################################################################################
# @file         display_shift_power_event.py
# @brief        Verifies Display shift between Integrated and Discrete before and after power events.
# @details      Test scenario:
#                   1. Boot system with EDP
#                   2. Verify display shift after power event (CS/S3/S4)
# @author       Nivetha.B
########################################################################################################################

import sys
import unittest
import logging

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper import control_api_wrapper
from Tests.Display_Shift import display_shift_base


##
# @brief   Verifies Display shift after power event (CS/S3/S4)
class DisplayShiftPowerEvent(display_shift_base.DisplayShiftBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Display shift Power event")
        for cycle_no in range(0, self.iterations):
            if self.iterations > 1:
                logging.info("--------------Test cycle {0}-----------------".format(cycle_no + 1))

            self.verify_display_shift()
            self.base_invoke_power_event()
            self.verify_display_shift(True)
            self.base_invoke_power_event()
            self.verify_display_shift(True)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Display Shift Power event Verification')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
