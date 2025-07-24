########################################################################################################################
# @file         gfx_registry_restore.py
# @brief        Usage: gfx_registry_restore.py -path absolute_path -driver driver_name
# @author       Vinod D S, Kiran Kumar L
########################################################################################################################

import filecmp
import logging
import os
import subprocess
import sys
import unittest

from Libs.Core import cmd_parser, display_essential, reboot_helper
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import display_logger
from Libs.Core.test_env import test_environment


##
# @brief        GfxRegistryRestore Class
class GfxRegistryRestore(unittest.TestCase):
    gfx_path = None
    driver_name = None
    is_reboot_required = False

    ##
    # @brief        SetupClass method
    # @return       None
    @classmethod
    def setUpClass(cls) -> None:
        # sys.argv
        cmd_params = cmd_parser.parse_cmdline(sys.argv, ["-PATH", "-DRIVER"])

        # Handle multi-adapter scenario
        if not isinstance(cmd_params, list):
            cmd_params = [cmd_params]

        if cmd_params[0]['PATH'] != 'NONE':
            cls.gfx_path = cmd_params[0]['PATH'][0]
        if cmd_params[0]['DRIVER'] != 'NONE':
            cls.driver_name = cmd_params[0]['DRIVER'][0]

    ##
    # @brief        TeardownClass function
    # @return       None
    @classmethod
    def tearDownClass(cls):
        gta_state_manager.update_reboot_state(cls.is_reboot_required)

    ##
    # @brief        Runtest Method
    # @return       None
    def runTest(self) -> None:
        for indx in range(4):
            master_fname = f"{self.driver_name.lower()}_000{indx}.reg"
            master_fpath = os.path.join(self.gfx_path, master_fname)
            logging.info(f"Trying to find master registry path: {master_fpath}")
            if not os.path.exists(master_fpath):
                logging.warning(f"Master registry path not exist: {master_fpath}")
                continue
            logging.info(f"Found master registry path: {master_fpath}")
            current_fname = f"{self.driver_name.lower()}_000{indx}_temp.reg"
            current_fpath = os.path.join(os.getcwd(), current_fname)
            if os.path.exists(current_fpath):
                os.remove(current_fpath)
            reg_cmd = "reg.exe export HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\" \
                      "{4d36e968-e325-11ce-bfc1-08002be10318}\\000" + f"{indx} {current_fname} /y"
            ret = subprocess.run(reg_cmd, capture_output=True, cwd=os.getcwd())
            if ret.returncode != 0:
                logging.error(f"Reg export error: {ret.stderr}")
                continue
            logging.info(f"Trying to find current registry path: {current_fpath}")
            if not os.path.exists(current_fpath):
                logging.error(f"Current registry path not exist: {current_fpath}")
                continue
            logging.info(f"Found current registry path: {current_fpath}")
            if filecmp.cmp(master_fpath, current_fpath) is False:
                reg_cmd = f"reg.exe import {master_fname}"
                ret = subprocess.run(reg_cmd, capture_output=True, cwd=self.gfx_path)
                if ret.returncode != 0:
                    logging.error(f"Reg import error: {ret.stderr}")
                    self.fail("Gfx registry restore failed")
                logging.info("Registry restored successfully")

        logging.info("Restarting display driver after registry restore")
        stat, reboot_required = display_essential.restart_gfx_driver()
        if stat is False and reboot_required is True:
            logging.error("\tFailed to restart driver, rebooting system as requested by OS")
            self.is_reboot_required = True
        elif stat is False and reboot_required is False:
            self.fail("\tFailed to restart display driver")
        else:
            logging.info("\tSuccess: restart display driver")


if __name__ == '__main__':
    # gfx_registry_restore.py -path path1 -driver driver_name1
    test_environment.TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('GfxRegistryRestore'))
    status = test_environment.TestEnvironment.log_test_result(outcome)
    test_environment.TestEnvironment.store_cleanup_logs(status)
    display_logger._cleanup()
