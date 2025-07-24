########################################################################################################################
# @file         mpo_smoke_basic.py
# @brief        Basic test to verify MPO when media is played in windowed mode
#               * Open media app in windowed mode
#               * Verify plane parameters
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import enum, winkb_helper, window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ui_base


##
# @brief    Contains basic test to verify MPO during media playback
class MpoSmokeBasic(mpo_ui_base.MPOUIBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):

        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
            plane2_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][1])
            topology = eval(f"enum.{self.cmd_line_param['CONFIG']}")
        else:
            self.fail("Incorrect Commandline parameters. Add EXPECTED_PIXELFORMAT tag in commandline")

        for display_index in range(len(self.connected_list)):
            if self.config.set_display_configuration_ex(topology, [self.connected_list[display_index]]) is True:
                logging.info(
                    self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                        DisplayConfigTopology(topology).name,
                        self.mpo_helper.get_display_configuration([self.connected_list[display_index]],
                                                                  self.enumerated_displays)))
                winkb_helper.press('WIN+M')

                ##
                # Open Media app and play it in windowed mode
                self.mpo_helper.play_media(self.media_file, False)

                ##
                # Verify the plane format
                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for media playback")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_1',
                                                     plane1_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed during media playback",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for media playback")

                logging.info(self.mpo_helper.getStepInfo() + "Verifying plane for desktop screen")
                if not self.mpo_helper.verify_planes(self.connected_list[display_index], 'PLANE_CTL_2',
                                                     plane2_pixelformat):
                    gdhm.report_bug(
                        title="[MPO][Plane formats]Plane verification failed for desktop screen",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Plane verification failed for desktop screen")

                # Close media
                window_helper.close_media_player()
                logging.info(self.mpo_helper.getStepInfo() + "Closed media playback application")

            else:
                self.fail(f"Display Configuration failed {DisplayConfigTopology(topology).name} \
                                                        {self.connected_list[display_index]}")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: To verify MPO when media is played in in windowed mode")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
