########################################################################################################################
# @file         test_display_switch.py
# @brief        Tests for DC state in Display_switch scenario
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains Display Switch tests for DC States
class TestDisplaySwitch(DCStatesBase):

    ##
    # @brief        This function tests DC states across various display configurations
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V"])
    # @endcond
    def t_11_display_switch_dc6v(self):
        for adapter in dut.adapters.values():
            config_list = [(enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.CLONE, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.CLONE, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port])]

            for config in config_list:
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail(f"Failed to apply DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")
                logging.info(f"Applied DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")
                time.sleep(5)

                if config[0] == enum.SINGLE:
                    logging.info("Verifying DC6v with App")
                    if dc_state.verify_dc6v(adapter, method='APP') is False:
                        self.fail("DC6V verification with app failed")
                    logging.info("\tDC6V verification with app is successful")

    ##
    # @brief        This function tests DC states across various display configurations
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6"])
    # @endcond
    def t_12_display_switch_dc6(self):
        for adapter in dut.adapters.values():
            config_list = [(enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.CLONE, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.CLONE, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port])]

            for config in config_list:
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail(f"Failed to apply DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")
                logging.info(f"Applied DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")

                if config[0] == enum.SINGLE:
                    logging.info("Verifying DC5/6 with Idle desktop")
                    if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                        self.fail("DC5/6 verification with idle failed")
                    logging.info("\tDC5/6 verification with idle is successful")

    ##
    # @brief        This function tests DC states across various display configurations
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC9"])
    # @endcond
    def t_13_display_switch_dc9(self):
        for adapter in dut.adapters.values():
            config_list = [(enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.CLONE, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.CLONE, [self.lfp_panels[0].port, self.ext_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port])]

            for config in config_list:
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail(f"Failed to apply DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")
                logging.info(f"Applied DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")

                if dc_state.verify_dc9(adapter) is False:
                    self.fail("DC9 verification failed")
                logging.info("\tDC9 verification is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)
