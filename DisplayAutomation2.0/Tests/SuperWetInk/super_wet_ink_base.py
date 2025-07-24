########################################################################################################################
# @file         super_wet_ink_base.py
# @brief        contains the base TestCase class for all superWetInk tests
# @details      @ref super_wet_ink_base.py New bfr tests can be created by inheriting this class and adding new
#               test functions. It implements the common setUp and tearDown functions.
#
#               For SuperWetInk validation, we are following below steps:
#                   1. Start ETL tracer
#                   2. Open the targeted app (Snip and Sketch Tool/Microsoft tool for boosting).
#                   3. Change the FPS by simulating keyboard key press events
#                   4. Close the app
#                   5. Stop ETL tracer
#                   6. Generate JSON reports from ETL file and verify below:
#                       * Boosted App gives flips in different duration parameters
#                       * VrrVmax / Vtotal programming immediately after Flip with different duration
#                       * Vbi Interval change after the RR is programmed
#                       * Unnecessary RR registers programming without trigger from OS
#                       * Under-run
#                       * TDR
#
#
# @author       Nivetha B
########################################################################################################################

import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_power
from Libs.Core.logger import html
from Tests.PowerCons.Modules import common, dut, workload

##
# @brief    BFR base class
class SuperWetInkBase(unittest.TestCase):
    cmd_line_param = None
    duration = 60

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any SuperWetInk test case. Helps to initialize some
    #               parameters required for SuperWetInk test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        # Get game playback duration
        if cls.cmd_line_param[0]['DURATION'] != 'NONE':
            cls.duration = int(cls.cmd_line_param[0]['DURATION'][0]) * 60  # convert into seconds

        dut.prepare(power_source=display_power.PowerSource.DC)

    ##
    # @brief        Test function to check panel and adapter satisfies the criteria for SuperWetInk
    # @return       None
    def t_00_requirements(self):
        html.step_start(f"Printing panel capabilities for SuperWetInk")

        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                # Printing Panel capabilities
                logging.info(f"{panel}:")
                logging.info(f"\t{panel.psr_caps}")
                logging.info(f"\t{panel.drrs_caps}")
                logging.info(f"\t{panel.lrr_caps}")
                logging.info(f"\t{panel.vrr_caps}")
                logging.info(f"\t{panel.bfr_caps}")
        html.step_end()

    ##
    # @brief        This method is the exit point for all SuperWetInk test cases. This resets the environment changes
    # @return       None
    @classmethod
    def tearDownClass(cls):
        dut.reset()
