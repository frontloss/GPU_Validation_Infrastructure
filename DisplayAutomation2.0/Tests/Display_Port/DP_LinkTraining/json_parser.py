##########################################################################################################
# @file         json_parser.py
# @brief        This file contains helper functions for parsing DPCD model data from XML file.
# @author       Ashish Kumar
##########################################################################################################

import json
import logging

__report = {
    'DpLinkTrainingData': None,
}


##
# @brief JsonParser Class
class JsonParser:
    ##################################################################################
    # Exposed APIs
    ##################################################################################

    ##
    # @brief        Exposed API to load data from report
    # @param[in]    report_name json file path
    # @return       True if reloading is successful, False otherwise
    # @cond
    @staticmethod
    # @endcond
    def load_report(report_name):
        global __report
        try:
            with open(report_name) as f:
                __report = json.load(f)
        except OSError as err:
            logging.error("error: {0}, Fail to open {1}".format(err, report_name))
            return __report
        return __report

    ##
    # @brief        Exposed helper API to check if given key is present in __report dictionary
    # @param[in]    key key string
    # @return       dict value for respective key if found in dictionary, None otherwise
    # @cond
    @staticmethod
    # @endcond
    def get_event_list(key):
        global __report
        if key in __report.keys():
            return __report[key]
        else:
            return None


##
# @brief    Exposed object for storing DpLinkTraining event data
class DpLinkTrainingData:
    LTStatus = None  # Boolean
    CRIterations = None  # Int
    EQIterations = None  # Int
    PreEmphasis = None  # Int
    VoltageSwing = None  # Int
    Port = None  # String
    Tag = None  # String
    DataType = None  # String
    Level = None  # String
    TimeStamp = None  # Float : Time in ms

    ##
    # @brief        Constructor definition for DpLinkTrainingData class
    # @param[in]    data_dict dictionary of (key, values) for parameters that need to be set in this object.
    def __init__(self, data_dict):
        for k in data_dict.keys():
            self.__setattr__(k, data_dict[k])

    ##
    # @brief    For printing DpLinkTrainingData
    # @return   None
    def __repr__(self):
        return "LTStatus= {0}, CRIterations= {1}, EQIterations= {2}, PreEmphasis= {3}, VoltageSwing= {4}, " \
               "Port= {5}, Tag= {6}, DataType= {7}, Level= {8}, TimeStamp= {9}".format(
                    self.LTStatus, self.CRIterations, self.EQIterations, self.PreEmphasis, self.VoltageSwing,
                    self.Port, self.Tag, self.DataType, self.Level, self.TimeStamp)
