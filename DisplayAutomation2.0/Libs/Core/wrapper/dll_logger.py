######################################################################################
# @file         dll_logger.py
# @brief        Python wrapper module to implement exposed DLL Logger APIs
# @author       Amit Sau
######################################################################################
import ctypes
import os
from Libs.Core.test_env import test_context

_logger_dll = None
__path = os.path.join(test_context.LOG_FOLDER, "dll_logger.txt")  # Specifies which file to write DLL logs
__config_log_path = os.path.join(test_context.LOG_FOLDER,
                                 "display_config_log.txt")  # Specifies which file to write DLL logs


##
# @brief        DLL Logger Load Library function which loads the Logger.dll
# @return       None
def load_library() -> None:
    global _logger_dll
    # Load Logger C library
    _logger_dll = ctypes.cdll.LoadLibrary(os.path.join(test_context.BIN_FOLDER, 'Logger.dll'))


##
# @brief        Initialize DLL Logger function which calls the exposed Initialize API
# @param[in]    debug_log - enable DLL debug logs if True, False if disable
# @return       None
def initialize(debug_log: bool = False) -> None:
    prototype = ctypes.PYFUNCTYPE(None, ctypes.c_char_p, ctypes.c_bool)
    func = prototype(('Initialize', _logger_dll))
    func(__path.encode(), debug_log)
    if debug_log:
        __init_display_config_logger()


##
# @brief        Initialize Display Config Logger function which calls the exposed InitDisplayConfigLogger API
# @return       None
def __init_display_config_logger() -> None:
    prototype = ctypes.PYFUNCTYPE(None, ctypes.c_char_p)
    func = prototype(('InitDisplayConfigLogger', _logger_dll))
    func(__config_log_path.encode())


##
# @brief        Initialize DLL Logger function which calls the exposed Cleanup API
# @return       None
def cleanup() -> None:
    prototype = ctypes.PYFUNCTYPE(None)
    func = prototype(('Cleanup', _logger_dll))
    func()
