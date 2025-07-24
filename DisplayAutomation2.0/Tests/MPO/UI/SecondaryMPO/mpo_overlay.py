########################################################################################################################
# @file         mpo_overlay.py
# @brief        Basic test to verify plane format getting enabled while video and overlay application is open.
#               * Open media app and play it in full screen mode.
#               * Verify the plane format for CLONE and EXTENDED mode.
#               * Play video in windowed mode.
#               * Open overlay application.
#               * Verify the plane format for CLONE and EXTENDED mode.
#               * Close the media and overlay application.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import os
import sys
import time
import unittest
from subprocess import Popen

from Libs.Core import enum, winkb_helper,window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Tests.MPO import mpo_ui_base

##
# @brief    Contains function to check plane format getting enabled while video and overlay application is open
class MPOOverlay(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            logging.error("Command line is incorrect")
            gdhm.report_bug(
                title="[MPO][Plane concurrency]Incorrect command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail()

        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))

        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info("Successfully applied the configuration as %s %s" % (
                DisplayConfigTopology(topology).name, self.mpo_helper.get_display_configuration(self.connected_list, self.enumerated_displays)))

            winkb_helper.press('WIN+M')

            ##
            # Opens media app and play it in full screen mode
            self.mpo_helper.play_media(self.media_file, True)

            ##
            # To enable 'Repeat' option in the Video App
            winkb_helper.press("CTRL+T")
            # logging.info("Enabling Repeat option on media playback")

            ##
            # The media app will play for 30 secs
            time.sleep(30)

            ##
            # Verify the plane format for EXTENDED mode
            if topology == enum.EXTENDED:
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback app in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed during media playback in EXTENDED mode",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed during media playback in EXTENDED mode")
            ##
            # Verify the plane format for CLONE mode
            else:
                for display in range(0, len(self.connected_list)):
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback app in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_1', plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane concurrency]Plane verification failed during media playback in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed during media playback in CLONE mode")

            ##
            # Play the video in windowed mode
            winkb_helper.press("ALT_ENTER")
            logging.info(self.mpo_helper.getStepInfo() + "Playing video in Windowed mode")

            time.sleep(1)

            ##
            # Open the overlay application
            logging.info(self.mpo_helper.getStepInfo() + "Launching dx9_overlay.exe")
            self.mpo_helper.app = Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                             cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))

            ##
            # Verify the plane format for EXTENDED mode
            if topology == enum.EXTENDED:
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback app in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for media playback in EXTENDED mode",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for  media playback in EXTENDED mode")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_2', 'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for Desktop window in EXTENDED mode",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for Desktop window in EXTENDED mode")
            ##
            # Verify the plane format for CLONE mode
            else:
                for display in range(0, len(self.connected_list)):
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback app in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_1', plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane concurrency]Plane verification failed for media playback in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed for media playback in CLONE mode")

                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_2',
                                              'source_pixel_format_RGB_8888'):
                        gdhm.report_bug(
                            title="[MPO][Plane concurrency]Plane verification failed for Desktop window in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed for Desktop window in CLONE mode")

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
            logging.info(self.mpo_helper.getStepInfo() + "Launching dx9_overlay.exe")
            self.mpo_helper.app = Popen(os.getcwd()[:2] + r'/SHAREDBINARY/920697932/dx9_overlay.exe',
                             cwd=os.path.join(test_context.SHARED_BINARY_FOLDER))
            if not self.mpo_helper.app:
                gdhm.report_bug(
                    title="[MPO][Plane concurrency]Failed to open overlay application",
                    problem_classification=gdhm.ProblemClassification.APP_CRASH,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Failed to open overlay application")
            else:
                logging.info("Successfully opened overlay application")

            # Breather time after the app opens
            time.sleep(0.5)

            ##
            # Verify the plane format for EXTENDED mode
            if topology == enum.EXTENDED:
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for overlay application in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', 'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed with overlay application in EXTENDED mode",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed with overlay application in EXTENDED mode")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop plane in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_2', 'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for Desktop plane in EXTENDED mode",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for Desktop plane in EXTENDED mode")
            ##
            # Verify the plane format for CLONE mode
            else:
                for display in range(0, len(self.connected_list)):
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for overlay application in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_1',
                                              'source_pixel_format_RGB_8888'):
                        gdhm.report_bug(
                            title="[MPO][Plane concurrency]Plane verification failed during overlay app in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed during overlay app in CLONE mode")

                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop plane in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_2',
                                              'source_pixel_format_RGB_8888'):
                        gdhm.report_bug(
                            title="[MPO][Plane concurrency]Plane verification failed for Desktop plane in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed for Desktop plane in CLONE mode")

            ##
            # Opens media app and plays it in windowed screen mode
            self.mpo_helper.play_media(self.media_file, False)

            ##
            # Verify the plane format for EXTENDED mode
            if topology == enum.EXTENDED:
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for overlay application in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', 'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed with overlay app in EXTENDED mode",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed with overlay app in EXTENDED mode")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_2', 'source_pixel_format_RGB_8888'):
                    gdhm.report_bug(
                        title="[MPO][Plane concurrency]Plane verification failed for Desktop window in EXTENDED mode",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for Desktop window in EXTENDED mode")
            ##
            # Verify the plane format for CLONE mode
            else:
                for display in range(0, len(self.connected_list)):
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for overlay application in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_1',
                                              'source_pixel_format_RGB_8888'):
                        gdhm.report_bug(
                            title="[MPO][Plane concurrency]Plane verification failed with overlay app in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed with overlay app in CLONE mode")

                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Desktop window in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_2',
                                              'source_pixel_format_RGB_8888'):
                        gdhm.report_bug(
                            title="[MPO][Plane concurrency]Plane verification failed for media Desktop window in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed for media Desktop window in CLONE mode")

            ##
            # Close the media app
            window_helper.close_media_player()
            logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")

            ##
            # Close the overlay application
            self.mpo_helper.app.terminate()
            logging.info(self.mpo_helper.getStepInfo() + "Closed overlay application")

        else:
            self.fail("Failed to apply the configuration as %s %s" % (DisplayConfigTopology(topology).name,
                                                                      self.connected_list))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Secondary MPO: Test to verify enabling of MPO during media playback and overlay application")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
