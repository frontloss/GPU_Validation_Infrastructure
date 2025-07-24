########################################################################################################################
# @file         test_session_zero.py
# @brief        Test launches the IGCL sample apps and verifies the app in Session Zero mode.
#                   * Get IGCL Sample App name from command line.
#                   * Launch the IGCL Sample App and verify the Session Zero.
# @author       Prateek Joshi
########################################################################################################################

import os
import subprocess
import sys
import unittest
import logging
import fnmatch

from Libs.Core import winkb_helper
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.test_env import test_context
from Tests.Control_API.control_api_base import testBase

__CAPI_FOLDER = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "Control_Library")


##
# @brief - Verify Sample App in Session Zero mode
class testSessionZero(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Control Library Sample Apps testing in Session Zero mode")

        logging.info("APP used - {}".format(self.cmd_line_param['SAMPLE_APP'][0]))

        if self.cmd_line_param['SAMPLE_APP'] is not None:
            if self.cmd_line_param['SAMPLE_APP'][0] == 'BASIC':
                self.app = "Sample_app.exe"
            elif self.cmd_line_param['SAMPLE_APP'][0] == 'COLOR':
                self.app = "Color_Sample_app.exe"
            elif self.cmd_line_param['SAMPLE_APP'][0] == 'PANEL_DESCRIPTOR':
                self.app = "Panel_descriptor_Sample_App.exe"
            elif self.cmd_line_param['SAMPLE_APP'][0] == 'POWER':
                self.app = "PowerFeature_Sample_App.exe"
            elif self.cmd_line_param['SAMPLE_APP'][0] == 'I2C_AUX':
                self.app = "I2C_AUX_Sample_app.exe"
            elif self.cmd_line_param['SAMPLE_APP'][0] == 'SCALING':
                self.app = "Scaling_Sample_App.exe"
            elif self.cmd_line_param['SAMPLE_APP'][0] == 'UBRR':
                self.app = "UBRR_Sample_App.exe"
        else:
            self.app = "Panel_descriptor_Sample_App.exe"
            logging.info("Sample App Argument is not in Command line, Using default app as Panel Descriptor")

        sample_app_file_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "ControlApi\\Release\\SampleApp\\dump64")
        logging.info("sample app path {}".format(sample_app_file_path))
        execute_file_path = os.path.join(sample_app_file_path, self.app)
        for path, dirs, files in os.walk(sample_app_file_path):
            for sample_file in fnmatch.filter(files, self.app):
                if self.app == sample_file:
                    logging.info("Sample app is present in folder: Actual - {}, Requested - {}".format(sample_file, self.app))
                else:
                    gdhm.report_driver_bug_clib("Sample App is not available in folder: Actual - {}, Requested - {}".format(sample_file, self.app))
                    self.fail("Sample App is not available in folder: Actual - {}, Requested - {}".format(sample_file, self.app))

        # Command line : PsExec.exe -i sample_app.exe
        ps_exe_file_path = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "PsExec.exe -accepteula")
        cmd_line = "%s -i %s" % (ps_exe_file_path, execute_file_path)

        with subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process, open('ps_logfile', 'wb') as file_handle:
            for line in process.stdout:
                sys.stdout.buffer.write(line)
                file_handle.write(line)
        with open('ps_logfile', 'rb') as file_handle:
            ps_result_line = file_handle.readlines()[-1].decode("utf-8")

        result_status = True
        if ("error code 0") in ps_result_line:
            logging.info("Error Code Line {}".format(ps_result_line))
            result_status &= True
        else:
            logging.error("Error Code Line {}".format(ps_result_line))
            result_status &= False

        if result_status:
            logging.info("** PASS: Session 0 Testing with Sample App {} **".format(self.app))
        else:
            logging.error("** FAIL: Session 0 Testing with Sample App {} **".format(self.app))
            gdhm.report_driver_bug_clib("Failed to Session 0 Testing with Sample App {}".format(self.app))
            self.fail("FAIL: Session 0 Testing with Sample App {} **".format(self.app))


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Library Sample App in Session Zero mode')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)