########################################################################################################################
# @file     assert_verification.py
# @brief    This module is used to check any assert in given etl file.
# @author   Nainesh Doriwala
########################################################################################################################
import logging
import os

from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.Verifier.common_verification_args import VerifierCfg, ErrorCode, DIANA_ERROR_JSON_FILE, Verify
from Libs.Core.Verifier.diana_analysis import parse_diana_output
from Libs.Core import etl_parser


##
# @brief    API to initialize assert verification
# @return   None
def initialize():
    pass


##
# @brief        verify and detect assert using DiAna or etl parser
# @param[in]    etl_file_name - ETL File Name
# @return       None
def verify(etl_file_name=None):
    if VerifierCfg.assert_verification == Verify.SKIP:
        logging.info("Assert verification has skipped")
        return
    # Verify assert using etl parser for each etl if diana crash
    if VerifierCfg.diana_status_code is False:
        verify_assert_using_etl_parser(etl_file_name)
    else:
        verify_assert_using_diana()
    return


##
# @brief        Exposed API to report display driver asserts to GDHM
# @param[in]    etl_file_name - The ETL File name
# @return       None
def __report_driver_assert(etl_file_name):
    try:
        config = etl_parser.EtlParserConfig()
        config.commonData = 1

        etl_file = os.path.join(test_context.LOG_FOLDER, etl_file_name)
        if etl_parser.generate_report(etl_file, config) is False:
            logging.warning(f"Failed to generate report for {etl_file_name}")
            return

        logging.info(f"Checking for any DDASSERT entry in {etl_file_name}")
        assert_output = etl_parser.get_event_data(etl_parser.Events.DISPLAY_ASSERT)
        if assert_output is None:
            logging.info("\tPASS: No DDASSERT entry found")
            return
        test_context.DiagnosticDetails().save_etl = True

        for assert_data in assert_output:
            logging.warning("\t{0}".format(assert_data))
            gdhm.report_bug(
                title="DDASSERT {0} {1}".format(assert_data.Function, assert_data.Assert),
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE
            )
    except Exception as e:
        logging.warning(e)


##
# @brief        Verify assert using etl parsing for passed etl file
# @details      tdr status is logged and returned if TDR is observed in etl file and observed with DiAna Analysis
# @param[in]    etl_file_name - ETL file name
# @return       None
def verify_assert_using_etl_parser(etl_file_name):
    logging.debug("Assert verification using etl parser")
    if etl_file_name is not None:
        __report_driver_assert(etl_file_name)
    else:
        for etl_file_name in os.listdir(test_context.LOG_FOLDER):
            if etl_file_name.endswith('.etl'):
                __report_driver_assert(etl_file_name)


##
# @brief        Logs assert details using diana
# @details      assert details is logged if Assert is observed in etl file and observed with DiAna Analysis
# @return       None
def verify_assert_using_diana():

    logging.debug("Assert verification using DiAna Analyzer")
    if VerifierCfg.diana_return_error_code & ErrorCode.ASSERT.value:

        logging.warning("Assert observed using DiAna Analyzer")
        json_data = parse_diana_output(DIANA_ERROR_JSON_FILE, "DISPLAY_ASSERT")
        for error in json_data:
            logging.warning("[{0}]: {1}".format(VerifierCfg.platform, error['DETAILS']))
            assert_details = error["DETAILS"].split("@")
            assert_reason = assert_details[0].split(":")
            functions = assert_details[1].split(" ")
            test_context.DiagnosticDetails().save_etl = True

            gdhm.report_bug(
                title="DDASSERT {0} {1}".format(functions[-3][:-2], assert_reason[1]),
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE
            )
    else:
        logging.info("[{0}] - No ASSERT Observed.".format(VerifierCfg.platform))


##
# @brief        API to cleanup assert verification
# @return       None
def cleanup():
    pass
