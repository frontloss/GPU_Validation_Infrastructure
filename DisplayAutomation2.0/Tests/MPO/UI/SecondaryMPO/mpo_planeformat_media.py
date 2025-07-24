########################################################################################################################
# @file         mpo_planeformat_media.py
# @brief        This test script performs various operations like enabling charms, app switch screen and media controls
#               on media file being opened in metro mode.
#               * Start Underrun monitor.
#               * Open media app and play it in maximized mode.
#               * Verify the plane format for CLONE and EXTENDED mode.
#               * Keep app running and try enabling and disabling charms to simulate planes enable/disable.
#               * Verify the plane format for CLONE and EXTENDED mode.
#               * Close the media app.
#               * Stop underrun monitor and check if any underrun was observed during the test execution.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import time
import sys
import unittest

import win32api
import win32con

from Libs.Core import enum, winkb_helper,window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_base

##
# @brief    Contains function to perform operations like enabling charms, app switch screen and media controls on media file
class MPOPlaneFormatMedia(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            gdhm.report_bug(
                title="[MPO][Plane formats]Incorrect command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error("Command line is incorrect")
            self.fail()

        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))

        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info("Applied Display configuration %s %s" % (DisplayConfigTopology(topology).name,
                                                                  self.mpo_helper.get_display_configuration(self.connected_list, self.enumerated_displays)))
            winkb_helper.press('WIN+M')

            ##
            # Open Media app and plays it in maximized mode
            self.mpo_helper.play_media(self.media_file, True)

            ##
            # To enable 'Repeat' option in the Video App
            winkb_helper.press("CTRL+T")
            # logging.info("Enabled Repeat option on media plaback")

            ##
            # The opened app will play for 1 minute
            time.sleep(60)

            ##
            # Verify the plane format for EXTENDED mode
            if topology == enum.EXTENDED:
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback application in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed during media playback application in EXTENDED mode",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed during media playback application in EXTENDED mode")
            ##
            # Verify the plane format for CLONE mode
            else:
                for display in range(0, len(self.connected_list)):
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback application in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_1', plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane formats]Plane verification failed during media playback application in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed during media playback application in CLONE mode")

            ##


            ##
            # When the MPO app is open try enabling and disabling charms to simulate planes enable/disable
            # logging.info("Enabling charms and media control plane in a loop")
            for iteration in range(1, 10):
                winkb_helper.press('WIN+P')
                logging.info(self.mpo_helper.getStepInfo() + "Enabled charms(WIN + P)")


                if self.os_info.BuildNumber <= '16299':  # Check for RS4 and above
                    ##
                    # Verify the plane format for EXTENDED mode
                    if topology == enum.EXTENDED:
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Charms plane in EXTENDED mode")
                        if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_2',
                                                  'source_pixel_format_RGB_8888'):
                            gdhm.report_bug(
                                title="[MPO][Plane formats]Plane verification failed for Charms plane in EXTENDED mode",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane verification failed for Charms plane in EXTENDED mode")
                    ##
                    # Verify the plane format for CLONE mode
                    else:
                        for display in range(0, len(self.connected_list)):
                            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for Charms plane in CLONE mode")
                            if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_2',
                                                      'source_pixel_format_RGB_8888'):
                                gdhm.report_bug(
                                    title="[MPO][Plane formats]Plane verification failed for Charms plane in CLONE mode",
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E2
                                )
                                self.fail("Plane verification failed for charms plane in CLONE mode")


                winkb_helper.press('ESC')
                logging.info(self.mpo_helper.getStepInfo() + "Disabled charms (WIN + P)")


                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1 + iteration, 1 + iteration)
                logging.info(self.mpo_helper.getStepInfo() + "Enabled media controls")


                if self.os_info.BuildNumber <= '16299':  # Check for RS4 and above
                    ##
                    # Verify the plane format for EXTENDED mode
                    if topology == enum.EXTENDED:
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media control plane in EXTENDED mode")
                        if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_2',
                                                  'source_pixel_format_RGB_8888'):
                            gdhm.report_bug(
                                title="[MPO][Plane formats]Plane verification failed for media control plane in EXTENDED mode",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane verification failed for media control plane in EXTENDED mode")
                    ##
                    # Verify the plane format for CLONE mode
                    else:
                        for display in range(0, len(self.connected_list)):
                            logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media control plane in CLONE mode")
                            if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_2',
                                                      'source_pixel_format_RGB_8888'):
                                gdhm.report_bug(
                                    title="[MPO][Plane formats]Plane verification failed for media control plane in CLONE mode",
                                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                    component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                    priority=gdhm.Priority.P2,
                                    exposure=gdhm.Exposure.E2
                                )
                                self.fail("Plane verification failed for media control plane in CLONE mode")


            ##
            # Close the MPO app at the end of the test
            window_helper.close_media_player()
            logging.info(self.mpo_helper.getStepInfo() + "Closed media player")
        else:
            self.fail("Display Configuration failed: %s %s" % (DisplayConfigTopology(topology).name,
                                                               self.connected_list))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test verifies enabling of MPO with media app running and"
                 "charms getting enabled, media controls enabled and disabled in a loop")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
