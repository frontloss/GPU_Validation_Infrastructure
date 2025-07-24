########################################################################################################################
# @file         planeformat_display_switch_sd.py
# @brief        Basic test to verify plane format getting enabled on video app during display switch.
#               * Create a configuration list of various topologies and the displays connected.
#               * Play video app in Metro mode.
#               * Apply each configuration across the displays connected.
#               * Verify plane programming.
#               * Close the Video App.
# @author       Shetty, Anjali N
########################################################################################################################
import itertools
import logging
import time
import sys
import unittest

from Libs.Core import enum, winkb_helper,window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.logger import gdhm
from Tests.MPO import mpo_ui_base

##
# @brief    Contains function to check plane format getting enabled on video app during display switch
class PlaneformatDisplaySwitchSD(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        disp_list = []
        config_list = []

        ##
        # topology list to apply various configurations on the displays connected
        topology_list = [enum.SINGLE, enum.CLONE, enum.EXTENDED]

        ##
        #
        for disp in range(len(self.connected_list)):
            disp_list.append(self.connected_list[disp])
        ##
        # creating a configuration list of various topologies and the displays connected
        # ex: SINGLE Disp1, CLONE Disp1+Disp 2, SINGLE Disp2, ...
        for i in range(2, len(disp_list) + 1):
            for subset in itertools.permutations(disp_list, i):
                for j in range(1, len(topology_list)):
                    config_list.append((topology_list[0], [subset[0]]))
                    config_list.append((topology_list[j], list(subset)))

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
        # Play the Video app in Metro Mode
        media_window_handle = self.mpo_helper.play_media(self.media_file, True)

        ##
        # applying each configuratin across the displays connected

        for each_config in range(0, len(config_list)):
            if self.config.set_display_configuration_ex(config_list[each_config][0],
                                                        config_list[each_config][1]) is True:

                # @Todo: Remove as part of VSDI-31758
                time.sleep(6)

                logging.info(self.mpo_helper.getStepInfo() + "Applied Display configuration as %s %s" % (
                    DisplayConfigTopology(config_list[each_config][0]).name,
                    self.mpo_helper.get_display_configuration(config_list[each_config][1], self.enumerated_displays)))

                ##
                # Moving the window to Full screen as after mode change the video is sometimes minimized.
                if media_window_handle:
                    logging.info("changing  media player to fullscreen mode")
                    winkb_helper.press("ALT_ENTER")
                    time.sleep(2)

                if config_list[each_config][0] == enum.SINGLE or config_list[each_config][0] == enum.EXTENDED:
                    ##
                    # Verify the plane format for SINGLE and EXTENDED mode
                    logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback in %s mode" %
                                 DisplayConfigTopology(config_list[each_config][0]).name)

                    if not self.mpo_helper.verify_planes(config_list[each_config][1][0], 'PLANE_CTL_1', plane1_pixelformat):
                        gdhm.report_bug(
                            title="[MPO][Plane concurrency]Plane verification failed in {0} mode with media playback"
                                .format(DisplayConfigTopology(config_list[each_config][0]).name),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail(
                            "Plane verification failed in %s mode with media playback" % DisplayConfigTopology(
                                config_list[each_config][0]).name)



            else:
                self.fail("Failed to apply display configuration as %s %s" % (
                    DisplayConfigTopology(config_list[each_config][0]).name, config_list[each_config][1]))

        ##
        # Close the Video App
        window_helper.close_media_player()
        logging.info(self.mpo_helper.getStepInfo() + "Closed media player app")

        # to-do : implement metro snap mode


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info(
        "Test purpose: Test to verify enabling of MPO during media playback with display switch(SINGLE/EXTENDED)")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
