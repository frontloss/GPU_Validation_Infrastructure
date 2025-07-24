#######################################################################################################################
# @file         vdsc_base.py
# @brief        This file contains VDSC base class which should be inherited by all VDSC related tests.
# @details      vdsc_base.py contains VdscBase class which implements setUpClass class method to setup the environment
#               required for all the VDSC test cases and tearDownClass class method to reset the environment by
#               unplugging the displays, un-initialize sdk, resetting any registry values etc
#               Also contains some helper methods and variables that are required for the VDSC test cases.
#
# @author       Bhargav Adigarla, Praburaj Krishnan
#######################################################################################################################
import copy
import ctypes
import logging
import sys
import time
import unittest
from dataclasses import dataclass
from operator import attrgetter
from typing import List, Dict, Any, Tuple, Optional

from Libs.Core.wrapper.control_api_args import ctl_display_timing_t, ctl_genlock_target_mode_list_t
from Libs.Core import cmd_parser, display_utility, enum
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_power import DisplayPower
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Core.system_utility import SystemUtility
from Libs.Core.test_env import test_context
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ModeEnumXMLParser
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Tests.Display_Port.DP_MST.dp_mst_parser import DPCommandParser
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import common
from Libs.Core.display_config.display_config_struct import SamplingMode


##
# @brief        A data class which holds information about the topology to be applied and port list on which the
#               topology must be applied.
@dataclass
class ConfigData:
    topology: enum
    port_list: List


##
# @brief        A class which has to be inherited by all the VDSC test cases and contains some class methods, test
#               methods to set the environment required for the VDSC test case to run and also contains helper methods
#               which is used across VDSC test cases.
class VdscBase(unittest.TestCase):
    topology = None
    dp_mode_enum_xml_path = "Tests\\VDSC\\dp_dsc_xml\\"
    hdmi_mode_enum_xml_path = "Tests\\VDSC\\hdmi_dsc_xml\\"
    cmd_line_param: List[Dict[str, Any]] = [{}]
    cmd_line_adapters: Dict = {}
    edp_panels = []
    mipi_panels = []
    lfp_panels = []
    target_ids = {}
    _system_utility = SystemUtility()
    _display_config = DisplayConfiguration()
    _display_power = DisplayPower()
    external_panels = []
    vdsc_panels: List[Dict[str, str]] = []
    non_vdsc_panels: List[Dict[str, str]] = []
    edp_vdsc_panels = []
    mipi_vdsc_panels = []
    vdsc_target_ids = {}
    mode_enum_parser_dict: Dict[str, ModeEnumXMLParser] = {}
    is_pre_si_environment = False
    cmd_line_displays: List[Dict] = []
    display_port = DisplayPort()
    system_info = SystemInfo()
    mst_port_name_list = []
    sst_tiled_port_name_list: List[Tuple] = []

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any VDSC test case. Helps to initialize some of the
    #               parameters required for VDSC the test execution.
    # @return       None
    @classmethod
    def setUpClass(cls) -> None:
        logging.info(" SETUP: VDSC_BASE ".center(common.MAX_LINE_WIDTH, "*"))

        execution_environment = VdscBase._system_utility.get_execution_environment_type()
        VdscBase.is_pre_si_environment = True if execution_environment in ["SIMENV_FULSIM", "SIMENV_PIPE2D"] else False

        vdsc_custom_tags = ['-XML', '-PLUG_TOPOLOGIES', '-NON_VDSC', '-REG_KEY_VALUE']

        VdscBase.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS + vdsc_custom_tags)

        # In single adapter case cmd_line_param will be a single dictionary, else it will be list of dictionaries one
        # for each of the 4 adapters.And get_sorted_display_list() returns list of ports ['DP_F','DP_G'] in SA case and
        # in MA case a list of dictionaries of single item containing gfx_index and port name as key value pair
        # respectively.E.g [{'gfx_1': 'DP_F'}, {'gfx_1': 'DP_G'}, {'gfx_0': 'DP_C'}]. To have unified structure for both
        # SA and MA case it is converted to list, if its not already one.
        if type(VdscBase.cmd_line_param) is not list:
            VdscBase.cmd_line_param = [VdscBase.cmd_line_param]
        logging.info(f"Cmd Line Params: {VdscBase.cmd_line_param}")

        VdscBase.topology = eval("enum.%s" % VdscBase.get_cmd_line_param_values('CONFIG'))

        # get_sorted_display_list() will now always return a list of dictionaries for both SA and MA case
        # E.g [{'gfx_1': 'DP_F'}, {'gfx_1': 'DP_G'}, {'gfx_0': 'DP_C'}]
        VdscBase.cmd_line_displays = cmd_parser.get_sorted_display_list(VdscBase.cmd_line_param)
        logging.info(f"Cmd Line Displays: {VdscBase.cmd_line_displays}")

        # Details of Distinct adapters present in the system
        VdscBase.cmd_line_adapters = test_context.TestContext.get_gfx_adapter_details()

    ##
    # @brief        This test method acts as wrapper that invokes command line handler based on the arguments.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_handle_vdsc_command_line(self) -> None:
        if self.get_cmd_line_param_values('XML') != 'NONE':
            self._handle_mode_enum_cmd()
        elif self.get_cmd_line_param_values('PLUG_TOPOLOGIES') != 'NONE':
            self._handle_mst_and_tiled_dsc_cmd()
        else:
            self._handle_other_dsc_cmd()

        common.print_current_topology()

    ##
    # @brief    This test method helps to identify the EDP, MIPI, DP, HDMI VDSC panels and Non VDSC panels
    # @return   None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_01_update_panel_info(self) -> None:
        enumerated_displays = VdscBase._display_config.get_enumerated_display_info()
        self.assertIsNotNone(enumerated_displays, "[Test Issue] - API get_enumerated_display_info() FAILED")

        for adapter_display_dict in VdscBase.cmd_line_displays:
            # Each dictionary inside vdsc_panel list will be of length 1, hence iterating over it is not needed
            [(gfx_index, port)] = adapter_display_dict.items()

            # Check if the Current Port is the Slave Port of SST Tiled Display. If So Skip further Processing on the
            # Port as for SST Tiled Display all Operations Should be Performed on the Master Port only.
            if len([tiled_ports for tiled_ports in VdscBase.sst_tiled_port_name_list if port in tiled_ports[1]]) == 1:
                continue

            display_adapter_info_list = VdscBase._display_config.get_display_and_adapter_info_ex(port, gfx_index)
            if type(display_adapter_info_list) is not list:
                display_adapter_info_list = [display_adapter_info_list]

            for display_adapter_info in display_adapter_info_list:
                is_success = VdscBase._display_config.set_display_configuration_ex(enum.SINGLE, [display_adapter_info])
                self.assertTrue(is_success, "[Driver Issue] - Failed to apply display configuration")

                target_id = VdscBase._display_config.get_target_id(port, enumerated_displays)
                self.assertNotEqual(target_id, 0, "[Test Issue] - Target ID for {0} is 0 ".format(port))

                # update all panel info about vdsc/non-vdsc edp, mipi and external panels and target_id
                VdscBase.target_ids[port] = target_id

                if display_utility.get_vbt_panel_type(port, gfx_index) == display_utility.VbtPanelType.LFP_DP:
                    VdscBase.edp_panels.append({gfx_index: port})
                    VdscBase.update_vdsc_panel_target_info(gfx_index, port, target_id, panel_filter="EDP")

                elif display_utility.get_vbt_panel_type(port, gfx_index) == display_utility.VbtPanelType.LFP_MIPI:
                    VdscBase.mipi_panels.append({gfx_index: port})
                    VdscBase.update_vdsc_panel_target_info(gfx_index, port, target_id, panel_filter="MIPI")

                else:
                    VdscBase.external_panels.append({gfx_index: port})
                    VdscBase.update_vdsc_panel_target_info(gfx_index, port, target_id)

        VdscBase.lfp_panels = VdscBase.edp_panels + VdscBase.mipi_panels

        logging.info('VDSC Supported Panels: {}'.format(VdscBase.vdsc_target_ids))
        logging.info('Non VDSC Panels: {}'.format(VdscBase.non_vdsc_panels))

    ##
    # @brief        This test method disable PSR functionality only if Panel supports both PSR2 + VDSC and for Pre-Gen13
    #               platforms as PSR2 + VDSC can co-exist from Gen13 onwards(except DG2). Applicable for VDSC EDP
    #               displays that supports PSR2. For other VDSC displays and Gen13+ platforms(other than DG2) it will
    #               be skipped
    # @return       None.
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_02_enable_edp_vdsc(self) -> None:

        # Enable DSC explicitly Only if EDP DSC panel is connected.
        # Enabling the feature in INF
        if len(self.edp_vdsc_panels) > 0:
            is_success = self.__enable_disable_edp_vdsc(to_enable_vdsc=True)
            self.assertTrue(is_success, "Failed in enable eDP VDSC in driver")
            # Gdhm bug reporting handled in enable_disable_psr2

            logging.info("eDP VDSC enabled in driver using INF(PSR2Disable)")

    ##
    # @brief        This test method disables edp vdsc by enabling back the PSR2 functionality which got disabled in
    #               t_02_enable_edp_vdsc(), for Pre-Gen13 + DG2 platforms
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_20_disable_edp_vdsc(self) -> None:
        # Disable DSC explicitly Only if EDP DSC panel is connected.
        # Disabling the feature in INF
        if len(self.edp_vdsc_panels) > 0:
            is_success = self.__enable_disable_edp_vdsc(to_enable_vdsc=False)
            self.assertTrue(is_success, "Failed to disable eDP VDSC in driver")
            # Gdhm bug reporting handled in enable_disable_psr2

            logging.info("eDP VDSC disabled in driver using INF(PSR2Disable)")

    ##
    # @brief        This private method enables or disables vdsc based on the boolean value passed to parameter
    #               to_enable_vdsc. VDSC + PSR2 cannot co-exist for pre-gen13 + DG2 platforms. So to enable vdsc, we
    #               need to disable PSR2 and vice-versa
    # @param[in]    to_enable_vdsc: bool
    #                    True represents enable vdsc feature, False represents disable vdsc feature
    # @return       is_success: bool
    #                    Returns True if enable/disable of psr2 to disable/enable vdsc is successful, False otherwise
    def __enable_disable_edp_vdsc(self, to_enable_vdsc: bool) -> bool:
        is_success = True
        gfx_index_list = []

        for adapter_display_dict in VdscBase.edp_vdsc_panels:
            # Each dictionary inside edp_vdsc_panel list will be of length 1, hence iterating dict is not needed
            [(gfx_index, port)] = adapter_display_dict.items()

            display_adapter_info = VdscBase._display_config.get_display_and_adapter_info_ex(port, gfx_index)

            # making display active before checking psr2 support
            # TODO: Once SINK_EDP081 tests are enabled inplace of SINK_EDP010 tests, psr2 check can be ignored
            # TODO: Jira link : https://jira.devtools.intel.com/browse/VSDI-22826
            return_status = VdscBase._display_config.set_display_configuration_ex(enum.SINGLE, [display_adapter_info])
            self.assertTrue(return_status, "[Driver Issue] - Failed to apply display configuration")

            # get platform name ad panel target_id
            adapter_info = VdscBase.cmd_line_adapters[gfx_index]
            self.platform = adapter_info.get_platform_info().PlatformName.upper()
            panel_target_id = VdscBase.vdsc_target_ids[port]

            # this API helps to know if PSR2 is supported by the panel or not
            is_psr2_supported_by_panel = psr.is_feature_supported_in_panel(panel_target_id,
                                                                           psr.UserRequestedFeature.PSR_2)

            # Get the adapter_index only for pre-gen13 + DG2 platforms and only if panels on them support PSR
            if self.platform in (common.PRE_GEN_13_PLATFORMS + ['DG2']) and is_psr2_supported_by_panel:
                gfx_index_list.append(gfx_index)

        # disable psr2 to enable dsc or enable psr2 to disable dsc for adapters whose platform belongs to Pre-Gen13 as
        # psr2 + vdsc can co-exist from Gen13 onwards(except DG2) and if edp dsc panel on them supports psr2
        for gfx_index in set(gfx_index_list):
            is_success = is_success & DSCHelper.enable_disable_psr2(gfx_index, not to_enable_vdsc)

        return is_success

    ##
    # @brief        Class Method to Get the Display Config and Port List Based on the No of DSC Panel Plugged.
    # @return       config_data: ConfigData
    #                   Returns the Display Config and Port List on Which the Config has to Applied.
    @classmethod
    def get_config_to_apply(cls) -> Tuple[bool, ConfigData]:
        is_success: bool = True
        if len(VdscBase.vdsc_panels) == 1:
            vdsc_port_list = list(VdscBase.vdsc_panels[0].values())
            config_data = ConfigData(enum.SINGLE, vdsc_port_list)

        elif 2 <= len(VdscBase.vdsc_panels) <= 4:
            vdsc_port_list = [port for adapter_display_dict in VdscBase.vdsc_panels
                              for gfx_index, port in adapter_display_dict.items()]
            config_data = ConfigData(enum.EXTENDED, vdsc_port_list)

        else:
            config_data = None
            is_success = False

        return is_success, config_data

    ##
    # @brief        Private method which handles VDSC mode enumeration command lines, initializes the mode enumeration
    #               xml parser and plugs the display with the help of the parsed data from the xml.
    # @return       None
    def _handle_mode_enum_cmd(self) -> None:
        is_success = True
        lfp_panel_type_list = [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]

        xml_file_list: List[str] = self.get_cmd_line_param_values('XML')
        self.assertEqual(len(xml_file_list), len(VdscBase.cmd_line_displays), "[Test Issue] - Invalid command line.")

        for adapter_display_dict, xml_file_name in zip(VdscBase.cmd_line_displays, xml_file_list):
            [(gfx_index, port)] = adapter_display_dict.items()
            xml_file_path = ""
            if "DP" in port.upper():
                xml_file_path = VdscBase.dp_mode_enum_xml_path + xml_file_name.lower()
            elif "HDMI" in port.upper():
                xml_file_path = VdscBase.hdmi_mode_enum_xml_path + xml_file_name.lower()
            else:
                self.assertTrue(False, "[Test Issue] - Invalid command line")

            xml_parser = ModeEnumXMLParser(gfx_index, port, xml_file_path)
            panel_type = display_utility.get_vbt_panel_type(port, gfx_index)
            if panel_type not in lfp_panel_type_list:
                if xml_parser.mst_topology_path is not None:
                    display_tech, mst_topology_path = xml_parser.display_tech, xml_parser.mst_topology_path
                    self._plug_mst_or_tiled_display(gfx_index, port, display_tech, mst_topology_path, False)
                    if display_tech == 'MST':
                        VdscBase.mst_port_name_list.append(port)
                else:
                    edid, dpcd = xml_parser.edid_file, xml_parser.dpcd_file
                    is_success = display_utility.plug(port=port, edid=edid, dpcd=dpcd, gfx_index=gfx_index)
                self.assertTrue(is_success, "Failed to Plug Display at {}".format(port))
            xml_parser.parse_and_construct_mode_tables()
            VdscBase.mode_enum_parser_dict[port] = xml_parser

    ##
    # @brief        Private method which handles MST VDSC command lines. Creates DP command parser object which helps
    #               to parse the command line and plug the display based on the data obtained from it.
    # @return       None
    def _handle_mst_and_tiled_dsc_cmd(self) -> None:
        dp_mst_command_parser = DPCommandParser()
        requested_topology_info_dict = dp_mst_command_parser.requested_topology_info_dict
        port_name_list = dp_mst_command_parser.requested_dp_port_list

        index = 0
        while index < len(port_name_list):
            port_name = port_name_list[index]

            xml_file_name = requested_topology_info_dict[index].path
            logging.info("XML File Name: {}".format(xml_file_name))

            topology_type = requested_topology_info_dict[index].display_tech
            logging.info("Topology Type: {}".format(topology_type))

            self._plug_mst_or_tiled_display('gfx_0', port_name, topology_type, xml_file_name, is_low_power=False)

            if topology_type == 'MST':
                VdscBase.mst_port_name_list.append(port_name)
            elif topology_type == 'SST':
                s_port_name = port_name_list[index + 1]
                s_xml_file_name = requested_topology_info_dict[index + 1].path
                logging.info("Slave XML File Name: {}".format(s_xml_file_name))

                s_topology_type = requested_topology_info_dict[index + 1].display_tech
                logging.info("Slave Topology Type: {}".format(s_topology_type))

                VdscBase.sst_tiled_port_name_list.append((port_name, s_port_name))
                self._plug_mst_or_tiled_display('gfx_0', s_port_name, s_topology_type, s_xml_file_name, False)
                index = index + 1

            index = index + 1

    ##
    # @brief        Private method which handles command lines that can either have panel index or edid dpcd values and
    #               plugs the display accordingly.
    # @return       None
    def _handle_other_dsc_cmd(self) -> None:

        for adapter_display_dict in VdscBase.cmd_line_displays:
            [(gfx_index, port)] = adapter_display_dict.items()

            # Perform plug operation only for non lfp panels
            if display_utility.get_vbt_panel_type(port, gfx_index) not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                panel_index = self.get_cmd_line_param_values('panel_index', gfx_index, port)
                port_type = self.get_cmd_line_param_values('connector_port_type', gfx_index, port)

                # A panel will either have a panel_index or edid, dpcd values.Plug them accordingly
                if panel_index is not None:
                    is_success = display_utility.plug(port=port, port_type=port_type, panelindex=panel_index,
                                                      gfx_index=gfx_index)
                    self.assertTrue(is_success, "Failed to Plug Display at {} on {}".format(port, gfx_index))
                else:
                    edid_val = self.get_cmd_line_param_values('edid_name', gfx_index, port)
                    dpcd_val = self.get_cmd_line_param_values('dpcd_name', gfx_index, port)

                    is_success = display_utility.plug(port=port, edid=edid_val, dpcd=dpcd_val, port_type=port_type,
                                                      gfx_index=gfx_index)
                    self.assertTrue(is_success, "Failed to Plug Display at {} on {}".format(port, gfx_index))

    ##
    # @brief        This method fetches the value of field requested, from cmd_line_param which is list of dictionaries,
    #               one for each adapter mentioned in command line. All non port specific fields will have same key
    #               value pair across all adapter dictionaries.
    # @param[in]    field: str
    #                   name of the field whose values has to be fetched
    # @param[in]    gfx_index: str
    #                   adapter index with default value set to gfx_0 as we don't need to pass gfx_index value for
    #                   non-port specific fields.E.g gfx_0, gfx_1
    # @param[in]    port: str
    #                   optional argument with default value set to None. Name of port is needed to fetch values of
    #                   port specific fields from command_line_param
    # @return       value: str
    #                   value of the requested field
    @classmethod
    def get_cmd_line_param_values(cls, field, gfx_index='gfx_0', port=None):
        value = ''
        if port is None:
            # Non-port specific fields have same values across adapter dictionaries, hence fetch it from 1st dictionary
            if field in VdscBase.cmd_line_param[0].keys():
                value = VdscBase.cmd_line_param[0][field]
            else:
                # Port name has to be passed to fetch port specific fields as display can be connected to different
                # ports of different adapters
                logging.debug("Please provide port name for port specific fields")
        else:
            gfx_index_num = int(gfx_index[-1])

            # Add NATIVE to the port name if the key is not found. E.g. When cmd has HDMI_F_NATIVE, the port arg will
            # contain only the port name (HDMI_F) but the cmd dict will have HDMI_F_NATIVE as the key.
            if VdscBase.cmd_line_param[gfx_index_num].get(port) is None:
                port = port + "_" + "NATIVE"

            if field in VdscBase.cmd_line_param[gfx_index_num][port]:
                value = VdscBase.cmd_line_param[gfx_index_num][port][field]
            else:
                # If field name is neither a generic field nor port specific then it is invalid
                logging.debug("Invalid field name passed by user")

        return value

    ##
    # @brief        This method checks if the port on given adapter is vdsc_supported or not and updates info
    #               accordingly, also updates vdsc_target_ids dictionary.If display is vdsc_supported and is lfp
    #               then corresponding list is updated
    # @note         IMPORTANT: Make displays active before calling this function
    # @param[in]    gfx_index: str
    #                   adapter name Ex. gfx_0, gfx_1
    # @param[in]    port: str
    #                   Contains port names which has to be checked for vdsc_support
    # @param[in]    target_id: str
    #                   Contains list of target id for the port
    # @param[in]    panel_filter: str
    #                   Indicates if panel type is EDP, MIPI etc. Default value = None indicates external panel
    # @return       None
    @classmethod
    def update_vdsc_panel_target_info(cls, gfx_index, port, target_id, panel_filter=None) -> None:
        panel_info = {gfx_index: port}
        is_vdsc_panel = DSCHelper.is_vdsc_supported_in_panel(gfx_index, port)

        if is_vdsc_panel is True:
            # if its a vdsc_supported panel but not present in vdsc related lists then append it accordingly
            if panel_info not in cls.vdsc_panels:
                if panel_filter == "EDP":
                    cls.edp_vdsc_panels.append({gfx_index: port})
                elif panel_filter == "MIPI":
                    cls.mipi_vdsc_panels.append({gfx_index: port})

                cls.vdsc_panels.append({gfx_index: port})
                cls.vdsc_target_ids[port] = target_id

            # if vdsc supported panel_info was previously present in non-vdsc list, then remove it
            if panel_info in cls.non_vdsc_panels:
                cls.non_vdsc_panels.remove(panel_info)

        if is_vdsc_panel is False:
            # if Non-vdsc supported panel_info was previously present in vdsc related lists, then remove it
            if panel_info in cls.vdsc_panels:
                cls.vdsc_panels.remove(panel_info)
                del cls.vdsc_target_ids[port]

                if panel_info in cls.edp_vdsc_panels:
                    cls.edp_vdsc_panels.remove(panel_info)
                elif panel_info in cls.mipi_vdsc_panels:
                    cls.mipi_vdsc_panels.remove(panel_info)

            # if Non-vdsc supported panel_info is not already present in non-vdsc list, then append it
            if panel_info not in cls.non_vdsc_panels:
                cls.non_vdsc_panels.append(panel_info)

    ##
    # @brief        Private method which is used to plug the MST or SST Tiled display.
    # @param[in]    gfx_index: str
    #                    Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port_name: str
    #                   Represents the name of the port in which the display has to be plugged. E.g. dp_b, dp_c
    # @param[in]    topology_type: str
    #                   Represents whether its MST/SST
    # @param[in]    xml_file_name: str
    #                   Contains the MST topology information.
    # @param[in]    is_low_power: bool
    #                   True to plug in low power mode, False to plug in normal mode
    # @return       None
    def _plug_mst_or_tiled_display(self, gfx_index: str, port_name: str, topology_type: str, xml_file_name: str,
                                   is_low_power: bool) -> None:

        is_success = VdscBase.display_port.init_dp(port_name, topology_type)
        self.assertTrue(is_success, "Initializing of {} Failed".format(port_name))
        logging.info("Initializing {} Succeeded".format(port_name))

        is_success = VdscBase.display_port.parse_send_topology(port_name, topology_type, xml_file_name, is_low_power)
        self.assertTrue(is_success, "Failed to parse and send data to simulation driver for {}".format(port_name))
        logging.info("Successfully parsed and send data to simulation driver for {}".format(port_name))

        is_success = VdscBase.display_port.set_hpd(port_name, attach_dettach=True, gfx_index=gfx_index)
        self.assertTrue(is_success, "Set HPD call failed for {}".format(port_name))
        logging.info("Set HPD call succeeded for {}".format(port_name))

        time.sleep(20) if VdscBase.is_pre_si_environment is True else time.sleep(15)

    ##
    # @brief        A class method to get the target id from the port list.
    # @param[in]    port_list: List[str]
    #                   Contains list of port names for which target ids are required
    # @return       target_id_list: List[int]
    #                   Contains list of target ids for each of the port in the port list
    @classmethod
    def get_target_id_list(cls, port_list: List[str]) -> List[int]:
        target_id_list = []
        enumerated_display_info = VdscBase._display_config.get_enumerated_display_info()

        for port in port_list:
            target_id = VdscBase._display_config.get_target_id(port, enumerated_display_info)
            target_id_list.append(target_id)

        return target_id_list

    ##
    # @brief        Helper function to get the max mode from the supported mode array.
    # @param[in]    ctl_timing_array: ctypes.POINTER(ctl_genlock_target_mode_list_t)
    #                   Ctype pointer to an array of type ctl_display_timing_t which has supported modes.
    # @return       max_mode: ctl_display_timing_t
    #                   Contains the max mode that passed supported mode array contains.
    @classmethod
    def get_max_mode(cls, ctl_timing_array: ctypes.POINTER(ctl_genlock_target_mode_list_t)) -> ctl_display_timing_t:
        ctl_display_timing_list = []
        for mode_index in range(ctl_timing_array.NumModes):
            mode = copy.deepcopy(ctl_timing_array.pTargetModes[mode_index])
            ctl_display_timing_list.append(mode)

        max_mode = sorted(ctl_display_timing_list, key=attrgetter('HActive', 'VActive', 'RefreshRate'))[-1]
        logging.info(f"Max mode: {max_mode}")

        return max_mode

    ##
    # @brief        Update the SamplingMode string based on modes enabled in samplingMode structure
    # @param[in]    sampling_mode: SamplingMode() object
    #                    The first four bits of this object represents RGB, YUV420,YUV444, YUV422 formats respectively
    #                    These bits are set based on the color format bits obtained from mode_control_flag_data
    # @return       sampling_mode_str
    #                    returns the constructed sampling mode string
    @classmethod
    def prepare_sampling_mode_string(cls, sampling_mode: SamplingMode) -> str:
        sampling_mode_str = ""
        if sampling_mode.rgb == 1:
            sampling_mode_str += 'RGB '
        if sampling_mode.yuv420 == 1:
            sampling_mode_str += 'YUV420 '
        if sampling_mode.yuv444 == 1:
            sampling_mode_str += 'YUV444 '
        if sampling_mode.yuv422 == 1:
            sampling_mode_str += 'YUV422 '

        return sampling_mode_str

    ##
    # @brief        This method is the exit point for all VDSC test cases. This method takes care of unplugging the
    #               displays, resetting any of the registry, un-initialize sdk if any etc. Bring back the environment
    #               before the test has ran.
    # @return       None
    @classmethod
    def tearDownClass(cls):

        for port_name in VdscBase.mst_port_name_list:
            is_success = VdscBase.display_port.set_hpd(port_name, attach_dettach=False)
            assert is_success, "Set HPD call failed for {}".format(port_name)

            time.sleep(20) if VdscBase.is_pre_si_environment is True else time.sleep(15)
            logging.info("Set HPD call succeeded for {}".format(port_name))

        for master_port, slave_port in VdscBase.sst_tiled_port_name_list:
            is_success = VdscBase.display_port.set_hpd(master_port, attach_dettach=False)
            assert is_success, "Set HPD call failed for {}".format(master_port)
            is_success = VdscBase.display_port.set_hpd(slave_port, attach_dettach=False)
            assert is_success, "Set HPD call failed for {}".format(slave_port)

            time.sleep(20) if VdscBase.is_pre_si_environment is True else time.sleep(15)
            logging.info("Set HPD call succeeded for {} and {}".format(master_port, slave_port))

        # Unplug the displays and restore the configuration to the initial configuration
        for adapter_display_dict in VdscBase.external_panels:
            for adapter_index, port_name in adapter_display_dict.items():
                if port_name in VdscBase.mst_port_name_list:
                    continue
                is_success = display_utility.unplug(port_name, gfx_index=adapter_index)
                assert is_success, f"Unplugging the display at {port_name} failed"
                logging.info(f"Unplugging the display at {port_name} succeeded")

        VdscBase.display_port.uninitialize_sdk()
