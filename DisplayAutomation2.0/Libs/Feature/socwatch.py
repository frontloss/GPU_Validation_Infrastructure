#################################################################################################################
# @file         socwatch.py
# @brief        implements helper functions for socwatch verification
# @details      CommandLine: python Libs\Feature\socwatch.py
# @author       Vinod D S
#################################################################################################################
import io, os, re, sys
import logging
import subprocess
from enum import IntEnum


##
# SocWatch capture fields
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


##
# @brief API for running SocWatch.
# @param[in] soc_folder is the socwatch tool folder absolute path
# @param[in]  soc_command is the socwatch command to be executed
# @param[in]  is_blocking_call is optional, if user needs non-blocking socwatch run then set this to False
# @return True if executed correctly, otherwise False
def run_socwatch(soc_folder, soc_command, is_blocking_call=True):
    if soc_folder is None or soc_command is None:
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
    soc_command = soc_command.replace("socwatch", actual_soc_dir + "\\socwatch")
    actual_soc_command = "%s -o SOCWatchOutput" % soc_command

    for each_file in os.listdir(os.getcwd()):
        if each_file.endswith(".csv") or each_file.endswith(".etl"):
            os.remove(os.path.join(os.getcwd(), each_file))

    if not os.path.exists(full_path_soc_exe):
        logging.error(f"socwatch.exe does not exist in the specified location - {full_path_soc_exe}")
        return False

    if is_blocking_call:
        p = subprocess.Popen(actual_soc_command)
        p.wait()
    else:
        subprocess.Popen(actual_soc_command)
        logging.debug("Launching SocWatch is successful")

    return True


##
# @brief      API for parsing the SocWatch output log.
# @param[in]  soc_log_file is the socwatch log file with absolute path
# @return     True for success or False failure and dictionary with SocWatchFields as key
def parse_socwatch_output(soc_log_file):
    if soc_log_file is None:
        logging.error("SocWatch log file with absolute path is None")
        return False, {}

    if not os.path.exists(soc_log_file):
        logging.error(f"{soc_log_file} does not exist in the specified location")
        return False, {}

    soc_ver_new = True
    total_bw_filled = False
    version_pattern = r"^[a-zA-Z]+\(.\)[a-zA-Z ]+\*[a-zA-Z ]+(?P<version>[0-9]\.[0-9]+)\.?[0-9]? ?\[[\w ]+\]$"
    fl = io.open(soc_log_file, 'r')
    all_lines = fl.readlines()
    # Get the version
    for line in all_lines:
        match_obj = re.match(version_pattern, line, re.M | re.I)
        if match_obj:
            soc_ver_new = float(match_obj.group('version')) > 2
            break

    socwatch_output = {}
    # For ver < 2
    cstate_pattern = r"^ +(?P<state_name>C[0-9]{1,2}), +(?P<state_percent>[0-9]+\.[0-9]{2})%, +(?P<state_time>[0-9]+\.[0-9]{2})s,$"
    bw_pattern = r"^ +(?P<bw_name>[A-Z ]+Requests), +(?P<bw_rate>[0-9]+\.[0-9]{2}), +(?P<bw_request>[0-9]+),$"
    total_bw_pattern = r"^ +Total Memory [a-zA-Z ]+\([a-zA-Z/]+\) +=, +(?P<bw_total>[0-9]+\.[0-9]{2}),$"

    if soc_ver_new:
        cstate_pattern = r"^(?P<state_name>PC[0-9]{1,2}) +, +(?P<state_percent>[0-9]+\.[0-9]{2}) +, +(?P<state_time>[0-9]+\.[0-9]{2}) *$"
        bw_pattern = r"^DDR +, +(?P<bw_name>[A-Z-]+REQUESTS), +(?P<bw_rate>[0-9]+\.[0-9]{2}) +, +(?P<bw_request>[0-9]+\.[0-9]{2}) *$"
        total_bw_pattern = r"^Total +, +, +(?P<bw_total>[0-9]+\.[0-9]{2}) +, +[0-9]+\.[0-9]{2} *$"

    ##
    # Initializing the dictionary
    for soc_watch_field in SocWatchFields:
        socwatch_output[soc_watch_field.value] = float(0.0)
    ##
    # Get package c-state
    for line in all_lines:
        match_obj = re.match(cstate_pattern, line, re.M | re.I)
        if match_obj:
            for soc_watch_field in SocWatchFields:
                search_str = match_obj.group('state_name').upper()
                if soc_ver_new:
                    search_str = search_str[1:len(search_str)]
                if search_str in soc_watch_field.name.upper():
                    socwatch_output[soc_watch_field.value] = float(match_obj.group('state_percent'))
                    break
        else:
            match_obj = re.match(bw_pattern, line, re.M | re.I)
            if match_obj:
                for soc_watch_field in SocWatchFields:
                    search_str = match_obj.group('bw_name').upper()[0:2]
                    if search_str in soc_watch_field.name.upper():
                        socwatch_output[soc_watch_field.value] = float(match_obj.group('bw_rate'))
                        break
            else:
                if total_bw_filled is False:
                    match_obj = re.match(total_bw_pattern, line, re.M | re.I)
                    if match_obj:
                        socwatch_output[SocWatchFields.TOTAL_BANDWIDTH] = float(match_obj.group('bw_total'))
                        total_bw_filled = True

    soc_op_str = ""
    for key1, val1 in socwatch_output.items():
        soc_op_str += "%s = %s, " % (SocWatchFields(key1).name, val1)
    logging.debug("SocWatch Output = %s" % soc_op_str)

    return True, socwatch_output


if __name__ == '__main__':
    soc_command = "socwatch --polling -n 1000 -t 120 -s 5 -f sys"
    result = run_socwatch("C:\SocWatch", soc_command)
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