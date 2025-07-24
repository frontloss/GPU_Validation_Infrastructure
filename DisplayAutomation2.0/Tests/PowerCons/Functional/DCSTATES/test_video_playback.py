########################################################################################################################
# @file         test_video_playback.py
# @brief        Test for DC state in video playback scenario
#
# @author       Vinod D S
########################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.DCSTATES.dc_state_base import *


##
# @brief        This class contains DC States tests with video playback
class DcStateVideoPlayback(DCStatesBase):
    ##
    # @brief        This function verifies DC6V with Video playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC6V"])
    # @endcond
    def t_10_test_dc6v(self):
        self.video_fps = [24.000]
        for adapter in dut.adapters.values():
            logging.info("Step: Verifying DC6v with Video playback")
            for v_fps in self.video_fps:
                if dc_state.verify_dc6v(adapter, method='VIDEO', fps=v_fps) is False:
                    self.fail("DC6v verification with video failed")
                logging.info("\tDC6v verification with video is successful")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DcStateVideoPlayback))
    test_environment.TestEnvironment.cleanup(test_result)
