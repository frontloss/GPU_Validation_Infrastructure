########################################################################################################################
# @file         planeformat_resolution_switch_window.py
# @brief        Basic test to verify plane format getting enabled on video app in windowed mode during mode change.
#               * Fetch the display configuration of all the displays connected.
#               * Play the Video app in Window Mode.
#               * Verify the plane format for CLONE and EXTENDED mode.
#               * Fetch all the modes supported by each of the displays connected.
#               * Close the Video App.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ui_base


##
# @brief    Contains function to verify plane format getting enabled on video app in windowed mode during mode change
class PlaneFormatResolutionSwitchWindow(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        target_id_list = []
        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
        else:
            gdhm.report_bug(
                title="[MPO][Plane concurrency]Incorrect command line",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.error("Command line is incorrect")
            self.fail()

        ##
        # fetch the display configuration of all the displays connected
        display_info = self.config.get_all_display_configuration()

        ##
        # target_id_list is a list of all the target_ids of the displays connected
        for displays in range(display_info.numberOfDisplays):
            target_id_list.append(display_info.displayPathInfo[displays].targetId)

        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))

        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info(self.mpo_helper.getStepInfo() + "Applied Display configuration as %s %s" % (
                DisplayConfigTopology(topology).name,
                self.mpo_helper.get_display_configuration(self.connected_list, self.enumerated_displays)))
            ##
            # Play the Video app in Window Mode
            self.mpo_helper.play_media(self.media_file, False)

            ##
            # To enable 'Repeat' option in the Video App
            winkb_helper.press("CTRL+T")
            # logging.info("Enabling repeat option on media playback application")

            ##
            # Verify the plane format for EXTENDED mode
            if topology == enum.EXTENDED:
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback in EXTENDED mode")
                if not self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane scaling]Plane verification failed during media playback in EXTENDED mode",
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
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback in CLONE mode")
                    if not self.mpo_helper.verify_planes(self.connected_list[display], 'PLANE_CTL_1',
                                                         plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane scaling]Plane verification failed during media playback in CLONE mode",
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
                    # set all the supported modes
                    logging.info(
                        self.mpo_helper.getStepInfo() + "Applying Display mode: %s" % mode.to_string(
                            self.enumerated_displays))
                    self.config.set_display_mode([mode])

            ##
            # Close the Video App
            window_helper.close_media_player()
            logging.info(self.mpo_helper.getStepInfo() + "Closed media player application")

        else:
            self.fail("Failed to apply display configuration %s %s" % (DisplayConfigTopology(topology).name,
                                                                       self.connected_list))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Test to verify enabling of MPO during media playabck with display mode changed to EXTENDED / SINGLE")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
