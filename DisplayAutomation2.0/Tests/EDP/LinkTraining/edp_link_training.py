########################################################################################################################
# @file         edp_link_training.py
# @brief        The file contain basic API for edp Link Training
# @author       Tulika
########################################################################################################################
import logging
from enum import IntEnum

from Tests.PowerCons.Modules import dpcd
from Libs.Core import etl_parser

ETL_PARSER_CONFIG = etl_parser.EtlParserConfig()
ETL_PARSER_CONFIG.commonData = 1

# GDHM header
GDHM_LT = "[Display_Interfaces][EDP][LINK_TRAINING]"


##
# @brief        This class has value for edp tps.
class TrainingPatternSequence(IntEnum):
    TRAINING_PAT_1 = 1
    TRAINING_PAT_2 = 2
    TRAINING_PAT_3 = 3
    TRAINING_PAT_4 = 12


##
# @brief        This functions verifies link training in the diana file.
# @param[in]    diana_log_file
# @return       True if link training found else False
def verify_link_training(diana_log_file):
    status = False
    try:
        with open(diana_log_file, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if "Link Training SUCCESS" in line:
                    status = True
            return status
    except IOError:
        logging.error(f"FAIL: Diana file read error: {diana_log_file}")
        return False


##
# @brief        This function checks the training pattern that is supported in DPCD
# @param[in]    panel
# @return       training pattern from dpcd
def get_training_pattern_sequence_from_dpcd(panel):
    dpcd_rev = dpcd.get_edp_revision(panel.target_id)
    lane_count = dpcd.MaxLaneCount(panel.target_id)
    max_down_spread = dpcd.MaxDownSpread(panel.target_id)
    if dpcd_rev >= dpcd.EdpDpcdRevision.EDP_DPCD_1_4_A and max_down_spread.tps4_supported:
        return TrainingPatternSequence.TRAINING_PAT_4
    if lane_count.tps3_supported:
        return TrainingPatternSequence.TRAINING_PAT_3
    return TrainingPatternSequence.TRAINING_PAT_2
