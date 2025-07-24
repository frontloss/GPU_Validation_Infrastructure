########################################################################################################################
# @file         control_api_base.py
# @brief        The script consists of unittest setup and tear down classes for Control Library.
#                   * Parse command line.
#                   * Plug and unplug of displays.
#                   * Apply display configuration.
# @author       Prateek Joshi
########################################################################################################################
import logging
import os
import sys
import time
import json
import unittest

from Libs.Core import cmd_parser, display_utility, enum
from Libs.Core.system_utility import SystemUtility
from Libs.Core.display_power import DisplayPower
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology, CONNECTOR_PORT_TYPE
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus

MAX_LINE_WIDTH = 64
input_csc_file_path = os.path.join(test_context.ROOT_FOLDER, "Tests\\Color\\ApplyCSC\\input_csc_matrix.json")


##
# @brief - Control Library Test Base
class testBase(unittest.TestCase):
    connected_list = []
    is_ddrw = SystemUtility().is_ddrw()
    display_config = DisplayConfiguration()
    machine_info = SystemInfo()
    platform = None
    display_power = DisplayPower()
    custom_tags = [
        # PSR
        "-psr_version",
        # CSC
        "-matrix_info",
        # NN Scaling
        "-hw_modeset",
        # Endurance Gaming
        "-eg_control", "-eg_mode",
        # Async Flips
        "-dx_app", "-async_feature",
        # IGCL
        "-igcl_major_version", "-igcl_minor_version", "-sample_app", "-dll_version", "-uid",
        # DPST
        "-power_plan", "-dpst_feature",
    ]
    power_plan = None
    hw_modeset = False
    display = targetid = None
    enumerated_displays = None
    igcl_major_version = igcl_minor_version = None

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        logging.info(" SETUP: CONTROL_API_BASE ".center(MAX_LINE_WIDTH, "*"))

        self.test_name = sys.argv[0]

        # Parse command line
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags)

        for key, value in self.cmd_line_param.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    self.connected_list.insert(value['index'], value['connector_port'])
                    self.display = value['connector_port']

        # Load the CSC matrix file from file path
        with open(input_csc_file_path) as f:
            csc_info = json.load(f)

        if self.cmd_line_param['MATRIX_INFO'] != 'NONE':
            for index in range(0, len(csc_info)):
                if csc_info[index]['name'] == self.cmd_line_param['MATRIX_INFO'][0]:
                    self.matrix_info = csc_info[index]['matrix']
        else:
            for index in range(0, len(csc_info)):
                if csc_info[index]['name'] == 'IDENTITY_MATRIX':
                    self.matrix_info = csc_info[index]['matrix']

        # Verify and plug the display
        if len(self.connected_list) <= 0:
            logging.error("Minimum 1 display is required to run the test")
            self.fail()
        else:
            self.plugged_display, self.enumerated_displays = display_utility.plug_displays(self, self.cmd_line_param)

        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.connected_list) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.connected_list))

        logging.info('Successfully applied the display configuration as %s %s' %
                     (DisplayConfigTopology(topology).name, self.connected_list))

        self.underrun = UnderRunStatus()

        self.current_config = self.display_config.get_current_display_configuration()

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        logging.info(" TEARDOWN: CONTROL_API_BASE ".center(MAX_LINE_WIDTH, "*"))

        # Unplug the displays and restore the configuration to the initial configuration
        for display in self.plugged_display:
            logging.info("Trying to unplug %s", display)
            display_utility.unplug(display)

        logging.info(" TEST ENDS ".center(MAX_LINE_WIDTH, "*"))


if __name__ == '__main__':
    unittest.main()