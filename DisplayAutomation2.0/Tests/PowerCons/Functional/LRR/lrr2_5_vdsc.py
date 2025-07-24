########################################################################################################################
# @file         lrr2_5_vdsc.py
# @brief        Contains concurrency tests of the 2_5
#
# @author       Mukesh M
########################################################################################################################
import logging
import unittest

from Libs.Core.test_env import test_environment
from Libs.Feature.vdsc import dsc_verifier
from Tests.PowerCons.Functional.LRR.lrr_base import LrrBase
from Tests.PowerCons.Modules import dut, common
from registers.mmioregister import MMIORegister


##
# @brief        This class contains LRR 2_5 concurrency tests with VDSC
class LrrVdsc(LrrBase):
    ##
    # @brief        Test function to make sure all the requirements are fulfilled before running other LRR test
    #               functions. Failure of this test will stop the execution. This function checks if there is at least
    #               one panel which supports VDSC
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_11_vdsc_requirements(self):
        # Check if there is at least one VDSC supported panel in command line.
        is_vdsc_panel_present = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info(f"\t{panel.vdsc_caps}")
                if panel.vdsc_caps.is_vdsc_supported:
                    is_vdsc_panel_present = True
        if not is_vdsc_panel_present:
            self.fail("At least one VDSC supported panel is required for testing concurrency of LRR 2.5 with VDSC")

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test function verifies the existence of VDSC with LRR2_5
    # @return      None
    # @cond
    @common.configure_test(critical=True, selective=["VDSC"])
    # @endcond
    def t_12_vdsc_lrr2_5_check(self):
        # VDSC should be enabled with LRR2.5 only on ADLP+ platforms
        # Check if VDSC is enabled on platforms other than ADLP+
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info(
                    f"STEP: Verification of VDSC on LRR2.5 supported panel on {panel.port} -{adapter.gfx_index}")
                logging.info(f"Panel : {panel.port} VDSCCaps({panel.vdsc_caps})")
                # Check if VDSC is supported on Panel
                if not panel.vdsc_caps.is_vdsc_supported:
                    logging.info(f" VDSC is not supported on Panel on {panel.port}")
                    continue

                # If VDSC is supported it should be enabled on Gen13+ platforms
                if adapter.name in common.PRE_GEN_12_PLATFORMS:
                    edp_dss_ctl2 = MMIORegister.read('DSS_CTL2_REGISTER', 'DSS_CTL2', adapter.name,
                                                     gfx_index=adapter.gfx_index)
                else:
                    edp_dss_ctl2 = MMIORegister.read('PIPE_DSS_CTL2_REGISTER', 'PIPE_DSS_CTL2_P' + panel.pipe,
                                                     adapter.name, gfx_index=adapter.gfx_index)
                if adapter.name in common.PRE_GEN_13_PLATFORMS + ['DG2']:
                    if edp_dss_ctl2.left_branch_vdsc_enable == 0x1:
                        logging.error(
                            f"VDSC and LRR2.5 should be enabled only on ADLP+ platforms, Not Expected on {panel.port}")
                        status &= False
                        continue
                else:
                    # DSC should be enabled on Gen13+ platforms
                    if edp_dss_ctl2.left_branch_vdsc_enable != 0x1:
                        logging.error(
                            f"VDSC should be enabled on ADLP+ platforms. Not enabled on {panel.port} - {adapter.name}")
                        status &= False
                        continue

                # VDSC verification
                dsc_status = dsc_verifier.verify_dsc_programming(adapter.gfx_index, panel.port)
                logging.info(f"Interim DSC Status: {dsc_status} Panel: {panel.port} adapter: {adapter.name}")
                if (dsc_status is True) and (adapter.name in common.PRE_GEN_13_PLATFORMS + ['DG2']):
                    # Fail the test if dsc verification passes on common.PRE_GEN_13_PLATFORMS
                    logging.error(f"VDSC verification failed on {panel.port} attached to {adapter.gfx_index}"
                                  f"VDSC should be enabled with LRR2.5 only on ADLP+ platforms")
                    status &= False
                if (dsc_status is False) and (adapter.name not in common.PRE_GEN_13_PLATFORMS):
                    logging.error(
                        f"FAIL: VDSC programming not proper on {panel.port} attached to {adapter.gfx_index}")
                    status &= False

        if not status:
            self.fail("FAIL: VDSC verification with LRR2.5 failed")
        logging.info("PASS : VDSC verification with LRR2.5 passed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrVdsc))
    test_environment.TestEnvironment.cleanup(test_result)
