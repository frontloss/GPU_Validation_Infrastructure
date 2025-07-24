########################################################################################################################
# @file         reboot_helper.py
# @brief        Python library containing reboot related APIs.
# @author       Rohit Kumar
########################################################################################################################

import inspect
import logging
import os
import pickle
import sys
import time
import unittest
from functools import wraps

from Libs.Core import enum, display_power
from Libs.Core.gta import gta_state_manager
from Libs.Core.logger import gdhm, etl_tracer
from Libs.Core.test_env import test_context

__REBOOT_CONTEXT_FILE = os.path.join(test_context.LOG_FOLDER, "reboot_context.pickle")
__REBOOT_SYSTEM_STATE_FILE = os.path.join(test_context.LOG_FOLDER, "reboot_system_state.pickle")


##
# @brief        RebootSystemState Class
# @details      Exposed class defining reboot system state structure
class RebootSystemState(object):
    screen_saver = None  # Boolean
    power_plan = None  # PowerScheme Enum (display_power.py)
    power_line = None  # PowerSource Enum (display_power.py)
    lid_close_event = None  # LidSwitchOption Enum (display_power.py)
    wake_timers = None  # WakeTimersStatus Enum (display_power.py)
    display_configuration = None  # DisplayConfig Structure (display_config.py)
    display_mode = None  # DisplayMode Structure (display_config.py) for each active display


##
# @brief        RebootContext Class
# @details      Internal class defining reboot context
class RebootContext(object):
    is_valid_reboot = False  # keeps track of valid/invalid reboot scenario
    caller = None  # function name who called reboot
    callee = None  # function to be called after reboot
    data = None  # user data provided in reboot call
    class_data = None  # caller class data
    errors = []  # unittest TextTestRunner result errors
    failures = []  # unittest TextTestRunner result failures


##
# @brief        setup decorator modifies the setUp function of unittest to handle reboot scenario.
# @details      Usage:
#                   \@reboot_helper.__(reboot_helper.setup)
#                   def setUp():
#                       pass
#               It ensures below functionality:
#                   - setUp() will run only once across single or multiple reboots
#                   - in case of failure, it will make sure tearDown() is executed
#               Note : must be used with reboot_helper.__() for proper functionality
#               Note : The '\@' symbol is mentioned as 'at the rate symbol' in all previous Phases of Documentation.
# @param[in]    func - decorator method name
# @return       setup_wrapper - Decorator return object
def setup(func):
    ##
    # @brief        Setup decorator wrapper method
    # @return       None
    @wraps(func)
    def setup_wrapper(self, *args, **kwargs):
        self.__reboot_context = RebootContext()

        if is_reboot_scenario() is True:
            # Restore the reboot context in case of reboot scenario
            self.__reboot_context = __get_reboot_context()

            # Make is_valid_reboot False to handle unexpected reboot case
            self.__reboot_context.is_valid_reboot = False

            # Restore unittest errors, failures and class data
            __restore_reboot_context(self)

            # Skip the setUp() in case of reboot scenario
            logging.debug("Skipping setup steps")
            return

        # Execute setUp() function in try block to handle the failure
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            self.tearDown()
            raise Exception(e)

        # EVE specific: after finishing setUp(), reboot the system and run the function having @test decorator. If no
        # such function is present, execution will continue as per unittest flow without rebooting
        for member in inspect.getmembers(self, predicate=inspect.ismethod):
            if '_decorators' in member[1].__dict__.keys():
                for decorator in member[1].__dict__['_decorators']:
                    if 'test' == decorator.__name__:
                        logging.debug("Rebooting after running setup steps")
                        reboot(self, callee=member[0])
                        break

    return setup_wrapper


##
# @brief        EVE specific: test decorator modifies the runTest or other unittest test cases to handle reboot
#               scenario.
# @details      Usage:
#                   reboot_helper.__(reboot_helper.test)
#                   def runTest():
#                       pass
#               It ensures below functionality:
#                   - in case of failure, it will make sure tearDown() is executed
#               must be used with reboot_helper.__() for proper functionality
# @param[in]    func - decorator method name
# @return       test_wrapper - Decorator return object
def test(func):
    ##
    # @brief    Test decorator wrapper method
    # @return   None
    @wraps(func)
    def test_wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)

    return test_wrapper


##
# @brief        teardown decorator modifies the unittest tearDown() function to handle reboot scenario.
# @param[in]    func - decorator method name
# @details      Usage:
#                   reboot_helper.__(reboot_helper.teardown)
#                   def tearDown():
#                       pass
#               It ensures below functionality:
#                   - cleanup reboot context after completing the test
#               Note :  must be used with reboot_helper.__() for proper functionality
# @return       teardown_wrapper - Decorator return object
def teardown(func):
    ##
    # @brief        Teardown decorator wrapper method
    # @return       None
    @wraps(func)
    def teardown_wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            logging.error(e)
        logging.debug("Removing reboot context")
        __remove_reboot_context()

    return teardown_wrapper


##
# @brief        Helper decorator, used to attach decorator names to functions.
# @details      All decorators must be called using this decorator for proper functionality.
# @param[in]    *decorators - invoked decorators list
# @return       add_decorators - Decorator return object
def __(*decorators):
    ##
    # @brief        Add decorator wrapper method
    # @return       func - Decorator return object
    def add_decorators(func):
        # Add decorator names to target function. It helps to identify which function represents test case.
        func._decorators = decorators
        for decorator in decorators[::-1]:
            func = decorator(func)
        return func

    return add_decorators


##
# @brief        Exposed API to determine valid reboot scenario
# @return       bool - True if valid reboot scenario is identified, False otherwise
def is_reboot_scenario():
    reboot_context = __get_reboot_context()
    if reboot_context is not None:
        if reboot_context.is_valid_reboot is True:
            return True

    # In case of invalid reboot context, clean the context
    __remove_reboot_context()
    return False


##
# @brief        Internal API to find the TextTestRunner frame.
# @details      TextTestRunner frame is used to add errors and failures to unittest result in case of setUp()
#               and test() failure. todo : handle the failing case
# @param[in]    f_back - current frame
# @return       f_back - TextTestRunner frame
def __find_runner_frame(f_back):
    # Check for orig_result and result properties to identify the frame instance.
    # These properties are part of TextTestRunner object.
    if ('outcome' not in f_back.f_locals.keys()) or ('result' not in f_back.f_locals.keys()):
        return __find_runner_frame(f_back.f_back)
    return f_back


##
# @brief        Internal API to store the reboot context.
# @return       True if operation is successful, False otherwise
def __store_reboot_context(self):
    # Skip list for class data. These attributes will not be saved.
    skip_list = ['reboot_context', '_testMethodName', '_resultForDoCleanups', '_cleanups', '_type_equality_funcs',
                 '_testMethodDoc']

    # clear errors and failures list
    self.__reboot_context.errors = []
    self.__reboot_context.failures = []

    # get TextTestRunner frame
    f_back = __find_runner_frame(inspect.currentframe().f_back)

    # get errors and failures from TextTestRunner result
    for error in f_back.f_locals['result'].errors:
        self.__reboot_context.errors.append((error[0].__class__.__name__, error[1]))
    for failure in f_back.f_locals['result'].failures:
        self.__reboot_context.failures.append((failure[0].__class__.__name__, failure[1]))

    # clear class data
    self.__reboot_context.class_data = {}

    # get caller class specific attributes
    attributes = set(dir(self)) - set(dir(unittest.TestCase))
    for attr in attributes:
        # Skip callable attributes
        if callable(getattr(self, attr)) or attr in skip_list:
            continue

        # Skip non serializable attributes
        try:
            pickle.dumps(getattr(self, attr))
        except Exception as e:
            logging.debug(e)
            continue

        self.__reboot_context.class_data[attr] = getattr(self, attr)

    # Pickle the reboot context in __REBOOT_CONTEXT_FILE
    try:
        with open(__REBOOT_CONTEXT_FILE, 'wb') as f:
            pickle.dump(self.__reboot_context, f)
            logging.debug("Reboot context saved successfully")
            return True
    except Exception as e:
        logging.error(e)
    return False


##
# @brief        Internal API to restore reboot context
# @return       None
def __restore_reboot_context(self):
    # get TextTestRunner frame
    f_back = __find_runner_frame(inspect.currentframe().f_back)

    # Restore unittest errors and failures
    for error in self.__reboot_context.errors:
        f_back.f_locals['result'].errors.append((self, error[1]))
    for failure in self.__reboot_context.failures:
        f_back.f_locals['result'].failures.append((self, failure[1]))

    # Restore caller class data
    for d in self.__reboot_context.class_data.keys():
        setattr(self, d, self.__reboot_context.class_data[d])


##
# @brief        Internal API to get reboot context
# @return       object - reboot_context if successful, None otherwise
def __get_reboot_context():
    if os.path.exists(__REBOOT_CONTEXT_FILE):
        try:
            with open(__REBOOT_CONTEXT_FILE, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logging.error(e)
    return None


##
# @brief        Exposed API to get reboot data stored using reboot() API
# @return       object - If successful return data, None otherwise
def _get_reboot_data():
    return None if __get_reboot_context() is None else __get_reboot_context().data


##
# @brief        Internal API to clean reboot context
# @return       None
def __remove_reboot_context():
    if os.path.exists(__REBOOT_CONTEXT_FILE):
        os.remove(__REBOOT_CONTEXT_FILE)
        gta_state_manager.update_reboot_state(False)


##
# @brief        Exposed API to reboot the system
# @details      todo: make sure callee is a valid reference of caller class function
# @param[in]    callee - target function. Execution will be switched to this function after reboot.
#               Callee must be a member of caller class.
# @param[in]    data - It can be retrieved after reboot using get_reboot_data() API.
# @return       bool - True if reboot successful, False otherwise
def reboot(self, callee, data=None):
    display_power_ = display_power.DisplayPower()

    if hasattr(self, '__reboot_context') is False:
        setattr(self, '__reboot_context', RebootContext())

    # set caller function name
    # In stack, caller function is present at index 1
    # Caller function name is at index 3 in stack entry tuple
    self.__reboot_context.caller = inspect.stack()[1][3]

    if data is not None:
        self.__reboot_context.data = data

    # check if callee is valid
    if callee is None:
        logging.error("Invalid callee")
        return False

    self.__reboot_context.callee = callee
    self.__reboot_context.is_valid_reboot = True

    if __store_reboot_context(self) is False:
        logging.error("Failed to store reboot context")
        return False

    if self is not None and self.defaultTestResult() is not None:
        logging.debug('Stopping current test')
        self.defaultTestResult().stop()

    etl_tracer.stop_etl_tracer()
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(
            test_context.LOG_FOLDER, 'GfxTraceBeforeReboot.' + str(time.time()) + '.etl')
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    etl_tracer.start_etl_tracer(etl_tracer.TraceType.TRACE_WITH_BOOT)

    result = display_power_.invoke_power_event(display_power.PowerEvent.S5, 0)
    if result is False:
        gdhm.report_bug(
            f"[RebootHelperLib] Failed to reboot the system",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
        logging.error('Failed to invoke power event S5')
        return False
    time.sleep(60)
    # Code is not supposed to reach here
    return False


##
# @brief        Exposed API to shutdown the system
# @param[in]    callee - target function. Execution will be switched to this function after reboot.
#               Callee must be a member of caller class.
# @param[in]    data - It can be retrieved after shutdown using get_reboot_data() API.
# @return       bool - True if shutdown is successful, False otherwise
def shutdown(self, callee, data=None):
    display_power_ = display_power.DisplayPower()

    if hasattr(self, '__reboot_context') is False:
        setattr(self, '__reboot_context', RebootContext())

    # set caller function name
    # In stack, caller function is present at index 1
    # Caller function name is at index 3 in stack entry tuple
    self.__reboot_context.caller = inspect.stack()[1][3]

    if data is not None:
        self.__reboot_context.data = data

    # check if callee is valid
    if callee is None:
        logging.error("Invalid callee")
        return False

    self.__reboot_context.callee = callee
    self.__reboot_context.is_valid_reboot = True

    if __store_reboot_context(self) is False:
        logging.error("Failed to store reboot context")
        return False

    if self is not None and self.defaultTestResult() is not None:
        logging.debug('Stopping current test')
        self.defaultTestResult().stop()

    etl_tracer.stop_etl_tracer()
    if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        etl_file_path = os.path.join(
            test_context.LOG_FOLDER, 'GfxTraceBeforeReboot.' + str(time.time()) + '.etl')
        os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    etl_tracer.start_etl_tracer(etl_tracer.TraceType.TRACE_WITH_BOOT)

    result = display_power_.invoke_power_event(display_power.PowerEvent.SHUTDOWN, 0)
    if result is False:
        gdhm.report_bug(
            f"[RebootHelperLib] Failed to shutdown the system",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
        logging.error('Failed to invoke Shutdown')
        return False
    time.sleep(60)
    # Code is not supposed to reach here
    return False

##
# @brief        Exposed API to get test suite.
# @param[in]    class_name - name of unittest.TestCase class
# @return       object - TestSuite object
def get_test_suite(class_name):
    self = getattr(sys.modules['__main__'], class_name)

    # get names of all tests defined in the class
    test_cases = unittest.TestLoader().getTestCaseNames(self)

    if is_reboot_scenario() is True:
        reboot_context = __get_reboot_context()

        # get callee function starting line number
        start_line_number = getattr(self, reboot_context.callee).__code__.co_firstlineno

        # check for multiple test cases
        if len(test_cases) > 1:
            loader = unittest.TestLoader()
            custom_suite = unittest.TestSuite()
            custom_suite.addTests(loader.loadTestsFromName(reboot_context.callee, self))

            tests = {name: getattr(self, name).__code__.co_firstlineno for name in test_cases}
            tests = {k: v for k, v in sorted(tests.items(), key=lambda item: item[1])}

            # In case of multiple test cases, add functions to test suite which are present after callee in the caller
            # class
            for test_case_name, line_no in tests.items():
                if test_case_name == reboot_context.callee:
                    continue
                if line_no > start_line_number:
                    custom_suite.addTests(loader.loadTestsFromName(test_case_name, self))
            return custom_suite

        # if only one test is present, return test suite with callee
        return unittest.makeSuite(self, prefix=reboot_context.callee)
    else:
        # check for multiple test cases
        if len(test_cases) > 1:
            loader = unittest.TestLoader()
            custom_suite = unittest.TestSuite()

            tests = {name: getattr(self, name).__code__.co_firstlineno for name in test_cases}
            tests = {k: v for k, v in sorted(tests.items(), key=lambda item: item[1])}

            # In case of multiple test cases, add functions to test suite which are present after callee in the caller
            # class
            for test_case_name, line_no in tests.items():
                custom_suite.addTests(loader.loadTestsFromName(test_case_name, self))
            return custom_suite

        # if only one test is present, return default test suite
        return unittest.makeSuite(self)
