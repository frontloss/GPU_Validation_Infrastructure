########################################################################################################################
# @file         idd_base.py
# @brief        This test script implements unittest default functions for setUp and tearDown for IDD tests
# @author       Pai, Vinayak1
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import reboot_helper, cmd_parser
from Libs.Core.logger import gdhm
from Tests.VirtualDisplay.Yangra import virtual_display_helper

LINE_WIDTH = 64


##
# @brief    This class contains unittest setUp and tearDown function for IDD tests
class IDDBase(unittest.TestCase):
    custom_tags = [
        '-MONITOR_RESOLUTION',  # Expected values [1080p, 1440p, 2160p]
        '-APP',                 # Expected values [FLIPAT, D3D12FULLSCREEN, CLASSICD3D]
        '-TIME'                 # Expected values [Integer values]
    ]

    ##
    # @brief        Unittest setUp function
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("TEST STARTS HERE".center(LINE_WIDTH, '*'))

        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)
        if self.cmd_line_param['MONITOR_RESOLUTION'] != 'NONE':
            self.monitor_resolution = self.cmd_line_param['MONITOR_RESOLUTION'][0]
        else:
            self.monitor_resolution = '1080P'
        logging.info(f"CmdLineParams(MonitorResolution:{self.monitor_resolution})")

        logging.info("Step: Uninstall Microsoft Display Adapter")
        if virtual_display_helper.disable_msft_display_driver() is False:
            gdhm.report_test_bug_os(f"{virtual_display_helper.GDHM_IDD} MSFT Driver is not Disabled")
            self.fail("MSFT Driver is not Disabled [Test Issue]")

        if reboot_helper.reboot(self, callee="runTest") is False:
            gdhm.report_test_bug_os(f"{virtual_display_helper.GDHM_IDD} Failed to reboot the system")
            self.fail("Failed to reboot the system [Test Issue]")

    ##
    # @brief        Unittest tearDown function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Step: Uninstall the Driver")
        if virtual_display_helper.install_uninstall_idd_driver(virtual_display_helper.IddDriver.UNINSTALL,
                                                               self.monitor_resolution) is False:
            gdhm.report_test_bug_os(f"{virtual_display_helper.GDHM_IDD} Uninstall of IDD Driver Failed")
            self.fail("")

        logging.info("TEST ENDS HERE".center(LINE_WIDTH, '*'))
