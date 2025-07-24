######################################################################################
# @file     display_utility.py
# @brief    Python module providing utility methods for display related operations
# @author   Ami Golwala, Smitha B, Vinod D S, Amit Sau, Suraj Gaikwad
######################################################################################
import itertools
import logging
import os
import time
import xml.etree.ElementTree as ET
from Lib.enum import IntEnum  # Override with Built-in python3 enum script path

from Libs import env_settings
from Libs.Core import cmd_parser
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.sw_sim import driver_interface
from Libs.Core.test_env.test_context import TestContext, TestContextPersistence
from Libs.Core.vbt import vbt_context
from Libs.Core.vbt.vbt import Vbt
from Libs.Core.wrapper.valsim_args import DongleType
from Libs.Feature.crc_and_underrun_verification import UnderRunStatus


##
# @brief        VbtPanelType enum
# @details      Update this Enum based on vbt_context.DEVICE_CLASS dictionary changes
class VbtPanelType(IntEnum):
    LFP_DP = vbt_context.DEVICE_CLASS['LFP_DP']  # Integrated eDP display
    LFP_MIPI = vbt_context.DEVICE_CLASS['LFP_MIPI']  # Integrated MIPI display
    HDMI = vbt_context.DEVICE_CLASS['HDMI']  # Integrated HDMI/DVI display
    DP = vbt_context.DEVICE_CLASS['DP']  # Integrated DisplayPort only
    PLUS = vbt_context.DEVICE_CLASS['PLUS']  # Integrated DisplayPort with HDMI/DVI Compatible


##
# TODO:
#   1. Ensure DFT and Smart Hot Plug Emulation works hand in hand

##
# @brief        Helper function which will verify required displays are attached or not.
# @details      This API will plug the display if its not attached.
# @param[in]    cmdline_args_dict - Command line arguments dictionary
# @return       (plugged_display_list, enumerated_displays) - (list of displays plugged, enumerated display object)
def plug_displays(self, cmdline_args_dict):
    dp_edid = 'DP_3011.EDID'
    dp_dpcd = 'DP_3011_dpcd.txt'
    hdmi_edid = 'HDMI_Dell_3011.EDID'
    __display_config = disp_cfg.DisplayConfiguration()

    # calling enumeratedDisplay
    enumerated_displays = __display_config.get_enumerated_display_info()

    if enumerated_displays is None:
        logging.error("enumerated_displays is None")
        self.fail("enumerated_displays is None")

    logging.debug("Enumerated Display Information: %s", enumerated_displays.to_string())
    plugged_display_list = []

    for key, value in cmdline_args_dict.items():
        if cmd_parser.display_key_pattern.match(key) is not None:
            connector_port_name = value['connector_port']
            vbt_panel_type = get_vbt_panel_type(connector_port_name, 'gfx_0')
            if vbt_panel_type not in [VbtPanelType.LFP_DP, VbtPanelType.LFP_MIPI] and connector_port_name[:2] == 'DP':
                ##
                # Assign default edid_name if it is None
                if value['edid_name'] is not None:
                    dp_edid = value['edid_name']
                    ##
                # Assign default dpcd_name if it is None
                if value['dpcd_name'] is not None:
                    dp_dpcd = value['dpcd_name']

                logging.debug(
                    "Trying to plug %s with Edid_name:%s Dpcd_name:%s" % (
                        value['connector_port'] + "_" + value['connector_port_type'], dp_edid, dp_dpcd))
                if plug(value['connector_port'], dp_edid, dp_dpcd, False, value['connector_port_type']) is False:
                    logging.error("Failed to plug %s" % value['connector_port'] + "_" + value['connector_port_type'])
                    self.fail()
                plugged_display_list.append(value['connector_port'])

            if (connector_port_name is not None and
                    connector_port_name[:4] == 'HDMI'):

                ##
                # Assign default edid_name if it is None
                if value['edid_name'] is not None:
                    hdmi_edid = value['edid_name']

                logging.debug("Trying to plug %s with Edid_name:%s" % (
                    value['connector_port'] + "_" + value['connector_port_type'], hdmi_edid))
                if plug(value['connector_port'], hdmi_edid, None, False, value['connector_port_type']) is False:
                    logging.error("Failed to plug %s" % value['connector_port'] + "_" + value['connector_port_type'])
                    self.fail()
                plugged_display_list.append(value['connector_port'])

    enumerated_displays = __display_config.get_enumerated_display_info()

    if enumerated_displays is None:
        logging.error("enumerated_displays is None")
        self.fail("enumerated_displays is None")

    logging.info('Enumerated display info[In display utility]: {}'.format(enumerated_displays.to_string()))

    for key, value in cmdline_args_dict.items():
        ##
        # check if display is plugged in or not
        if cmd_parser.display_key_pattern.match(key) is not None:
            connector_port = value['connector_port']
            if disp_cfg.is_display_attached(enumerated_displays, connector_port) is False:
                logging.error("Failed to plug %s", connector_port)
                plugged_display_list.remove(connector_port)
                self.fail()

    logging.debug("Enumerated Display Information: %s", enumerated_displays.to_string())
    return plugged_display_list, enumerated_displays


##
# @brief        Helper function for plugging a single display
# @param[in]    plugged_display - Connector port name of display to be plugged
# @param[in]    cmdline_args_dict - Command line arguments dictionary
# @param[in]    low_power_plug - True if low power, False otherwise
# @return       bool - True if Plug is successful, False otherwise
def plug_display(plugged_display, cmdline_args_dict, low_power_plug=False):
    dp_edid = 'DP_3011.EDID'
    dp_dpcd = 'DP_3011_dpcd.txt'
    hdmi_edid = 'HDMI_Dell_3011.EDID'
    __display_config = disp_cfg.DisplayConfiguration()

    ##
    # Get Plugged display parameter from command line
    plug_display_args = {}
    value = {}
    for key, value in cmdline_args_dict.items():
        if cmd_parser.display_key_pattern.match(key) is not None:
            connector_port_name = value['connector_port']
            if connector_port_name == plugged_display:
                plug_display_args[plugged_display] = value
                break

    if len(plug_display_args) == 0:
        logging.error("Invalid display {%s} parameter has passed" % cfg_enum.CONNECTOR_PORT_TYPE(plugged_display).name)
        return False

    connector_port = plug_display_args[plugged_display]['connector_port']
    if connector_port is not None and connector_port[:2] == 'DP':
        ## Assign default EDID if it is none
        if plug_display_args[plugged_display]['edid_name'] is not None:
            dp_edid = plug_display_args[plugged_display]['edid_name']

        ## Assign default DPCD if it is none
        if plug_display_args[plugged_display]['dpcd_name'] is not None:
            dp_dpcd = plug_display_args[plugged_display]['dpcd_name']

        logging.debug("Trying to plug %s with EDID :%s DPCD:%s " % (
            connector_port + "_" + value['connector_port_type'], dp_edid, dp_dpcd))
        if plug(plugged_display, dp_edid, dp_dpcd, low_power_plug, value['connector_port_type']) is False:
            return False

    if connector_port is not None and connector_port[:4] == 'HDMI':
        if plug_display_args[plugged_display]['edid_name'] is not None:
            hdmi_edid = plug_display_args[plugged_display]['edid_name']
        logging.debug(
            "Trying to plug %s with EDID:%s " % (connector_port + "_" + value['connector_port_type'], hdmi_edid))
        if plug(plugged_display, hdmi_edid, None, low_power_plug, value['connector_port_type']) is False:
            return False

    ##
    # Check Display enumeration only if plug is not in low power state
    if low_power_plug is False:
        enumerated_displays = __display_config.get_enumerated_display_info()

        if enumerated_displays is None:
            logging.error("Enumerated_displays is None")
            return False

        if disp_cfg.is_display_attached(enumerated_displays, plugged_display) is False:
            logging.error("Failed to plug %s", plugged_display)
            return False
        logging.debug("Enumerated Display Information: %s", enumerated_displays.to_string())

    return True


##
# @brief        Get Panel Type from VBT data
# @details      Pass VBT identifiable port name (from vbt_context.DVO_PORT_MAPPING key) and gfx_index in lower case
# @param[in]    port_name - connector port name
# @param[in]    gfx_index - Graphics Adapter Index
# @return       panel_type - VbtPanelType object, None if port not in VBT configuration
def get_vbt_panel_type(port_name: str, gfx_index: str) -> VbtPanelType:
    if port_name is None or not gfx_index.startswith('gfx_'):
        logging.error(f"Invalid parameter passed - port name {port_name}, gfx_index {gfx_index}")
        return None

    for display_device in Vbt(gfx_index).block_2.DisplayDeviceDataStructureEntry:
        if display_device.DeviceHandle <= 0 or display_device.DeviceClass == 0:
            continue

        if port_name[-1] != vbt_context.DVO_PORT_NAMES.get(display_device.DVOPort, None)[-1]:
            continue

        if display_device.DeviceClass in VbtPanelType.__members__.values():
            return VbtPanelType(display_device.DeviceClass)

    logging.error(f"Unable to find panel type for port name ({port_name}) on gfx_index ({gfx_index})")


##
# @brief        API to plug DFT panel
# @param[in]    port - connector port
# @param[in]    edid - panel's EDID to be simulated. Example: DP_3011.EDID
# @param[in]    dpcd - DPCD capability of the panel. Applicable for EDP or DP panels. Example: DP_3011_DPCD.txt
# @param[in]    is_low_power - True if panel to be plugged in Low Power state, False otherwise
# @param[in]    port_type - connector port type
# @param[in]    panelindex - Panel index from PanelInputData.xml
# @param[in]    is_lfp - True if LFP, False if EFP
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    dp_dpcd_model_data - model data containing DPCD transactions to be done (e.g link training transactions)
# @param[in]    dongle_type - Specifies the type of Dongle
# @param[in]    is_delay_required - Specifies the delay required
# @return       ret_val - True if plug is successful, False otherwise
def plug(port, edid=None, dpcd=None, is_low_power=False, port_type='NATIVE', panelindex=None, is_lfp=False,
         gfx_index='gfx_0', dp_dpcd_model_data=None, dongle_type: DongleType = None, is_delay_required = True):
    ret_val = False
    root_folder = None
    adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]

    simulation_type = env_settings.get('SIMULATION', 'simulation_type')
    if simulation_type is not None and simulation_type == 'MANUAL':
        if is_low_power:
            user_msg = "MANUAL MODE [MSG]: Plug display during sleep state to %s with EDID = %s and DPCD = %s" % (
                port, edid, dpcd)
            user_msg += "\nMANUAL MODE [CONFIRM]: Press enter to continue with the test\n"
            input(user_msg)
        else:
            user_msg = "MANUAL MODE [ACTION]: Plug display to %s with EDID = %s and DPCD = %s" % (port, edid, dpcd)
            user_msg += "\nMANUAL MODE [CONFIRM] After plugging, press enter...\n"
            input(user_msg)
        return True

    if simulation_type is not None and simulation_type == 'NONE':
        logging.info("Assuming display already plugged. So, skipping plug as simulation_type configured as NONE")
        return True

    # Verify if requested port is enabled in VBT.
    # we relay on is_lfp key during dual eDP simulation/plug call from prepare_display as VBT will not yet be
    # configured with EDP_B at that instance
    if port not in disp_cfg.get_supported_ports(gfx_index).keys() and not is_lfp:
        logging.warning("{} is not present in VBT supported port, hence plug failed".format(port + "_" + port_type))
        gdhm.report_bug(
            f"[DisplayUtilityLib] Plug request received with invalid port {port}_{port_type}",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
        return ret_val

    # Plug will use supplied EDID/DPCD.
    # If EDID is None:
    #   Retrieve EDID/DPCD data as per Index specified in Port (DP_A_EDP001),
    #       If index is not specified Retrieve EDID/DPCD data as per Default Index specified in PanelInputData.xml
    if (panelindex is not None) or (edid is None) or ('DP' in port and dpcd is None):
        input_data = get_panel_edid_dpcd_info(port=port, panel_index=panelindex, is_lfp=is_lfp)
        if input_data is None:
            return False
        else:
            edid = input_data['edid']
            dpcd = input_data['dpcd']
            panel_desc = input_data['desc']
    else:
        panel_desc = edid

    if 'HDMI' in port:
        if os.path.exists(os.path.join(TestContext.panel_input_data(), 'HDMI', edid)):
            root_folder = 'HDMI'
        else:
            logging.error("EDID File [{0}] not found in HDMI sub-folder of [{1}]".format(edid,
                                                                                         TestContext.panel_input_data()))
            return ret_val

    elif 'DP' in port:
        if os.path.exists(os.path.join(TestContext.panel_input_data(), 'eDP_DPSST', edid)):
            root_folder = 'eDP_DPSST'
        elif os.path.exists(os.path.join(TestContext.panel_input_data(), 'DP_MST_TILE', edid)):
            root_folder = 'DP_MST_TILE'
        else:
            logging.error("EDID File [{0}] not found in [eDP_DPSST \ DP_MST_TILE] sub-folder of [{1}]".format(
                edid, TestContext.panel_input_data()))
            return ret_val

    edid_path = os.path.join(TestContext.panel_input_data(), root_folder, edid)

    if 'HDMI' in port:
        dpcd_path = None
    else:
        dpcd_path = os.path.join(TestContext.panel_input_data(), root_folder, dpcd)
        if not os.path.exists(dpcd_path):
            logging.error("DPCD File Not Found : {0}".format(dpcd_path))
            return ret_val

    _driver_interface = driver_interface.DriverInterface()
    ret_val = _driver_interface.simulate_plug(adapter_info, port, edid_path, dpcd_path, is_low_power, port_type, is_lfp,
                                              dp_dpcd_model_data, dongle_type)

    # Delay to get the display enumerated after plug call.
    # Not required in low_power case since HPD happens during sleep
    if is_delay_required is True and is_low_power is False:
        time.sleep(10)

    # Printing Underrun Status after plug
    UnderRunStatus().verify_underrun()

    if ret_val:
        TestContextPersistence()._record_plugged_port(gfx_index, port, port_type)
        logging.info(
            "Plug of %s successful with low power=%s (Panel: %s)" % (port + "_" + port_type, is_low_power, panel_desc))
    else:
        logging.error(
            "Plug of %s failed with low power=%s (Panel: %s)" % (port + "_" + port_type, is_low_power, panel_desc))
        gdhm.report_bug(
            f"[DisplayUtilityLib] Failed to plug {port + '_' + port_type} with LowPower= {is_low_power}",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )

    return ret_val


##
# @brief        API to unplug DFT panel
# @param[in]    port - connector port
# @param[in]    is_low_power - True if panel to be unplugged is in Low Power state, False otherwise
# @param[in]    port_type - connector port type
# @param[in]    is_lfp - True if LFP, False if EFP
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    is_delay_required - Specifies the delay required
# @return       ret_value - True if unplug is successful, False otherwise
def unplug(port, is_low_power=False, port_type='NATIVE', is_lfp=False, gfx_index='gfx_0', is_delay_required = True):
    ret_val = False
    adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]

    simulation_type = env_settings.get('SIMULATION', 'simulation_type')
    if simulation_type is not None and simulation_type == 'MANUAL':
        if is_low_power:
            user_msg = "MANUAL MODE [MSG]: Unplug %s during S3/S4 cycle" % port
            user_msg += "\n MANUAL MODE [CONFIRM]: Press enter to continue with the test\n"
            input(user_msg)
        else:
            user_msg = "MANUAL MODE [ACTION]: UnPlug Display in Port %s now" % port
            user_msg += "\n MANUAL MODE [CONFIRM]: Press enter after display is plugged\n"
            input(user_msg)
            user_msg = "\n MANUAL MODE [ACTION]: Press enter to continue with the test"
            input(user_msg)
        return True

    if simulation_type is not None and simulation_type == 'NONE':
        logging.info("Skipping unplug as simulation_type configured as NONE")
        return True

    if port not in disp_cfg.get_supported_ports(gfx_index).keys():
        logging.warning("{} is not supported and hence cannot unplug".format(port + "_" + port_type))
        gdhm.report_bug(
            f"[DisplayUtilityLib] UnPlug request received with invalid port {port}_{port_type}",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
        return ret_val

    _driver_interface = driver_interface.DriverInterface()
    ret_val = _driver_interface.simulate_unplug(adapter_info, port, is_low_power, port_type)

    # Delay to get the display enumeration changes after unplug call
    # Not required in low_power case since HPD happens during sleep
    if is_delay_required is True and is_low_power is False:
        time.sleep(10)

    # Printing Underrun Status after UnPlug
    UnderRunStatus().verify_underrun()

    if ret_val:
        TestContextPersistence()._record_unplugged_port(gfx_index, port)
        logging.debug("UnPlug of %s successful with low power=%s" % (port + "_" + port_type, is_low_power))
    else:
        logging.error("UnPlug of %s failed with low power=%s" % (port + "_" + port_type, is_low_power))
        gdhm.report_bug(
            f"[DisplayUtilityLib] Failed to unplug {port + '_' + port_type} with LowPower= {is_low_power}",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
    return ret_val


##
# @brief        API to get Panel's EDID or DPCD specifications
# @param[in]    port - connector port
# @param[in]    panel_index - Panel index from PanelInputData.xml
# @param[in]    is_lfp - True if LFP, False if EFP
# @return       ret_info - Panel specifications dictionary, None otherwise
def get_panel_edid_dpcd_info(port=None, panel_index=None, is_lfp=False):
    ret_info = {}
    index_to_read = None
    platform_name = None
    xml_file = os.path.join(TestContext.panel_input_data(), "PanelInputData.xml")

    if os.path.isfile(xml_file):
        xml_root = ET.parse(xml_file).getroot()
    else:
        logging.error("FAIL: Panel Input XML file not found (Path: {0}).".format(xml_file))
        return None

    if panel_index is None:
        # Get Display hardware info list
        gfx_display_hwinfo = SystemInfo().get_gfx_display_hardwareinfo()
        # Get platform name from each display hardware info list.
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            platform_name = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).upper()
            break

        default_lfp_list = xml_root.find("DefaultPanelList").findall("PanelPlatform")
        for panel_platform in default_lfp_list:
            if panel_platform.attrib["Platform"].upper() == platform_name:
                if is_lfp:
                    index_to_read = panel_platform.attrib["EDP"]
                elif 'HDMI' in port:
                    index_to_read = panel_platform.attrib["HDMI"]
                else:
                    index_to_read = panel_platform.attrib["DP"]

        if index_to_read is None:
            logging.error("Default Panel Not Specified. Port: {0} Platform: {1}".format(panel_index, platform_name))
            return None
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
        logging.error("Invalid Panel Index : {0}".format(index_to_read))
        return None


##
# @brief        Generate possible permutation of display config using display list
# @param[in]    display_list - List of displays
# @param[in]    combination - True to get Combination list, False to get Permutation list
# @returns      possible_list - Possible config topology with connected displays list.
def get_possible_configs(display_list, combination=False):
    possible_list = {'enum.SINGLE': [],
                     'enum.CLONE': [],
                     'enum.EXTENDED': []
                     }

    display_permute_list = []
    for i in range(1, len(display_list) + 1):
        if combination:
            permute_list = (itertools.combinations(display_list, i))
        else:
            permute_list = (itertools.permutations(display_list, i))
        for new_config in permute_list:
            display_permute_list.append(list(new_config))

    for displays in display_permute_list:
        if len(displays) == 1:
            possible_list["enum.SINGLE"].append(displays)
        elif len(displays) > 1:
            possible_list["enum.CLONE"].append(displays)
            possible_list["enum.EXTENDED"].append(displays)

    return possible_list
