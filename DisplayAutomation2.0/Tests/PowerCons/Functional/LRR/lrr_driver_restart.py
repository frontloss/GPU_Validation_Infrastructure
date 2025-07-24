#################################################################################################################
# @file         lrr_driver_restart.py
# @brief        Contains LRR driver restart tests
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core import display_essential
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains tests to verify LRR after driver restarts
class LrrDriverRestartTest(LrrBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        This function verifies LRR after DriverRestart operation
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_driver_restart(self):
        status = True

        for adapter in dut.adapters.values():
            status &= self.verify(adapter)
            logging.info(f"Step: Restart display driver for {adapter.name}")
            result, reboot_required = display_essential.restart_gfx_driver()
            if result is False:
                self.fail(f"Failed to restart display driver for {adapter.name}")
            logging.info("\tPASS: Restarted display driver successfully")
            status &= self.verify(adapter)

        if status is False:
            self.fail(f"FAIL: LRR Basic Verification after DriverRestart operation")
        logging.info(f"PASS: LRR Basic Verification after DriverRestart operation")

    ##
    # @brief        Helper function to verify LRR after driver restart
    # @param[in]    adapter Adapter
    # @return       None
    def verify(self, adapter: dut.Adapter) -> bool:
        test_status = True

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
            test_status &= lrr.verify(
                adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)

        return test_status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrDriverRestartTest))
    test_environment.TestEnvironment.cleanup(test_result)
