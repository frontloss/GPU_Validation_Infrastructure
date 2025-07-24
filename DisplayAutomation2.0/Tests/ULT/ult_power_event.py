##########################################################################################################################################################################
# @file         ult_power_event.py
# @brief        Intention of this test is to verify Power Events CS/S3 and S4
# @details      Test steps are as follows
#               * Invoke S3/CS based on system support
#               * Invoke S4 once the last step is successful
#
# @author       Gowtham K L
##########################################################################################################################################################################
import sys
import unittest
import logging

from Libs.Core import display_power
from Libs.Core.logger import html
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Modules import common


##
# @brief        This class contains Power Event test ULT
class UltPowerEvent(unittest.TestCase):
    display_power_ = display_power.DisplayPower()

    ##
    # @brief        Test to invoke power event S3/CS
    # @return       None
    def test_11_s3_cs(self):
        power_event = None
        # Check for S3/CS support
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            power_event = display_power.PowerEvent.CS
        elif self.display_power_.is_power_state_supported(display_power.PowerEvent.S3):
            power_event = display_power.PowerEvent.S3
        else:
            self.fail("CS/S3 not supported (Planning issue)")

        # Invoke Power event (S3/CS based on support)
        html.step_start(f"Invoking Power event : {display_power.PowerEvent(display_power.PowerEvent.CS)}")
        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail(f"FAILED to invoke power event {display_power.PowerEvent(power_event)}")
        logging.info(f"Successfully resumed back from {power_event}")


    ##
    # @brief        Test to invoke power event S4
    # @return       None
    def test_12_s4(self):
        html.step_start(f"Invoking Power event : {display_power.PowerEvent(display_power.PowerEvent.CS)}")
        if self.display_power_.invoke_power_event(display_power.PowerEvent.S4, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail(f"FAILED to invoke power event {display_power.PowerEvent(display_power.PowerEvent.CS)}")
        logging.info(f"Successfully resumed back from {display_power.PowerEvent(display_power.PowerEvent.CS)}")
        html.step_end()



if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)

