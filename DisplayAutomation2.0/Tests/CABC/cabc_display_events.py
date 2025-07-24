########################################################################################################################
# @file         cabc_display_events.py
# @brief        Test for CABC display events scenario
#
# @author       Tulika
########################################################################################################################
from Libs.Core import enum
from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import *
from Tests.CABC import cabc
from Tests.CABC.cabc_base import CabcBase


##
# @brief        This class contains CABC verification during display events
#               This class inherits the CABC class.


##
# @brief        This class contains test to validate CABC status in driver
class CabcDisplayEvents(CabcBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This function validates CABC status in driver during display events
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_display_events(self):
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
                    skip_igcl_for_cabc = False
                    if (cabc.optimization_params[panel.port].feature_2.level is not None and
                            cabc.optimization_params[panel.port].feature_1.level != cabc.optimization_params[
                                panel.port].feature_2.level):
                        skip_igcl_for_cabc = True
                    if self.verify_with_display_events(adapter, panel, skip_igcl_for_cabc) is False:
                        self.fail(
                            f"FAIL: CABC features disabled after {common.print_current_topology} event")
                    logging.info(f"PASS: CABC features enabled after {common.print_current_topology} event")

    ##
    # @brief        CABC verification during display events
    # @param[in]    adapter
    # @param[in]    panel
    # @param[in]    skip_igcl_for_cabc
    # @return       None
    def verify_with_display_events(self, adapter, panel, skip_igcl_for_cabc):
        status = True
        status &= cabc.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                              brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_cabc)
        status &= cabc.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                              brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_cabc)
        return status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CabcDisplayEvents))
    test_environment.TestEnvironment.cleanup(test_result)
