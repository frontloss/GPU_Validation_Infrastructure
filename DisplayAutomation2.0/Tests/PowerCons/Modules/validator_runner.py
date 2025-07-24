########################################################################################################################
# @file     validator_runner.py
# @brief    Python wrapper helper module providing validator runner functionality for powercons features
#
# @author   Rohit Kumar, Vinod D S
########################################################################################################################

import json
import logging
import os
import re
import shutil
import time
import xml.etree.ElementTree as elementTree

from Libs.Core import enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context

from Tests.PowerCons.Modules import common

# Validators for legacy platforms
VALIDATORS = [
    {
        'Name': 'blc-frequency',
        'Feature': 'BLC',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    {
        'Name': 'blc-user-brightness',
        'Feature': 'BLC',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    {
        'Name': 'blc-phase-adjust',
        'Feature': 'BLC',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    {
        'Name': 'blc-duty-cycle',
        'Feature': 'BLC',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    {
        'Name': 'dpst-feature-status',
        'Feature': 'DPST',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    {
        'Name': 'dpst-algorithm-run-time',
        'Feature': 'DPST',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    {
        'Name': 'dpst-algorithm-result',
        'Feature': 'DPST',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    {
        'Name': 'drrs-feature-status',
        'Feature': 'DRRS',
        'Group': ['DRRS'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    {
        'Name': 'psr-feature-status',
        'Feature': 'PSR',
        'Group': ['PSR'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    {
        'Name': 'cxsr-feature-status',
        'Feature': 'CxSR',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['SKL', 'KBL', 'CFL', 'GLK']
    },
    # LACE validator doesn't support beyond ICL
    {
        'Name': 'lace-validate-read-hist-write-ie-values',
        'Feature': 'LACE',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['GLK']
    },
    {
        'Name': 'lace-feature-status',
        'Feature': 'LACE',
        'Group': ['PSR', 'DRRS', 'DPST_OVERRIDE'],
        'Platform': ['GLK']
    }
]

__POWERCONS_VALIDATOR_BIN = os.path.join(test_context.TEST_SPECIFIC_BIN_FOLDER, "PowerCons\\Validator")
__SYSTEM_STATIC_INFO_XML_FILE = os.path.join(__POWERCONS_VALIDATOR_BIN, "system_static_info.xml")
__TIMESTAMP = str(time.time())
__RUNNER_CONFIG_FILE = os.path.join(test_context.LOG_FOLDER, "validator_request_" + __TIMESTAMP + ".xml")
__RUNNER_OUTPUT_BASE_PATH = test_context.LOG_FOLDER + "\\"

__POWERCONS_DIANA_EXE = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna\\DiAna.exe")
__POWERCONS_DIANA_FAILURE_MAP = {
    'BLC': ['BLC_USERBRIGHTNESS_FAILURE', 'BLC_DUTYCYCLE_FAILURE', 'BLC_PHASEADJUST_FAILURE', 'BLC_FREQUENCY_FAILURE'],
    'DPST': ['DPST_ALGORITHMRUNTIME_FAILURE', 'DPST_ALGORITHMRESULT_FAILURE',
             'DPST_FEATURESTATUS_FAILURE', 'DPST_PHASEADJUST_FAILURE'],
    'DRRS': ['DRRS_FAILURE'],
    'PSR': ['PSR_FAILURE']
}


##
# @brief        Enum for panel target type
class TargetType(enum.Enum):
    PORT = 0
    PIPE = 1


##
# @brief        Exposed API to get the validators for a feature
# @param[in]    group string, of the feature
# @param[in]    feature string, feature for which the validators have to be filtered
# @return       feature_validators, if the any validators found
#               None otherwise
def get_validators(group, feature=None):
    platform = common.PLATFORM_NAME[:3]
    filtered_validators = [v['Name'] for v in VALIDATORS if platform in v['Platform'] and group in v['Group'] and (
            (feature is not None and feature == v['Feature']) or feature is None)]

    if len(filtered_validators) == 0:
        return None
    return sorted(filtered_validators)


##
# @brief        Exposed API to create validator request
# @param[in]    test_name name of the test in execution
# @param[in]    etw_log_path string, path of the etl file
# @return       xml file, if creation is successful
#               None, if xml creation is unsuccessful
def create_validator_request(test_name, etw_log_path, validators):
    if not os.path.exists(etw_log_path):
        logging.error("{0} NOT found".format(etw_log_path))
        return None

    if common.PLATFORM_NAME not in ['SKL', 'KBL', 'CFL', 'GLK']:
        logging.error("Validator runner is NOT supported for {0} platform".format(common.PLATFORM_NAME))
        return None

    power_cons_tag = elementTree.Element("PowerCons")

    platform_info_tag = elementTree.SubElement(power_cons_tag, "PlatformInfo")
    elementTree.SubElement(platform_info_tag, "ProductFamily").text = common.PLATFORM_NAME
    elementTree.SubElement(platform_info_tag, "PchProductFamily").text = 'UNKNOWN'
    elementTree.SubElement(platform_info_tag, "PlatformType").text = 'NONE'

    data_tag = elementTree.SubElement(power_cons_tag, "Data")
    elementTree.SubElement(data_tag, "EtwLogPath").text = etw_log_path
    elementTree.SubElement(data_tag, "SystemStaticInfo").text = __SYSTEM_STATIC_INFO_XML_FILE

    output_tag = elementTree.SubElement(power_cons_tag, "Output")
    elementTree.SubElement(output_tag, "BasePath").text = __RUNNER_OUTPUT_BASE_PATH
    elementTree.SubElement(output_tag, "TestName").text = test_name
    elementTree.SubElement(output_tag, "FileTimeStamp").text = __TIMESTAMP

    validators_tag = elementTree.SubElement(power_cons_tag, "Validators")
    for v in validators:
        elementTree.SubElement(validators_tag, "Name").text = v

    xml = elementTree.ElementTree(power_cons_tag)
    try:
        xml.write(__RUNNER_CONFIG_FILE)
        return __RUNNER_CONFIG_FILE
    except Exception as ex:
        logging.error(ex)
    return None


##
# @brief        Exposed API to run validator
# @param[in]    test_name name of the test in execution
# @param[in]    config_file string, config file path required for running validator
# @return       output, dictionary containing result and file path if validator run is successful
#               None, if run failed
def run_validators(test_name, config_file):
    # Check whether config file exists or not
    if not os.path.exists(config_file):
        logging.error("{0} NOT found (Test Issue)".format(config_file))
        return None
    # Get the appropriate validator exe name
    validator_exe = get_validator_binary()
    logging.info("PowerCons Validator Binary Name= {0}".format(validator_exe))

    # Check whether validator exe exists or not
    if validator_exe is None or not os.path.exists(os.path.join(__POWERCONS_VALIDATOR_BIN, validator_exe)):
        logging.error("{0}\\{1} NOT found (Test Issue)".format(__POWERCONS_VALIDATOR_BIN, validator_exe))
        return None

    os.chdir(__POWERCONS_VALIDATOR_BIN)
    status = os.system(validator_exe + " " + config_file)
    os.chdir(test_context.ROOT_FOLDER)
    if status != 0:
        logging.error("Failed to execute {0}. Please check that {0} is compatible with the driver used".format(
            validator_exe))
        validator_type = validator_exe.split("_", 1)[0]  # PowerConsYangra from PowerConsYangra_v7.exe
        gdhm_title = f"[PowerCons][AppCrash] Failed to execute {validator_type} EXE"
        gdhm.report_bug(
            title=gdhm_title,
            problem_classification=gdhm.ProblemClassification.APP_CRASH,
            component=gdhm.Component.Test.DISPLAY_POWERCONS,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E3
        )
        return None

    output_file = os.path.join(__RUNNER_OUTPUT_BASE_PATH, test_name + '_ValidatorResults' + __TIMESTAMP + ".xml")
    if not os.path.exists(output_file):
        logging.error("{0} NOT found (Test Issue)".format(output_file))
        return None
    try:
        output_file_tree = elementTree.parse(output_file)
    except Exception as ex:
        logging.error(ex)
        return None
    output = {}
    output_root = output_file_tree.getroot()
    for validator_result in output_root:
        output[validator_result[0].text] = {
            'result': validator_result[1].text,
            'output_file_path': validator_result[2].text
        }
        if validator_result[1].text.lower() != 'pass':
            with open(validator_result[2].text) as _f:
                output[validator_result[0].text]['error'] = _f.read()
    return output


##
# @brief        This is a helper function used to get the path of the validator exe file
# @return       exe_file, if file is found
#               None, if file not found
def get_validator_binary():
    # Check path exists - TestStore\TestSpecificBin\PowerCons\Validator
    if not os.path.exists(__POWERCONS_VALIDATOR_BIN):
        logging.error("{0} NOT found (Test Issue)".format(__POWERCONS_VALIDATOR_BIN))
        return None

    exe_file = None
    driver = 'yangra' if common.IS_DDRW else 'legacy'
    for file in os.listdir(__POWERCONS_VALIDATOR_BIN):
        if file.lower().endswith(".exe") and driver in file.lower():
            exe_file = file
            break
    return exe_file


##
# @brief        Exposed API to execute DiAna
# @param[in]    test_name name of the test in execution
# @param[in]    etl_file traced etl
# @param[in]    features list of features to be given in argument
# @param[in]    get_only_error bool, optional flag to get only error tag from json
# @return       new_output_file, json file located in logs folder
#               None, if failed in any condition
def run_diana(test_name, etl_file, features, get_only_error=False):
    # Check that etl_file exists or not
    if not os.path.exists(etl_file):
        logging.error(f"{etl_file} NOT found")
        return None

    # Check whether DiAna exe exists or not
    if not os.path.exists(__POWERCONS_DIANA_EXE):
        logging.error(f"{__POWERCONS_DIANA_EXE} NOT found (Test Issue)")
        return None

    log_file = test_name + (".txt" if get_only_error else ".json")
    report_tag = f" -REPORT ERROR > {log_file}" if get_only_error else f" -REPORT INFO -GDHM {log_file}"
    diana_cmd = ' '.join(list(map(lambda x: '-' + x, features))) + report_tag
    status = os.system(__POWERCONS_DIANA_EXE + " " + etl_file + " " + diana_cmd)
    logging.debug(f"Diana execution status = {bool(status)}")

    output_file = os.path.join(os.getcwd(), log_file)
    if not os.path.exists(output_file):
        logging.error(f"{output_file} NOT found (Test Issue)")
        gdhm.report_bug(
            title="[PowerCons][AppCrash] Failed to execute DiAna",
            problem_classification=gdhm.ProblemClassification.APP_CRASH,
            component=gdhm.Component.Driver.DISPLAY_POWERCONS,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E3
        )
        return None

    try:
        new_output_file = os.path.join(test_context.LOG_FOLDER, log_file)
        shutil.move(output_file, new_output_file)

    except Exception as ex:
        logging.error(ex)
        return None
    return new_output_file


##
# @brief        Exposed API to parse state machine failure from json file
# @param[in]    log_file, output file from DiAna
# @param[in]    features, list of features to be given in argument
# @return       new_output_file, json file located in logs folder
#               None, if failed in any condition
def parse_diana_output(log_file, features):
    if not os.path.exists(log_file):
        logging.error("{0} NOT found (Test Issue)".format(log_file))
        return None

    if ".txt" in log_file:
        result = __parse_text_file(log_file, features)
    else:
        result = __parse_json_file(log_file, features)

    return result


def __parse_json_file(log_file, features):
    result = {}
    try:
        with open(log_file) as f:
            data = f.read()
            invalid_strings = re.findall('new Date\(\d+\)', data)
            for invalid_string in invalid_strings:
                data = data.replace(invalid_string, '"0"')
            d = json.loads(data)
            for feature in features:
                for failure in __POWERCONS_DIANA_FAILURE_MAP[feature.upper()]:
                    key_feature = failure.replace('_FAILURE', '')
                    result[key_feature] = {'RESULT': 'FAIL' if failure in data else 'PASS',
                                           'FILE': log_file}
                    if result[key_feature]['RESULT'] == 'FAIL':
                        result[key_feature]['DETAILS'] = []
                        for msg in d['TagStore'].get(failure, []):
                            result[key_feature]['DETAILS'].append(
                                '(TimeStamp - {0} S): {1}'.format(float(msg['TimeStamp']) / 1000, msg['Details']))
    except Exception as ex:
        logging.error(ex)
        return None
    return result


def __parse_text_file(log_file, features):
    feature_error_tags = []
    error_tags_from_diana = []
    result = {}
    try:
        for feature in features:
            feature_error_tags += (__POWERCONS_DIANA_FAILURE_MAP[feature.upper()])

            # prepare result Dictionary with defaults of Details and Result
            for failure in __POWERCONS_DIANA_FAILURE_MAP[feature.upper()]:
                key_feature = failure.replace('_FAILURE', '')
                result[key_feature] = {'RESULT': 'PASS', 'FILE': log_file}
                if result[key_feature]['RESULT'] == 'FAIL':
                    result[key_feature]['DETAILS'] = []

        # get all the error tags from text file
        with open(log_file) as f:
            lines = f.readlines()
            for l in lines:
                if "Tags : " in l:
                    actual_tags = l.split(" ")

        # get all error tags which are required for feature verification
        for f in feature_error_tags:
            if f in actual_tags:
                error_tags_from_diana.append(f)

        # Compare all the error tags with individual lines to get the details and marking as FAIL
        with open(log_file) as f:
            lines = f.readlines()
            for fail in error_tags_from_diana:
                for l in lines:
                    if fail in l:
                        if "Tags : " in l:
                            result[fail.replace('_FAILURE', '')] = {'RESULT': 'FAIL'}
                        else:
                            if 'DETAILS' not in result[fail.replace('_FAILURE', '')]:
                                result[fail.replace('_FAILURE', '')]['DETAILS'] = [l]
                            else:
                                result[fail.replace('_FAILURE', '')]['DETAILS'].append(l)

    except Exception as ex:
        logging.error(ex)
        return None
    return result


##
# @brief        Exposed API to parse json file with specific event name
# @param[in]    adapter adapter object
# @param[in]    json_file output file from DiAna
# @param[in]    event_name etl event name as per the DiAna prints in json
# @param[in]    field_name field name of respective etl name
# @param[in]    target_check enum 1 if required to be look for PIPE, enum 0 for PORT
# @return       values dictionary, target wise if target_check is mentioned else all values in 1
#               None, if failed in any condition
def parse_etl_events(adapter, json_file, event_name, field_name, target_check=TargetType.PORT):
    if not os.path.exists(json_file):
        logging.error("{0} NOT found (Test Issue)".format(json_file))
        return None

    def fetch_value(event, field):
        ind = event.index(field + "= ")
        arr = (event[ind + len(field + "= "):]).split(',')
        field_values.append(int(arr[0]))

    values = {}
    brightness_event = "SET_BRIGHTNESS"
    nits_op_type = "SET_NITS_PANEL_LUMINANCE_OVERRIDE"
    #   sample ETL event name: BlcClientEvent, Field name: TargetBrightness
    #   BlcClientEvent(0.3770886 S): Port= PORT_A, PipeId= PIPE_A, Operation= SET_BRIGHTNESS, TargetBrightness= 1,
    #   field_values = [1]
    for panel in adapter.panels.values():
        field_values = []
        with open(json_file) as f:
            data = f.read()
            invalid_strings = re.findall('new Date\(\d+\)', data)
            for invalid_string in invalid_strings:
                data = data.replace(invalid_string, '"0"')
            d = json.loads(data)

            if target_check == TargetType.PIPE:
                target_type = "PipeId= PIPE_" + panel.pipe
            if target_check == TargetType.PORT:
                if panel.port in ['MIPI_A', 'MIPI_C']:
                    target_type = "Port= " + panel.port
                else:
                    target_type = "Port= PORT_" + panel.port.split('_')[1]  # DP_A -> A
            for msg in d['ReportQueue']:
                if event_name + '(' in msg['Header']:
                    event_list = [msg['Header']]
                    for e in event_list:
                        if target_check is None:
                            fetch_value(e, field_name)
                        elif target_type in e:
                            if event_name == "BlcClientEvent":
                                if brightness_event in e:
                                    fetch_value(e, field_name)
                            elif event_name == "BlcGetSetNitsBrightness":
                                if nits_op_type in e:
                                    fetch_value(e, field_name)
                            else:
                                fetch_value(e, field_name)
        if target_check is None:
            # some events are irrespective of Pipe or Port then assign all in one and break
            values['NONE'] = field_values
            break
        else:
            target = panel.pipe if target_check == TargetType.PIPE else panel.port
            values[target] = field_values
    return values


##
# @brief        Exposed API to parse json file with specific event name
# @param[in]    adapter adapter object
# @param[in]    json_file output file from DiAna
# @param[in]    error_msg in etl event name as per the DiAna prints in json
# @return       returns True if the nitranges are inCorrect
def get_error_from_diana(adapter, json_file, error_msg):
    error_msg_present = False
    if not os.path.exists(json_file):
        logging.error("{0} NOT found (Test Issue)".format(json_file))
        return None

    # checks the Diana that it is Invalid Nit Ranges or not
    for panel in adapter.panels.values():
        field_values = []
        with open(json_file) as f:
            data = f.read()
            invalid_strings = re.findall('new Date\(\d+\)', data)
            for invalid_string in invalid_strings:
                data = data.replace(invalid_string, '"0"')
            d = json.loads(data)
            for msg in d['ReportQueue']:
                if error_msg not in msg['Header']:
                    error_msg_present = False
            for msg in d['ReportQueue']:
                if error_msg in msg['Header']:
                    error_msg_present = True

    return error_msg_present


if __name__ == '__main__':
    print(get_validators(group='PSR'))
    print(get_validators(group='PSR', feature='BLC'))
    print(create_validator_request("SampleTestName", "Logs\\sample.etl", get_validators(group='PSR')))
