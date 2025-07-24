#######################################################################################################################
# @file         collage_xml_parser.py
# @brief        This file contains CollageParser class which helps to parse the collage the command line
#
# @author       Praburaj Krishnan
#######################################################################################################################

import json
import logging
import os
import re
import sys
import xml.etree.ElementTree as eTree
from collections import Counter
from collections import OrderedDict
from typing import Optional, Dict, List, Tuple

from Libs.Core import cmd_parser, display_utility
from Libs.Core.test_env.test_context import TestContext

from Tests.PowerCons.Modules import common


dp_pattern = re.compile('DP_' + (r'(?:%s)\b' % '|'.join(cmd_parser.supported_ports)))
hdmi_pattern = re.compile('HDMI_' + (r'(?:%s)\b' % '|'.join(cmd_parser.supported_ports)))
xml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CollagePanelData', 'collage_edid_dpcd_config.xml')


##
# @brief        Contains functions required to parse and get the display data from collage_edid_dpcd_config.xml
class CollageParser(object):
    custom_tag_list = common.CUSTOM_TAGS + ['-CONFIG_PATH', '-ID', '-USER_EVENT']

    ##
    # @brief        Gets display list from the xml by using the config_path, config_id.
    # @param[in]    config_path: str
    #                   Contains path of the particular configuration like 'SST/TRI_COLLAGE'.
    # @param[in]    config_id: str
    #                   Contains the configuration id, using which the displays to plug will be determined.
    # @param[in]    xml_to_be_parsed: Optional[str]
    #                   Contains the xml name where display data will be present.
    # @return       status: bool
    #                   Indicates the status of the function call.
    #               display_list: List[Dict] - sorted by key 'type';
    #                   A list which contains the display details like 'edid', 'dpcd' and display type like 'DP'
    #                   or 'HDMI'. Example:  [{ 'gfx_index'='gfx_0', 'panel_index'='DPS006', 'type': 'DP', '
    #                   edid': 'Benq_SW320_DP.bin', 'dpcd': 'Benq_SW320_DPCD.txt', 'is_child_display'='True'}]
    @classmethod
    def get_display_list_from_xml(cls, config_path: str, config_id: str, xml_to_be_parsed: Optional[str] = xml_path
                                  ) -> Tuple[bool, List[Dict]]:

        logging.info('Parsing collage xml to get the display details to be plugged')
        logging.debug('config_path: %s.config_id: %s.xml_to_be_parsed: %s' % (config_path, config_id, xml_to_be_parsed))

        data = eTree.parse(xml_to_be_parsed)
        collage_config_list = data.getroot()
        config_path = config_path + '/CONFIGURATION[@id="' + config_id + '"]'
        configuration = collage_config_list.find(config_path)

        logging.debug("Full config path: %s" % config_path)

        if configuration is not None:
            return True, list(display.attrib for display in configuration)

        return False, []

    ##
    # @brief        Helper function to get the command line dictionary using the command parser by passing the sys args
    #               and custom collage tag used in the collage command line.
    # @return       cmd_dict: Dict
    #                   Format - {key: {'': '', '': '', ...}, key: {'':''. '': '', ...}}
    #                   Contains all information passed in the command line in dictionary format.
    @classmethod
    def parse_collage_command(cls) -> Dict:

        logging.info("Parsing collage command line to get the type of collage topology to plug")

        cmd_dict = cmd_parser.parse_cmdline(sys.argv, cls.custom_tag_list)

        logging.debug("cmd_dict: " + json.dumps(cmd_dict))
        return cmd_dict

    ##
    # @brief        Helper function to get the port list passed in the command line by iterating the cmd_dict.
    # @param[in]    cmd_dict: Dict
    #                   Format - {key: {'': '', '': '', ...}, key: {'':''. '': '', ...}}
    #                   Contains all information passed in the command line in dictionary format.
    # @return       port_list: List[str]
    #                   Contains all the ports passed in the command
    #                   line. Example: ['dp_a', 'dp_b', 'hdmi_e']
    @classmethod
    def get_port_list(cls, cmd_dict: Dict) -> List[str]:

        logging.info("Get port list by iterating through cmd_dict")
        logging.debug("cmd_dict: " + json.dumps(cmd_dict))

        port_dict = {}

        for key, value in cmd_dict.items():
            if (dp_pattern.match(key) is not None or hdmi_pattern.match(key) is not None
                    and value['connector_port'] is not None):
                port_dict.update({value['index']: key})

        # Order by position in the command line.
        sorted_port_tuple = sorted(port_dict.items(), key=lambda k: k[0])
        port_dict = OrderedDict(sorted_port_tuple)
        port_list = list(port_dict.values())

        logging.debug("Port list obtained by iterating the cmd_dict: {}".format(port_list))

        return port_list

    ##
    # @brief        Checks for the validity of the command line by matching the port list in the command line and with
    #               the display list parsed which contains the port type
    # @param[in]    port_list: List[str]
    #                   Contains the port names present in the command line
    #                   Example: ['dp_a', 'dp_b', 'hdmi_d']
    # @param[in]    display_list: List[Dict]
    #                   Contains the edid, dpcd and display type information.
    #                   Example: [{'edid': 'DP_3011.EDID', 'type': 'DP', 'dpcd': 'DP_3011_DPCD.txt'}, ...]
    # @return       status: bool
    #                   Returns True if the count(port_list) matches with the count(display_list) else False
    @classmethod
    def is_valid_collage_command(cls, port_list: List[str], display_list: List[Dict]) -> bool:

        logging.info("Checking for the validity of the command line arguments")

        xml_display_mapping = Counter(display['type'] for display in display_list)
        argument_display_mapping = Counter(port[:-2] for port in port_list)

        return xml_display_mapping == argument_display_mapping

    ##
    # @brief        Parses the collage xml which contains all possible collage topology supported along with the display
    #               details like edid, dpcd and type of the display
    # @param[in]    xml_to_be_parsed: Optional[str]
    #                   Contains the xml name where display data will be present.
    # @return       status, cmd_dict: Tuple[bool, Dict]
    #               status: bool
    #                   Indicates the status of the function call.
    #               cmd_dict: Dict
    #                   Format - {key: {'': '', '': '', ...}, key: {'':''. '': '', ...}}
    #                   Contains all information passed in the command line in dictionary format.
    @classmethod
    def parse_collage_xml(cls, xml_to_be_parsed: Optional[str] = xml_path) -> Tuple[bool, Dict]:

        logging.info("Getting panel data by parsing " + xml_to_be_parsed)
        cmd_dict = cls.parse_collage_command()
        port_list = cls.get_port_list(cmd_dict=cmd_dict)

        if {'CONFIG_PATH', 'ID'}.issubset(set(cmd_dict)) is False:
            logging.error("Missing mandatory arguments in the command line.")
            return False, cmd_dict

        config_id = cmd_dict['ID'][0]
        config_path = cmd_dict['CONFIG_PATH'][0]

        is_success, display_list = cls.get_display_list_from_xml(config_path, config_id, xml_to_be_parsed)
        if is_success is False and len(display_list) > 0:
            logging.error("Failed to parse " + xml_to_be_parsed + " file")
            return False, cmd_dict

        if cls.is_valid_collage_command(port_list, display_list) is False:
            logging.error("Invalid command line/configuration, not present in " + xml_to_be_parsed)
            return False, cmd_dict

        for port, display in zip(port_list, display_list):
            port_properties = cmd_dict[port]
            if "MST" in config_path:
                port_properties['topology_type'] = display['topology']
                port_properties['xml_file'] = os.path.join(TestContext.panel_input_data(), "DP_MST_TILE", display['xml'])
            else:
                input_data = display_utility.get_panel_edid_dpcd_info(port=port, panel_index=display['panel_index'])
                if input_data is not None:
                    port_properties['edid_name'] = input_data['edid']
                    port_properties['dpcd_name'] = input_data['dpcd']
                # Common port properties.
                port_properties['panel_index'] = display['panel_index']
            port_properties['gfx_index'] = display['gfx_index']
            port_properties['is_child_display'] = True if display['is_child_display'] == 'True' else False

            # For all other cases this key won't be present.
            if 'is_vdsc_required' in display:
                port_properties['is_vdsc_required'] = True if display['is_vdsc_required'] == 'True' else False

        return True, cmd_dict


if __name__ == '__main__':
    _, command_dict = CollageParser.parse_collage_xml()
    print("New cmd dict: %s" % command_dict)
