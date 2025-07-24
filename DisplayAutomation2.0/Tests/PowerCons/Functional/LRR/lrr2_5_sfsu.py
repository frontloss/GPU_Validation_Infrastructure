########################################################################################################################
# @file         lrr2_5_sfsu.py
# @brief        This file contains concurrency tests of the LRR 2.5 and SFSU.
#
# @author       Mukesh M
########################################################################################################################
import logging
import unittest

from Libs.Core.logger import html
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.LRR.lrr import LrrVersion
from Tests.PowerCons.Functional.LRR.lrr_base import LrrBase
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import dut, common
from Tests.PowerCons.Modules import workload
from Tests.PowerCons.Functional.PSR import sfsu


##
# @brief        This class contains LRR 2_5 concurrency tests with SFSU
class LrrSfsu(LrrBase):

    ##
    # @brief        This test function verifies SFSU with LRR2.5
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_basic(self):
        status = True
        html.step_start("Verification of LRR2.5 with SFSU")
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.feature == LrrVersion.LRR2_5 and panel.lrr_caps.is_lrr_2_5_supported:
                    etl_file, polling_data = workload.run(
                        workload.VIDEO_PLAYBACK_USING_FILE,
                        [self.video_file, self.duration_in_seconds, False, True, None, None, False],
                        [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2) + psr.get_polling_offsets(
                            psr.UserRequestedFeature.PSR2_SFSU), self.polling_delay_in_seconds]
                    )

                    status &= lrr.verify(
                        adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)

                    html.step_start(f"SFSU Verification for {panel.port} on {adapter.gfx_index}")
                    if sfsu.verify_sfsu(
                            adapter, panel, etl_file, self.method, psr.UserRequestedFeature.PSR2_SFSU, True) is False:
                        logging.error("\tFAIL: SFSU verification")
                        status &= False
                    else:
                        logging.info("\tPASS: SFSU verification")
                    html.step_end()

        if status is False:
            html.step_end()
            self.fail("FAIL: LRR2.5 verification with SFSU")
        logging.info("PASS: LRR 2.5 verification with SFSU")
        html.step_end()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrSfsu))
    test_environment.TestEnvironment.cleanup(test_result)
