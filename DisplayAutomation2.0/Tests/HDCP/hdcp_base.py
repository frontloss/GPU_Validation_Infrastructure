#####################################################################################################
# @file          hdcp_base.py
# @brief         It contains setUp, tearDown and helper methods for all hdcp tests
# @details       @ref hdcp_base.py <br>
#                This file implements unittest default functions for setUp and tearDown,
#                hdcp verification functions used across all hdcp tests, and helper functions.
# @author        chandrakanth reddy y
#####################################################################################################

import logging
import os
import random
import re
import shutil
import sys
import time
import unittest
from subprocess import Popen, PIPE
from threading import Thread
from enum import IntEnum

import win32serviceutil

from Libs.Core import cmd_parser, enum
from Libs.Core import display_utility
from Libs.Core import reboot_helper
from Libs.Core import display_essential
from Libs.Core import window_helper
from Libs.Core.display_config import display_config as disp_cfg
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_power import DisplayPower, MonitorPower, PowerEvent
from Libs.Core.hw_emu.hotplug_emulator_utility import HotPlugEmulatorUtility
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.manual.modules import alert
from registers.mmioregister import MMIORegister
from Libs.Core.vbt.vbt import Vbt

POWER_EVENT_DURATION = 60
OPM_LITE_RE_INTIALIZE_DURATION = 20  # wait time for OPM-lite to re-intialize after event(hotplug/display switch..)
HDCP_ENABLE_CHECK_DURATION = 30  # wait time to make sure no linklost occured after HDCP Enable
MANUAL_DISPLAY_LIST = ['LSPCON_HDMI', 'USB-C=>HDMI', 'USB-C=>DP', 'DP=>DVI']
HDCP_SERVICE = "Intel(R) Content Protection HDCP Service"
OPM_TESTER_EXE = "OPMTester.exe"

OPMTEST_BINARY_PATH = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "HDCP")
port_connector_type = {}

# Platform details for all connected adapters
PLATFORM_INFO = {
    gfx_index: {
        'gfx_index': gfx_index,
        'name': adapter_info.get_platform_info().PlatformName
    }
    for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
}


##
# @brief        Check whether the service is running or not
# @param[in]    service  service name
# @return       True if service is running, False otherwise
def is_service_running(service):
    return win32serviceutil.QueryServiceStatus(service)[1] == 4


##
# @brief Exposed enum class for supported HDCP types
class HDCPType(IntEnum):
    HDCP_1_4 = 0
    HDCP_2_2 = 1


##
# @brief Provides setUp and tearDown methods of unittest framework and HDCP activate/deactivate verification methods
class HDCPBase(unittest.TestCase):
    enumerated_displays = None
    display_list = []
    attached_display_list = []
    ext_displays = []
    hdcp_type = HDCPType.HDCP_1_4
    is_hotplug_test_case = False
    is_monitor_turn_off = False
    mst_depth = 0

    display_config = disp_cfg.DisplayConfiguration()
    display_power = DisplayPower()
    hotplug_emulator_utility = HotPlugEmulatorUtility()

    ##
    # @brief    Unittest Setup function
    # @return   None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.display_list = []
        # Check tool is present or not
        # If the tool is not available exit the test
        if os.path.exists(os.path.join(OPMTEST_BINARY_PATH, "OPMTester.exe")) is False:
            self.fail("OPM tool is not present")
        # HDCP service is required for only Integrated graphics platforms
        if PLATFORM_INFO['gfx_0']['name'] not in ['DG1', 'DG2', 'DG3']:
            if is_service_running(HDCP_SERVICE) is False:
                self.fail("HDCP Service is not running")

        if display_essential.is_process_running(OPM_TESTER_EXE):
            window_helper.kill_process_by_name(OPM_TESTER_EXE)

        try:
            self.attached_display_list = []
            self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv,
                                                           ['-HDCPTYPE', '-HOTPLUG', '-POWER_EVENT', '-Display1',
                                                            '-Display2', '-Display3', '-Display4', '-DEPTH'])

            # Set HDCP Type
            if self.cmd_line_param['HDCPTYPE'] != 'NONE':
                if self.cmd_line_param['HDCPTYPE'][0] == '0':
                    self.hdcp_type = HDCPType.HDCP_1_4
                else:
                    if self.cmd_line_param['HDCPTYPE'][0] == '1':
                        self.hdcp_type = HDCPType.HDCP_2_2
                    else:
                        self.fail("Invalid value for parameter HDCPTYPE. Supported values are [{0}, {1}]".format(
                            HDCPType.HDCP_1_4.value, HDCPType.HDCP_2_2.value))

            # Check for Hotplug/Unplug Test Cases
            if self.cmd_line_param['HOTPLUG'] != 'NONE':
                if self.cmd_line_param['HOTPLUG'][0] == 'TRUE':
                    self.is_hotplug_test_case = True
                else:
                    if self.cmd_line_param['HOTPLUG'][0] == 'FALSE':
                        self.is_hotplug_test_case = False
                    else:
                        self.fail("Invalid value for parameter HOTPLUG. Supported values are [True, False]")

            # check for Power event test cases
            if self.cmd_line_param['POWER_EVENT'] != 'NONE':
                if self.cmd_line_param['POWER_EVENT'][0] == 'CS':
                    self.power_event = PowerEvent.CS
                    self.is_cs_system_expected = True
                elif self.cmd_line_param['POWER_EVENT'][0] == 'S3':
                    self.power_event = PowerEvent.S3
                    self.is_cs_system_expected = False
                elif self.cmd_line_param['POWER_EVENT'][0] == 'S4':
                    self.power_event = PowerEvent.S4
                    self.is_cs_system_expected = False
                elif self.cmd_line_param['POWER_EVENT'][0] == 'MTO':
                    self.power_event = MonitorPower.OFF_ON
                    self.is_monitor_turn_off = True
                    self.is_cs_system_expected = False
                else:
                    self.fail("Invalid value for parameter POWER EVENT. Supported values are [ CS, S3, S4, MTO ]")

            # Check for Hotplug/Unplug Test Cases
            if self.cmd_line_param['DEPTH'] != 'NONE':
                self.mst_depth = int(self.cmd_line_param['DEPTH'][0])
                if self.mst_depth < 2 or self.mst_depth > 3:
                    self.fail("Invalid value for Depth. Expected value 2/3")
            if self.hdcp_type == HDCPType.HDCP_1_4:
                for adapter in PLATFORM_INFO.values():
                    gfx_index = adapter['gfx_index']
                    hdcp_key_status = MMIORegister.read('HDCP_KEY_STATUS_REGISTER', 'HDCP_KEY_STATUS', adapter['name'],
                                                        gfx_index=gfx_index)
                    if not (hdcp_key_status.key_load_done and hdcp_key_status.key_load_status):
                        self.fail("HDCP 1.4 keyLoad failed for {}. Please check DAM is disabled or not".format(
                            adapter['name']))
                    logging.info("HDCP 1.4 keys already Loaded")

            if PLATFORM_INFO['gfx_0']['name'] not in ['GLK', 'ICLLP'] and self.is_hotplug_test_case is False:
                # Create a set of valid connector_ports from passed arguments
                for key, value in self.cmd_line_param.items():
                    if cmd_parser.display_key_pattern.match(key) is not None:
                        if value['connector_port'] is not None:
                            self.display_list.insert(value['index'], value['connector_port'])
                # negative test is verified with simulated displays. SKIP connection status check
                if not sys.argv[0].__contains__('negative_test'):
                    # Collect the display details in enumerated displays from cmdline
                    self.enumerated_displays = self.display_config.get_enumerated_display_info()
                    # Verify the plugged displays for non hotplug/unplug test cases
                    for count in range(len(self.display_list)):
                        is_display_found = False
                        for index in range(self.enumerated_displays.Count):
                            if self.display_list[count] == CONNECTOR_PORT_TYPE(
                                    self.enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name:
                                is_display_found = True

                        if is_display_found is False:
                            self.fail("Display %s is not plugged correctly" % self.display_list[count])
            else:
                self.parse_north_gate_cmd_lines()

            # Remove previous logs
            files = os.listdir(os.getcwd())
            for filename in filter(lambda x: re.match('hdcp_log*', x), files):
                os.remove(filename)
            if os.path.exists('./opm_tester.txt'):
                os.remove('opm_tester.txt')
            logging.debug("Successfully removed previous log files")

        except Exception as e:
            # If any Exception happens: Call teardown and fail the test
            self.tearDown()
            self.fail(e)

    ##
    # @brief    Unittest tearDown function
    # @return   None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info("*********** IN TEAR DOWN ****************")
        logging.debug("OPM output : {}".format(self.exit_opm()))

    ##
    # @brief    Exposed function to parse north gate cmd-line
    # @return   None
    def parse_north_gate_cmd_lines(self):
        retry_count = 1
        # get the displays passed in cmd_line
        if self.cmd_line_param['DISPLAY1'] != 'NONE':
            if "EDP" in self.cmd_line_param['DISPLAY1'][0] or \
                    "MIPI" in self.cmd_line_param['DISPLAY1'][0]:
                self.attached_display_list.append(self.cmd_line_param['DISPLAY1'][0].split(' ')[0])

            elif self.is_hotplug_test_case:
                display = self.cmd_line_param['DISPLAY1'][0].split()
                self.attached_display_list.append(display[2] + "_" + display[-1].replace(')', ''))
            else:
                self.attached_display_list.append(self.cmd_line_param['DISPLAY1'][0].split(' ')[2])

        if self.cmd_line_param['DISPLAY2'] != 'NONE':
            if "EDP" in self.cmd_line_param['DISPLAY2'][0] or \
                    "MIPI" in self.cmd_line_param['DISPLAY2'][0]:
                self.attached_display_list.append(self.cmd_line_param['DISPLAY2'][0].split(' ')[0])
            elif self.is_hotplug_test_case:
                display = self.cmd_line_param['DISPLAY2'][0].split()
                self.attached_display_list.append(display[2] + "_" + display[-1].replace(')', ''))

            else:
                self.attached_display_list.append(self.cmd_line_param['DISPLAY2'][0].split(' ')[2])

        if self.cmd_line_param['DISPLAY3'] != 'NONE':
            if self.is_hotplug_test_case:
                display = self.cmd_line_param['DISPLAY3'][0].split()
                self.attached_display_list.append(display[2] + "_" + display[-1].replace(')', ''))
            else:
                self.attached_display_list.append(self.cmd_line_param['DISPLAY3'][0].split(' ')[2])

        if self.cmd_line_param['DISPLAY4'] != 'NONE':
            if self.is_hotplug_test_case:
                display = self.cmd_line_param['DISPLAY4'][0].split()
                self.attached_display_list.append(display[2] + "_" + display[-1].replace(')', ''))
            else:
                self.attached_display_list.append(self.cmd_line_param['DISPLAY4'][0].split(' ')[2])

        if self.is_hotplug_test_case is True:
            while retry_count:
                display_list = self.get_display_data()
                missed_display = list(set(display_list).symmetric_difference(self.attached_display_list))

                for display in missed_display:
                    if display not in self.attached_display_list:
                        alert.error(
                            "{} Display not planned in Test Grid but found in enumerated list "
                            "(connected displays).Please unplug Display and click OK to continue test".format(display))
                        retry_count = 1

                    else:
                        alert.error("Display {} not plugged properly.Try re-plug the cable".
                                    format(missed_display))
                        retry_count = 1
                if not len(missed_display):
                    # All planned displays connected .exit from the while loop
                    break
        else:
            display_list = self.get_display_data()
            if len(self.attached_display_list) < len(self.display_list):
                for display in display_list:
                    if display not in self.attached_display_list:
                        self.display_list.pop(display_list.index(display))
            elif len(self.attached_display_list) > len(self.display_list):
                for display in self.attached_display_list:
                    if display not in display_list:
                        self.fail(" {} Display not connected".format(display))

    ##
    # @brief   get planned and enumerated display data
    # @return  display_list list of connected displays
    def get_display_data(self):
        self.display_list = []
        # Collect the display details in enumerated displays from cmdline
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        for index in range(self.enumerated_displays.Count):
            self.display_list.insert(index, CONNECTOR_PORT_TYPE(
                self.enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name)

        logging.info("enumerated displays ={}".format(self.display_list))
        logging.info("planned Grid displays = {}".format(self.attached_display_list))
        self.attached_display_list = ['DP' if display in MANUAL_DISPLAY_LIST else display for display in
                                      self.attached_display_list]
        display_list = [display.split('_')[0] if self.is_hotplug_test_case is False else display for display in
                        self.display_list]
        if 'DP_A' in self.display_list:
            index = self.display_list.index('DP_A')
            display_list[index] = "EDP"
        return display_list

    ##
    # @brief       Verify whether displays are connected in daisy chain mode on given DP port
    # @param[in]   port DP port to be verified
    # @param[in]   depth mst MST topology depth(No.of branch devices)
    # @return      True if verification successful otherwise false
    def verify_mst(self, port, depth):
        enumerated_displays = self.display_config.get_enumerated_display_info()
        display_list = [display for display in enumerated_displays.ConnectedDisplays
                        if CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name.lower() == port.lower()]
        if len(display_list) == depth:
            logging.info("DP Displays are connected in Daisy Chain mode")
            return True
        else:
            logging.error("DP Displays are not connected in Daisy chain mode on {}".format(port))
            return False

    ##
    # @brief   Method to verify HDCP using OPM Lite tool
    # @return  True if HDCP verification passes, False otherwise
    def base_verify_hdcp(self):
        status = False

        for i in range(1, 6):
            # Start the automation commandline
            logging.info("--------------- HDCP Verify Iteration {} start -----------------------".format(i))
            if self.hdcp_type == HDCPType.HDCP_1_4:
                os.system(os.path.join(OPMTEST_BINARY_PATH, "OPMTester.exe") + " -type0 > hdcp_log.txt")
            else:
                os.system(os.path.join(OPMTEST_BINARY_PATH, "OPMTester.exe") + " -type1 > hdcp_log.txt")

            # wait for the HDCP test to complete and log file generation.
            time.sleep(15)

            # check the results(total, pass, fail) and display information(port_id, HDCPCapability, ConnectorType)
            [display_info, test_result] = self.parse_log_file()
            # check the display_info is bool or list .if File has no content display_info,test_result will be FALSE
            if isinstance(display_info, list):
                if len(display_info):
                    for display in display_info:
                        if display['HDCPCapability'] is True:
                            if display['HDCP_TYPE'] != self.hdcp_type:
                                if self.hdcp_type == HDCPType.HDCP_1_4 and display['HDCP_TYPE'] != HDCPType.HDCP_2_2:
                                    self.fail(
                                        "Iteration {} - FAIL: Expected HDCP 1.4 Panel, Actual= HDCP UnSupported Panel".
                                            format(i))
                                if self.hdcp_type == HDCPType.HDCP_2_2:
                                    self.fail(
                                        "Iteration {} - FAIL: Expected HDCP 2.2 Panel, Actual= HDCP 1.4 Panel".format(
                                            i))
                            else:
                                if self.hdcp_type == HDCPType.HDCP_1_4:
                                    logging.info(
                                        "Iteration {} - PASS: Expected HDCP 1.4 Panel, Actual= HDCP 1.4 Panel".format(
                                            i))
                                if self.hdcp_type == HDCPType.HDCP_2_2:
                                    logging.info(
                                        "Iteration {} - PASS: Expected HDCP 2.2 Panel, Actual= HDCP 2.2 Panel".format(
                                            i))

                else:
                    logging.error("Iteration {} - FAIL: Display Connector Data is missing.".format(i))
            else:
                logging.error("Iteration {} - FAIL: HDCP log file is Empty or file not generated".format(i))

            # Condition for checking test results are updated correctly
            if test_result is not False:
                if len(test_result):
                    if test_result['total_test_cases'] and test_result['total_pass']:
                        if test_result['total_fail'] == '0' and \
                                (test_result['total_test_cases'] != '0') and \
                                (test_result['total_test_cases'] == test_result['total_pass']):
                            status = True
                        else:
                            logging.error(" Test case is Failed due to some internal error")
                            status = False
                            break
                else:
                    logging.error("Iteration {} - FAIL: test_result data is Empty.It may be due to hdcp_log File is "
                                  "not generated or file is Empty".format(i))
            logging.info("-------------- HDCP Verify Iteration {} End -------------------".format(i))
        return status

    ##
    # @brief   Method to parse the OPM Lite tool log
    # @return  display_info and test_result
    def parse_log_file(self):
        current_line_index = 0
        is_display_info_set = False
        test_result = {}  # stores the results for test; test_result{total, fail, pass}
        display_info = []  # stores the display information for all the available displays

        # if the log file is not generated, exit
        logging.info("STEP: Started parsing the OPM log")
        if os.path.exists("hdcp_log.txt") is False:
            self.fail("FAIL: Log file hdcp_log.txt is not generated")

        try:
            log_file = open("hdcp_log.txt", "r")
        except IOError:
            self.fail('FAIL: Failed to open hdcp_log.txt')
        else:
            lines = log_file.readlines()
            log_file.close()

        if len(lines) < 1:
            self.fail('FAIL: hdcp_log.txt file is Empty')

        for line in lines:
            display_info_property_list = line.strip().split("\t")
            if len(display_info_property_list) < 1:
                continue

            # port_id, HDCPCapability, HDCPLocalLevel, ConnectorType for all connected display_path
            if display_info_property_list[0] == "port_id" and is_display_info_set is False:
                next_line_index = current_line_index + 2

                display_info_property_data = lines[next_line_index].strip()
                if len(display_info_property_data) > 0:
                    while display_info_property_data[0] != '*':
                        display_info_temp = {
                            'port_id': display_info_property_data[0],
                            'HDCPCapability': False,
                            'HDCP_TYPE': None
                        }
                        if display_info_property_data.find('Not Supported') == -1:
                            display_info_temp['HDCPCapability'] = True
                            if display_info_property_data.find('HDCP_TYPE_ENFORCEMENT') == -1:
                                display_info_temp['HDCP_TYPE'] = 0
                            else:
                                display_info_temp['HDCP_TYPE'] = 1

                        display_info.append(display_info_temp)
                        next_line_index += 1
                        display_info_property_data = lines[next_line_index].strip()

                        if len(display_info_property_data) > 0:
                            continue
                        else:
                            break
                is_display_info_set = True

            # Total test cases, Total Fail, Total Pass
            if len(display_info_property_list[0]) > 0:
                if display_info_property_list[0][0] == '#':
                    result = display_info_property_list[0][2:].split(": ")
                    if result[0] == 'Total TestCases':
                        test_result['total_test_cases'] = result[1]
                    if result[0] == 'Total Pass':
                        test_result['total_pass'] = result[1]
                    if result[0] == 'Total Fail':
                        test_result['total_fail'] = result[1]

            current_line_index += 1
        logging.info("PASS: OPM Log Parsing successful")
        return [display_info, test_result]

    ##
    # @brief         Exposed API to plug EFP via SHE tool
    # @param[in]     port string required port to hot plug EFP
    # @return        True if hot plug is successful, False otherwise
    def she_hot_plug(self, port):

        # Hotplug the port using SHE tool
        if self.hotplug_emulator_utility.hot_plug(port, 5):
            time.sleep(30)
        else:
            logging.error("Unable to hotplug {}".format(port))
            return False

        # Check if hotplug is successful
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if disp_cfg.is_display_attached(enumerated_displays, port) is True:
            logging.info("{} PLUG Successful".format(port))
            return True
        else:
            logging.error("{} PLUG Failed".format(port))
            return False

    ##
    # @brief          Exposed API to hot unplug EFP via SHE tool
    # @param[in]      port string required port to unplug EFP
    # @return         True if hot unplug is successful otherwise False
    def she_hot_unplug(self, port):

        if self.hotplug_emulator_utility.hot_unplug(port, 5):
            time.sleep(30)
        else:
            logging.error("Unable to unplug {}".format(port))
            return False

        enumerated_displays = self.display_config.get_enumerated_display_info()
        if disp_cfg.is_display_attached(enumerated_displays, port) is True:
            logging.error("{} Unplug not Successful".format(port))
            return False
        else:
            logging.info("{} Unplug Success".format(port))
            return True

    ##
    # @brief       Manually hot plug the display
    # @param[in]   display  string port_id
    # @return      True if hot plug is successful, False otherwise
    def manual_hot_unplug_plug(self, display):
        if self.manual_hot_unplug(display) is False:
            return False
        # plug the display
        alert.info('Plug the Display and click OK to continue ' + str(display))
        # delay for display detection after plug
        time.sleep(5)
        # Check if hotplug is successful
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if disp_cfg.is_display_attached(enumerated_displays, display) is True:
            logging.info("{} PLUG Successful".format(display))
            return True
        else:
            logging.error("{} PLUG Failed".format(display))
            return False

    ##
    # @brief       Manually unplug the display
    # @param[in]   display string port_id
    # @return      True if hot unplug is successful, False otherwise
    def manual_hot_unplug(self, display):

        # unplug the display
        alert.info('unplug the Display ' + str(display))
        # min delay required for unplug the display manually
        time.sleep(5)
        # check display unplug is success
        enumerated_displays = self.display_config.get_enumerated_display_info()
        if disp_cfg.is_display_attached(enumerated_displays, display) is True:
            logging.error("{} Unplug not Successful".format(display))
            return False
        else:
            logging.info("{} Unplug Success".format(display))
            return True

    ##
    # @brief       Method to verify HDCP for single display
    # @param[in]   disable bool specifies whether HDCP needs to disabled after verification
    # @param[in]   is_negative bool specifies whether the test is a negative scenario
    # @return      True if HDCP verification is successful, False otherwise
    def single_display_single_session(self, disable=False, is_negative=False):

        status = False
        # Open the session
        self.session = OPMSession(self.hdcp_type)
        logging.info("OPM Session started successfully")

        # Enable HDCP for the session
        if self.hdcp_type == HDCPType.HDCP_1_4:
            self.session.enable_type0()
        else:
            if self.hdcp_type == HDCPType.HDCP_2_2:
                self.session.enable_type1()
            else:
                logging.error("FAIL : Invalid HDCP capability Passed")
                return False

        # Get the local level status
        local_status = self.session.get_local_status()

        # Get the global level status
        global_status = self.session.get_global_status()

        logging.info("Global level : {0} and Local level: {1} are as expected".format(local_status['code'],
                                                                                      global_status['code']))
        # Verifying global and local status
        if local_status['status'] is True and global_status['status'] is True:
            logging.info("PASS: HDCP_TYPE {0} enabled successfully".format(self.hdcp_type))
            status = True
        elif is_negative:
            return status
        else:
            logging.error('FAIL: Activating HDCP_TYPE {0} failed on display '.format(self.hdcp_type))
            return False
        if disable:
            # disable HDCP for the session
            self.session.disable()

            # Get the local level status
            local_status = self.session.get_local_status()

            # Get the global level status
            global_status = self.session.get_global_status()

            # Verifying global and local status
            if local_status['status'] is False and global_status['status'] is False:
                logging.info("Global level : {0} and Local level: {1} are as expected".format(local_status['code'],
                                                                                              global_status['code']))
                logging.info("PASS: HDCP_TYPE {0} disabled successfully on display ".format(self.hdcp_type))
                status = True
            else:
                status = False
                gdhm.report_bug(
                    title="[HDCP][OPM] Failed to disable HDCP Type {}".format(self.hdcp_type),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error('FAIL: Deactivating HDCP_TYPE {0} failed on display '.format(self.hdcp_type))
        return status

    ##
    # @brief       Method to verify HDCP for single display with multiple opm sessions
    # @param[in]   disable specifies whether HDCP needs to disabled after verification
    # @return      True if HDCP verification is successful else return False
    def single_display_multi_session(self, disable=False):
        status = False

        time.sleep(1)
        # Open the session 1
        self.session1 = OPMSession(self.hdcp_type)
        logging.info("STEP : OPM Session 1 started successfully")

        time.sleep(5)

        # Open the session 2
        self.session2 = OPMSession(self.hdcp_type)
        logging.info("STEP: OPM Session 2 started successfully")

        time.sleep(1)

        # Enable HDCP for the session 1
        if self.hdcp_type == HDCPType.HDCP_1_4:
            enable_status = self.session1.enable_type0()
        else:
            if self.hdcp_type == HDCPType.HDCP_2_2:
                enable_status = self.session1.enable_type1()
            else:
                logging.error("FAIL: Invalid HDCP capability passed as an argument")
                return False

        # Get the local level status for session 1
        local_status = self.session1.get_local_status()

        # Get the global level status for session 1
        global_status = self.session1.get_global_status()

        # Verifying global and local status for session 1
        if local_status['status'] is True and global_status['status'] is True:
            logging.info(
                "Global level : {} and Local level: {} are as expected for session 1".format(local_status['code'],
                                                                                             global_status['code']))
            logging.info("PASS: HDCP_TYPE {} enabled successfully for session 1".format(self.hdcp_type))
            status = True
        else:
            logging.error('FAIL: HDCP_TYPE {} verification failed for session 1'.format(self.hdcp_type))
            return False

        # Enable HDCP for the session 2
        if self.hdcp_type == 0:
            enable_status = self.session2.enable_type0()
        else:
            if self.hdcp_type == 1:
                enable_status = self.session2.enable_type1()
            else:
                logging.error("FAIL: Invalid HDCP capability passed in session 2")
                return False

        # Get the local level status for session 2
        local_status = self.session2.get_local_status()

        # Get the global level status for session 2
        global_status = self.session2.get_global_status()

        if local_status['status'] is True and global_status['status'] is True:
            logging.info(
                "Global level : {} and Local level: {} are as expected for session 2".format(local_status['code'],
                                                                                             global_status['code']))
            logging.info("PASS: HDCP_TYPE {} enabled successfully for session 2".format(self.hdcp_type))
            status = True
        else:
            logging.error("FAIL: HDCP_TYPE {} verification failed for session 2".format(self.hdcp_type))
            return False
        if disable:
            logging.info("STEP: HDCP Disabling started for session 2")
            # disable HDCP for the session 2
            self.session2.disable()

            # Get the local level status for session 2
            local_status = self.session2.get_local_status()

            # Get the global level status for session 2
            global_status = self.session2.get_global_status()

            if local_status['status'] is False and global_status['status'] is True:
                logging.info(
                    "Global level : {} and Local level: {} are as expected for session 2".format(local_status['code'],
                                                                                                 global_status['code']))
                logging.info("PASS: HDCP_TYPE {} disabled successfully for session 2".format(self.hdcp_type))
                status = True
            else:
                logging.error("FAIL: HDCP_TYPE {} verification failed for session 2".format(self.hdcp_type))
                return False

            logging.info("STEP: HDCP Disabling started for session 1")
            # disable HDCP for the session 1
            self.session1.disable()

            # Get the local level status for session 1
            local_status = self.session1.get_local_status()

            # Get the global level status for session 1
            global_status = self.session1.get_global_status()

            if local_status['status'] is False and global_status['status'] is False:
                logging.info(
                    "Global level : {} and Local level: {} are as expected for session 1".format(local_status['code'],
                                                                                                 global_status['code']))
                logging.info("PASS: HDCP_TYPE {} disabled successfully for session 1".format(self.hdcp_type))
                status = True
            else:
                status = False
                logging.error("FAIL: HDCP_TYPE {} verification failed for session 1".format(self.hdcp_type))
        return status

    ##
    # @brief       Method to verify HDCP for multi display with single opm session
    # @param[in]   disable bool specifies whether HDCP needs to disabled after verification
    # @param[in]   is_negative bool specifies whether the test is a negative scenario
    # @return      True if HDCP verification is successful, False otherwise
    def multi_display_single_session(self, disable=False, is_negative=False):
        status = False
        hdcp_displays = []
        self.session = OPMSession(self.hdcp_type)

        # get connected displays
        display_info = self.session.get_display_info()
        if display_info:
            connected_display_count = len(display_info['ports'])
            for current_display in range(0, connected_display_count):
                hdcp_type = display_info['ports'][current_display]['HDCP_TYPE']
                if hdcp_type is not None:
                    if hdcp_type != self.hdcp_type:
                        logging.error("HDCP capability mismatch. Expected Hdcp type = {0} and Actual = {1}".format(
                            HDCPType(self.hdcp_type).name, HDCPType(hdcp_type).name))
                        return False
                    hdcp_displays.append(current_display)
                    logging.info("Enable HDCP Type %r" % self.hdcp_type)
                    status = self.enable_hdcp(current_display, is_negative)
                else:
                    logging.warning("Non - HDCP Panel is connected on Port {}".format(current_display))
            if disable:
                for display in hdcp_displays:
                    status = self.disable_hdcp(display)

        return status

    ##
    # @brief       This function is used to enable hdcp for the given port Number,
    #              In multiple displays, single HDCP session is activated and verified
    # @param[in]   port_id int port to enable the HDCP
    # @param[in]   is_negative bool specifies whether the test is a negative scenario
    # @return      True if HDCP verification is successful else return False
    def enable_hdcp(self, port_id=None, is_negative=False):
        status = False
        # Enable HDCP for the session
        if self.hdcp_type == HDCPType.HDCP_1_4:
            logging.info("STEP: HDCP Type 0 Enable for Port %r" % int(port_id or 0))
            self.session.enable_type0(port_id)
        else:
            if self.hdcp_type == HDCPType.HDCP_2_2:
                logging.info("STEP: Type 1 Enable for Port %r" % int(port_id or 0))
                self.session.enable_type1(port_id)
            else:
                logging.error("FAIL: Invalid HDCP Capability passed as argument")
                return False
        time.sleep(2)
        self.session.hdcp_type = self.hdcp_type
        global_status = self.session.get_global_status(port_id)
        local_status = self.session.get_local_status(port_id)

        if local_status['status'] is True and global_status['status'] is True:
            logging.info(" Local protection level :{} and Global Protection level :{} are as Expected".format(
                local_status['code'], global_status['code']))
            logging.info("PASS: HDCP_TYPE %d enabled successfully for port %d" % (self.hdcp_type, int(port_id or 0)))
            status = True

        else:
            msg = "local Protection level = {0} and global Protection level = {1}".format(local_status['code'],
                                                                                          global_status['code'])
            if is_negative:
                logging.info("PASS: " + msg)
                return status
            logging.error("FAIL: " + msg)
            gdhm.report_bug(
                title="[HDCP][OPM] Failed to enable HDCP Type {}".format(self.hdcp_type),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return status

    ##
    # @brief       This function is used to verify hdcp for the given port Number
    #              HDCP protection level is verified for the given port number
    # @param[in]   port_id
    # @return      True if HDCP verification is successful else return False
    def query_global_and_local_level(self, port_id=None):
        status = False
        local_status = self.session.get_local_status(port_id)
        global_status = self.session.get_global_status(port_id)
        if local_status['status'] is True and global_status['status'] is True:
            logging.info("PASS: HDCP verified successfully for port %d" % int(port_id or 0))
            status = True
        else:
            logging.error("FAIL: local protection level = %r and global protection level = %r on port = %r" %
                          (local_status['code'], global_status['code'], int(port_id or 0)))
            logging.error('FAIL: HDCP Global and Local level verification failed')
            gdhm.report_bug(
                title="[HDCP][OPM] Global and local protection level is OFF",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return status

    ##
    # @brief       This function is used to disable hdcp protection for the given display
    # @param[in]   current_display port number
    # @return      True if HDCP disable is successful else return False
    def disable_hdcp(self, current_display=None):
        status = False
        logging.info("STEP: HDCP is Disabling for the port %d" % int(current_display or 0))
        self.session.disable(current_display)
        local_status = self.session.get_local_status(current_display)
        global_status = self.session.get_global_status(current_display)
        if local_status['status'] is False and global_status['status'] is False:
            logging.info(" Local protection level :{} and Global Protection level :{} are as Expected".format(
                local_status['code'], global_status['code']))

            logging.info("PASS: HDCP disabled successfully for port %d" % int(current_display or 0))
            status = True
        else:
            logging.error("FAIL: local protection level = %r and global protection level = %r" % (local_status['code'],
                                                                                                  global_status[
                                                                                                      'code']))
            gdhm.report_bug(
                title="[HDCP][OPM] Failed to disable HDCP Type {}".format(self.hdcp_type),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        return status

    ##
    # @brief   This function is used to close the HDCP session and copy the OPM logs to Logs Folder
    # @return  output of the command
    def exit_opm(self):
        # OPM will send HDCP disable call to driver and then exits. HDCP status should be False
        if hasattr(self, 'session'):
            exit_data = self.session.quit()

        elif self._testMethodName.endswith('multisession'):
            logging.info(" Closing OPM Session 1 ....")
            exit_data = self.session1.quit()
            logging.info(" Closing OPM Session 2 ....")
            exit_data = self.session2.quit()
        else:
            logging.info(" OPM Session not yet Established")

        if 'exit_data' in locals() and exit_data['status'] is not False:
            logging.error(" FAIL: status = %r.Problem occurred while quitting OPM Lite App" % (exit_data['status']))
        if os.path.exists('./Logs'):
            for file_name in os.listdir(os.getcwd()):
                if file_name.startswith('opm_tester'):
                    shutil.copy2(file_name, './Logs')
                    logging.info(" Successfully copied OPM Lite Tool log to Logs folder")
                if file_name.startswith('hdcp_log_manual'):
                    shutil.copy2(file_name, './Logs')
                    logging.info(" Successfully copied HDCP session log to Logs folder")
        # wait added for GTA job
        time.sleep(2)
        return (exit_data if 'exit_data' in locals() else None)

    ##
    # @brief   Method to verify HDCP for multi display with multiple opm session
    # @return  True if HDCP verification is successful else return False
    def multi_display_multi_session(self):

        self.session1 = OPMSession(self.hdcp_type)
        time.sleep(5)
        self.session2 = OPMSession(self.hdcp_type)
        time.sleep(1)
        status = False

        # get connected displays
        display_info = self.session1.get_display_info()
        connected_display_count = [self.display_list.index(port) for port in self.display_list if
                                   display_utility.get_vbt_panel_type(port, 'gfx_0') not in
                                   [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]]
        record = []
        for i in range(len(self.display_list)):
            record.append({})
            for j in range(0, 2):
                record[i][j + 1] = False

        # Activate Session 1 for all the displays
        for current_display in connected_display_count:
            logging.info("STEP : Trying to enable HDCP for port " + str(current_display) + " in session 1")
            if self.hdcp_type == HDCPType.HDCP_1_4:
                self.session1.enable_type0(current_display)
            else:
                if self.hdcp_type == HDCPType.HDCP_2_2:
                    self.session1.enable_type1(current_display)
                else:
                    logging.error("FAIL: Invalid HDCP capability {} passed as an argument ".format(self.hdcp_type))
                    return False
            if display_info['ports'][current_display]['HDCPCapability'] is True:
                record[current_display][1] = True
            else:
                record[current_display][1] = False
            status = self.show_hdcp_status(current_display, self.session1, self.session2, record)
            if status is False:
                return status

        # Activate Session 2 for all the displays
        for current_display in connected_display_count:
            logging.info("Trying to enable HDCP for port " + str(current_display) + " in session 2")
            if self.hdcp_type == HDCPType.HDCP_1_4:
                enable_status = self.session2.enable_type0(current_display)
            else:
                if self.hdcp_type == HDCPType.HDCP_2_2:
                    enable_status = self.session2.enable_type1(current_display)
                else:
                    logging.error("Invalid HDCP_TYPE passed as argument")
                    return False
            if enable_status['status'] is True:
                record[current_display][2] = True
            status = self.show_hdcp_status(current_display, self.session1, self.session2, record)
            if status is False:
                return status

        # Deactivate Session 2 for all the displays
        # After this try to check the protection level on session 1
        for current_display in connected_display_count:
            logging.info("STEP:Trying to disable HDCP for port " + str(current_display) + " in session 2")
            disable_status = self.session2.disable(current_display)
            if disable_status['status'] is True:
                record[current_display][2] = False
            status = self.show_hdcp_status(current_display, self.session1, self.session2, record)
            if status is False:
                return status

        # Deactivate Session 1 for all the displays
        for current_display in connected_display_count:
            logging.info("STEP: Trying to disable HDCP for port " + str(current_display) + " in session 1")
            disable_status = self.session1.disable(current_display)
            if disable_status['status'] is True:
                record[current_display][1] = False
            status = self.show_hdcp_status(current_display, self.session1, self.session2, record)
            if status is False:
                return status

        return status

    ##
    # @brief       Shows the current HDCP status for multiple display
    # @param[in]   check_display_index  display index to be passed to opm lite
    # @param[in]   session1 opm lite session1 instance
    # @param[in]   session2 opm lite session2 instance
    # @param[in]   record opm session status recorded for the display index
    # @return      True if successful, False otherwise
    def show_hdcp_status(self, check_display_index, session1, session2, record):

        status = False
        # check the protection level on session 1
        local_status = session1.get_local_status(check_display_index)
        global_status = session1.get_global_status(check_display_index)

        # If any of the session is active for the current display global status should be true
        global_state = False
        for session_index in range(1, 3):
            if record[check_display_index][session_index] is True:
                global_state = True

        if local_status['status'] is record[check_display_index][1] and global_status['status'] is global_state:
            if local_status['status'] is True:
                logging.info("PASS : HDCP_TYPE " + str(self.hdcp_type) + " is active for display " +
                             str(check_display_index) + " for session 1")
            else:
                logging.info("PASS : HDCP is OFF for display " + str(check_display_index) + " for session 1")
            status = True
        else:
            status = False
            logging.error("Actual : local status = {} and global status = {}. Expected : local status = {} and global "
                          "status ={} ".format(local_status['code'], global_status['code'],
                                               record[check_display_index][1], global_state))
            logging.error('FAIL : HDCP verification failed for session 1')
            return status
        # Check for session 2
        local_status = session2.get_local_status(check_display_index)
        global_status = session2.get_global_status(check_display_index)

        # If any of the session is active for the current display global status should be true
        global_state = False
        for session_index in range(1, 3):
            if record[check_display_index][session_index] is True:
                global_state = True

        if local_status['status'] is record[check_display_index][2] \
                and global_status['status'] is global_state:
            if local_status['status'] is True:
                logging.info("PASS: HDCP_TYPE " + str(self.hdcp_type) + " is active for display " +
                             str(check_display_index) + " for session 2")
            else:
                logging.info("PASS: HDCP  is OFF for display " + str(check_display_index) + " for session 2")
            status = True
        else:
            status = False
            logging.error("Actual : local protection level = {} and global protection level = {}. Expected : "
                          "local protection level = {} and global protection level ={} ".format(local_status['code'],
                                                                                                global_status['code'],
                                                                                                record[
                                                                                                    check_display_index][
                                                                                                    2], global_state))
            logging.error('FAIL : HDCP verification failed for session 2')

        return status


##
# OPM Session Class
class OPMSession(object):
    multi_session_id = 0
    filename = None
    opm_process = {}
    output = {}
    platform = None
    hdcp_type = HDCPType.HDCP_1_4
    display_config = disp_cfg.DisplayConfiguration()

    ##
    # @brief      init method of OPMSession Base class to start the OPM tester
    # @param[in]  hdcptype hdcp version
    def __init__(self, hdcptype=HDCPType.HDCP_1_4.value):
        opm_tester_thread = Thread(target=self.start_opm_tester())
        opm_tester_thread.setDaemon(True)
        opm_tester_thread.start()
        self.hdcp_type = hdcptype

    ##
    # @brief   Start OPM Tester Tool
    # @return  None
    def start_opm_tester(self):

        logging.info("Starting the OPMTester")
        self.multi_session_id = random.randint(0, 100)
        self.filename = "hdcp_log_manual_" + str(self.multi_session_id) + ".txt"
        self.opm_process = Popen(
            "\"" + OPMTEST_BINARY_PATH + "\\OPMTester.exe\" > hdcp_log_manual_" + str(self.multi_session_id) + ".txt",
            stdin=PIPE,
            stdout=PIPE,
            shell=True
        )

    ##
    # @brief    Function will return connected display details and corresponding HDCP level
    # @return   platform details with ports & HDCP support
    def get_display_info(self):
        current_line_index = 0
        display_info = []
        platform_data = {}
        port = 0

        self.display_list = []
        # Collect the display details in enumerated displays from cmdline
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        for index in range(self.enumerated_displays.Count):
            self.display_list.insert(index, CONNECTOR_PORT_TYPE(
                self.enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name)
        ##
        # if the log file is not generated, exit
        time.sleep(5)
        if os.path.exists(self.filename) is False:
            logging.error("FAIL: Log file {0} is not generated".format(self.filename))
            return platform_data
        log_file = open(self.filename)
        lines = log_file.readlines()
        log_file.close()
        if len(lines) < 1:
            logging.error("FAIL: Log file {0} is Empty".format(self.filename))
            return platform_data

        for line in lines:
            display_info_property_list = line.strip().split("\t")
            if len(display_info_property_list) < 1:
                continue

            # port_id, HDCP Capability, HDCPLocalLevel, ConnectorType for all connected display_path
            if display_info_property_list[0] == "PortID":
                next_line_index = current_line_index + 2
                display_info_property_data = lines[next_line_index].strip().split("\t")
                if len(display_info_property_data) > 0:
                    if len(display_info_property_data[0]) > 0:
                        while display_info_property_data[0][0] != '*':
                            display_info_property_index = 0
                            port_connector_type[self.display_list[port]] = display_info_property_data[-1]
                            port += 1
                            display_info_temp = {
                                'PortID': display_info_property_data[0],
                                'HDCPCapability': False,
                                'HDCP_TYPE': None
                            }
                            for dict_index in display_info:
                                if dict_index['PortID'] == display_info_property_data[0]:
                                    continue
                            hdcp_capability_data = display_info_property_data[1].strip().split('    ')
                            if hdcp_capability_data[0] == 'HDCP':
                                display_info_temp['HDCPCapability'] = True
                                display_info_temp['HDCP_TYPE'] = 0
                            else:
                                if hdcp_capability_data[0] == 'HDCP_TYPE_ENFORCEMENT':
                                    display_info_temp['HDCPCapability'] = True
                                    display_info_temp['HDCP_TYPE'] = 1

                            display_info.append(display_info_temp)
                            next_line_index += 1
                            display_info_property_data = lines[next_line_index].strip().split("\t")
                            if len(display_info_property_data) > 0:
                                if len(display_info_property_data[0]) > 0:
                                    continue
                                else:
                                    break
                            else:
                                break
            current_line_index += 1
        self.platform = {'ports': display_info}
        return self.platform

    ##
    # @brief       This function will create a list to identify the last command output
    # @param[in]   operation_type to get the OPM result
    # @param[in]   port_id to get the verification status
    # @return      output list with dictionary containing the opm output
    def parse_output(self, operation_type, port_id):

        current_line_index = 0
        output = []

        log_file = open(self.filename)
        lines = log_file.readlines()
        log_file.close()
        current_line_index = 0
        for line in lines:
            is_last_output = True
            temp = {}
            if line[:5] == 'Enter':
                temp = {'operation': operation_type, 'output': '', 'status': False, 'port': port_id}
                next_line_index = current_line_index + 1
                while next_line_index < len(lines):
                    if lines[next_line_index][:5] == 'Enter':
                        is_last_output = False
                        break
                    temp['output'] += lines[next_line_index].strip() + ' '
                    next_line_index += 1
                if is_last_output:
                    break
                if temp['operation'] == 'gl':
                    if self.hdcp_type == HDCPType.HDCP_1_4:
                        status = re.search(r'HDCP_ON_WITH_NO_TYPE', temp['output'], re.I)
                        if status:
                            temp['code'] = 'OPM_HDCP_ON'
                            temp['status'] = True
                        else:
                            temp['code'] = 'OPM_HDCP_OFF'
                            temp['status'] = False
                    else:
                        status = re.search(r'HDCP_ON_WITH_TYPE1', temp['output'], re.I)
                        if status:
                            temp['code'] = 'OPM_HDCP_WITH_TYPE_ON'
                            temp['status'] = True
                        else:
                            temp['code'] = 'OPM_HDCP_WITH_TYPE_OFF'
                            temp['status'] = False
                if temp['operation'] == 'gg':
                    if self.hdcp_type == HDCPType.HDCP_1_4:
                        status = re.search(r'HDCP_ON_WITH_NO_TYPE', temp['output'], re.I)
                        if status:
                            temp['code'] = 'OPM_HDCP_ON'
                            temp['status'] = True
                        else:
                            temp['code'] = 'OPM_HDCP_OFF'
                            temp['status'] = False
                    else:
                        status = re.search(r'HDCP_ON_WITH_TYPE1', temp['output'], re.I)
                        if status:
                            temp['code'] = 'OPM_HDCP_WITH_TYPE_ON'
                            temp['status'] = True
                        else:
                            temp['code'] = 'OPM_HDCP_WITH_TYPE_OFF'
                            temp['status'] = False
                if temp['operation'] == 'e0':
                    status = re.search(r'succeeded', temp['output'], re.I)
                    if status:
                        temp['code'] = 'OPM_HDCP_ON'
                        temp['status'] = True
                    else:
                        temp['code'] = 'OPM_HDCP_OFF'
                        temp['status'] = False
                if temp['operation'] == 'e1':
                    status = re.search(r'succeeded', temp['output'], re.I)
                    if status:
                        temp['code'] = 'OPM_HDCP_WITH_TYPE_ON'
                        temp['status'] = True
                    else:
                        temp['code'] = 'OPM_HDCP_WITH_TYPE_OFF'
                        temp['status'] = False
                if temp['operation'] == 'd':
                    status = re.search(r'succeeded', temp['output'], re.I)
                    if status:
                        temp['status'] = True
                    else:
                        temp['status'] = False

                output.append(temp)
            current_line_index += 1
        if len(output) == 0:
            temp_output = [{'operation': operation_type, 'output': '', 'status': False, 'port': port_id}]
            return temp_output
        else:
            return output

    ##
    # @brief       This function will return the last command output
    # @param[in]   operation_type opm command name
    # @param[in]   port_id port_id of display
    # @return      output opm command output
    def get_last_output(self, operation_type, port_id=None):
        output = self.parse_output(operation_type, port_id)
        # returning the last command result
        return output[len(output) - 1]

    ##
    # @brief       This function will help to pass the HDCP command to the OPM session
    # @param[in]   operation opm command
    # @return      None
    def set_operation(self, operation):
        try:
            time.sleep(1)
            self.opm_process.stdin.write((str(operation) + '\n').encode())
            self.opm_process.stdin.flush()
            time.sleep(5)
        except Exception as e:
            logging.error("FAIL: Error occurred in set_operation {} : {}".format(str(operation), str(e)))

    ##
    # @brief       This function will enable HDCP Type-0 and returns the output
    # @param[in]   port_id port name to enable HDCP Type 0 protection
    # @return      get_last_output opm output for the HDCP operation
    def enable_type0(self, port_id=None):

        if self.platform is None:
            self.get_display_info()
        if self.platform is None:
            logging.error("No platform information available")
            return False

        if len(self.platform['ports']) < 1:
            logging.error("No ports available")
            return False
        else:
            if port_id is None:
                logging.info("Activate HDCP_TYPE 0")
                self.set_operation('e0')
            else:
                logging.info("Activate HDCP_TYPE 0 on port {}".format(port_id))
                self.set_operation('e0')
                self.set_operation(port_id)
            return self.get_last_output('e0', port_id)

    ##
    # @brief       This function will enable HDCP Type-1 and returns the output
    # @param[in]   port_id port name to enable HDCP Type 1 protection
    # @return      get_last_output opm output for the HDCP operation
    def enable_type1(self, port_id=None):

        if self.platform is None:
            self.get_display_info()
        if self.platform is None:
            logging.error("No platform information available")
            return False
        if len(self.platform['ports']) < 1:
            logging.error("No ports available")
            return False
        else:
            if port_id is None:
                self.set_operation('e1')
            else:
                logging.info(" Activate HDCP_TYPE 1 on port {}".format(port_id))
                self.set_operation('e1')
                self.set_operation(port_id)
            return self.get_last_output('e1', port_id)

    ##
    # @brief       This function will return the local status
    # @param[in]   port_id port name to verify local protection level
    # @return      get_last_output opm output for local protection level
    def get_local_status(self, port_id=None):

        if self.platform is None:
            self.get_display_info()
        if self.platform is None:
            logging.error("No platform information available")
            return False
        if len(self.platform['ports']) < 1:
            logging.error("No ports available")
            return False
        else:
            if port_id is None:
                self.set_operation('gl')
            else:
                self.set_operation('gl')
                self.set_operation(port_id)
            return self.get_last_output('gl', port_id)

    ##
    # @brief       This function will return the global status
    # @param[in]   port_id port name to verify global protection level
    # @return      get_last_output opm output for global protection level
    def get_global_status(self, port_id=None):
        if self.platform is None:
            self.get_display_info()
        if self.platform is None:
            logging.error("No platform information available")
            return False
        if len(self.platform['ports']) < 1:
            logging.error("No ports available")
            return False
        else:
            if port_id is None:
                logging.info("Only one Display is connected")
                self.set_operation('gg')
            else:
                logging.info("port id for gg is %s" % port_id)
                self.set_operation('gg')
                self.set_operation(port_id)
            return self.get_last_output('gg', port_id)

    ##
    # @brief       This function will disable the HDCP
    # @param[in]   port_id port number to disable HDCP
    # @return      get_last_output opm output for HDCP disable operation
    def disable(self, port_id=None):

        if self.platform is None:
            self.get_display_info()
        if self.platform is None:
            logging.error("No platform information available")
            return False
        if len(self.platform['ports']) < 1:
            logging.error("No ports available")
            return False
        else:
            if port_id is None:
                self.set_operation('d')
            else:
                self.set_operation('d')
                self.set_operation(port_id)
            return self.get_last_output('d', port_id)

    ##
    # @brief    This function will quit the OPM Session
    # @return   get_last_output opm output for session quit operation
    def quit(self):
        logging.info("Quitting the OPM Lite APP")
        self.set_operation('q')
        time.sleep(3)
        return self.get_last_output('q')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome)
