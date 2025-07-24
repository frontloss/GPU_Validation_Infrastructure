#################################################################################################################
# @file         lrr_mode_set.py
# @brief        Contains LRR mode set tests
#
# @author       Rohit Kumar
#################################################################################################################

from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload

##
# @brief        This class contains tests to verify LRR after mode sets


class LrrModeSetTest(LrrBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        This function verifies LRR after ModeSet operation
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_mode_set(self):
        test_status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Get two supported modes with max RR
                mode_list = common.get_display_mode(panel.target_id, panel.max_rr, 2)

                for mode in mode_list:
                    # Skip to next mode if current and target modes are same
                    current_mode = self.display_config_.get_current_mode(panel.target_id)
                    if current_mode == mode:
                        continue

                    html.step_start(f"Applying display mode {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                    if self.display_config_.set_display_mode([mode], False) is False:
                        logging.error("\tFailed to apply display mode")
                        test_status = False
                        continue
                    html.step_end()

                    count = int(self.cmd_line_param[0]['COUNT'][0]) if self.cmd_line_param[0]['COUNT'] != 'NONE' else 1
                    for iteration in range(0, count):
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

                        test_status &= lrr.verify(
                            adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)

        if test_status is False:
            self.fail("FAIL: LRR verification after ModeSet operation")
        logging.info("PASS: LRR verification after ModeSet operation")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrModeSetTest))
    test_environment.TestEnvironment.cleanup(test_result)
