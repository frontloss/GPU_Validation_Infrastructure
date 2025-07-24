########################################################################################################################
# @file         test_ac_dc.py
# @brief        Test for DC state with AC/DC switch
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains DC States tests in AC/DC power source switch
class TestAcDc(DCStatesBase):

    ##
    # @brief        This function verifies DC5/6 in AC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6", "AC"])
    # @endcond
    def t_10_test_dc5_dc6_in_ac(self):
        for adapter in dut.adapters.values():
            if self.display_power_.set_current_powerline_status(PowerSource.AC) is False:
                self.fail("Failed to switch power line status to AC (Test Issue)")
            logging.info("Step: Verifying DC5/6 with Idle desktop")
            if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                self.fail("DC5/6 verification failed")
            logging.info("\tDC5/6 verification is successful")

    ##
    # @brief        This function verifies DC5/6 in DC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6", "DC"])
    # @endcond
    def t_11_test_dc5_dc6_in_dc(self):
        for adapter in dut.adapters.values():
            if self.display_power_.set_current_powerline_status(PowerSource.DC) is False:
                self.fail("Failed to switch power line status to DC (Test Issue)")
            logging.info("Step: Verifying DC5/6 with Idle desktop")
            if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                self.fail("DC5/6 verification failed")
            logging.info("\tDC5/6 verification is successful")

    ##
    # @brief        This function verifies DC6V in AC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V", "AC"])
    # @endcond
    def t_12_test_dc6v_in_ac(self):
        for adapter in dut.adapters.values():
            if self.display_power_.set_current_powerline_status(PowerSource.AC) is False:
                self.fail("Failed to switch power line status to AC (Test Issue)")
            logging.info("Step: Verifying DC6V with App")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6V verification with app failed")
            logging.info("\tDC6V verification with app is successful")

    ##
    # @brief        This function verifies DC6V in DC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V", "DC"])
    # @endcond
    def t_13_test_dc6v_in_dc(self):
        for adapter in dut.adapters.values():
            if self.display_power_.set_current_powerline_status(PowerSource.DC) is False:
                self.fail("Failed to switch power line status to DC (Test Issue)")
            logging.info("Step: Verifying DC6V with App")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6V verification with app failed")
            logging.info("\tDC6V verification with app is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestAcDc))
    test_environment.TestEnvironment.cleanup(test_result)
