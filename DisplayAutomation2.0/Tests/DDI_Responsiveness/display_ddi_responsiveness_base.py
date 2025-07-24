#######################################################################################################################
# @file         display_ddi_responsiveness_base.py
# @brief        This file contains DDI_Responsiveness base file which should be inherited by all DDI_Responsiveness
#               related tests
# @details      display_ddi_responsiveness_base.py contains ADKBase class which implements SetUp method
#               to setup the environment
#               required. Also contains Methods to invoke to power event and collect etl traces and also capture and
#               verify diana values with respective target values
#
# @author       Nivetha B, Ravichandran M
#######################################################################################################################

import logging
import os
import shutil
import sys
import json
import unittest

from Libs.Core import cmd_parser, enum, etl_parser, display_power
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.logger import etl_tracer, gdhm
from Libs.Core.test_env import test_context

##
# @brief Default power event duration in seconds
POWER_EVENT_DURATION = 30
DIANA_ETL_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna\\")
DIANA_EXE = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna\\DiAna.exe")
JSON_OUTPUT = os.path.join(test_context.ROOT_FOLDER, 'ValReport.json')
GFX_TRACE_ETL_FILE = os.path.join(DIANA_ETL_PATH, "GfxTrace.etl")
# Below DDI targets are fixed as per discussion with Dev/Arch. HSD will be filed if not meeting the target values.
# Values cannot be changed without Dev/Arch team suggestions.
DDI = {etl_parser.Ddi.DDI_SETTIMINGSFROMVIDPN.name: {'S4': 1100, 'S3': 700, 'CS': 250},
       etl_parser.Ddi.DDI_SET_POWER_STATE.name: {'S4': 60, 'S3': 110, 'CS': 35},
       etl_parser.Ddi.DDI_SETTARGETGAMMA.name: {'S4': 15, 'S3': 15, 'CS': 15},
       etl_parser.Ddi.DDI_DISPLAYDETECTCONTROL.name: {'S4': 20, 'S3': 20, 'CS': 20},
       etl_parser.Ddi.DDI_INTERRUPT_ROUTINE.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_ESCAPE.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_SETVIDPNSOURCEADDRESSWITHMULTIPLANEOVERLAY3.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_ISSUPPORTEDVIDPN.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_SETVIDPNSOURCEVISIBILITY.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_CONTROLINTERRUPT2.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDISETPOWERCOMPONENTFSTATE.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_BLC_SET_BRIGHTNESS.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_QUERYCONNECTIONCHANGE.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_QUERY_DEVICE_DESCRIPTOR.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_GETMULTIPLANEOVERLAYCAPS.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_SETPOINTERPOSITION.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_GETPOSTCOMPOSITIONCAPS.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_DPC.name: {'S4': 5, 'S3': 5, 'CS': 5},
       etl_parser.Ddi.DDI_WORK_ITEM.name: {'S4': 5, 'S3': 5, 'CS': 5}}


##
# @class ResponsivenessBase
# @brief Common Base Class for Responsiveness Test Cases
class ResponsivenessBase(unittest.TestCase):
    command_line_tags = ['-POWER_EVENT']
    cmd_line_param = None
    display_list = []
    plugged_display = []
    ddi_error = []
    step_counter = 0
    ddi_count = 0
    gdhm_error_msg = None

    display_config = DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    # Power Event
    power_event_status = False
    power_event_type = None
    power_event_str = None
    error_check = False

    ##
    # @brief Unit Test Setup Function
    # @return None
    def setUp(self):
        # Gets the display connected from the command line
        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, self.command_line_tags)
        self.display_list = cmd_parser.get_sorted_display_list(self.cmd_line_param)

        # set POWER_EVENT based on the command line
        expected_cs_status = False
        if self.cmd_line_param['POWER_EVENT'] != 'NONE':
            self.power_event_status = True
            expected_cs_status = False
            if self.cmd_line_param['POWER_EVENT'][0] == 'CS':
                self.power_event_type = display_power.PowerEvent.CS
                self.power_event_str = "CS"
                expected_cs_status = True

            if self.cmd_line_param['POWER_EVENT'][0] == 'S3':
                self.power_event_type = display_power.PowerEvent.S3
                self.power_event_str = "S3"
                expected_cs_status = False

            if self.cmd_line_param['POWER_EVENT'][0] == 'S4':
                self.power_event_type = display_power.PowerEvent.S4
                self.power_event_str = "S4"
                expected_cs_status = None

            # Make sure system CS state is as expected
            # Fails if CS is not enabled
            if expected_cs_status is not None:
                if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) != expected_cs_status:
                    self.fail(
                        f"Connected Standby is not {'enabled' if expected_cs_status else 'disabled'} on the system")

    ##
    # @brief Invokes the specified power event
    # @param[in] power_event power event state to be invoked
    # @return None
    def base_invoke_power_event(self, power_event= display_power.PowerEvent.S3):
        # Invoke Power event based on the command line
        self.step_counter += 1
        if self.display_power_.invoke_power_event(power_event, POWER_EVENT_DURATION) is False:
            gdhm.report_driver_bug_os(title=f"[DDI_Responsiveness] Failed To Invoke Power Event: {power_event.name}")
            self.fail('Failed to invoke power event {0}'.format(power_event.name))

    ##
    # @brief        Exposed API to invoke the power event based on the command line
    # @return       new_etl_file, location of generated ETL file
    def run_etl_file(self):
        # Start ETL tracer
        logging.info("******************** START ETL Trace logs (test) *************************")
        if etl_tracer.start_etl_tracer() is False:
            logging.error("FAILED to start ETL Tracer(Test Issue)")
            return False

        # Invoke the power event based on the power_event type (CS/S3/S4)
        self.base_invoke_power_event(power_event=self.power_event_type)

        # Stop ETL tracer
        if etl_tracer.stop_etl_tracer() is False:
            logging.error("\tFAILED to stop ETL Tracer(Test Issue)")
            return False
        logging.info("************************ END ETL Trace logs ****************************")

        # Make sure etl file is present
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE) is False:
            logging.error(etl_tracer.GFX_TRACE_ETL_FILE + " NOT found.")
            return False

        # Remove etl file if already present
        file_path = os.path.join(DIANA_ETL_PATH, "GfxTrace.etl")
        if os.path.exists(file_path):
            os.remove(file_path)

        # Rename the ETL file to avoid overwriting
        new_etl_file = shutil.move(etl_tracer.GFX_TRACE_ETL_FILE, DIANA_ETL_PATH)

        return new_etl_file

    ##
    # @brief helper function to parse the etl file to Diana
    # @param[in] etl_file_path GfxTrace file collected
    # @return DDI values from Diana
    def run_diana(self, etl_file_path=None):
        # Check if etl_file exists or not
        if not os.path.exists(etl_file_path):
            logging.error("{0} NOT found".format(etl_file_path))
            return None

        # Check whether DiAna exe exists or not
        if not os.path.exists(DIANA_EXE):
            logging.error("{0} NOT found (Test Issue)".format(DIANA_EXE))
            return None

        etl_parser.generate_report(etl_file_path)
        # Executes diana command
        os.system(DIANA_EXE + " " + etl_file_path)
        for ddi_name, ddi_value in DDI.items():
            self.verify_ddi_values(name=ddi_name)
        # Move json output to Logs folder
        shutil.move(JSON_OUTPUT, test_context.LOG_FOLDER)
        shutil.move(GFX_TRACE_ETL_FILE, test_context.LOG_FOLDER)
        if self.error_check:
            self.fail("DDI values are not as expected")

    ##
    # @brief        helper function to verify ddi values
    # @param[in]    name - DDI name to verify
    # @return       None
    def verify_ddi_values(self, name=None):
        if not os.path.exists(JSON_OUTPUT):
            logging.error("ValReport.json file NOT found")
        # Fetch data from json
        with open(JSON_OUTPUT) as js_handle:
            json_data = json.load(js_handle)
        for i in json_data.values():
            for js_data in i:
                # Get the DDI values from Json file
                first_set = js_data.get('DDIResumeDetails')
                for value in first_set:
                    for key, val in value.items():
                        if val == name:
                            # Gets the actual value and the count from json
                            exe_time = value.get('TotalExecutionTime')
                            count = value.get('Count')
                            # Calculating actual value based on the number of calls(cumulative value/number of calls)
                            actual_val = round(round(exe_time, 2)/count, 2)
                            for ddi_name, ddi_value in DDI.items():
                                if ddi_name == name:
                                    for power_event, expected_val in ddi_value.items():
                                        if power_event == self.power_event_str:
                                            if expected_val < actual_val:
                                                logging.error("FAIL: {0}: Expected:{1} Actual:{2}".format(name,
                                                                                                          expected_val,
                                                                                                          actual_val))
                                                gdhm.report_driver_bug_os(
                                                    title=f"[DDI_Responsiveness] {name} is taking more time than expected")
                                                if ddi_name != etl_parser.Ddi.DDI_SETTARGETGAMMA.name or ddi_name != \
                                                        etl_parser.Ddi.DDI_DISPLAYDETECTCONTROL.name:
                                                    self.error_check = True
                                            else:
                                                logging.info("PASS: {0}: Expected:{1} Actual:{2}".format(name,
                                                                                                         expected_val,
                                                                                                         actual_val))
