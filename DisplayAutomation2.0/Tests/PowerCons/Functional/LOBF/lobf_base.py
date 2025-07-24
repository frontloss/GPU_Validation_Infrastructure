#################################################################################################################
# @file         lobf_base.py
# @brief        Contains base class for all LOBF tests
# @details      @ref lobf_base.py <br>
#               This file implements unittest default functions for setUp and tearDown, common test functions used
#               across all lobf tests, and helper functions.
#
# @author       Bhargav Adigarla
#################################################################################################################

import logging
import sys
import unittest

from Libs.Core import cmd_parser, display_essential
from Libs.Core.display_config import display_config
from Libs.Core.display_power import DisplayPower
from Libs.Core.sw_sim import driver_interface
from Tests.PowerCons.Functional.LOBF import lobf
from Tests.PowerCons.Functional.DRRS import drrs
from Tests.PowerCons.Modules import common, dut


##
# @brief        Exposed Class to write Lobf tests. Any new LOBF test can inherit this class common setUp
#               and tearDown functions. LobfBase also includes some functions used across all LOBF tests.
class LobfBase(unittest.TestCase):
    cmd_line_param = None  # Used to store command line parameters
    driver_interface_ = driver_interface.DriverInterface()
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = DisplayPower()
    lfp_panels = []
    ext_panels = []
    dc_state = None
    method = 'IDLE' # Method used for feature verification APP/VIDEO

    ############################
    # Default UnitTest Functions
    ############################
    ##
    # @brief        This class method is the entry point for any LOBF test case. Helps to initialize some of the
    #               parameters required for LOBF test execution.
    # @details      This function checks for feature support and initialises parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info(" SETUP: LOBF_BASE ".center(common.MAX_LINE_WIDTH, "*"))

        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        if cls.cmd_line_param[0]['METHOD'] != 'NONE':
            cls.method = cls.cmd_line_param[0]['METHOD'][0]
            if len(cls.cmd_line_param[0]['METHOD']) > 1:
                if 'FPS' in cls.cmd_line_param[0]['METHOD'][1]:
                    fps = cls.cmd_line_param[0]['METHOD'][1]
                    if fps == 'FPS_30':
                        lobf.MEDIA_FPS = 30
                    elif fps == 'FPS_29.97':
                        lobf.MEDIA_FPS = 29.970
                    elif fps == 'FPS_59.94':
                        lobf.MEDIA_FPS = 59.94
                    elif fps == 'FPS_23.97':
                        lobf.MEDIA_FPS = 23.976
                    elif fps == 'FPS_25':
                        lobf.MEDIA_FPS = 25
                    else:
                        assert False, "Invalid Media fps value :{} passed in cmd-line".format(fps)

        dut.prepare()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is True:
                    cls.lfp_panels.append(panel)
                else:
                    cls.ext_panels.append(panel)

    ##
    # @brief        This method is the exit point for all DC States test cases. This resets the environment changes done
    #               for the DC States tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        logging.info(" TEARDOWN: ALPM ".center(common.MAX_LINE_WIDTH, "*"))
        dut.reset()
        cls.display_power_.enable_disable_simulated_battery(False)


