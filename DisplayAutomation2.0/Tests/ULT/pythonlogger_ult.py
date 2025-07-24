#####################################################################################################################################
# \file
# \ref pythonlogger_ult.py
# \verbatim
# Sample code to verify the Python logger for DLL
# \endverbatim
# \author       Beeresh, Bharath
####################################################################################################################################
import unittest
import logging
import sys
from Libs.Core.test_env.test_environment import *
from Libs.Core.logger import display_logger
from Libs.Core.test_env import test_context
from Libs.Core.gta import gta_state_manager
from Libs.Core import test_header


def verify_string(input_string):
    found = False
    log_level = logging.getLogger().getEffectiveLevel()

    str_level = logging.getLevelName(log_level)

    [h_weak_ref().flush() for h_weak_ref in logging._handlerList]

    log_file = os.path.join(test_context.LOG_FOLDER, "pythonlogger_ult.log")
    with open(log_file,'r') as f:
        for line in f:
            if input_string in line:
                if str_level in line:
                    found = True

    if found:
        logging.log(log_level, "PASSED")
    else:
        logging.error("FAILED")

    return found


def logging_sanity(log_level):
    dll_name = "my_test.dll"
    function_name = "my_test_function"
    line_no = 1
    msg = "my test log message"

    try:
        pDLLName = ctypes.c_char_p(dll_name)
        pFunctionName = ctypes.c_char_p(function_name)
        pMsg = ctypes.c_char_p(msg)
        loggerDll = ctypes.cdll.LoadLibrary(os.path.join(test_context.BIN_FOLDER, 'CommonLogger.dll'))
        prototype = ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint,
                                      ctypes.c_char_p)
        func = prototype(('CommonLogger', loggerDll))
        func(pDLLName, log_level, pFunctionName, line_no, pMsg)


        return verify_string("my_test.dll:my_test_function:1 - my test log message")
    except Exception as e:
        logging.error("Exception %s" % e)

def perform_ult(test_handler, log_level):
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    logging_sanity(log_level)


class PythonLoggerULT(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger_obj = display_logger.DisplayLogger()
        logger_obj.set_dll_logger()


    def test_1_DEBUG(self):
        logging.debug("********** DEBUG **********")
        perform_ult(self, log_level=logging.DEBUG)

    def test_2_INFO(self):
        logging.info("********** INFO **********")
        perform_ult(self, log_level=logging.INFO)

    def test_3_WARN(self):
        logging.warning("********** WARNING **********")
        perform_ult(self, log_level=logging.WARN)

    def test_4_ERROR(self):
        logging.error("********** ERROR **********")
        perform_ult(self, log_level=logging.ERROR)

    @classmethod
    def tearDownClass(cls):
        logger_obj = display_logger.DisplayLogger()
        logger_obj.unset_dll_logger()


if __name__ == "__main__":
    TestEnvironment.load_dll_module()
    display_logger._initialize(console_logging=True)
    gta_state_manager.create_gta_default_state()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    status = test_header.cleanup(outcome.result)
    gta_state_manager.update_test_result(outcome.result, status)
    display_logger._cleanup()
