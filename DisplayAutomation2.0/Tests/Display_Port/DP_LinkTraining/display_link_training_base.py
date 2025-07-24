##########################################################################################################
# @file         display_link_training_base.py
# @brief        This script contains helper functions that will be used by Link training test scripts
# @author       Ashish Kumar
##########################################################################################################

import os
import sys
import logging
import time
import unittest
import xml.etree.ElementTree as xml_ET
import Libs.Core.display_utility as disp_util
from Libs.Core.logger import etl_tracer
from Libs.Core import cmd_parser
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.test_env import test_context
from Libs.Core import reboot_helper
from Libs.Core.sw_sim import gfxvalsim
from Libs.Core.logger import gdhm
from Libs.Feature.app import App3D
from Libs.Feature.app import AppMedia
import Tests.Display_Port.DP_LinkTraining.json_parser as jparser

from Tests.Display_Port.DP_LinkTraining.display_dpcd_model import DisplayDPCDModel

CLASSICD3D_APP = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "Flips\\ClassicD3D\\ClassicD3D.exe")
media_file_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO\mpo_3840_2160_avc.mp4")


##
# @brief This class contains functions that help in filling Link training data, and validating it.
class DisplayLinkTrainingBase(unittest.TestCase):
    config = DisplayConfiguration()
    dpcd_model = DisplayDPCDModel()

    ##
    # @brief        This class method is the entry point for Link Training test cases.
    #               Helps to initialize some of the parameters required for test execution.
    # @return       None
    def setUp(self):
        logging.debug("Entry: setUpClass")

        # Variable Initialization
        self.input_display_list = []
        self.panel_info = {}
        self.hpd_mode = None
        self.iteration_count = 0
        self.platform = None
        self.app_type = ['MEDIA', 'CLASSICD3D']
        self.fail_re_link_training = False

        cmdline_args = sys.argv

        # Set control variable based on command line options
        for arg in cmdline_args:
            if arg.upper() == "-SIM":
                self.hpd_mode = "SIM"
                cmdline_args.remove("-SIM")
            elif arg.upper() == "-EMU":
                self.hpd_mode = "EMU"
                cmdline_args.remove("-EMU")

        if self.hpd_mode is None:
            self.hpd_mode = "SIM"

        # Parse the commandline params
        cmd_line_param = cmd_parser.parse_cmdline(cmdline_args, ['-iteration', '-fail_re_link_training'])
        self.iteration_count = int(cmd_line_param['ITERATION'][0])
        if cmd_line_param['FAIL_RE_LINK_TRAINING'] != 'NONE':
            self.fail_re_link_training = True

        # input_display_list[] is a list of Port Names from user args
        for key, value in cmd_line_param.items():
            if key == 'XML' and 'XML' not in self.panel_info.keys():
                self.panel_info[value['connector_port']] = value
            if cmd_parser.display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None:
                    if key not in self.panel_info.keys():
                        self.panel_info[value['connector_port']] = {}
                    if value['panel_index'] is not None:
                        self.panel_info[value['connector_port']].update({'panel_index': value['panel_index']})
                    if value['index'] is not None:
                        self.panel_info[value['connector_port']].update({'index': value['index']})
                    if value['dpcd_model'] is not None:
                        self.panel_info[value['connector_port']].update({'xml': value['dpcd_model']})
                    self.input_display_list.insert(value['index'], value['connector_port'])

        logging.info("Panel Info: {}".format(self.panel_info))
        logging.info("Test Flow : Plug and UnPlug of given display ports on respective port with link "
                     "training data for number of Iterations given.")
        logging.debug("Exit: DisplayLinkTrainingBase -> setUpClass")

        machine_info = SystemInfo()
        gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName)
            break

    ##
    # @brief        This method returns currently emulated display name and target id.
    # @return       Dictionary. Display Name as Key and Target ID as Value.
    def get_display_names(self):
        enum_display_dict = {}
        enumerated_displays = self.config.get_enumerated_display_info()
        for index in range(0, enumerated_displays.Count):
            port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[index].ConnectorNPortType).name
            target_id = enumerated_displays.ConnectedDisplays[index].TargetID
            enum_display_dict[port] = target_id
        return enum_display_dict

    ##
    # @brief        This method stops the etl, renames the etl file and returns its path
    # @return       path of etl
    # @cond
    @staticmethod
    # @endcond
    def stop_etl_get_etl_file_path():
        if etl_tracer.stop_etl_tracer() is False:
            logging.error("Failed to stop ETL Tracer")
            # Gdhm bug reporting handled in stop_etl_tracer
            return None

        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            file_name = 'GfxTraceLinkTraining-' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, file_name)
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
        else:
            logging.error("[Test Issue]: Default etl file does not exist")
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Default etl file is not present in the system",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return None

        if not os.path.exists(etl_file_path):
            logging.error("[Test Issue]: {0} NOT found".format(etl_file_path))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Renamed Etl file not present in the system",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return None
        return etl_file_path

    ##
    # @brief        This method/utility function helps in validating link training expected data.
    # @param[in]    link_training_exp_data link training expected data to be validated
    # @return       True if data is fine; False otherwise.
    # @cond
    @staticmethod
    # @endcond
    def validate_link_training_expected_data(link_training_exp_data):
        if len(link_training_exp_data) != 6:
            logging.debug("link_training_expected_data: {}".format(link_training_exp_data))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Validation of link_training_expected_data failed",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False
        return True

    ##
    # @brief        This method helps to filling dpcd model data.
    # @param[in]    diana_log_file diana log file path
    # @param[in]    link_training_exp_data Expected Channel EQ link training data
    # @param[in]    port port for which link training data is verified on
    # @return       True if pass; False otherwise.
    def validate_link_training_sequence(self, diana_log_file, link_training_exp_data, port):

        if not os.path.exists(diana_log_file):
            logging.error("[Test Issue]: {0} NOT found".format(diana_log_file))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Invalid platform input to func get_link_training_expected_data",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False

        if not self.validate_link_training_expected_data(link_training_exp_data):
            logging.error("[Test Issue]: Link Training Expected data validation failed")
            # Gdhm bug reporting handled in validate_link_training_expected_data
            return False

        json_lt_obj = jparser.JsonParser()
        json_report = json_lt_obj.load_report(diana_log_file)
        if json_report is None:
            logging.error("[Test Issue]: json parser issue")

        # Initialization of Variables
        key = 'DpLinkTrainingData'
        cr_iteration = 0
        eq_iteration = 0
        voltage_swing = 0
        pre_emp = 0
        link_training_status = False
        result = True
        link_training_dict_arr = json_lt_obj.get_event_list(key)
        if link_training_dict_arr is None:
            return False

        splitport = port.split("_")
        port = 'PORT_' + splitport[len(splitport) - 1]
        for item in link_training_dict_arr:
            dp_lt_data_obj = jparser.DpLinkTrainingData(item)
            if item['Port'] == port:
                cr_iteration = item['CRIterations']
                eq_iteration = item['EQIterations']
                voltage_swing = item['VoltageSwing']
                pre_emp = item['PreEmphasis']
                if item['LTStatus']:
                    link_training_status = True
                else:
                    logging.debug("Link Training details: {}".format(dp_lt_data_obj.__repr__()))

        if not link_training_status:
            logging.error("[Driver Issue]: Link Training Failed")
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Link Training Failed for port: {}".format(port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            result = False
        else:
            # Comparing expected and actual CR and EQ voltage swing and Pre-emphasis level
            if int(cr_iteration) == link_training_exp_data[0] and \
                    int(eq_iteration) == link_training_exp_data[1] and \
                    int(voltage_swing) == link_training_exp_data[2] and \
                    int(pre_emp) == link_training_exp_data[3]:
                logging.info("Expected CR iteration, EQ iteration, voltage swing and pre-emphasis level = "
                             "[{} {} {} {}]".format(link_training_exp_data[0], link_training_exp_data[1],
                                                    link_training_exp_data[2], link_training_exp_data[3]))
                logging.info("PASS: Actual CR iteration, EQ iteration, voltage swing and pre-emphasis level = "
                             "[{} {} {} {}]".format(cr_iteration, eq_iteration, voltage_swing, pre_emp))
            else:
                logging.error("[Driver Issue]: Expected CR iteration, EQ iteration, voltage swing and "
                              "pre-emphasis level = [{} {} {} {}]".format(link_training_exp_data[0],
                                                                          link_training_exp_data[1],
                                                                          link_training_exp_data[2],
                                                                          link_training_exp_data[3]))
                logging.error("FAIL: [Driver Issue]: Actual CR iteration, EQ iteration, voltage swing and "
                              "pre-emphasis level = [{} {} {} {}]".format(cr_iteration, eq_iteration,
                                                                          voltage_swing, pre_emp))
                gdhm.report_bug(
                    title="[Interfaces][DP_LT] Link Training sequence failed for Port: {}".format(port),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                result = False
        return result

    ##
    # @brief        This method helps in getting expected link training data from XML file.
    # @param[in]    xml_file  xml file path.
    # @param[in]    display_port port for which link training data to get.
    # @param[in]    platform the platform (like MTL, ADLP) for which expected data to get.
    # @return       filled-in link_training_expected_data list
    def get_link_training_expected_data(self, xml_file, display_port, platform):
        if not os.path.exists(xml_file.strip()):
            logging.error("[Test Issue]: LinkTraining xml file: {} not present".format(xml_file))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Link Training xml file: {} is missing".format(xml_file),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        if platform is None:
            logging.error("[Test Issue]: Platform can not be none")
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Invalid platform input to func get_link_training_expected_data",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

        link_training_exp_data = []
        xml_root = xml_ET.parse(xml_file).getroot()

        for child in xml_root:
            if child.tag == 'LTExpectedData':
                for child in xml_root.findall('.//LTExpectedData/*'):
                    if child.tag == 'Platform':
                        platform_xml = child.get('Name')
                        supported_ports = child.get('Port')
                        if supported_ports is not None:
                            supported_ports = [port.strip() for port in supported_ports.split(",")]
                        if (platform_xml is not None and platform.upper() == platform_xml.upper()) and \
                                display_port.upper() in map(lambda x: x.upper(), supported_ports):
                            logging.debug("Platform: {}, supported_ports:{}".
                                          format(platform_xml, supported_ports))
                            if child.find('crLTIter') is not None:
                                link_training_exp_data.insert(0, int(child.find('crLTIter').text))
                            if child.find('eqLTIter') is not None:
                                link_training_exp_data.insert(1, int(child.find('eqLTIter').text))
                            if child.find('ltVoltage') is not None:
                                link_training_exp_data.insert(2, int(child.find('ltVoltage').text))
                            if child.find('ltPreemp') is not None:
                                link_training_exp_data.insert(3, int(child.find('ltPreemp').text))
                            if child.find('linkRateCheck') is not None:
                                link_training_exp_data.insert(4, int(child.find('linkRateCheck').text))
                            if child.find('linkRate') is not None:
                                if '0x' in child.find('linkRate').text:
                                    link_training_exp_data.insert(5, int(child.find('linkRate').text, 16))
                                else:
                                    link_training_exp_data.insert(5, int(child.find('linkRate').text))

        logging.debug("Expected link training verification data: {}".format(link_training_exp_data))
        return link_training_exp_data

    ##
    # @brief        This method helps to getting panel index which was input at cmdline
    # @param[in]    display_port the port string like DP_B, DP_C, etc
    # @return       Panel index value
    def get_panel_index(self, display_port):
        if display_port in self.panel_info.keys():
            for key, value in self.panel_info[display_port].items():
                if key == 'panel_index':
                    return value
        return None

    ##
    # @brief        This method helps to getting xml file which was input at cmdline
    # @param[in]    display_port the port string like DP_B, DP_C, etc
    # @return       xml file name
    def get_xml_filename(self, display_port):
        if display_port in self.panel_info.keys():
            for key, value in self.panel_info[display_port].items():
                if key == 'xml':
                    return value
        return None

    ##
    # @brief        This method provides the absolute path of diana log file.
    # @param[in]    diana_exe_path  diana exe path
    # @param[in]    etl_file_path etl file path used by diana
    # @return       Absolute path of diana log file
    # @cond
    @staticmethod
    # @endcond
    def get_diana_file(diana_exe_path, etl_file_path):
        if not os.path.exists(diana_exe_path):
            logging.error("[Test Issue]: {0} NOT found".format(diana_exe_path))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Diana Exe path not found on the system",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return None

        output_filename = 'link_training_diana' + str(time.time()) + '.txt'
        diana_json_file = 'ValReport.json'
        diana_cmd = " -dispdiag info -dp verbose > " + output_filename
        status = os.system(diana_exe_path + "  " + etl_file_path + diana_cmd)
        if status & 0x00000001:
            logging.error(
                "[Test Issue]: Failed to execute {0}. Please check {0} compatibility with driver".format(
                    diana_exe_path))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Diana exe failed to execute on etl",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return None

        output_file_path = os.path.join(os.getcwd(), diana_json_file)
        if not os.path.exists(output_file_path):
            logging.error("[Test Issue]: {0} NOT found (Test Issue)".format(output_file_path))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Diana output log file: {} is not found on system".format(output_file_path),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return None
        return output_file_path

    ##
    # @brief        This method helps to get the link training model data from xml file
    # @param[in]    xml_file  xml file path.
    # @return       dp_dpcd_model_data structure containing the link training model data
    def get_link_training_model_data(self, xml_file):
        dp_dpcd_model_data = self.dpcd_model.get_dpcd_model_data(xml_file)
        if dp_dpcd_model_data is None:
            self.fail()
            # Gdhm bug reporting handled in get_dpcd_model_data
        else:
            return dp_dpcd_model_data

    ##
    # @brief        Helper function to create an object for specified app
    # @param[in]    app_type : Type of app MEDIA/D3D
    # @return       object of the specified app type
    def create_app_instance(self, app_type=None):
        if app_type == 'MEDIA':
            return AppMedia(media_file_path)
        if app_type == 'CLASSICD3D':
            return App3D('ClassicD3D',
                         CLASSICD3D_APP)
        else:
            self.fail("[Test Issue]: Specified APP is not defined")
