########################################################################################################################
# @file         test_sample_apps.py
# @brief        Test launches the sample apps and verifies the app verifier for sample applications.
#                   * Get Sample App name and version from command line.
#                   * Launch the Sample App and verify the App verifier through GTA CFG.
# @author       Prateek Joshi, Dheeraj Dayakaran
########################################################################################################################

import fnmatch
import logging
import os
import subprocess
import sys
import time
import unittest
import shutil
import xml.etree.ElementTree as ET

import win32api
import win32con

from Libs.Core import winkb_helper
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Control_API.control_api_base import testBase
from Libs.Core import test_header

DEFAULT_LINE_WIDTH = 172
BASE_PATH_APP_VERIFIER = r"C:\Users\gta\AppVerifierLogs"

##
# @brief - Verify Sample App - App Verifier
class testSampleApps(testBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        logging.info("Test: Control Library Sample Apps")


        if self.cmd_line_param['SAMPLE_APP'] and self.cmd_line_param['DLL_VERSION'] is not None:
            
            dll_version = self.cmd_line_param['DLL_VERSION'][0]
            logging.info(f"APP used - {self.cmd_line_param['SAMPLE_APP'][0]} of {dll_version} bit")
            
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
            logging.error(
                "Incorrect Command line: Test requires Sample App tag and version input to run sample applications")
            logging.info("Sample apps Tag: EXE Name \n"
                         "Basic:        Sample_app.exe\n"
                         "Color:        Color_Sample_app.exe\n"
                         "Panel_Descriptor:    Panel_descriptor_Sample_App.exe\n"
                         "Power:        PowerFeature_Sample_App.exe\n"
                         "I2C_Aux:      I2C_AUX_Sample_app.exe\n"
                         "Scaling:      Scaling_Sample_App.exe\n"
                         "DisplayShift:  DisplayShift.exe\n"
                         "SWPSR:        SwPsr_Sample_App.exe\n"
                         "UBRR:         UBRR_Sample_App.exe\n")
            logging.info("Sample app version input: \n"
                         "32: 32-bit version\n"
                         "64: 64-bit version\n"
                         )
            self.fail()

        if dll_version == "32":
            sample_app_file_path = os.path.join(test_context.SHARED_BINARY_FOLDER,
                                                "Windows\\Release\\SampleApp\\dump32")
        else:
            sample_app_file_path = os.path.join(test_context.SHARED_BINARY_FOLDER,
                                                "Windows\\Release\\SampleApp\\dump64")

        logging.info("Sample app path {}".format(sample_app_file_path))

        for path, dirs, files in os.walk(sample_app_file_path):
            for sample_file in fnmatch.filter(files, self.app):
                if self.app == sample_file:
                    logging.info(
                        "Sample app is present in folder: Actual - {}, Requested - {}".format(sample_file, self.app))
                else:
                    self.fail("Sample App is not availble in folder: Actual - {}, Requested - {}".format(sample_file,
                                                                                                         self.app))

        execute_file_path = os.path.join(sample_app_file_path, self.app)
        logging.info("Execute file path {}".format(execute_file_path))

        # run the sample app
        shell_execution_result = subprocess.run([execute_file_path], capture_output=True, text=True).stdout
        logging.info("\n\n"+"SHELL EXECUTION RESULT - START".center(DEFAULT_LINE_WIDTH, '=')+ "\n\n"+f"{shell_execution_result}"+"\n\n"+ "SHELL EXECUTION RESULT - END".center(DEFAULT_LINE_WIDTH, '=')+"\n")
        time.sleep(5)

        app_name = (self.app).split(".")[0]

        # wait for event Quit for basic sample app
        if self.app == "Sample_app.exe":
            winkb_helper.press('Q')

        logging.info("Verifying using  verifier")
        deleteFiles(r"{0}".format(BASE_PATH_APP_VERIFIER))

        status = subprocess.Popen(["appverif", "-delete", "settings", "-for", self.app], stdout=subprocess.PIPE)
        time.sleep(3)
        status.communicate()
        if status.returncode != 0:
            gdhm.report_driver_bug_clib("Config Deletion failed for {0} in App verifier".format(self.app))
            self.fail("Unable to delete the config for {0} in App verifier".format(self.app))
        logging.info("Deleted the already existig config for {0} in App verifier successfully".format(self.app))

        status = subprocess.Popen(["appverif","/verify",execute_file_path], stdout=subprocess.PIPE)
        time.sleep(3)
        status.communicate()
        if status.returncode != 0:
            gdhm.report_driver_bug_clib("Failed to add app - {0} in App verifier".format(self.app))
            self.fail("Unable to add the app - {0} in App verifier".format(self.app))
        logging.info("Added app - {0} succesfully".format(self.app))

        status = subprocess.run([execute_file_path], capture_output=True, text=True)
        time.sleep(3)
        if status.returncode < 0:
            self.fail("Unable to run the app - {0}".format(self.app))

        export2XML = r"appverif.exe -logtoxml {0}\{1}.exe.0.dat {0}\{1}.xml".format(BASE_PATH_APP_VERIFIER,app_name).split(" ")
        status = subprocess.Popen(export2XML, stdout=subprocess.PIPE)
        time.sleep(3)
        status.communicate()
        if status.returncode > 1:
            gdhm.report_driver_bug_clib("Failed to generate the XML logs for {0} in App verifier".format(self.app))
            self.fail("Unable to generate the XML logs for {0} in App verifier".format(self.app))
        logging.info(f"XML generated Successfully")
        
        xml_parser_helper(r"{0}\{1}.xml".format(BASE_PATH_APP_VERIFIER,app_name))
        logging.info(f"XML parsed successfully")


##
# @brief            Helper function to delete existing files in Appverifier logs
# @param[in]        path: Appverfier Log Folder
# @return           None
def deleteFiles(path):
    if os.path.exists(BASE_PATH_APP_VERIFIER):
        dir = os.listdir(path)
        if len(dir) > 0:
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    logging.error('Failed to delete %s. Reason: %s' % (file_path, e))

##
# @brief            Helper function to parse XML for logging
# @param[in]        path: XML file path
# @return           None
def xml_parser_helper(path):
    logging.info(f"Path: {path}")
    tree = ET.parse(path)
    root = tree.getroot()

    xml_logs = ""

    # Find all the avrf:logEntry elements
    log_entries = root.findall(".//{Application Verifier}logEntry")

    if (len(log_entries)>0):
    
        # Iterate over each log entry and print the details
        for entry in log_entries:

            xml_logs = "Time: {0}, LayerName: {1}, StopCode: {2}, Severity: {3}, Message: {4}".format(
                entry.get('Time'),entry.get('LayerName'), entry.get('StopCode'), entry.get('Severity'),
                entry.get('Message')
            )

            # Get all the parameters and their values
            p = 1
            paramter = ""
            while (p > 0):
                params = entry.findall('{Application Verifier}parameter'+str(p))
                if (len(params)>0):
                    for param in params:
                        paramter += param.text
                    p+=1
                else:
                    break
            xml_logs += "\nParameter: {0}".format(paramter)

            # Get the stack trace
            trace_text = ""
            trace = entry.find('{Application Verifier}stackTrace')
            for t in trace.findall('{Application Verifier}trace'):
                trace_text += t.text
                trace_text += "\n"
            xml_logs += "\nTrace: {0}".format(trace_text)
    else:
        xml_logs = "No error found"    

    logging.info("\n\n"+"APP VERIFIER LOGS - START".center(DEFAULT_LINE_WIDTH, '=')+ "\n\n"+f"{xml_logs}"+"\n\n"+ "APP VERIFIER LOGS - END".center(DEFAULT_LINE_WIDTH, '=')+"\n")



if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Test Control Library Sample App - App Verifer')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
