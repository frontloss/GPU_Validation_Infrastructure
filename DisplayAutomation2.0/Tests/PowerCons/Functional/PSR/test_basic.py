########################################################################################################################
# @file         test_basic.py
# @brief        Test for PSR/LRR basic scenarios
#
# @author       Rohit Kumar
########################################################################################################################

from Libs.Core import display_power
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.PSR.psr_base import *

##
# @brief        This class contains basic PSR tests
class TestBasic(PsrBase):

    ##
    # @brief        This function validates PSR with AC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC"])
    # @endcond
    def t_11_psr_basic_ac(self):
        self.validate_feature(display_power.PowerSource.AC)

    ##
    # @brief        This function validates PSR with DC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC"])
    # @endcond
    def t_12_psr_basic_dc(self):
        self.validate_feature(display_power.PowerSource.DC)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestBasic))
    test_environment.TestEnvironment.cleanup(test_result)
