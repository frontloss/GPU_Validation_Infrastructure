########################################################################################################################
# @file         mpo_overlay.py
# @brief        Basic test to verify plane format getting enabled with no corruption while video and overlay app is
#               played.
#               * Apply display configuration.
#               * Open media app and play it in full screen mode.
#               * Verify the plane format.
#               * Play the video in windowed mode, open the overlay application.
#               * Verify the plane format.
#               * Perform Watermark verification at different scenarios as mentioned below:
#                   * WM verification with both Media player and Overlay application.
#                   * WM verification with Overlay application only.
#               * Close the media and overlay application.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import os
import sys
import time
import unittest
from subprocess import Popen

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ui_base


##
# @brief    Contains function to check plane format getting enabled with no corruption while video and overlay app is played
class MPOOverlay(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        topology = enum.SINGLE
        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
            plane2_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][1])
        else:
            plane1_pixelformat = "source_pixel_format_YUV_422_PACKED_8_BPC"
            plane2_pixelformat = "source_pixel_format_RGB_8888"

        ##
        # Apply display configuration
        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]):
                logging.info(self.mpo_helper.getStepInfo() + "Applied Display configuration as %s %s" %
                             (DisplayConfigTopology(topology).name,
                              self.mpo_helper.get_display_configuration([self.connected_list[display_index]],
                                                                        self.enumerated_displays)))
                winkb_helper.press('WIN+M')

                ##
                # Opens media app and plays it in full screen mode
                self.mpo_helper.play_media(self.media_file, True)

                ##
                # To enable 'Repeat' option in the Video App
                winkb_helper.press("CTRL+T")

                ##
                # The media app will play for 1 minute
                time.sleep(60)

                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                     plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed during media playback",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed during media playback")

                ##
                # Play the video in windowed mode
                winkb_helper.press("ALT_ENTER")
                logging.info(self.mpo_helper.getStepInfo() + "Playing media application in windowed mode")

                time.sleep(1)

                ##
                # Open the overlay application
                logging.info(self.mpo_helper.getStepInfo() + "Launching overlay app(dx9_overlay.exe)")
                self.mpo_helper.app = Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                                            cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))

                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback application")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                     plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for media playback application",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for media playback application")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_2',
                                                     plane2_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for Desktop window",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for Desktop window")

                ##
                # WM verification with both Media player and Overlay application
                logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark when media playback app is running")
                if self.wm.verify_watermarks() is not True:
                    self.fail("Error Observed in watermark verification")
                else:
                    logging.info("Watermark verification passed")

                ##
                # Close the media app
                window_helper.close_media_player()
                logging.info(self.mpo_helper.getStepInfo() + "Closed media playback application")

                ##
                # Close the overlay application
                self.mpo_helper.app.terminate()
                logging.info(self.mpo_helper.getStepInfo() + "Closed overlay application")

                ##
                # Open the overlay application
                logging.info(self.mpo_helper.getStepInfo() + "Launching overlay app(dx9_overlay.exe)")
                self.mpo_helper.app = Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                                            cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
                if not self.mpo_helper.app:
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Failed to launch overlay application",
                        problem_classification=gdhm.ProblemClassification.APP_CRASH,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Failed to launch overlay application")
                else:
                    logging.info("Launched overlay application successfully")

                time.sleep(2)

                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for overlay application")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                     'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for overlay application",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for overlay application")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop Window")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_2',
                                                     'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for Desktop Window",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for Desktop Window")

                ##
                # WM verification with Overlay application only
                logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
                if self.wm.verify_watermarks() is not True:
                    self.fail("Error Observed in watermark verification")
                else:
                    logging.info("Watermark verification passed")

                ##
                # Opens media app and plays it in windowed screen mode
                self.mpo_helper.play_media(self.media_file, False)

                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for overlay application")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                     'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for overlay application",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for overlay application")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_2',
                                                     'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for Desktop window",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for Desktop window")

                ##
                # Close the media app
                window_helper.close_media_player()
                logging.info(self.mpo_helper.getStepInfo() + "Closed media playback application")

                ##
                # Close the overlay application
                self.mpo_helper.app.terminate()
                logging.info(self.mpo_helper.getStepInfo() + "Closed overlay application")

            else:
                self.fail(
                    "Failed to apply Display configuration %s %s" % (DisplayConfigTopology(topology).name,
                                                                     self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test to verify enabling of MPO during media playback and overlay apps running")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
