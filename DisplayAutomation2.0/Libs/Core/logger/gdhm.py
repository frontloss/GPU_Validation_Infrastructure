########################################################################################################################
# @file         gdhm.py
# @brief        Exposed library for reporting bugs to GDHM
# @author       Rohit Kumar, Kiran Kumar Lakshmanan
########################################################################################################################
import json
import logging
import os
import shutil
from configparser import ConfigParser

from Libs.Core.test_env import test_context

traces_file_name = "Traces.7z"

GDHM_DIAG_LOG_DIR = "C:\\DiagLogs"
DISPLAY_GDHM_BUG_REPORT_PATH = os.path.join(GDHM_DIAG_LOG_DIR, "display_gdhm_bug_report.json")
DEFAULT_NOTIFY_LIST = ['GTA_Execution_BA', 'VPG Display HSD Group']
COMPONENT_NOTIFY_LIST = {
    "ip.graphics_test.display_interfaces": ['VTT SWS DISPLAY VAL DI Compliance'],
    "ip.graphics_test.display_os_features": ['GSE Display Val OS_Features'],
    "ip.graphics_test.display_powercons": ['VPG SWE Display Val DI1'],
    "ip.graphics_test.display_gfx_automation": [],
    "ip.test_display_audio_driver": ['VPG SWE Display Val DI1'],
    "ip.graphics_driver.display_interfaces": ['VTT SWS DISPLAY VAL DI Compliance'],
    "ip.graphics_driver.display_os_features": ['GSE Display Val OS_Features'],
    "ip.graphics_driver.display_powercons": ['VPG SWE Display Val DI1'],
    "ip.display_audio_driver": ['VPG SWE Display Val DI1'],
    "ip.graphics_driver.control_library": ['GSE Display Val OS_Features', 'VPG SWE Display Val DI1']
}


##
# @brief        Exposed object class for HSD component data
class Component(object):

    ##
    # @brief    Test Components
    class Test(object):
        DISPLAY_INTERFACES = "ip.graphics_test.display_interfaces"
        DISPLAY_OS_FEATURES = "ip.graphics_test.display_os_features"
        DISPLAY_POWERCONS = "ip.graphics_test.display_powercons"
        DISPLAY_GFX_AUTOMATION = "ip.graphics_test.display_gfx_automation"
        DISPLAY_AUDIO = "ip.test_display_audio_driver"
        DISPLAY_VAL_INFRA = "ip.graphics_test.display_val_infra"

    ##
    # @brief    Driver components
    class Driver(object):
        DISPLAY_INTERFACES = "ip.graphics_driver.display_interfaces"
        DISPLAY_OS_FEATURES = "ip.graphics_driver.display_os_features"
        DISPLAY_POWERCONS = "ip.graphics_driver.display_powercons"
        DISPLAY_AUDIO = "ip.display_audio_driver"
        DISPLAY_CONTROL_LIBRARY = "ip.graphics_driver.control_library"


##
# @brief        Exposed object class for HSD problem classification data
class ProblemClassification(object):
    APP_CRASH = "app_crash"
    COMPLIANCE = "compliance"
    CORRUPTION = "corruption"
    FLICKER = "flicker"
    FUNCTIONALITY = "functionality"
    LOG_FAILURE = "log_failure"
    OTHER = "other"
    PERFORMANCE = "performance"
    SYSTEM_CRASH = "system_crash"
    UNDER_RUN = "underrun"


##
# @brief        Exposed object class for HSD priority data
class Priority(object):
    P1 = "p1-showstopper"
    P2 = "p2-high"
    P3 = "p3-medium"
    P4 = "p4-low"


##
# @brief        Exposed object class for HSD exposure data
class Exposure(object):
    E1 = "1-critical"
    E2 = "2-high"
    E3 = "3-medium"
    E4 = "4-low"


##
# @brief        Exposed API to report bug to GDHM. This API will add the bug entry in JSON file, which will be shared
#               with GDHM after finishing the test.
# @note         Recommended to use component specific APIs listed below to make use of pre-defined fields to keep the
#               code readable at caller side
#               For Driver Issue,
#                   report_driver_bug_di(): Display Interfaces Component
#                   report_driver_bug_os(): Display OS Component
#                   report_driver_bug_pc(): Display PC Component
#                   report_driver_bug_audio(): Display Audio Component
#               For Test Issue,
#                   report_test_bug_di(): Display Interfaces Component
#                   report_test_bug_os(): Display OS Component
#                   report_test_bug_pc(): Display PC Component
#                   report_test_bug_audio(): Display Audio Component
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem_classification - string from ProblemClassification class
# @param[in]    component [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_bug(title, problem_classification, component=None, priority=None, exposure=None):
    assert title
    assert problem_classification
    # Set default values
    if priority is None:
        priority = Priority.P2
    if exposure is None:
        exposure = Exposure.E2
    # Create bug entry. This will be added in JSON file.
    bug_entry = {
        'title': title,
        'problem_classification': problem_classification,
        'notify': DEFAULT_NOTIFY_LIST
    }
    if component is not None:
        bug_entry['component'] = component
        bug_entry['notify'] += COMPONENT_NOTIFY_LIST[component]
    if priority is not None:
        bug_entry['priority'] = priority
    if exposure is not None:
        bug_entry['exposure'] = exposure
    if os.path.exists(DISPLAY_GDHM_BUG_REPORT_PATH) is False:
        # Bug report doesn't exists, this is the first bug to be added in file
        # Check for DiagLogs directory exists or not, if not, create one
        if os.path.exists(GDHM_DIAG_LOG_DIR) is False:
            os.mkdir(GDHM_DIAG_LOG_DIR)
        with open(DISPLAY_GDHM_BUG_REPORT_PATH, "w") as f:
            json.dump({'bugs': [bug_entry]}, f)
        return
    # Get already added bugs from report
    with open(DISPLAY_GDHM_BUG_REPORT_PATH) as f:
        existing_bugs = json.load(f)['bugs']
    # check if same title is already available
    for bug_ in existing_bugs:
        if bug_['title'] == title:
            return
    existing_bugs.append(bug_entry)
    with open(DISPLAY_GDHM_BUG_REPORT_PATH, "w") as f:
        json.dump({'bugs': existing_bugs}, f)


##
# @brief        Exposed API to clear the GDHM report (if any)
# @return       None
def clear_report():
    if os.path.exists(DISPLAY_GDHM_BUG_REPORT_PATH):
        try:
            os.remove(DISPLAY_GDHM_BUG_REPORT_PATH)
        except Exception as e:
            logging.warning(f"Exception in clearing GDHM report: {e}")


##
# @brief        copy GDHM logs to logs folder
# @return       None
def copy_gdhm_logs():
    _configParser = ConfigParser()
    gdhm_etl = "FAIL_ONLY"
    gdhm_bug = "ENABLE"
    if os.path.exists(os.path.join(test_context.TEST_TEMP_FOLDER, "config.ini")):
        _configParser.read(os.path.join(test_context.TEST_TEMP_FOLDER, "config.ini"))
        if _configParser.has_option('GENERAL', 'GDHM_ETL'):
            gdhm_etl = _configParser.get('GENERAL', 'GDHM_ETL')
        if _configParser.has_option('GENERAL', 'GDHM_BUG'):
            gdhm_bug = _configParser.get('GENERAL', 'GDHM_BUG')

    try:
        # Copy ETL files(Traces.7z) to GDHM DiagLogs folder
        if gdhm_etl != "FAIL_ONLY":
            # Check for DiagLogs directory exists or not, if not, create one
            if os.path.exists(GDHM_DIAG_LOG_DIR) is False:
                os.mkdir(GDHM_DIAG_LOG_DIR)

            if traces_file_name in os.listdir(test_context.LOG_FOLDER):
                shutil.copyfile(os.path.join(test_context.LOG_FOLDER, traces_file_name),
                                os.path.join(GDHM_DIAG_LOG_DIR, traces_file_name))
    except Exception as e:
        logging.error(e)

    try:
        if os.path.exists(DISPLAY_GDHM_BUG_REPORT_PATH):
            shutil.copyfile(DISPLAY_GDHM_BUG_REPORT_PATH, os.path.join(test_context.LOG_FOLDER, "bug_report.log"))

            # Delete the GDHM bug report if option is disabled in config.ini
            if gdhm_bug != 'ENABLE':
                os.remove(DISPLAY_GDHM_BUG_REPORT_PATH)

    except Exception as e:
        logging.error(e)


##
# @brief        Exposed API for DI DRIVER ISSUE to report GDHM
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_driver_bug_di(title: str, problem=ProblemClassification.FUNCTIONALITY,
                         priority=Priority.P2, exposure=Exposure.E2):
    report_bug(title, problem, Component.Driver.DISPLAY_INTERFACES, priority, exposure)


##
# @brief        Exposed API for OS DRIVER ISSUE to report GDHM
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_driver_bug_os(title: str, problem=ProblemClassification.FUNCTIONALITY,
                         priority=Priority.P2, exposure=Exposure.E2):
    report_bug(title, problem, Component.Driver.DISPLAY_OS_FEATURES, priority, exposure)


##
# @brief        Exposed API for PC DRIVER ISSUE to report GDHM
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_driver_bug_pc(title: str, problem=ProblemClassification.FUNCTIONALITY,
                         priority=Priority.P2, exposure=Exposure.E2):
    report_bug(title, problem, Component.Driver.DISPLAY_POWERCONS, priority, exposure)


##
# @brief        Exposed API for AUDIO DRIVER ISSUE to report GDHM
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_driver_bug_audio(title: str, problem=ProblemClassification.FUNCTIONALITY,
                            priority=Priority.P2, exposure=Exposure.E2):
    report_bug(title, problem, Component.Driver.DISPLAY_AUDIO, priority, exposure)


##
# @brief        Exposed API for CONTROL LIBRARY DRIVER ISSUE to report GDHM
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_driver_bug_clib(title: str, problem=ProblemClassification.FUNCTIONALITY,
                         priority=Priority.P2, exposure=Exposure.E2):
    report_bug(title, problem, Component.Driver.DISPLAY_CONTROL_LIBRARY, priority, exposure)


##
# @brief        Exposed API for DI TEST ISSUE to report GDHM
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_test_bug_di(title: str, problem=ProblemClassification.FUNCTIONALITY,
                       priority=Priority.P2, exposure=Exposure.E2):
    report_bug(title, problem, Component.Test.DISPLAY_INTERFACES, priority, exposure)


##
# @brief        Exposed API for OS TEST ISSUE to report GDHM
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_test_bug_os(title: str, problem=ProblemClassification.FUNCTIONALITY,
                       priority=Priority.P2, exposure=Exposure.E2):
    report_bug(title, problem, Component.Test.DISPLAY_OS_FEATURES, priority, exposure)


##
# @brief        Exposed API for PC TEST ISSUE to report GDHM
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_test_bug_pc(title: str, problem=ProblemClassification.FUNCTIONALITY,
                       priority=Priority.P2, exposure=Exposure.E2):
    report_bug(title, problem, Component.Test.DISPLAY_POWERCONS, priority, exposure)


##
# @brief        Exposed API for AUDIO TEST ISSUE to report GDHM
# @param[in]    title - string, Title of the HSD bug
# @param[in]    problem [Optional]- string from Component class
# @param[in]    priority [Optional]- string from Priority class
# @param[in]    exposure [Optional]- string from Exposure class
# @return       None
def report_test_bug_audio(title: str, problem=ProblemClassification.FUNCTIONALITY,
                          priority=Priority.P2, exposure=Exposure.E2):
    report_bug(title, problem, Component.Test.DISPLAY_AUDIO, priority, exposure)
