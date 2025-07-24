########################################################################################################################
# @file         test_basic.py
# @brief        Tests for DC5/DC6/DC6v/DC9 state in IDLE desktop & app scenario
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains basic tests for DC5/DC6/DC6v/DC9 states
class TestBasic(DCStatesBase):

    ##
    # @brief        This function tests DC5/6 with Idle desktop
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6"])
    # @endcond
    def t_10_test_dc5_dc6(self):
        for adapter in dut.adapters.values():
            logging.info("Verifying DC5/6 with Idle desktop")
            if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                self.fail("DC5/6 verification with idle desktop failed")
            logging.info("\tDC5/6 verification with idle desktop is successful")

    ##
    # @brief        This function tests DC6v
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V"])
    # @endcond
    def t_12_test_dc6v(self):
        for adapter in dut.adapters.values():
            logging.info("STEP 1: Verifying DC6v with App")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6V verification with app failed")
            logging.info("\tDC6V verification with app is successful")

    ##
    # @brief        This function DC9 with CS/S3
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC9"])
    # @endcond
    def t_11_state_dc9_basic(self):
        for adapter in dut.adapters.values():
            if dc_state.verify_dc9(adapter) is False:
                self.fail("DC9 verification failed")
            logging.info("\tDC9 verification is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestBasic))
    test_environment.TestEnvironment.cleanup(test_result)
