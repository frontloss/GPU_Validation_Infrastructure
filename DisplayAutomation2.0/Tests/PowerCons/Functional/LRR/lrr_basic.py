#################################################################################################################
# @file         lrr_basic.py
# @brief        Contains basic LRR test
#
# @author       Rohit Kumar
#################################################################################################################
from Libs.Core.display_config import display_config
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DRRS import drrs

from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload


##
# @brief        Contains basic LRR tests
class LrrBasicTest(LrrBase):
    display_config_ = display_config.DisplayConfiguration()

    ##
    # @brief        Test function for basic LRR verification
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_basic(self):
        status = True

        for adapter in dut.adapters.values():
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

                status &= lrr.verify(adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method,
                                     pause_video=False, verify_hrr=self.is_hrr_test, video=self.video_file)

                if drrs.verify_watermark_during_rr_switch(adapter, panel, etl_file) is False:
                    logging.error("FAIL: Watermark verification during RR switch")
                    status &= False

        if status is False:
            self.fail(f"FAIL: LRR Basic Verification with Method= {self.method}")
        logging.info(f"PASS: LRR Basic Verification with Method= {self.method}")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrBasicTest))
    test_environment.TestEnvironment.cleanup(test_result)
