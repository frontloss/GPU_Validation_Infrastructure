########################################################################################################################
# @file         diana_analysis.py
# @brief        Contains diana analysis
# @author       Nainesh Doriwala
########################################################################################################################
import json
import logging
import os
from subprocess import call

from Libs.Core.Verifier.common_verification_args import VerifierCfg, ErrorCode, DIANA_ERROR_JSON_FILE
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context

DIANA_EXE = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna", "DiAna.exe")

SIMPLIFY_VIOLATIONS = ['BSPEC_VIOLATION']


##
# @brief        Exposed API to execute DiAna
# @param[in]    etl_file_name - etl file under log folder to analyze
# @param[in]    diana_cmd  - diana command line which require as input to diana apart from etl file
#               example: diana_cmd = "-dispdiag" or diana_cmd = "-REPORT INFO -blc test.json"
# @param[in]    bdf - Bus Device Function string
# @return       bool - True if ETL analyzed successfully, False otherwise
def analyze(etl_file_name, diana_cmd=' ', bdf=None):
    # check for etl_file and diana exe
    etl_file = os.path.join(test_context.LOG_FOLDER, etl_file_name)
    if not os.path.exists(etl_file):
        logging.error("{0} NOT found".format(etl_file))
        gdhm.report_bug(
            f"[DiAnaAnalysisLib] Unable to find ETL file",
            gdhm.ProblemClassification.LOG_FAILURE,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
        return False

    # Check whether DiAna exe exists or not
    if not os.path.exists(DIANA_EXE):
        logging.error("{0} NOT found (Test Issue)".format(DIANA_EXE))
        gdhm.report_bug(
            f"[DiAnaAnalysisLib] Unable to find DiAna exe",
            gdhm.ProblemClassification.LOG_FAILURE,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
        return False

    # Removing existing ErrorTagReport.json file before passing new file to DiAna
    if os.path.exists(DIANA_ERROR_JSON_FILE):
        logging.info("removing {0} file from path{1}".format(DIANA_ERROR_JSON_FILE[-19:], os.getcwd()))
        os.unlink(DIANA_ERROR_JSON_FILE)

    if run_diana(etl_file, etl_file_name, diana_cmd, bdf=bdf) is False:
        return False

    if VerifierCfg.diana_return_error_code & int(ErrorCode.UNSUCCESSFUL.value):
        logging.warning("DiAna exited unsuccessful")
        gdhm.report_bug(
            f"[DiAnaAnalysisLib] DiAna exited unsuccessfully",
            gdhm.ProblemClassification.LOG_FAILURE,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
        return False
    if VerifierCfg.diana_return_error_code != int(ErrorCode.SUCCESSFUL.value):
        if not os.path.exists(DIANA_ERROR_JSON_FILE):
            gdhm_title = "[DiAnaAnalysisLib] Failed to generate {0} file".format(DIANA_ERROR_JSON_FILE[-19:])
            gdhm.report_bug(
                title=gdhm_title,
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False
    return True


##
# @brief        This function runs DiAna for analysis of given ETL file based on file size
# @param[in]    etl_file - ETL File Path
# @param[in]    etl_file_name - DiAna file name
# @param[in]    diana_cmd - Process commandline for running DiAna
# @param[in]    bdf - Bus Device Function string
# @return       any - False if timeout occurred or falling back to registry based analysis,
#               else return error code from process output
def run_diana(etl_file: str, etl_file_name: str, diana_cmd: str, bdf: str = "") -> any:
    # Retry condition to increase timeout during test execution, if process takes longer than expected.
    retry_count = 2

    # WA: Get ETL Size in GigaBytes for setting appropriate timeout
    # Added to apply timeouts based on ETL file size, since time taken to analyze depends on the same
    # Converting the ETL Bytes value received from stat function to GB
    etl_file_size = round((os.stat(etl_file).st_size / pow(1024, 3)), 2)
    logging.debug(f"Generated ETL File {etl_file} with file_size : {etl_file_size} GB")
    index, VerifierCfg.max_timeout = VerifierCfg._get_max_timeout(etl_file_size)
    if VerifierCfg.max_timeout == 0:
        # Fall back to Registry based analysis
        return False

    # Run DiAna for Analysis and save logs into diana_log.txt
    diana_log_file_name = "diana_log_" + etl_file_name[:-4] + "_bdf_" + bdf.replace(":", "_") + ".txt"
    logging.debug("diana_log_file_name:{}".format(diana_log_file_name))
    diana_log_file = os.path.join(test_context.LOG_FOLDER, diana_log_file_name)
    # Iterate based on retry count in case of exception occurred while running DiANa cmd
    while retry_count:
        with open(diana_log_file, "w") as diana_log:
            try:
                bdf_cmd = "" if bdf is None else "-BDF "
                diana_cmd = " ".join([DIANA_EXE, etl_file, diana_cmd, "-basicverification", bdf_cmd, bdf])
                logging.info(f"Parsing ETL file {etl_file} with DiAna command {diana_cmd}")
                VerifierCfg.diana_return_error_code = call(diana_cmd, stdout=diana_log, timeout=VerifierCfg.max_timeout,
                                                           universal_newlines=True)
                logging.info("return_err_code : {0}".format(hex(VerifierCfg.diana_return_error_code)))
                retry_count = 0  # Exit upon successful parsing
            except Exception as e:
                if retry_count == 1:
                    logging.error(f"Failed to parse ETL through DiAna with error - {e}")
                # If exception occurs, update the timeout to next value from the VerifierCfg._timeout list
                # Else, Fall back to Registry based analysis
                if index is not None and index < (len(VerifierCfg._timeout) - 1):
                    # Set next timeout value from list
                    logging.debug(f"Insufficient timeout({VerifierCfg.max_timeout}) to analyse current ETL file of "
                                  f"size {etl_file_size} GB")
                    VerifierCfg.max_timeout = VerifierCfg._timeout[index + 1]
                    retry_count -= 1
                    # File GDHM bug if parsing failed even after increasing timeout
                    if retry_count <= 0:
                        gdhm.report_bug(
                            title="[DiAnaAnalysisLib] Insufficient timeout({0})s to analyse current ETL".format(
                                VerifierCfg.max_timeout),
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Test.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P3,
                            exposure=gdhm.Exposure.E3
                        )
                else:
                    # If current timeout is maximum index, we do not need to perform retry logic.
                    # Hence, Fall back to Registry based analysis
                    VerifierCfg.diana_return_error_code = False
    return VerifierCfg.diana_return_error_code


##
# @brief        Exposed API to parse json file based in feature/problem classification
# @param[in]    json_file - json file to parse
# @param[in]    feature - to check in json file as problem classification
# @return       result - list of error or empty list
def parse_diana_output(json_file, feature):
    result = []
    try:
        with open(json_file) as f:
            data = json.load(f)
            for key, values in data.items():
                for value in values:
                    if feature == value['Problem_classification']:
                        if feature == 'BSPEC_VIOLATION':
                            tag_bspec_violation(value, result)
                        else:
                            result.append({'DETAILS': value['Title'], 'CRITICAL': value['Exposure']})
    except Exception as ex:
        logging.error(ex)
        gdhm.report_bug(
            title="[DiAnaAnalysisLib] [{0}] Failed to parse ErrorTagReport.json File".format(VerifierCfg.platform),
            problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
            component=gdhm.Component.Test.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P3,
            exposure=gdhm.Exposure.E3
        )
        result = []
    return result


##
# @brief        Method to isolate and add warning tags to bugs without history
# @param[in]    value - Bugs entry list from ErrorTagReport.json
# @param[in]    result - bug_report.json to report identified GDHM entry
# @return       None. Appends separated BSpec MMIO Violations as individual GDHM Bug to existing result list
def tag_bspec_violation(value: dict, result: list) -> None:
    gdhm_title = value['Title']
    description = value['Description']

    if "History not present for Verification" in description:
        gdhm_title = "[WARNING] " + gdhm_title
    result.append({'DETAILS': gdhm_title, 'CRITICAL': value['Exposure']})
