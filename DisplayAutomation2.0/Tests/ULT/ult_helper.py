###############################################################################
# @file      ult_helper.py
# @brief     This script try all possible Plug and UnPlug on the target machine
# @author    Beeresh
###############################################################################


import os, sys, time
import logging

import win32con

from Libs.Core import display_essential
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import *
from Libs.Core.display_config.display_config import *
from Libs.Core.system_utility import *
from Libs.Core.display_utility import *



'''
WARM_UP required only for GTA environment. 
 Due to multiple power cycles, heart beat of DUT has not reached runner within expected time frame and GTA Runner 
 interpret DUT unreacheable and aborts JOB. 
'''
POWER_CYCLE_WARM_UP_TIME = 120

'''
Duration in seconds DUT will be in specified power state
'''
POWER_CYCLE_DURATION = 10


def do_nothing():
    logging.info("Sleep for 5 seconds")
    time.sleep(5)


def goto_powerstate_s3():
    disp_power = DisplayPower()
    ret = disp_power.invoke_power_event(PowerEvent.S3, POWER_CYCLE_DURATION)
    time.sleep(POWER_CYCLE_WARM_UP_TIME)
    return ret


def goto_powerstate_s4():
    disp_power = DisplayPower()
    ret = disp_power.invoke_power_event(PowerEvent.S4, POWER_CYCLE_DURATION)
    time.sleep(120)
    return ret


def monitor_turnoff():
    disp_power = DisplayPower()
    ret = disp_power.invoke_monitor_turnoff(MonitorPower.OFF_ON, POWER_CYCLE_DURATION)
    if ret:
        win32api.keybd_event(win32con.VK_ESCAPE, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        logging.info("Wake-up machine using key press event successful !!")
    time.sleep(120)
    return ret


def get_current_displays():
    config = DisplayConfiguration()
    enumerated_displays = config.get_enumerated_display_info()
    return enumerated_displays


def get_supported_external_ports():
    supported_ports = get_supported_ports()
    external_ports = [port_name for port_name in supported_ports if '_A' not in port_name.upper()]
    return external_ports


def get_hdmi_ports():
    ports = get_supported_external_ports()
    hdmi_ports = [port for port in ports if "HDMI_" in port.upper()]
    return hdmi_ports


def get_dp_ports():
    ports = get_supported_external_ports()
    dp_ports = [port for port in ports if "DP_" in port.upper()]
    return dp_ports


def get_external_free_ports():
    free_ports = get_free_ports()
    external_ports = [port_name for port_name in free_ports if '_A' not in port_name.upper()]
    return external_ports


def get_port_targetid_mapping(reverse: bool, gfx_index: str = 'gfx_0') -> dict:
    enumerated_displays = DisplayConfiguration().get_enumerated_display_info()
    target_id_mapping = dict()

    for display_index in range(enumerated_displays.Count):
        display = enumerated_displays.ConnectedDisplays[display_index]
        if gfx_index == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
            if reverse:
                target_id_mapping[int(display.TargetID)] = CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name
            else:
                target_id_mapping[CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name] = int(display.TargetID)

    return target_id_mapping


def get_modes(port_name):
    port_and_targetid = get_port_targetid_mapping(reverse=False)
    port_target_id = port_and_targetid[port_name]
    target_list = [port_target_id]
    cfg = DisplayConfiguration()
    port_and_targetid = get_port_targetid_mapping(reverse=True)
    target_list = port_and_targetid.keys()
    modes = cfg.get_all_supported_modes(target_list)
    port_modes = modes[port_target_id]
    return port_modes


def restart_gfxdriver(delay=10):
    status, reboot_required = display_essential.restart_gfx_driver()
    time.sleep(delay)