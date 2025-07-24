#######################################################################################################################
# @file         psr_display_switch.py
# @brief        PSR display switching tests
# @details  Test for PSR in display switch scenarios SD eDP + External displays, Dual eDP,
#               Dual eDP + External displays
#
# @author       Rohit Kumar
#######################################################################################################################

from Libs.Core import display_power
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.PSR.psr_base import *


##
# @brief        Contains PSR tests with display switching
class TestDisplaySwitch(PsrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function checks if atleast two displays are connected
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_03_display_switch_requirements(self):
        for adapter in dut.adapters.values():
            if len(adapter.panels) < 2:
                self.fail("At least two displays are required for DisplaySwitch test (Command Line Issue)")

    ##
    # @brief        This function checks PSR with AC power
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC"])
    # @endcond
    def t_11_display_switch_ac(self):
        self.verify_feature_with_display_switch(display_power.PowerSource.AC)

    @common.configure_test(repeat=True, selective=["DC"])
    ##
    # @brief        This function checks PSR with DC power
    # @return       None
    def t_12_display_switch_dc(self):
        self.verify_feature_with_display_switch(display_power.PowerSource.DC)

    ############################
    # Helper Function
    ############################
    ##
    # @brief        Helper function to checks PSR with display switching
    # @param[in]    power_source enum AC/DC
    # @return       None
    def verify_feature_with_display_switch(self, power_source):
        if not self.display_power_.set_current_powerline_status(power_source):
            self.fail("Failed to switch power line status to {0}(Test Issue)".format(
                power_source.name))
        self.power_source = power_source
        for adapter in dut.adapters.values():
            lfp_panels = []
            ext_panels = []
            for panel in adapter.panels.values():
                if panel.is_lfp is True:
                    lfp_panels.append(panel.port)
                else:
                    ext_panels.append(panel.port)

            if len(lfp_panels) > 1:
                ##
                # Dual eDP case
                if len(ext_panels) == 0:
                    ##
                    # Dual eDP only
                    self.config_list = [(enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], lfp_panels[1]]),
                                        (enum.CLONE, [lfp_panels[0], lfp_panels[1]]),
                                        (enum.SINGLE, [lfp_panels[1]]),
                                        (enum.SINGLE, [lfp_panels[0]])
                                        ]
                else:
                    ##
                    # Dual eDP with external panel
                    self.config_list = [(enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], lfp_panels[1], ext_panels[0]]),
                                        (enum.CLONE, [lfp_panels[0], lfp_panels[1], ext_panels[0]]),
                                        (enum.SINGLE, [lfp_panels[1]]),
                                        (enum.EXTENDED, [lfp_panels[0], lfp_panels[1]]),
                                        (enum.CLONE, [lfp_panels[0], lfp_panels[1]]),
                                        (enum.SINGLE, [lfp_panels[0]])
                                        ]

            else:
                ##
                # Single eDP case
                if len(ext_panels) > 1:
                    ##
                    # Single eDP with multiple external panels
                    self.config_list = [(enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], ext_panels[0]]),
                                        (enum.CLONE, [lfp_panels[0], ext_panels[0]]),
                                        (enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], ext_panels[0],
                                                         ext_panels[1]]),
                                        (enum.SINGLE, [lfp_panels[0]])
                                        ]
                elif len(ext_panels) == 1:
                    ##
                    # Single eDp with single external panel
                    self.config_list = [(enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], ext_panels[0]]),
                                        (enum.CLONE, [lfp_panels[0], ext_panels[0]]),
                                        (enum.SINGLE, [lfp_panels[0]]),
                                        (enum.SINGLE, [lfp_panels[0]])]

            for config in self.config_list:
                logging.info("STEP: verifying {0} on {1}".format(self.feature_str, config[1]))
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail("Failed to apply display configuration(Test Issue)")
                time.sleep(5)
                dut.refresh_panel_caps(adapter)
                self.validate_feature()
                logging.info("PASS : {0} verification is successful with config {1} on {2}".format(
                    self.feature_str, DisplayConfigTopology(config[0]).name, config[1]))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)
