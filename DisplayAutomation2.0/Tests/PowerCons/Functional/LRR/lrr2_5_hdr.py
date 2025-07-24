########################################################################################################################
# @file         lrr2_5_hdr.py
# @brief        Contains concurrency tests of LRR2.5 with HDR
#
# @author       Mukesh M
########################################################################################################################
import logging
import unittest

from Libs.Core.logger import html
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.LRR.lrr_base import LrrBase
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import dut, common
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains LRR 2_5 concurrency tests with HDR
class LrrHdr(LrrBase):
    duration = None

    ##
    # @brief        Test function to make sure all the requirements are fulfilled before running other LRR 2.5
    #               concurrency test functions in this file. Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start("Verifying adapter and panel requirements for LRR2.5")
        # Setting power line to ac mode as HDR enabling requires enabling AC mode.
        assert workload.change_power_source(workload.PowerSource.AC_MODE), "FAILED to switch PowerSource"
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info(f"Panel on {panel.port} HDR caps: {panel.hdr_caps}")
                if panel.hdr_caps.is_hdr_supported:
                    logging.info(f"Enabling HDR for {panel.port}")
                    if pc_external.enable_disable_hdr([panel.port], True) is False:
                        self.fail(f"FAILED to enable HDR for {panel.port}")
        html.step_end()

    ##
    # @brief        This test function verifies LRR 2.5 with HDR
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_basic(self):
        status = True
        logging.info("Step: Verifying LRR2.5 with HDR enabled")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.method == lrr.Method.IDLE:
                    etl_file, polling_data = workload.run(
                        workload.IDLE_DESKTOP,
                        [self.duration_in_seconds],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )
                else:
                    etl_file, polling_data = workload.run(
                        workload.VIDEO_PLAYBACK_USING_FILE,
                        [self.video_file, self.duration_in_seconds, False],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                    )
                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)
        
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info(f"Disabling HDR for {panel.port}")
                if pc_external.enable_disable_hdr([panel.port], False) is False:
                    self.fail(f"FAILED to disable HDR for {panel.port}")

        if status is False:
            self.fail("FAIL: LRR2.5 verification with HDR")
        logging.info("PASS: LRR2.5 verification with HDR")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrHdr))
    test_environment.TestEnvironment.cleanup(test_result)
