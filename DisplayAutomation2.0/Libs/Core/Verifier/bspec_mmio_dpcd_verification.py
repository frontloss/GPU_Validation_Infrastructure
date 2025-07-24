########################################################################################################################
# @file     bspec_mmio_dpcd_verification.py
# @brief    This module is used to check any wrong mmio programming/ BSPEC violation in given etl file.
# @author   Nainesh Doriwala
########################################################################################################################
import logging

from Libs.Core.test_env import test_context
from Libs.Core.logger import gdhm
from Libs.Core.Verifier.common_verification_args import VerifierCfg, ErrorCode, DIANA_ERROR_JSON_FILE, Verify
from Libs.Core.Verifier.diana_analysis import parse_diana_output


##
# @brief    API to initialize bspec verification
# @return   None
def initialize():
    pass


##
# @brief        verify and detect bspec violation using DiAna
# @param[in]    result - Test result object
# @return       None
def verify(result):
    # Return None if DiAna Crash for particular etl
    if VerifierCfg.diana_status_code is False:
        return
    if VerifierCfg.bspec_violation == Verify.SKIP:
        logging.info("Bspec MMIO violation verification has skipped")
    else:
        # Verify Bspec violation using DiAna
        verify_bspec_mmio_violation_using_diana()
    # DPCD violation verification check
    if VerifierCfg.dpcd_violation == Verify.SKIP:
        logging.info("DPCD violation verification has skipped")
    else:
        # Verify DPCD violation using DiAna
        verify_dpcd_violation_using_diana()


##
# @brief        Logs and return Bspec MMIO verification status using diana
# @details      MMIO verification status is logged and returned if voilation is observed in etl file
#               and observed with DiAna Analysis
# @return       None
def verify_bspec_mmio_violation_using_diana():
    logging.debug("Bspec violation verification using DiAna Analyzer")
    if VerifierCfg.diana_return_error_code & ErrorCode.BSPEC_VIOLATION.value:

        logging.warning("Bspec violation observed using DiAna Analyzer")
        json_data = parse_diana_output(DIANA_ERROR_JSON_FILE, "BSPEC_VIOLATION")
        for error in json_data:
            logging.warning("[{0}]: {1}".format(VerifierCfg.platform, error['DETAILS']))
            test_context.DiagnosticDetails().save_etl = True
            gdhm.report_bug(
                title="[DiAnaAnalysisLib] {0}".format(error['DETAILS']),
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE
            )
    else:
        logging.info("[{0}] - No BSPEC VIOLATION Observed.".format(VerifierCfg.platform))


##

# @brief        Logs and return DPCD verification status using diana
# @details      DPCD verification status is logged and returned if violation is observed in etl file
#               and observed with DiAna Analysis
# @return       Bool True violation observed, False violation not observed
def verify_dpcd_violation_using_diana():
    logging.debug("DPCD violation verification using DiAna Analyzer")
    if VerifierCfg.diana_return_error_code & ErrorCode.DPCD_VIOLATION.value:
        test_context.DiagnosticDetails().save_etl = True
        logging.warning("DPCD violation observed using DiAna Analyzer")
        json_data = parse_diana_output(DIANA_ERROR_JSON_FILE, "DPCD_VIOLATION")
        for error in json_data:
            logging.warning("[{0}]: {1}".format(VerifierCfg.platform, error['DETAILS']))
            gdhm.report_bug(
                title="[DiAnaAnalysisLib] {0}".format(error['DETAILS']),
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE
            )
    else:
        logging.info("[{0}] - No DPCD VIOLATION Observed.".format(VerifierCfg.platform))


##
# @brief        API to cleanup Bspec Violationc verification
# @return       None
def cleanup():
    pass
