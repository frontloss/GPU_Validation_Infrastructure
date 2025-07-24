######################################################################################
# @file         test_header.py
# @brief        Python module to print test header and test footer
# @author       Amit Sau
######################################################################################
import datetime
import logging
import os
from concurrent import futures
from typing import Tuple, List

from Libs.Core import reboot_helper, driver_escape
from Libs.Core import system_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import display_logger
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.wrapper import driver_escape_args

QUICK_BUILD_VERSION = 'version.txt'
DEFAULT_LINE_WIDTH = 172


##
# @brief        Formatted Line separator
# @param[in]    separator - filler symbol
# @param[in]    width - line width
# @return       str - Separator formatted line
def formatted_line_separator(separator: str = "=", width: int = DEFAULT_LINE_WIDTH) -> str:
    return "|" + (separator * (width + 1)) + "|" + "\n"


##
# @brief        Format Line
# @param[in]    string - String to be formatted
# @param[in]    width - line width
# @return       str - String formatted line
def format_line(string: str, width: int = DEFAULT_LINE_WIDTH) -> str:
    return "| " + '{0: <{width}}'.format(string, width=width) + "|" + "\n"


##
# @brief        Get configuration data
# @return       config_data - Display configuration details
def __get_config_data() -> str:
    config = display_config.DisplayConfiguration()
    config_data = None
    current_config, displays, display_and_adapter_info_list = config.get_current_display_configuration_ex()
    if current_config is not None and 'DispNone' not in displays:

        config_data = 'Topology - ' + current_config
        enum_displays = config.get_enumerated_display_info()
        mode_data = ''
        for eachDisplay in range(len(displays)):  # display in displays:
            port_name = displays[eachDisplay]
            gfx_index = display_and_adapter_info_list[eachDisplay].adapterInfo.gfxIndex
            mode_details = config.get_current_mode(
                config.get_target_id(port_name, enum_displays, gfx_index))
            mode_data = mode_data + gfx_index + ':' + port_name + '[' + str(mode_details.HzRes) + " x " + str(
                mode_details.VtRes) + "@" + str(mode_details.refreshRate) + ']' + ' '
        config_data = config_data + ', ' + mode_data
    return config_data


##
# @brief        Prints adapter Information
# @param[in]    driver_info - EnumeratedDrivers object
# @return       ret_string - Formatted Adapter information
def __print_adapter_information(driver_info: machine_info.EnumeratedDrivers) -> str:
    ret_string = ""
    for driver_count in range(driver_info.Count):
        display_driver_info = driver_info.DriverInfo[driver_count]
        bus_instance_id = "{0}\\{1}".format(display_driver_info.BusDeviceID, display_driver_info.DeviceInstanceID)
        gfx_adapter_name = str(display_driver_info.DriverDescription).split(',')
        ret_string += format_line("{0:18} {1:<16} [{2}] {3}".format("Adapter-{} ".format(driver_count + 1),
                                                                    display_driver_info.DriverVersion,
                                                                    display_driver_info.Status, bus_instance_id +
                                                                    " : " +
                                                                    gfx_adapter_name[len(gfx_adapter_name) - 1]))
    return ret_string


##
# @brief        Print device Info
# @param[in]    device_info - EnumeratedDrivers object
# @param[in]    device_name - Device driver name
# @return       ret_string - Formatted device info
def __print_device_info(device_info: machine_info.EnumeratedDrivers, device_name: str) -> str:
    ret_string = ""
    audio_string = ""
    device_found = []
    if device_info is None:
        ret_string += format_line("{0:18} {1:<16} [{2:^7}] {3}".format(
            device_name, 'None', 'None', '{} NOT Installed'.format(device_name)))
    else:
        count = 0
        for driver_count in range(device_info.Count):
            each_device_info = device_info.DriverInfo[driver_count]
            if "High Definition Audio Device" in device_name:
                if len(audio_string) == 0:
                    device_found.append(False)
                    audio_string += format_line(
                        "{0:18} {1:<16} [{2:^7}] {3}".format(device_name, 'None', 'None', '{} NOT Installed'.
                                                             format(device_name)))
                continue
            ret_string += format_line("{0:18} {1:<16} [{2}] {3} {4}".format(device_name + "-{}".format(count + 1),
                                                                            each_device_info.DriverVersion,
                                                                            each_device_info.Status,
                                                                            each_device_info.BusDeviceID + " : ",
                                                                            device_name))
            count = count + 1
            device_found.append(True)
        if True not in device_found:
            ret_string += audio_string
    return ret_string


##
# @brief        Helper API to invoke APIs to run in parallel
# @param[in]    task - Tuple data (identifier name, method name, method parameter)
# @return       (str, object) - (identifier name, output data)
def __preamble_runner(task: Tuple[str, any, any]) -> Tuple[str, any]:
    # Call methods based on parameter.
    # If method parameter is None call task[1](), else call task[1](task[2])
    return (task[0], task[1]()) if task[2] is None else (task[0], task[1](task[2]))


##
# @brief        Calls get_misc_system_info escape
# @details      Default value is 'gfx_0' for handling Single Adapter Case
# @return       misc_system_info - MiscEscGetSystemInfoArgs object
def __get_system_info() -> driver_escape_args.MiscEscGetSystemInfoArgs:
    gfx_index = 'gfx_0'
    escape_status, misc_system_info = driver_escape.get_misc_system_info(gfx_index)
    if escape_status is False:
        logging.error('Escape Call failed to get System Info')
    return misc_system_info


##
# @brief        Initialize test header data
# @param[in]    cmdline_args - Command Line Arguments
# @return       None
def initialize(cmdline_args: List[str] = None) -> None:
    if reboot_helper.is_reboot_scenario() is True:
        return

    preamble = "\n"
    preamble += formatted_line_separator()
    preamble += format_line("TEST ENVIRONMENT DETAILS")
    preamble += formatted_line_separator()
    now = datetime.datetime.now()

    preamble += format_line("Execution Start: %s" % now.strftime("%d %B %Y %H:%M:%S %p"))
    if cmdline_args:
        working_path = "Working Path: %s" % os.path.dirname(os.path.abspath(cmdline_args[0]))
        preamble += format_line(working_path)
        cmd_param_str = " ".join(cmdline_args)
        preamble += format_line("Command Line Parameters: %s" % cmd_param_str)
    else:
        preamble += format_line("Command Line Parameters: NO ARGUMENTS")
        preamble += formatted_line_separator()

    preamble += format_line("Display Automation Binary Version : %s" % get_binary_version())

    preamble += formatted_line_separator()
    execution_env = 'Pre-Si' \
        if system_utility.SystemUtility().get_execution_environment_type() in ['SIMENV_FULSIM', 'SIMENV_PIPE2D'] \
        else 'Post-Si'
    preamble += format_line("{0:^25}: {1}".format("Environment", execution_env))

    obj_machine_info = machine_info.SystemInfo()

    tasks = [
        ('system_info', obj_machine_info._get_system_info, None),
        ('misc_info', __get_system_info, None),
        ('config_data', __get_config_data, None),
        ('display_driver_info', obj_machine_info.get_driver_info, machine_info.SystemDriverType.GFX),
        ('audio_driver_info', obj_machine_info.get_driver_info, machine_info.SystemDriverType.AUDIO),
        ('valsim_driver_info', obj_machine_info.get_driver_info, machine_info.SystemDriverType.VALSIM),
    ]

    with futures.ThreadPoolExecutor(max_workers=8) as executor:
        for output in executor.map(__preamble_runner, tasks):
            if output[0] == 'system_info':
                for info in output[1]:
                    preamble += format_line(info)
            if output[0] == 'misc_info':
                misc_sys_info = output[1]
                if misc_sys_info is None or len(misc_sys_info.get_gop_version().strip()) == 0:
                    preamble += format_line("{0:^25}: {1}".format("GOP/VBIOS Version", "None"))
                    gdhm.report_bug(
                        f"[TestHeader] : Invalid GOP version retrieved from driver escape call",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES,
                        gdhm.Priority.P4
                    )
                else:
                    preamble += format_line("{0:^25}: {1}".format("GOP/VBIOS Version", misc_sys_info.get_gop_version()))
            if output[0] == 'config_data':
                preamble += format_line("{0:^25}: {1}".format("Display Config & Mode", output[1]))

                platform_info = obj_machine_info.get_gfx_display_hardwareinfo()
                for i in range(len(platform_info)):
                    gfx_index = str(platform_info[i].gfxIndex)
                    supported_ports = display_config.get_supported_ports(gfx_index=gfx_index)
                    preamble += format_line(
                        "{0:^18}-{1} : {2} [{3}] [{4}]".format("Platform", platform_info[i].gfxIndex,
                                                               platform_info[i].DisplayAdapterName,
                                                               platform_info[i].SkuName, platform_info[i].SkuConfig))
                    if len(supported_ports) == 0:
                        preamble += format_line("{0:^25}: {1}".format("Enabled_Ports", "None"))
                    else:
                        preamble += format_line("{0:^18}-{1} : {2}".format("Enabled Ports",
                                                                           gfx_index, supported_ports))

            if output[0] == 'display_driver_info':
                driver_info = output[1]

                platform_info = obj_machine_info.get_platform_details(driver_info.DriverInfo[0].DeviceID)
                line = "{0:^25}: {1} [{2}] [{3}]".format("Platform", platform_info.PlatformName,
                                                         platform_info.SkuConfig,
                                                         platform_info.SkuName)
                preamble += format_line(line)

                preamble += format_line("{0:^25}: {1}".format("No. of Display Adapters", driver_info.Count))
                preamble += formatted_line_separator(width=DEFAULT_LINE_WIDTH)
                header = "{0:18} {1:<16} {2:<9} {3}".format("Service", "Version", "State", "Details & Description")
                preamble += format_line(header)
                preamble += formatted_line_separator(separator="-", width=DEFAULT_LINE_WIDTH)
                preamble += __print_adapter_information(driver_info)

            if output[0] == 'audio_driver_info':
                preamble += __print_device_info(output[1], 'Audio')

            if output[0] == 'valsim_driver_info':
                preamble += __print_device_info(output[1], 'GfxValSimDriver')

    preamble += formatted_line_separator(width=DEFAULT_LINE_WIDTH)

    preamble += "\n\n"
    preamble += formatted_line_separator()
    preamble += format_line("TEST SCRIPT EXECUTION START")
    preamble += formatted_line_separator()

    # print platform details on command prompt
    print(preamble)

    file_handle, log_file_path = display_logger._get_file_handle()
    # Python logging FileHandle class will have attribute named baseFilename which stores log file name
    with open(file_handle.baseFilename, 'w') as log_file:
        log_file.write(preamble)


##
# @brief        Get Display Automation binary version
# @return       binary_version - Returns binary version as formatted string
def get_binary_version() -> str:
    binary_version = ""
    if os.path.isfile(QUICK_BUILD_VERSION):
        with open(QUICK_BUILD_VERSION) as f:
            binary_version = f.readline().strip()
    return binary_version
