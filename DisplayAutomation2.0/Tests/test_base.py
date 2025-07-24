######################################################################################
# @file         test_base.py
# @brief        This script is the common base class for all the Color Tests.
# @details      The setUp() parses the command line and creates a list of all adapters
#               and displays attached to each of the adapters.
#               Custom tags will be parsed to get details about the scenarios/ input files
#               The setUp() plugs all the displays requested as part of the command line
#               and applies the configuration passed from the command line.
#               tearDown() performs unplug of all the displays which were simulated
# @author       Smitha B
######################################################################################
import os
import sys
import time
import logging
import unittest
import xml.etree.ElementTree as ET
from Libs.Core.test_env import context
from Libs.Core.test_env import test_context
from Libs.Core.sw_sim import driver_interface
from Libs.Core.display_utility import plug, unplug
from Libs.Core import cmd_parser, reboot_helper, enum
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.sw_sim.dp_mst import DisplayPort
from Libs.Feature.display_port import dp_mst_helper
from Libs.Core.system_utility import SystemUtility
from Libs.Core.logger import gdhm


##
# @brief            TestBase class
class TestBase(unittest.TestCase):
    config = DisplayConfiguration()
    system_utility = SystemUtility()
    context_args = context.Context()
    mst_dp = DisplayPort()
    dp_mst_helper_obj = dp_mst_helper.DPMSTHelper()
    test_params_from_cmd_line = None
    is_disp_plug_required = True
    is_apply_config_required = True
    custom_tags = {
        '-SCENARIO': ['BASIC', 'STRESS', 'RESTART_DRIVER', 'DISPLAY_SWITCH', 'MONITOR_TURNOFF', 'HOTPLUG_UNPLUG',
                      'POWER_EVENT_S3', 'POWER_EVENT_S4', 'POWER_EVENT_CS', 'POWER_EVENT_S5', 'VIDEO_PLAYBACK',
                      'SNAP_MODE', 'ROTATION', 'MODE_SWITCH', 'GENERATE_TDR', 'AC_DC'],
        '-INPUTFILEPATH': '',
        '-WRITEBACK': '',
        '-IMAGEFILE': ''
    }

    ##
    # @brief        Helper function to prepare parameters required by the test
    # @param[in]    cmd_line_param - command line arguments from which parameters such as
    #               scenario, topology, required displays are parsed and prepared
    # return        test_params - test param object of type CmdLineParams
    @staticmethod
    def __prepare_params_from_command_line(self, cmd_line_param):
        test_params = context.CmdLineParams()
        for index in range(0, len(cmd_line_param)):
            for key, value in cmd_line_param[index].items():
                for custom_key, custom_value in self.custom_tags.items():
                    test_params.test_custom_tags[custom_key] = cmd_line_param[index][custom_key.strip('-')]
                test_params.topology = eval("enum.%s" % (cmd_line_param[index]['CONFIG']))
                test_params.file_name = cmd_line_param[index]['FILENAME']
                test_params.log_level = cmd_line_param[index]['LOGLEVEL']
                if cmd_parser.display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        disp_details_obj = context.CmdLineDisplayAttributes(
                            index=value['index'], connector_port=value['connector_port'], edid_name=value['edid_name'],
                            dpcd_name=value['dpcd_name'], panel_index=value['panel_index'], is_lfp=value['is_lfp'],
                            connector_port_type=value['connector_port_type'], gfx_index=value['gfx_index'].lower())
                        test_params.display_details.append(disp_details_obj)
        return test_params

    ##
    # @brief        Wrapper function to facilitate plug of the displays required by the test
    # @param[in]    display_details_list - List of all the displays passed as part of the command line
    # @return       None
    def __plug_required_displays(self, display_details_list):
        sst_tile_display = []
        if len(display_details_list) == 0:
            self.fail("Minimum 1 display is required to run the test")

        if self.is_disp_plug_required:
            self.plug_display(display_details_list)

    ##
    # @brief        Helper function to apply the display configuration requested by the test
    # @param[in]    display_details_list - List of all the displays passed as part of the command line
    # @param[in]    topology - display topology of type DisplayConfigTopology
    #                          If topology is not specified in the command line,
    #                          default configuration will be applied based on the number of displays
    # @return       Nonw
    def __set_required_display_configuration(self, display_details_list, topology):
        if self.is_apply_config_required:
            # By default, config would be set as SINGLE by the command parser
            if display_details_list.__len__() > 1 and topology == enum.SINGLE:
                topology = enum.EXTENDED
            display_and_adapter_list = []
            # Set display configuration
            enumerated_displays = self.config.get_enumerated_display_info()

            for display_index in range(0, len(display_details_list)):
                adapter_index = display_details_list[display_index].gfx_index.lower()
                port = display_details_list[display_index].connector_port
                for enum_displays in range(0, enumerated_displays.Count):
                    enum_adapter_index = enumerated_displays.ConnectedDisplays[enum_displays].DisplayAndAdapterInfo.adapterInfo.gfxIndex
                    enum_connector_port = cfg_enum.CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[enum_displays].ConnectorNPortType).name
                    if adapter_index == enum_adapter_index and port == enum_connector_port:
                        display_and_adapter_list.append(enumerated_displays.ConnectedDisplays[enum_displays].DisplayAndAdapterInfo)
            if self.config.set_display_configuration_ex(topology, display_and_adapter_list) is False:
                self.fail("Failed to apply display configuration")

    ##
    # @brief        Setup function
    # @return       None
    def setUp(self):
        # Parse the command line
        cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.custom_tags.keys())

        # Handle multi-adapter scenario
        if not isinstance(cmd_line_param, list):
            cmd_line_param = [cmd_line_param]

        # Fetch and initialize the parameters required by the test
        self.test_params_from_cmd_line = self.__prepare_params_from_command_line(self, cmd_line_param)

        # Performing Plugging and applying a configuration to Non-Reboot scenarios only
        if reboot_helper.is_reboot_scenario() is False:
            # Plug the required displays
            self.__plug_required_displays(self.test_params_from_cmd_line.display_details)

            # Set the required display configuration
            self.__set_required_display_configuration(self.test_params_from_cmd_line.display_details, self.test_params_from_cmd_line.topology)

        # Initialize context
        self.context_args.init_test_context(self.test_params_from_cmd_line)

    ##
    # @brief get EDID, DPCD and Panel spec of particular Index name
    # @param[in]    gfx_index
    # @param[in]    port
    # @param[in]    panel_index
    # @param[in]    is_lfp
    # @return       ret_info - EDID, DPCD with Panel description
    def get_panel_edid_dpcd_info(self, gfx_index: str, port: str, panel_index: str, is_lfp: bool):
        ret_info = {}
        index_to_read = None
        xml_file = os.path.join(self.context_args.test.path_info.panel_input_data_path, "PanelInputData.xml")
        if os.path.isfile(xml_file):
            xml_root = ET.parse(xml_file).getroot()
        else:
            raise Exception("Panel Input XML file not found (Path: {0}).".format(xml_file))

        if panel_index is None:
            adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()
            adapter_info = adapter_info_dict[gfx_index.lower()]
            platform_name = adapter_info.get_platform_info().PlatformName.upper()

            default_panel_list = xml_root.find("DefaultPanelList").findall("PanelPlatform")
            for panel_platform in default_panel_list:
                if panel_platform.attrib["Platform"].upper() == platform_name:
                    if is_lfp:
                        if 'DP' in port:
                            index_to_read = panel_platform.attrib["EDP"]
                        else:
                            index_to_read = 'MIPI001' #@todo : Currently PanelInputData.xml doesnt have MIPI hence same logic as prepare display followed
                    elif 'HDMI' in port:
                        index_to_read = panel_platform.attrib["HDMI"]
                    else:
                        index_to_read = panel_platform.attrib["DP"]

            if index_to_read is None:
                raise Exception("Default Panel Not Specified. Port: {0} Platform: {1}".format(panel_index, platform_name))
        else:
            index_to_read = panel_index

        for instance in list(xml_root):
            test = instance.findall('PanelInstance')
            for test_item in test:
                if test_item.attrib['PanelIndex'] == index_to_read:
                    ret_info['edid'] = test_item.attrib['EDID']
                    ret_info['dpcd'] = test_item.attrib['DPCD']
                    ret_info['desc'] = test_item.attrib['Description']
                    ret_info['dpcd'] = None if ret_info['dpcd'] == 'NA' else ret_info['dpcd']

        if len(ret_info) >= 1:
            return ret_info
        else:
            raise Exception("Invalid Panel Index : {0}".format(index_to_read))

    ##
    # @brief API to plug DFT panel. Simulate Non-MST display panel. The EDID files are read from Tools/EDIDFiles.
    # @param[in]    display_panel_info - object of type CmdLineDisplayAttributes
    # @param[in]    dp_dpcd_model_data is the model data containing DPCD transactions to be done
    #               (e.g: link training transactions)
    # @return - True if plug is successful; False, otherwise
    def plug_display_non_mst(self, display_panel_info: context.CmdLineDisplayAttributes, dp_dpcd_model_data=None):
        if display_panel_info.is_lfp is True:
            logging.warning("LFP Panel will be simulated during prepare_display")
            return True

        port_name = display_panel_info.connector_port
        gfx_index = display_panel_info.gfx_index.lower()
        edid_name = display_panel_info.edid_name
        dpcd_name = display_panel_info.dpcd_name
        panel_index = display_panel_info.panel_index

        plug_status = plug(port=port_name, edid=edid_name, dpcd=dpcd_name, is_low_power=False, panelindex=panel_index,
                           gfx_index=gfx_index)

        if plug_status is False:
            logging.error("\tFail: Plug {0} on {1} failed".format(port_name, gfx_index))
            return False

        time.sleep(5)

        # Verify if the display is plugged
        enumerated_displays = self.config.get_enumerated_display_info()
        display_attached = False
        for display_index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[display_index]
            enum_port_name = cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
            if (display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex == gfx_index) and (enum_port_name == port_name):
                logging.info("Pass: {0} plugged successfully on {1}".format(port_name, gfx_index))
                self.context_args.update_adapter_display_context()
                display_attached = True
                break
        return display_attached

    ##
    # @brief API to unplug DFT panel
    # Unplug DFT panel. The EDID files are read from Tools/EDIDFiles.
    # @param[in]    adapter_info - object of type GfxAdapterInfo
    # @param[in]    port - port on which panel to be simulated. Example: DP_B, HDMI_C...
    # @param[in]    is_low_power Pass True if panel to be plugged in Low Power state.
    # @param[in]    port_type represents if the requested port is NATIVE/TC/TBT etc.,.
    # @return       True, if unplug is successful; False, otherwise
    def unplug_display_non_mst(self, adapter_info: GfxAdapterInfo, port: str, port_type: str, is_low_power: bool=False):
        logging.info("Unplugging {0} on {1}".format(port, adapter_info.gfxIndex))
        unplug_status = unplug(port=port, is_low_power=is_low_power, port_type=port_type,
                               gfx_index=adapter_info.gfxIndex)
        if unplug_status is False:
            logging.error("\tUnable to unplug {0}".format(port))
            return False

        time.sleep(10)

        # Verify if the display is unplugged
        enumerated_displays = self.config.get_enumerated_display_info()
        for display_index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[display_index]
            if display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex == adapter_info.gfxIndex and \
                    (cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType)).name == port.upper():
                logging.error("FAIL : Display {0} is still getting enumerated; Unplug functionality failure")
                return False
        self.context_args.update_adapter_display_context()
        return True

    ##
    # @brief API to MST panel information from PanelInputData
    # @param[in]    panel_index - Panel Index value to read from PanelInputData.xml file
    # @return       dict - MST Xml file name, display tech and description from PanelInputData.xml
    def get_mst_tile_panel_info(self, panel_index: str):
        xml_file = os.path.join(self.context_args.test.path_info.panel_input_data_path, "PanelInputData.xml")
        if os.path.isfile(xml_file):
            xml_root = ET.parse(xml_file).getroot()
        else:
            raise Exception("Panel Input XML file not found (Path: {0}).".format(xml_file))

        ret_info = {'edid': None, 'display_tech': None, 'desc': None}
        for instance in xml_root:
            test = instance.findall('PanelInstance')
            for test_item in test:
                if test_item.attrib['PanelIndex'] == panel_index.upper():
                    ret_info['topology'] = test_item.attrib['TOPOLOGY']
                    ret_info['display_tech'] = test_item.attrib['display_tech']
                    ret_info['desc'] = test_item.attrib['Description']

        return ret_info

    ##
    # @brief API to plug MST/MST Tile DFT panel
    # Simulate MST display panel. The EDID files are read from Tools/EDIDFiles.
    # @param[in]    display_panel_info - object of type CmdLineDisplayAttributes
    # @return - True if plug is successful; False, otherwise
    def plug_display_mst(self, display_panel_info: context.CmdLineDisplayAttributes):
        topology_type = "MST"
        port_name = display_panel_info.connector_port
        free_port_list = display_config.get_free_ports(display_panel_info.gfx_index)

        # # Requested ports should be present in free port list
        if display_panel_info.connector_port not in free_port_list:
            logging.error(f"Port: {display_panel_info.connector_port} is not free. Exiting")
            return False

        panel_info = self.get_mst_tile_panel_info(display_panel_info.panel_index)
        if panel_info['topology'] is None:
            self.fail(f"Unable to find the Panel information for {display_panel_info.panel_index}")

        xml_file = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, "DP_MST_TILE", panel_info['topology'])
        if os.path.exists(xml_file) is False:
            self.fail(f"MST information XML File not found {xml_file}")

        # Tiled Display is being plugged in - MST Tiled Display.
        if display_panel_info.panel_index.startswith("DPMT"):
            # ToDo: Need to add support for Multi-Adapter
            # self.set_tiled_mode(port_name, topology_type, xml_file)
            self.simulate_mst_tile_panel(port_name, topology_type, xml_file)

            # Get tiled displays list.
            is_tiled_display, tiled_target_ids_list = self.dp_mst_helper_obj.get_tiled_displays_list()
            logging.info("Tiled Display List {}".format(tiled_target_ids_list))

            # Verify if the display is detected as Tiled Display - MST Tiled Display.
            if is_tiled_display:
                return self.dp_mst_helper_obj.verify_tiled_display(True, True, False, tiled_target_ids_list[0])
            else:
                logging.error("MST Tiled display not found")
                return False
        else:
            self.setnverifyMST(port_name, topology_type, xml_file)
            return True

    ##
    # @brief API to plug SST Tile DFT panel
    # Simulate SST-TILE display panel. The EDID files are read from Tools/EDIDFiles.
    # @param[in]    display_panel_info - object of type CmdLineDisplayAttributes
    # @return - True if plug is successful; False, otherwise
    def plug_display_sst_tile(self, display_panel_info: list):
        master_slave_pair = {}
        status_list = []
        for display_item in display_panel_info:
            if display_item.panel_index[:-1] not in master_slave_pair.keys():
                master_slave_pair[display_item.panel_index[:-1]] = {}
            if display_item.panel_index.endswith('M'):
                master_slave_pair[display_item.panel_index[:-1]].update({'master': display_item})
            elif display_item.panel_index.endswith('S'):
                master_slave_pair[display_item.panel_index[:-1]].update({'slave': display_item})

        for index in master_slave_pair:
            master_panel = master_slave_pair[index]['master']
            slave_panel = master_slave_pair[index]['slave']

            logging.info("TestBase: Plugging DP SST Tile on {0} and {1}({2})".format(master_panel.connector_port,
                                                                                     slave_panel.connector_port,
                                                                                     master_panel.gfx_index))

            master_plug_status = plug(port=master_panel.connector_port, is_low_power=False,
                                      panelindex=master_panel.panel_index, gfx_index=master_panel.gfx_index)

            slave_plug_status = plug(port=slave_panel.connector_port, is_low_power=False,
                                     panelindex=slave_panel.panel_index, gfx_index=master_panel.gfx_index)

            if (master_plug_status and slave_plug_status) is False:
                logging.error("\tFail: Plugging DP SST Tile on {0} and {1}({2}) failed".format(
                    master_panel.connector_port, slave_panel.connector_port, master_panel.gfx_index))
                return False
            else:
                logging.error("\tPass: Plugging DP SST Tile on {0} and {1}({2}) Success".format(
                    master_panel.connector_port, slave_panel.connector_port, master_panel.gfx_index))

            time.sleep(5)

            # Verify if the display is plugged
            enumerated_displays = self.config.get_enumerated_display_info()
            display_attached = False
            for display_index in range(enumerated_displays.Count):
                display_info = enumerated_displays.ConnectedDisplays[display_index]
                if (display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex == master_panel.gfx_index) and (
                        (cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType)).name == master_panel.connector_port.upper()):
                    logging.info("{0} successfully getting enumerated".format(master_panel.connector_port))
                    self.context_args.update_adapter_display_context()
                    display_attached = True

            status_list.append(display_attached)

        if len(status_list) == 0 or False in status_list:
            return False
        else:
            return True

    ##
    # @brief API to unplug DFT panel MST
    # Unplug MST DFT panel. The EDID files are read from Tools/EDIDFiles.
    # @param[in]    adapter_info - object of type GfxAdapterInfo
    # @param[in]    port - port on which panel to be simulated. Example: DP_B, HDMI_C...
    # @return       True, if unplug is successful; False, otherwise
    def unplug_display_mst(self, adapter_info: GfxAdapterInfo, port: str):
        logging.info("Unplugging {0} on {1}".format(port, adapter_info.gfxIndex))
        return self.mst_dp.set_hpd(port_type=port, attach_dettach=False, gfx_index=adapter_info.gfxIndex)

    ##
    # @brief        Wrapper function to facilitate plug of the displays required by the test
    # @param[in]    display_details_list - List of all the displays passed as part of the command line
    # @return       None
    def plug_display(self, display_details_list):
        sst_tile_display = []
        for index in range(0, len(display_details_list)):
            display_panel_index = display_details_list[index].panel_index

            if (display_panel_index is not None) and ((display_panel_index.startswith("DPM") or (
                    display_panel_index.startswith("DPMT")))):
                status = self.plug_display_mst(display_details_list[index])
                if status is True:
                    logging.info(f"{display_details_list[index].connector_port} Display plugged successfully")
                else:
                    logging.info(f"{display_details_list[index].connector_port} Display plugged failed")
                    self.fail(f"{display_details_list[index].connector_port} Display plugged failed")
            elif (display_panel_index is not None) and (display_panel_index.startswith("DPST")):
                sst_tile_display.append(display_details_list[index])
            else:
                status = self.plug_display_non_mst(display_details_list[index])
                if status is False:
                    # TODO: Add GDHM logging
                    self.fail("Plug display {0} on {1} failed".format(display_details_list[index].connector_port,
                                                                      display_details_list[index].gfx_index))
        if len(sst_tile_display) >= 2:
            status = self.plug_display_sst_tile(sst_tile_display)

    ##
    # @brief        API to unplug DFT panel
    #               Unplug DFT panel. The EDID files are read from Tools/EDIDFiles.
    # @param[in]    adapter_info - object of type GfxAdapterInfo
    # @param[in]    port - port on which panel to be simulated. Example: DP_B, HDMI_C...
    # @param[in]    is_low_power Pass True if panel to be plugged in Low Power state.
    # @param[in]    port_type - represents if the requested port is LFP or EFP
    # @return       True, if unplug is successful; False, otherwise
    def unplug_display(self, adapter_info: GfxAdapterInfo, port: str, is_low_power: bool, port_type: str):
        b_unplug_status = False
        b_cmdline_port = False
        logging.info("Unplugging Display {0} from Adapter {1}".format(port, adapter_info.gfxIndex))
        display_details_list = self.test_params_from_cmd_line.display_details
        for index in range(0, len(display_details_list)):
            connector_port = display_details_list[index].connector_port
            gfx_index = display_details_list[index].gfx_index
            if (connector_port == port) and (gfx_index == adapter_info.gfxIndex):
                b_cmdline_port = True
                display_panel_index = display_details_list[index].panel_index
                if (display_panel_index is not None) and (display_panel_index.startswith("DPM") or
                                                          display_panel_index.startswith("DPMT")):
                    b_unplug_status = self.unplug_display_mst(adapter_info=adapter_info, port=port)
                else:
                    b_unplug_status = self.unplug_display_non_mst(adapter_info=adapter_info, port=port,
                                                                  is_low_power=is_low_power, port_type=port_type)

        if b_cmdline_port is False:
            b_unplug_status = self.unplug_display_non_mst(adapter_info=adapter_info, port=port,
                                                          is_low_power=is_low_power, port_type=port_type)

        if b_unplug_status is False:
            logging.error("\tFAIL: Failed to unplug display {0}".format(port))
            return False

        time.sleep(10)

        # Verify if the display is unplugged
        enumerated_displays = self.config.get_enumerated_display_info()
        for display_index in range(enumerated_displays.Count):
            display_info = enumerated_displays.ConnectedDisplays[display_index]
            if display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex == adapter_info.gfxIndex and \
                    (cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType)).name == port.upper():
                logging.error("\tFAIL : Display {0} is still getting enumerated after unplug".format(port))
                return False
        self.context_args.update_adapter_display_context()
        return True

    ##
    # @brief        Tear Down function
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("Test Clean Up")
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if not panel.is_lfp:
                    unplug_status = self.unplug_display(adapter.adapter_info, panel.connector_port_type, False,
                                                        panel.port_type)
                    if unplug_status is False:
                        self.fail("Failed to unplug display")
                    else:
                        logging.info("Successfully unplugged the display {0}".format(panel.connector_port_type))

    ##
    # @brief        This method is used to build and verify a DP1.2 Topology
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type: str
    #                   This is the type of topology to be applied like SST, MST, MST Tiled
    # @param[in]    xml_file: str
    #                   Contains xml file path for give topology
    # @return       None
    def setnverifyMST(self, port_type, topology_type, xml_file):
        DPCD_MSTM_CAP_OFFSET = 0x21

        self.simulate_mst_tile_panel(port_type, topology_type, xml_file)

        # Adding additional 20 second delay for pre-si environments to make simulation data reflect in driver
        if self.system_utility.get_execution_environment_type() in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            time.sleep(20)

        # Verify the MST Topology being created by comparing the data provided and seen in CUI DP topology page
        status = self.dp_mst_helper_obj.verify_mst_topology(port_type)
        if status is False:
            self.fail()

        ##
        # Read the DPCD 600h & check the HPD status
        nativeDPCDRead = True
        dpcd_length = 1

        ##
        # Read the DPCD 21h for checking if immediate branch / native device is MST capable
        dpcd_address = DPCD_MSTM_CAP_OFFSET

        mstm_cap_reg = self.dp_mst_helper_obj.dpcd_read(port_type, nativeDPCDRead, dpcd_length, dpcd_address, None,
                                                        action="MST_CAP")
        if mstm_cap_reg is None:
            self.fail()

        if mstm_cap_reg & 0x3 == 0x1:  # Check if bit 0 only is set
            logging.info("The Connected Display is MST Display")
        elif mstm_cap_reg & 0x3 == 0x2:  # Check if bit 1 only is set
            logging.info("The connected Display is Single Stream Sideband Message Supported Display")
        else:
            logging.error("[Test Issue]: The Connected Display is not a MST Display.")
            gdhm.report_bug(
                title="[Interfaces][DP_MST] MST Test is running on non-MST display on port: {}".format(port_type),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

    ##
    # @brief        This method is used to simulate tiled mode
    # @param[in]    port_type: str
    #                   contains port type Ex: DP_B, HDMI_B
    # @param[in]    topology_type: str
    #                   This is the type of topology to be applied like SST, MST, MST Tiled
    # @param[in]    xmlfile: str
    #                   Contains xml file path for give topology
    # @param[in]    lowpower: bool
    #                   is plug during power event
    # @param[in]    attach_dettach: bool
    #                   To specify mst attach/remove status
    # @return       None
    def simulate_mst_tile_panel(self, port_type, topology_type, xmlfile, lowpower=False, attach_dettach=True):

        # initialize_dp
        if self.mst_dp.init_dp(port_type, topology_type):
            logging.info("Graphics simulation driver initialized DP object successfully")
        else:
            logging.error("Graphics simulation driver initialized DP object Failed")
            self.fail("Graphics simulation driver initialized DP object Failed")

        # parse_send_topology
        if self.mst_dp.parse_send_topology(port_type, topology_type, xmlfile, lowpower):
            logging.info("%s data parsed and sent to simulation driver successfully" % topology_type)
        else:
            logging.error("%s data parsed and sent to simulation driver failed..." % topology_type)
            self.fail("%s data parsed and sent to simulation driver failed..." % topology_type)

        # set_hpd
        if self.mst_dp.set_hpd(port_type, attach_dettach):
            if attach_dettach:
                logging.info("Simulation driver issued HPD (Hotplug Interrupt) to Graphics driver successfully")
            else:
                logging.info("Simulation driver issued HPD (Hotunplug Interrupt) to Graphics driver successfully")
            time.sleep(5)  # bug:https://hsdes.intel.com/appstore/article/#/1605363520
        else:
            logging.error("Simulation driver failed to issue HPD to Graphics driver")
            self.fail("Simulation driver failed to issue HPD to Graphics driver")

        # Wait for the simulation driver to reflect the MST/SST Tiled connection status in CUI
        time.sleep(15)
