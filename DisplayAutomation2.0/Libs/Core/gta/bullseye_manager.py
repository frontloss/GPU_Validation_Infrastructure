########################################################################################################################
# @file      bullseye_manager.py
# @brief     Python wrapper exposes interfaces for bullseye functionality
# @author    Chandrakanth Pabolu
########################################################################################################################


import hashlib
import logging
import os
import shutil
import subprocess

from Libs import env_settings
from Libs.Core.test_env import test_context

COV_RESULT_FILE = os.path.join(test_context.LOG_FOLDER, "BullseyeCodeCoverage.cov")
# Temporarily storing in GfxEvents folder until plug-in changes are done to copy to BullseyeCoverage folder.
COV_GFX_EVENTS_FILE = os.path.join(os.getcwd()[:3], "SHAREDBINARY", "920697932", "GfxEvents",
                                   "BullseyeCodeCoverage.cov")
COV_BULLSEYE_COV_FILE = os.path.join(os.getcwd()[:3], "SHAREDBINARY", "920697932", "BullseyeCoverage",
                                     "BullseyeCodeCoverage.cov")
COV_ORIGINAL_FILE = COV_BULLSEYE_COV_FILE if os.path.exists(COV_BULLSEYE_COV_FILE) else COV_GFX_EVENTS_FILE
COV_WORKING_FILE = os.path.join(os.path.expanduser('~'), "Documents", "BullseyeCodeCoverage.cov")
COV_ERROR_FILE = os.path.join(os.path.expanduser('~'), "Documents", "BullseyeCoverageError.txt")
COV_ERROR_RESULT_FILE = os.path.join(test_context.LOG_FOLDER, "BullseyeCoverageError.txt")


##
# @brief        Checks if bullseye is enabled from config.ini file
# @return       bool - True if bulleye is enabled Otherwise False
def __is_bullseye_enabled():
    force_lfp_tag = env_settings.get('GENERAL', 'bullseye')
    if force_lfp_tag == 'ENABLE':
        logging.debug("enabled")
        return True
    else:
        return False


##
# @brief        Computes file hash of the file path passed to this function
# @param[in]    file_name - file for which hash to be computed
# @return       int - Returns hash of file.
def __compute_file_hash(file_name):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


##
# @brief        Copies error logs to Logs folder
# @return       None
def __copy_error_logs():
    if os.path.exists(COV_ERROR_FILE):
        logging.info(f"Copying: {COV_ERROR_FILE} to {COV_ERROR_RESULT_FILE}")
        shutil.copyfile(COV_ERROR_FILE, COV_ERROR_RESULT_FILE)


##
# @brief        Sets environment variable
# @param[in]    name - name of an environment variable.
# @param[in]    path - value of the environment variable specified by name
# @param[in]    scope - Specifies the location where an environment variable is stored(machine, user, process)
# @return       bool -  True if bulleye is enabled Otherwise False
def __set_env_variable(name: str, path: str, scope: str):
    command = f"[Environment]::SetEnvironmentVariable('{name}', '{path}', '{scope}')"
    logging.info(f"Running powershell.exe {command}")
    status_code = subprocess.call(["powershell.exe", command])

    if status_code != 0:
        logging.error(f"Failed to configure {name}. status_code:{status_code}")
        return False
    else:
        return True


##
# @brief        Configures bullseye by writing required environment variables.
# @param[in]    enable - Pass True to enable bullseye coverage.
# @return       None
def configure_bullseye_coverage(enable):
    dest_cov_file_path = ''
    dest_error_file_path = ''

    if enable == True:
        dest_cov_file_path = COV_WORKING_FILE
        dest_error_file_path = COV_ERROR_FILE

    __set_env_variable("COVFILE", dest_cov_file_path, "Machine")
    __set_env_variable("COVERR", dest_error_file_path, "Machine")


##
# @brief        This will initializes and perform operations to start bullseye coverage
# @return       None
def setup():
    if not __is_bullseye_enabled():
        return

    # Implementation 1(Copy the file from Test store to Documents, run the test and copy back to Logs folder)
    if os.path.exists(COV_ERROR_FILE):
        logging.info(f"Removing: {COV_ERROR_FILE}")
        os.remove(COV_ERROR_FILE)

    if os.path.exists(COV_WORKING_FILE):
        logging.info(f"Removing: {COV_WORKING_FILE}")
        os.remove(COV_WORKING_FILE)

    if os.path.exists(COV_ORIGINAL_FILE):
        logging.info(f"Copying: {COV_ORIGINAL_FILE}")
        shutil.copyfile(COV_ORIGINAL_FILE, COV_WORKING_FILE)
    else:
        logging.error(f"{COV_ORIGINAL_FILE} doesn't exists.")


##
# @brief        Cleanup method to perform cleanup after tests which performed bullsye coverage.
# @return       None
def cleanup():
    if not __is_bullseye_enabled():
        return

    ##upload error logs if present
    __copy_error_logs()

    # Implementation 1(Copy the file from Test store to Documents, run the test and copy back to Logs folder)
    if os.path.exists(COV_RESULT_FILE):
        logging.info(f"Removing: {COV_RESULT_FILE}")
        os.remove(COV_RESULT_FILE)

    if os.path.exists(COV_WORKING_FILE):
        logging.info(f"Copying: {COV_WORKING_FILE} to {COV_RESULT_FILE}")
        shutil.copyfile(COV_WORKING_FILE, COV_RESULT_FILE)

        if __compute_file_hash(COV_ORIGINAL_FILE) == __compute_file_hash(COV_RESULT_FILE):
            logging.error(f"No coverage data logged: {COV_RESULT_FILE}")
    else:
        logging.error(f"{COV_WORKING_FILE} doesn't exists.")
