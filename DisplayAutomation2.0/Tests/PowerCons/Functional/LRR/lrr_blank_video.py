########################################################################################################################
# @file         lrr_blank_video.py
# @brief        This file contains test for LRR with blank video
#
# @author       Rohit Kumar
########################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.LRR.lrr_base import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import workload


##
# @brief        Contains LRR test with Blank Video
class LrrBlankVideo(LrrBase):
    ##
    # @brief        This test function test verifies LRR with Blank video in DC mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_basic_dc(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                etl_file, polling_data = workload.run(
                    workload.VIDEO_PLAYBACK_USING_FILE,
                    [self.video_file, self.duration_in_seconds],
                    [psr.get_polling_offsets(psr.UserRequestedFeature.PSR_2), self.polling_delay_in_seconds]
                )

                if etl_file is None:
                    self.fail(f"FAILED to run workload for Video Playback using {self.video_file}")
                status &= lrr.verify(
                    adapter, panel, etl_file, polling_data, self.method, self.rr_switching_method, video=self.video_file)

        if status is False:
            self.fail("Fail: LRR verification with blank video")
        logging.info("\tPASS: LRR verification with blank video")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(LrrBlankVideo))
    test_environment.TestEnvironment.cleanup(test_result)
