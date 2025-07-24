########################################################################################################################
# @file         lrr2_5_mso.py
# @brief        This file contains LRR2.5 concurrency tests with MSO.
#
# @author       Mukesh M
########################################################################################################################
import logging
import unittest

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LRR import lrr
from Tests.PowerCons.Functional.LRR.lrr import Method, LrrVersion
from Tests.PowerCons.Functional.LRR.lrr_base import LrrBase
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import dut, common
from Tests.PowerCons.Modules import workload
from registers.mmioregister import MMIORegister
from Tests.EDP.MSO import mso


##
# @brief        This class contains LRR 2_5 with MSO concurrency tests with MSO
class LrrMso(LrrBase):
    ##
    # @brief        Test function to make sure all the requirements are fulfilled before running other LRR test
    #               functions. Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_11_mso_requirements(self):
        # Check if there is at least one MSO supported panel in command line.
        is_mso_panel_present = False
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                logging.info(f"\t{panel.mso_caps}")
                if panel.mso_caps.is_mso_supported:
                    is_mso_panel_present = True
        if not is_mso_panel_present:
            self.fail("At least one MSO supported panel is required for testing concurrency of LRR 2.5 with MSO")

    ##
    # @brief        Test function for verification of LRR 2.5 with MSO
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_12_lrr2_5_mso(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if self.feature == LrrVersion.LRR2_5 and panel.mso_caps.is_mso_supported:
                    logging.info(f"STEP: Verification of LRR2.5 with MSO for {adapter.gfx_index} - {panel.port}")
                    port = panel.transcoder_type.name.split('_')[1]
                    # Offset for polling the MSO registers
                    polling_offsets = psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2)
                    polling_offsets.append(MMIORegister.get_instance(
                        "PIPE_DSS_CTL1_REGISTER", 'PIPE_DSS_CTL1_P' + port, adapter.name).offset)
                    if self.method == Method.IDLE:
                        etl_file, polling_data = workload.run(
                            workload.IDLE_DESKTOP,
                            [self.duration_in_seconds],
                            [polling_offsets, self.polling_delay_in_seconds]
                        )
                    else:
                        etl_file, polling_data = workload.run(
                            workload.VIDEO_PLAYBACK_USING_FILE,
                            [self.video_file, self.duration_in_seconds, False],
                            [polling_offsets, self.polling_delay_in_seconds]
                        )
                    status &= lrr.verify(
                        adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)

                    if mso.is_mso_enabled(adapter, panel, polling_data) is False:
                        logging.error(f"FAIL: LRR 2.5 verification with MSO on {adapter.gfx_index} - {panel.port} ")
                        status &= False

        if status is False:
            self.fail(f"FAIL: LRR2.5 verification failed with MSO")
        logging.info("PASS: LRR 2.5 verification with MSO passed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrMso))
    test_environment.TestEnvironment.cleanup(test_result)
