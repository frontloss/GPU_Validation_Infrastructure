########################################################################################################################
# @file     underrun_verification.py
# @brief    This module is used to monitor under-runs generated on all the pipes.
# @author   Nainesh Doriwala
########################################################################################################################
import logging
import struct
import sys

from Libs.Core import system_utility as sys_utility, registry_access
from Libs.Core.Verifier.common_verification_args import VerifierCfg, ErrorCode, DIANA_ERROR_JSON_FILE, Verify
from Libs.Core.Verifier.diana_analysis import parse_diana_output
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context

UNDERRUN_REGISTRY_KEYS = ['UnderRunCountPipeA', 'UnderRunCountPipeB', 'UnderRunCountPipeC', 'UnderRunCountPipeD']
UNDERRUN_FAIL_TEST_PLATFORMS = ['JSL', 'EHL', 'ICL', 'LKF', 'LKFR', 'TGL', 'ADLS', 'RKL', 'RYF', 'DG1']


##
# @brief        API to initialize all required config for under-run verification.
# @return       None
def initialize():
    if VerifierCfg.underrun == Verify.LOG_CRITICAL:
        # Clear under-run registry for both adapter
        _clear_underrun_registry()


##
# @brief        Clear the under-run counter register to zero for all adapters.
# @return       None
def _clear_underrun_registry():
    # type: () -> None

    binary_type_data = (registry_access.RegDataType.BINARY, bytes([0, 0, 0, 0]))
    dword_type_data = (registry_access.RegDataType.DWORD, 0)

    # Gets the gfx adapter details from test_context
    gfx_adapter_details_dict = test_context.TestContext.get_gfx_adapter_details()

    # Iterate through each adapter and reset the registry counters.
    for gfx_index, gfx_adapter_info in gfx_adapter_details_dict.items():

        # Fill the registry information to be written based on the driver type.
        is_ddrw = sys_utility.SystemUtility().is_ddrw(gfx_index)

        reg_data_type, reg_data_list = binary_type_data if is_ddrw is True else dword_type_data
        reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)
        # Iterate through all underrun registry keys and reset the values based on the driver type.
        for reg_key in UNDERRUN_REGISTRY_KEYS:
            registry_access.write(args=reg_args, reg_name=reg_key, reg_type=reg_data_type, reg_value=reg_data_list)

    logging.info("Cleared UnderRunCount for all pipes")


##
# @brief        Logs and returns underrun status for each gfx adapter, if underrun is observed.
# @details      Note: Test should not invoke this API. Only called from framework in TestEnvironment.cleanup()
# @param[in]    result - Test result object
# @return       status - True if under-run observed, False otherwise.
def verify(result):
    status = False
    if VerifierCfg.underrun == Verify.SKIP:
        logging.info("Under-run verification has skipped")
        return status
    # verify under-run with registry based method.
    if VerifierCfg.diana_status_code is False:
        status = _verify_underrun_with_registry(file_gdhm=True)
    else:
        status = __verify_underrun_using_diana()
    if status and VerifierCfg.underrun == Verify.LOG_CRITICAL and VerifierCfg.platform in UNDERRUN_FAIL_TEST_PLATFORMS:
        result.errors.append((sys.argv[0], "Under-run occurred."))
    return status


##
# @brief        Logs and return underrun status , if under-run is observed in etl file and observed with DiAna Analysis
# @details      Verify under-run using etl parsing to DiAna. Files GDHM bug if underrun is observed.
# @return       is_underrun_observed - True if underrun is observed and reported by DiAna, False otherwise.
def __verify_underrun_using_diana():
    # type: () -> bool
    critical = '1-Critical'
    is_underrun_observed = False

    logging.debug("Under-run verification using DiAna Analyzer")
    if VerifierCfg.diana_return_error_code & ErrorCode.UNDERRUN.value:
        test_context.DiagnosticDetails().save_etl = True
        feature = __get_feature()

        json_data = parse_diana_output(DIANA_ERROR_JSON_FILE, "Underrun")
        for error in json_data:
            plane_status = "PLANE_OFF"
            if critical == error['CRITICAL']:
                if VerifierCfg.platform in UNDERRUN_FAIL_TEST_PLATFORMS:
                    logging.critical("[{0}] [{1}]: {2}".format(feature, VerifierCfg.platform, error['DETAILS']))
                else:
                    logging.error("[{0}] [{1}]: {2}".format(feature, VerifierCfg.platform, error['DETAILS']))
                is_underrun_observed = True
                plane_status = "PLANE_ON"
            gdhm_title = "[DiAnaAnalysisLib] [{0}] [{1}] [{2}]: {3}".format(feature, VerifierCfg.platform,
                                                                            plane_status, error['DETAILS'])
            gdhm_priority = gdhm.Priority.P2 if VerifierCfg.platform in UNDERRUN_FAIL_TEST_PLATFORMS else gdhm.Priority.P1
            gdhm_exposure = gdhm.Exposure.E2 if VerifierCfg.platform in UNDERRUN_FAIL_TEST_PLATFORMS else gdhm.Exposure.E1
            gdhm.report_bug(
                title=gdhm_title,
                problem_classification=gdhm.ProblemClassification.UNDER_RUN,
                priority=gdhm_priority,
                exposure=gdhm_exposure
            )
    else:
        logging.info("[{0}] - No UnderRun Observed.".format(VerifierCfg.platform))

    return is_underrun_observed


##
# @brief        Logs and returns underrun status for each gfx adapter, if underrun is observed in any of the pipe.
# @details      verify and detect under-run on display Pipes using registry. Files GDHM bug if underrun is observed.
# @param[in]    file_gdhm - File GDHM bug if True, else do not file a bug. Added to handle duplicate bugs filed
#               Note: Only to be logged from framework side during cleanup
# @return       is_underrun_observed - True if underrun is observed is at least one of the gfx adapter, False otherwise
def _verify_underrun_with_registry(file_gdhm=False):
    # type: () -> bool
    is_underrun_observed = False
    feature = __get_feature()

    '''
+        Get the under-run status and iterate through the dict and log the Pipe and Under-run count info including the
        Graphics adapter name in which the under-run occurred.
    '''
    logging.debug("Under-run verification using registry")
    device_underrun_status = __get_underrun_status()
    for gfx_index, underrun_info in device_underrun_status.items():
        if underrun_info is not None and len(underrun_info.keys()) > 0:
            test_context.DiagnosticDetails().save_etl = True
            underrun_string = ", ".join(["%s[%s]" % (x, underrun_info[x]) for x in underrun_info.keys()])
            if file_gdhm is True:
                gdhm_string = ", ".join([x for x in underrun_info.keys()])
                if VerifierCfg.platform in UNDERRUN_FAIL_TEST_PLATFORMS:
                    gdhm_priority, gdhm_exposure = gdhm.Priority.P2, gdhm.Exposure.E2
                else:
                    gdhm_priority, gdhm_exposure = gdhm.Priority.P1, gdhm.Exposure.E1

                gdhm.report_bug(
                    title="[{0}] {1}: UnderRun Observed on {2}".format(feature, gfx_index, gdhm_string),
                    problem_classification=gdhm.ProblemClassification.UNDER_RUN,
                    priority=gdhm_priority,
                    exposure=gdhm_exposure
                )
            logging.error("[{0}] {1}: UnderRun Observed on {2}".format(feature, gfx_index, underrun_string))
            is_underrun_observed = True
        else:
            logging.info("%s - No UnderRun Observed." % gfx_index)

    return is_underrun_observed


##
# @brief        get feature name
# @return       feature - returns feature name example: MPO, BLC, COLLAGE and sub-feature (if any)
def __get_feature():
    feature: str = "PrepareDisplay"
    sub_feature: str = ""

    try:
        if len(sys.argv) > 0:
            cmd_line = sys.argv[0].replace('/', '\\')
            if 'Tests\\' in cmd_line:
                feature_split = cmd_line.split('\\')
                # Get Sub-feature
                if len(feature_split) > 3 and feature_split[-2] != feature_split[1]:
                    sub_feature = "_" + feature_split[-2]
                # Get Feature
                feature = feature_split[1] + sub_feature
    except Exception as e:
        logging.warning(e)
        feature = "PrepareDisplay"

    return feature


##
# @brief        Gets the under-run status of each pipe available in each of the adapter present in the system.
# @return       device_underrun_status - dictionary which contains under-run status of each pipe
#               present in each gfx adapter.
#               Eg: { 'gfx_0': { 'PIPEA' : 2, 'PIPEC' : 4}, 'gfx_1': {'PIPEA': 2, 'PIPEC': 1} }
def __get_underrun_status():
    # type: () -> dict

    is_found = False

    # Gets the gfx adapter details from test_context
    gfx_adapter_details_dict = test_context.TestContext.get_gfx_adapter_details()

    # Creates a dict with keys as 'gfx_0, gfx_1, ...'
    device_underrun_status = dict.fromkeys(gfx_adapter_details_dict.keys(), {})

    # Iterate through each adapter and get the under-run status for each adapter present in the system.
    for gfx_index, gfx_adapter_info in gfx_adapter_details_dict.items():

        # Fill the registry information to be written based on the driver type.
        is_ddrw = sys_utility.SystemUtility().is_ddrw(gfx_index)

        reg_data_type = registry_access.RegDataType.BINARY if is_ddrw is True else registry_access.RegDataType.DWORD

        # Iterate through under-run registry keys and read the registry to get the under-run count for each of pipe.
        for reg_key in UNDERRUN_REGISTRY_KEYS:
            reg_args = registry_access.StateSeparationRegArgs(gfx_index)
            reg_value, _ = registry_access.read(args=reg_args, reg_name=reg_key)

            # Unpack the value based on the data type of the value present in reg_value.
            if reg_value is not None:
                underrun_count = struct.unpack("<L", reg_value)[0] \
                    if reg_data_type == registry_access.RegDataType.BINARY else reg_value

                # Update the dict if under-run count is greater than zero based on gfx_device and pipe_name info.
                if underrun_count > 0:
                    pipe_name = reg_key[-5:].upper()
                    device_underrun_status[gfx_index].update({pipe_name: underrun_count})

                is_found = True

    if is_found is False:
        logging.error("GetUnderRunStatus - Reg Key Missing or Not Enabled in GFX Driver")

    return device_underrun_status


##
# @brief        Cleanup API method
# @return       None
def cleanup():
    pass
