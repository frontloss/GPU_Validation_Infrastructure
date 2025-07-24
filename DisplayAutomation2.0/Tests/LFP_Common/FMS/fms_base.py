########################################################################################################################
# @file         fms_base.py
# @brief        This file contains the base class for LFP FMS test cases.
# @author       Tulika
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import cmd_parser
from Libs.Core import display_power
from Libs.Core import reboot_helper
from Libs.Core.display_config import display_config
from Tests.PowerCons.Modules import dut, common


##
# @brief        Exposed Class for LFP FMS tests. Any new LFP FMS test can inherit this class to use common setUp and
#               tearDown functions.
class LfpFmsBase(unittest.TestCase):
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    ##
    # @brief        This class method is the entry point for LFP FMS test cases which inherit this class.
    #               It does the initializations and setup required for LFP FMS test execution.
    # @details      This function parses command line arguments for display list and custom tags
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info(" SETUP: LFP FMS".center(common.MAX_LINE_WIDTH, "*"))
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        dut.prepare()

    ##
    # @brief        This method is the exit point for LFP FMS tests.
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info(" TEARDOWN: LFP FMS".center(common.MAX_LINE_WIDTH, "*"))
        dut.reset()
        logging.info("Test Cleanup Completed")

