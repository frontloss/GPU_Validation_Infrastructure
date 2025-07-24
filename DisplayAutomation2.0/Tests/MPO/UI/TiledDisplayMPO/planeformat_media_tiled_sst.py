########################################################################################################################
# @file         planeformat_media_tiled_sst.py
# @brief        Basic test to verify register programming and also check for underrun during basic video playback
#               scenario on Tiled display.
#               * Get the DP panel details from the command line and plug tiled display.
#               * Set display configuration and apply max tiled mode.
#               * Play media content in fullscreen.
#               * Verify plane programming.
#               * Close the media player.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import winkb_helper, window_helper
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ui_tiled_sst_base

##
# @brief    Contains function to check register programming and underrun during basic video playback scenario on Tiled display
class PlaneFormatMediaTiledSST(mpo_ui_tiled_sst_base.MPOUITiledSSTBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        ##
        # Expected pixel format
        pixel_format = self.mpo_helper.get_pixel_format_value('YUV420_8BPC')

        ##
        # Get the DP panel details from the command line
        self.sst_base.process_cmdline()

        ##
        # Get the config details
        topology = self.sst_base.config

        ##
        # Plug tiled display
        self.sst_base.tiled_display_helper("Plug")

        ##
        # Set display configuration
        self.sst_base.set_config(topology)

        ##
        # Set max tiled mode
        self.sst_base.apply_tiled_max_modes()

        ##
        # Minimize all the windows
        winkb_helper.press('WIN+M')

        ##
        # Play media content in fullscreen
        self.mpo_helper.play_media(self.media_file, True)

        time.sleep(60)

        ##
        # Verify plane programming
        logging.info("************************Plane verification started************************")
        if not self.mpo_helper.verify_planes_sst(pixel_format, 'PLANE_CTL_1'):
            gdhm.report_bug(
                title="[MPO]Plane verification failed during fullscreen video playback on Tiled display",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Plane verification failed during fullscreen video playback on Tiled display")
        else:
            logging.info("Plane verification passed for fullscreen video playback on Tiled display")
        logging.info("*************************Plane verification ended*************************")

        ##
        # Close the media player
        window_helper.close_media_player()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify for register programming and also check for underrun during basic"
                 "video playback scenario on Tiled Display")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
