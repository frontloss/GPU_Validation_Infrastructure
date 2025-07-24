###############################################################################
# @file     valsim_setup.py
# @brief    python module to install or uninstall val sim driver
# @author   Bharath Venkatesh, Amit Sau
###############################################################################

import logging
import os
import shutil
import stat
import subprocess
import sys
import time
import traceback
import unittest
from datetime import datetime
from types import TracebackType
from typing import List

from Libs.Core import reboot_helper
from Libs.Core import test_header
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import display_logger
from Libs.Core.logger import etl_tracer
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_context import TestContext, BIN_FOLDER, TEST_TEMP_FOLDER, ROOT_FOLDER

# DevCon return status code
DEVCON_SUCCESS = 0  # 0 Success
DEVCON_REBOOT_CODE = 1  # 1 Success, Reboot Required
DEVCON_FAIL = 2  # 2 Failed
DEVCON_SYNTAX_ERROR = 3  # 3 Syntax Error

# Val-Sim device name as seen from DevCon output
VAL_SIM_DEVICE_DESC = "intel(r) gfx val simulation driver"
devcon_exe = TestContext.devcon_path()


##
# @brief        Function to get Action Type
# @return       item - INSTALL or UNINSTALL if action type passed, None otherwise
def get_action_type():
    for item in sys.argv:
        item = item.strip().upper()
        if item == 'INSTALL' or item == 'UNINSTALL':
            return item
    return None


##
# @brief        ValSim Driver Information
class ValSimDriverInfo(object):
    Name = ""
    DEV_INST_ID = ""
    Status = "Unknown Error"

    ##
    # @brief        function reset
    # @return       None
    def reset(self) -> None:
        self.Name = ""
        self.DEV_INST_ID = ""
        self.Status = "Unknown Error"

    ##
    # @brief        String representation of ValSimDriverInfo class
    # @return       str - formatted ValSimDriverInfo Object
    def to_string(self) -> str:
        return "instance id: " + self.DEV_INST_ID + " " + self.Name + " Status: " + self.Status


##
# @brief        ValSim Setup Class
class ValsimSetup(unittest.TestCase):
    log_folder = TestContext.logs_folder()
    log_handle = None
    valsim_inf = os.path.join(BIN_FOLDER, "GfxValSimDriver", "GfxValSimDriver.inf")
    active_config_file = os.path.join(TEST_TEMP_FOLDER, "config.ini")
    action_tag = None

    ##
    # @brief        This test verifies the setup environment
    # @return       None
    def test_0_setup(self) -> None:
        logging.info(f"Display Automation Binary Version : {test_header.get_binary_version()}")
        now = datetime.now()
        logging.info("Execution Start: %s" % now.strftime("%d %B %Y %H:%M:%S %p"))
        logging.info("sys.argv: %s" % sys.argv)
        logging.info("Step: test_0_setup")
        self.action_tag = get_action_type()
        if self.action_tag is None:
            self.fail("Invalid Custom tag")

    ##
    # @brief        This test installs val sim driver
    # @return       None
    @unittest.skipIf(get_action_type() != "INSTALL", "Skipping test step as action type is un-installation")
    def test_1_install_before_reboot(self) -> None:
        logging.info("Step: test_1_install_before_reboot")
        self.__copy_config_file()
        driver_list = get_driver_info()
        for dev_index in range(len(driver_list)):
            invoke_uninstall(driver_list[dev_index].DEV_INST_ID)
        self.__install_valsim()
        driver_list = get_driver_info()
        if len(driver_list) > 1:  # Val-Sim two instance WA
            # if multiple instance of val-sim driver present, un-install all and do fresh installation
            # in this case there will be always one instance will be present
            for dev_index in range(len(driver_list)):
                invoke_uninstall(driver_list[dev_index].DEV_INST_ID)
            self.__install_valsim()

    ##
    # @brief        This test uninstalls val sim driver
    # @return       None
    @unittest.skipIf(get_action_type() != "UNINSTALL", "Skipping test step as action type is installation")
    def test_2_uninstall_before_reboot(self) -> None:
        logging.info("Step: test_2_uninstall_before_reboot")
        self.__remove_readonly_file(self.active_config_file)
        self.__uninstall_valsim()

    ##
    # @brief        This test verifies val sim driver installation
    # @return       None
    def test_3_verification(self) -> None:
        logging.info("Step: test_3_verification")
        self.action_tag = get_action_type()
        # Val-Sim Driver installation verification
        driver_list = get_driver_info()
        if self.action_tag == "INSTALL":
            driver_new_list = get_driver_info()
            if len(driver_new_list) != 0:
                logging.info("PASS : Successfully installed Val-Sim Driver")
            else:
                gdhm.report_bug(
                    f"[ValSimSetup] Failed to install ValSim driver",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES
                )
                self.fail("FAIL : Failed to install Val-Sim Driver")

        elif self.action_tag == "UNINSTALL":
            if len(driver_list) == 0:
                logging.info("PASS : Successfully un-installed Val-Sim Driver")
            else:
                gdhm.report_bug(
                    f"[ValSimSetup] Failed to uninstall ValSim driver",
                    gdhm.ProblemClassification.FUNCTIONALITY,
                    gdhm.Component.Test.DISPLAY_INTERFACES
                )
                self.fail("FAIL : Failed to un-installed Val-Sim Driver")

        driver_list = get_driver_info()
        for dev_index in range(len(driver_list)):
            logging.info("Val-Sim Driver Details: %s" % driver_list[dev_index].to_string())

        logging.info("Step: Val-Sim Setup Complete")

    ##
    # @brief        Helper function to install GfxValsim driver
    # @return       None
    def __install_valsim(self) -> None:
        logging.info("Installation of Val-Sim driver started")
        # Enabling iClick tool to take care of popup's that appear during driver installation
        arm_disarm_iclick("/arm")
        status = subprocess.call([devcon_exe, "install", self.valsim_inf, "root\\umbus"])
        logging.info("Devcon status = {}".format(status))
        if status == DEVCON_SUCCESS:
            logging.info("PASS : Val-Sim installed successfully. System reboot not required")
        elif status == DEVCON_REBOOT_CODE:
            logging.info("PASS : Val-Sim installed successfully. System reboot required")
            logging.debug("Skipping System reboot")  # WA to optimize GTA reboot time
        elif status == DEVCON_FAIL:
            logging.error("FAIL : Val-Sim installation failed")
        elif status == DEVCON_SYNTAX_ERROR:
            gdhm.report_bug(
                f"[ValSimSetup] DevCon syntax error seen during ValSim installation",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            logging.error("FAIL : Devcon syntax error")
        else:
            logging.error("FAIL : Val-Sim installation failed")

        arm_disarm_iclick("/disarm")

        # Complete val sim installation
        logging.info("Installation of Val-Sim driver completed")

    ##
    # @brief        Helper function to un-install GfxValsim driver
    # @return       None
    def __uninstall_valsim(self) -> None:
        driver_list = get_driver_info()
        if len(driver_list) == 0:
            logging.info("Val-Sim is not installed, skipping un-installation")
            return

        for dev_index in range(len(driver_list)):
            logging.info("Val-Sim Driver Details: %s" % driver_list[dev_index].to_string())

        logging.info("Un-installation of Val-Sim driver started")
        # Start val sim un-installation
        devcon_status_list = []
        for dev_index in range(len(driver_list)):
            if VAL_SIM_DEVICE_DESC in driver_list[dev_index].Name:
                devcon_status = invoke_uninstall(driver_list[dev_index].DEV_INST_ID)
                logging.info("Devcon status = {}".format(devcon_status))
                devcon_status_list.append(devcon_status)

        # Check devcon status
        if DEVCON_REBOOT_CODE in devcon_status_list:
            logging.info("PASS : Val-Sim driver un-installed successfully. System reboot required")
            logging.debug("Skipping System reboot")  # WA to optimize GTA reboot time
        elif DEVCON_FAIL in devcon_status_list:
            logging.info("FAIL : Val-Sim driver un-installed failed.")
        elif DEVCON_SYNTAX_ERROR in devcon_status_list:
            gdhm.report_bug(
                f"[ValSimSetup] DevCon syntax error seen during ValSim uninstallation",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            logging.error("FAIL : Devcon syntax error")

        logging.info("PASS : Val-Sim driver un-installed successfully.")

    ##
    # @brief        Valsim cleanup function
    # @param[in]    driver_list - Driver List
    # @return       None
    def __cleanup_valsim(self, driver_list: list) -> None:
        for dev_index in range(len(driver_list)):
            if (driver_list[dev_index].Status != "Running" or
                    "root\system" in driver_list[dev_index].DEV_INST_ID.lower().strip()):
                logging.debug("Un-installing Val-Sim Driver: %s" % driver_list[dev_index].DEV_INST_ID)
                invoke_uninstall(driver_list[dev_index].DEV_INST_ID)

    ##
    # @brief        Copies the config file
    # @return       None
    def __copy_config_file(self) -> None:
        logging.debug("Delete old and copy new config.ini file at {0} path".format(TEST_TEMP_FOLDER))
        self.__remove_readonly_file(self.active_config_file)
        default_config_file = os.path.join(ROOT_FOLDER, "Libs\\Core\\test_env\\config.ini")
        if not os.path.exists(os.path.dirname(self.active_config_file)):
            os.makedirs(os.path.dirname(self.active_config_file))
        if not os.path.exists(self.active_config_file):
            shutil.copy2(default_config_file, self.active_config_file)

    ##
    # @brief        Removes stale config File
    # @param[in]    path - File path
    # @return       None
    def __remove_readonly_file(self, path: str) -> None:
        if os.path.exists(path):
            logging.debug("Deleting the stale config file at : {}".format(path))
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)


##
# @brief        Helper method to get all the details of driver instances installed under 'root\\umbus'
# @return       driver_instance - list of val sim Drivers
def get_driver_info() -> List[ValSimDriverInfo]:
    from copy import deepcopy
    driver_info = ValSimDriverInfo()
    driver_instance = []
    output = subprocess.check_output([devcon_exe, 'status', 'root\\umbus'], universal_newlines=True)
    time.sleep(3)

    out_buffer = output.splitlines()
    if (len(out_buffer)) < 3:
        return driver_instance

    index = 0
    while index < len(out_buffer):
        description = out_buffer[index].lower()
        if index >= len(out_buffer):
            break
        if ("root\system" in description or "root\\umbus" in description) and \
                VAL_SIM_DEVICE_DESC in out_buffer[index + 1].lower().strip():
            driver_info.DEV_INST_ID = description
            driver_info.Name = out_buffer[index + 1].lower().strip()
            status = out_buffer[index + 2].lower().strip()
            if "running" in status:
                driver_info.Status = "Running"
            elif "disabled" in status:
                driver_info.Status = "Disabled"
            elif "stopped" in status:
                driver_info.Status = "Stopped"
            driver_instance.append(deepcopy(driver_info))
            driver_info.reset()
            index += 3
        else:
            index += 1
    return driver_instance


##
# @brief        Helper method to remove driver instance via DevCon
# @param[in]    dev_inst_id - Instance Id of the Val-sim driver
# @return       str - console output of val sim driver uninstallation
def invoke_uninstall(dev_inst_id: str) -> int:
    logging.info("Un-installing val-sim driver with device instance %s" % dev_inst_id)
    return subprocess.call([devcon_exe, "remove", "@" + dev_inst_id])


##
# @brief        Method to take care of popup's during PnP driver installation
# @param[in]    action - command to be executed
# @return       None
def arm_disarm_iclick(action: str) -> None:
    # iClick.exe /arm waits for any popup to appear and then acts on it, if there are no popup's it
    # waits for ~10min and disarms automatically, to overcome this blocking call using Popen
    iclick_exe = os.path.join(BIN_FOLDER, "GfxValSimDriver", "iClick.exe")
    cmd = iclick_exe + ' ' + action
    subprocess.Popen(cmd)
    logging.info("PASS : iClick {0}ed".format(action))


##
# @brief        Global Exception Handler
# @param[in]    exception_type - exception category
# @param[in]    value - Exception message
# @param[in]    tb - traceback info
# @return       None
def __global_exception_handler(expection_type, value: str, tb: TracebackType) -> None:
    logging.error(value)
    logging.error(''.join(traceback.format_tb(tb)))


##
# @brief        Verify the ValSim driver status
# @return       bool - True if Driver is running, False otherwise.
def verify_sim_drv_status() -> bool:
    driver_list = get_driver_info()
    if len(driver_list) == 1 and driver_list[0].Status == "Running":
        return True
    for dev_index in range(len(driver_list)):
        if driver_list[dev_index].Status != "Running":
            logging.debug("Val-Sim Driver Details: %s" % driver_list[dev_index].to_string())
            invoke_uninstall(driver_list[dev_index].DEV_INST_ID)
            time.sleep(2)  # delay between val-sim driver un-installation and rescan
            subprocess.call([devcon_exe, "rescan"])
            time.sleep(2)
    driver_new_list = get_driver_info()
    if len(driver_new_list) == 1 and driver_new_list[0].Status == "Running":
        return True
    return False


if __name__ == '__main__':
    from Libs.Core.test_env import test_environment

    sys.excepthook = __global_exception_handler
    test_environment.TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    etl_tracer._register_trace_scripts()
    etl_tracer.start_etl_tracer()
    gta_state_manager.create_gta_default_state()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('ValsimSetup'))
    status = test_environment.TestEnvironment.log_test_result(outcome)
    test_environment.TestEnvironment.store_cleanup_logs(status)
    etl_tracer.stop_etl_tracer()
    etl_tracer._unregister_trace_scripts()
    display_logger._cleanup()
