########################################################################################################################
# @file         test_dc_states_with_hotplug.py
# @brief        Tests to verify DC states before and after hotplug and hotunplug
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief       This class contains tests for DCStates with hotplug and unplug of external panel
class TestDcStateWithHotPlugUnplug(DCStatesBase):

    ##
    # @brief        This test verifies DC5/DC6 state with hotplug and unplug of external panel
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC5", "DC6"])
    # @endcond
    def t_10_dc5_dc6_hotplug(self):
        for adapter in dut.adapters.values():
            if len(self.lfp_panels) == 1:
                if self.display_config_.set_display_configuration_ex(enum.SINGLE, [self.lfp_panels[0].port]) is False:
                    self.fail(f"Failed to apply DisplayConfig SINGLE {[self.lfp_panels[0].port]}")
                logging.info(f"Applied DisplayConfig SINGLE {[self.lfp_panels[0].port]}")
            elif len(self.lfp_panels) == 2:
                if self.display_config_.set_display_configuration_ex(
                        enum.EXTENDED, [self.lfp_panels[0].port, self.lfp_panels[1].port]) is False:
                    self.fail(
                        f"Failed to apply DisplayConfig EXTENDED {[self.lfp_panels[0].port, self.lfp_panels[1].port]}")
                logging.info(f"Applied DisplayConfig EXTENDED {[self.lfp_panels[0].port, self.lfp_panels[1].port]}")

            logging.info("Verifying DC5/6 with Idle desktop")
            if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                self.fail("DC5/6 verification failed")
            logging.info("\tDC5/6 verification is successful")

            if self.ext_panels is not None:
                if dut.plug_wrapper(adapter, self.ext_panels[0]) is False:
                    self.fail("Failed to plug external display")
                logging.info("Hotplug external panel successful")

                if dut.unplug_wrapper(adapter, self.ext_panels[0]) is False:
                    self.fail("Failed to unplug external display")
                logging.info("Successfully unplugged external panel")

            logging.info("Verifying DC5/6 with Idle desktop")
            if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                self.fail("DC5/6 verification failed")
            logging.info("\tDC5/6 verification is successful")

    ##
    # @brief        This test verifies DC9 state with hotplug and unplug of external panel
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC9"])
    # @endcond
    def t_11_dc9_hotplug(self):
        for adapter in dut.adapters.values():
            if len(self.lfp_panels) == 1:
                if self.display_config_.set_display_configuration_ex(enum.SINGLE, [self.lfp_panels[0].port]) is False:
                    self.fail(f"Failed to apply DisplayConfig SINGLE {[self.lfp_panels[0].port]}")
                logging.info(f"Applied DisplayConfig SINGLE {[self.lfp_panels[0].port]}")
            elif len(self.lfp_panels) == 2:
                if self.display_config_.set_display_configuration_ex(
                        enum.EXTENDED, [self.lfp_panels[0].port, self.lfp_panels[1].port]) is False:
                    self.fail(
                        f"Failed to apply DisplayConfig EXTENDED {[self.lfp_panels[0].port, self.lfp_panels[1].port]}")
                logging.info(f"Applied DisplayConfig EXTENDED {[self.lfp_panels[0].port, self.lfp_panels[1].port]}")

            logging.info("Verifying DC9")
            if dc_state.verify_dc9(adapter) is False:
                self.fail("DC9 verification failed")
            logging.info("\tDC9 verification is successful")

            if self.ext_panels is not None:
                if dut.plug_wrapper(adapter, self.ext_panels[0]) is False:
                    self.fail("Failed to plug external display")
                logging.info("Hotplug external panel successful")

                if dut.unplug_wrapper(adapter, self.ext_panels[0]) is False:
                    self.fail("Failed to unplug external display")
                logging.info("Successfully unplugged external panel")

            logging.info("Verifying DC9")
            if dc_state.verify_dc9(adapter) is False:
                self.fail("DC9 verification failed")
            logging.info("\tDC9 verification is successful")

    ##
    # @brief        This test verifies DC6V state with hotplug and unplug of external panel
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V"])
    # @endcond
    def t_12_dc6v_hotplug(self):
        for adapter in dut.adapters.values():
            if len(self.lfp_panels) == 1:
                if self.display_config_.set_display_configuration_ex(enum.SINGLE, [self.lfp_panels[0].port]) is False:
                    self.fail(f"Failed to apply DisplayConfig SINGLE {[self.lfp_panels[0].port]}")
                logging.info(f"Applied DisplayConfig SINGLE {[self.lfp_panels[0].port]}")
            elif len(self.lfp_panels) == 2:
                if self.display_config_.set_display_configuration_ex(
                        enum.EXTENDED, [self.lfp_panels[0].port, self.lfp_panels[1].port]) is False:
                    self.fail(
                        f"Failed to apply DisplayConfig EXTENDED {[self.lfp_panels[0].port, self.lfp_panels[1].port]}")
                logging.info(f"Applied DisplayConfig EXTENDED {[self.lfp_panels[0].port, self.lfp_panels[1].port]}")

            logging.info("Verifying DC6v with App")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6v verification with app failed")
            logging.info("\tDC6V verification with app is successful")

            if self.ext_panels is not None:
                if dut.plug_wrapper(adapter, self.ext_panels[0]) is False:
                    self.fail("Failed to plug external display")
                logging.info("Hotplug external panel successful")

                if dut.unplug_wrapper(adapter, self.ext_panels[0]) is False:
                    self.fail("Failed to unplug external display")
                logging.info("Successfully unplugged external panel")

            logging.info("Verifying DC6v with App")
            if dc_state.verify_dc6v(adapter, method='APP') is False:
                self.fail("DC6v verification with app failed")
            logging.info("\tDC6v verification with app is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDcStateWithHotPlugUnplug))
    test_environment.TestEnvironment.cleanup(test_result)
