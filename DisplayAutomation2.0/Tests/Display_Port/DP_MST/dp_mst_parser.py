########################################################################################################################
# @file         dp_mst_parser.py
# @brief        It contains several classes and methods that help in parsing the MST command lines
# @author       Praburaj Krishnan
########################################################################################################################

import os
import sys
import json
import logging
from Libs.Core import cmd_parser
from Libs.Core.test_env.test_context import TestContext
from typing import List, Dict

from Tests.PowerCons.Modules import common

topology_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dp_topologies.json')

##
# @brief        Topology Class
class Topology(object):

    ##
    # @brief        Creates topology object and initializes the attributes of the class
    # @param[in]    index: int
    #                   Index of the topology. Ex: 0, 1, 2 etc
    # @param[in]    name: str
    #                   Name of the topology. Ex: SST_TP_5, SST_TP_6
    # @param[in]    display_tech: str
    #                   Kind of the display technology requested. Ex: SST, MST etc
    # @param[in]    path: str
    #                   Contains path of the xml file
    # @param[in]    total_link_count: int
    #                   Contains total link count for RAD
    # @param[in]    parent_branch_index: int
    #                   Contains parent link count
    # @param[in]    comments: str
    #                   Contains information on supporting parent topology
    def __init__(self, index, name, display_tech, path, total_link_count = 0, parent_branch_index = 0, comments = ""):
        # type: (int, str, str, int, int, str) -> None

        self.index = index  # type: int
        self.name = name  # type: str
        self.display_tech = display_tech  # type: str
        self.path = os.path.join(TestContext.panel_input_data(), path)  # type: str
        self.total_link_count = total_link_count
        self.parent_branch_index = parent_branch_index
        self.comments = comments

    ##
    # @brief        This helps to construct a topology string which contains topology index, name, type, xml file path
    #               and returns it
    # @return       None
    def __str__(self):
        # type: () -> str

        topology_string = "Topology Index: {}, ".format(self.index)
        topology_string += "Topology Name: {}, ".format(self.name)
        topology_string += "Topology Type: {}, ".format(self.display_tech)
        topology_string += "Topology Structure Path: {}".format(self.path)
        topology_string += "Rad info total link count: {}".format(self.total_link_count)
        topology_string += "Topology parent link count: {}".format(self.parent_branch_index)
        topology_string += "Informational comments: {}".format(self.comments)

        return topology_string

    ##
    # @brief        This is a special built-in function that returns the object representation in string format
    # @return       None
    def __repr__(self):
        # type: () -> str

        return self.__str__()


##
# @brief        DPTopologyData class contains methods to convert json file data to dictionary, to convert list to dict,
#               to fetch topology object given a topology name
class DPTopologyData(object):

    ##
    # @brief        Initializes the attributes of DPTopologyData object.Topology_dict contains topology_name and
    #               topology_object as key-value pairs
    # @param[in]    sst_topology_list: List
    #                   Contains a list of sst topologies
    # @param[in]    mst_topology_list: List
    #                   Contains a list of mst topologies
    # @param[in]    mst_tiled_topology_list: List
    #                   Contains a list of mast tiled topologies
    # @param[in]    rad_info_list: List
    #                   Contains a list of RAD Info elements
    def __init__(self, sst_topology_list, mst_topology_list, mst_tiled_topology_list, rad_info_list):
        # type: ([Topology], [Topology], [Topology], [Topology]) -> None

        self.topology_dict = {}  # type : dict(str, Topology)

        self.topology_dict.update(self.to_dict(sst_topology_list))
        self.topology_dict.update(self.to_dict(mst_topology_list))
        self.topology_dict.update(self.to_dict(mst_tiled_topology_list))
        self.topology_dict.update(self.to_dict(rad_info_list))

    ##
    # @brief        This method basically loads json data into a dictionary, json.load() takes DP_topologies.json file
    #               object and returns a JSON object which contains data in the form of key/value pair. Hence it is
    #               stored into a dictionary
    # @return       unparsed_topology_dict: Dict
    #                   It is a dictionary that contains the json data from dp_topologies.json file
    @classmethod
    def from_json_file(cls):
        # type: () -> dict

        unparsed_topology_dict = {}  # type: dict

        try:
            logging.debug('Topology Data Path: {}'.format(topology_data_path))

            with open(topology_data_path) as topology_file:
                unparsed_topology_dict = json.load(topology_file)

        except EnvironmentError as error:
            logging.error(error.strerror)

        return unparsed_topology_dict

    ##
    # @brief        Converts given topology list to topology dict
    # @param[in]    topology_list: List
    #                   Contains list of topologies
    # @return       temp_topology_dict: Dict
    #                   A dictionary that contains topology details
    #                   Ex: {"SST_TP_1": {"index":1, "name":"SST_TP_1", "display_tech":"SST",
    #                   "path":"DP_MST_TILE\\DPSST_DELL_U2711.xml"}, .....}
    @classmethod
    def to_dict(cls, topology_list: List) -> Dict:
        #  type : ([]) -> dict

        temp_topology_dict = {}  # type: dict

        for topology in topology_list:
            topology = Topology(**topology)
            temp_topology_dict[topology.name] = topology

        return temp_topology_dict

    ##
    # @brief        It returns the topology object if the given topology name exists in topology dict
    # @param[in]    topology_name: str
    #                   Contains names of the topologies mentioned in the command line. Ex: SST_TP_5, MST_TILED_1
    # @return       topology: Object
    #                   Object of topology class
    def get_topology(self, topology_name):
        # type : (str) -> Topology

        topology = Topology(0, '', '', '',0 , 0, '')
        try:
            topology = self.topology_dict[topology_name]
        except KeyError as error:
            logging.error('Key {} not found.'.format(error))

        return topology

    ##
    # @brief        This helps to construct a topology data string which contains topology_id and topology data of every
    #               topology present in topology_dict
    # @return       None
    def __str__(self):
        # type: () -> str

        topology_data_string = ""

        for topology_id, topology in self.topology_dict.items():
            topology_data_string += "Key: {}, Data: {}\n".format(topology_id, topology)

        return topology_data_string

    ##
    # @brief        This is a special built-in function that returns the object representation in string format
    # @return       None
    def __repr__(self):
        # type: () -> str

        return self.__str__()


##
# @brief        DPCommandParser class contains methods to fetch requested topology details, config and DP port list from
#               the command line
class DPCommandParser:

    ##
    # @brief        Initializes the attributes of DPCommandParser object
    def __init__(self):
        self.dp_mst_custom_tag = ["-PLUG_TOPOLOGIES", "-LL_ITERATION", "-XML", "-RESTRICT", "-REG_KEY_VALUE"] \
                                 + common.CUSTOM_TAGS
        self.cmd_dict = cmd_parser.parse_cmdline(sys.argv, self.dp_mst_custom_tag)
        logging.info(f"CMD Dict: {self.cmd_dict}")

    ##
    # @brief        This method parses the DP_Topologies.json file and converts it to unparsed_json_dict.
    #               A parsed_topology_dict is created from it which contains toplogy_name, topology_object as key-value
    #               pairs.For each topology_name mentioned in the commandline, the corresponding topology object is
    #               fetched from parsed_topology_dict and topology_info_dict is created.
    # @return       topology_info_dict: Dict
    #                   Contains index, topology as key-value pairs.
    #                  {0: Topology Index: 5, Topology Name: SST_TP_5, Topology Type: SST, Topology Structure Path:
    #                  DP_MST_TILE\SSTTiled_Master_DELL2715K.xml,
    #                  1: Topology Index: 1, Topology Name: MST_TILED_1, Topology Type: MST, Topology Structure Path:
    #                  DP_MST_TILE\MST_Tiled_Basic.xml}
    @property
    def requested_topology_info_dict(self):
        # type: () -> dict

        topology_info_dict = {}  # type : dict(str, Topology)

        unparsed_json_dict = DPTopologyData.from_json_file()
        parsed_topology_dict = DPTopologyData(**unparsed_json_dict)
        topology_name_list = self.cmd_dict['PLUG_TOPOLOGIES']

        if topology_name_list != 'NONE':
            for index, topology_name in enumerate(topology_name_list):
                topology_info_dict[index] = parsed_topology_dict.get_topology(topology_name)   

        logging.info("Topology Info Dict: {}".format(topology_info_dict))               

        return topology_info_dict

    ##
    # @brief        This method helps to fetch the requested config mentioned in the commandline
    # @return       self.cmd_dict['CONFIG']: str
    #                   Returns requested config from command line parameters. Ex: SINGLE, CLONE, EXTENDED
    @property
    def requested_config(self):
        # type: () -> str

        return self.cmd_dict['CONFIG']

    ##
    # @brief        This method helps to fetch the requested DP ports from the commandline
    # @return       dp_port_list: List
    #                   Returns list of requested DP ports from the commandline.Ex ['DP_B', 'DP_C']
    @property
    def requested_dp_port_list(self):
        # type: () -> []

        dp_port_list = []

        for key, value in self.cmd_dict.items():
            if cmd_parser.display_key_pattern.match(key) is not None and key.startswith('DP_'):
                # Trimming the port type as tests checks only for the port name in free port DP list.
                dp_port_list.append(key[:4])

        return dp_port_list

    ##
    # @brief        This method helps to fetch the requested LL_ITERATION from the commandline
    # @return       iteration: int
    #                   Returns requested LL_ITERATION from command line parameters. Ex: 0, 1, 2, 10
    @property
    def requested_linkloss_b2b_iteration(self):
        # type: () -> int

        iteration = 0
        if self.cmd_dict['LL_ITERATION'] != 'NONE':
            iteration = int(self.cmd_dict['LL_ITERATION'][0])
        return iteration

    ##
    # @brief        This method helps to sort list of displays based on their index in command line dictionary
    # @return       dp_port_list: List
    #                   Returns Sorted list of displays based on index in command line
    @property
    def get_sorted_display_list(self):
        # type: () -> []

        return cmd_parser.get_sorted_display_list(self.cmd_dict)

    ##
    # @brief        This property helps to get the xml file used in mode enumeration test case
    # @return       File name of the xml which contains the MST topology xml file name and modes that has to be
    #               validated.
    @property
    def mode_enum_xml_file(self) -> str:
        file_name = ''
        if self.cmd_dict['XML'] != 'NONE':
            file_name = self.cmd_dict['XML'][0].lower()

        return file_name


if __name__ == '__main__':
    x = DPCommandParser()
    print(x.requested_topology_info_dict)
