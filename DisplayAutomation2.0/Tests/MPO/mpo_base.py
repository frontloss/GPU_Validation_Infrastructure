########################################################################################################################
# @file         mpo_base.py
# @brief        This script contains helper functions that will be used by MPO test scripts.
#               *SetUp function:
#                   * Plug the displays.
#                   * Verify devices are correctly plugged and enumerated.
#                   * Enable DFT framework and feature.
#               *Teardown function:
#                   * Disable DFT framework and feature.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_utility, flip
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Tests.MPO import mpo_dft_helper

##
# @brief    Contains unittest default functions for setUp and tearDown function
class MPOBase(unittest.TestCase):
    enable_mpo = None
    underrun = None
    platform = None
    config = DisplayConfiguration()
    machine_info = SystemInfo()
    connected_list = []
    mpo_helper_dft = mpo_dft_helper.MPODFTHelper()

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        ##
        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])

        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()

        ##
        # Get machine info
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
            break
        self.mpo_helper_dft.get_platform()

        self.underrun = UnderRunStatus()
        self.underrun.clear_underrun_registry()

        self.enable_mpo = flip.MPO()

        ##
        # Enable the DFT framework and feature
        self.enable_mpo.enable_disable_mpo_dft(True, 1)

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        ##
        # Disable the DFT framework and feature
        self.enable_mpo.enable_disable_mpo_dft(False, 1)
        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s" % display)
            display_utility.unplug(display)
        logging.info("************** TEST  ENDS HERE*************************")


if __name__ == '__main__':
    unittest.main()
