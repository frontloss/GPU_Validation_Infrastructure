########################################################################################################################
# @file         gta_state_manager.py
# @brief        Python wrapper exposes interfaces for maintaining gta state
# @author       Chandrakanth Pabolu
########################################################################################################################


import logging
import os
import subprocess
import time
import xml.etree.ElementTree as Et

from Libs.Core.test_env import test_context

GTA_RESULT_XML = os.path.join(test_context.LOG_FOLDER, "GtaResult.xml")
TC_PATH = "D:\\gtax-client\\bin\\win64"
TC_CTL_EXE_NAME = "tc-ctl.exe"
TC_EXE_NAME = "tc.exe"
TAG_TEST_RESULT = "TestResult"
TAG_GTA_TC_STATUS = "GtaTcStatus"
TAG_TEST_STATUS = "TestStatus"
TAG_TEST_STATE = "TestState"
TAG_DESCRIPTION = "Description"
TAG_MEASUREMENTS = "Measurements"
TAG_PASS_COUNT = "PassCount"
TAG_FAIL_COUNT = "FailCount"
TAG_ERROR_COUNT = "ErrorCount"
TAG_SKIP_COUNT = "SkipCount"
TEST_STATUS_PASS = "Pass"
TEST_STATUS_FAIL = "Fail"
TEST_STATE_REBOOT = "Reboot"
TC_STATUS_STOPPED = "Stopped"
TC_PARAM_START = "start"
TC_PARAM_STOP = "stop"


##
# @brief        Exposed API to create default GTA state.
# @return       None
def create_gta_default_state():
    if os.path.exists(GTA_RESULT_XML):
        os.remove(GTA_RESULT_XML)

    root = Et.Element(TAG_TEST_RESULT)
    Et.SubElement(root, TAG_DESCRIPTION).text = "DisplayAuto2.0 Test"
    Et.SubElement(root, TAG_TEST_STATE).text = ""
    Et.SubElement(root, TAG_GTA_TC_STATUS).text = ""
    measurements = Et.SubElement(root, TAG_MEASUREMENTS)
    Et.SubElement(measurements, TAG_PASS_COUNT).text = ""
    Et.SubElement(measurements, TAG_SKIP_COUNT).text = ""
    Et.SubElement(measurements, TAG_ERROR_COUNT).text = ""
    Et.SubElement(measurements, TAG_FAIL_COUNT).text = ""
    Et.SubElement(root, TAG_TEST_STATUS).text = ""
    tree = Et.ElementTree(root)
    tree.write(GTA_RESULT_XML)


##
# @brief        Exposed API to update test result.
# @param[in]    result - is of type (TestResult) contains all the test result information.
# @param[in]    test_status - is of type (bool) which will be the final test result
# @return       None
def update_test_result(result, test_status):
    if not os.path.exists(GTA_RESULT_XML):
        logging.error("{} doesn't exist.".format(GTA_RESULT_XML))
        return

    tree = Et.parse(GTA_RESULT_XML)
    root = tree.getroot()

    for elem in root.iter():
        if elem.tag == TAG_PASS_COUNT:
            elem.text = str(result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped))
        if elem.tag == TAG_FAIL_COUNT:
            elem.text = str(len(result.failures))
        if elem.tag == TAG_ERROR_COUNT:
            elem.text = str(len(result.errors))
        if elem.tag == TAG_SKIP_COUNT:
            elem.text = str(len(result.skipped))
        if elem.tag == TAG_TEST_STATUS:
            elem.text = TEST_STATUS_PASS if test_status else TEST_STATUS_FAIL

    tree.write(GTA_RESULT_XML)


##
# @brief        Exposed API to update TestState ie., Reboot or None.
# @param[in]    is_reboot - is of type (bool) Pass True for reboot else False
# @return       None
def update_reboot_state(is_reboot):
    if not os.path.exists(GTA_RESULT_XML):
        logging.error("{} doesn't exist.".format(GTA_RESULT_XML))
        return

    tree = Et.parse(GTA_RESULT_XML)
    root = tree.getroot()
    for child in root:
        if child.tag == TAG_TEST_STATE:
            child.text = TEST_STATE_REBOOT if is_reboot else ""
            break
    else:
        logging.error("{} doesn't exist.".format(TAG_TEST_STATE))

    tree.write(GTA_RESULT_XML)


##
# @brief        Exposed API to get GtaTcStatus
# @return       tc_status - returns True if TC is running else False
def get_gta_tc_status():
    task_manager_out = subprocess.run('tasklist', capture_output=True)
    task_manager_lines = task_manager_out.stdout.decode()
    if task_manager_out.returncode != 0 or len(task_manager_lines) == 0:
        logging.error("Couldn't get tasklist.")
        return False

    for line in task_manager_lines.splitlines():
        try:
            current_process = line[0:28].strip()
            if TC_EXE_NAME in current_process:
                logging.info(f"{TC_EXE_NAME} is running.")
                return True
        except Exception as e:
            logging.error(f"Exception occurred while fetching tasklist. {e}")

    logging.info(f"{TC_EXE_NAME} is not running.")
    return False


##
# @brief        Exposed API to update Description.
# @param[in]    description - is of type (string) updates data in the description tag.
# @return       None
def update_gta_description(description):
    if not os.path.exists(GTA_RESULT_XML):
        logging.error("{} doesn't exist.".format(GTA_RESULT_XML))
        return

    tree = Et.parse(GTA_RESULT_XML)
    root = tree.getroot()
    for child in root:
        if child.tag == TAG_DESCRIPTION:
            child.text = description
            break
    else:
        logging.error("{} doesn't exist.".format(TAG_DESCRIPTION))

    tree.write(GTA_RESULT_XML)


##
# @brief        Exposed API to configure ThinClient.
# @param[in]    launch - Pass True to Launch ThinClient, False to kill it.
# @return       None
def configure_tc(launch: bool) -> None:
    tc_exe_path = os.path.join(TC_PATH, TC_CTL_EXE_NAME)
    if not os.path.exists(tc_exe_path):
        logging.error("{} doesn't exist.".format(tc_exe_path))
        return

    # If tc is already running and re-launch is requested.
    if get_gta_tc_status() == launch:
        return

    action = TC_PARAM_START if launch == True else TC_PARAM_STOP
    status = subprocess.call([tc_exe_path, action], cwd=TC_PATH)

    if status != 0:
        logging.error(f"Failed to {action} Thin Client with error code - {status}.")
        return

    time.sleep(5)  # Buffer for Thin Client to get started.
    logging.info(f"Successfully {'Started' if action == TC_PARAM_START else 'Stopped'} Thin Client.")
