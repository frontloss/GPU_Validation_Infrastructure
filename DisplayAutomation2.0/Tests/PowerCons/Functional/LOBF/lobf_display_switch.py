########################################################################################################################
# @file         lobf_display_switch.py
# @brief        Contains basic functional tests covering below scenarios:
#               * LOBF verification in with display switch scenario with external panel
# @author       Bhargav Adigarla
########################################################################################################################
from Libs.Core import enum
from Libs.Core.test_env import test_environment
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Tests.PowerCons.Functional.LOBF.lobf_base import *


##
# @brief        Contains basic LOBF tests
class LobfDisplaySwitch(LobfBase):
    ##
    # @brief        This function verifies LOBF with SD and Dual edp scenarios
    # @return       None
    def t_10_basic(self):
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
                    self.fail("Applying Display config {0} {1} Failed".format(DisplayConfigTopology(config[0]).name,
                                                                              config[1]))
                logging.info("Applied Display config {0} {1}".format(DisplayConfigTopology(config[0]).name, config[1]))

            for panel in adapter.panels.values():
                if panel.is_active and panel.is_lfp:
                    if lobf.is_alpm_supported(panel):
                        if lobf.verify_restrictions(adapter, panel) is False:
                            self.fail("LOBF restrictions failed in driver")
                        logging.info("LOBF restrictions satisfied, verifying LOBF")
                        if lobf.is_lobf_enabled_in_driver(adapter, panel) is False:
                            self.fail("LOBF is disabled in driver")
                        logging.info("LOBF Enabled in driver")

                    else:
                        logging.info("ALPM is not supported in panel, verifying AUX wake LOBF")
                        if lobf.verify_auxwake(adapter, panel) is False:
                            self.fail("AUX wake LOBF disabled on non ALPM panel")
                        logging.info("AUX wake LOBF enabled")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LobfDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)