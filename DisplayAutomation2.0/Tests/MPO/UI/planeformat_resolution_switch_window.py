########################################################################################################################
# @file         planeformat_resolution_switch_window.py
# @brief        This test script verifies plane format getting enabled with no corruption on video app in windowed mode
#               during mode change across all the displays connected.
#               * Fetch the display configuration of all the displays connected.
#               * Apply SINGLE display configuration across all the displays
#               * Play the Video app in Window Mode.
#               * Fetch and apply all the modes supported by each of the displays connected.
#               * Close the Video App.
# @author       Balasubramnayam, Smitha
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
# @brief    Contais function to check plane format getting enabled with no corruption on video app in windowed mode
class PlaneFormatResolutionSwitchWindow(mpo_ui_base.MPOUIBase):

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
                logging.info(self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                    DisplayConfigTopology(topology).name,
                    self.mpo_helper.get_display_configuration([self.connected_list[display_index]], self.enumerated_displays)))

                ##
                # Play the Video app in Window Mode
                self.mpo_helper.play_media(self.media_file, False)
                ##
                # To enable 'Repeat' option in the Video App
                winkb_helper.press("CTRL+T")
                # logging.info("Enabled repeat option on media playback application")
                # The media Playback will run for 30 secs
                time.sleep(30)
                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1', plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane scaling]Plane verification failed during media playback",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed on media playback")



                logging.info(self.mpo_helper.getStepInfo() + "Verifying watermark")
                if self.wm.verify_watermarks() is not True:
                    self.fail("Error Observed in watermark verification")
                else:
                    logging.info("Watermark verification passed")

                ##
                # fetch all the modes supported by each of the displays connected
                supported_modes = self.config.get_all_supported_modes(target_id_list)
                for key, values in supported_modes.items():
                    for mode in values:
                        ##
                        # set all the supported modes
                        logging.info(self.mpo_helper.getStepInfo() + "Applying Display mode: %s" % (
                            mode.to_string(self.enumerated_displays)))
                        self.config.set_display_mode([mode])

                ##
                # Close the Video App
                window_helper.close_media_player()
                logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")

            else:
               self.fail(
                    "Failed to apply display configuration as %s %s" % (DisplayConfigTopology(topology).name,
                                                                        self.connected_list[display_index]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify MPO is getting enabled on video playback in windowed mode with mode change"
                 "across all the connected display")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
