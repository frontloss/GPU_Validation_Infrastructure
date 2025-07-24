#######################################################################################################################
# @file         bellwin_power_splitter.py
# @brief        Python wrapper exposes API's related to Bellwin Power splitter.
# @author       Chandrakanth Pabolu
#######################################################################################################################
import subprocess
import time
import os
import logging

from Libs.Core.test_env import test_context

PS_PATH = os.path.join(test_context.COMMON_BIN_FOLDER, "BellWinPowerSplitterCli")
PS_CTL_EXE_NAME = "BellWinPowerSplitterCli.exe"


##
# @brief        Exposed API to plug display.
# @param[in]    port - Port to which power splitter is connected.
# @return       bool - Returns True if success else False
def plug_display(port) -> bool:
    tc_exe_path = os.path.join(PS_PATH, PS_CTL_EXE_NAME)
    if not os.path.exists(tc_exe_path):
        logging.error("{} doesn't exist.".format(tc_exe_path))
        return False
    logging.info(f"Plugging Display on port: {port}.")
    status = subprocess.call([tc_exe_path, "--outlet", str(port), "--on", "on"], cwd=PS_PATH)

    if status != 0:
        logging.error(f"Failed to plug display. error code - {status}.")
        return False

    time.sleep(2)  # Buffer Time
    logging.info(f"Successfully Plugged Display on port: {port}.")
    return True


##
# @brief        Exposed API to unplug display.
# @param[in]    launch - Port to which power splitter is connected.
# @return       bool - Returns True if success else False
def unplug_display(port) -> bool:
    tc_exe_path = os.path.join(PS_PATH, PS_CTL_EXE_NAME)
    if not os.path.exists(tc_exe_path):
        logging.error("{} doesn't exist.".format(tc_exe_path))
        return False
    logging.info(f"Unplugging Display on port: {port}.")
    status = subprocess.call([tc_exe_path, "--outlet", str(port), "--on", "off"], cwd=PS_PATH)

    if status != 0:
        logging.error(f"Failed to unplug. error code - {status}.")
        return False

    time.sleep(2)  # Buffer Time
    logging.info(f"Successfully Unplugged Display on port: {port}.")
    return True


##
# @brief        Exposed API to check if bellwin power splitter connected.
# @return       bool - Returns True if connected else False
def is_connected() -> bool:
    is_splitter_connected = False
    tc_exe_path = os.path.join(PS_PATH, PS_CTL_EXE_NAME)
    if not os.path.exists(tc_exe_path):
        logging.error("{} doesn't exist.".format(tc_exe_path))
        return False

    return_status = subprocess.run([tc_exe_path, "--list"], capture_output=True, cwd=PS_PATH)
    logging.info(f"Return Status: {return_status}")
    time.sleep(2)  # Buffer Time

    if "No Belwin PowerSplitters found." not in return_status.stdout.decode():
        logging.info(f"Bellwin Power Splitter connected to system.")
        is_splitter_connected = True

    return is_splitter_connected


if __name__ == '__main__':
    unplug_display(1)
    plug_display(1)

