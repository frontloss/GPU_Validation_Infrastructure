########################################################################################################################
# @file         video_playback.py
# @details      @ref video_playback.py <br>
#               This file implements video playback scenario for all display pc feature testing.
#
# @author       Ashish Tripathi
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.EventValidation.Basic.event_validation_base import *
from Libs.Core import window_helper, app_controls


##
# @brief        This class contains tests for events with video playback
class VideoPlayBack(EventValidationBase):
    ##
    # @brief        This function verifies events with video playback
    # @return       None
    def test_video_playback(self):
        video_list = ["mpo_3840_2160_avc", "mpo_1920_1080_avc"]
        logging.info(" SCENARIO: {0} ".format(self.cmd_test_name.upper()).center(common.MAX_LINE_WIDTH, "*"))

        for itr in range(len(video_list)):
            logging.info("Running Workload VIDEO_PLAYBACK for 30 seconds")
            logging.info("\tVideo Playback started : {0}.mp4".format(video_list[itr]))
            app_controls.launch_video(os.path.join(common.MPO_VIDEOS_PATH, "{0}.mp4".format(video_list[itr])))
            time.sleep(30)
            window_helper.close_media_player()
            logging.info("\tClosing media player")
        self.check_validators()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
