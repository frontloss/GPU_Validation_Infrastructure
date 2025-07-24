########################################################################################################################
# @file         test_dual_lfp_display_switch.py
# @brief        Tests for DC state in Display_switch scenario with dual eDP plus external display
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains Display Switch tests for DC States
class TestDualLfpDisplaySwitch(DCStatesBase):

    ##
    # @brief        This function tests DC states across various display configurations
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6"])
    # @endcond
    def t_10_display_switch_dc6(self):
        for adapter in dut.adapters.values():
            config_list = [(enum.SINGLE, [self.lfp_panels[0].port], True),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.lfp_panels[1].port], True),
                           (enum.SINGLE, [self.ext_panels[0].port], False),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.lfp_panels[1].port], True),
                           (enum.SINGLE, [self.ext_panels[0].port], False),
                           (enum.SINGLE, [self.lfp_panels[1].port], True),
                           (enum.SINGLE, [self.lfp_panels[0].port], True)]

            for config in config_list:
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail(f"FAILED to apply DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")
                logging.info(f"Applied DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")

                if config[2]:  # Checking DC states for eDP panel config
                    logging.info("Verifying DC5/6 with Idle desktop")
                    if dc_state.verify_dc5_dc6(adapter, method='IDLE') is False:
                        self.fail("DC5/6 verification failed")
                    logging.info("\tDC5/6 verification is successful")

    ##
    # @brief        This function tests DC states across various display configurations
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC9"])
    # @endcond
    def t_11_display_switch_dc9(self):
        for adapter in dut.adapters.values():
            config_list = [(enum.SINGLE, [self.lfp_panels[0].port], True),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.lfp_panels[1].port], True),
                           (enum.SINGLE, [self.ext_panels[0].port], False),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.lfp_panels[1].port], True),
                           (enum.SINGLE, [self.ext_panels[0].port], False),
                           (enum.SINGLE, [self.lfp_panels[1].port], True),
                           (enum.SINGLE, [self.lfp_panels[0].port], True)]

            for config in config_list:
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail(f"FAILED to apply DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")
                logging.info(f"Applied DisplayConfig {DisplayConfigTopology(config[0]).name} {config[1]}")

                if dc_state.verify_dc9(adapter) is False:
                    self.fail("DC9 verification failed")
                logging.info("\tDC9 verification is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDualLfpDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)
