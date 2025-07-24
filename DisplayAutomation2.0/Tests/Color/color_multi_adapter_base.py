############################################################################################
# \file         color_multi_adapter_base.py
# \section      color_multi_adapter_base
# \remarks      This script contains helper functions that will be used by color multi adapter test scripts
# \ref          color_multi_adapter_base.py \n
# \author       Vimalesh D
############################################################################################


import sys
import logging
import unittest
from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core import reboot_helper
from Libs.Core.logger import gdhm
from Libs.Core.display_config import display_config
from collections import OrderedDict


class ColorMultiAdapterBase(unittest.TestCase):
    connected_list = []
    plugged_display = []
    platform = None
    app = None
    target_id = 0
    display = None
    stepCounter = 0
    display_details = OrderedDict()  # To store the gfx_index as key and connector port as the value
    ycbcr_enable_status = 0
    ycbcr_supported = 0

    def create_display_adapter_list(self, key, value):
        if not bool(self.display_details):
            self.display_details[key] = []
            self.display_details[key].append(value)
        else:
            if key in self.display_details.keys():
                self.display_details[key].append(value)
            else:
                self.display_details[key] = []
                self.display_details[key].append(value)

    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info("************** TEST  STARTS HERE*************************")
        ##
        # Parse the command line.
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv)
        ##
        # Verify and plug the display
        self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)
        ##
        # Obtain display port and adapter list from the command line.
        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        self.connected_list.insert(value['index'], value['connector_port'])
                        self.create_display_adapter_list(value['gfx_index'], value['connector_port'])
        ##
        # Verify and plug the display.
        if len(self.connected_list) >= 2:
            for key, value in self.display_details:
                if len(value) <= 0:
                    gdhm.report_bug(
                        title="[Color][MultiAdapter] Plug and verify display failed due to "
                              "invalid commandline parameters",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("Minimum 1 display is required per adapter")

            for index in range(0, len(self.cmd_line_param)):
                for key, value in self.cmd_line_param[index].items():
                    if cmd_parser.display_key_pattern.match(key) is not None:
                        if value['connector_port'] is not None:
                            display_utility.plug_display(value['connector_port'], self.cmd_line_param[index])
        else:
            gdhm.report_bug(
                title="[Color][MultiAdapter] Plug and verify display failed due to invalid commandline parameters",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Minimum 2 displays are required for the test")

    ##
    # @brief        Get the step value for logging.
    # @return       Step count.
    def getStepInfo(self):
        self.stepCounter = self.stepCounter + 1
        return "STEP-%d: " % self.stepCounter

    def get_display_configuration(self, connected_port_list):
        config = display_config.DisplayConfiguration()
        port_config_str = ""
        for each_port in connected_port_list:
            target_id = config.get_target_id(each_port, self.enumerated_displays)
            mode = config.get_current_mode(target_id)
            port_config_str = port_config_str + "\n" + mode.to_string(self.enumerated_displays)
        return port_config_str

    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Clean Up")
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        for key, value in self.display_details.items():
            for display in value:
                logging.info("Trying to unplug %s", display)
                display_utility.unplug(display, gfx_index=key.lower())
        logging.info("****************TEST ENDS HERE********************************")
