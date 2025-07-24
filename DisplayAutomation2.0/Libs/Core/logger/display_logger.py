########################################################################################################################
# @file         display_logger.py
# @brief        This script is an internal interface and not qualified for API
# @author       Beeresh
########################################################################################################################

import logging
import os
import re
import sys
from configparser import ConfigParser

from Libs.Core import reboot_helper
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import dll_logger

LOG_FORMAT = '[ %(asctime)s %(filename)-40s:%(lineno)-4s - %(funcName)36s() : %(levelname)-9s] %(message)s'
DISPLAY_LOG_FORMATTER = logging.Formatter(LOG_FORMAT, "%H:%M:%S ")

file_handle = None
log_file = None


##
# @brief        Function to enable console logging
# @return       None
def __enable_console_logging():
    console_handler = logging.StreamHandler()
    logging.getLogger().addHandler(console_handler)
    console_handler.setFormatter(DISPLAY_LOG_FORMATTER)


##
# @brief        Function to add log file handler
# @param[in]    script_name - python file name
# @param[in]    log_level - level of logging
# @return       file_handler - Handle to the logger file
def __add_file_handler(script_name, log_level=logging.DEBUG):
    global log_file
    log_level_list = [logging.CRITICAL, logging.FATAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]

    log_file, file_extension = os.path.splitext(script_name)
    log_file = "%s.log" % log_file
    log_file = os.path.join(test_context.LOG_FOLDER, log_file)

    root_logger = logging.getLogger()
    if log_level not in log_level_list:
        log_level = logging.DEBUG

    root_logger.setLevel(log_level)

    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            if log_file in handler.baseFilename:
                return handler

    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(DISPLAY_LOG_FORMATTER)
    root_logger.addHandler(file_handler)
    return file_handler


##
# @brief        Preparatory setup for logging
# @param[in]    console_logging - Enable logging statements on console if True else disable logging
#               1. Removes stale .dat and .dmp files
#               2. Create Logs folder if not exists
#               3. Remove stale log files within existing Logs folder
#               4. Print preamble with test environment details
# @return       None
def _initialize(console_logging=False):
    global file_handle

    path, script_name = os.path.split(sys.argv[0])
    opt_pattern = re.compile('^-([A-Za-z]+[0-9]*)(_*([A-Za-z])*([0-9])*)(_*([A-Za-z])*)?$')

    # Convert arguments to uppercase.
    for index, argument in enumerate(sys.argv):
        if opt_pattern.match(argument) is not None:
            sys.argv[index] = argument.upper()

    log_level = logging.INFO
    if '-LOGLEVEL' in sys.argv:
        level = sys.argv[sys.argv.index('-LOGLEVEL') + 1].upper()
        log_level = eval(f"logging.{level}")
    else:
        _configParser = ConfigParser()
        if os.path.exists(os.path.join(test_context.TEST_TEMP_FOLDER, "config.ini")):
            _configParser.read(os.path.join(test_context.TEST_TEMP_FOLDER, "config.ini"))
            if _configParser.has_option('GENERAL', 'collect_logs'):
                log_level = logging.DEBUG if _configParser.get('GENERAL',
                                                               'collect_logs').upper() == 'TRUE' else logging.INFO

    root_folder_path = test_context.ROOT_FOLDER

    file_list = [f for f in os.listdir(root_folder_path) if os.path.isfile(os.path.join(root_folder_path, f))]
    for file in file_list:
        if ".dat" in file:
            os.remove(os.path.join(root_folder_path, file))
        if ".dmp" in file:
            os.remove(os.path.join(root_folder_path, file))

    log_folder_path = test_context.LOG_FOLDER

    ##
    # Create Logs folder, if it is not present
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    elif reboot_helper.is_reboot_scenario() is False:
        ##
        # If Logs folder present, remove the folder and create new (only if reboot scenario is false)
        file_list = [f for f in os.listdir(log_folder_path) if os.path.isfile(os.path.join(log_folder_path, f))]
        for old_log_file in file_list:
            os.remove(os.path.join(log_folder_path, old_log_file))

    file_handle = __add_file_handler(script_name, log_level)
    if console_logging:
        __enable_console_logging()

    debug_log = True if log_level == logging.DEBUG else False
    dll_logger.initialize(debug_log)
    test_context.DiagnosticDetails().save_etl = debug_log


##
# @brief        Cleanup method to perform cleanup of logger modules
# @return       None
def _cleanup():
    dll_logger.cleanup()
    logging.getLogger().removeHandler(file_handle)


##
# @brief        Get file handle helper method
# @return       (file_handle, log_file) - (log file handle, log file path)
def _get_file_handle():
    return file_handle, log_file
