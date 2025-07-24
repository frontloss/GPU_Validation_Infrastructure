#######################################################################################################################
# @file         dp_mst_manual_base.py
# @brief        This file contains MST Manual test base class which should be inherited by all MST related tests.
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import re
import sys
import unittest

from Libs.Core import cmd_parser
from Libs.Core import display_utility
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import DisplayConfig
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus
from Libs.manual.modules import alert
from Tests.Display_Port.ManualTests.dp_ui_constants import UIStringConstants

# List of Supported Ports
supported_ports = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

# Regular expressions to parse keys in the Output dictionary
# E.g.: DP_C, DP_B, etc
dp_pattern = re.compile('DP_' + (r'(?:%s)\b' % '|'.join(supported_ports)))

##
# @brief    Base class
class DisplayPortMSTManualBase(unittest.TestCase):

    ##
    # @brief        This method initialises the object and process the cmd line parameters.
    # @return       None
    def setUp(self):
        logging.info("Initializing the DisplayPortMSTManualBase")

        ##
        # Contains supported configurations.
        self.SUPPORTED_CONFIG_LIST = ['SINGLE', 'CLONE', 'EXTENDED']

        ##
        # Creating object necessary to access function required from different
        # module.
        self.display_configuration = DisplayConfiguration()
        self.display_port = DisplayPort()
        self.under_run_status = UnderRunStatus()

        ##
        # Initializing the command line argument
        self.cmd_line_dict = None

        ##
        # Defining the custom tags that will be used as part of the dp mst
        # command lines.
        self.mst_custom_tags = ['-DEPTH', '-ALL_PORTS', '-DISPLAY1', '-DISPLAY2', '-DISPLAY3', '-DISPLAY4']

        ##
        # Holds the number of displays to be plugged, defaults to 3.
        self.max_depth = 3

        ##
        # Holds the data about whether the test has to run on all available
        # ports, defaults to True.
        self.is_executed_on_all_ports = True

        ##
        # Holds the data about dp supported ports which are free.
        self.supported_dp_port_list = []
        self.type_c_ports = []
        self.native_dp_ports = []

        ##
        # Holds the port type passed in the command line.
        self.dp_port_list = []

        ##
        # Holds the data about which configuration to be applied.
        self.display_config = None

        ##
        # Set dp supported ports.
        self.set_dp_supported_ports()

        ##
        # Process the command line arguments.
        self.process_cmdline()

        ##
        # Current port type.
        self.port_type = ""

        ##
        # MST need 2 or more displays.
        if self.max_depth < 2 or self.max_depth > 3:
            logging.error("[Test Issue]: MST topology cannot be constructed using %s displays", self.max_depth)
            self.fail()

        ##
        # Prompt the user with General instructions to be followed while
        # executing the test.
        alert.info(UIStringConstants.GENERAL_INSTRUCTION)

    ##
    # @brief        Prompts the user to build the MST topology on the specified port.
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @return       None
    def build_mst_topology(self, port_type):
        logging.info("Building MST topology on {0}".format(self.port_type))
        alert.warning(UIStringConstants.UNPLUG_ALL_DISPLAYS)
        self.port_type = port_type
        enumerated_displays = self.display_configuration.get_enumerated_display_info()

        if enumerated_displays.Count <= 1:
            ##
            # Prompting to plug displays at depth 1.
            is_display_plugged = False
            panel_type = self.cmd_line_dict['DISPLAY2']
            while is_display_plugged is False:
                alert.info(UIStringConstants.BUILD_MST_TOPOLOGY_STEP_ONE.format(panel_type, self.port_type))
                is_display_plugged = self.is_display_plugged(panel_type=panel_type)
                if is_display_plugged is False:
                    to_retry = alert.warning(
                        UIStringConstants.PLUG_FAILURE.format(panel_type), alert_type=alert.AlertTypes.confirm)
                    if to_retry is False:
                        logging.error("Failed to plug {0} panel".format(panel_type))
                        self.fail()

            ##
            # Prompting to plug displays at depth 2.
            is_display_plugged = False
            panel_type = self.cmd_line_dict['DISPLAY3']
            while is_display_plugged is False:
                alert.info(UIStringConstants.BUILD_MST_TOPOLOGY_STEP_TWO.format(panel_type))
                is_display_plugged = self.is_display_plugged(panel_type=panel_type, depth=2)
                if is_display_plugged is False:
                    to_retry = alert.warning(
                        UIStringConstants.PLUG_FAILURE.format(panel_type), alert_type=alert.AlertTypes.confirm)
                    if to_retry is False:
                        logging.error("Failed to plug {0} panel".format(panel_type))
                        self.fail()

            ##
            # Prompting to plug displays at depth 3.
            if self.max_depth == 3:
                is_display_plugged = False
                panel_type = self.cmd_line_dict['DISPLAY4']
                while is_display_plugged is False:
                    alert.info(UIStringConstants.BUILD_MST_TOPOLOGY_STEP_THREE.format(panel_type))
                    is_display_plugged = self.is_display_plugged(panel_type=panel_type, depth=3)
                    if is_display_plugged is False:
                        to_retry = alert.warning(
                            UIStringConstants.PLUG_FAILURE.format(panel_type), alert_type=alert.AlertTypes.confirm)
                        if to_retry is False:
                            logging.error("Failed to plug {0} panel".format(panel_type))
                            self.fail()
        else:
            logging.error(
                "Displays are already Hot plugged. Remove all external displays before executing the test.Exiting...")
            self.fail()

        ##
        # Check CUI to confirm the plugged display
        user_response = alert.confirm("Are all panels got enumerated in CUI?")
        if user_response is False:
            logging.error("Failed to build DP MST topology on port {0}".format(self.port_type))
            self.fail()

        user_response = alert.confirm("Is display anomaly observed?")
        if user_response is True:
            observation = alert.radio(
                "Display Anomalies", ["Flickering", "Corruption", "Display blankout", "Other anomalies"])
            logging.error(
                "[Driver Issue]: Display anomaly: {0} is observed after building DP MST topology on {1}".format(
                    observation, self.port_type))
            self.fail()
        else:
            logging.info("DP MST topology has been built successfully on port {0}".format(self.port_type))

    ##
    # @brief        Checks whether display is plugged at the given depth.
    # @param[in]    panel_type: str
    #                   contains panel type Ex: Display DP 1.2 (Depth 1)
    # @param[in]    depth: int
    #                   contains depth at which display is plugged
    # @return       Bool
    def is_display_plugged(self, panel_type, depth=1):
        enumerated_displays = self.display_configuration.get_enumerated_display_info()
        display_list = [display for display in enumerated_displays.ConnectedDisplays
                        if CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name.lower() == self.port_type.lower()]
        if len(display_list) == depth:
            logging.info(
                "{0} panel has been successfully plugged on {1} at depth {2}".format(panel_type, self.port_type, depth))
            return True
        else:
            logging.info("{0} panel is not plugged on {1} at depth {2}".format(panel_type, self.port_type, depth))
            return False

    ##
    # @brief        Apply the display configuration and verify the applied configuration with current config
    # @param[in]    topology: str
    #                   contains config topology Ex:'SINGLE', 'CLONE'
    # @param[in]    current_configuration_list: list
    #                   list containing displays enabled in current config.
    # @param[in]    set_mode: Bool
    #                   True or False based on whether mode set is needed by caller
    # @return       None
    def apply_display_config_and_verify(self, topology, current_configuration_list, set_mode=True):
        set_config = DisplayConfig()
        set_config.topology = eval('enum.%s' % topology)
        enumerated_displays = self.display_configuration.get_enumerated_display_info()

        ##
        # Iterate through all possible config 
        # Apply the config and do a setmode for each config.
        for target_id_list in current_configuration_list:
            depth = 0
            for target_id in target_id_list:
                set_config.displayPathInfo[depth].targetId = target_id
                depth += 1
            set_config.numberOfDisplays = depth
            logging.info(
                "Trying to Apply Display Configuration as : {0}".format(set_config.to_string(enumerated_displays)))
            self.display_configuration.set_display_configuration(set_config)
            if self.verify_applied_config(set_config) is True:
                user_response = alert.confirm("Is display anomaly observed?")
                if user_response is True:
                    observation = alert.radio(
                        "Display Anomalies", ["Flickering", "Corruption", "Display blankout", "Other anomalies"])
                    logging.error(
                        "[Driver Issue]: Display anomaly: {0} observed after applying display configuration...Exiting...".format(
                            observation))
                    self.fail()
            else:
                self.fail()
            if set_mode is True:
                self.set_modes()

    ##
    # @brief        Verify applied config
    # @param[in]    set_config: obj
    #                   set_config struct
    # @return       Bool
    def verify_applied_config(self, set_config):
        enumerated_displays = self.display_configuration.get_enumerated_display_info()
        current_config = self.display_configuration.get_current_display_configuration()
        logging.info("Current display configuration: {0}".format(current_config.to_string(enumerated_displays)))

        ##
        # Check current configuration with the set configuration.
        if current_config.equals(set_config):
            logging.info("Successfully applied display configuration.")
            return True
        else:
            logging.error("Failed to apply display configuration..Exiting..")
            return False

    ##
    # @brief        Apply mode
    # @return       None
    def set_modes(self):
        config = self.display_configuration.get_current_display_configuration()
        target_id_list = []

        if self.display_config == "CLONE":
            target_id_list.append(config.displayPathInfo[0].targetId)
        else:
            for index in range(config.numberOfDisplays):
                target_id_list.append(config.displayPathInfo[index].targetId)

        supported_modes_dict = self.display_configuration.get_all_supported_modes(target_id_list)
        for target_id, supported_mode_list in supported_modes_dict.items():
            ##
            # Get min, max and mid mode from the supported mode list.
            min_mode = supported_mode_list[0]
            mid_mode = supported_mode_list[(len(supported_mode_list) / 2) + 1]
            max_mode = supported_mode_list[-1]

            ##
            # Apply min, max and mid mode.
            self.set_modes_helper([[min_mode], [mid_mode], [max_mode]], target_id=target_id)

    ##
    # @brief        Applies and verifies the applied mode.
    # @param[in]    mode_list: list
    #                   List of modes that has to be applied.
    # @param[in]    target_id: unsigned int
    #                   Target ID for which mode set is required.
    # @return       None
    def set_modes_helper(self, mode_list, target_id):
        enumerated_displays = self.display_configuration.get_enumerated_display_info()
        for mode in mode_list:
            modes_flag = self.display_configuration.set_display_mode(mode)
            if modes_flag is False:
                logging.error("Failed to apply display mode for the current configuration. Exiting ...")
                self.fail()

            ##
            # Check for under_run
            if self.under_run_status.verify_underrun() is True:
                logging.error("[Driver Issue]: Under run observed")

            ##
            # User Verification for display anomaly after each ModeSet
            user_response = alert.confirm("Is display anomaly observed?")
            if user_response is True:
                observation = alert.radio(
                    "Display Anomalies", ["Flickering", "Corruption", "Display blankout", "Other anomalies"])
                logging.error("[Driver Issue]: Display anomaly: {0} after ModeSet with resolution {1}".format(
                    observation, mode.to_string(enumerated_displays, False)))
                self.fail()

    ##
    # @brief        Get the configurations possible for displays connected
    # @return       configuration_list: list
    #                   list of possible configurations
    def get_possible_configurations(self):
        ##
        # Get the enumerated displays from DisplayConfiguration
        target_id_list = []
        enumerated_displays = self.display_configuration.get_enumerated_display_info()
        if enumerated_displays.Count >= 1:
            for index in range(enumerated_displays.Count):
                target_id = enumerated_displays.ConnectedDisplays[index].TargetID
                target_id_list.append(target_id)
            configuration_list = display_utility.get_possible_configs(target_id_list, True)
        return configuration_list

    ##
    # @brief        Set the dp supported port list.
    # @return       None
    def set_dp_supported_ports(self):

        logging.info("Getting supported dp ports")

        ##
        # Holds data for the list of all free ports based on VBT settings.
        port_details = display_config.get_supported_ports()

        ##
        # Filtering out the display ports from the free port list.
        for port in port_details.keys():
            if port_details[port] == 'TC':
                self.type_c_ports.append(port)
            if port.startswith('DP_') and port_details[port] == 'NATIVE':
                self.native_dp_ports.append(port)

        ##
        # Remove DP_A from the list since it's an internal display.
        if 'DP_A' in self.native_dp_ports:
            self.native_dp_ports.remove('DP_A')

        self.supported_dp_port_list = self.native_dp_ports + self.type_c_ports

        ##
        # Fail the test case if no dp ports are available.
        if len(self.supported_dp_port_list) < 1:
            logging.info("[Test Issue]: Not enough free ports available..Exiting..")
            self.fail()

    ##
    # @brief        Processing the command line and extracting the required arguments.
    # @return       None
    def process_cmdline(self):
        logging.info("Parsing the command line arguments")
        self.cmd_line_dict = cmd_parser.parse_cmdline(sys.argv, self.mst_custom_tags)
        self.display_config = self.cmd_line_dict['CONFIG']
        for key, value in self.cmd_line_dict.items():
            if dp_pattern.match(key) is not None and value['connector_port'] is not None:
                if value['connector_port'].startswith('DP_A') or \
                        not value['connector_port'] in self.supported_dp_port_list:
                    logging.info("%s is not supported..Exiting..", value['connector_port'])
                    self.fail()
                if not self.dp_port_list.__contains__(value['connector_port']):
                    self.dp_port_list.append(value['connector_port'])
        try:
            ##
            # Getting the integer value from the command line argument -DEPTH.
            if self.cmd_line_dict['DEPTH'] is not None:
                self.max_depth = int(self.cmd_line_dict['DEPTH'][0])
                if not (2 <= self.max_depth <= 3):
                    logging.error("[Test Issue]: MAX depth should be 2 or 3")
                    self.fail()
            ##
            # Getting the boolean value from the command line argument -
            # ALL_PORTS.
            if self.cmd_line_dict['ALL_PORTS'] is not None:
                self.is_executed_on_all_ports = bool(self.cmd_line_dict['ALL_PORTS'][0])
            if self.is_executed_on_all_ports is False and self.dp_port_list is None:
                logging.error(
                    "Ports not present in command line..But All ports is passed as False..Invalid command line..")
                self.fail()
        except ValueError:
            logging.error("Invalid argument passed in command line")
            self.fail()

    ##
    # @brief        Get dp ports on which the MST topology is to build as per XML.
    # @return       port_list: list
    #                   list of ports requested in the command line
    def get_dp_port_list(self):
        port_list = []
        if self.is_executed_on_all_ports is True:
            if 'USB-C' in self.cmd_line_dict['DISPLAY2']:
                port_list = self.type_c_ports
            else:
                port_list = self.native_dp_ports
        elif len(self.dp_port_list) != 0:
            port_list = self.dp_port_list
        else:
            logging.info("Port type is not specified in the command line..Exiting..")
            self.fail()
        if len(port_list) == 0:
            logging.info("Not enough free ports available..Exiting..")
            self.fail()
        return port_list

    ##
    # @brief        Verify under run
    # @return       None
    def verify_underrun(self):
        under_run_status = UnderRunStatus()
        if under_run_status.verify_underrun() is True:
            self.fail()

    ##
    # @brief        Verify test result
    # @param[in]    msg: str
    #                   Failure message.
    # @return       Bool
    def fail(self, msg=None):
        alert.fail(UIStringConstants.GENERAL_FAILURE_MESSAGE)
        return super(DisplayPortMSTManualBase, self).fail(msg)
