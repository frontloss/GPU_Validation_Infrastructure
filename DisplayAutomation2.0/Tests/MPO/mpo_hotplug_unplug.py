########################################################################################################################
# @file         mpo_hotplug_unplug.py
# @brief        Basic test to verify enabling of MPO when media is running with hotplug and unplug of displays.
#               * Run the media application in fullscreen mode
#               * Unplug all the displays (except DP_A)
#               * Parse the command line and plug all the displays
#               * Verify plane programming
#               * Close the media application
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import sys
import time
import unittest

from Libs.Core import display_utility, enum, window_helper
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MPO import mpo_ui_base


##
# @brief    Contains function to check enabling of MPO when media is running with hotplug and unplug of displays
class HotPlugUnplug(mpo_ui_base.MPOUIBase):

    ##
    # @brief         Unittest runTest function
    # @return        None
    def runTest(self):
        if self.cmd_line_param['EXPECTED_PIXELFORMAT'] != 'NONE':
            plane1_pixelformat = self.mpo_helper.get_pixel_format(self.cmd_line_param['EXPECTED_PIXELFORMAT'][0])
            topology = eval(f"enum.{self.cmd_line_param['CONFIG']}")
        else:
            self.fail("Incorrect Commandline parameters. Add EXPECTED_PIXELFORMAT tag in commandline")

        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info(
                self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                    DisplayConfigTopology(topology).name,
                    self.mpo_helper.get_display_configuration(self.connected_list, self.enumerated_displays)))

        ##
        # Play media application in fullscreen mode
        self.mpo_helper.play_media(self.media_file, True)

        ##
        # Play for 60 seconds
        time.sleep(60)

        ##
        # Unplug the displays
        for each_display in self.connected_list:
            if each_display != 'DP_A':
                logging.info(f"Trying to unplug {each_display}")
                display_utility.unplug(each_display)

        ##
        # Plug the displays
        for each_display in self.connected_list:
            if each_display != 'DP_A':
                logging.info(f"Trying to plug {each_display}")
                display_utility.plug(each_display)

        if self.config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info(
                self.mpo_helper.getStepInfo() + "Applied the configuration as %s %s" % (
                    DisplayConfigTopology(topology).name,
                    self.mpo_helper.get_display_configuration(self.connected_list, self.enumerated_displays)))

        if topology == enum.EXTENDED:
            logging.info(
                self.mpo_helper.getStepInfo() + f"Verifying plane format for media in {self.mpo_helper.get_topology(topology)} mode")
            if self.mpo_helper.verify_planes(self.connected_list[0], 'PLANE_CTL_1', plane1_pixelformat) is False:
                self.mpo_helper.report_to_gdhm_verifcation_failure("media", topology, True)
                self.mpo_helper.fail_statement("media", topology, True)
            else:
                logging.info(
                    f"Plane verification passed for media in fullscreen mode with {self.mpo_helper.get_topology(topology)} config")

        ##
        # Close the app
        window_helper.close_media_player()
        logging.info(self.mpo_helper.getStepInfo() + "Closed media playback application")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Verifies enabling of MPO when media is running with hotplug and unplug of displays")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
