########################################################################################################################
# @file         edp_link_training_base.py
# @addtogroup   EDP
# @section      EDP_Link_Training_Tests
# @brief        @ref edp_link_training_base.py contains the base class for EDP Full link training test cases.
# @details      Base class contains the setUp and tearDown functions for all EDP Full link training test cases.
#               Also other helper functions included.
# @author       Kruti Vadhavaniya, Bhargav Adigarla
########################################################################################################################

import logging
import sys, os, time
import unittest
import shutil
import xml.etree.ElementTree as xml_ET

from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core import cmd_parser, reboot_helper, display_power
from Libs.Core.logger import etl_tracer
from Libs.Core.test_env import test_context
import Libs.Core.sw_sim.dpcd_model_data_struct as dpcd_struct
from Libs.Core.wrapper.valsim_args import ValSimPort
from Libs.Core.sw_sim import gfxvalsim, driver_interface
from Tests.PowerCons.Modules import common, dut
from Tests.Display_Port.DP_LinkTraining.display_dpcd_model import DisplayDPCDModel


##
# @brief        This class is the base class for EDP Full link training test cases with setup, teardown and common
#               functions used across the tests.
class EdpLinkTrainingBase(unittest.TestCase):
    dpcd_model_data_info = DisplayDPCDModel()
    driver_interface_ = driver_interface.DriverInterface()
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()

    ##
    # @brief        This method initializes and prepares the setup required for execution of link training test cases on
    #               eDP
    # @details      It parses the command line amd gets the DPCD model data input xml
    # @return       None
    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        logging.info(" SETUP: EDP_LINK_TRAINING ".center(common.MAX_LINE_WIDTH, "*"))
        self.panel_info = {}
        self.connector_port = None
        self.xml_file_path = None
        self.xml_file_name = None

        self.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, ['-DPCD_MODEL_DATA'])

        if self.cmd_line_param['DPCD_MODEL_DATA'] != 'NONE':
            self.xml_file_name = (self.cmd_line_param['DPCD_MODEL_DATA'][0])

        # Get DPCD model data input xml
        if self.xml_file_name is not None:
            logging.debug("xml_file = {}".format(self.xml_file_name))
            self.xml_file_path = os.path.join(test_context.PANEL_INPUT_DATA_FOLDER, 'LINK_TRAINING_DATA',
                                              self.xml_file_name)
        dut.prepare()

    ##
    # @brief        This method logs teardown phase
    # @return       None
    @reboot_helper.__(reboot_helper.teardown)
    def tearDown(self):
        logging.info(" TEARDOWN: EDP_LINK_TRAINING ".center(common.MAX_LINE_WIDTH, "*"))
        dut.reset()
        logging.info("Test Cleanup Completed")

    ##
    # @brief        This method stops the etl, rename it and returns it path
    # @return       returns path of etl
    @staticmethod
    def stop_etl_get_etl_file_path():
        if etl_tracer.stop_etl_tracer() is False:
            logging.error("FAIL to stop ETL Tracer")
            return None

        if os.path.exists(etl_tracer.GFX_BOOT_TRACE_ETL_FILE):
            etl_file_name = 'GfxTrace_' + str(time.time()) + '.etl'
            etl_file_path = os.path.join(test_context.LOG_FOLDER, etl_file_name)
            shutil.move(etl_tracer.GFX_BOOT_TRACE_ETL_FILE, etl_file_path)
        else:
            logging.error("FAIL: Default etl file does not exist")
            return None

        if not os.path.exists(etl_file_path):
            logging.error(f"FAIL: ETL file path= {etl_file_path} NOT found")
            return None
        return etl_file_path

    ##
    # @brief        This method provides the absolute path of diana log file.
    # @param[in]    diana_exe_path  diana exe path
    # @param[in]    etl_file_path etl file path used by diana
    # @return       Absolute path of diana log file
    @staticmethod
    def get_diana_file(diana_exe_path, etl_file_path):
        logging.debug(diana_exe_path)
        logging.debug(etl_file_path)
        if not os.path.exists(diana_exe_path):
            logging.error(f"FAIL: Diana Path= {diana_exe_path} NOT found")
            return None

        output_filename = 'edp_link_training_diana' + str(time.time()) + '.txt'

        diana_cmd = " -dispdiag info -dp verbose > " + output_filename.lower()
        status = os.system(diana_exe_path + " " + etl_file_path + diana_cmd)
        logging.debug(f"Diana execution status = {bool(status)}")

        output_file_path = os.path.join(os.getcwd(), output_filename.lower())
        if not os.path.exists(output_file_path):
            logging.error(f"FAIL: Output file path= {output_file_path} NOT found")
            return None
        return output_file_path

    ##
    # @brief        This method provides model data from input xml file.
    # @param[in]    dpcd_xml_file  XML file with dpcd data input
    # @return       DPCD model data
    @staticmethod
    def get_dpcd_model_data(self, dpcd_xml_file):
        dpcd_model_data = []
        if not os.path.exists(dpcd_xml_file.strip()):
            logging.error("[Test Issue]: DPCD Model file: {} not present".format(dpcd_xml_file))
            gdhm.report_bug(
                title="[EDP][LINK TRAINING] Input DPCD model xml file not found in provided path",
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return None

        xml_root = xml_ET.parse(dpcd_xml_file).getroot()
        transaction_count = 0
        input_starting_offsets = []
        response_starting_offsets = []
        ul_trigger_offset_for_trans = []
        response_values = []
        input_values = []

        # Read XML and get DPCD model data in desired format
        for child in xml_root:
            if child.tag == 'DPCDModelData':
                for transaction_count_val in child.findall('transactionCount'):
                    transaction_count = int(transaction_count_val.text)
                for input_starting_offsets_val in child.findall('inputStartingOffsets'):
                    input_starting_offsets.append(
                        self.dpcd_model_data_info.get_dpcd_parsed_value(input_starting_offsets_val.text))
                for input_values_val in child.findall('inputValues'):
                    input_values.append(self.dpcd_model_data_info.get_dpcd_parsed_value(input_values_val.text))
                for response_starting_offsets_val in child.findall('responseStartingOffsets'):
                    response_starting_offsets.append(
                        self.dpcd_model_data_info.get_dpcd_parsed_value(response_starting_offsets_val.text))
                for ul_trigger_offset_for_trans_val in child.findall('ulTriggerOffsetForTrans'):
                    ul_trigger_offset_for_trans = (
                        self.dpcd_model_data_info.get_dpcd_parsed_value(ul_trigger_offset_for_trans_val.text))
                for responseValues_val in child.findall('responseValues'):
                    response_values.append(self.dpcd_model_data_info.get_dpcd_parsed_value(responseValues_val.text))

        logging.debug("ulTriggerOffsetForTrans: {}".format(hex(ul_trigger_offset_for_trans)))
        logging.debug("transactionCount: {}".format(transaction_count))
        logging.debug("inputStartingOffsets: {}".format(self.dpcd_model_data_info.log_in_hex(input_starting_offsets)))
        logging.debug("inputValues: {}".format(self.dpcd_model_data_info.log_in_hex(input_values)))
        logging.debug(
            "responseStartingOffsets: {}".format(self.dpcd_model_data_info.log_in_hex(response_starting_offsets)))
        logging.debug("responseValues: {}".format(self.dpcd_model_data_info.log_in_hex(response_values)))

        dpcd_model_data.extend((input_starting_offsets, input_values, response_starting_offsets, response_values,
                                transaction_count, ul_trigger_offset_for_trans))

        return dpcd_model_data

    ##
    # @brief        This method provides dpcd model data filled from input values
    # @param[in]    input_starting_offsets Input offset
    # @param[in]    input_values offset values
    # @param[in]    response_starting_offsets Response offset
    # @param[in]    response_values response values
    # @param[in]    transaction_count number indicating the number of transactions
    # @param[in]    ul_trigger_offset_for_trans Trigger offset
    # @return       DPCD model data
    @staticmethod
    def set_dpcd_model(self, input_starting_offsets, input_values, response_starting_offsets, response_values,
                       transaction_count=0, ul_trigger_offset_for_trans=0):
        dpcd_model_data = dpcd_struct.DPDPCDModelData()

        dpcd_model_data.uiPortNum = getattr(ValSimPort, "DP_A").value
        dpcd_model_data.eTopologyType = getattr(gfxvalsim.DpTopology, 'DPSST').value

        model_data = dpcd_model_data.stDPCDModelData
        model_data.ucTransactionCount = transaction_count
        model_data.ulTriggerOffset = ul_trigger_offset_for_trans

        for trans_index in range(model_data.ucTransactionCount):
            dpcd_trans = model_data.stDPCDTransactions[trans_index]

            dpcd_trans.ucNumInputDpcdSets = len(input_starting_offsets[trans_index])
            dpcd_trans.stInputDpcdSets[0].ulStartingOffset = input_starting_offsets[trans_index][0]
            dpcd_trans.stInputDpcdSets[0].ucLength = len(input_values[trans_index])
            for i in range(len(input_values[trans_index])):
                dpcd_trans.stInputDpcdSets[0].ucValues[i] = input_values[trans_index][i]

            dpcd_trans.ucNumResponseDpcdSets = len(response_starting_offsets[trans_index])
            dpcd_trans.stResponseDpcdSets[0].ulStartingOffset = response_starting_offsets[trans_index][0]
            dpcd_trans.stResponseDpcdSets[0].ucLength = len(response_values[trans_index])
            for i in range(len(response_values[trans_index])):
                dpcd_trans.stResponseDpcdSets[0].ucValues[i] = response_values[trans_index][i]

        return dpcd_model_data

    ##
    # @brief        This method validates Link training data
    # @param[in]    diana_log_file  Diana log file with link training data
    # @return       [Bool] True if link training successful else False
    def validate_dpcd_model_data(self, diana_log_file):

        lane_training_data = []
        lane_adjust_data = []
        response_values_from_xml = []
        response_lane_training_data_from_xml = []
        response_lane_adjust_data = []
        training_status = False
        cr_start_status = cr_end_status = False
        eq_start_status = eq_end_status = False

        try:
            with open(diana_log_file, 'r') as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if "Link Training SUCCESS" in line:
                        logging.info("Link training success")
                        training_status = True
                    if "0x00202" in line:
                        line = line.split(":")[-1].strip()
                        lane_training_data.append(line.replace('\n', '').replace('\t', ''))
                    if "0x00206" in line:
                        line = line.split(":")[-1].strip()
                        lane_adjust_data.append(line.replace('\n', '').replace('\t', ''))
                    if "0x00207" in line:
                        line = line.split(":")[-1].strip()
                        lane_adjust_data.append(line.replace('\n', '').replace('\t', ''))
                    if "DE_CONFIG_LINK_CR_START" in line:
                        logging.info("Link training for CR start: Successful")
                        cr_start_status = True
                    if "DE_CONFIG_LINK_CR_END" in line:
                        logging.info("Link training for CR end: Successful")
                        cr_end_status = True
                    if "DE_CONFIG_LINK_EQ_START" in line:
                        logging.info("Link training for EQ start: Successful")
                        eq_start_status = True
                    if "DE_CONFIG_LINK_EQ_END" in line:
                        logging.info("Link training for EQ end: Successful")
                        eq_end_status = True

                f.close()
                os.remove(diana_log_file)

                # Get response values from xml
                xml_root = xml_ET.parse(self.xml_file_path).getroot()
                for child in xml_root:
                    if child.tag == 'DPCDModelData':
                        for responseValues_val in child.findall('responseValues'):
                            response_values_from_xml.append(responseValues_val.text)

                for value in response_values_from_xml:
                    if value.startswith('['):
                        if value.replace(" ", "").replace("]", "").split(",")[-1] != "0x00":
                            response_lane_adjust_data.append(value.replace(" ", "").replace("]", "").split(",")[-1])
                        if value.replace(" ", "").replace("]", "").split(",")[-2] != "0x00":
                            response_lane_adjust_data.append(
                                value.replace(" ", "").replace(" ", "").replace("]", "").split(",")[-2])
                        response_lane_training_data_from_xml.append(
                            value.replace(" ", "").replace('[', '').replace(']', '').split(",")[:3])

                if training_status is True and cr_start_status is True and eq_start_status is True and cr_end_status is True and eq_end_status is True:

                    for count, value in enumerate(lane_training_data):
                        lane_training_data[count] = value.replace(" ", ",").split(",")

                    if response_lane_training_data_from_xml == lane_training_data:
                        logging.info("PASS: Lane training data : Expected :{}, Actual:{}".format(
                            response_lane_training_data_from_xml, lane_training_data))
                        if response_lane_adjust_data == lane_adjust_data:
                            logging.info("PASS: Lane adjust data : Expected :{}, Actual:{}".format(
                                response_lane_adjust_data, lane_adjust_data))
                            return True
                else:
                    return False
        except IOError:
            logging.error(f"FAIL: Diana File read error: {diana_log_file}")
            return False
