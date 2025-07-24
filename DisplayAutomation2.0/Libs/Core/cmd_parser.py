########################################################################################################################
# @file         cmd_parser.py
# @brief        Parser for command line arguments
#               Contains APIs for parsing command line arguments.
#
#               **Predefined arguments**
#               Tag                 Possible Values                                         Default
#               *************************************************************************************
#               -CONFIG             SINGLE/CLONE/EXTENDED                                   SINGLE
#               -LOGLEVEL           CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET                NOTSET
#               -LFP_NONE           Standalone tag. No value required.                      NONE
#                                   LFP_NONE is a special tag which is specified for each
#                                   adapter separately. LFP_NONE is used to request to
#                                   unplug any simulated LFP panel on target system. If no
#                                   adapter index is given, gfx_0 will be considered.
#                                   Ex:
#                                   test.py -gfx_0 -lfp_none -gfx_1 -lfp_none
#                                   test.py -lfp_none
#                                   test.py -gfx_1 -lfp_none
#               -[DISPLAY]_[PORT]   where, DISPLAY and PORT can be anything from
#                                   DISPLAYS = ['EDP', 'DP', 'HDMI', 'MIPI'] and
#                                   PORTS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
#                                   Ex: -EDP_A, -DP_B, -HDMI_C
#
#                                   This tag can take three arguments
#                                   [EDID_NAME] - EDID file name to be used for this port
#                                   [DPCD_NAME] - DPCD file name
#                                   [PANEL_INDEX] - Panel Index ( from PanelInputData.xml )
#                                   Ex:
#                                   -edp_a SINK_EDP011
#                                   -dp_b DELL_3011.EDID DELL_3011_DPCD.txt
#               -VBT_INDEX_[INDEX]  where, INDEX can be any integer based on the port_index_mapping dictionary from
#                                   prepare_display_setup script
#                                   Ex:
#                                   test.py -edp_a SINK_EDP023 VBT_INDEX_1
#                                   test.py -mipi_a VBT_INDEX_0
#                                   test.py -mipi_a VBT_INDEX_0 -mipi_c VBT_INDEX_1
#                                   test.py -mipi_a SINK_MIP008 VBT_INDEX_1 -mipi_c SINK_MIP011 VBT_INDEX_0
#                                   test.py -edp_a SINK_EDP023 VBT_INDEX_1 -edp_b SINK_EDP011 VBT_INDEX_0
#                                   test.py -edp_a edid dpcd VBT_INDEX_1 -edp_b edid dpcd VBT_INDEX_0
#                                   test.py -edp_a edid dpcd VBT_INDEX_1 -mipi_c VBT_INDEX_0
#                                   test.py -edp_a edid dpcd VBT_INDEX_0 -mipi_c SINK_MIP011 VBT_INDEX_1
#
#                                   Note:
#                                   1. This tag should be given after EDID or DPCD or Panel_Index in command line
#                                   2. If VBT_INDEX tag is provided for one LFP or EFP displays, other corresponding
#                                   LFPs or EFPs must contain the custom VBT_INDEX provided.
#                                   3. Mapping for individual platforms and possible LFP or EFP VBT indices for the same
#                                   can be found in the 'port_index_mapping' dictionary
#                                   Ex: 'TGL': {'LFP': [0, 1], 'EFP': [2, 3, 4, 5, 6, 7]}
#                                       Here, TGL can have 2 LFPs with possible VBT Index 0 or 1.
#                                       Similarly, EFPs can have index between 2 to 7.
#               -GFX_[INDEX]        where, INDEX can be anything from [0, 1, 2, 3]
#                                   Ex: -gfx_0, -gfx_1
#
#               **Adding custom arguments**
#               User can pass their own custom tags as a list to parse_cmdline() API.
#               Example:
#               custom_tags = ["-FEATURE", "-DURATION", ...]
#               output = cmd_parser.parse_cmdline(sys.argv, custom_tags)
#
#               **Parsing Output**
#               Command:
#               test.py -edp_a SINK_EDP011 -dp_b DELL_3011.EDID DELL_3011_DPCD.txt -hdmi_c -config extended -duration 1
#
#               Output:
#               {
#                   'CONFIG': 'EXTENDED',           --> Predefined tag
#                   'LOGLEVEL': 'NOTSET',           --> Predefined tag with default value
#                   'FILENAME': 'test.py',          --> Predefined tag
#                   'DURATION': ['1'],              --> Custom tag added by user. Note that it is a list of strings.
#                   'FEATURE': 'NONE',              --> Custom tag added by user with default value
#                   'DP_A': {                       --> Note that EDP_A is converted to DP_A
#                       'index': 0,                 --> position of display in command line (EDP_A is given first)
#                       'connector_port': 'DP_A',
#                       'edid_name': None,
#                       'dpcd_name': None,
#                       'panel_index': 'SINK_EDP011',
#                       'connector_port_type': 'NATIVE',    --> Possible values: NATIVE/TC/TC_TBT/TBT/PLUS
#                       'is_lfp': True,             --> Will be True in case of eDP and MIPI ports
#                       'gfx_index': 'gfx_0',       --> graphics adapter index
#                   },
#                   'DP_B': {
#                       'index': 1,                 --> position of display in command line (DP_B is given second)
#                       'connector_port': 'DP_B',
#                       'edid_name': 'DELL_3011.EDID',
#                       'dpcd_name': 'DELL_3011_DPCD.txt',
#                       'panel_index': None,
#                       'connector_port_type': 'NATIVE',
#                       'is_lfp': False,
#                       'gfx_index': 'gfx_0',
#                   },
#                   'HDMI_C': {
#                       'index': 2,
#                       'connector_port': 'HDMI_C',
#                       'edid_name': None,
#                       'dpcd_name': None,
#                       'panel_index': None,
#                       'connector_port_type': 'NATIVE',
#                       'is_lfp': False,
#                       'gfx_index': 'gfx_0',
#                   }
#               }
#               The parser generates a list of above dictionary in case of multi-adapter scenario where index of list
#               represents the adapter.
#
#               **Sample commands**
#               python file_name.py
#               python file_name.py -edp_a
#               python file_name.py -EDP_A -loglevel info
#               python file_name.py -eDp_a -LOGLEVEL DEBUG
#               python file_name.py -dp_a abc
#               python file_name.py -edp_f asb -dp_f qwe asd -loglevel critical
#               python file_name.py -edp_f asb -dp_f qwe asd -loglevel critical -myTag psr1 psr2
#               python file_name.py -edp_f asb -dp_f qwe asd -loglevel critical -c1 psr1 -customTag psr2
#               python file_name.py -edp_b asb -dp_c qwe asd
#               python file_name.py -config abc -edp_c asb zxc -dp_f qwe asd
#               python file_name.py -CONFIG CLONE -EDP_A EDID DPCD -dp_b EDID -hdmi_c EDID DPCD -MIPI_f EDID DPCD
#               python file_name.py -CONFIG CLONE -EDP_A EDID DPCD -DP_B EDID DPCD -HDMI_C EDID DPCD -MIPI_F EDID DPCD
#               python file_name.py -gfx_0 -edp_a SINK_EDP001 -dp_b -gfx_1 -hdmi_c -config clone
#               python file_name.py -gfx_1 -dp_b -gfx_0 -dp_b -gfx_1 -edp_a -config extended
#               python file_name.py -edp_a edid dpcd VBT_INDEX_1 -edp_b panel_index VBT_INDEX_0
#               python file_name.py -mipi_a edid dpcd VBT_INDEX_1 -mipi_c edid dpcd VBT_INDEX_0
#               python file_name.py -edp_a panel_index VBT_INDEX_0 -mipi_c panel_index VBT_INDEX_1
#               No Validation is done by this parser.
#               The parser is case insensitive except the EDID and DPCD values provided
# @author       Suraj Gaikwad, Beeresh Gopal, Ami Golwala, Rohit Kumar
########################################################################################################################

import argparse
import re
import sys

MAX_ADAPTER_COUNT = 4
__cursor = {}  # Used to store the current position of display params in case of similar display for multi adapter

##
# List of Supported Displays
supported_displays = ['EDP', 'DP', 'HDMI', 'MIPI']
##
# List of Supported Ports
supported_ports = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                   'B_TC', 'C_TC', 'D_TC', 'E_TC', 'F_TC', 'G_TC', 'H_TC', 'I_TC',
                   'B_TBT', 'C_TBT', 'D_TBT', 'E_TBT', 'F_TBT', 'G_TBT', 'H_TBT', 'I_TBT',
                   'B_TC_TBT', 'C_TC_TBT', 'D_TC_TBT', 'E_TC_TBT', 'F_TC_TBT', 'G_TC_TBT', 'H_TC_TBT', 'I_TC_TBT',
                   'B_PLUS', 'C_PLUS', 'D_PLUS', 'E_PLUS', 'F_PLUS', 'G_PLUS', 'H_PLUS', 'I_PLUS',
                   'A_NATIVE', 'B_NATIVE', 'C_NATIVE', 'D_NATIVE', 'E_NATIVE', 'F_NATIVE', 'G_NATIVE', 'H_NATIVE',
                   'I_NATIVE']

##
# Regular expressions to parse and build parser flag
# E.g.: -EDP_A, -EDP_F, -DP_B, etc.
display_flag_pattern = re.compile(
    '-' + (r'\b(?:%s)' % '|'.join(supported_displays)) + '_' + (r'(?:%s)\b' % '|'.join(supported_ports)))

##
# Regular expressions to parse keys in the Output dictionary
# E.g.: EDP_A, EDP_F, DP_B, etc
display_key_pattern = re.compile(
    (r'\b(?:%s)' % '|'.join(supported_displays)) + '_' + (r'(?:%s)\b' % '|'.join(supported_ports)))


##
# @brief        Converts the all the command arguments to UPPERCASE except the EDID and DPCD values
# @param[in]    args_list - list consisting command option and values in sequence
# @return       args_list - list consisting command option and values in sequence and in UPPERCASE
def flatten_cmd_case(args_list):
    opt_pattern = re.compile('^-([A-Za-z]+[0-9]*)(_*([A-Za-z])*([0-9])*)(_*[A-Za-z]*[0-9]*)(_*[A-Za-z]*[0-9]*)?$')

    for i in range(len(args_list)):
        cmd = args_list[i]
        if opt_pattern.match(cmd) is not None:
            args_list[i] = args_list[i].upper()

    return args_list


##
# @brief        API to map display plug order based on command-line
# @details      Based on assumption that display plug order will be the same as command line input order.
#               It traverse the command line argument in sequence and assign the index value starting from 0.
#               If EDID and DPCD argument exists then assign them to the respective display type else assign None
#               Port names are not assigned in this function
# @param[in]    args_dict - Intermediate arguments dictionary
# @param[in]    cmd_args - List containing the system command line arguments in sequence
# @param[in]    adapter_index - Targeted graphics adapter index
# @return       output - Arguments dictionary with display attributes from command line
def map_plug_order_and_port(args_dict, cmd_args, adapter_index):
    global __cursor
    display_sequence = []
    output = {}
    display_adapter_mapping = [[] for _ in range(MAX_ADAPTER_COUNT)]
    lfp_none_mapping = ['NONE' for _ in range(MAX_ADAPTER_COUNT)]
    active_adapter_index = 0
    for item in cmd_args:
        if item.startswith('-'):
            if item == '-LFP_NONE':
                lfp_none_mapping[active_adapter_index] = 'TRUE'
                continue

            tag = item[1:].split('_')[0]
            if tag == 'GFX':
                active_adapter_index = int(item[1:].split('_')[1])
            if tag in supported_displays:
                display_sequence.append(item[1:])
                display_adapter_mapping[active_adapter_index].append(item[1:])

    ##
    # Set LFP_NONE tag for requested adapter_index
    output['LFP_NONE'] = lfp_none_mapping[adapter_index]

    for i in range(len(display_sequence)):
        key = display_sequence[i]
        if key not in display_adapter_mapping[adapter_index] or key in output.keys():
            continue
        __cursor[key] = 0 if key not in __cursor.keys() else __cursor[key] + 1
        value = args_dict[key][__cursor[key]]
        plug_order = i
        port_list = key.split('_')
        display_name = port_list[0]
        port_name = port_list[1]
        if len(port_list) == 4:
            port_type = port_list[2] + "_" + port_list[3]
        elif len(port_list) == 3:
            port_type = port_list[2]
        else:
            port_type = 'PLUS'
        edid_file_name = None
        dpcd_file_name = None
        vbt_index = None

        ##
        # Connector Port for EDP_A => DP_A
        if 'EDP' in display_name:
            connector_port = ('{0}_{1}'.format('DP', port_name))
        else:
            connector_port = ('{0}_{1}'.format(display_name, port_name))

        # Check if panel index is passed through commandline. If so extract and remove from list so that it will not
        # disturb EDID/DPCD parsing provided below
        raw_sink_data = [var for var in value if var.upper().startswith('SINK_')]
        if len(raw_sink_data) == 1:
            value.remove(raw_sink_data[0])
            panel_index = raw_sink_data[0].upper().replace('SINK_', '')
        else:
            panel_index = None

        xml_file_name = [var for var in value if var.upper().startswith('DPCD_MODEL_')]
        if len(xml_file_name) == 1:
            value.remove(xml_file_name[0])
            xml_file_name = xml_file_name[0].upper().replace('DPCD_MODEL_', '')
        else:
            xml_file_name = None

        non_pr_panel_index = [var for var in value if var.upper().startswith('NONPR_')]
        if len(non_pr_panel_index) == 1:
            value.remove(non_pr_panel_index[0])
            non_pr_panel_index = non_pr_panel_index[0].upper().replace('NONPR_', '')
        else:
            non_pr_panel_index = None
        # Check if VBT_INDEX_X is passed in the commandline
        vbt_index_ls = [var for var in value if var.upper().startswith('VBT_INDEX_')]
        if len(vbt_index_ls) > 0:
            vbt_index = vbt_index_ls[0]
            value.remove(vbt_index)  # To make sure current logic works intact

        ##
        # Only EDID value provided
        if len(value) == 1:
            edid_file_name = value[0]
        ##
        # EDID and DPCD value provided
        if len(value) == 2:
            edid_file_name = value[0]
            dpcd_file_name = value[1]
        output[key] = {
            'index': plug_order, 'edid_name': edid_file_name, 'dpcd_name': dpcd_file_name, 'vbt_index': vbt_index,
            'connector_port': connector_port, 'panel_index': panel_index, 'connector_port_type': port_type,
            'dpcd_model': xml_file_name, 'non_pr_panel_index': non_pr_panel_index,
            'is_lfp': True if ('MIPI' in display_name or 'EDP' in display_name) else False,
            'gfx_index': 'GFX_%s' % adapter_index}
    return output


##
# @brief        Prepares the parser by adding the valid flags in the parser
# @param[in]    custom_tags - list of custom tags passed by user
# @return       parser - ArgumentParser object
def prepare_parser(custom_tags=None):
    parser = argparse.ArgumentParser(description='Process the Command line Arguments.')

    ##
    # Add flag/option for CONFIG for the parser
    parser.add_argument('-CONFIG', default='SINGLE', type=str.upper)
    parser.add_argument('-LOGLEVEL', default='NOTSET',
                        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'], type=str.upper)
    parser.add_argument('-LFP_NONE', nargs='*', action='append')

    ##
    # Adds display flags/options for the parser.
    # E.g.: -EDP_A, -DP_B, -HDMI_C etc...
    for display_name in supported_displays:
        for port_name in supported_ports:
            parser.add_argument("-{0}_{1}".format(display_name, port_name), nargs='*', action='append')

    if custom_tags is not None:
        for tags in custom_tags:
            parser.add_argument(tags, default='None', nargs='*', type=str.upper)

    for adapter_index in range(MAX_ADAPTER_COUNT):
        parser.add_argument('-GFX_{0}'.format(adapter_index), nargs='*', default='NO_ADAPTER')
    return parser


##
# @brief        Command Line Argument Parser Main Module
# @param[in]    args_list - Command-line arguments list
# @param[in]    custom_tags - List of custom tags
# @return       output - Arguments List if Multi-adapter, Dict if Single-adapter
def parse_cmdline(args_list, custom_tags=None):
    global __cursor

    # Converts the arguments to UPPERCASE
    args_list = flatten_cmd_case(args_list)

    if custom_tags is not None:
        custom_tags = [tag.upper() for tag in custom_tags]

    # Assigning back the arguments list to sys.argv for argparser to process it
    sys.argv = args_list
    parser = prepare_parser(custom_tags)
    results = parser.parse_args()
    args_dict = vars(results)

    ##
    # Removing the keys containing None values from the dictionary
    temp_dict = {}
    for key, value in args_dict.items():
        if value is not None and value != 'NO_ADAPTER':
            temp_dict[key] = value
    args_dict = temp_dict

    ##
    # Checking the values passed for each argument in command line
    # At most two values are allowed. i.e. EDID name and DPCD name respectively
    for key, value in args_dict.items():
        if display_key_pattern.match(key) is not None and value is not None:
            for display_value in value:
                if len(display_value) > 3:
                    parser.error('A Display can have zero to three values not {}.'.format(len(display_value)))

    output = []
    __cursor = {}
    for adapter_index in range(MAX_ADAPTER_COUNT):
        output.append({
            'CONFIG': args_dict['CONFIG'],
            'LOGLEVEL': args_dict['LOGLEVEL'],
            'FILENAME': sys.argv[0]
        })
        if custom_tags is not None:
            output[-1].update({tag[1:]: args_dict[tag[1:]] for tag in custom_tags})

        ##
        # Assigns the port, panel_name and index to the displays
        display_dict = map_plug_order_and_port(args_dict, args_list, adapter_index)
        output[-1].update(display_dict)

    ##
    # Return the complete list in case of multi adapter
    if len(set(['-GFX_{0}'.format(adapter_index) for adapter_index in range(MAX_ADAPTER_COUNT)]) & set(sys.argv)) > 0:
        return output

    ##
    # Return GFX_0 dictionary otherwise
    return output[0]


##
# @brief        sort list of displays based on their index in command line dictionary
# @param[in]    cmdline_args_dict - Command line dictionary
# @return       output - Sorted displays list based on index
def get_sorted_display_list(cmdline_args_dict):
    output = []
    # Multi adapter scenario
    if isinstance(cmdline_args_dict, list):
        for cmdline_args in cmdline_args_dict:
            for display_key, display in cmdline_args.items():
                if display_key_pattern.match(display_key):
                    output.insert(display['index'], {display['gfx_index'].lower(): display['connector_port']})
        return output
    for key in cmdline_args_dict.keys():
        if display_key_pattern.match(key):
            display_items = {key: cmdline_args_dict[key]}
            for key2, value in sorted(display_items.items(), key=lambda kv: kv[1]['index']):
                output.append(display_items[key2]['connector_port'])
    return output


##
# @brief        Get custom tag list from command line
# @return       custom_tags - list of displays supported custom tags
def get_custom_tag():
    # Strip out all the custom tags present in the command line. Display, config, loglevel, lfp_none and gfx index tags
    # are hard coded in command parser, hence no need to include in custom tags list.
    custom_tags = [custom_tag.upper() for custom_tag in sys.argv if custom_tag.startswith("-") and
                   display_flag_pattern.match(custom_tag.upper()) is None and
                   custom_tag.upper() not in ["-CONFIG", "-LOGLEVEL", "-LFP_NONE"] and
                   not custom_tag.upper().startswith("-GFX_")]

    # Add TEST and RESET tags if not already present
    custom_tags += ["-TEST"] if "-TEST" not in custom_tags else []
    custom_tags += ["-RESET"] if "-RESET" not in custom_tags else []
    return custom_tags


if __name__ == '__main__':

    args = sys.argv
    ##
    # mytags is a list of custom tags which user wants to pass from commandline
    mytags = ['-c1']
    result_dict = parse_cmdline(args, mytags)

    print('\n', result_dict, '\n')

    for key, value in result_dict.items():
        if display_key_pattern.match(key) is not None:
            print('\n\n', key, ': \n')
            for subkey, subvalue in value.items():
                print('\t', subkey, ' : ', subvalue)
        else:
            print('\n\n', key, ' : ', value)
