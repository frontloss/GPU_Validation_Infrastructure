########################################################################################################################
# @file         planeformat_rotation.py
# @brief        Basic test to verify hardware rotation and plane format getting enabled on video app during rotation.
#               * Fetch the display configuration of all the displays connected.
#               * Play the Metro 3D app in Metro Mode.
#               * Verify the plane format for CLONE and EXTENDED mode.
#               * Rotate the display to 180, 270 and 0 degrees while the Video app is open.
#               * Close the App.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper,window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_base

##
# @brief    Contains function to check hardware rotation and plane format getting enabled on video app during rotation
class PlaneFormatRotation(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        target_id_list = []

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

        ##
        # fetch the display configuration of all the displays connected
        display_info = self.config.get_all_display_configuration()

        ##
        # target_id_list is a list of all the target_ids of the displays connected
        for displays in range(display_info.numberOfDisplays):
            target_id_list.append(display_info.displayPathInfo[displays].targetId)

        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info(self.mpo_helper.getStepInfo() + "Applied Display configuration as %s %s" % (
                DisplayConfigTopology(topology).name, self.mpo_helper.get_display_configuration(self.connected_list, self.enumerated_displays)))

            ##
            # Open the Metro 3D App in metro mode
            self.mpo_helper.play_media(self.media_file, True)

            ##
            # To enable 'Repeat' option in the Video App
            winkb_helper.press('CTRL+T')
            # logging.info("Enabling repeat option on media playback")

            time.sleep(60)

            ##
            # Verify the plane format for EXTENDED mode
            if topology == enum.EXTENDED:
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed during media playback in EXTENDED mode",
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
                    logging.info(self.mpo_helper.getStepInfo() + "%s: Verifying plane for media playback in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_1', plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane formats]Plane verification failed during media playback in CLONE mode",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Plane verification failed during media playback in CLONE mode")

            ##
            # fetch all the modes supported by each of the displays connected
            supported_modes = self.config.get_all_supported_modes(target_id_list)
            for key, values in supported_modes.items():
                for mode in values:
                    ##
                    # rotate the display to 90 degrees while the Video app is open
                    mode.rotation = enum.ROTATE_90
                    self.config.set_display_mode([mode])
                    logging.info(self.mpo_helper.getStepInfo() + "Display rotation set to 90: mode: %s" % mode.to_string(
                        self.enumerated_displays))
                    # to-do: Planes cannot be verified at present because
                    # "rotation in MPO is disabled currently due to MS issue: 8158628"

                    ##
                    # rotate the display to 180 degrees while the Video app is open
                    mode.rotation = enum.ROTATE_180
                    self.config.set_display_mode([mode])
                    logging.info(self.mpo_helper.getStepInfo() + "Display rotation set to 180: mode: %s" % mode.to_string(
                        self.enumerated_displays))
                    # to-do: Planes cannot be verified at present because
                    # "rotation in MPO is disabled currently due to MS issue: 8158628"

                    ##
                    # rotate the display to 270 degrees while the Video app is open
                    mode.rotation = enum.ROTATE_270
                    self.config.set_display_mode([mode])
                    logging.info(self.mpo_helper.getStepInfo() + "Display rotation set to 270: mode: %s" % mode.to_string(
                        self.enumerated_displays))
                    # to-do: Planes cannot be verified at present because
                    # "rotation in MPO is disabled currently due to MS issue: 8158628"

                    ##
                    # rotate the display to 0 degrees while the Video app is open
                    mode.rotation = enum.ROTATE_0
                    self.config.set_display_mode([mode])
                    logging.info(self.mpo_helper.getStepInfo() + "Display rotation set to 0: mode: %s" % mode.to_string(
                        self.enumerated_displays))

            window_helper.close_media_player()
            logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")

        else:
            self.fail("Failed to apply display configuration as %s %s" % (DisplayConfigTopology(topology).name,
                                                                          self.connected_list))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test to verify enabling of MPO during media playback with rotation of display")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
