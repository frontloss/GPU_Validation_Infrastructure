########################################################################################################################
# @file         test_power_events.py
# @brief        Tests for DC state in IDLE desktop scenario
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core import display_power
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains DC States tests with power events
class TestPowerEvent(DCStatesBase):

    ##
    # @brief        This function verifies DC5/DC6 with Idle desktop with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6", "CS"])
    # @endcond
    def t_10_state_dc5_dc6_cs(self):
        for adapter in dut.adapters.values():
            if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
                self.fail("CS is NOT supported on the system (Planning Issue)")

            if self.display_power_.invoke_power_event(display_power.PowerEvent.CS,
                                                      common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('FAILED to invoke power event CS')
            logging.info("Step: Verifying DC5/6 with Idle desktop with CS")
            if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                self.fail("DC5/6 verification with idle failed")
            logging.info("\tDC5/6 verification with idle is successful")

    ##
    # @brief        This function verifies DC5/DC6 with Idle desktop with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6", "S3"])
    # @endcond
    def t_11_state_dc5_dc6_s3(self):
        for adapter in dut.adapters.values():
            if self.display_power_.invoke_power_event(display_power.PowerEvent.S3,
                                                      common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('FAILED to invoke power event S3')

            if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
                self.fail("S3 is NOT supported on the system (Planning Issue)")
            logging.info("Step: Verifying DC5/6 with Idle desktop with S3")
            if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                self.fail("DC5/6 verification with idle failed")
            logging.info("\tDC5/6 verification with idle is successful")

    ##
    # @brief        This function verifies DC5/DC6 with Idle desktop with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6", "S4"])
    # @endcond
    def t_12_state_dc5_dc6_s4(self):
        for adapter in dut.adapters.values():
            if self.display_power_.invoke_power_event(display_power.PowerEvent.S4,
                                                      common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('FAILED to invoke power event S4')
            logging.info("Step: Verifying DC5/6 with Idle desktop with S4")
            if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                self.fail("DC5/6 verification with idle failed")
            logging.info("\tDC5/6 verification with idle is successful")

    ##
    # @brief        This function verifies DC6V with Idle desktop with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V", "CS"])
    # @endcond
    def t_13_state_dc6v_cs(self):
        for adapter in dut.adapters.values():
            if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
                self.fail("CS is NOT supported on the system (Planning Issue)")
            if self.display_power_.invoke_power_event(display_power.PowerEvent.CS,
                                                      common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('Failed to invoke power event CS')

            logging.info("Step: Verifying DC6v with CS in APP scenario")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6v verification with app failed")
            logging.info("\t DC6v verification with app is successful")

    ##
    # @brief        This function verifies DC6V with Idle desktop with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V", "S3"])
    # @endcond
    def t_14_state_dc6v(self):
        for adapter in dut.adapters.values():
            if self.display_power_.is_power_state_supported(display_power.PowerEvent.S3) is False:
                self.fail("S3 is NOT supported on the system (Planning Issue)")

            if self.display_power_.invoke_power_event(display_power.PowerEvent.S3,
                                                      common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('FAILED to invoke power event S3')

            logging.info("Step: Verifying DC6v with S3 in APP scenario")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6V verification with app failed")
            logging.info("\tDC6V verification with app is successful")

    ##
    # @brief        This function verifies DC6V with Idle desktop with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V", "S4"])
    # @endcond
    def t_15_state_dc6V_s4(self):
        for adapter in dut.adapters.values():
            if self.display_power_.invoke_power_event(display_power.PowerEvent.S4,
                                                      common.POWER_EVENT_DURATION_DEFAULT) is False:
                self.fail('FAILED to invoke power event S4')

            logging.info("Step: Verifying DC6V with App")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6V verification with app failed")
            logging.info("\tDC6V verification with app is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestPowerEvent))
    test_environment.TestEnvironment.cleanup(test_result)