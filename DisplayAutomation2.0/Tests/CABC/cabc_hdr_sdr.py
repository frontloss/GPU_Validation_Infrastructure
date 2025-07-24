########################################################################################################################
# @file         cabc_hdr_sdr.py
# @brief        Test for CABC Optimization when HDR toggle
# @author       Tulika
########################################################################################################################
from Libs.Core.wrapper import control_api_wrapper
from Libs.Core.test_env import test_environment
from Tests.BrightnessOptimization.test_base import *
from Tests.CABC import cabc
from Tests.CABC.cabc_base import CabcBase
from Tests.PowerCons.Functional.BLC import blc


##
# @brief        This class contains CABC verification during HDR/SDR toggle
#               This class inherits the CabcBase class.


class CabcHdr(CabcBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        CABC verification during HDR/SDR Toggle
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_hdr_sdr_toggle(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                skip_igcl_for_cabc = False
                if (cabc.optimization_params[panel.port].feature_2.level is not None and
                        cabc.optimization_params[panel.port].feature_1.level != cabc.optimization_params[
                            panel.port].feature_2.level):
                    skip_igcl_for_cabc = True

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
                    # @todo to remove later once re-init is handled in infra
                    # Need to re-init as due to driver restart happened
                    if not control_api_wrapper.configure_control_api(flag=False):
                        self.fail("\tFailed to close Control API")

                    if not control_api_wrapper.configure_control_api(flag=True):
                        self.fail("\tFailed to re-init Control API")

                status = cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_1.name,
                                    cabc.optimization_params[panel.port].feature_1.level, skip_igcl_for_cabc)

                if cabc.optimization_params[panel.port].feature_1.name == cabc.Feature.CABC:
                    if status:
                        logging.info(
                            f"PASS: {cabc.optimization_params[panel.port].feature_1.name} persistence passed post HDR Enable")
                    else:
                        self.fail(
                            f"FAIL: {cabc.optimization_params[panel.port].feature_1.name} persistence failed post HDR Enable")

                if cabc.optimization_params[panel.port].feature_2.name == cabc.Feature.OPST:

                    status = cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_2.name,
                                        cabc.optimization_params[panel.port].feature_2.level, skip_igcl_for_cabc)
                    if status:
                        self.fail(
                            f"FAIL: {cabc.optimization_params[panel.port].feature_2.name} persistence failed post HDR Enable")
                    else:
                        logging.info(
                            f"PASS: {cabc.optimization_params[panel.port].feature_2.name} persistence passed post HDR Enable")

                # disabling HDR
                status = blc.disable_hdr(adapter, os_aware=False)

                if status is False:
                    self.fail("Failed to disable HDR")
                elif status is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail("Failed to restart display driver post HDR disable")
                    vbt.Vbt(adapter.gfx_index).reload()
                    # @todo to remove later once re-init is handled in infra
                    # Need to re-init as due to driver restart happened
                    if not control_api_wrapper.configure_control_api(flag=False):
                        self.fail("\tFailed to close Control API")

                    if not control_api_wrapper.configure_control_api(flag=True):
                        self.fail("\tFailed to re-init Control API")

                status = cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_1.name,
                                    cabc.optimization_params[panel.port].feature_1.level, skip_igcl_for_cabc)
                if status:
                    logging.info(
                        f"PASS: {cabc.optimization_params[panel.port].feature_1.name} persistence passed post HDR Disable")
                else:
                    self.fail(
                        f"FAIL: {cabc.optimization_params[panel.port].feature_1.name} persistence failed post HDR Disable")

                if cabc.optimization_params[panel.port].feature_2.name is not None:
                    status = cabc.verify(adapter, panel, cabc.optimization_params[panel.port].feature_2.name,
                                        cabc.optimization_params[panel.port].feature_2.level, skip_igcl_for_cabc)
                    if status:
                        logging.info(
                            f"PASS: {cabc.optimization_params[panel.port].feature_2.name} persistence passed post HDR Disable")
                    else:
                        self.fail(
                            f"FAIL: {cabc.optimization_params[panel.port].feature_2.name} persistence failed post HDR Disable")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CabcHdr))
    test_environment.TestEnvironment.cleanup(test_result)
