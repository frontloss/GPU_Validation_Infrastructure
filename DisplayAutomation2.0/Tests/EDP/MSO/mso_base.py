#######################################################################################################################
# @file         mso_base.py
# @addtogroup   EDP
# @section      MSO_Base
# @brief        @ref mso_base.py contains common setUp and tearDown steps for all MSO tests. Also contains the
#               common test functions used across all the MSO verification scenarios.
#
# @author       Bhargav Adigarla
#######################################################################################################################

import logging
import sys
import unittest

from Libs.Core import cmd_parser, enum, display_power, display_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Tests.EDP.MSO import mso
from Tests.PowerCons.Modules import common, dut, workload
from registers.mmioregister import MMIORegister


##
# @brief        Exposed Base Class for MSO test cases with setup, teardown and common functions used by the tests
class MsoBase(unittest.TestCase):
    cmd_line_param = None
    edp_panels = []
    target_ids = {}
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    external_panels = []
    mso_panels = []
    mso_target_ids = {}
    mso_valid_links = [0, 2, 4]
    plugged_display = []

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This function creates setup required for execution of MSO tests
    # @details      It parses the command line, checks eDP connection and MSO support
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info(" SETUP: MSO_BASE ".center(common.MAX_LINE_WIDTH, "*"))

        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        dut.prepare()

        ##
        # Check for all the eDPs given in command line
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if not panel.is_lfp:
                    cls.external_panels.append(panel.port)
                    continue
                if panel.panel_type == 'DP':
                    cls.edp_panels.append(panel.port)

                if mso.is_mso_supported_in_panel(panel.target_id):
                    logging.info("MSO supported in {0}".format(panel.pipe))
                    cls.mso_panels.append(panel)
                    cls.mso_target_ids[panel.port] = panel.target_id
                else:
                    logging.debug("Connected panel is not supporting MSO {0} (Planning Issue)".format(panel.pipe))
                    gdhm.report_driver_bug_di(f"{mso.GDHM_MSO_COG} connected panel is not supporting MSO")

    ##
    # @brief        This function creates setup required for execution of MSO tests
    # @details      It parses the command line, checks eDP connection and MSO support
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: MSO_BASE ".center(common.MAX_LINE_WIDTH, "*"))
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        dut.reset()

    ############################
    # Test Functions
    ############################

    ##
    # @brief        Test to verify all the requirements to start the test.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        if len(self.mso_panels) == 0:
            self.fail("Minimum one mso capable panel is required for testing(planning issue)")
