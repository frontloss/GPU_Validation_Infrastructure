#######################################################################################################################
# @file         windows_brightness.py
# @brief        @ref windows_brightness.py provides following APIs: <br>
# @details      Contains functions to get, set and change brightness
#
# @author       Rohit Kumar
#######################################################################################################################

import logging
import subprocess
import time

from Libs.Core import display_power, enum

GUID_POWER_SCHEME_BALANCED = "SCHEME_BALANCED"
GUID_POWER_SCHEME_POWER_SAVER = "SCHEME_MAX"
GUID_POWER_SCHEME_HIGH_PERFORMANCE = "SCHEME_MIN"
GUID_SUBGROUP_DISPLAY = "SUB_VIDEO"
GUID_TURN_OFF_DISPLAY_AFTER = "VIDEOIDLE"
GUID_DISPLAY_BRIGHTNESS = "aded5e82-b909-4619-9949-f5d71dac0bcb"
GUID_DIMMED_DISPLAY_BRIGHTNESS = "f1fbfde2-a960-4165-9f88-50667911ce96"
GUID_ENABLE_ADAPTIVE_BRIGHTNESS = "ADAPTBRIGHT"


##
# @brief        Internal function to parse WMI query and powercfg output
# @param[in]    power_cfg_query_output
# @return       output_list list
def __parse_power_cfg_info(power_cfg_query_output):
    output_list = []
    output_dict = dict()

    for line in power_cfg_query_output.splitlines():
        if ":" in line:
            row = line.split(":")
            if len(row) == 2:
                key = row[0].strip()
                value = row[1].strip()

                if key in output_dict.keys():
                    output_list.append(output_dict)
                    output_dict = dict()

                output_dict[key] = value
    if len(output_dict.keys()):
        output_list.append(output_dict)
    return output_list


##
# @brief        Exposed API to get the current brightness
# @return       brightness level in percentage (Ex: 50) if operation is successful, None otherwise
def get_current_brightness():
    ##
    # WMI query to get current brightness
    output = subprocess.check_output(['powershell.exe', "Get-Ciminstance",
                                      "-Namespace", "root/WMI",
                                      "-ClassName", "WmiMonitorBrightness"], universal_newlines=True)
    if output == '':
        return None
    brightness_info = __parse_power_cfg_info(output)
    if len(brightness_info) == 0:
        return None
    brightness_info = brightness_info[0]
    if 'CurrentBrightness' in brightness_info.keys():
        return int(brightness_info['CurrentBrightness'])
    return None


##
# @brief        Exposed API to get brightness levels
# @return       number of available brightness levels (Ex: 101 (0 to 100)) if operation is successful, None otherwise
def get_brightness_levels():
    ##
    # WMI query to get available brightness levels
    output = subprocess.check_output(['powershell.exe', "Get-Ciminstance",
                                      "-Namespace", "root/WMI",
                                      "-ClassName", "WmiMonitorBrightness"], universal_newlines=True)
    if output == '':
        return None
    brightness_info = __parse_power_cfg_info(output)
    if len(brightness_info) == 0:
        return None
    brightness_info = brightness_info[0]
    if 'Levels' in brightness_info.keys():
        return int(brightness_info['Levels'])
    return None


##
# @brief        Exposed API to set current brightness
# @param[in]    brightness_level
# @param[in]    delay_in_seconds time in seconds to wait before setting new brightness level
# @return       status, True if operation is successful, False otherwise
def set_current_brightness(brightness_level, delay_in_seconds=0):
    ##
    # WMI query to set current brightness_level
    subprocess.check_output(["powershell.exe",
                             "$query=Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods;",
                             "$query.wmisetbrightness({0}, {1})".format(delay_in_seconds, brightness_level)],
                            universal_newlines=True)

    ##
    # If delay_in_seconds is not 0, wait for given time for verification
    if delay_in_seconds != 0:
        time.sleep(delay_in_seconds + 1)

    ##
    # Verify the current brightness_level
    current_brightness_level = get_current_brightness()
    if current_brightness_level == brightness_level:
        return True
    return False


##
# @brief        Exposed API to increase or decrease brightness by given levels
# @param[in]    brightness_levels number of levels by which brightness will be increased or decreased.
#               Valid brightness levels range is -max_levels to +max_levels (given by get_brightness_levels() API)
# @return       status, True if operation is successful, False otherwise
def change_current_brightness(brightness_levels):
    ##
    # return True if current brightness is already 0 (minimum)
    current_brightness_level = get_current_brightness()
    if current_brightness_level == 0 and brightness_levels < 0:
        return False

    ##
    # return False if number of available brightness brightness_levels is less than 2
    max_brightness_levels = get_brightness_levels()
    if max_brightness_levels < 2:
        logging.warning("Not enough brightness brightness_levels ({0})".format(brightness_levels))
        return False

    if brightness_levels < 0:
        if current_brightness_level + brightness_levels < 0:
            return False
    else:
        if current_brightness_level + brightness_levels > max_brightness_levels:
            return False

    return set_current_brightness(current_brightness_level + brightness_levels)


##
# @brief        Exposed API to get OS brightness setting
# @param[in]    power_source_ac_or_dc AC/DC
# @param[in]    os_power_plan BALANCED/POWER_SAVER/HIGH_PERFORMANCE
# @return       power_plan_brightness_level
def get_power_plan_brightness(power_source_ac_or_dc, os_power_plan):
    if power_source_ac_or_dc == display_power.PowerSource.INVALID:
        logging.error("Invalid powerline status")
        return None

    if os_power_plan == display_power.PowerScheme.UNDEFINED:
        logging.error("Invalid os power plan")
        return None

    power_cfg_query = []
    power_plan_brightness_level = None

    ##
    # Set powercfg.exe parameters to get brightness setting for given power source and OS power plan
    if os_power_plan == display_power.PowerScheme.POWER_SAVER:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_POWER_SAVER, GUID_SUBGROUP_DISPLAY,
                           GUID_DISPLAY_BRIGHTNESS]
    elif os_power_plan == display_power.PowerScheme.BALANCED:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_BALANCED, GUID_SUBGROUP_DISPLAY,
                           GUID_DISPLAY_BRIGHTNESS]
    elif os_power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_HIGH_PERFORMANCE, GUID_SUBGROUP_DISPLAY,
                           GUID_DISPLAY_BRIGHTNESS]

    power_cfg_output = subprocess.check_output(power_cfg_query, universal_newlines=True)
    if power_cfg_output == '':
        return None
    brightness_info = __parse_power_cfg_info(power_cfg_output)
    if len(brightness_info) == 0:
        return None
    brightness_info = brightness_info[-1]
    if power_source_ac_or_dc == display_power.PowerSource.AC:
        if 'Current AC Power Setting Index' in brightness_info.keys():
            power_plan_brightness_level = int(brightness_info['Current AC Power Setting Index'], 16)
        else:
            logging.error("Brightness level is NOT present in powercfg.exe query output")
            return None
    elif power_source_ac_or_dc == display_power.PowerSource.DC:
        if 'Current DC Power Setting Index' in brightness_info.keys():
            power_plan_brightness_level = int(brightness_info['Current DC Power Setting Index'], 16)
        else:
            logging.error("Brightness level is NOT present in powercfg.exe query output")
            return None

    return power_plan_brightness_level


##
# @brief        Exposed API to set OS brightness setting
# @param[in]    power_source_ac_or_dc AC/DC
# @param[in]    os_power_plan BALANCED/POWER_SAVER/HIGH_PERFORMANCE
# @param[in]    power_plan_brightness_level
# @return       status, True if operation is successful, False otherwise
def set_power_plan_brightness(power_source_ac_or_dc, os_power_plan, power_plan_brightness_level):
    if power_source_ac_or_dc == display_power.PowerSource.INVALID:
        logging.error("Invalid powerline status")
        return None

    if os_power_plan == display_power.PowerScheme.UNDEFINED:
        logging.error("Invalid os power plan")
        return None

    power_cfg_query = []
    power_scheme = None

    ##
    # Set power scheme GUID
    if os_power_plan == display_power.PowerScheme.POWER_SAVER:
        power_scheme = GUID_POWER_SCHEME_POWER_SAVER
    elif os_power_plan == display_power.PowerScheme.BALANCED:
        power_scheme = GUID_POWER_SCHEME_BALANCED
    elif os_power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        power_scheme = GUID_POWER_SCHEME_HIGH_PERFORMANCE

    ##
    # Set powercfg.exe parameters to set power_plan_brightness_level setting for given power source and OS power plan
    if power_source_ac_or_dc == display_power.PowerSource.DC:
        power_cfg_query = ["powercfg.exe", "/SETDCVALUEINDEX", power_scheme, GUID_SUBGROUP_DISPLAY,
                           GUID_DISPLAY_BRIGHTNESS, str(power_plan_brightness_level)]
    elif power_source_ac_or_dc == display_power.PowerSource.AC:
        power_cfg_query = ["powercfg.exe", "/SETACVALUEINDEX", power_scheme, GUID_SUBGROUP_DISPLAY,
                           GUID_DISPLAY_BRIGHTNESS, str(power_plan_brightness_level)]
    subprocess.call(power_cfg_query)
    current_brightness_level = get_power_plan_brightness(power_source_ac_or_dc, os_power_plan)
    if current_brightness_level == power_plan_brightness_level:
        return True
    return False


##
# @brief        Exposed API to set OS adaptive display brightness status
# @param[in]    power_source_ac_or_dc AC/DC
# @param[in]    os_power_plan BALANCED/POWER_SAVER/HIGH_PERFORMANCE
# @param[in]    is_enable_adaptive_brightness True/False
# @return       status, True if operation is successful, False otherwise
def change_adaptive_brightness_in_power_plan(power_source_ac_or_dc, os_power_plan, is_enable_adaptive_brightness):
    if power_source_ac_or_dc == display_power.PowerSource.INVALID:
        logging.error("Invalid powerline status")
        return None

    if os_power_plan == display_power.PowerScheme.UNDEFINED:
        logging.error("Invalid os power plan")
        return None

    power_cfg_query = []
    power_scheme = None
    is_adaptive_brightness_enabled_value = 0
    if is_enable_adaptive_brightness is True:
        is_adaptive_brightness_enabled_value = 1

    # set power scheme GUID
    if os_power_plan == display_power.PowerScheme.POWER_SAVER:
        power_scheme = GUID_POWER_SCHEME_POWER_SAVER
    elif os_power_plan == display_power.PowerScheme.BALANCED:
        power_scheme = GUID_POWER_SCHEME_BALANCED
    elif os_power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        power_scheme = GUID_POWER_SCHEME_HIGH_PERFORMANCE

    # set powercfg.exe parameters to set adaptive brightness setting for given power source and OS power plan
    if power_source_ac_or_dc == display_power.PowerSource.DC:
        power_cfg_query = ["powercfg.exe", "/SETDCVALUEINDEX", power_scheme, GUID_SUBGROUP_DISPLAY,
                           GUID_ENABLE_ADAPTIVE_BRIGHTNESS, str(is_adaptive_brightness_enabled_value)]
    elif power_source_ac_or_dc == display_power.PowerSource.AC:
        power_cfg_query = ["powercfg.exe", "/SETACVALUEINDEX", power_scheme, GUID_SUBGROUP_DISPLAY,
                           GUID_ENABLE_ADAPTIVE_BRIGHTNESS, str(is_adaptive_brightness_enabled_value)]
    subprocess.call(power_cfg_query)
    os_adaptive_brightness_status = is_adaptive_brightness_enabled_in_power_plan(power_source_ac_or_dc, os_power_plan)
    if os_adaptive_brightness_status == is_enable_adaptive_brightness:
        return True
    return False


##
# @brief        Exposed API to get OS adaptive display brightness status
# @param[in]    power_source_ac_or_dc AC/DC
# @param[in]    os_power_plan BALANCED/POWER_SAVER/HIGH_PERFORMANCE
# @return       is_adaptive_brightness_enabled, True if enabled, False otherwise
def is_adaptive_brightness_enabled_in_power_plan(power_source_ac_or_dc, os_power_plan):
    if power_source_ac_or_dc == display_power.PowerSource.INVALID:
        logging.error("Invalid powerline status")
        return None

    if os_power_plan == display_power.PowerScheme.UNDEFINED:
        logging.error("Invalid os power plan")
        return None

    power_cfg_query = []
    is_adaptive_brightness_enabled = None

    # set powercfg.exe parameters to get adaptive brightness setting for given power source and OS power plan
    if os_power_plan == display_power.PowerScheme.POWER_SAVER:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_POWER_SAVER, GUID_SUBGROUP_DISPLAY,
                           GUID_ENABLE_ADAPTIVE_BRIGHTNESS]
    elif os_power_plan == display_power.PowerScheme.BALANCED:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_BALANCED, GUID_SUBGROUP_DISPLAY,
                           GUID_ENABLE_ADAPTIVE_BRIGHTNESS]
    elif os_power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_HIGH_PERFORMANCE, GUID_SUBGROUP_DISPLAY,
                           GUID_ENABLE_ADAPTIVE_BRIGHTNESS]

    power_cfg_output = subprocess.check_output(power_cfg_query, universal_newlines=True)
    if power_cfg_output == '':
        return None
    brightness_info = __parse_power_cfg_info(power_cfg_output)
    if len(brightness_info) == 0:
        return None
    brightness_info = brightness_info[-1]
    if power_source_ac_or_dc == display_power.PowerSource.AC:
        if 'Current AC Power Setting Index' in brightness_info.keys():
            is_adaptive_brightness_enabled = int(brightness_info['Current AC Power Setting Index'], 16)
        else:
            logging.error("Adaptive brightness information is NOT present in powercfg.exe query output")
            return None
    elif power_source_ac_or_dc == display_power.PowerSource.DC:
        if 'Current DC Power Setting Index' in brightness_info.keys():
            is_adaptive_brightness_enabled = int(brightness_info['Current DC Power Setting Index'], 16)
        else:
            logging.error("Adaptive brightness information is NOT present in powercfg.exe query output")
            return None

    if is_adaptive_brightness_enabled == 1:
        return True
    return False


##
# @brief        Exposed API to get OS brightness after dimming setting
# @param[in]    power_source_ac_or_dc AC/DC
# @param[in]    os_power_plan BALANCED/POWER_SAVER/HIGH_PERFORMANCE
# @return       brightness
def get_power_plan_brightness_level_after_dimming(power_source_ac_or_dc, os_power_plan):
    if power_source_ac_or_dc == display_power.PowerSource.INVALID:
        logging.error("Invalid powerline status")
        return None

    if os_power_plan == display_power.PowerScheme.UNDEFINED:
        logging.error("Invalid os power plan")
        return None

    power_cfg_query = []
    brightness_level_after_dimming = None

    # Set powercfg.exe parameters to get brightness after dimming setting for given power source and OS power plan
    if os_power_plan == display_power.PowerScheme.POWER_SAVER:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_POWER_SAVER, GUID_SUBGROUP_DISPLAY,
                           GUID_DIMMED_DISPLAY_BRIGHTNESS]
    elif os_power_plan == display_power.PowerScheme.BALANCED:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_BALANCED, GUID_SUBGROUP_DISPLAY,
                           GUID_DIMMED_DISPLAY_BRIGHTNESS]
    elif os_power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_HIGH_PERFORMANCE, GUID_SUBGROUP_DISPLAY,
                           GUID_DIMMED_DISPLAY_BRIGHTNESS]

    power_cfg_output = subprocess.check_output(power_cfg_query, universal_newlines=True)
    if power_cfg_output == '':
        return None
    brightness_info = __parse_power_cfg_info(power_cfg_output)
    if len(brightness_info) == 0:
        return None
    brightness_info = brightness_info[-1]
    if power_source_ac_or_dc == display_power.PowerSource.AC:
        if 'Current AC Power Setting Index' in brightness_info.keys():
            brightness_level_after_dimming = int(brightness_info['Current AC Power Setting Index'], 16)
        else:
            logging.error("Brightness level is NOT present in powercfg.exe query output")
            return None
    elif power_source_ac_or_dc == display_power.PowerSource.DC:
        if 'Current DC Power Setting Index' in brightness_info.keys():
            brightness_level_after_dimming = int(brightness_info['Current DC Power Setting Index'], 16)
        else:
            logging.error("Brightness level is NOT present in powercfg.exe query output")
            return None

    return brightness_level_after_dimming


##
# @brief        Exposed API to set OS adaptive display brightness
# @param[in]    power_source_ac_or_dc AC/DC
# @param[in]    os_power_plan BALANCED/POWER_SAVER/HIGH_PERFORMANCE
# @param[in]    brightness_level_after_dimming
# @return       status, True if operation is successful, False otherwise
def set_power_plan_brightness_level_after_dimming(power_source_ac_or_dc, os_power_plan, brightness_level_after_dimming):
    if power_source_ac_or_dc == display_power.PowerSource.INVALID:
        logging.error("Invalid powerline status")
        return None

    if os_power_plan == display_power.PowerScheme.UNDEFINED:
        logging.error("Invalid os power plan")
        return None

    power_cfg_query = []
    power_scheme = None

    # set power scheme GUID
    if os_power_plan == display_power.PowerScheme.POWER_SAVER:
        power_scheme = GUID_POWER_SCHEME_POWER_SAVER
    elif os_power_plan == display_power.PowerScheme.BALANCED:
        power_scheme = GUID_POWER_SCHEME_BALANCED
    elif os_power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        power_scheme = GUID_POWER_SCHEME_HIGH_PERFORMANCE

    # Set powercfg.exe parameters to set brightness_level_after_dimming after dimming setting for given power source
    # and OS power plan
    if power_source_ac_or_dc == display_power.PowerSource.DC:
        power_cfg_query = ["powercfg.exe", "/SETDCVALUEINDEX", power_scheme, GUID_SUBGROUP_DISPLAY,
                           GUID_DIMMED_DISPLAY_BRIGHTNESS, str(brightness_level_after_dimming)]
    elif power_source_ac_or_dc == display_power.PowerSource.AC:
        power_cfg_query = ["powercfg.exe", "/SETACVALUEINDEX", power_scheme, GUID_SUBGROUP_DISPLAY,
                           GUID_DIMMED_DISPLAY_BRIGHTNESS, str(brightness_level_after_dimming)]
    subprocess.call(power_cfg_query)
    current_brightness_level_after_dimming = get_power_plan_brightness_level_after_dimming(power_source_ac_or_dc,
                                                                                           os_power_plan)
    if current_brightness_level_after_dimming == brightness_level_after_dimming:
        return True
    return False


##
# @brief        Exposed API to get time in seconds for which OS waits before dimming the display
# @param[in]    power_source_ac_or_dc AC/DC
# @param[in]    os_power_plan BALANCED/POWER_SAVER/HIGH_PERFORMANCE
# @return       delay, in seconds
def get_power_plan_delay_for_dim_display(power_source_ac_or_dc, os_power_plan):
    if power_source_ac_or_dc == display_power.PowerSource.INVALID:
        logging.error("Invalid powerline status")
        return None

    if os_power_plan == display_power.PowerScheme.UNDEFINED:
        logging.error("Invalid os power plan")
        return None

    power_cfg_query = []
    delay_in_seconds = None

    # set powercfg.exe parameters to get dim display after setting for given power source and OS power plan
    if os_power_plan == display_power.PowerScheme.POWER_SAVER:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_POWER_SAVER, GUID_SUBGROUP_DISPLAY,
                           GUID_TURN_OFF_DISPLAY_AFTER]
    elif os_power_plan == display_power.PowerScheme.BALANCED:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_BALANCED, GUID_SUBGROUP_DISPLAY,
                           GUID_TURN_OFF_DISPLAY_AFTER]
    elif os_power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        power_cfg_query = ["powercfg.exe", "/query", GUID_POWER_SCHEME_HIGH_PERFORMANCE, GUID_SUBGROUP_DISPLAY,
                           GUID_TURN_OFF_DISPLAY_AFTER]

    power_cfg_output = subprocess.check_output(power_cfg_query, universal_newlines=True)
    if power_cfg_output == '':
        return None
    brightness_info = __parse_power_cfg_info(power_cfg_output)
    if len(brightness_info) == 0:
        return None
    brightness_info = brightness_info[-1]
    if power_source_ac_or_dc == display_power.PowerSource.AC:
        if 'Current AC Power Setting Index' in brightness_info.keys():
            delay_in_seconds = int(brightness_info['Current AC Power Setting Index'], 16)
        else:
            logging.error("Dimming time information is NOT present in powercfg.exe query output")
            return None
    elif power_source_ac_or_dc == display_power.PowerSource.DC:
        if 'Current DC Power Setting Index' in brightness_info.keys():
            delay_in_seconds = int(brightness_info['Current DC Power Setting Index'], 16)
        else:
            logging.error("Dimming time information is NOT present in powercfg.exe query output")
            return None

    return delay_in_seconds


##
# @brief        Exposed API to set OS adaptive display brightness
# @param[in]    power_source_ac_or_dc AC/DC
# @param[in]    os_power_plan BALANCED/POWER_SAVER/HIGH_PERFORMANCE
# @param[in]    delay_in_seconds in seconds
# @return       status, True if operation is successful, False otherwise
def set_power_plan_delay_for_dim_display(power_source_ac_or_dc, os_power_plan, delay_in_seconds):
    if power_source_ac_or_dc == display_power.PowerSource.INVALID:
        logging.error("Invalid powerline status")
        return None

    if os_power_plan == display_power.PowerScheme.UNDEFINED:
        logging.error("Invalid os power plan")
        return None

    power_cfg_query = []
    power_scheme = None

    # set power scheme GUID
    if os_power_plan == display_power.PowerScheme.POWER_SAVER:
        power_scheme = GUID_POWER_SCHEME_POWER_SAVER
    elif os_power_plan == display_power.PowerScheme.BALANCED:
        power_scheme = GUID_POWER_SCHEME_BALANCED
    elif os_power_plan == display_power.PowerScheme.HIGH_PERFORMANCE:
        power_scheme = GUID_POWER_SCHEME_HIGH_PERFORMANCE

    # set powercfg.exe parameters to set dim display after setting for given power source and OS power plan
    if power_source_ac_or_dc == display_power.PowerSource.DC:
        power_cfg_query = ["powercfg.exe", "/SETDCVALUEINDEX", power_scheme, GUID_SUBGROUP_DISPLAY,
                           GUID_TURN_OFF_DISPLAY_AFTER, str(delay_in_seconds)]
    elif power_source_ac_or_dc == display_power.PowerSource.AC:
        power_cfg_query = ["powercfg.exe", "/SETACVALUEINDEX", power_scheme, GUID_SUBGROUP_DISPLAY,
                           GUID_TURN_OFF_DISPLAY_AFTER, str(delay_in_seconds)]
    subprocess.call(power_cfg_query)
    current_delay_in_seconds = get_power_plan_delay_for_dim_display(power_source_ac_or_dc, os_power_plan)
    if current_delay_in_seconds == delay_in_seconds:
        return True
    return False
