########################################################################################################################
# @file         bfr_power_events.py
# @brief        Contains tests for validating BFR after various power events
# @details      Basic functional tests are covering below scenarios:
#               * BFR verification in FULL SCREEN mode for various power events
#               * All tests will be executed on VRR panel with VRR enabled. BFR is expected to be working in all above
#               scenarios.
#
# @author       Gopikrishnan R
########################################################################################################################
from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.BFR.bfr_base import *


##
# @brief        This class contains Contains tests for validating BFR after various power events
#               This class inherits the BfrBase class.
class BfrPowerEvents(BfrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        BFR verification after resuming from S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_11_power_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
            self.fail("S3 is NOT supported on the system(Planning Issue)")
        # set static RR
        self.verify_with_power_event(display_power.PowerEvent.S3)

    ##
    # @brief        BFR verification after resuming from CS
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_12_power_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("CS is NOT supported on the system (Planning Issue)")
        self.verify_with_power_event(display_power.PowerEvent.CS)

    ##
    # @brief        BFR verification after resuming from S4
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_13_power_s4(self):
        self.verify_with_power_event(display_power.PowerEvent.S4)

    ##
    # @brief        BFR verification in MAXIMISED mode
    # @param[in]    power_event        : indicates the power event to go before running bfr workload
    # @return       None
    def verify_with_power_event(self, power_event):
        negative = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.bfr_caps.is_bfr_supported:
                    negative = not(bfr.is_dynamic_rr(panel))
                    break
        # consider as negative case in case of static RR
        if not self.bfr_basic(negative=negative, power_event=power_event):
            self.fail(f"FAIL : Power_event Test : BFR verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BfrPowerEvents))
    TestEnvironment.cleanup(test_result)
