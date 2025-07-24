########################################################################################################################
# @file         mpo_planeformat_media.py
# @brief        This test script performs various operations like enabling charms, app switch screen and media controls
#               on media file being opened in metro mode.
#               * Apply display configuration.
#               * Open Media app and play it in maximized mode.
#               * Verify the plane format.
#               * When the MPO app is open try enabling and disabling charms to simulate planes enable/disable.
#               * Close the MPO app.
# @author       Shrivastava,Shubhangi , Ilamparithi Mahendran , Balasubramanyam,Smitha
########################################################################################################################
import logging
import sys
import time
import unittest

import win32api
import win32con

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_base

##
# @brief    Contains function that perform operations like enabling charms, app switch screen and media controls
class PlaneFormat_Media(mpo_ui_base.MPOUIBase):

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

        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info(
                    self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                        DisplayConfigTopology(topology).name,
                        self.mpo_helper.get_display_configuration([self.connected_list[display_index]], self.enumerated_displays)))
                winkb_helper.press('WIN+M')

                ##
                # Open Media app and plays it in maximized mode
                self.mpo_helper.play_media(self.media_file, True)
                ##
                # To enable 'Repeat' option in the Video App
                winkb_helper.press("CTRL+T")
                ##
                # The opened app will play for 1 minute
                time.sleep(60)

                logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
                if self.wm.verify_watermarks() is not True:
                    self.fail("Error Observed in watermark verification")
                else:
                    logging.info("Watermark verification passed")



                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1', plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed during media playback",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed during media playback")

                ##


                ##
                # When the MPO app is open try enabling and disabling charms to simulate planes enable/disable
                for iteration in range(1, 10):
                    winkb_helper.press('WIN+P')
                    logging.info(self.mpo_helper.getStepInfo() + "Enabled charms(WIN+P)")

                    if self.os_info.BuildNumber <= '16299':  # Check for RS4 and above
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for charms window(WIN+P)")
                        if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_2',
                                                  plane2_pixelformat):
                            gdhm.report_bug(
                                title="[MPO][Plane formats]Plane verification failed when charms (WIN+P) is enabled",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane verification failed when charms (WIN+P) is enabled")

                    winkb_helper.press('WIN+A')
                    logging.info(self.mpo_helper.getStepInfo() + "Enabled charms(WIN+A)")

                    if self.os_info.BuildNumber <= '16299':  # Check for RS4 and above
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for charms window(WIN+A)")
                        if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_2',
                                                  plane2_pixelformat):
                            gdhm.report_bug(
                                title="[MPO][Plane formats]Plane verification failed when charms (WIN+A) is enabled",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane verification failed when charms (WIN+A) is enabled")

                    winkb_helper.press('ESC')
                    logging.info(self.mpo_helper.getStepInfo() + "Disabled charms(WIN+A)")

                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1 + iteration, 1 + iteration)
                    logging.info(self.mpo_helper.getStepInfo() + "Enabled media controls")

                    if self.os_info.BuildNumber <= '16299':  # Check for RS4 and above
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media controls")
                        if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_2',
                                                  plane2_pixelformat):
                            gdhm.report_bug(
                                title="[MPO][Plane formats]Plane verification failed during media controls",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Plane verification failed during media controls")


                ##
                # Close the MPO app at the end of the test
                window_helper.close_media_player()
                logging.info(self.mpo_helper.getStepInfo() + "Closed media playback application")
            else:
                self.fail("Display Configuration failed %s %s" % (DisplayConfigTopology(topology).name,
                                                                  self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify underrun is not observed during various operations like"
                 "media playback in metro mode, enabling charms, media playback controls")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
