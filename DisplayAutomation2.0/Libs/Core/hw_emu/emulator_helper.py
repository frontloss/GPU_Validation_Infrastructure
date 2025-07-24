#######################################################################################################################
# @file         emulator_helper.py
# @brief        Contains ConfigData dataclass, HubDisplayInfo, TiledPanelInfo and EmulatorTestCommandParser classes
#               which are used for different purposes across emulator test cases.
# @author       Praburaj Krishnan
#######################################################################################################################

from __future__ import annotations

import enum
import json
import logging
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

from Libs.Core import cmd_parser
from Libs.Core.display_config.display_config_enums import DisplayConfigTopology

tiled_panel_info_path = os.path.join("Tests\\Emulator", 'tiled_panel_info.json')
tbt_hub_display_info_path = os.path.join("Tests\\Emulator", 'tbt_hub_display_info.json')


##
# @brief        A data class which contains the required topology information to apply a display configuration.
@dataclass
class ConfigData:
    topology: enum  # E.g. enum.SINGLE, enum.EXTENDED etc
    port_list: List  # E.g ['dp_b'], ['dp_b', 'dp_c']

    ##
    # @brief     A computed property which returns the name of the config.
    #               E.g. 'EXTENDED', 'SINGLE'
    # @return    DisplayConfigTopology(self.topology).name - Name of the Display Config Topology
    @property
    def name(self):
        return DisplayConfigTopology(self.topology).name


##
# @brief        A data class which contains all the information about the tiled display and helper functions to parse
#                   the tile data from the json file. Refer tiled_panel_info.json file
class TiledPanelInfo:
    tiled_panel_info_dict: Dict[str, Dict[str, Dict[str, str]]] = {}
    MST_TILE_INFO: str = "mst_tiled_info"
    SST_TILE_INFO: str = "sst_tiled_info"

    ##
    # @brief        Initializes data members of the class.
    # @param[in]    name - String formatted Name.
    # @param[in]    tiled_dpcd_path - DPCD Path for Tiled Display
    # @param[in]    master_tiled_edid_path - EDID Path for Master tile
    # @param[in]    slave_tiled_edid_path - EDID Path for Slave tile
    def __init__(self, name: str, tiled_dpcd_path: str, master_tiled_edid_path: str, slave_tiled_edid_path: str):
        self.name: str = name
        self.tiled_dpcd_path: str = tiled_dpcd_path
        self.master_tiled_edid_path: str = master_tiled_edid_path
        self.slave_tiled_edid_path: str = slave_tiled_edid_path

    ##
    # @brief        A class method to parse the json file and get the required tile information based on the tile type
    #               and name of the tiled panel.
    # @param[in]    get - Contains the type of the Tiled display. Contains one of these two values 'mst_tiled_info' or
    #                     'sst_tiled_info'
    # @param[in]    name - Name of the Tiled Panel for which the information is required.
    # @return       tiled_panel_info - TiledPanelInfo, Returns the TilePanelInfo object by parsing the Json file.
    @classmethod
    def from_json_file(cls, get: str, name: str) -> TiledPanelInfo:
        tiled_panel_info: TiledPanelInfo
        logging.debug("Parsing {} file".format(tiled_panel_info_path))

        if bool(cls.tiled_panel_info_dict) is False:
            with open(tiled_panel_info_path) as topology_file:
                cls.tiled_panel_info_dict = json.load(topology_file)

        tiled_panel_info = cls(**cls.tiled_panel_info_dict[get][name])

        logging.debug('Get={}, name={}, TiledPanelInfo={}'.format(get, name, tiled_panel_info))
        return tiled_panel_info

    ##
    # @brief        Constructs the object representation in string format that can be returned.
    # @return       obj_repr - Object Representation in String Format.
    def __repr__(self):
        obj_repr = "name: {}, master_tiled_edid_path: {}, slave_tiled_edid_path: {}, tiled_dpcd_path: {}".format(
            self.name, self.master_tiled_edid_path, self.slave_tiled_edid_path, self.tiled_dpcd_path)

        return obj_repr


##
# @brief        A data class which contains all the information about the displays connected to the hub and helper
#               functions to parse the hub data from the json file. Refer tbt_hub_display_info.json file
class HubDisplayInfo:
    _hub_config_dict: Dict[str, List[Dict]] = {}

    ##
    # @brief        Initializes data members of the class.
    # @param[in]    port_index - Represents the position of the port in the Hub.
    # @param[in]    port_type -  Tells if its HDMI, DP or VGA
    # @param[in]    edid_name -  Name of the edid that should be plugged to the port
    # @param[in]    dpcd_name -  Name of the dpcd file that should be used along with the edid
    def __init__(self, port_index: int, port_type: str, edid_name: str, dpcd_name: str):
        self.port_index = port_index
        self.port_type = port_type
        self.edid_name = edid_name
        self.dpcd_name = dpcd_name

    ##
    # @brief        Private member function to convert the list of json string(key value pair) into list of
    #               corresponding object.
    # @param[in]    hub_config_list - List of json string object for each of the entry in the file
    #                   tbt_hub_display_info.json
    # @return       hub_display_info_list - Returns the list of HubDisplayInfo object by creating object out of the
    #                   json string.
    @classmethod
    def _convert_to_list_of_obj(cls, hub_config_list: List[Dict]) -> List[HubDisplayInfo]:
        hub_display_info_list: List[HubDisplayInfo] = []

        for item in hub_config_list:
            hub_display_info_list.append(cls(**item))

        return hub_display_info_list

    ##
    # @brief        A class method to parse the json file and get the display information connected to the hub based on
    #               the config name passed to the function.
    # @param[in]    get_hub_config - Contains the hub config name which is used to retrieve hub information
    #                   from Json file.
    # @return       hub_display_info_list - Returns the information about the each of the display connected to the hub
    #                   and as well as the position of the display on the hub
    @classmethod
    def from_json(cls, get_hub_config: str) -> List[HubDisplayInfo]:
        hub_display_info_list: List[HubDisplayInfo]
        logging.debug("Parsing {} file".format(tbt_hub_display_info_path))

        with open(tbt_hub_display_info_path) as tbt_config_file:
            cls._hub_config_dict = json.load(tbt_config_file)

        hub_display_info_list = cls._convert_to_list_of_obj(cls._hub_config_dict[get_hub_config])

        logging.debug("Hub Config Name={}, Hub Display Info: {}".format(get_hub_config, hub_display_info_list))
        return hub_display_info_list

    ##
    # @brief        Constructs the object representation in string format that can be returned.
    # @return       obj_repr - Object Representation in String Format.
    def __repr__(self) -> str:
        obj_repr = "port_index: {}, port_type: {}, edid_name: {}, dpcd_name: {}".format(self.port_index, self.port_type,
                                                                                        self.edid_name, self.dpcd_name)

        return obj_repr


##
# @brief        A parser which specifically parses the emulator test case command lines and retrieves the required info
#               from the command lines.
class EmulatorTestCommandParser:

    ##
    # @brief        Initializes the member variables for the parser to work.
    def __init__(self):
        from Tests.PowerCons.Modules import common  # To Avoid Circular Dependency.
        self.custom_tag: List[str] = ["-MST", "-SST", "-TBT", "-XML", "-ITERATION"]
        self.cmd_dict: Dict = cmd_parser.parse_cmdline(sys.argv, self.custom_tag + common.CUSTOM_TAGS)
        self.mst_tile_panel_name_list: List[str] = self.cmd_dict["MST"]
        self.sst_tile_panel_name_list: List[str] = self.cmd_dict["SST"]
        self.tbt_hub_config_name_list: List[str] = self.cmd_dict["TBT"]
        self.dp_port_list = self.get_requested_dp_port_list()
        self.port_list = self.get_requested_port_list()

    ##
    # @brief        A Member method which parses the tiled command line and retrieves the dp ports in which display
    #               needs to be plugged.
    # @return       dp_port_list - Contains dp port names in the command line.
    def get_requested_dp_port_list(self) -> List[str]:
        dp_port_list: List[str] = []
        for key, value in self.cmd_dict.items():
            if cmd_parser.display_key_pattern.match(key) is not None and key.startswith('DP_'):
                # Trimming the port type as tests checks only for the port name in free port DP list.
                dp_port_list.append(key[:4])

        logging.debug("DP Port List in the command line: {}".format(dp_port_list))
        return dp_port_list

    ##
    # @brief        A Member method which parses the command line and retrieves the ports(dp/hdmi) in which display
    #               needs to be plugged.
    # @return       port_list - Contains dp/hdmi port names in the command line.
    def get_requested_port_list(self) -> List[str]:
        port_list: List[str] = []
        for key, value in self.cmd_dict.items():
            if cmd_parser.display_key_pattern.match(key) is not None:
                if key.startswith("DP_"):
                    port_list.append(key[:4])
                elif key.startswith("HDMI_"):
                    port_list.append(key[:6])

        logging.debug("Port List in the command line: {}".format(port_list))
        return port_list

    ##
    # @brief        A Member method which constructs a dictionary which contains port name as the key and TilePanelInfo
    #               as the object.
    # @return       mst_port_panel_dict - Dictionary which maps DP port in the command line with TilePanelInfo in the
    #                   json by using the tile panel name in the command line in the same order.
    def get_mst_port_panel_dict(self) -> Dict[str, TiledPanelInfo]:
        mst_port_panel_dict = {}

        for index, name in enumerate(self.mst_tile_panel_name_list):
            tiled_panel_info = TiledPanelInfo.from_json_file(TiledPanelInfo.MST_TILE_INFO, name)
            port = self.dp_port_list[index]
            mst_port_panel_dict[port] = tiled_panel_info

        logging.debug('MST Port Panel Dict: {}'.format(mst_port_panel_dict))
        return mst_port_panel_dict

    ##
    # @brief        A Member method which constructs a dictionary which contains port pair as the key and TilePanelInfo
    #               as the object.
    # @return       sst_port_panel_dict - Dictionary which maps DP port in the command line with TilePanelInfo in the
    #                   json by using the tile panel name in the command line in the same order.
    def get_sst_port_panel_dict(self) -> Dict[Tuple[str, Optional[str]], TiledPanelInfo]:
        sst_port_panel_dict = {}

        tile_name_index = port_index = 0
        while tile_name_index < len(self.sst_tile_panel_name_list):
            name = self.sst_tile_panel_name_list[tile_name_index]
            tiled_panel_info = TiledPanelInfo.from_json_file(TiledPanelInfo.SST_TILE_INFO, name)

            # If the Slave edid path is empty it means its Master only Edid and uses only one input dp port.
            if tiled_panel_info.slave_tiled_edid_path == "":
                port_pair = (self.dp_port_list[port_index], None)
                port_index = port_index + 1
            else:
                # Uses both Master and Slave port.
                port_pair = (self.dp_port_list[port_index], self.dp_port_list[port_index + 1])
                port_index = port_index + 2

            tile_name_index = tile_name_index + 1
            sst_port_panel_dict[port_pair] = tiled_panel_info

        logging.debug('SST Port Panel Dict: {}'.format(sst_port_panel_dict))
        return sst_port_panel_dict

    ##
    # @brief        A member method which constructs a dictionary which contains tbt port in which hub is connected as
    #               the key and information about the displays connected to it as the value.
    # @return       tbt_hub_port_display_info_dict - Dict[str, List[HubDisplayInfo]]
    #                   Dictionary which maps DP port in the command line with Hub information in the json by using the
    #                   hub config name in the command line in the same order.
    def get_tbt_hub_display_info_dict(self) -> Dict[str, List[HubDisplayInfo]]:
        tbt_hub_port_display_info_dict: Dict[str, List[HubDisplayInfo]] = {}

        index = 0
        while index < len(self.tbt_hub_config_name_list):
            config_name, port_name = self.tbt_hub_config_name_list[index], self.dp_port_list[index]
            hub_display_info_list = HubDisplayInfo.from_json(get_hub_config=config_name)
            tbt_hub_port_display_info_dict[port_name] = hub_display_info_list
            index = index + 1

        logging.debug('TBT Hub Port Display Info Dict: {}'.format(tbt_hub_port_display_info_dict))
        return tbt_hub_port_display_info_dict
