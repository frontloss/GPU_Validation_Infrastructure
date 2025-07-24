########################################################################################################################
# @file         edp_common.py
# @brief        @ref edp_common.py contains common APIs used across EDP tests.
# @author       Vinod D S, Rohit Kumar
########################################################################################################################

import logging
import os
import random
import sys
import time
import unittest
import xml.etree.ElementTree as Et
from functools import wraps

from Libs.Core import cmd_parser, registry_access, display_essential
from Libs.Core import enum
from Libs.Core import system_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import etl_tracer
from Libs.Core.test_env import test_context
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.voltage_swing import voltage_swing_dp

EDP_PANEL_INPUT_DATA_XML = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, "PanelInputData.xml")
POWER_EVENT_DURATION_DEFAULT = 20
FMS_DISABLED = 0x1c
FMS_ENABLED = 0x1d
IS_DDRW = system_utility.SystemUtility().is_ddrw()


##
# @brief        Get panel description from PanelInputData.xml based on panel_id
# @param[in]    panel_id
# @return       description if parsing is successful, None otherwise
def get_panel_description(panel_id):
    if panel_id is None:
        return None

    description = None
    try:
        tree = Et.parse(EDP_PANEL_INPUT_DATA_XML)
        panel_input_data = tree.getroot()
        for panel_tag in panel_input_data:
            if panel_tag.tag == 'PanelCaps':
                for panel_instance in panel_tag:
                    if panel_instance.attrib["PanelIndex"] == panel_id:
                        description = panel_instance.attrib["Description"]
                        break
    except Exception as e:
        logging.info("Failed to parse {0}".format(EDP_PANEL_INPUT_DATA_XML))
        logging.debug(e)
    return description


##
# @brief        Updates registry key
# @param[in]    key_name register key name
# @param[in]    key_value value to be updated in registry
# @param[in]    key_path path of the registry key
# @param[in]    restart_driver [optional], boolean indicating if the driver has to be restarted after registry
#               key change
# @return       status, True if operation completed successfully, False otherwise
def change_reg_key(key_name, key_value, key_path=None, restart_driver=True):
    ##
    # Check if expected value is already set
    diss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
    legacy_reg_args = registry_access.LegacyRegArgs(registry_access.HKey.LOCAL_MACHINE, key_path)
    if key_path is None:
        data, _ = registry_access.read(diss_reg_args, key_name)
    else:
        data, _ = registry_access.read(legacy_reg_args, key_name)

    if data == key_value:
        logging.debug("\tPASS: {0} Expected= {1}, Actual= {2}".format(key_name, hex(key_value), hex(data)))
    else:
        ##
        # if expected value is not set, update the registry key
        if key_path is None:
            result = registry_access.write(diss_reg_args, key_name, registry_access.RegDataType.DWORD, key_value)
        else:
            result = registry_access.write(legacy_reg_args, key_name, registry_access.RegDataType.DWORD, key_value)
        if result is False:
            logging.error("\tChanging %s in registry is failed" % key_name)
            return False

        ##
        # Restart Display Driver if gfx registry got changed
        if key_path is None and restart_driver:
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                logging.error("\tDisplay driver restart failed")
                return False

        ##
        # Check if expected value is set
        if key_path is None:
            data, _ = registry_access.read(diss_reg_args, key_name)
        else:
            data, _ = registry_access.read(legacy_reg_args, key_name)
        if data == key_value:
            logging.debug("\tPASS: {0} Expected= {1}, Actual= {2}".format(key_name, hex(key_value), hex(data)))
        else:
            logging.error("\tFAIL: {0} Expected= {1}, Actual= {2}".format(key_name, hex(key_value), hex(data)))
            logging.error("\tFailed to change {0} in registry".format(key_name))
            return False

    return True


##
# @brief        Helper function to print current display configuration
# @param[in]    prefix [optional], string indicating the prefix to be used while printing the current topology
# @return       None
def print_current_topology(prefix=""):
    display_config_ = display_config.DisplayConfiguration()

    enumerated_displays = display_config_.get_enumerated_display_info()
    current_config = display_config_.get_current_display_configuration_ex()
    topology = current_config[0]
    for index in range(len(current_config[1])):
        current_mode = display_config_.get_current_mode(enumerated_displays.ConnectedDisplays[index].TargetID)
        panel_name = enumerated_displays.ConnectedDisplays[index].FriendlyDeviceName
        if panel_name == '':
            panel_name = 'Internal Display'
        temp = " {0} (TargetID= {1}, PanelName= \"{2}\", Res= {3}x{4}@{5})".format(
            current_config[1][index],
            enumerated_displays.ConnectedDisplays[index].TargetID,
            panel_name,
            current_mode.HzRes,
            current_mode.VtRes,
            current_mode.refreshRate
        )
        topology += temp
    logging.info("{0}Current Topology= {1}".format(prefix, topology))


##
# @brief        Update voltage swing table selection
# @param[in]    edp_panel string indicating edp panel
# @param[in]    table table selection - low or default
# @return       None
def set_vswing_table(edp_panel='DP_A', table='DEFAULT'):
    logging.info("\tSetting {0} VSwing table for {1}".format(table, edp_panel))
    gfx_vbt = Vbt()

    table_selection = 0 if table == 'LOW' else 1

    ##
    # Get panel index
    # PanelType for port A
    # PanelType2 for port B
    panel_index = gfx_vbt.get_lfp_panel_type(edp_panel)
    logging.info("\t\tPanel Index= {0}".format(panel_index))

    shift = 0
    if panel_index % 2 != 0:
        shift = 3

    ##
    # VSwingPreEmphasisTableSelection
    # Bit 3:0/7:4 - based on panel index
    #               eDP Vswing Pre-emph setting table
    #               0 =  Low Power Swing setting(200 mV)
    #               1 =  Default Swing settings(400 mV)
    # https://gfxspecs.intel.com/Predator/Home/Index/20142
    logging.debug("\t\tVSwingPreEmphasisTableSelection[{0}]= {1}".format(int(panel_index / 2), hex(
        gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)])))
    if (gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)] >> shift) & 0xF == table_selection:
        logging.info(
            "\t\tPASS: {0} VBT VSwingPreEmphasis Table Selection Expected= {1}, Actual= {1}".format(edp_panel, table))
    else:
        gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)] = table_selection << shift
        if gfx_vbt.apply_changes() is False:
            logging.error("\t\tUnable to set VBT_BLOCK_27")
            return False
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            logging.error("\t\tFailed to restart display driver")
            return False

        gfx_vbt.reload()

        ##
        # VSwingPreEmphasisTableSelection
        # Bit 3:0/7:4 - based on panel index
        #               eDP Vswing Pre-emph setting table
        #               0 =  Low Power Swing setting(200 mV)
        #               1 =  Default Swing settings(400 mV)
        # https://gfxspecs.intel.com/Predator/Home/Index/20142
        logging.debug("\t\tVSwingPreEmphasisTableSelection[{0}]= {1}".format(int(panel_index / 2), hex(
            gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)])))
        if (gfx_vbt.block_27.VSwingPreEmphasisTableSelection[int(panel_index / 2)] >> shift) & 0xF == table_selection:
            logging.info(
                "\t\tPASS: {0} VBT VSwingPreEmphasis Table Selection Expected= {1}, Actual= {1}".format(edp_panel,
                                                                                                        table))
        else:
            logging.info(
                "\t\tFAIL: {0} VBT VSwingPreEmphasis Table Selection Expected= {1}, Actual= {2}".format(
                    edp_panel, table, 'LOW' if table == 'DEFAULT' else 'DEFAULT'))
            return False
    return True


##
# @brief        Verifies the PHY programming for EDP by comparing voltage swing level programmed in DPCD with
#               voltage swing level programmed in PHY registers
# @param[in]    edp_panel [optional], string indicating edp panel
# @return       status, True if verification passed, False otherwise
def verify_phy_programming(edp_panel='DP_A'):
    voltage_swing_levels = voltage_swing_dp.verify_voltage_swing(display=edp_panel)
    if voltage_swing_levels is False:
        return False, voltage_swing_levels
    return True, voltage_swing_levels


##
# @brief        Verify expected ModeSet path from analyzer logs
# @param[in]    fms Expected mode set path. Checks for FMS if True, otherwise checks for Full Mode Set
# @param[in]    edp_panels list of targeted eDP panels
# @param[in]    is_vswing_supported [optional], boolean indicating if voltage swing is supported
# @return       status, True if expected path matches for all the edp panels, False otherwise
def verify_fms(fms=True, edp_panels=None, is_vswing_supported=False):
    ##
    # Add default eDP panel (DP_A) to list of edp_panels is None
    if edp_panels is None:
        edp_panels = ['DP_A']

    status = True
    for edp_panel in edp_panels:
        # Parse ETL Analyzer logs to get FMS information
        mode_set_data = __parse_analyzer_logs(edp_port=edp_panel.split('_')[-1])
        if mode_set_data is None:
            logging.error("No ModeSet logs found for {0}".format(edp_panel))
            status = False
            continue

        ##
        # Get the most recent mode set data
        mode_set_data = mode_set_data[-1]

        if fms is True and mode_set_data['fms'] is True:
            logging.info("\tPASS: Expected {0} ModeSet= FastModeSet, Actual= FastModeSet (Timing: {1}ms)".format(
                edp_panel, mode_set_data['total_time']))
            if mode_set_data['link_training_status'] is False:
                logging.info(
                    "\tPASS: Expected {0} LinkTraining= NoLinkTraining, Actual= NoLinkTraining".format(edp_panel))
            else:
                logging.error(
                    "\tFAIL: Expected {0} LinkTraining= NoLinkTraining, Actual= {1}".format(
                        edp_panel, "FastLinkTraining" if mode_set_data['flt'] is True else "FullLinkTraining"))
                status = False
        elif fms is True and mode_set_data['fms'] is False:
            logging.error("\tFAIL: Expected {0} ModeSet= FastModeSet, Actual= FullModeSet (Timing: {1}ms)".format(
                edp_panel, mode_set_data['total_time']))
            if mode_set_data['link_training_status'] is False:
                logging.info(
                    "\tPASS: Expected {0} LinkTraining= NoLinkTraining, Actual= NoLinkTraining".format(edp_panel))
            else:
                logging.error(
                    "\tFAIL: Expected {0} LinkTraining= NoLinkTraining, Actual= {1}".format(
                        edp_panel, "FastLinkTraining" if mode_set_data['flt'] is True else "FullLinkTraining"))
            status = False
        elif fms is False and mode_set_data['fms'] is True:
            logging.error("\tFAIL: Expected {0} ModeSet= FullModeSet, Actual= FastModeSet (Timing: {1}ms)".format(
                edp_panel, mode_set_data['total_time']))
            if mode_set_data['link_training_status'] is False:
                logging.error(
                    "\tFAIL: Expected {0} LinkTraining= FLT or FullLinkTraining, Actual= NoLinkTraining".format(
                        edp_panel))
            else:
                logging.info(
                    "\tPASS: Expected {0} LinkTraining= {1}, Actual= {1}".format(
                        edp_panel, "FastLinkTraining" if mode_set_data['flt'] is True else "FullLinkTraining"))
            status = False
        elif fms is False and mode_set_data['fms'] is False:
            logging.info("\tPASS: Expected {0} ModeSet= FullModeSet , Actual= FullModeSet (Timing: {1}ms)".format(
                edp_panel, mode_set_data['total_time']))
            if mode_set_data['link_training_status'] is False:
                logging.error(
                    "\tFAIL: Expected {0} LinkTraining= FLT or FullLinkTraining, Actual= NoLinkTraining".format(
                        edp_panel))
                status = False
            else:
                logging.info(
                    "\tPASS: Expected {0} LinkTraining= {1}, Actual= {1}".format(
                        edp_panel, "FastLinkTraining" if mode_set_data['flt'] is True else "FullLinkTraining"))
        if is_vswing_supported is True:
            phy_status, vswing_emp_sel = verify_phy_programming(edp_panel)
            if phy_status is False:
                status = False
    return status


##
# @brief        Verify expected LinkTraining path from analyzer logs
# @param[in]    flt Expected link training path. Checks for FLT if True, otherwise checks for Full link training
# @param[in]    flt_params FastLinkParameters given in VBT at the time of FLT enabling
# @param[in]    edp_panels list of targeted eDP panels
# @param[in]    is_vswing_supported [optional], boolean indicating if voltage swing is supported
# @return       status, True if expected link training path matches for all the eDP panels, False otherwise
def verify_flt(flt=True, flt_params=None, edp_panels=None, is_vswing_supported=False):
    # Add default eDP panel (DP_A) to list of edp_panels is None
    if edp_panels is None:
        edp_panels = ['DP_A']

    status = True
    for edp_panel in edp_panels:
        # Parse ETL Analyzer logs to get FMS information
        mode_set_data = __parse_analyzer_logs(edp_port=edp_panel.split('_')[-1])
        if mode_set_data is None:
            logging.error("No ModeSet logs found for {0}".format(edp_panel))
            status = False
            continue

        # Get the most recent mode set data
        mode_set_data = mode_set_data[-1]

        if mode_set_data['link_training_status'] is False:
            logging.error(
                "\tFAIL: Expected {0} LinkTraining= {1}, Actual= NoLinkTraining".format(
                    edp_panel, "FastLinkTraining" if flt is True else "FullLinkTraining"))
            status = False
        else:
            if flt is True and mode_set_data['flt'] is True:
                logging.info("\tPASS: Expected= FastLinkTraining , Actual= FastLinkTraining")
            elif flt is True and mode_set_data['flt'] is False:
                logging.error("\tFAIL: Expected= FastLinkTraining, Actual= FullLinkTraining")
                status = False
            elif flt is False and mode_set_data['flt'] is True:
                logging.error("\tFAIL: Expected= FullLinkTraining, Actual= FastLinkTraining")
                status = False
            elif flt is False and mode_set_data['flt'] is False:
                logging.info("\tPASS: Expected= FullLinkTraining , Actual= FullLinkTraining")

        if mode_set_data['fms'] is True:
            logging.error(
                "\tFAIL: Expected {0} ModeSet= FullModeSet, Actual= FastModeSet (Timing: {1}ms)".format(
                    edp_panel, mode_set_data['total_time']))
            status = False
        else:
            logging.info(
                "\tPASS: Expected {0} ModeSet= FullModeSet, Actual= FullModeSet (Timing: {1}ms)".format(
                    edp_panel, mode_set_data['total_time']))

        # Check the expected and actual link rate, lane count, voltage swing and pre-emphasis values for Yangra
        if IS_DDRW:
            if mode_set_data['link_training_status'] is True and edp_panel in flt_params.keys():
                if mode_set_data['link_bw_set'] != flt_params[edp_panel]['link_rate']:
                    logging.warning(
                        '\tLink Rate Expected= {0}, Actual= {1}'.format(
                            hex(flt_params[edp_panel]['link_rate']), hex(mode_set_data['link_bw_set'])))
                else:
                    logging.info(
                        '\tPASS: Link Rate Expected= {0}, Actual= {1}'.format(
                            hex(flt_params[edp_panel]['link_rate']), hex(mode_set_data['link_bw_set'])))

                if mode_set_data['lane_count_set'] != flt_params[edp_panel]['lane_count']:
                    logging.error(
                        '\tFAIL: Lane Count Expected= {0}, Actual= {1}'.format(
                            hex(flt_params[edp_panel]['lane_count']), hex(mode_set_data['lane_count_set'])))
                    status = False
                else:
                    logging.info(
                        '\tPASS: Lane Count Expected= {0}, Actual= {1}'.format(
                            hex(flt_params[edp_panel]['lane_count']), hex(mode_set_data['lane_count_set'])))

                if mode_set_data['training_lane0_set'][0] & 0x3 != flt_params[edp_panel]['voltage_swing']:
                    logging.error(
                        '\tFAIL: Voltage Swing Level Expected= {0}, Actual= {1}'.format(
                            hex(flt_params[edp_panel]['voltage_swing']),
                            hex(mode_set_data['training_lane0_set'][0] & 0x3)))
                    status = False
                else:
                    logging.info(
                        '\tPASS: Voltage Swing Level Expected= {0}, Actual= {1}'.format(
                            hex(flt_params[edp_panel]['voltage_swing']),
                            hex(mode_set_data['training_lane0_set'][0] & 0x3)))

                if (mode_set_data['training_lane0_set'][0] >> 3) & 0x3 != flt_params[edp_panel]['pre_emphasis']:
                    logging.error(
                        '\tFAIL: Pre-emphasis Level Expected= {0}, Actual= {1}'.format(
                            hex(flt_params[edp_panel]['pre_emphasis']),
                            hex((mode_set_data['training_lane0_set'][0] >> 3) & 0x3)))
                    status = False
                else:
                    logging.info(
                        '\tPASS: Pre-emphasis Expected= {0}, Actual= {1}'.format(
                            hex(flt_params[edp_panel]['pre_emphasis']),
                            hex((mode_set_data['training_lane0_set'][0] >> 3) & 0x3)))

        if is_vswing_supported is True:
            phy_status, vswing_emp_sel = verify_phy_programming(edp_panel)
            if phy_status is False:
                status = False
    return status


##
# @brief        Parse Analyzer logs
# @param[in]    edp_port strign indicating
# @param[in]    filename ETL Analyzer logs file
# @return       output, a list containing mode set events data
#               None, in case of any failure
def __parse_analyzer_logs(edp_port='A', filename=etl_tracer.ANALYZER_LOG_FILE):
    output = []

    ##
    # Wait for 5 seconds to make sure Analyzer.exe has dumped the logs in ANALYZER_LOG_FILE
    time.sleep(5)

    ##
    # Make sure analyzer logs are present
    if not os.path.exists(filename):
        logging.error("Analyzer logs NOT found at {0}".format(filename))
        return None

    with open(filename, 'r') as fp:
        if IS_DDRW:
            ##
            # Analyzer logs sequence for Yangra ModeSet
            # SetTiming Entry Event
            # SetTiming logs
            # Link Training logs
            # SetTiming Exit Event
            mode_set_entry = None
            for line in fp:
                line = line.lower()
                if 'settiming entry event' in line:
                    ##
                    # Initialize mode set entry dictionary on SetTiming Entry Event
                    # Example: SetTiming Entry Event - DDI_SETTIMINGSFROMVIDPN, Entry Time - 3912537228060.07
                    mode_set_entry = {
                        'entry_time': float(line.strip().split('entry time - ')[1]),
                        'exit_time': None,
                        'total_time': None,
                        'fms': None,
                        'flt': True,
                        'link_bw_set': 0,
                        'lane_count_set': 0,
                        'training_lane0_set': [],
                        'link_training_status': False
                    }
                elif 'dpcd read' in line and 'link_bw_set' in line:
                    if mode_set_entry is None:
                        continue
                    next_line = next(fp)
                    mode_set_entry['link_bw_set'] = int(next_line.strip()[:4], 16)
                elif 'dpcd read' in line and 'lane_count_set' in line:
                    if mode_set_entry is None:
                        continue
                    next_line = next(fp)
                    mode_set_entry['lane_count_set'] = int(next_line[:4], 16)
                    mode_set_entry['lane_count_set'] &= 0x3
                elif 'dpcd write' in line and 'training_lane0_set' in line:
                    if mode_set_entry is None:
                        continue
                    next_line = next(fp)
                    lane_settings = next_line.split(',')[:-1]
                    mode_set_entry['training_lane0_set'] = []
                    for setting in lane_settings:
                        if setting != '':
                            mode_set_entry['training_lane0_set'].append(int(setting, 16))
                elif 'dpcd read' in line:
                    if mode_set_entry is None:
                        continue
                    next_line = next(fp)
                    if '0x77,0x77,0x81' in next_line or '0x77,0x00,0x81' in next_line:
                        mode_set_entry['link_training_status'] = True
                elif 'dpcd write' in line and 'training_pattern_set' in line:
                    if mode_set_entry is None:
                        continue
                    next_line = next(fp)
                    if '0x00' not in next_line:
                        mode_set_entry['flt'] = False
                ##
                # Example: SetTiming @ PORT_A:PIPE_A:Sink_0_eDP Src 2880x1920 : B8G8R8X8 SCALING_IDENTITY Active
                # 2880x1920 @ 60 Hz : Total 3040x1964 @ 358150000 Hz as FMS
                elif 'Full Mode Set'.lower() in line and ('PORT_' + edp_port).lower() in line:
                    if mode_set_entry is not None:
                        mode_set_entry['fms'] = False
                elif 'FMS'.lower() in line and ('PORT_' + edp_port).lower() in line:
                    if mode_set_entry is not None:
                        mode_set_entry['fms'] = True
                ##
                # Example: SetTiming Exit Event - DDI_SETTIMINGSFROMVIDPN, Exit Time - 3912537228078.03,
                # SetTiming Time - 17.96484375
                elif 'SetTiming Exit Event'.lower() in line:
                    if mode_set_entry is None:
                        continue
                    if mode_set_entry['fms'] is None:
                        mode_set_entry = None
                        continue
                    mode_set_entry['exit_time'] = float(line.strip().split('exit time - ')[1].split(',')[0])
                    mode_set_entry['total_time'] = float(line.strip().split(' - ')[-1])
                    output.append(mode_set_entry)
                    mode_set_entry = None
        else:
            mode_set_entry = None
            for line in fp:
                if "FastLinkTraining True".lower() in line.lower():
                    mode_set_entry = {
                        'flt': True,
                        'link_training_status': True
                    }
                elif "FullLinkTraining True".lower() in line.lower():
                    mode_set_entry = {
                        'flt': False,
                        'link_training_status': True
                    }
                elif "SetTiming time".lower() in line.lower():
                    if mode_set_entry is None:
                        mode_set_entry = {
                            'flt': False,
                            'link_training_status': False
                        }
                    mode_set_entry['total_time'] = float(line[17:-1])
                    if float(line[17:-1]) < 100:
                        mode_set_entry['fms'] = True
                    else:
                        mode_set_entry['fms'] = False
                    output.append(mode_set_entry)
                    mode_set_entry = None
    return output


##
# @brief        Internal helper function to make decorator parameterized
def __parameterized_decorator(decorator):
    def caller_layer(*args, **kwargs):
        def callee_layer(f):
            return decorator(f, *args, **kwargs)

        return callee_layer

    return caller_layer


##
# @brief        Exposed decorator to configure any given test.
#               Available options:
#                   Repeat a test
#                   Block/Unblock a test
#               Repeat count is decided based on '-repeat' parameter in command line.
#               Block/Unblock is decided based on '-selective' parameter in command line.
#
#               Example:
#                   For example, please see EDP\FMS\edp_fms_basic.py
#
# @param[in]    func target test
# @param[in]    repeat If true, test will be repeated based on '-repeat' value
# @param[in]    selective a list of whitelisted events for the test.
# @param[in]    clear_args if True '-repeat', '-selective' and following values will be deleted from sys.argv
# @note         There is no need to add '-repeat' and '-selective' tags in your test's custom tag list. This decorator
#               will take care of cleaning additional arguments based on clear_arg flag. There must be at least one
#               test case with clear_repeat_arg=True in the TestCase class.
# @return       None
@__parameterized_decorator
def configure_test(func, repeat=False, selective=None, clear_args=False):
    wraps(func)

    ##
    # -REPEAT:      repeat tag is used to run a test multiple times. If there is no value given for repeat in command
    #               line all the tests will be executed only once.
    # -SELECTIVE:   selective tag is used to run only selective tests. If there is no value given for selective in
    #               command line, all the tests will be executed.
    #
    # Both of the above features can be used in any test case. Selective list can be expanded to include more possible
    # events.
    __possible_selective_values = ["CS", "S3", "S4", "S5", "DRIVER_RESTART", "MODE_SET", "LID", "AC_DC",
                                   "MULTI_RR", "DISPLAY_SWITCH"]
    cmd_line_params = cmd_parser.parse_cmdline(sys.argv, ['-REPEAT', '-SELECTIVE'])

    ##
    # If clear_repeat_arg flag is True, remove the -repeat and -selective tags from command line
    if clear_args is True:
        new_args = []
        skip = False
        for arg in sys.argv:
            if skip is True:
                if str(arg).upper() in __possible_selective_values:
                    continue
                skip = False
                continue
            if str(arg).lower() in ['-repeat', '-selective']:
                skip = True
                continue
            new_args.append(arg)
        sys.argv = new_args

    ##
    # Check if test has some selective conditions
    if selective is not None:
        ##
        # Check for blocked tests
        if "BLOCKED" in selective:
            return

        ##
        # Check for Yangra of Legacy
        if "LEGACY" in selective and IS_DDRW:
            return
        if "YANGRA" in selective and not IS_DDRW:
            return

        ##
        # Check for Pre-Si or Post-Si environment
        if "POST_SI" in selective and \
                system_utility.SystemUtility().get_execution_environment_type() in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            return
        if "PRE_SI" in selective and \
                not system_utility.SystemUtility().get_execution_environment_type() in \
                    ["SIMENV_FULSIM", "SIMENV_PIPE2D"]:
            return

        ##
        # If no selective condition is given in command line all tests will run
        # If there is some selective condition given in command line, test will run only if one or more selective
        # conditions are present in selective_test_list
        if (selective != ["LEGACY"] and selective != ["YANGRA"]) and \
                (cmd_line_params['SELECTIVE'] != 'NONE' and
                 len(set(selective) & set(cmd_line_params['SELECTIVE'])) == 0):
            return

    # Check for test repeat count
    number_of_repeats = 1
    if repeat is True and cmd_line_params['REPEAT'] != 'NONE':
        number_of_repeats = int(cmd_line_params['REPEAT'][0])

    def wrapper(*args, **kwargs):
        status = True
        error_message = None
        for index in range(number_of_repeats):
            if number_of_repeats > 1:
                logging.info("")
                logging.info("{0} iteration : {1}".format(func.__name__, index + 1))
                logging.info("")
            try:
                func(*args, **kwargs)
            except Exception as e:
                status = False
                logging.error(e)
                error_message = e
        if status is False:
            assert False, error_message

    return wrapper


##
# @brief        This function is used to get a test suite
# @param[in]    test_case_class test class name
# @param[in]    section_list list of strings for prefixes of test suite
# @return       test suite that can be run using runner
def get_test_suite(test_case_class, section_list):
    cmd_line_params = cmd_parser.parse_cmdline(sys.argv, ["-TEST_SEQUENCE"])
    test_suite = None
    if cmd_line_params['TEST_SEQUENCE'] != 'NONE':
        for test_name in cmd_line_params['TEST_SEQUENCE']:
            test_name = test_name.lower()
            if test_suite is None:
                test_suite = unittest.makeSuite(test_case_class, prefix=test_name)
            else:
                temp_test_suite = unittest.makeSuite(test_case_class, prefix=test_name)
                setattr(test_suite, '_tests', getattr(test_suite, '_tests') + getattr(temp_test_suite, '_tests'))

        ##
        # clear command line
        new_args = []
        skip = False
        for arg in sys.argv:
            if skip is True:
                if str(arg).upper()[0] == "T":
                    continue
                skip = False
                continue
            if str(arg).lower() in ['-test_sequence']:
                skip = True
                continue
            new_args.append(arg)
        sys.argv = new_args
    else:
        for section in section_list:
            if test_suite is None:
                test_suite = unittest.makeSuite(test_case_class, prefix=("t_" + section))
                if len(getattr(test_suite, '_tests')) > 0:
                    to_be_shuffled = getattr(test_suite, '_tests')[1:]
                    random.shuffle(to_be_shuffled)
                    setattr(test_suite, '_tests', [getattr(test_suite, '_tests')[0]] + to_be_shuffled)
            else:
                temp_test_suite = unittest.makeSuite(test_case_class, prefix=("t_" + section))
                if len(getattr(temp_test_suite, '_tests')) > 0:
                    to_be_shuffled = getattr(temp_test_suite, '_tests')[1:]
                    random.shuffle(to_be_shuffled)
                    setattr(
                        test_suite,
                        '_tests',
                        getattr(test_suite, '_tests') + [getattr(temp_test_suite, '_tests')[0]] + to_be_shuffled)

    test_sequence = [getattr(t, '_testMethodName') for t in getattr(test_suite, '_tests')]
    logging.info("Test Sequence: {0}".format(' '.join(test_sequence)))
    return test_suite
