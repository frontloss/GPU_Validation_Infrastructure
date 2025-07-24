########################################################################################################################
# @file         powermeter.py
# @brief        Contains powermeter command and parsing methods
# @details      This file contains below methods
#               * start_pm - to start powermeter tool
#               * stop_pm  - to stop powermeter tool
#               * run_pm_workload - to run workload like idle,video playback with pm start and stop
#               * get_hw_metric - to get hw metrics from powermeter log file
# @author       Bhargav Adigarla
########################################################################################################################
import os
import logging
import subprocess
import time

from Libs.Core.test_env import test_context

TEST_SPECIFIC_BIN = os.path.join(test_context.TEST_STORE_FOLDER, "TestSpecificBin")
PM_TOOL_PATH = (TEST_SPECIFIC_BIN + "\\PowerMeter")
PM_TOOL_NAME = "PowerMeterCli.exe"
PM_LOG_FILE = "PowerMeter.csv"


##
# @brief        Start power meter tool
# @param[in]    interval :sampling interval with default value 1sec
# @return       Process object if command ran successfully, else False
def run_pm(duration=130):
    if os.path.isdir(PM_TOOL_PATH) is False:
        logging.error("PowerMeter folder provided does not exist")
        return False

    tool_path = os.path.join(PM_TOOL_PATH, PM_TOOL_NAME)
    if os.path.isfile(tool_path) is False:
        logging.error("PowerMeter tool provided does not exist: {0}".format(PM_TOOL_NAME))
        return False

    op_path = os.path.join(test_context.ROOT_FOLDER, PM_LOG_FILE)
    pm_command = tool_path + f" -p=0.5 -r={duration*2} -n={op_path} -noWindow"
    p = subprocess.Popen(pm_command)
    if p is None:
        logging.info("Failed to launch power meter")
        return False
    logging.debug("command: {0}".format(pm_command))
    logging.info("Launching PowerMeter is successful")
    return p


def get_pm_log():
    tool_path = os.path.join(PM_TOOL_PATH, PM_TOOL_NAME)
    if os.path.isfile(tool_path) is False:
        logging.error("PowerMeter tool provided does not exist: {0}".format(PM_TOOL_NAME))
        return False

    op_path = os.path.join(test_context.ROOT_FOLDER, PM_LOG_FILE)
    pm_command = tool_path + f" -stop"
    p = subprocess.Popen(pm_command)
    if p is None:
        logging.info("Failed to launch power meter")
        return False
    time.sleep(5)
    pm_logfile_path = os.path.join(os.getcwd(), PM_LOG_FILE)
    report_path = os.path.join(test_context.LOG_FOLDER, "PowerMeter-{0}.csv".format(time.time()))
    if os.path.exists(pm_logfile_path) is False:
        logging.error("{0} not found".format(pm_logfile_path))
        return None

    os.rename(pm_logfile_path, report_path)
    return get_hw_metrics(report_path)


##
# @brief        get hw metrics after averaging all rows in csv file
# @param[in]    report_path :power meter log file path
# @return       power meter log path on success, else False
def get_hw_metrics(report_path):
    return __get_averages(report_path)


##
# @brief        calculate average of a given list
# @param[in]    numbers :list
# @return       average of give list
def average(numbers):
    return sum(numbers)/len(numbers)


##
# @brief        calculate averages for all columns in given csv file
# @param[in]    file_path :csv file path
# @return       dictionary of metrics after taking average
def __get_averages(file_path):
    output = {}
    cleaned_lines = []

    with open(file_path) as f:
        lines = f.readlines()
        rails = lines[0].split(',')[2:-1]
        lines = lines[1:]

        for line in lines:
            if '-nan(ind)' in line:
                continue
            cleaned_lines.append(line)

        rows_of_numbers = [map(float, line.split(',')[2:-1]) for line in cleaned_lines]
        averages = list(map(average, zip(*rows_of_numbers)))

        index = 0
        for col in rails:
            output[col] = round(averages[index],4)
            index += 1
        return output