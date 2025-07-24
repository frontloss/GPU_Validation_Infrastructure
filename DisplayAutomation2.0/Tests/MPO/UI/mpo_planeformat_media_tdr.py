########################################################################################################################
# @file         mpo_planeformat_media_tdr.py
# @brief        Basic test to verify  MPO enabling before and after TDR.
#               * Apply SINGLE display configuration.
#               * Open Media app and plays it in maximized mode.
#               * Verify the plane format.
#               * Generate & Verify TDR.
#               * Once again open the media app, play it in maximized mode and verify plane format.
#               * Close the MPO app.
# @author       Ilamparithi Mahendran
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core import display_essential
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.MPO import mpo_ui_base
from Libs.Core.logger import gdhm

##
# @brief    Contains function to check MPO enabling before and after TDR
class MPOPlaneFormatMediaTDR(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            plane1_pixelformat = "source_pixel_format_YUV_422_PACKED_8_BPC"

        ##
        # Apply SINGLE display configuration
        topology = enum.SINGLE
        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info(self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                    DisplayConfigTopology(topology).name,
                    self.mpo_helper.get_display_configuration([self.connected_list[display_index]], self.enumerated_displays)))
                winkb_helper.press('WIN+M')

                ##
                # Open Media app and plays it in maximized mode
                self.mpo_helper.play_media(self.media_file, False)

                ##
                # To enable 'Repeat' option in the Video App
                winkb_helper.press("CTRL+T")
                # logging.info("Enabling repeat option on media playback application")
                ##
                # The opened app will play for 30 secs
                time.sleep(30)

                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1', plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed during media playback",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed during media playback")
                else:
                    logging.info("Plane verification successful during media playback")
                ##


                ##
                # Generate & Verify TDR
                VerifierCfg.tdr = Verify.SKIP
                logging.debug("updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))
                logging.info(self.mpo_helper.getStepInfo() + "Generating TDR")
                if not display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Failed to generate TDR",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error('Failed to generate TDR')
                    self.fail()
                if display_essential.detect_system_tdr(gfx_index='gfx_0') is True:
                    logging.info('TDR generated successfully')

                ##
                # Wait for 5 seconds after generating TDR
                time.sleep(5)

                ##
                # Open Media app and plays it in maximized mode
                self.mpo_helper.play_media(self.media_file, False)
                ##
                # To enable 'Repeat' option in the Video App
                winkb_helper.press("CTRL+T")
                # logging.info("Enabling repeat option on media playback application")
                ##


                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane after TDR")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1', plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed after TDR",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed after TDR")
                logging.info("Plane verification successful after TDR")

                ##
                # Close the MPO app at the end of the test
                window_helper.close_media_player()
                logging.info(self.mpo_helper.getStepInfo() + "Closing media player application")

                if display_essential.clear_tdr() is True:
                    logging.info("TDR cleared successfully post MPO functionality verify post TDR")

            else:
                self.fail("Display Configuration failed as %s %s" % (DisplayConfigTopology(topology).name,
                                                                     self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test to verify enabling of MPO before and after TDR")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
