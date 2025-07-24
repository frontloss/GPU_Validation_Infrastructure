########################################################################################################################
# @file         planeformat_rotation.py
# @brief        Basic test to verify hardware rotation and plane format getting enabled with no corruption when video app
#               is being played with rotation.
#               * Play the Metro 3D app in Metro Mode.
#               * Verify the plane format for SINGLE display configuration.
#               * Rotate the display to 180, 270 and 0 degrees while the Video app is open.
#               * Close the App.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_base

##
# @brief    Contains function to check hardware rotation and plane format getting enabled with no corruption
class PlaneFormatRotation(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        target_id_list = []

        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            plane1_pixelformat = "source_pixel_format_YUV_422_PACKED_8_BPC"

        ##
        # set topology to SINGLE display configuration
        topology = enum.SINGLE

        ##
        # fetch the display configuration of all the displays connected
        display_info = self.config.get_all_display_configuration()

        ##
        # target_id_list is a list of all the target_ids of the displays connected
        for displays in range(display_info.numberOfDisplays):
            target_id_list.append(display_info.displayPathInfo[displays].targetId)

        ##
        # Apply SINGLE display configuration across all the displays
        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info(
                    "Applied the display configuration as %s %s" % (DisplayConfigTopology(topology).name,
                                                                    self.mpo_helper.get_display_configuration(
                                                                        [self.connected_list[display_index]], self.enumerated_displays)))
                ##
                # Open the Metro 3D App in metro mode
                self.mpo_helper.play_media(self.media_file, True)
                ##
                # To enable 'Repeat' option in the Video App
                winkb_helper.press('CTRL+T')
                # logging.info("Enabled repeat option on media playback application")
                # the App will run for 30 secs
                time.sleep(30)

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
                    self.fail("Plane verification failed on media playback")

                ##
                # fetch all the modes supported by each of the displays connected
                supported_modes = self.config.get_all_supported_modes(target_id_list)
                for key, values in supported_modes.items():
                    for mode in values:

                        ##
                        # rotate the display to 90 degrees while the Video app is open
                        mode.rotation = enum.ROTATE_90
                        self.config.set_display_mode([mode])
                        logging.info(self.mpo_helper.getStepInfo() + "Setting Display rotation to 90, mode: %s" % mode.to_string(
                            self.enumerated_displays))
                        # to-do: Planes cannot be verified at present because
                        # "rotation in MPO is disabled currently due to MS issue: 8158628"

                        # WM verification will be enabled once the above issue is resolved
                        # if self.wm.verify_watermarks() is not True:
                        #     self.fail("Error Observed in watermark verification")
                        # logging.info("Watermark verification passed")

                        ##
                        # rotate the display to 180 degrees while the Video app is open
                        mode.rotation = enum.ROTATE_180
                        self.config.set_display_mode([mode])
                        logging.info(self.mpo_helper.getStepInfo() + "Setting Display rotation to 180, mode: %s" % mode.to_string(
                            self.enumerated_displays))
                        # to-do: Planes cannot be verified at present because
                        # "rotation in MPO is disabled currently due to MS issue: 8158628"

                        # WM verification will be enabled once the above issue is resolved
                        # if self.wm.verify_watermarks() is not True:
                        #     self.fail("Error Observed in watermark verification")
                        # logging.info("Watermark verification passed")

                        ##
                        # rotate the display to 270 degrees while the Video app is open
                        mode.rotation = enum.ROTATE_270
                        self.config.set_display_mode([mode])
                        logging.info(self.mpo_helper.getStepInfo() + "Setting Display rotation to 270, mode: %s" % mode.to_string(
                            self.enumerated_displays))
                        # to-do: Planes cannot be verified at present because
                        # "rotation in MPO is disabled currently due to MS issue: 8158628"

                        # WM verification will be enabled once the above issue is resolved
                        # if self.wm.verify_watermarks() is not True:
                        #     self.fail("Error Observed in watermark verification")
                        # logging.info("Watermark verification passed")

                        ##
                        # rotate the display to 0 degrees while the Video app is open
                        mode.rotation = enum.ROTATE_0
                        self.config.set_display_mode([mode])
                        logging.info(self.mpo_helper.getStepInfo() + "Setting Display rotation to 0, mode: %s" % mode.to_string(
                            self.enumerated_displays))

                        time.sleep(5)

                        ##
                        # The media app will play for 1 minute
                        logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
                        if self.wm.verify_watermarks() is not True:
                            self.fail(
                                "Error Observed in watermark verification in media playback with display rotation = 0")
                        else:
                            logging.info(
                                "Watermark verification passed during media playback with display rotation = 0")



                window_helper.close_media_player()
                logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")

            else:
                self.fail(
                    "Failed to apply display configuration %s %s" % (DisplayConfigTopology(topology).name,
                                                                     self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Test to verify MPO getting enabled on video playback with display rotation")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
