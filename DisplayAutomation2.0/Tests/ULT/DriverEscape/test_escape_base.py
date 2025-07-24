#######################################################################################################################
# @file         test_escape_base.py
# @brief        This file contains base class which should be inherited by all driver escape calls ULT test scripts
# @details      This base class file contains DriverEscapeBase class which implements setUpClass class method to
#               verify command-line and initialize the environment required for Driver Escape ULT test cases, and
#               tearDownClass class method to reset the environment by unplugging the displays.
#               Also contains helper methods and variables that are required for the driver escape ULT test cases.
#               Note: Test supports only command-lines with Panel Sink Index passed for all displays
#
# @author       Kiran Kumar Lakshmanan, Chandrakanth Pabolu,
#######################################################################################################################
import logging
import os
import sys
import unittest
from typing import Dict, List

from Libs.Core import cmd_parser, display_utility, enum
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE, DriverType, DisplayConfigTopology
from Libs.Core.display_config.display_config_struct import DisplayConfig
from Libs.Core.logger import html
from Libs.Core.test_env import test_context

MAX_LINE_WIDTH = 64  # Test Log formatting


##
# @brief        DriverEscape ULT Base Class
class DriverEscapeBase(unittest.TestCase):
    display_config_ = display_config.DisplayConfiguration()
    cmd_params: List[Dict[str, any]] = []
    port_list: List[Dict[str, str]] = []
    gfx_index: str = ""
    driver_branch: DriverType = DriverType.UNKNOWN
    config: DisplayConfig
    dp_list: List[str] = []
    hdmi_list: List[str] = []
    panel_dict: Dict[str, Dict[str, str]] = {}

    ##
    # @brief        Setup class method
    # @return       None
    @classmethod
    @html.step("Test SetupClass Phase")
    def setUpClass(cls) -> None:
        logging.info(" SETUP CLASS: Driver Escape ULT ".center(MAX_LINE_WIDTH, "*"))

        cls.custom_tags = cmd_parser.get_custom_tag()
        cls.cmd_params = cmd_parser.parse_cmdline(sys.argv, cls.custom_tags)

        cls.port_list: List[Dict[str, str]] = cmd_parser.get_sorted_display_list(cls.cmd_params)
        logging.info(f"Port List - {cls.port_list}")
        try:
            # Plug and Verify EFPs
            cls.__verify_commandline_args()
            cls.__plug_external_displays()
            cls.__verify_plugged_displays()
        except RuntimeError as err_msg:
            cls.tearDownClass()
            raise Exception(f"Exception occurred - {err_msg}")

        # Todo: If PlatformName not ddrw() -> Skip the test execution
        logging.info(f"Driver Type - {cls.driver_branch} for {cls.gfx_index}")

    ##
    # @brief        Teardown class method
    # @return       None
    @classmethod
    @html.step("Test TearDownClass Phase")
    def tearDownClass(cls) -> None:
        logging.info(" TEARDOWN CLASS: Driver Escape ULT ".center(MAX_LINE_WIDTH, "*"))

        # Unplug EFPs
        cls.__unplug_external_displays()

    ##
    # @brief        Test Setup method
    # @return       None
    def setUp(self) -> None:
        # Display Current Configuration in current test
        self.config = self.display_config_.get_config()
        # Fetch all Displays connected over DP
        self.dp_list = self.get_dp_display_list()
        # Fetch all Displays connected over HDMI
        self.hdmi_list = self.get_hdmi_display_list()

    ##
    # @brief        Helper method to fetch DP port displays from command-line
    # @details      This will fetch displays from gfx_index initialized in the class variable
    # @return       dp_list - List of DP displays
    def get_dp_display_list(self) -> List[str]:
        if bool(self.dp_list):
            return self.dp_list
        for port_element in self.port_list:
            for gfx_index, port in port_element.items():
                # Fetch only DP ports from VBT Panel Index list
                if not ('DP' in port and display_utility.get_vbt_panel_type(port, gfx_index) in
                        [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.PLUS,
                         display_utility.VbtPanelType.DP]):
                    continue
                self.dp_list.append(port)
        return self.dp_list

    ##
    # @brief        Helper method to fetch HDMI port displays from command-line
    # @details      This will fetch displays from gfx_index initialized in the class variable
    # @return       hdmi_list - List of HDMI displays
    def get_hdmi_display_list(self) -> List[str]:
        if bool(self.hdmi_list):
            return self.hdmi_list
        for port_element in self.port_list:
            for gfx_index, port in port_element.items():
                # Fetch only HDMI ports from VBT Panel Index list
                if not ('HDMI' in port and display_utility.get_vbt_panel_type(port, gfx_index) in
                        [display_utility.VbtPanelType.HDMI, display_utility.VbtPanelType.PLUS]):
                    continue
                self.hdmi_list.append(port)
        return self.hdmi_list

    ##
    # @brief        Helper function to apply display config on all plugged displays on specific adapter
    # @param[in]    topology - Display Topology to be applied
    # @return       None
    def apply_display_config_all_displays(self, topology: int):
        display_and_adapter_info_list = []
        for port_element in self.port_list:
            for gfx_index, port in port_element.items():
                display_adapter_info = self.config.get_display_and_adapter_info(gfx_index, port)
                if type(display_adapter_info) is list:
                    display_adapter_info = display_adapter_info[0]
                display_and_adapter_info_list.append(display_adapter_info)
        if not self.display_config_.set_display_configuration_ex(topology, display_and_adapter_info_list):
            logging.error(f"Failed to apply {DisplayConfigTopology(topology).name} Display Configuration")
        else:
            logging.info(f"Successfully applied {DisplayConfigTopology(topology).name} Display Configuration")

    ##
    # @brief        Verification method for displays to be plugged with current command-line
    # @details      Verification will pass if all expected displays are plugged. Raises RuntimeError in case of failure
    # @return       None
    @classmethod
    def __verify_plugged_displays(cls) -> None:
        # Check for EDP and supported panel capabilities for each test set if required
        enum_displays = cls.display_config_.get_enumerated_display_info()
        logging.info(f"Verify Displays | Enumerated Displays : {enum_displays.to_string()}")

        config = cls.display_config_.get_config()
        logging.info(f"Current Configuration: {config.to_string(enum_displays)}")

        cls.driver_branch = config.get_driver_type(cls.gfx_index)
        logging.info(f"Identified Driver Branch: {DriverType(cls.driver_branch).name}")

        temp_display_list = cls.port_list.copy()
        for display_index in range(enum_displays.Count):
            for adapter_dict in temp_display_list:
                [(gfx_index, port)] = adapter_dict.items()
                current_display = enum_displays.ConnectedDisplays[display_index]
                if CONNECTOR_PORT_TYPE(current_display.ConnectorNPortType).name == port and \
                        current_display.DisplayAndAdapterInfo.adapterInfo.gfxIndex == gfx_index:
                    temp_display_list.remove(adapter_dict)

        if len(temp_display_list) > 0:
            raise RuntimeError(f"Displays not verified for plug : {temp_display_list} !!")
        logging.info("Requested displays are plugged properly")

    ##
    # @brief        Helper method to unplug external displays
    # @return       None
    @classmethod
    def __unplug_external_displays(cls) -> None:
        enum_displays = cls.display_config_.get_enumerated_display_info()
        logging.info(f"Unplug Displays | Enumerated Displays : {enum_displays.to_string()}")

        config = cls.display_config_.get_config()
        logging.info(f"Get config data - {config.to_string(enum_displays)}")

        # Switch to enum displays way of removing EFPs instead of cmd_params
        for display_index in range(config.numberOfDisplays):
            current_display = config.displayPathInfo[display_index].displayAndAdapterInfo
            current_port = CONNECTOR_PORT_TYPE(current_display.ConnectorNPortType).name
            current_gfx_index = current_display.adapterInfo.gfxIndex

            # Skip Unplug if VirualDisplay
            if current_port == 'VIRTUALDISPLAY':
                continue

            # Check if panel is LFP
            if display_utility.get_vbt_panel_type(current_port, current_gfx_index) in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                # Skip Unplug if LFP
                continue

            # Check for plugged EFP
            if not display_config.is_display_attached(enum_displays, current_port, current_gfx_index):
                logging.info(f"Display is not attached on port ({current_port}) on ({current_gfx_index})")
                continue

            # Unplug connected display
            unplugged = display_utility.unplug(port=current_port, gfx_index=current_gfx_index)
            logging.info(f"Unplug status of ({current_port}) - {unplugged}")

    ##
    # @brief        Helper method to plug external displays
    # @details      Collects Panel Data from TestStore and Plug the displays in sequence. Raises RuntimeError in case of
    #               failure in any of the steps
    # @return       None
    @classmethod
    def __plug_external_displays(cls) -> None:
        # Call unplug to remove plugged EFPs
        for cmdline_args_dict in cls.cmd_params:
            for key, value in cmdline_args_dict.items():
                if cmd_parser.display_key_pattern.match(key) is None:
                    continue

                if value['panel_index'] is None:
                    logging.warning(f"Expected a Sink Index for port {value['connector_port']}")
                cls.panel_dict[value['connector_port']] = display_utility.get_panel_edid_dpcd_info(
                    value['connector_port'], value['panel_index'], value['is_lfp'])

                if cls.panel_dict[value['connector_port']] is None:
                    raise RuntimeError(f"Invalid panel index found: {cls.panel_dict[value['connector_port']]}")
                intermediate_folder = None

                if 'HDMI' in value['connector_port']:
                    if os.path.exists(os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'HDMI',
                                                   cls.panel_dict[value['connector_port']]['edid'])):
                        intermediate_folder = 'HDMI'
                elif 'DP' in value['connector_port']:
                    if os.path.exists(os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'eDP_DPSST',
                                                   cls.panel_dict[value['connector_port']]['edid'])):
                        intermediate_folder = 'eDP_DPSST'
                    elif os.path.exists(os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'DP_MST_TILE',
                                                     cls.panel_dict[value['connector_port']]['edid'])):
                        intermediate_folder = 'DP_MST_TILE'
                    else:
                        raise RuntimeError(
                            f"EDID file {cls.panel_dict[value['connector_port']]['edid']} given for "
                            f"{value['connector_port']} doesn't exist in [eDP_DPSST, DP_MST_TILE] directories")

                if intermediate_folder is None:
                    raise RuntimeError(f"Failed to identify EDID folder path for port {value['connector_port']}")

                cls.panel_dict[value['connector_port']]['edid'] = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER,
                                                                               intermediate_folder,
                                                                               cls.panel_dict[value['connector_port']][
                                                                                   'edid'])
                assert os.path.exists(cls.panel_dict[value['connector_port']]['edid'])
                if 'HDMI' in value['connector_port']:
                    cls.panel_dict[value['connector_port']]['dpcd'] = None
                elif 'DP' in value['connector_port']:
                    cls.panel_dict[value['connector_port']]['dpcd'] = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER,
                                                                                   intermediate_folder, cls.panel_dict[
                                                                                       value['connector_port']]['dpcd'])
                else:
                    raise RuntimeError(f"Failed to identify DPCD folder path for port {value['connector_port']}")

                if value["is_lfp"] is True:  # Skip Plug if LFP
                    continue
                if display_utility.plug(port=value['connector_port'], edid=value['edid_name'], dpcd=value['dpcd_name'],
                                        panelindex=value['panel_index'], gfx_index=value['gfx_index'].lower()) is False:
                    raise RuntimeError(f"Failed to plug {value['connector_port']} on {value['gfx_index'].lower()}")
                logging.info(f"Plugged {value['connector_port']} on {value['gfx_index'].lower()}")
        logging.info(f"Panel dict - {cls.panel_dict}")

    ##
    # @brief        Verification method to Validate current command-line
    # @details      Verification will pass only if one gfx_index is present. Raises RuntimeError in case of failure
    # @return       None
    @classmethod
    def __verify_commandline_args(cls) -> None:
        gfx_index = []
        if not all(isinstance(port_dict, dict) for port_dict in cls.port_list):
            raise RuntimeError("Invalid commandline. Please run the test with gfx_index (-gfx_0/-gfx_1) in args.")
        for port_dict in cls.port_list:
            for index, port_name in port_dict.items():
                if index not in gfx_index:
                    gfx_index.append(index)

        if len(gfx_index) != 1:
            raise RuntimeError("Invalid commandline. Please run the test with one gfx_index (-gfx_0/-gfx_1) in args.")

        cls.gfx_index = gfx_index[0].lower()
        logging.info(f"Identified gfx_index as {cls.gfx_index}")

    ##
    # @brief        Get EDID data from bin file
    # @param[in]    path - Absolute path for required bin file
    # @return       (bin_file_exists, bin_data) - (True if file exists in path False otherwise, bin file data as List)
    @staticmethod
    def get_edid_data_from_file(path) -> (bool, List[int]):
        bin_file_exists = True
        bin_data = []
        logging.debug(f"Trying to get EDID from file path - {path}")
        try:
            with open(path.encode(), 'rb') as fp:
                data = fp.read()
                for index in range(len(data)):
                    bin_data.append(data[index])
        except FileNotFoundError:
            bin_file_exists = False
            logging.error(f"Bin File doesn't exists - {path}")
        return bin_file_exists, bin_data
