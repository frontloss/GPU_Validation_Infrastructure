########################################################################################################################
# @file         socwatch.py
# @brief        Contains socwatch parsing methods
# @details      This file contains below methods
#               * run_socwatch - to run socwatch command
#               * parse_socwatch_output - to parse socwatch output
#               * run_workload - to run workload like idle,video playback
#               * get_metric - to get specific socwatch metric from socwatch log file
#               * run_socwacth_cs - run socwatch command with CS
# @author       Rohit Kumar, Bhargav Adigarla
########################################################################################################################

import logging
import multiprocessing
import os
import re
import subprocess
import sys
import time

from enum import IntEnum

from Libs.Core import winkb_helper as kb, app_controls, window_helper
from Libs.Core.test_env import test_context

__SOC_WATCH_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "SocWatch_2021_1_1")
__TEST_VIDEO_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos", "24.000.mp4")

# Example: PC0    , 7.45                   , 2235.76
PKG_C_STATE_PATTERN = r"^(?P<state_name>PC[0-9]{1,2}) +, +(?P<state_percent>[0-9]+\.[0-9]{2}) +, +" \
                      r"(?P<state_time>[0-9]+\.[0-9]{2}) *$"

# "Display, DC5          , 415.00"
# "Display, DC6          , 1234.00"
DCSTATE_PATTERN = r"Display, +(?P<dc_state_name>DC[0-9]{1,2}) + +, +(?P<count>[0-9]+\.[0-9]{2}) *$"

# Example
# DDR   , GT-REQUESTS, 6.75               , 202843968.00
# DDR   , IA-REQUESTS, 147.62             , 4434113408.00
# DDR   , IO-REQUESTS, 18.77              , 563960896.00
# Total ,            , 173.14             , 5200918272.00
BW_PATTERN = r"^DDR +, +(?P<bw_name>[A-Z-]+REQUESTS), +(?P<bw_rate>[0-9]+\.[0-9]{2}) +, +" \
             r"(?P<bw_request>[0-9]+\.[0-9]{2}) *$"

# Example
# DDR   , IO_BANDWIDTH                , 910488.41          , 109676212964864.00
BW_PATTERN2 = r"^DDR +, +(?P<bw_name>[A-Z_]+BANDWIDTH) +, +(?P<bw_rate>[0-9]+\.[0-9]{2}) +, +" \
             r"(?P<bw_request>[0-9]+\.[0-9]{2}) *$"

# Example: Total ,        , 173.12
TOTAL_BW_PATTERN = r"^Total +, +, +(?P<bw_total>[0-9]+\.[0-9]{2}) +, +[0-9]+\.[0-9]{2} *$"

IO_READ_PATTERN = r"^SoC +, +(?P<bw_name>[A-Z-]+TOTAL-READS) +, +(?P<bw_rate>[0-9]+\.[0-9]{2}) +, +" \
             r"(?P<bw_request>[0-9]+\.[0-9]{2}) *$"

IO_WRITE_PATTERN = r"^SoC +, +(?P<bw_name>[A-Z-]+TOTAL-WRITES) +, +(?P<bw_rate>[0-9]+\.[0-9]{2}) +, +" \
             r"(?P<bw_request>[0-9]+\.[0-9]{2}) *$"

__SCORE_MULTIPLIER = {
    "PACKAGE_C0": 0, "PACKAGE_C2": 0, "PACKAGE_C3": 0, "PACKAGE_C6": 0, "PACKAGE_C7": 0, "PACKAGE_C8": 0,
    "PACKAGE_C9": 1, "PACKAGE_C10": 3,
    'CORE_C0': 0, 'CORE_C1': 1, 'CORE_C6': 3, 'CORE_C7': 5,
    'DC_5': 1, 'DC_6': 3
}

PSR1_PATTERN = r"PSR1 is enabled."
PSR1_OFF = r"Full On"
PSR1_ON = r"Full Off"
PSR2_PATTERN = r"PSR2 is enabled."
PSR2_OFF = r"Display On (Not PSR)"
PSR2_SU = r"PSR Selective Update"
PSR2_DEEP_SLEEP = r"PSR Deep Sleep"


##
# @brief        Enum Class for Socwatch Fields
class SocWatchFields(IntEnum):
    PACKAGE_C0 = 0
    PACKAGE_C2 = 1
    PACKAGE_C3 = 2
    PACKAGE_C6 = 3
    PACKAGE_C7 = 4
    PACKAGE_C8 = 5
    PACKAGE_C9 = 6
    PACKAGE_C10 = 7
    GT_REQUESTS = 8
    IA_REQUESTS = 9
    IO_REQUESTS = 10
    TOTAL_BANDWIDTH = 11
    CORE_C0 = 12
    CORE_C1 = 13
    CORE_C6 = 14
    CORE_C7 = 15
    DC_5 = 16
    DC_6 = 17
    PSR1_STATUS = 18
    PSR2_STATUS = 19
    LINK_ON = 20
    LINK_OFF = 21
    PSR2_SU = 22
    PSR2_DEEP_SLEEP = 23,
    IO_BANDWIDTH = 24,
    IO_READS = 25,
    IO_WRITES = 26


##
# @brief        Exposed API for running SocWatch.
# @param[in]    soc_folder is the socwatch tool folder absolute path
# @param[in]    soc_command is the socwatch command to be executed
# @param[in]    is_blocking_call is optional, if user needs non-blocking socwatch run then set this to False
# @return       returns True if executed correctly, otherwise False
def __run_socwatch(command, soc_folder=__SOC_WATCH_PATH, is_blocking_call=True):
    if soc_folder is None or command is None:
        logging.error("Parameters provided are none, please provide the valid parameters")
        return False

    if os.path.isdir(soc_folder) is False:
        logging.error("SocWatch folder provided does not exist")
        return False

    is_64bit = sys.maxsize > 2 ** 32
    platform_arch = 32
    if is_64bit:
        platform_arch = 64

    actual_soc_dir = "%s\\%s" % (soc_folder, platform_arch)
    full_path_soc_exe = actual_soc_dir + "\\socwatch.exe"
    command = command.replace("socwatch", actual_soc_dir + "\\socwatch")
    actual_soc_command = "%s -o SOCWatchOutput" % command

    for each_file in os.listdir(os.getcwd()):
        if each_file.endswith(".csv") or each_file.endswith(".etl"):
            os.remove(os.path.join(os.getcwd(), each_file))

    if not os.path.exists(full_path_soc_exe):
        logging.error("socwatch.exe does not exist in the specified location")
        return False

    if is_blocking_call:
        p = subprocess.Popen(actual_soc_command)
        p.wait()
    else:
        subprocess.Popen(actual_soc_command)
        logging.debug("Launching SocWatch is successful")

    return True


##
# @brief        Exposed API for parsing the SocWatch output log.
# @param[in]    soc_log_file is the socwatch log file with absolute path
# @return       True for success or False failure and dictionary with SocWatchFields as key
def parse_socwatch_output(soc_log_file):
    if soc_log_file is None or not os.path.exists(soc_log_file):
        logging.error("Invalid SoCWatch log file: {0}".format(soc_log_file))
        return False, {}

    total_cores = int(multiprocessing.cpu_count() / 2)
    socwatch_output = {}

    # Example: CC0    , 3.78                , 3.14                , 2.94                , 1.70
    # Number of Core C State entries is decided by physical core count.
    core_c_state_pattern = r"^(?P<state_name>CC[0-9])"
    for core_index in range(total_cores):
        core_c_state_pattern += r" +, +(?P<core" + str(core_index) + r"_percent>[0-9]+\.[0-9]{2})"
    core_c_state_pattern += r" [ ,.0-9]*$"

    for eachitem in SocWatchFields:
        if 'CORE_C' in eachitem.name:
            socwatch_output[eachitem.value] = [0.0] * total_cores
        else:
            socwatch_output[eachitem.value] = 0.0

    with open(soc_log_file, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    for line in all_lines:
        match_obj = re.match(PKG_C_STATE_PATTERN, line, re.M | re.I)
        if match_obj:
            # PC0 - PC10
            state_name = 'PACKAGE_C' + match_obj.group('state_name').upper()[2:]
            for eachitem in SocWatchFields:
                if state_name in eachitem.name.upper():
                    socwatch_output[eachitem.value] = float(match_obj.group('state_percent'))
                    break
            continue

        match_obj = re.match(core_c_state_pattern, line, re.M | re.I)
        if match_obj:
            # CC0 - CC7
            state_name = 'CORE_C' + match_obj.group('state_name').upper()[2:]
            for eachitem in SocWatchFields:
                if state_name in eachitem.name.upper():
                    for core_index in range(total_cores):
                        socwatch_output[eachitem.value][core_index] = float(
                            match_obj.group('core{0}_percent'.format(core_index)))
                    break
            continue

        match_obj = re.match(BW_PATTERN, line, re.M | re.I)
        if match_obj:
            state_name = match_obj.group('bw_name').upper()[0:2]
            for eachitem in SocWatchFields:
                if state_name in eachitem.name.upper():
                    socwatch_output[eachitem.value] = float(match_obj.group('bw_rate'))
                    break
            continue

        match_obj = re.match(BW_PATTERN2, line, re.M | re.I)
        if match_obj:
            state_name = match_obj.group('bw_name').upper()[0:2]
            for eachitem in SocWatchFields:
                if state_name in eachitem.name.upper():
                    socwatch_output[eachitem.value] = float(match_obj.group('bw_rate'))
                    break
            continue

        match_obj = re.match(DCSTATE_PATTERN, line, re.M | re.I)
        if match_obj:
            state_name = 'DC_' + match_obj.group('dc_state_name').upper()[2:]
            for eachitem in SocWatchFields:
                if state_name in eachitem.name.upper():
                    socwatch_output[eachitem.value] = float(match_obj.group('count'))
                    break
            continue

        match_obj = re.match(IO_READ_PATTERN, line, re.M | re.I)
        if match_obj:
            for eachitem in SocWatchFields:
                if eachitem.name is 'IO_READS':
                    socwatch_output[eachitem.value] = float(match_obj.group('bw_rate'))

        match_obj = re.match(IO_WRITE_PATTERN, line, re.M | re.I)
        if match_obj:
            for eachitem in SocWatchFields:
                if eachitem.name is 'IO_WRITES':
                    socwatch_output[eachitem.value] = float(match_obj.group('bw_rate'))

        if re.search(PSR1_PATTERN, line):
            for eachitem in SocWatchFields:
                if eachitem.name is 'PSR1_STATUS':
                    socwatch_output[eachitem.value] = True

        if re.search(PSR2_PATTERN, line):
            for eachitem in SocWatchFields:
                if eachitem.name is 'PSR2_STATUS':
                    socwatch_output[eachitem.value] = True

        if socwatch_output[SocWatchFields.PSR1_STATUS.value]:
            if re.search(PSR1_OFF, line):
                for eachitem in SocWatchFields:
                    if eachitem.name is 'LINK_ON':
                        socwatch_output[eachitem.value] = float(re.findall(r"\d*\.\d+|\d+", line)[0])
            if re.search(PSR1_ON, line):
                for eachitem in SocWatchFields:
                    if eachitem.name is 'LINK_OFF':
                        socwatch_output[eachitem.value] = float(re.findall(r"\d*\.\d+|\d+", line)[0])

        if socwatch_output[SocWatchFields.PSR2_STATUS.value]:
            if re.search(PSR2_OFF, line):
                for eachitem in SocWatchFields:
                    if eachitem.name is 'LINK_ON':
                        socwatch_output[eachitem.value] = float(re.findall(r"\d*\.\d+|\d+", line)[0])
            if re.search(PSR2_SU, line):
                for eachitem in SocWatchFields:
                    if eachitem.name is 'PSR2_SU':
                        socwatch_output[eachitem.value] = float(re.findall(r"\d*\.\d+|\d+", line)[0])
            if re.search(PSR2_DEEP_SLEEP, line):
                for eachitem in SocWatchFields:
                    if eachitem.name is 'PSR2_DEEP_SLEEP':
                        socwatch_output[eachitem.value] = float(re.findall(r"\d*\.\d+|\d+", line)[0])

    soc_op_str = ""
    for key1, val1 in socwatch_output.items():
        soc_op_str += "%s = %s, " % (SocWatchFields(key1).name, val1)
    logging.debug("SocWatch Output = %s" % soc_op_str)

    return True, socwatch_output


##
# @brief        Exposed API to run socwatch with a given workload
# @param[in]    workload
# @param[in]    duration
# @return       report_path, String, full path of the socwatch report
def run_workload(workload, duration):
    assert workload in ["IDLE", "VIDEO"], "'{0} workload' is not supported by SoCWatch tool".format(workload)
    assert duration, "Invalid duration"

    if workload == "IDLE":
        logging.info("Step: Running Workload IDLE for {0} seconds".format(duration))
        kb.press('WIN+M')

    if workload == "VIDEO":
        logging.info("Step: Running Workload VIDEO for {0} seconds".format(duration))
        logging.info("\tVideo Playback started : 24.000.mp4")
        app_controls.launch_video(__TEST_VIDEO_PATH)

    __run_socwatch("socwatch --polling -n 100 -t {0} -s 30 -f sys --skip-usage-collection ".format(duration))

    if workload == "IDLE":
        kb.press("ALT+TAB")

    if workload == "VIDEO":
        logging.info("\tClosing video playback")
        window_helper.close_media_player()
        kb.press("ALT+TAB")

    socwatch_log_path = os.path.join(os.getcwd(), "SOCWatchOutput.csv")
    if os.path.exists(socwatch_log_path) is False:
        logging.error("{0} not found".format(socwatch_log_path))
        return None

    report_path = os.path.join(test_context.LOG_FOLDER, "SOCWatchOutput-{0}.csv".format(time.time()))
    os.rename(socwatch_log_path, report_path)
    return report_path


##
# @brief        Exposed API to get the socwatch log path
# @return       report_path, String, full path of the socwatch report
def get_socwatch_log():
    socwatch_log_path = os.path.join(os.getcwd(), "SOCWatchOutput.csv")
    report_path = os.path.join(test_context.LOG_FOLDER, "SOCWatchOutput-{0}.csv".format(time.time()))
    if os.path.exists(socwatch_log_path) is False:
        logging.error("{0} not found".format(socwatch_log_path))
        return None

    os.rename(socwatch_log_path, report_path)
    return report_path


##
# @brief        This function is used to get metric from a given report
# @param[in]    report_path string path of the report
# @param[in]    metric metric to be calculated from the report (PKG_C_SCORE/CORE_C_SCORE/DC_STATE_COUNT)
# @return       metric if present, None otherwise
def get_metric(report_path, metric):
    assert report_path
    assert metric

    result, soc_output = parse_socwatch_output(report_path)
    if result is False:
        return None

    if metric == "PKG_C_SCORE":
        pkg_c_score = 0
        logging.info("\tGetting Pkg C Residency score")
        for state, state_value in soc_output.items():
            if "PACKAGE" in SocWatchFields(state).name.upper():
                logging.info("\t\t{0}= {1} %".format(SocWatchFields(state).name, state_value))
                pkg_c_score += (state_value * __SCORE_MULTIPLIER[SocWatchFields(state).name])
        logging.info("\t\tTotal Pkg C State Residency Score= {0}".format(pkg_c_score))
        return pkg_c_score

    if metric == "CORE_C_SCORE":
        core_c_score = 0
        logging.info("\tGetting Core C State Residency score")
        for state, state_value in soc_output.items():
            if "CORE_" in SocWatchFields(state).name.upper():
                logging.info("\t\t{0}= {1} %".format(SocWatchFields(state).name, state_value))
                for core_value in state_value:
                    core_c_score += (core_value * __SCORE_MULTIPLIER[SocWatchFields(state).name])
        logging.info("\t\tTotal Core C State Residency Score= {0}".format(core_c_score))
        return core_c_score

    if metric == 'DC_STATE_COUNT':
        dc_state_count = 0
        logging.info("\tGetting DC State count")
        for state, state_value in soc_output.items():
            if "DC_" in SocWatchFields(state).name.upper():
                logging.info("\t\t{0}= {1}".format(SocWatchFields(state).name, state_value))
                dc_state_count += (state_value * __SCORE_MULTIPLIER[SocWatchFields(state).name])
        logging.info("\t\tTotal DC state count = {0}".format(dc_state_count))
        return dc_state_count

    logging.info("\t{0}= {1}".format(metric, soc_output[SocWatchFields[metric].value]))
    return soc_output[SocWatchFields[metric].value]


##
# @brief        Exposed API to run socwatch
# @param[in]    duration for how long socwatch has to be run
# @return       report_path, String, full path of the socwatch report
def run_socwatch(duration=120):
    __run_socwatch(f"socwatch --polling -n 100 -t {duration} -f sys --skip-usage-collection", is_blocking_call=False)


##
# @brief        Exposed API to run socwatch with CS
# @param[in]    duration for how long socwatch has to be run
# @return       report_path, String, full path of the socwatch report
def run_soc_watch_with_cs(duration=120):
    __run_socwatch(f"socwatch -s 3 -t {duration} -f cpu-cstate -z --skip-usage-collection", is_blocking_call=True)
    return get_socwatch_log()


if __name__ == '__main__':
    soc_command = "socwatch --polling -n 1000 -t 120 -s 5 -f sys --skip-usage-collection"
    result = __run_socwatch(soc_command)
    if result:
        soc_logfile_path = os.path.join(os.getcwd(), "SOCWatchOutput.csv")
        result, soc_output = parse_socwatch_output(soc_logfile_path)
        if result:
            p_state_str = ""
            for key, value in soc_output.items():
                if "PACKAGE" in SocWatchFields(key).name.upper():
                    p_state_str += "%s = %s, " % (SocWatchFields(key).name, value)
            print("Package Residency: %s" % p_state_str)
        else:
            print("SocWatch log parse is failed")
    else:
        print("Running the SocWatch failed")
