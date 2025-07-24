#################################################################################################################
# @file         lrr_basic.py
# @brief        Contains LRR 2.5 concurrency test with PSR1
#
# @author       Mukesh M
#################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload


##
# @brief        Contains basic LRR2.5 concurrency tests with PSR1
class LrrPsr1(LrrBase):

    ##
    # @brief        Test function to verify LRR 2.5 concurrency with PSR1
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_lrr2_5_psr1(self):
        status = True

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # check if PSR1 is enabled before running the workload if yes set the status to False
                if psr.is_psr_enabled_in_driver(adapter, panel, psr.UserRequestedFeature.PSR_1):
                    logging.error(f"PSR1 is enabled on {adapter.gfx_index} with panel on {panel.port}")
                    status &= False
                    continue
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
                status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                     False, False, True, self.video_file)

        if status is False:
            self.fail("FAIL: LRR2.5 verification failed with PSR1")
        logging.info("PASS: LRR2.5 verification with PSR1 passed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrPsr1))
    test_environment.TestEnvironment.cleanup(test_result)
