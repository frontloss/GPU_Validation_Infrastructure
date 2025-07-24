#######################################################################################################################
# @file         common.py
# @brief        Contains global constants, custom tags, functions and decorators used across eDP, power cons and VRR
#               tests
#
# @author       Rohit Kumar
#######################################################################################################################

import logging
import os
import sys
import unittest
from functools import wraps
from operator import attrgetter
from typing import List, Dict

from Libs.Core import cmd_parser, driver_escape
from Libs.Core import enum
from Libs.Core import system_utility
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context

from Tests.PowerCons.Modules.dut_context import Panel
from Tests.PowerCons.Modules.dut_context import Adapter
from Libs.Feature.powercons import registry

# Common Objects
system_utility_ = system_utility.SystemUtility()
display_config_ = display_config.DisplayConfiguration()
__critical_tests = []

# Common Constants
IS_DDRW = system_utility_.is_ddrw()
IS_PRE_SI = system_utility_.get_execution_environment_type() in ["SIMENV_FULSIM", "SIMENV_PIPE2D"]
PLATFORM_NAME = machine_info.SystemInfo().get_gfx_display_hardwareinfo()[0].DisplayAdapterName
PLATFORM_REGISTERS_DIR = PLATFORM_NAME.replace('_', '').lower()
POWER_EVENT_DURATION_DEFAULT = 20
MAX_LINE_WIDTH = 64
MAX_TEST_SECTIONS = 9
TEST_VIDEOS_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "TestVideos")
MPO_VIDEOS_PATH = os.path.join(test_context.SHARED_BINARY_FOLDER, "MPO")

# All simulated eDP EDIDs have serial abc1230. Byte representation of 'ab' 'c1' '23' '00' in reverse
SIMULATED_EDP_SERIAL = [0, 35, 193, 171]

GEN_09_PLATFORMS = ['SKL', 'KBL', 'CFL']
GEN_10_PLATFORMS = ['GLK', 'CNL', 'APL']
GEN_11_PLATFORMS = ['ICLLP', 'EHL', 'JSL']
GEN_11p5_PLATFORMS = ['LKF1']
GEN_12_PLATFORMS = ['TGL', 'RKL', 'DG1', 'ADLS']
GEN_13_PLATFORMS = ['DG2', 'ADLP']
GEN_14_PLATFORMS = ['DG3', 'MTL', 'ELG']
GEN_15_PLATFORMS = ['LNL']
GEN_16_PLATFORMS = ['PTL']
GEN_17_PLATFORMS = ['CLS', 'NVL']
PRE_GEN_11_PLATFORMS = GEN_09_PLATFORMS + GEN_10_PLATFORMS
PRE_GEN_11_P_5_PLATFORMS = PRE_GEN_11_PLATFORMS + GEN_11_PLATFORMS
PRE_GEN_12_PLATFORMS = GEN_09_PLATFORMS + GEN_10_PLATFORMS + GEN_11_PLATFORMS + GEN_11p5_PLATFORMS
PRE_GEN_13_PLATFORMS = PRE_GEN_12_PLATFORMS + GEN_12_PLATFORMS
PRE_GEN_14_PLATFORMS = PRE_GEN_13_PLATFORMS + GEN_13_PLATFORMS
PRE_GEN_15_PLATFORMS = PRE_GEN_14_PLATFORMS + GEN_14_PLATFORMS
PRE_GEN_16_PLATFORMS = PRE_GEN_15_PLATFORMS + GEN_15_PLATFORMS
PRE_GEN_17_PLATFORMS = PRE_GEN_16_PLATFORMS + GEN_16_PLATFORMS

CUSTOM_TAGS = [
    # Common
    "-SELECTIVE",  # OR operation
    "-SELECTIVE2",  # AND operation
    "-REPEAT",
    "-TEST_SEQUENCE",

    # VRR
    "-APP",  # rectangle, triangle, cube, angrybots
    "-STATE",  # enabled, disabled, auto
    "-DURATION",  # in minutes
    "-GAME",  # game option for FlipAt app
    "-PATTERN",  # manual FPS pattern for FlipAt app
    "-TILED",  # To identify Tiled panel

    # PSR / PnP
    "-FEATURE",  # psr1, psr2, lrr1, lrr1.5, lrr2, auto
    "-DCSTATES",  # true, false
    "-METHOD",  # 'video'
    "-COUNT",  # SPI count
    "-WORKLOAD",  # IDLE, VIDEO
    "-TOOL",  # socwatch, giraffe
    "-DELAYED_VBLANK",  # delayed Vblank supported high RR panel

    # DRRS/ DMRRS/ LRR
    "-NORMAL_RR",
    "-FRACTIONAL_RR",
    "-CLOCK_BASED",
    "-VRR_BASED",
    "-HRR",
    "-LOOP_VIDEO",
    "-VIDEO",
    "-MEDIA_RR",
    "-DISABLE_LRR",
    "-RR_PROFILE",
    "-WITH",  # common tag to keep it enabled

    # VDSC/ DPST
    "-BPC_VALUE",  # '6, 8, 10, 12
    "-PRE_SILICON",  # 'FULSIM', 'FULSIM_SKIP_ANALYZE'
    "-BLC_THRESHOLD",  # number (percent)
    "-LOWER_BLC_THRESHOLD",  # number (milli percent)
    "-UPPER_BLC_THRESHOLD",  # number (milli percent)
    "-MAX_SMOOTHENING_SPEED",  # DPST temporal filter Max cutoff frequency in Milli Hz
    "-MIN_SMOOTHENING_SPEED",  # DPST temporal filter Min cutoff frequency in Milli Hz
    "-DPST_VERSION",  # 6_3, 7_0, 7_1
    "-OPST",  # Tag to indicate OPST
    "-LEVEL",  # Tag to indicate OPST aggressiveness Level
    "-INDEPENDENT_BRIGHTNESS",
    "-TIME_DELAY",
    "-CO_EXIST",  # Tag to indicate CABC co-existence with XPST
    "-OS_OPTION",  # Tag to indicate OS Option (AlwaysOn, OnBattery, Off)

    # EDP FLT/FMS
    "-FLT",  # true, false
    "-FMS",  # true, false
    "-PHY",  # true, false
    "-VSWING_TABLE",  # low/high

    # BLC
    "-HDR",  # true, false
    "-HIGH_PRECISION",  # enable high precision
    "-NIT_RANGES",  # 30_590_1 (min_max_step-size)
    "-NIT_RANGES_FFFF",  # disable boost nit ranges
    "-INVALID_NIT_RANGES",  # 30_590_1_595_700_10
    "-DISABLE_NITS_BRIGHTNESS",  # disable nits brightness and move to brightness2

    # Manual/ BLC
    "-MANUAL",  # true, false
    "-DISPLAY1", "-DISPLAY2", "-DISPLAY3", "-DISPLAY4",
    "-LFP1", "-LFP2",

    "-UBZRR", "-UBLRR", "-UBALL"
]


########################################################################################################################
#
# Python Unittest Framework Helpers
#
# This section contains decorators and some helper function to ease up the task to implement tests using python unittest
# framework. The most commonly used decorator is configure_test. Using this decorator, user can define any selective
# condition to run the test, block the test, repeat the test etc. For more info please see the decorator documentation.
# Other than this decorator, some functions are also provided to get custom test suite based on the decorator use and
# command line.
########################################################################################################################

##
# @brief        Internal helper function to parse given command line based on special tags
# @param[in]    tags, List, list of custom tags starting with "-"
# @return       parsed_cmdline, dict, parse_cmdline output
def __parse_command_line(tags):
    custom_tags = [custom_tag.upper() for custom_tag in sys.argv if custom_tag.startswith("-") and
                   cmd_parser.display_flag_pattern.match(custom_tag.upper()) is None and
                   custom_tag.upper() not in ["-CONFIG", "-LOGLEVEL", "-LFP_NONE"] and
                   not custom_tag.upper().startswith("-GFX_")]

    for tag in tags:
        custom_tags += [tag] if tag not in custom_tags else []

    output = cmd_parser.parse_cmdline(sys.argv, custom_tags)
    if isinstance(output, dict):
        return [output]
    return output


##
# @brief        Internal helper function to make decorator parameterized
# @param[in]    decorator, function, targeted decorator function
# @return       modified decorator with given parameters
def __parameterized_decorator(decorator):
    def caller_layer(*args, **kwargs):
        def callee_layer(f):
            return decorator(f, *args, **kwargs)

        return callee_layer

    return caller_layer


##
# @brief        Exposed decorator to configure any given test
# @description  configure_test decorator provides multiple options to configure any given test. A list of available
#               options is given below:
#               repeat:
#               If this option is set to True, it will repeat the targeted test function multiple times.
#               Repeat count is decided based on '-repeat' parameter in command line.
#
#               critical:
#               If this option is set to True, upon failure of target function the execution will be stopped.
#
#               selective:
#               This is a multi purpose option. User can provide a list of strings to identify the test uniquely. Using
#               the same string in command line with -selective or -selective2, user can run a part of the test without
#               running all the test functions. There are some predefined strings also, that have a special meaning.
#               A list of special strings is given below:
#                   BLOCKED:
#                       if "BLOCKED" string is a part of selective list, that test function will not be executed
#                   LEGACY:
#                       The test will be executed only on legacy driver
#                   YANGRA:
#                       The test will be executed only on Yangra driver
#                   PRE_SI:
#                       The test will be executed only on Pre-Si environment
#                   POST_SI:
#                       The test will be executed only on Post-Si environment
#
#               Example:
#                   For examples, please refer eDP FLT/FMS/ASSR or VRR tests
#
# @param[in]    func, Function, target test
# @param[in]    repeat, Boolean, If true, test will be repeated based on '-repeat' value
# @param[in]    selective, List, a list of whitelisted events for the test.
# @param[in]    critical, Boolean, If true, on test failure execution will be stopped
# @return       wrapped function
@__parameterized_decorator
def configure_test(func, repeat=False, selective=None, critical=False):
    global __critical_tests

    wraps(func)
    ##
    # Check if test is critical
    if critical:
        __critical_tests.append(func.__name__)

    ##
    # -REPEAT:      repeat tag is used to run a test multiple times. If there is no value given for repeat in command
    #               line all the tests will be executed only once.
    # -SELECTIVE:   selective tag is used to run only selective tests. If there is no value given for selective in
    #               command line, all the tests will be executed.
    #
    # Both of the above features can be used in any test case. Selective list can be expanded to include more possible
    # events.
    cmd_line_params = __parse_command_line(["-TEST_SEQUENCE", "-REPEAT", "-SELECTIVE", "-SELECTIVE2"])

    ##
    # Check if test has some selective conditions
    if selective is not None:
        ##
        # Check for blocked tests
        if "BLOCKED" in selective:
            return

        ##
        # Check for Yangra of Legacy
        if "LEGACY" in selective and IS_DDRW:
            return
        if "YANGRA" in selective and not IS_DDRW:
            return

        ##
        # Check for Pre-Si or Post-Si environment
        if "POST_SI" in selective and IS_PRE_SI:
            return
        if "PRE_SI" in selective and not IS_PRE_SI:
            return

        ##
        # If no selective condition is given in command line all tests will run
        # If there is some selective condition given in command line, test will run only if one or more selective
        # conditions are present in selective_test_list
        if (selective != ["LEGACY"] and selective != ["YANGRA"]) and \
                (cmd_line_params[0]['SELECTIVE'] != 'NONE' and
                 len(set(selective) & set(cmd_line_params[0]['SELECTIVE'])) == 0):
            return

        if (selective != ["LEGACY"] and selective != ["YANGRA"]) and \
                (cmd_line_params[0]['SELECTIVE2'] != 'NONE' and
                 len(set(selective) & set(cmd_line_params[0]['SELECTIVE2'])) != len(cmd_line_params[0]['SELECTIVE2'])):
            return

    ##
    # Check for test repeat count
    number_of_repeats = 1
    if repeat is True and cmd_line_params[0]['REPEAT'] != 'NONE':
        number_of_repeats = int(cmd_line_params[0]['REPEAT'][0])

    def wrapper(*args, **kwargs):
        status = True
        error_message = None
        for index in range(number_of_repeats):
            if number_of_repeats > 1:
                logging.info("")
                logging.info("{0} iteration : {1}".format(func.__name__, index + 1))
                logging.info("")
            try:
                func(*args, **kwargs)
            except Exception as e:
                status = False
                logging.error(e, exc_info=True)
                error_message = e
        if status is False:
            assert False, error_message

    return wrapper


##
# @brief        Common TestResult class for all the test cases
class CommonTestResult(unittest.TestResult):
    critical_tests = []

    def __init__(self, stream=None, descriptions=None, verbosity=None, critical_tests=None):
        super(CommonTestResult, self).__init__(stream, descriptions, verbosity)
        self.critical_tests = critical_tests

    def addFailure(self, test, err):
        if getattr(test, '_testMethodName') in self.critical_tests:
            self.stop()
        unittest.TestResult.addFailure(self, test, err)


##
# @brief        Exposed function to get test suite based on test sequence parameter
# @param[in]    test_case_class, TestCase, unittest test case class
# @param[in]    section_list[optional], List, a list of sections in the given test case
# @return       test_suite, List, a list of tests based on given parameters
def get_test_suite(test_case_class, section_list=None):
    if section_list is None:
        section_list = map(str, range(MAX_TEST_SECTIONS))

    cmd_line_params = __parse_command_line(["-TEST_SEQUENCE"])
    test_suite = None
    if cmd_line_params[0]['TEST_SEQUENCE'] != 'NONE':
        for test_name in cmd_line_params[0]['TEST_SEQUENCE']:
            test_name = test_name.lower()
            if test_suite is None:
                test_suite = unittest.makeSuite(test_case_class, prefix=test_name)
            else:
                temp_test_suite = unittest.makeSuite(test_case_class, prefix=test_name)
                setattr(test_suite, '_tests', getattr(test_suite, '_tests') + getattr(temp_test_suite, '_tests'))
    else:
        for section in section_list:
            if test_suite is None:
                test_suite = unittest.makeSuite(test_case_class, prefix=("t_" + section))
                if len(getattr(test_suite, '_tests')) > 0:
                    to_be_shuffled = getattr(test_suite, '_tests')[1:]
                    # random.shuffle(to_be_shuffled)
                    setattr(test_suite, '_tests', [getattr(test_suite, '_tests')[0]] + to_be_shuffled)
            else:
                temp_test_suite = unittest.makeSuite(test_case_class, prefix=("t_" + section))
                if len(getattr(temp_test_suite, '_tests')) > 0:
                    to_be_shuffled = getattr(temp_test_suite, '_tests')[1:]
                    # random.shuffle(to_be_shuffled)
                    setattr(
                        test_suite,
                        '_tests',
                        getattr(test_suite, '_tests') + [getattr(temp_test_suite, '_tests')[0]] + to_be_shuffled)

    test_sequence = [getattr(t, '_testMethodName') for t in getattr(test_suite, '_tests')]
    logging.debug("Test Sequence: {0}".format(' '.join(test_sequence)))
    return test_suite


##
# @brief        Exposed function to get test result class
def get_test_result_class(stream, descriptions, verbosity):
    global __critical_tests
    return CommonTestResult(stream, descriptions, verbosity, __critical_tests)


########################################################################################################################
#
# Other Misc Helper Functions
#
# print_current_topology() : prints current display configuration with target id, panel name and active resolution
#
########################################################################################################################

##
# @brief        Helper function to print current display configuration with resolution and refresh rate
# @param[in]    prefix[optional], string
def print_current_topology(prefix=""):
    enumerated_displays = display_config_.get_enumerated_display_info()
    current_config = display_config_.get_current_display_configuration_ex()
    topology = current_config[0]
    for index in range(len(current_config[1])):
        current_mode = display_config_.get_current_mode(enumerated_displays.ConnectedDisplays[index].TargetID)
        panel_name = enumerated_displays.ConnectedDisplays[index].FriendlyDeviceName
        if panel_name == '':
            panel_name = 'Internal Display'
        temp = " {0} (TargetID= {1}, PanelName= \"{2}\", Res= {3}x{4}@{5})".format(
            current_config[1][index],
            enumerated_displays.ConnectedDisplays[index].TargetID,
            panel_name,
            current_mode.HzRes,
            current_mode.VtRes,
            current_mode.refreshRate
        )
        topology += temp
    logging.info("{0}Current Topology= {1}".format(prefix, topology))


##
# @brief        Helper function to get supported refresh rates
# @param[in]    target_id, Number
# @param[in]    mrl_block, Boolean, True if MRL block to be considered to get RR, False otherwise
# @return       rr_list, List, a list of refresh rates
# @todo         remove this function once all features are using DUT
def get_supported_refresh_rates(target_id, mrl_block=False):
    rr_list = set()

    ##
    # Fetch the RR given in MRL block if mrl_block flag is True
    if mrl_block:
        edid_flag, edid_data, _ = driver_escape.get_edid_data(target_id)
        if not edid_flag:
            logging.error(f"Failed to get EDID data for target_id : {target_id}")
            assert edid_flag, "Failed to get EDID data"
        index = 54  # start of 1st 18 byte descriptor
        while index < 126:
            if edid_data[index + 3] == 0xFD:  # 0xFD is display range limits block
                if edid_data[index + 5] != 0:
                    rr_list.add(edid_data[index + 5])
                if edid_data[index + 6] != 0:
                    rr_list.add(edid_data[index + 6])
                break
            index += 18
        return list(rr_list)

    all_supported_modes = display_config_.get_all_supported_modes([target_id])
    for _, modes in all_supported_modes.items():
        for mode in modes:
            rr_list.add(mode.refreshRate)

    return list(rr_list)


##
# @brief        Helper function to get supported modes
# @param[in]    target_id, Number
# @return
def get_display_mode(target_id, refresh_rate=None, limit=1, scaling=None):
    mode_list = []
    all_supported_modes = display_config_.get_all_supported_modes([target_id])
    for _, modes in all_supported_modes.items():
        modes = sorted(modes, key=attrgetter('HzRes', 'refreshRate'), reverse=True)
        if refresh_rate is None and limit == 2 and scaling is None:
            mode_list.append(modes[0])  # Max
            mode_list.append(modes[-1])  # Min
            break

        for mode in modes:
            if refresh_rate is not None and mode.refreshRate != refresh_rate:
                continue
            if scaling is not None and mode.scaling == enum.MDS:
                continue
            mode_list.append(mode)
            if limit is not None and limit == len(mode_list):
                break

    if len(mode_list) < 1:
        logging.error("Failed to get Display mode")
        gdhm.report_driver_bug_os("Failed to get Display mode")
        return None

    if limit == 1:
        return mode_list[0]  # Max/Native

    return mode_list


##
# @brief        Exposed API to convert pixel clock value to linkM value
# @param[in]    link_rate, int
# @param[in]    pixel_clock, int
# @return       link_m_value, int
def pixel_clock_to_link_m(link_rate, pixel_clock):
    assert link_rate
    assert pixel_clock

    link_rate_mbps = int(link_rate * 1000)
    dot_clock_in_hz = pixel_clock

    adjusted_link_symbol_clock100_hz = (link_rate_mbps * 1000)
    adjusted_pixel_clock100_hz = dot_clock_in_hz / 100

    # link M and N
    # M / N = desired pixel clock / link symbol clock
    adjusted_link_symbol_clock100_hz /= 10000

    intermediate_link_m_result = adjusted_pixel_clock100_hz
    intermediate_link_m_result *= 0x80000
    intermediate_link_m_result *= 10000
    intermediate_link_m_result = (intermediate_link_m_result / adjusted_link_symbol_clock100_hz)

    logging.debug(f"IntermediateLinkM Value): {intermediate_link_m_result / 100000000}")
    # Using precision of 10^8
    return intermediate_link_m_result / 100000000


##
# @brief        Helper function to check whether connected eDP is simulated or physical
# @param[in]    target_id, Number
# @return       status, Boolean
# @todo         Move this as a panel capability in dut_context
def is_simulated_panel(target_id):
    edid_flag, edid_data, _ = driver_escape.get_edid_data(target_id)
    if not edid_flag:
        logging.error(f"Failed to get EDID data for target_id : {target_id}")
        assert edid_flag, "Failed to get EDID data"
    return edid_data[12:16] == SIMULATED_EDP_SERIAL


##
# @brief        Helper API to convert duration to Hz.
# @param[in]    duration, int
# @return       hz, float
def duration_to_hz(duration):
    if duration == 0:
        return 0
    return round((((10 ** 10) + (duration / 2.0)) / float(duration)) / 1000.0, 3)


##
# @brief        Helper function to set native mode of the panel
# @param[in]    panel object, Panel
# @return       status bool, True is successful, False otherwise
def set_native_mode(panel: Panel):
    native_mode = get_display_mode(panel.target_id)
    logging.info(f"Native mode for {panel.port}= {native_mode}")

    status = display_config_.set_display_mode([native_mode], False)

    if status:
        logging.info(f"Successfully to applied native mode for {panel.port}")
    else:
        logging.error(f"FAILED to apply native mode for {panel.port}")
    return status


##
# @brief        Helper API to compare actual value against reference value with tolerance
# @param[in]    actual_value, float/int actual value to be compared
# @param[in]    reference_value, float/int reference value to be compared against
# @param[in]    tolerance, float/int tolerance value
# @return       status, boolean True if comparing is passed, else False
def compare_with_tolerance(actual_value, reference_value, tolerance):
    return (reference_value - tolerance) <= actual_value <= (reference_value + tolerance)


##
# @brief        Helper function to get the regkey values
# @param[in]    adapter, Adapter object
# @param[in]    regkeys, List of regkeys to be verified
# @return       regkeys_with_values, Dict with regkey and value
def get_regkey_value(adapter: Adapter, regkeys: List):
    regkeys_with_values = {}
    for key in regkeys:
        current_value = registry.read(adapter.gfx_index, key)
        if current_value is None:
            logging.info(f"\t{key} does not exists. Storing it as None")
        regkeys_with_values[key] = current_value
    return regkeys_with_values


# @brief        Helper function to verify
# @param[in]    adapter, Adapter object
# @param[in]    regkeys_with_values, Dict of regkey and values to be verified
# @return       status, boolean True if expeted and actual values are same, else False
def verify_regkey_persistence(adapter: Adapter, regkeys_with_values: Dict):
    status = True
    for key, expected_value in regkeys_with_values.items():
        current_value = registry.read(adapter.gfx_index, key)
        logging.info(f"Checking value for {key}")
        if current_value is None:
            logging.error(f"\t{key} does not exist, Comparing it with None")

        elif current_value != expected_value:
            logging.error(f"\tValue mismatch. Expected= {expected_value}, Actual= {current_value}")
            status = False

        else:
            logging.info(f"Expected value: {expected_value} and actual value: {current_value} are same")

    return status
