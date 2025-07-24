######################################################################################
# @file         port_sync_with_clone_video_playback.py
# @brief        This file contains tests to verify port sync during clone video playback.
# @details      Verify port sync during clone video playback. If sync is proper in this case, there shouldn't be any
#               visual lag between the two displays
# @author       Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.LFP_Common.Port_Sync.port_sync_base import *


##
# @brief       This class contains basic LFP Port Sync tests with clone video playback in windowed and full screen mode
class PortSyncWithCloneVideoPlayback(PortSyncBase):

    ##
    # @brief      This test function verifies LFP Port Sync during clone video playback in windowed and full screen mode
    # @return     None
    def runTest(self):
        media_fps = 24
        video_file = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos", "{0:.3f}.mp4".format(media_fps))

        # run video playback in fullscreen and verify port sync during video playback
        logging.info('Step :\t Run video playback in fullscreen and check for port sync')
        self.test_result &= self.capture_trace_and_verify_port_sync_during_playback(is_full_screen=True)

        # run video playback in windowed mode and verify port sync during video playback
        logging.info('Step :\t Run video playback in windowed mode and check for port sync')
        self.test_result &= self.capture_trace_and_verify_port_sync_during_playback(is_full_screen=False)

        # report test failure if any verifications failed
        if self.test_result == False:
            self.fail('Some checks in the test have failed. Check ERROR logs.')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
