###################################################################################################################
# @file         mode_xml_parser.py
# @addtogroup   NorthGate
# @brief        To parse xml having display and mode details
# @author       Golwala Ami
###################################################################################################################

import xml.etree.ElementTree as ET
from collections import OrderedDict


##
# @brief        Parses xml for the details of displays and corresponding mode details
# @param[in]    xml_file: xml file which needs to be parsed
# @return       display_dictionary: Ordered dictionary having panel details
def parse_xml(xml_file):
    # display_dictionary = {
    #     'Display1': {'panel': 'DELL 3219Q', 'Connector': 'Type-C', 'HActive': 1024, 'VActive': 768, 'RefreshRate': 60,
    #               'Scaling': 'MDS', 'AudioChannels':2, 'AudioSampleRates':[32, 44.1, 48]},
    #     'Display2': {'panel': 'BENQ SW320', 'Connector': 'DP', 'HActive': 1920, 'VActive': 1080, 'RefreshRate': 60,
    #               'Scaling': 'MDS', 'AudioChannels':None, 'AudioSampleRates':None}}
    display_dictionary = OrderedDict()

    tree = ET.parse(xml_file)
    root = tree.getroot()

    displays = root.findall("./Displays")
    verifications = root.findall("./Verification1")
    for element in displays:
        display_instance_handle = element.findall('Display')
        for display_instance in display_instance_handle:
            sub_dictionary = {}
            key = 'Display' + display_instance.get('Index')
            sub_dictionary['panel'] = display_instance.get('Name')
            sub_dictionary['Connector'] = display_instance.get('Connector')
            display_dictionary[key] = sub_dictionary

    for element in verifications:
        verification_instance_handle = element.findall('Display')
        for verification_instance in verification_instance_handle:
            key = 'Display' + verification_instance.get('Index')
            display_dictionary[key]['HActive'] = verification_instance.get('HActive')
            display_dictionary[key]['VActive'] = verification_instance.get('VActive')
            display_dictionary[key]['RefreshRate'] = verification_instance.get('RefreshRate')
            display_dictionary[key]['Scaling'] = verification_instance.get('Scaling')
            display_dictionary[key]['AudioChannels'] = verification_instance.get('AudioChannels')
            display_dictionary[key]['AudioSampleRates'] = verification_instance.get('AudioSampleRates')

    return display_dictionary
