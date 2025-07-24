#################################################################################################################
# @file         lrr_vbt.py
# @brief        Contains LRR VBT test
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload
from Tests.VRR import vrr


##
# @brief        This class contains LRR VBT tests
class LrrVbtTest(LrrBase):

    ##
    # @brief        This function verifies LRR with VBT settings
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_vbt(self):
        status = True

        for adapter in dut.adapters.values():
            html.step_start("Disabling VRR in VBT for DP_A")
            if vrr.update_vbt(adapter, 'DP_A', False) is False:
                self.fail("FAILED to update VRR settings in VBT")
            logging.info("Successfully disabled VRR in VBT for DP_A")
            html.step_end()

            if adapter.lfp_count > 1:
                html.step_start("Disabling VRR in VBT for DP_B")
                if vrr.update_vbt(adapter, 'DP_B', False) is False:
                    self.fail("FAILED to update VRR settings in VBT")
                logging.info("Successfully disabled VRR in VBT for DP_B")
                html.step_end()

            for panel in adapter.panels.values():
                if self.method == Method.IDLE:
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

            html.step_start("Enabling VRR in VBT for DP_A")
            if vrr.update_vbt(adapter, 'DP_A', True) is False:
                self.fail("FAILED to update VRR settings in VBT")
            logging.info("Successfully enabled VRR in VBT for DP_A")
            html.step_end()

            if adapter.lfp_count > 1:
                html.step_start("Enabling VRR in VBT for DP_B")
                if vrr.update_vbt(adapter, 'DP_B', True) is False:
                    self.fail("FAILED to update VRR settings in VBT")
                logging.info("Successfully enabled VRR in VBT for DP_B")
                html.step_end()

        if status is False:
            self.fail("FAIL: LRR verification with VRR disabled from VBT")
        logging.info("PASS: LRR verification with VRR disabled from VBT")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrVbtTest))
    test_environment.TestEnvironment.cleanup(test_result)
