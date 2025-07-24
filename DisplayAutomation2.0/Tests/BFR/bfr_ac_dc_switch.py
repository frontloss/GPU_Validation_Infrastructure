########################################################################################################################
# @file         bfr_ac_dc_switch.py
# @brief        Contains AC/DC switch cases for BFR
# @details      Basic functional tests are covering below scenarios:
#               * BFR verification in FULL SCREEN mode, when mode is switched from DC to AC
#               * All tests will be executed on VRR panel with VRR enabled. BFR is expected to be working in all above
#               scenarios.
#
# @author       Gopikrishnan R
########################################################################################################################
from Libs.Core import enum, display_power
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.BFR.bfr_base import *


##
# @brief        This class contains basic BFR test with DC to AC switch
#               This class inherits the BfrBase class.
class BfrAcDcSwitch(BfrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        BFR verification in maximized modein AC Mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC"])
    # @endcond
    def t_11_power_ac(self):
        self.verify_with_power_source(display_power.PowerSource.AC)

    ##
    # @brief        BFR verification in maximized modein DC Mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC"])
    # @endcond
    def t_12_power_dc(self):
        self.verify_with_power_source(display_power.PowerSource.DC)

    ##
    # @brief        BFR verification in MAXIMISED mode
    # @param[in]    power_source
    # @return       None
    def verify_with_power_source(self, power_source):
        max_trials = 3
        result = False
        for trial in range(max_trials):
            result = self.validate_bfr(duration=self.duration, power_source=power_source)[0]
            if result:
                break
        if not result:
            self.fail(f"FAIL : BFR with {power_source} switch : BFR verification failed in all {max_trials} attempts")
        logging.info(f"\tPASS: BFR with {power_source} switch : BFR verification passed successfully")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BfrAcDcSwitch))
    TestEnvironment.cleanup(test_result)
