######################################################################################
# @file             mipi_drrs_media_playback.py
# @addtogroup       Test_Power_DRRS
# @brief            This files contains test to verify the basic scenario of entering the DRRS with media playback.
# @details          DRRS state is verified before the media playback, during the media playback and after the media
#                   playback with and without fullscreen media launch
#                   CommandLine:python drrs_media_playback.py -mipi_a
#                   Test will pass only if DRRS status bits are set, after display scenario. else fails.
#                   Pre-requisite : Install WDTF Framework before running the test (This test uses SIMBATT)
# @note             Do not modify this test without consent from the author.
# @author           Kruti Vadhavaniya
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Power.MIPI_DRRS.mipi_drrs_base import *


##
# @brief        This class contains tests to verify Mipi DRRS with media playback
class DrrsMediaPlayback(MipiDrrsBase):

    ##
    # @brief        This function verifies Mipi DRRS before video playback with idle desktop and
    #               during the video playback
    # @return       None
    def runTest(self):
        # 1 verifying basic scenario of entering DRRS state, before media playback
        logging.info("verifying the basic scenario of entering DRRS state, before media playback")
        drrs_check = 1

        for display_port in self.current_connected_displays_list:
            self.do_idle_desktop()
            expected_refresh_rate = self.gfx_vbt.block_42.SeamlessDrrsMinRR[self.panel_index]
            drrs_check &= self.check_drrs_status(display_port, expected_rr=expected_refresh_rate)

        if drrs_check == 1:
            logging.info("PASS: DRRS check: Before media playback system DRRS state")
        else:
            logging.error("FAIL: DRRS check: Before media playback system DRRS state")
            self.fail_count += 1

        # 2 verifying basic scenario of entering DRRS state, during media playback
        for display_port in self.current_connected_displays_list:
            drrs_check &= self.check_drrs_with_media_playback(display_port, media_fps=self.media_fps)

        if (drrs_check == 1):
            logging.info("PASS: DRRS check: After media playback system DRRS state")
        else:
            logging.error("FAIL: DRRS check: After media playback system DRRS state")
            self.fail_count += 1


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
