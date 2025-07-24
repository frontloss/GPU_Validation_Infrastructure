#################################################################################################################
# @file         lrr_display_switching.py
# @brief        Contains LRR display switching tests
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload


##
# @brief        Contains LRR tests with display switching
class LrrDisplaySwitchingTest(LrrBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        Helper function containing the verification steps for LRR
    # @return       None
    def _verification_steps(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue

                logging.info("Step: Setting display configuration: SINGLE {0}".format(panel.port))
                if self.display_config_.set_display_configuration_ex(
                        enum.SINGLE, [panel.display_info.DisplayAndAdapterInfo]) is False:
                    self.fail("Failed to apply display configuration")

                dut.refresh_panel_caps(adapter)

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

                return lrr.verify(
                    adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)

    ##
    # @brief        Function for LRR verification after switching from CLONE/EXTENDED to SINGLE
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_single_idle(self):
        # From Clone/Extended to Single
        if self._verification_steps() is False:
            self.fail("LRR verification failed after switching from CLONE/EXTENDED to SINGLE")

    ##
    # @brief        Function for LRR verification after switching from SINGLE external to SINGLE eDP
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_12_external_to_edp(self):
        # From Single external to Single eDP
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp:
                    continue
                logging.info("Step: Setting display configuration: SINGLE {0}".format(panel.port))
                if self.display_config_.set_display_configuration_ex(
                        enum.SINGLE, [panel.display_info.DisplayAndAdapterInfo]) is False:
                    self.fail("Failed to apply display configuration")
                break

        if self._verification_steps() is False:
            self.fail("LRR verification failed after switching from SINGLE external to SINGLE eDP")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrDisplaySwitchingTest))
    test_environment.TestEnvironment.cleanup(test_result)
