##
# @file         sharpness_helper.py
# @brief        This script contains helper functions to support sharpness test scripts
# @author       Prateek Joshi

import ctypes
import logging
import os
import sys
from enum import IntEnum

from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_power import DisplayPower, PowerSource
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import control_api_args
from Libs.Core.wrapper import control_api_wrapper


##
# @brief            Feature Status Enable / Disable Sharpness
class Status(IntEnum):
    DISABLE = 0
    ENABLE = 1


##
# @brief            Enable / Disable Sharpness feature through IGCL
# @param[in]        strength            : Intensity of Sharpness
# @param[in]        panel               : Panel Info
# @param[in]        select_filter_type  : Filter type - Adaptive / Non-Adaptive
# @param[in]        enable_disable      : Enable / Disable feature
# @return           status              : True if operation is successful, else False
def enable_disable_feature_igcl(strength, panel, select_filter_type, enable_disable):
    filter_type = (
        control_api_args.ctl_sharpness_filter_type_flags_t.NON_ADAPTIVE.value
        if select_filter_type.upper() == "NON_ADAPTIVE"
        else control_api_args.ctl_sharpness_filter_type_flags_t.ADAPTIVE.value
    )

    set_sharpness = control_api_args.ctl_sharpness_settings()
    set_sharpness.Size = ctypes.sizeof(set_sharpness)
    set_sharpness.FilterType = filter_type
    set_sharpness.Enable = enable_disable
    set_sharpness.Intensity = float(strength)

    if control_api_wrapper.set_sharpness(set_sharpness, panel.target_id):
        logging.info(f"Set Sharpness Passed via IGCL - Intensity: {set_sharpness.Intensity}")
    else:
        logging.error("Set Sharpness Failed via IGCL - Sharpness Enable: {0} Intensity: {1} FilterType: {2}"
                      .format(set_sharpness.Enable, set_sharpness.Intensity, set_sharpness.FilterType))
        report_to_gdhm("Set Sharpness Failed via IGCL - Sharpness Enable: {0} Intensity: {1} FilterType: {2}"
                       .format(set_sharpness.Enable, set_sharpness.Intensity, set_sharpness.FilterType))
        return False
    return True


##
# @brief        Helper function to get the display configuration
# @param[in]    connected_port_list : List of connected port
# @param[in]    enumerated_displays : Enumerated displays
# @return       Port config
def get_display_configuration(connected_port_list, enumerated_displays):
    config = DisplayConfiguration()
    port_config_str = ""
    for each_port in connected_port_list:
        target_id = config.get_target_id(each_port, enumerated_displays)
        mode = config.get_current_mode(target_id)
        port_config_str = port_config_str + "\n" + mode.to_string(enumerated_displays)
    return port_config_str


##
# @brief        Helper function to get the action type from commandline
# @param[in]    argument : Action Argument
# @return       argument value
def get_action_type(argument):
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if argument in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == argument:
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        raise Exception("Incorrect command line")


##
# @brief        Helper function to get config type
# @param[in]    argument : Command line tag
# @return       value    : Argument value
def get_config_type(argument):
    tag_list = [custom_tag.strip().upper() for custom_tag in sys.argv]
    if argument in tag_list:
        for i in range(0, len(tag_list)):
            if tag_list[i] == argument:
                if str(tag_list[i + 1]).startswith("-") is False:
                    return sys.argv[i + 1]
    else:
        raise Exception("Incorrect command line")


##
# @brief        Helper function to start ETL capture
# @param[in]    file_name : Name of the File
# @return       status    : Value indicating the result of the start_etl_tracer
def start_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"

    file_name = file_name + '.etl'
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start Gfx Tracer")
    return True


##
# @brief        Helper function to stop ETL capture
# @param[in]    file_name     : Name of the File to stop ETL Capture
# @return       etl_file_path : Path of ETL file captured
def stop_etl_capture(file_name):
    assert etl_tracer.stop_etl_tracer(), "Failed to Stop GfxTrace"
    etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE

    file_name = file_name + '.etl'
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    if etl_tracer.start_etl_tracer() is False:
        logging.error("Failed to Start GfxTrace after playback")
    return etl_file_path


##
# @brief        Helper function to switch between AC/DC mode
# @param[in]    flag : True for DC and False for AC mode
# @return       None
def ac_dc_switch(flag):
    display_power = DisplayPower()
    display_power.enable_disable_simulated_battery(flag)
    power_type = PowerSource.DC if flag is True else PowerSource.AC

    if display_power.set_current_powerline_status(power_type) is False:
        report_to_gdhm(f"Failed to set the power line status to {'DC' if flag is True else 'AC'}",
                       driver_bug=False)
        return False
    else:
        return True


##
# @brief            Helper function to report GDHM
# @param[in]        title      : GDHM title
# @param[in]        priority   : Priority of the GDHM bug [P1/P2/P3/P4]
# @param[in]        driver_bug : True for driver bug reporting else False
# @return           None
def report_to_gdhm(title, priority='P2', driver_bug=True):
    if driver_bug:
        gdhm.report_driver_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))
    else:
        gdhm.report_test_bug_os(title=title, priority=eval(f"gdhm.Priority.{priority}"))

