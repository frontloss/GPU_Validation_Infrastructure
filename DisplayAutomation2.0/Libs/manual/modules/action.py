###################################################################################################################
# @file         action.py
# @addtogroup   NorthGate
# @brief        Common actions which test can ask user to perform manually.
# @description  This file contains the implementation of common actions which can be performed manually by user. Below
#               actions are exposed by this module:
#               1. plug()
#               Plug action is used to ask user to connect/plug a panel manually.
#
#               2. unplug()
#               Unplug action is used to ask user to disconnect/unplug a panel manually.
#
# @todo         Add change_display_config() action
# @todo         Add timeout for each action
#
# @author       Rohit Kumar
###################################################################################################################

import logging

from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.manual.modules import alert


##
# @brief        Asks user to plug the given display manually
# @param[in]    display, display name which will be show to user
# @return       True if plug action is successful, False otherwise
def plug(display):
    current_active_ports = []
    current_active_displays = []
    new_active_ports = []
    new_active_displays = []
    display_config_ = display_config.DisplayConfiguration()

    logging.info("Plugging {0} panel".format(display))
    enumerated_displays = display_config_.get_enumerated_display_info()
    for display_index in range(enumerated_displays.Count):
        _display = enumerated_displays.ConnectedDisplays[display_index]
        current_active_ports.append(cfg_enum.CONNECTOR_PORT_TYPE(_display.ConnectorNPortType).name)
        current_active_displays.append(_display.FriendlyDeviceName)
    current_display_count = enumerated_displays.Count
    new_display_count = current_display_count
    while new_display_count <= current_display_count:
        new_active_ports = []
        new_active_displays = []

        alert.info('Plug ' + display + ' panel \n\n\n Press OK after plugging the panel')
        enumerated_displays = display_config_.get_enumerated_display_info()
        for display_index in range(enumerated_displays.Count):
            _display = enumerated_displays.ConnectedDisplays[display_index]
            new_active_ports.append(cfg_enum.CONNECTOR_PORT_TYPE(_display.ConnectorNPortType).name)
            new_active_displays.append(_display.FriendlyDeviceName)
        new_display_count = enumerated_displays.Count
        if new_display_count <= current_display_count:
            retry = alert.warning("Plugging of {0} panel failed. Do you want to try plugging "
                                  "{0} panel again?".format(display), alert_type=alert.AlertTypes.confirm)
            logging.warning("\tPlugging of {0} panel failed".format(display))
            if retry is False:
                logging.error("\tFailed to plug {0} panel".format(display))
                return False
            else:
                logging.warning("\tTrying to plug again")

    ##
    # @todo select new_active_port and new_active_display based on target id
    # new_active_port = list(set(new_active_ports) - set(current_active_ports))
    # if len(new_active_port) != 1:
    #     return False
    # new_active_port = new_active_port[0]
    # new_active_display = list(set(new_active_displays) - set(current_active_displays))
    # if len(new_active_display) != 1:
    #     return False
    # new_active_display = new_active_display[0]
    # logging.info("\tPlugged the {0} panel on {1} port successfully".format(new_active_display, new_active_port))
    logging.info("\tPlugged the {0} panel successfully".format(display))
    return True


##
# @brief        Asks user to unplug the given display manually
# @param[in]    display, display name which will be show to user
# @return       True if unplug action is successful, False otherwise
def unplug(display=None):
    current_active_ports = []
    current_active_displays = []
    new_active_ports = []
    new_active_displays = []
    display_config_ = display_config.DisplayConfiguration()

    if display is None:
        display = "External"
    logging.info("UnPlugging {0} panel".format(display))
    enumerated_displays = display_config_.get_enumerated_display_info()
    for display_index in range(enumerated_displays.Count):
        _display = enumerated_displays.ConnectedDisplays[display_index]
        current_active_ports.append(cfg_enum.CONNECTOR_PORT_TYPE(_display.ConnectorNPortType).name)
        current_active_displays.append(_display.FriendlyDeviceName)
    current_display_count = enumerated_displays.Count
    new_display_count = current_display_count
    while new_display_count >= current_display_count:
        alert.info('UnPlug ' + display + ' panel \n\n\n Press OK after unplugging the panel')
        enumerated_displays = display_config_.get_enumerated_display_info()
        for display_index in range(enumerated_displays.Count):
            _display = enumerated_displays.ConnectedDisplays[display_index]
            new_active_ports.append(cfg_enum.CONNECTOR_PORT_TYPE(_display.ConnectorNPortType).name)
            new_active_displays.append(_display.FriendlyDeviceName)
        new_display_count = enumerated_displays.Count
        if new_display_count >= current_display_count:
            retry = alert.warning("UnPlugging of {0} panel failed. Do you want to try unplugging "
                                  "{0} panel again?".format(display), alert_type=alert.AlertTypes.confirm)
            logging.warning("\tUnPlugging of {0} panel failed".format(display))
            if retry is False:
                logging.error("\tFailed to UnPlug {0} panel".format(display))
                return False
            logging.warning("\tTrying to unplug again")

    ##
    # @todo select new_active_port and new_active_display based on target id
    # new_active_port = list(set(current_active_ports) - set(new_active_ports))
    # if len(new_active_port) != 1:
    #     return False
    # unplugged_port = new_active_port[0]
    # new_active_display = list(set(current_active_displays) - set(new_active_displays))
    # if len(new_active_display) != 1:
    #     return False
    # unplugged_display = new_active_display[0]
    # logging.info("\tUnPlugged the {0} panel from {1} port successfully".format(unplugged_display, unplugged_port))
    logging.info("\tUnPlugged the {0} panel successfully".format(display))
    return True
