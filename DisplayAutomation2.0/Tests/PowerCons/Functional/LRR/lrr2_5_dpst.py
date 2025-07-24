########################################################################################################################
# @file         lrr2_5_dpst.py
# @brief        This file contains concurrency test of LRR 2.5 and DPST features.
#
# @author       Mukesh M
########################################################################################################################
import logging
import unittest

from Libs.Core import display_essential
from Libs.Core.logger import html
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.LRR.lrr_base import LrrBase
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import dut, common
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains LRR 2_5 concurrency tests with DPST
class LrrDpst(LrrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test function verifies existence of DPST with LRR2.5.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_12_dpst_lrr2_5_check(self):
        html.step_start("Concurrency Test: LRR 2.5 verification with DPST")

        # registry change for the adapter
        for adapter in dut.adapters.values():
            # Check if DPST is enabled on the adapter if not enable it.
            logging.info(f"Step: Enabling DPST for {adapter.name}")
            dpst_status = dpst.enable(adapter, True)
            if dpst_status is False:
                self.fail("FAILED to enable DPST")
            if dpst_status is True:
                result, reboot_required = display_essential.restart_gfx_driver()
                if result is False:
                    self.fail("FAILED to restart the driver")
            logging.info("\tPASS: FeatureTestControl DPST status Expected= ENABLED, Actual= ENABLED")

        # Run the workload
        etl_file, polling_data = workload.run(
            workload.VIDEO_PLAYBACK_USING_FILE,
            [self.video_file, self.duration_in_seconds, False],
            [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
        )

        # verify on each panel
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Skip the panel if not LFP
                if panel.is_lfp is False:
                    continue
                verify_status = lrr.verify(
                    adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)
                if verify_status is False:
                    logging.error(
                        f"lrr verification failed on panel {panel.panel_index} attached on {adapter.gfx_index}")
                    status &= verify_status
                verify_status = dpst.verify(adapter, panel, etl_file)
                if verify_status is False:
                    logging.error(
                        f"DPST verification failed on panel {panel.panel_index} attached on {adapter.gfx_index}")
                    status &= verify_status

        if not status:
            html.step_end()
            self.fail("FAIL: LRR 2.5 verification with DPST")
        logging.info("PASS: LRR 2.5 verification with DPST")
        html.step_end()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrDpst))
    test_environment.TestEnvironment.cleanup(test_result)
