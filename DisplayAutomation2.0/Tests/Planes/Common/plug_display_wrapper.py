########################################################################################################################
# @file         plug_display_wrapper.py
# @brief        The script contains a wrapper function to plug a single display.
# @author       Shetty, Anjali N
########################################################################################################################
import logging

from Libs.Core import cmd_parser, display_utility
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE

display_config = disp_cfg.DisplayConfiguration()


##
# @brief            Helper function for plugging a single display
# @param[in]        plugged_display; Display interface which need to connect
# @param[in]        cmdline_args_dict; Command line dictionary
# @param[in]        low_power_plug; True, if the plug is in low power; False, otherwise
# @return           Return False if display is already plugged and enumerated else True
def plug_display(plugged_display, cmdline_args_dict, low_power_plug=False):
    dp_edid = 'DP_3011.EDID'
    dp_dpcd = 'DP_3011_dpcd.txt'
    hdmi_edid = 'HDMI_Dell_3011.EDID'
    display_list_before_plug = []

    enum_displays_before_plug = display_config.get_enumerated_display_info()
    for index in range(enum_displays_before_plug.Count):
        display = CONNECTOR_PORT_TYPE(enum_displays_before_plug.ConnectedDisplays[index].ConnectorNPortType).name
        display_list_before_plug.insert(index, display)

    if plugged_display in display_list_before_plug:
        logging.error("Display %s is already plugged and enumerated" % plugged_display)
        return False

    ##
    # Get Plugged display parameter from command line
    plug_display_args = {}
    value = ""
    for key, value in cmdline_args_dict.items():
        if cmd_parser.display_key_pattern.match(key) is not None:
            connector_port_name = value['connector_port']
            if connector_port_name == plugged_display:
                plug_display_args[key] = value
                break

    if len(plug_display_args) == 0:
        logging.error("Invalid display {%s} parameter has passed" % CONNECTOR_PORT_TYPE(plugged_display).name)
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
        if display_utility.plug(plugged_display, dp_edid, dp_dpcd, low_power_plug, value['connector_port_type'],
                                gfx_index=value['gfx_index'].lower()) is False:
            return False

    if connector_port is not None and connector_port[:4] == 'HDMI':
        if plug_display_args[plugged_display]['edid_name'] is not None:
            hdmi_edid = plug_display_args[plugged_display]['edid_name']
        logging.debug(
            "Trying to plug %s with EDID:%s " % (connector_port + "_" + value['connector_port_type'], hdmi_edid))
        if display_utility.plug(plugged_display, hdmi_edid, None, low_power_plug, value['connector_port_type'],
                                gfx_index=value['gfx_index'].lower()) is False:
            return False

    ##
    # Check Display enumeration only if plug is not in low power state
    if low_power_plug is False:
        enumerated_displays = display_config.get_enumerated_display_info()

        if enumerated_displays is None:
            logging.error("Enumerated_displays is None")
            return False

        if disp_cfg.is_display_attached(enumerated_displays, plugged_display,
                                        value['gfx_index'].lower()) is False:
            logging.error("Failed to plug %s", plugged_display)
            return False
        logging.debug("Enumerated Display Information: %s", enumerated_displays.to_string())

    return True
