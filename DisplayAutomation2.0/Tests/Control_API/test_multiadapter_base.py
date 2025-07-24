############################################################################################
# @file         test_multiadapter_base.py
# @brief        This script contains helper functions that will be used by igcl multi adapter test script
# @author       Dheeraj Dayakaran
############################################################################################


import sys
import logging
import unittest
from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core.logger import gdhm
from collections import OrderedDict
from Tests.Planes.Common import plug_display_wrapper


##
# @brief - Test base for IGCL multi adapter
class IGCLMultiAdapterBase(unittest.TestCase):
    connected_list = []
    stepCounter = 0
    display_details = OrderedDict()  # To store the gfx_index as key and connector port as the value

    ##
    # @brief            Creates display adapter key value pairs
    # @param[in]        key : gfx index
    # @param[in]        value : connector port
    # @return           void
    def create_display_adapter_list(self,key,value):
        if not bool(self.display_details):
            self.display_details[key] = []
            self.display_details[key].append(value)
        else:
            if key in self.display_details.keys():
                self.display_details[key].append(value)
            else:
                self.display_details[key] = []
                self.display_details[key].append(value)

    ##
    # @brief            Helper function to get all details
    # @return           void
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")

        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)

        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        self.connected_list.insert(value['index'], value['connector_port'])
                        self.create_display_adapter_list(value['gfx_index'], value['connector_port'])
        

        if len(self.connected_list) >= 2:
            for key, value in self.display_details.items():
                if len(value) <= 0:
                    gdhm.report_driver_bug_clib("Plug and verify display failed due to invalid commandline parameters")
                    self.fail("Minimum 1 display is required per adapter")

            for index in range(0, len(self.cmd_line_param)):
                for key, value in self.cmd_line_param[index].items():
                    if cmd_parser.display_key_pattern.match(key) is not None:
                        if value['connector_port'] is not None:
                            plug_display_wrapper.plug_display(value['connector_port'], self.cmd_line_param[index])
        else:
            gdhm.report_driver_bug_clib("Plug and verify display failed due to invalid commandline parameters")
            self.fail("Minimum 2 displays are required to test IGCL in multi-adapter configuration")

    ##
    # @brief        Get the step value for logging.
    # @return       Step count.
    def getStepInfo(self):
        self.stepCounter = self.stepCounter + 1
        return "STEP-%d: " % self.stepCounter

    ##
    # @brief        To restore to initial config
    # @return       Void
    def tearDown(self):
        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for key, value in self.display_details.items():
            for display in value:
                logging.info("Trying to unplug %s", display)
                display_utility.unplug(display, gfx_index=key.lower())
        logging.info("****************TEST ENDS HERE********************************")