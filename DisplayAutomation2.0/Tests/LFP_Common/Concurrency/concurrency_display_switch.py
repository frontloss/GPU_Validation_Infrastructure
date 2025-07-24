#######################################################################################################################
# @file         concurrency_display_switch.py
# @brief        Test for Dual eDP concurrency in display switch scenarios SD EDP, Dual eDP Clone and extended,
#
# @author       Bhargav Adigarla
#######################################################################################################################
import time

from Libs.Core import enum
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.PSR import psr
from Tests.LFP_Common.Concurrency.concurrency_base import *


##
# @brief        This class contains Concurrency Display Switch Tests. It inherits ConcurrencyBase Class.
class ConcurrencyDisplaySwitch(ConcurrencyBase):
    ############################
    # Test Function
    ############################
    ##
    # @brief        This test function verifies LFP concurrency with display switch to various configs
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_10_display_switch(self):

        # Enable Lace1.0 version support for ARL
        if SystemInfo().get_sku_name('gfx_0') == 'ARL' and self.lace1p0_status:
            if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                             reg_datatype=registry_access.RegDataType.DWORD, reg_value=10,
                                             driver_restart_required=True) is False:
                logging.error("Failed to enable Lace1.0 registry key")
                self.fail("Failed to enable Lace1.0 registry key")
            logging.info("Registry key add to enable Lace1.0 is successful")
        else:
            logging.info("Lace1.0 Registry Key is either not present or not enabled")

        for adapter in dut.adapters.values():
            self.lfp_panels = []
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    self.lfp_panels.append(panel)

            ##
            # Dual eDP only
            # Display Switch will be in below sequence. objective here is to verify feature w.r.t panel or pipe in all
            # Display configs ex:- SD EDP A, SD EDP B, SD MIPI, DDC, DDE
            config_list = [(enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.EXTENDED, [self.lfp_panels[0].port, self.lfp_panels[1].port]),
                           (enum.SINGLE, [self.lfp_panels[1].port]),
                           (enum.EXTENDED, [self.lfp_panels[1].port, self.lfp_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port]),
                           (enum.CLONE, [self.lfp_panels[0].port, self.lfp_panels[1].port]),
                           (enum.SINGLE, [self.lfp_panels[1].port]),
                           (enum.CLONE, [self.lfp_panels[1].port, self.lfp_panels[0].port]),
                           (enum.SINGLE, [self.lfp_panels[0].port])]

            for config in config_list:
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail("Applying Display config {0} Failed"
                              .format(str(config[0]) + " " + " ".join(str(x) for x in config[1])))
                logging.info("Applied Display config {0}"
                                 .format(str(config[0]) + " " + " ".join(str(x) for x in config[1])))

                # Update Panel caps post new config applied.
                dut.refresh_panel_caps(dut.adapters['gfx_0'])
                feature_supported = None
                # Verify feature in panel if panel is in current config
                for panel in self.lfp_panels:
                    if panel.port in config[1]:
                        panel.feature = self.display_feature_dict.get(panel.port)
                        if panel.feature == "VRR" and config[0] != enum.SINGLE:
                            continue

                        feature_map = { "PSR1": psr.UserRequestedFeature.PSR_1,
                                                  "PSR2": psr.UserRequestedFeature.PSR_2}

                        if panel.feature in ["PSR1", "PSR2"]:
                            feature_supported = psr.verify_psr_restrictions(adapter, panel, feature_map[panel.feature])
                            if panel.feature == 'PSR2' and feature_supported == psr.UserRequestedFeature.PSR_1:
                                panel.feature = 'PSR1'
                            if feature_supported == psr.UserRequestedFeature.PSR_NONE:
                                continue

                        logging.info("Verifying {0} {1}".format(panel.feature, panel.port))
                        if edp_feature_utility.verify_feature_enabled_in_driver(dut.adapters['gfx_0'], panel, feature_supported) is True:
                            logging.info("{0} Enabled on {1} pipe {2}".format(panel.feature, panel.port, panel.pipe))
                        else:
                            self.fail("{0} Disabled on {1} pipe {2}".format(panel.feature, panel.port, panel.pipe))
                time.sleep(5)  # 5 seconds Delay for every display switch.


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(ConcurrencyDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)
