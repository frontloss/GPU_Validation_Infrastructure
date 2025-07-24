########################################################################################################################
# @file         tdr_verification.py
# @brief        This module is used to monitor tdr on graphics driver
# @author       Nainesh Doriwala
########################################################################################################################
import logging
import sys

from Libs.Core import display_essential
from Libs.Core.Verifier.common_verification_args import VerifierCfg, ErrorCode, DIANA_ERROR_JSON_FILE, Verify
from Libs.Core.Verifier.diana_analysis import parse_diana_output
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context


##
# @brief    API to initialize TDR verifications
# @return   None
def initialize():
    if VerifierCfg.tdr == Verify.LOG_CRITICAL:
        # clear system log for tdr verification during test.
        display_essential.clear_system_log()


##
# @brief        verify and detect TDR using DiAna or system event log
# @param[in]    result - Test result object
# @return       status - True if TDR is generated, False otherwise
def verify(result):
    status = False
    if VerifierCfg.tdr == Verify.SKIP:
        logging.info("TDR verification has skipped")
        return status
    # Verify tdr with system level log for each graphics adapter if diana crash or config set to skip
    if VerifierCfg.diana_status_code is False:
        if __verify_tdr_using_system_log() is True:
            status = True
    else:
        if __verify_tdr_using_diana() is True:
            status = True
    if status and VerifierCfg.tdr == Verify.LOG_CRITICAL:
        result.errors.append((sys.argv[0], "TDR Observed during the test"))
    return status


##
# @brief        Logs and return tdr status , if TDR is observed in etl file and observed with DiAna Analysis
# @details      verify and detect tdr on graphics driver using system event log
# @return       is_tdr_observed - True if tdr is observed and reported by DiAna, False otherwise.
def __verify_tdr_using_system_log():
    # type: () -> bool

    is_tdr_observed = False
    logging.debug("TDR verification using system event log")

    # Gets the gfx adapter details from test_context
    gfx_adapter_details_dict = test_context.TestContext.get_gfx_adapter_details()

    # Iterate through the list of gfx device and unplug the stale external displays if any for each gfx device.
    for gfx_index, gfx_adapter_info in gfx_adapter_details_dict.items():
        if display_essential.detect_system_tdr(gfx_index=gfx_index) is True:
            logging.info("TDR observed for gfx_index:{}".format(gfx_index))
            is_tdr_observed = True

    return is_tdr_observed


##
# @brief        Logs and return tdr status , if TDR is observed in etl file and observed with DiAna Analysis
# @details      Verify tdr using etl parsing to DiAna
# @return       is_tdr_observed - True if tdr is observed and reported by DiAna, False otherwise.
def __verify_tdr_using_diana():
    # type: () -> bool

    is_tdr_observed = False
    logging.debug("TDR verification using DiAna Analyzer")
    if VerifierCfg.diana_return_error_code & ErrorCode.TDR.value:

        logging.info("TDR observed using DiAna Analyzer")
        json_data = parse_diana_output(DIANA_ERROR_JSON_FILE, "TDR")
        for error in json_data:
            logging.critical("[{0}]: {1}".format(VerifierCfg.platform, error['DETAILS']))
        is_tdr_observed = True
    else:
        logging.info("[{0}] - No TDR Observed.".format(VerifierCfg.platform))

    return is_tdr_observed


##
# @brief        API to cleanup TDR verification
# @return       None
def cleanup():
    if VerifierCfg.tdr == Verify.LOG_CRITICAL:
        # clear system log for tdr verification during test.
        display_essential.clear_system_log()
