########################################################################################################################
# @file         test_psr_entry_exit.py
# @brief        Test for DC state in frame update scenario
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains DC States tests with PSR entry/exit
class DcStatePsrEntryExit(DCStatesBase):

    ##
    # @brief        This function verifies DC5/6 with PSR entry/exit
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6"])
    # @endcond
    def t_10_test_dc5_dc6(self):
        for adapter in dut.adapters.values():
            logging.info("Step: Verifying DC5/6 with Idle desktop")
            if dc_state.verify_dc5_dc6(adapter, method='APP') is False:
                self.fail("DC5/6 verification with app failed")
            logging.info("\tDC5/6 verification with app is successful")

    ##
    # @brief        This function verifies DC5/6 with PSR entry/exit
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V"])
    # @endcond
    def t_11_test_dc6v(self):
        for adapter in dut.adapters.values():
            logging.info("Step: Verifying DC6V with App")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6V verification with app failed")
            logging.info("\tDC6V verification with app is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DcStatePsrEntryExit))
    test_environment.TestEnvironment.cleanup(test_result)
