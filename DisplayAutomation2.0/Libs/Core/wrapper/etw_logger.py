######################################################################################
# @file         etw_logger.py
# @brief        Python wrapper module to implement exposed DLL Etw Test APIs
# @author       Kasthuri R , Abhishek Ravoor
######################################################################################
import ctypes
from enum import Enum
from Libs.Core.wrapper import dll_logger


##
# @brief        WindowsOperation Enum
class WindowsOperation(Enum):
    NONE = 0
    PLAY = 1
    PAUSE = 2
    STOP = 3
    APPLICATION_OPEN = 4
    APPLICATION_CLOSE = 5
    APPLICATION_RESIZE = 6
    MOVE_WINDOW = 7
    SWITCH_WINDOW = 8
    WINDOWS_MAXIMIZE = 9
    WINDOWS_MINIMIZE = 10


##
# @brief        Feature Enum
class Feature(Enum):
    DISPLAY = 0
    AUDIO = 1
    VALSIM = 2
    LEGACY = 3


##
# @brief        Interface to add ETW logging for media operation
# @param[in]    target - Target ID
# @param[in]    action - Windows operation
# @return       None
def window_operation(target, action: WindowsOperation) -> None:
    prototype = ctypes.PYFUNCTYPE(None, ctypes.c_uint, ctypes.c_uint)
    func = prototype(('EtwMediaOperation', dll_logger._logger_dll))
    func(target, action.value)


##
# @brief        Interface to add ETW logging for read registry operation
# @param[in]    feature - Feature Type for which Registry Access was invoked
# @param[in]    reg_path - Registry Path
# @param[in]    sub_key - Optional Sub Key Path
# @param[in]    reg_name - Registry name
# @param[in]    reg_type - Type of Registry
# @param[in]    reg_data - Data stored in Registry
# @return       None
def read_registry(feature: Feature, reg_path: str, sub_key: str, reg_name: str, reg_type: int, reg_data: any) -> None:
    dll_logger.load_library()  # TODO: Clean up display_config_switching.py test and remove this line (VSDI-28914)
    prototype = ctypes.PYFUNCTYPE(None, ctypes.c_uint, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
                                  ctypes.c_uint, ctypes.c_wchar_p)
    func = prototype(('EtwReadRegistry', dll_logger._logger_dll))
    func(feature.value, reg_path, sub_key, reg_name, reg_type, str(reg_data))


##
# @brief        Interface to add ETW logging for write registry operation
# @param[in]    feature - Feature Type for which Registry Access was invoked
# @param[in]    reg_path - Registry Path
# @param[in]    sub_key - Optional Sub Key Path
# @param[in]    reg_name - Registry name
# @param[in]    reg_type - Type of Registry
# @param[in]    reg_value - Value of Registry
# @return       None
def write_registry(feature: Feature, reg_path: str, sub_key: str, reg_name: str, reg_type: int, reg_value: any) -> None:
    dll_logger.load_library()  # TODO: Clean up display_config_switching.py test and remove this line (VSDI-28914)
    prototype = ctypes.PYFUNCTYPE(None, ctypes.c_uint, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
                                  ctypes.c_uint, ctypes.c_wchar_p)
    func = prototype(('EtwWriteRegistry', dll_logger._logger_dll))
    func(feature.value, reg_path, sub_key, reg_name, reg_type, str(reg_value))
