########################################################################################################################
# @file         test_hdr.py
# @brief        Test for BRT Optimization when HDR toggle
# @author       Simran Setia
########################################################################################################################
from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import *
from Tests.PowerCons.Functional.BLC import blc



##
# @brief        This class contains Brightness Optimization verification when HDR toggle
#               This class inherits the BrtOptimizationBase class.


class TestHDR(BrtOptimizationBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        Brightness verification when HDR Toggle
    # @return       None
    # @cond
    # @endcond
    def t_11_hdr_toggle(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                skip_igcl_for_elp = False
                if brt.optimization_params[panel.port].feature_1.level != brt.optimization_params[
                    panel.port].feature_2.level:
                    skip_igcl_for_elp = True

                # checking for HDR support
                if not panel.hdr_caps.is_hdr_supported:
                    self.fail(f"{panel.port} does not support HDR on PIPE_{panel.pipe}")

                # enabling HDR
                status = blc.enable_hdr(adapter, os_aware=False)

                if status is False:
                    self.fail("Failed to enable HDR")
                elif status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("Failed to restart display driver post HDR enable")
                    vbt.Vbt(adapter.gfx_index).reload()

                status = brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                                    brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp)

                if brt.optimization_params[panel.port].feature_1.name == brt.Feature.ELP or brt.optimization_params[
                    panel.port].feature_1.name == brt.Feature.APD:
                    if status:
                        logging.info(
                            f"PASS: {brt.optimization_params[panel.port].feature_1.name} persistence passed post HDR Enable")
                    else:
                        self.fail(
                            f"FAIL: {brt.optimization_params[panel.port].feature_1.name} persistence failed post HDR Enable")

                if brt.optimization_params[panel.port].feature_2.name == brt.Feature.OPST:

                    status = brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                                        brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_elp)
                    if status:
                        self.fail(
                            f"FAIL: {brt.optimization_params[panel.port].feature_2.name} persistence failed post HDR Enable")
                    else:
                        logging.info(
                            f"PASS: {brt.optimization_params[panel.port].feature_2.name} persistence passed post HDR Enable")

                # disabling HDR
                status = blc.disable_hdr(adapter, os_aware=False)

                if status is False:
                    self.fail("Failed to disable HDR")
                elif status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("Failed to restart display driver post HDR disable")
                    vbt.Vbt(adapter.gfx_index).reload()

                status = brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_1.name,
                                    brt.optimization_params[panel.port].feature_1.level, skip_igcl_for_elp)
                if status:
                    logging.info(
                        f"PASS: {brt.optimization_params[panel.port].feature_1.name} persistence passed post HDR Disable")
                else:
                    self.fail(
                        f"FAIL: {brt.optimization_params[panel.port].feature_1.name} persistence failed post HDR Disable")

                if brt.optimization_params[panel.port].feature_2.name is not None:
                    status = brt.verify(adapter, panel, brt.optimization_params[panel.port].feature_2.name,
                                        brt.optimization_params[panel.port].feature_2.level, skip_igcl_for_elp)
                    if status:
                        logging.info(
                            f"PASS: {brt.optimization_params[panel.port].feature_2.name} persistence passed post HDR Disable")
                    else:
                        self.fail(
                            f"FAIL: {brt.optimization_params[panel.port].feature_2.name} persistence failed post HDR Disable")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestHDR))
    test_environment.TestEnvironment.cleanup(test_result)
