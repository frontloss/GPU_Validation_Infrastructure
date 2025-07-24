##########################################################################################################
# @file         display_dpcd_model.py
# @brief        This file contains helper functions for parsing DPCD model data from XML file.
# @author       Ashish Kumar
##########################################################################################################

import os
import logging
import xml.etree.ElementTree as xml_ET
import Libs.Core.sw_sim.dpcd_model_data_struct as dpcd_struct
from Libs.Core.logger import gdhm


##
# @brief This class contains functions that help in getting Link training data from XML and validating few parameters.
class DisplayDPCDModel:
    MAX_SET_VALUE = 2
    MAX_VALUE_LENGTH = 8
    MAX_TRANSACTION_COUNT = 15

    ##
    # @brief        This utility method compares transaction count with input provided
    # @param[in]    transaction_count transaction count number in xml
    # @param[in]    input_val it will be length of input_starting_offset or input_values or response_starting_offset
    #               or response values
    # @param[in]    string It will be name of the input parameter for logging purpose
    # @return       returns True if passed; False otherwise
    # @cond
    @staticmethod
    # @endcond
    def validate_transaction_count(transaction_count, input_val, string):
        if input_val != transaction_count:
            logging.error("[Test Issue]: Transaction count:{} not equal to count of {}: {}".format
                          (transaction_count, string, input_val))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] transaction count and {} count are not matching in link training DPCD "
                      "model data file".format(string),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False
        return True

    ##
    # @brief        This utility method compares expected max value with actual value
    # @param[in]    max_value expected max value
    # @param[in]    actual_value the value currently observed
    # @param[in]    t_count Transaction Count number
    # @param[in]    string It will be name of the input_value parameter for logging purpose
    # @return       returns True if passed; False otherwise
    # @cond
    @staticmethod
    # @endcond
    def validate_input_value_range(max_value, actual_value, t_count, string):
        if actual_value > max_value:
            logging.error("[Test Issue]: For {}, actual_value:{} exceeded max_value:{} for transaction no.:{}".
                          format(string, actual_value, max_value, t_count))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Invalid {} count in link training dpcd model data file".format(string),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False
        return True

    ##
    # @brief        This method compares and validates the arguments of xml
    # @param[in]    transaction_count Transaction Count number
    # @param[in]    input_starting_offsets list of input starting offset
    # @param[in]    input_values list of input values
    # @param[in]    response_starting_offsets list of response starting offset
    # @param[in]    response_values list of response values
    # @param[in]    ul_trigger_offset_for_trans trigger offset that indicates a DPCD write as LT transaction
    # @return       returns True if passed; False otherwise
    def validate_dpcd_model_data(self, transaction_count, input_starting_offsets, input_values,
                                 response_starting_offsets, response_values, ul_trigger_offset_for_trans):
        status = True

        # Transaction count > 15 is not supported
        if transaction_count < 0 or transaction_count > self.MAX_TRANSACTION_COUNT:
            logging.error("[Test Issue]: Transaction count range is 0 to 15, but its value is: {}".
                          format(transaction_count))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] Transaction Count: {} is out of range".format(transaction_count),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            status = False
        # Count in all the input lists should be same as number of transaction count
        if not self.validate_transaction_count(transaction_count, len(input_starting_offsets),
                                               string="input_starting_offsets"):
            status = False
        if not self.validate_transaction_count(transaction_count, len(input_values), string="input_values"):
            status = False
        if not self.validate_transaction_count(transaction_count, len(response_starting_offsets),
                                               string="response_starting_offsets"):
            status = False
        if not self.validate_transaction_count(transaction_count, len(response_values), string="response_values"):
            status = False

        # ul_trigger_offset_for_trans should not be empty
        if not ul_trigger_offset_for_trans:
            logging.error("ul_trigger_offset_for_trans should not be empty")
            gdhm.report_bug(
                title="[Interfaces][DP_LT] ul_trigger_offset_for_trans is empty in DPCD model data file",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            status = False

        # Early return if status is false
        if not status:
            return status

        # Verify xml data for each transaction number
        # Each transaction can have maximum two values in input/response starting offset
        # Based on no of values in input/response offsets corresponding input/response values will have those many list
        # Lenght of list for input/response values for each offsets should not be more than 8
        for t_count in range(transaction_count):
            if not self.validate_input_value_range(self.MAX_SET_VALUE, len(input_starting_offsets[t_count]), t_count,
                                                   string="input_starting_offsets"):
                status = False
            if len(input_starting_offsets[t_count]) == len(input_values[t_count]):
                for set_count in range(len(input_starting_offsets[t_count])):
                    if not self.validate_input_value_range(self.MAX_VALUE_LENGTH, len(input_values[t_count][set_count]),
                                                           t_count, string="input_values"):
                        status = False
            else:
                logging.error("[Test Issue]: count of input_offsets:{} and input_values:{} does not match "
                              "for transaction no.:{}".format(len(input_starting_offsets[t_count]),
                                                              len(input_values[t_count]), t_count))
                gdhm.report_bug(
                    title="[Interfaces][DP_LT] Invalid input_offset count in link training dpcd model data file",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                status = False

            if not self.validate_input_value_range(self.MAX_SET_VALUE, len(response_starting_offsets[t_count]), t_count,
                                                   string="response_starting_offsets"):
                status = False
            if len(response_starting_offsets[t_count]) == len(response_values[t_count]):
                for set_count in range(len(response_starting_offsets[t_count])):
                    if not self.validate_input_value_range(self.MAX_VALUE_LENGTH,
                                                           len(response_values[t_count][set_count]),
                                                           t_count, string="response_values"):
                        status = False
            else:
                logging.error("[Test Issue]: count of response_offsets:{} and response_values:{} does not "
                              "match for transaction no.:{}".format(len(response_starting_offsets[t_count]),
                                                                    len(response_values[t_count]), t_count))
                gdhm.report_bug(
                    title="[Interfaces][DP_LT] Invalid response_offsets count in link training dpcd model data file",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                status = False
        return status

    ##
    # @brief        This method  fills dpcd model data for link training.
    # @param[in]    input_starting_offsets address offset for input for each transaction
    # @param[in]    input_values List of values stored in input offset address
    # @param[in]    response_starting_offsets address offset for response for each transaction
    # @param[in]    response_values List of values stored in response offset address
    # @param[in]    transaction_count Total number of transaction count in xml
    # @param[in]    ul_trigger_offset_for_trans offset which is check to initiate Link Training Transactions
    # @return       returns dp_dpcd_model_data struct
    # @cond
    @staticmethod
    # @endcond
    def set_dpcd_model_struct(input_starting_offsets, input_values, response_starting_offsets, response_values,
                              transaction_count=0, ul_trigger_offset_for_trans=0):
        dp_dpcd_model_data = dpcd_struct.DPDPCDModelData()
        st_dpcd_model_data = dp_dpcd_model_data.stDPCDModelData
        st_dpcd_model_data.ucTransactionCount = transaction_count
        st_dpcd_model_data.ulTriggerOffset = ul_trigger_offset_for_trans

        # Individual Transaction Template
        # <inputStartingOffsets>[0x102] or [] or [x,y]</inputStartingOffsets> < Max length 2>
        # <inputValues>[[0x21] or []</inputValues> < Max length 2, max sub-length 8 >
        # <responseStartingOffsets>[0x202, 0x210] or [] or [0x102]</responseStartingOffsets>
        # <responseValues>[[0x11, 0x11, 0x80], [0x20,0x10,0x11]] or [[0x11, 0x11, 0x80]] </responseValues>
        for trans_index in range(st_dpcd_model_data.ucTransactionCount):
            dpcd_trans = st_dpcd_model_data.stDPCDTransactions[trans_index]

            dpcd_trans.ucNumInputDpcdSets = len(input_starting_offsets[trans_index])
            for input_set_index in range(dpcd_trans.ucNumInputDpcdSets):
                dpcd_trans.stInputDpcdSets[input_set_index].ulStartingOffset = \
                    input_starting_offsets[trans_index][input_set_index]
                dpcd_trans.stInputDpcdSets[input_set_index].ucLength = \
                    len(input_values[trans_index][input_set_index])
                for input_value_index in range(dpcd_trans.stInputDpcdSets[input_set_index].ucLength):
                    dpcd_trans.stInputDpcdSets[input_set_index].ucValues[input_value_index] = \
                        input_values[trans_index][input_set_index][input_value_index]

            dpcd_trans.ucNumResponseDpcdSets = len(response_starting_offsets[trans_index])
            for res_set_index in range(dpcd_trans.ucNumResponseDpcdSets):
                dpcd_trans.stResponseDpcdSets[res_set_index].ulStartingOffset = \
                    response_starting_offsets[trans_index][res_set_index]
                dpcd_trans.stResponseDpcdSets[res_set_index].ucLength = \
                    len(response_values[trans_index][res_set_index])
                for res_value_index in range(dpcd_trans.stResponseDpcdSets[res_set_index].ucLength):
                    dpcd_trans.stResponseDpcdSets[res_set_index].ucValues[res_value_index] = \
                        response_values[trans_index][res_set_index][res_value_index]

        return dp_dpcd_model_data

    ##
    # @brief        This Utility/Helper functions helps in parsing xml text
    # @param[in]    str_text xml string text
    # @return       Either a list or int value containing parsed value
    # @cond
    @staticmethod
    # @endcond
    def get_dpcd_parsed_value(str_text):
        if str_text is None:
            logging.debug("Parsed value is None")
            return None
        if str_text.startswith('[['):
            str_text = str_text.replace('[[', '')
            str_text = str_text.replace(']]', '')
            if len(str_text) == 0:
                str_list = []
            else:
                str_list = str_text.split(",")
            tmp_input_values = []
            input_value = []
            inner_loop_cnt = 0
            outer_loop_cnt = 0
            for i in range(len(str_list)):
                if ']' in str_list[i]:
                    str_list[i] = str_list[i].replace(']', '')
                    if '0x' in str_list[i]:
                        tmp_input_values.insert(inner_loop_cnt, int(str_list[i], 16))
                    else:
                        tmp_input_values.insert(inner_loop_cnt, int(str_list[i]))
                    inner_loop_cnt += 1
                elif '[' in str_list[i]:
                    input_value.insert(outer_loop_cnt, tmp_input_values)
                    outer_loop_cnt += 1
                    inner_loop_cnt = 0
                    tmp_input_values = []
                    str_list[i] = str_list[i].replace('[', '')
                    if '0x' in str_list[i]:
                        tmp_input_values.insert(inner_loop_cnt, int(str_list[i], 16))
                    else:
                        tmp_input_values.insert(inner_loop_cnt, int(str_list[i]))
                    inner_loop_cnt += 1
                else:
                    if '0x' in str_list[i]:
                        tmp_input_values.insert(inner_loop_cnt, int(str_list[i], 16))
                    else:
                        tmp_input_values.insert(inner_loop_cnt, int(str_list[i]))
                    inner_loop_cnt += 1
            input_value.insert(outer_loop_cnt, tmp_input_values)
            return input_value
        elif str_text.startswith('['):
            str_text = str_text.replace('[', '')
            str_text = str_text.replace(']', '')
            if len(str_text) == 0:
                str_list = []
            else:
                str_list = str_text.split(",")
            for i in range(len(str_list)):
                if '0x' in str_list[i]:
                    str_list[i] = int(str_list[i], 16)
                else:
                    str_list[i] = int(str_list[i])
            return str_list
        else:
            if '0x' in str_text:
                return int(str_text, 16)
            else:
                return int(str_text)

    ##
    # @brief        This method helps in getting dp_dpcd_model_data in hex format
    # @param[in]    lists list input
    # @return       list in hex format
    def log_in_hex(self, lists):
        return [hex(item) if not isinstance(item, list) else self.log_in_hex(item) for item in lists]

    ##
    # @brief        This method helps in populating dpcd model data from xml to dp_dpcd_model_data struct
    # @param[in]    dpcd_model_xml_file dpcd_model_info File
    # @return       dp_dpcd_model_data
    def get_dpcd_model_data(self, dpcd_model_xml_file):
        if not os.path.exists(dpcd_model_xml_file.strip()):
            logging.error("[Test Issue]: DPCD Model file: {} not present".format(dpcd_model_xml_file))
            gdhm.report_bug(
                title="[Interfaces][DP_LT] DPCD Model Input file: {} is missing".format(dpcd_model_xml_file),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return None
        xml_root = xml_ET.parse(dpcd_model_xml_file).getroot()
        transaction_count = 0
        input_starting_offsets = []
        response_starting_offsets = []
        ul_trigger_offset_for_trans = []
        response_values = []
        input_values = []

        # Read XML and get DPCD model data in desired format
        for child in xml_root:
            if child.tag == 'DPCDModelData':
                for ul_trigger_offset_for_trans_val in child.findall('ulTriggerOffsetForTrans'):
                    ul_trigger_offset_for_trans = (self.get_dpcd_parsed_value(ul_trigger_offset_for_trans_val.text))
                for transaction in child.findall('transaction'):
                    transaction_count = transaction_count + 1
                    for input_starting_offsets_val in transaction.findall('inputStartingOffsets'):
                        input_starting_offsets.append(self.get_dpcd_parsed_value(input_starting_offsets_val.text))
                    for input_values_val in transaction.findall('inputValues'):
                        input_values.append(self.get_dpcd_parsed_value(input_values_val.text))
                    for response_starting_offsets_val in transaction.findall('responseStartingOffsets'):
                        response_starting_offsets.append(self.get_dpcd_parsed_value(response_starting_offsets_val.text))
                    for responseValues_val in transaction.findall('responseValues'):
                        response_values.append(self.get_dpcd_parsed_value(responseValues_val.text))

        logging.debug("ulTriggerOffsetForTrans: {}".format(hex(ul_trigger_offset_for_trans)))
        logging.debug("transactionCount: {}".format(transaction_count))
        logging.debug("inputStartingOffsets: {}".format(self.log_in_hex(input_starting_offsets)))
        logging.debug("inputValues: {}".format(self.log_in_hex(input_values)))
        logging.debug("responseStartingOffsets: {}".format(self.log_in_hex(response_starting_offsets)))
        logging.debug("responseValues: {}".format(self.log_in_hex(response_values)))

        # Validate DPCD Model Data
        if not self.validate_dpcd_model_data(transaction_count, input_starting_offsets, input_values,
                                             response_starting_offsets, response_values, ul_trigger_offset_for_trans):
            logging.error("[Test Issue]: Validation on DPCD Model Data Failed")
            # Gdhm bug reporting handled in validate_dpcd_model_data
            return None

        # populated dpcd modem data from xml file to dp_dpcd_model_data struct
        dp_dpcd_model_data = self.set_dpcd_model_struct(input_starting_offsets, input_values,
                                                        response_starting_offsets, response_values,
                                                        transaction_count, ul_trigger_offset_for_trans)
        return dp_dpcd_model_data
