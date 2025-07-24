########################################################################################################################
# @file         test_display_events.py
# @brief        Test for BRT Optimization display events scenario
#
# @author       Tulika
########################################################################################################################
from Libs.Core import enum
from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import *


##
# @brief        This class contains Brightness Optimization verification during display events
#               This class inherits the BrtOptimizationBase class.


class BrtDisplayEvents(BrtOptimizationBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Brightness verification during display config events
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_display_events(self):
        status = True
        self.lfp_panels = []
        self.external_panels = []
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    self.lfp_panels.append(panel.port)
                else:
                    self.external_panels.append(panel.port)

        config_list = [(enum.SINGLE, [self.lfp_panels[0]]),
                       (enum.CLONE, [self.lfp_panels[0], self.external_panels[0]]),
                       (enum.SINGLE, [self.lfp_panels[0]])]

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                for config in config_list:
                    if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                        self.fail(f"FAILED to apply display config")
                    # Update Panel caps post new config applied.
                    dut.refresh_panel_caps(adapter)
                    if not panel.is_lfp:
                        continue
                    skip_igcl_for_elp = False
                    if brt.optimization_params[panel.port].feature_1.level != brt.optimization_params[panel.port].feature_2.level:
                        skip_igcl_for_elp = True

                    if self.verify_with_display_events(adapter, panel, skip_igcl_for_elp) is False:
                        self.fail(
                            f"FAIL: BRT OPTIMIZATION features disabled after {common.print_current_topology} event")
                    logging.info(f"PASS: BRT OPTIMIZATION features enabled after {common.print_current_topology} event")

    ##
    # @brief        Brightness Optimization verification in AC/DC switch
    # @param[in]    adapter
    # @param[in]    panel
    # @param[in]    skip_igcl_for_elp
    # @return       None
    def verify_with_display_events(self, adapter, panel, skip_igcl_for_elp):
        status = True
        status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                             brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp)
        status &= brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                             brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_elp)
        return status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BrtDisplayEvents))
    test_environment.TestEnvironment.cleanup(test_result)
