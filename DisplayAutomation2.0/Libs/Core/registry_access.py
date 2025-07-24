########################################################################################################################
# @file         registry_access.py
# @brief        Python wrapper exposes registry access API's related to OsInterfaces DLL
# @details      Usage:
#               1. Utilize read(), write() and delete() registry APIs accessing regkeys.
#               2. DISS path:     ss_reg_args = StateSeparationRegArgs(gfx_index)
#               3. Legacy path:   legacy_reg_args = LegacyRegArgs(HKey.LOCAL_MACHINE, r"SOFTWARE\Intel\Display")
#               Steps:
#               1. Create a registry handle either through StateSeparationRegArgs or LegacyRegArgs
#               2. sub_key parameters in the APIs has to be used in case if the key is not available.
#               Example:
#               1. write(legacy_reg_args, "BKPDisplayLACE", RegDataType.DWORD, 1, sub_key=r"igfxcui\MISC")
#               2. read(legacy_reg_args, "BKPDisplayLACE", sub_key=r"igfxcui\MISC")
#               Here, "igfxcui\MISC" path might not be available always and can be passed as a subkey parameter to
#               create it before writing the registry value. Similar implementation can be followed for DISS path.
#               Note: Other APIs will be deprecated and removed.
# @author       Kiran Kumar Lakshmanan,
########################################################################################################################
import logging
import winreg
from enum import Enum
from typing import Union

import win32api

from Libs.Core.display_config.adapter_info_struct import GUID
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import os_interfaces as os_interfaces_dll, etw_logger

# Max buffer size for registry name to be read
MAX_BUFFER_SIZE = 256

# Do not modify. Only used for reserved arguments using winreg APIs
__RESERVED = 0

# Check if requested registry key is not available in current handle
__KEY_NOT_FOUND = 2

# Note: Do not update the below GUID list objects.
# GUID - Display Device Class
GUID_DEVCLASS_DISPLAY = [0x4d36e968, 0xe325, 0x11ce, [0xbf, 0xc1, 0x08, 0x00, 0x2b, 0xe1, 0x03, 0x18]]
# GUID - System Device Class
GUID_DEVCLASS_SYSTEM = [0x4d36e97d, 0xe325, 0x11ce, [0xbf, 0xc1, 0x08, 0x00, 0x2b, 0xe1, 0x03, 0x18]]


##
# @brief        ConfigManagerFilterType Enum (DISS path)
class ConfigManagerFilterType(Enum):
    NONE = 0x00000000
    SERVICE = 0x00000002
    CLASS = 0x00000200


##
# @brief        ConfigManagerRegKeyType Enum (DISS path)
class ConfigManagerRegKeyType(Enum):
    HARDWARE = 0x00000000
    SOFTWARE = 0x00000001


##
# @brief        HKey Enum (Legacy path)
class HKey(Enum):
    CURRENT_USER = winreg.HKEY_CURRENT_USER
    LOCAL_MACHINE = winreg.HKEY_LOCAL_MACHINE
    CLASSES_ROOT = winreg.HKEY_CLASSES_ROOT
    USERS = winreg.HKEY_USERS
    PERFORMANCE_DATA = winreg.HKEY_PERFORMANCE_DATA
    CURRENT_CONFIG = winreg.HKEY_CURRENT_CONFIG


##
# @brief        RegDataType Enum (Legacy path)
class RegDataType(Enum):
    NONE = winreg.REG_NONE
    SZ = winreg.REG_SZ
    EXPAND_SZ = winreg.REG_EXPAND_SZ
    BINARY = winreg.REG_BINARY
    DWORD = winreg.REG_DWORD
    MULTI_SZ = winreg.REG_MULTI_SZ
    QWORD = winreg.REG_QWORD


##
# @brief        Feature Enum
class Feature(Enum):
    DISPLAY = 0
    AUDIO = 1
    VALSIM = 2


##
# @brief        StateSeparationRegArgs class (DISS path)
# @details      Pass mandatory gfx_index parameter while instantiating class object.
class StateSeparationRegArgs:

    ##
    # @brief        Initializes the data members of StateSeparationRegArgs
    # @param[in]    gfx_index - Graphics Adapter Index.
    # @param[in]    guid - GUID value to be converted for fetching handle
    # @param[in]    filter_type -  Device list filter type (Class/System devices)
    # @param[in]    key_type - Registry Key type (Software/Hardware key)
    # @param[in]    feature - Enum value of requested Feature
    def __init__(self, gfx_index: Union[str, None], guid: list = GUID_DEVCLASS_DISPLAY,
                 filter_type: ConfigManagerFilterType = ConfigManagerFilterType.CLASS,
                 key_type: ConfigManagerRegKeyType = ConfigManagerRegKeyType.SOFTWARE, feature=Feature.DISPLAY):
        self.gfx_index = gfx_index.lower() if gfx_index is not None else gfx_index
        self.guid = self.__convert_to_guid(guid)
        self.filter_type = filter_type
        self.key_type = key_type
        self.feature = feature

    ##
    # @brief        Converts List data into GUID
    # @param[in]    guid - GUID value to be converted for fetching handle
    # @return       guid_data - data list converted to GUID type object
    def __convert_to_guid(self, data: list) -> GUID:
        guid_data = GUID()
        if self.__validate_guid_list(data) is True:
            guid_data.Data1 = data[0]
            guid_data.Data2 = data[1]
            guid_data.Data3 = data[2]
            for i in range(len(data[3])):
                guid_data.Data4[i] = data[3][i]
        else:
            logging.error(f"Unable to convert data list ({data}) to GUID")
        return guid_data

    ##
    # @brief        Validates List data passed
    # @param[in]    guid - GUID value to be converted for fetching handle
    # @return       status - True if valid GUID list, else False.
    def __validate_guid_list(self, data: list) -> bool:
        return True if type(data) is list and len(data) == 4 and len(data[3]) == 8 else False

    ##
    # @brief    Overridden str method
    # @return   str - String representation of StateSeparationRegArgs class
    def __str__(self):
        return f" Adapter: {self.gfx_index}, Filter type: {self.filter_type}, Key type: {self.key_type}"


##
# @brief        LegacyRegArgs class (Legacy path)
# @details      Pass mandatory hkey and reg_path parameters while instantiating class object.
class LegacyRegArgs:

    ##
    # @brief        Initializes the data members of LegacyRegArgs
    # @param[in]    hkey - HKey enum object
    # @param[in]    reg_path - Trailing registry path after hkey parameter
    def __init__(self, hkey: HKey, reg_path: str):
        self.hkey = hkey
        self.reg_path = reg_path

    ##
    # @brief    Overridden str method
    # @return   str - String representation of LegacyRegArgs class
    def __str__(self):
        return f" HKey: {self.hkey}, Registry path: {self.reg_path}"


##
# @brief        Read Registry Value method
# @param[in]    args - Object of type StateSeparationRegArgs or LegacyRegArgs class
# @param[in]    reg_name - Registry name to read
# @param[in]    sub_key - Optional subkey path to read from base handle location
#               Use this parameter when the required path to be accessed might not be available.
# @return       (value_data, reg_type) - (data of returned registry, type of registry)
def read(args: Union[StateSeparationRegArgs, LegacyRegArgs], reg_name: str, sub_key: str = None) -> (any, int):
    value_data, reg_type = None, None
    # Get Base handle
    status, handle = __get_reghandle(args)
    if status is False:
        return value_data, reg_type
    try:
        if not sub_key:
            value_data, reg_type = winreg.QueryValueEx(handle, reg_name)
            if type(args) is LegacyRegArgs:
                etw_logger.read_registry(etw_logger.Feature.LEGACY, args.reg_path, "NA", reg_name, reg_type,
                                         reg_data=value_data)
            else:
                etw_logger.read_registry(args.feature, "NA", "NA", reg_name, reg_type, reg_data=value_data)
        else:
            sub_key_handle = winreg.OpenKey(handle, sub_key, __RESERVED, winreg.KEY_READ)
            value_data, reg_type = winreg.QueryValueEx(sub_key_handle, reg_name)
            if type(args) is LegacyRegArgs:
                etw_logger.read_registry(etw_logger.Feature.LEGACY, args.reg_path, sub_key, reg_name, reg_type,
                                         reg_data=value_data)
            else:
                etw_logger.read_registry(args.feature, "NA", sub_key, reg_name, reg_type, reg_data=value_data)
            # Closing only subkey handle
            winreg.CloseKey(sub_key_handle)
        # if value_data is not None and reg_type is not None and RegDataType(reg_type) == RegDataType.BINARY:
        #     # Logging the size of binary data fetched from registry. Since it might overload the logs
        #     logging.debug(f"Reg_name: {reg_name}, Reg_type: {reg_type}, Reg_Data size: {len(list(value_data))}")
        # else:
        #     logging.debug(f"Reg_name: {reg_name}, Reg_type: {reg_type}, Reg_Data: {value_data}")
    except (WindowsError, FileNotFoundError) as e:
        logging.debug(f"Unexpected error while reading registry value {reg_name} : {e}")
    # Closing Base handle
    __close_reghandle(args, handle)
    return value_data, reg_type


##
# @brief        Write Registry Value method
# @param[in]    args - Object of type StateSeparationRegArgs or LegacyRegArgs class
# @param[in]    reg_name - Registry name to write
# @param[in]    reg_type - Registry data type for the value to be written
# @param[in]    reg_value - Value to be written to registry
# @param[in]    sub_key - Optional subkey path to write from base handle location
#               Use this parameter when the required path to be accessed might not be available.
# @return       status - True if Write registry value is successful, False otherwise
def write(args: Union[StateSeparationRegArgs, LegacyRegArgs], reg_name: str, reg_type: RegDataType, reg_value: any,
          sub_key: str = None) -> bool:
    status = False
    # Get Base handle
    status, handle = __get_reghandle(args)
    if status is False:
        return status
    try:
        if not sub_key:
            winreg.SetValueEx(handle, reg_name, __RESERVED, reg_type.value, reg_value)
            if type(args) is LegacyRegArgs:
                etw_logger.write_registry(etw_logger.Feature.LEGACY, args.reg_path, "NA", reg_name, reg_type.value,
                                          reg_value)
            else:
                etw_logger.write_registry(args.feature, "NA", "NA", reg_name, reg_type.value, reg_value)
            winreg.FlushKey(handle)
        else:
            sub_key_handle = 0
            try:
                sub_key_handle = winreg.OpenKey(handle, sub_key, __RESERVED, winreg.KEY_WRITE)
            except WindowsError as win_err:
                if win_err.errno == __KEY_NOT_FOUND:
                    sub_key_handle = winreg.CreateKey(handle, sub_key)
                else:
                    logging.error(f"Unexpected error while Opening subkey handle for sub_key {sub_key} : {win_err}")
                    return status
            winreg.SetValueEx(sub_key_handle, reg_name, __RESERVED, reg_type.value, reg_value)
            winreg.FlushKey(sub_key_handle)
            if type(args) is LegacyRegArgs:
                etw_logger.write_registry(etw_logger.Feature.LEGACY, args.reg_path, "NA", reg_name, reg_type.value,
                                          reg_value)
            else:
                etw_logger.write_registry(args.feature, "NA", "NA", reg_name, reg_type.value, reg_value)
            # Closing only subkey handle
            winreg.CloseKey(sub_key_handle)
        status = True
    except (WindowsError, FileNotFoundError) as e:
        logging.error(f"Unexpected error while writing registry value {reg_name} : {e}")
        return status
    # Closing Base handle
    __close_reghandle(args, handle)
    return status


##
# @brief        Delete Registry Value method
# @param[in]    args - Object of type StateSeparationRegArgs or LegacyRegArgs class
# @param[in]    reg_name - Registry name to delete
# @param[in]    sub_key - Optional subkey path to delete from base handle location
#               Use this parameter when the required path to be accessed might not be available.
# @return       status - True if registry value is deleted, False otherwise
def delete(args: Union[StateSeparationRegArgs, LegacyRegArgs], reg_name: str, sub_key: str = None) -> bool:
    status = False
    # Get Base handle
    status, handle = __get_reghandle(args)
    if status is False:
        return status
    try:
        if not sub_key:
            winreg.DeleteValue(handle, reg_name)
        else:
            sub_key_handle = 0
            try:
                sub_key_handle = winreg.OpenKey(handle, sub_key, __RESERVED, winreg.KEY_SET_VALUE)
            except WindowsError as win_err:
                if win_err.errno == __KEY_NOT_FOUND:
                    logging.warning(f"Registry {reg_name} does not exist in given sub_key path {sub_key}  -> {win_err}")
                    # Since registry is not available to be deleted
                    return True
            winreg.DeleteValue(sub_key_handle, reg_name)
            # Closing only subkey handle
            winreg.CloseKey(sub_key_handle)
        status = True
    except (WindowsError, FileNotFoundError) as e:
        logging.error(f"Unexpected error while deleting registry value {reg_name} : {e}")
    # Closing Base handle
    __close_reghandle(args, handle)
    return status


##
# @brief        Helper function to fetch appropriate Registry handle based on input object type
# @param[in]    args - Object of type StateSeparationRegArgs or LegacyRegArgs class
# @return       (status, handle) - (Fetch registry handle status, Registry handle)
def __get_reghandle(args: Union[StateSeparationRegArgs, LegacyRegArgs]) -> (bool, int):
    status, handle = False, 0
    if type(args) is StateSeparationRegArgs:
        if args.feature == Feature.DISPLAY:
            # Get Adapter Info based on gfx_index
            adapter_info = test_context.TestContext.get_gfx_adapter_details()[args.gfx_index]
            status, handle = os_interfaces_dll.get_regkey_handle(adapter_info.deviceID, adapter_info.deviceInstanceID,
                                                                 args.guid, args.filter_type.value, args.key_type.value)

        elif args.feature == Feature.VALSIM:
            # Get Sim Driver interface handle
            status, handle = os_interfaces_dll.get_simdrv_regkey_handle()

        elif args.feature == Feature.AUDIO:
            # Get Adapter Info for audio controller based on gfx_index
            audio_info = machine_info.SystemInfo().get_audio_adapter_info().get_controller_details(args.gfx_index)
            if audio_info is not None:
                status, handle = os_interfaces_dll.get_regkey_handle(audio_info.controller_deviceID,
                                                                     audio_info.controller_deviceInstanceID,
                                                                     args.guid, args.filter_type.value,
                                                                     args.key_type.value)

        else:
            logging.error(f"Invalid Feature passed")
            gdhm.report_bug(
                title=f"[DisplayConfigLib] Invalid Feature passed to get regkey handle",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
    elif type(args) is LegacyRegArgs:
        try:
            handle = winreg.ConnectRegistry(None, args.hkey.value)
            if not handle:
                logging.error(f"Failed to establish connection to pre-defined registry handle for {args.hkey.value}")
            handle = winreg.OpenKey(handle, args.reg_path, __RESERVED, winreg.KEY_ALL_ACCESS)
            status = True
        except (WindowsError, FileNotFoundError) as e:
            pass

    else:
        logging.error(f"Invalid object passed to fetch registry handle - {args}")
    return status, handle


##
# @brief        Helper function to close Registry handle based on input object type
# @param[in]    args - Object of type StateSeparationRegArgs or LegacyRegArgs class
# @param[in]    handle - Registry key handle
# @return       None
def __close_reghandle(args: Union[StateSeparationRegArgs, LegacyRegArgs], handle: int) -> None:
    if type(args) is StateSeparationRegArgs:
        # Win32API::Registry - Low-level access to Win32 system API calls from WINREG.H
        win32api.RegCloseKey(handle)
    elif type(args) is LegacyRegArgs:
        winreg.CloseKey(handle)
    else:
        logging.error(f"Invalid object passed. Failed to close the Handle - {handle}")
