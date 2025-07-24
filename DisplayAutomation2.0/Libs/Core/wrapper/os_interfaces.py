########################################################################################################################
# @file         os_interfaces.py
# @brief        Python library containing OsInterfaces DLL related APIs.
# @author       Amit Sau, Raghupathy
########################################################################################################################
import ctypes
import logging
import os
from typing import List, Union

from Libs.Core.display_config import display_config_struct as cfg_struct
from Libs.Core.display_config.adapter_info_struct import GfxAdapterDetails, GUID, BdfInfo, MAX_GFX_ADAPTER
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.display_config.display_config_enums import QdcFlag
from Libs.Core.test_env.test_context import BIN_FOLDER

os_interface_dll = None
user32_dll = None


##
# @brief        Os Interfaces Load Library.
# @return       None
def load_library():
    global os_interface_dll
    global user32_dll
    ##
    # Load DisplayConfig C library
    os_interface_dll = ctypes.cdll.LoadLibrary(os.path.join(BIN_FOLDER, 'OsInterfaces.dll'))
    user32_dll = ctypes.windll.LoadLibrary("user32.dll")


##
# @brief        Get API interface version.
# @return       version.value - interface version value
def get_display_config_interface_version():
    version = ctypes.c_int()
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(ctypes.c_int))
    func = prototype(('GetDisplayConfigInterfaceVersion', os_interface_dll))
    func(ctypes.byref(version))
    return version.value


##
# @brief      Get Active Display Configuration API
# @return     active_config - ActiveDisplayConfig Object
def get_active_display_configuration():
    active_config = cfg_struct.ActiveDisplayConfig()
    active_config.size = ctypes.sizeof(cfg_struct.ActiveDisplayConfig)
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.ActiveDisplayConfig))
    func = prototype(('GetActiveDisplayConfiguration', os_interface_dll))
    func(ctypes.byref(active_config))
    return active_config


##
# @brief        Get display configuration which includes both active and inactive displays
# @return       get_config - DisplayConfig Object
def get_all_display_configuration():
    get_config = cfg_struct.DisplayConfig()
    get_config.size = ctypes.sizeof(cfg_struct.DisplayConfig)
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayConfig))
    func = prototype(('GetDisplayConfiguration', os_interface_dll))
    func(ctypes.byref(get_config))
    return get_config


##
# @brief        Set display configuration (SINGLE, CLONE, EXTENDED)
# @param[in]    config - DisplayConfig Object
# @param[in]    add_force_mode_enum_flag - set to True if flag is required while doing SDC call else False
# @return       config.status - DisplayConfig Error Code
def set_display_configuration(config, add_force_mode_enum_flag: bool = False):
    config.size = ctypes.sizeof(cfg_struct.DisplayConfig)
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayConfig), ctypes.c_bool)
    func = prototype(('SetDisplayConfiguration', os_interface_dll))
    func(ctypes.byref(config), add_force_mode_enum_flag)
    return config.status


##
# @brief        Get all supported modes for specified target ids which are active
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    rotation_flag - specify whether Rotation Modes to be added or not.
# @return       enumerated_modes - EnumeratedDisplayModes object
def get_all_supported_modes(display_and_adapter_info, rotation_flag):
    enumerated_modes = cfg_struct.EnumeratedDisplayModes()
    enumerated_modes.size = ctypes.sizeof(cfg_struct.EnumeratedDisplayModes)
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayAndAdapterInfo), ctypes.c_bool,
                                  ctypes.POINTER(cfg_struct.EnumeratedDisplayModes))
    get_all_mode_func = prototype(('GetAllSupportedModes', os_interface_dll))
    get_all_mode_func(ctypes.byref(display_and_adapter_info), rotation_flag, ctypes.byref(enumerated_modes))
    return enumerated_modes


##
# @brief        Get current display mode for specified displayAndAdapterInfo Type of DisplayAndAdapterInfo
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @return       mode - DisplayMode object
def get_current_mode(display_and_adapter_info):
    mode = cfg_struct.DisplayMode()
    mode.DisplayAdapterId = display_and_adapter_info
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayAndAdapterInfo),
                                  ctypes.POINTER(cfg_struct.DisplayMode))
    func = prototype(('GetCurrentMode', os_interface_dll))
    func(ctypes.byref(display_and_adapter_info), ctypes.byref(mode))
    return mode


##
# @brief        Retrieves Native Mode for specified displayAndAdapterInfo Type of DisplayAndAdapterInfo.
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @return       native_mode - Native Mode of type DisplayTimings
def get_native_mode(display_and_adapter_info):
    native_mode = cfg_struct.DisplayTimings()
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayAndAdapterInfo),
                                  ctypes.POINTER(cfg_struct.DisplayTimings))
    func = prototype(('GetOSPrefferedMode', os_interface_dll))
    func(ctypes.byref(display_and_adapter_info), ctypes.byref(native_mode))
    return native_mode


##
# @brief        Set display mode for specified displayAndAdapterInfo
# @param[in]    mode - specify display mode of type DisplayMode
# @param[in]    virtual_mode_set_aware - flag (Set this flag as True to enable PLANE scalar else PIPE scalar)
# @param[in]    force_modeset - set to True if no optimization is required while setting display mode else False
# @return       mode.status - DisplayConfig Error Code
def set_display_mode(mode, virtual_mode_set_aware = True, force_modeset = False):
    sdc_delay_in_mills = 10000
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayMode), ctypes.c_bool, ctypes.c_int, ctypes.c_bool)
    func = prototype(('SetDisplayMode', os_interface_dll))
    func(ctypes.byref(mode), virtual_mode_set_aware, sdc_delay_in_mills, force_modeset)
    return mode.status


##
# @brief        Set display mode for given IGCL display mode
# @param[in]    display_mode - specify display mode of type DisplayMode
# @param[in]    display_timing - specify display Timings from IGCL API of type DisplayTimings
# @param[in]    virtual_mode_set_aware - flag (Set this flag as True to enable PLANE scalar else PIPE scalar)
# @param[in]    force_modeset - set to True if no optimization is required while setting display mode else False
# @return       mode.status - DisplayConfig Error Code
def set_igcl_mode(display_mode, display_timing, virtual_mode_set_aware=True, force_modeset=False):
    sdc_delay_in_mills = 10000
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayMode), ctypes.c_bool, ctypes.c_int,
                                  ctypes.c_bool, ctypes.POINTER(cfg_struct.DisplayTimings))
    func = prototype(('SetIgclMode', os_interface_dll))
    func(ctypes.byref(display_mode), virtual_mode_set_aware, sdc_delay_in_mills, force_modeset, display_timing)
    return display_mode.status


##
# @brief        This class method helps to get QDC data from OS.
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    qdc_flag - QDC paths to be queried
# @return       get_config - QueryDisplay Object
def query_display_config(display_and_adapter_info, qdc_flag):
    get_config = cfg_struct.QueryDisplay()
    prototype = ctypes.PYFUNCTYPE(None, ctypes.c_int, ctypes.POINTER(cfg_struct.DisplayAndAdapterInfo),
                                  ctypes.POINTER(cfg_struct.QueryDisplay))
    func = prototype(('QueryDisplayConfigEx', os_interface_dll))
    func(qdc_flag, ctypes.byref(display_and_adapter_info), ctypes.byref(get_config))
    return get_config


##
# @brief        This class method helps to get QDC data from OS.
# @param[in]    qdc_flag - QDC paths to be queried (combination of QdcFlag as per MSDN)
# @return       (bool, path_info_arr, mode_info_arr, topology_id) - Returns
#                   status: True if OS API call is successful, False otherwise,
#                   path_info_arr: list of paths retrieved from OS, as per the qdc flag passed,
#                   mode_info_arr: list of modes retrieved from OS, as per the qdc flag passed,
#                   topology_id: Current topology as integer, can be derived from DisplayConfigTopologyId enum
def query_display_configuration_os(qdc_flag: QdcFlag) -> (bool, Union[None, List[cfg_struct.DisplayConfigPathInfo]],
                                                          Union[None, List[cfg_struct.DisplayConfigModeInfo]], int):
    num_path_info_array_elements, num_mode_info_array_elements = ctypes.c_uint(0), ctypes.c_uint(0)
    path_info_arr, mode_info_arr = None, None
    topology_id = ctypes.c_uint(0)

    # Ref: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-querydisplayconfig
    # If the QDC_DATABASE_CURRENT flag is set in the qdc_flag parameter, QueryDisplayConfig returns the topology
    # identifier of the active database topology in the variable that the pCurrentTopologyId parameter points to.
    # If the QDC_ALL_PATHS or QDC_ONLY_ACTIVE_PATHS flag is set in the qdc_flag parameter, the pCurrentTopologyId
    # parameter must be set to NULL; otherwise, QueryDisplayConfig returns ERROR_INVALID_PARAMETER.
    if (qdc_flag & QdcFlag.QDC_ONLY_ACTIVE_PATHS == QdcFlag.QDC_ONLY_ACTIVE_PATHS) or (
            qdc_flag & QdcFlag.QDC_ALL_PATHS == QdcFlag.QDC_ALL_PATHS):
        topology_id_param = ctypes.c_void_p(0)
    else:
        topology_id_param = ctypes.byref(topology_id)

    # Step 1: Get Buffers Size to call QDC
    qdc_flag_val = ctypes.c_uint(qdc_flag)
    logging.debug(f"QDC flag value = {qdc_flag_val}")

    prototype1 = ctypes.PYFUNCTYPE(ctypes.c_uint, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32),
                                   ctypes.POINTER(ctypes.c_uint32))
    get_display_config_buffer_size = prototype1(('GetDisplayConfigBufferSizes', user32_dll))
    ret_status = get_display_config_buffer_size(qdc_flag_val, ctypes.byref(num_path_info_array_elements),
                                                ctypes.byref(num_mode_info_array_elements))
    logging.debug(f"GetDisplayConfigBufferSizes returned = {ret_status},"
                  f" PathInfoArray = {num_path_info_array_elements}, ModeInfoArray = {num_mode_info_array_elements}")

    if ret_status != 0:
        logging.error(f"Failed to get Display Config Buffer sizes for QDC flag - {qdc_flag}")
        return False, path_info_arr, mode_info_arr, topology_id.value

    path_info_buffer_size = cfg_struct.DisplayConfigPathInfo * num_path_info_array_elements.value
    mode_info_buffer_size = cfg_struct.DisplayConfigModeInfo * num_mode_info_array_elements.value
    path_info_arr = path_info_buffer_size()
    mode_info_arr = mode_info_buffer_size()

    # Step 2: Invoke Query Display Config
    prototype2 = ctypes.PYFUNCTYPE(ctypes.c_uint, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32),
                                   path_info_buffer_size, ctypes.POINTER(ctypes.c_uint32),
                                   mode_info_buffer_size, ctypes.c_void_p)
    query_display_config = prototype2(('QueryDisplayConfig', user32_dll))
    ret_status = query_display_config(qdc_flag_val, ctypes.byref(num_path_info_array_elements), path_info_arr,
                                      ctypes.byref(num_mode_info_array_elements), mode_info_arr, topology_id_param)
    logging.debug(f"QueryDisplayConfig returned = {ret_status}, PathInfoArray = {path_info_arr},"
                  f" ModeInfoArray = {mode_info_arr}, TopologyId =  {topology_id_param}")

    if ret_status != 0:
        logging.error(f"Failed to get QDC data for QDC flag - {qdc_flag}")
        return False, path_info_arr, mode_info_arr, topology_id.value

    return True, path_info_arr, mode_info_arr, topology_id.value


##
# @brief        Get DisplayTimings for specified DisplayAndAdapterInfo.
# @param[in]    current_mode - Current mode for which display timings need to query.
# @return       display_timings - DisplayTimings Object
def get_display_timings(current_mode):
    display_timings = cfg_struct.DisplayTimings()
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayMode),
                                  ctypes.POINTER(cfg_struct.DisplayTimings))
    func = prototype(('GetDisplayTimings', os_interface_dll))
    func(ctypes.byref(current_mode), ctypes.byref(display_timings))
    return display_timings


##
# @brief        This class method helps to get all Gfx Display Adapter details through dll.
# @return       adapter_details - Structure of type GfxAdapterDetails
def get_all_gfx_adapter_details():
    adapter_details = GfxAdapterDetails()
    adapter_details.size = ctypes.sizeof(GfxAdapterDetails)
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(GfxAdapterDetails))
    func = prototype(('GetAllGfxAdapterDetails', os_interface_dll))
    func(ctypes.byref(adapter_details))
    return adapter_details


##
# @brief        Get currently enumerated display details
# @details      Retrieves information of connected displays, connector type, target ID, count, active status etc..,
# @return       (enum_info, enum_error) - (EnumeratedDisplaysEx Object , HRESULT Object)
def get_enumerated_display_info():
    enum_info = cfg_struct.EnumeratedDisplaysEx()
    enum_info.Size = ctypes.sizeof(cfg_struct.EnumeratedDisplaysEx)
    enum_error = ctypes.HRESULT()
    prototype = ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.POINTER(cfg_struct.EnumeratedDisplaysEx),
                                  ctypes.POINTER(ctypes.HRESULT))
    func = prototype(('GetEnumeratedDisplayInfo', os_interface_dll))
    func(ctypes.byref(enum_info), ctypes.byref(enum_error))
    return enum_info, enum_error


##
# @brief        Enables HDR for the all the HDR supported panels via OS API
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    enable - True to enable HDR, False to disable
# @return       result - hdr disable or enable error status code
def configure_hdr(display_and_adapter_info, enable):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_long, ctypes.POINTER(cfg_struct.DisplayAndAdapterInfo),
                                  ctypes.c_bool)
    func = prototype(('ConfigureHDR', os_interface_dll))
    result = func(ctypes.byref(display_and_adapter_info), enable)
    return result


##
# @brief        API to capture screen
# @param[in]    instance - Instance of Screen to be captured
# @param[in]    adapter_info -  Graphics Adapter Information
# @param[in]    capture_args -  ScreenCaptureArgs Object
# @return       result - True if Screen capture successful, False otherwise
def capture_screen(instance, adapter_info, capture_args):
    # type: (int, GfxAdapterInfo, cfg_struct.ScreenCaptureArgs) -> bool
    prototype = ctypes.PYFUNCTYPE(ctypes.c_ubyte, ctypes.c_uint, GfxAdapterInfo, cfg_struct.ScreenCaptureArgs)
    func = prototype(('CaptureScreen', os_interface_dll))
    result = func(instance, adapter_info, capture_args)
    return result


##
# @brief        Cleanup Function
# @details      In Get all supported modes we are allocating memory in C DLL (DisplayConfig.dll) for each target ID
#               which includes mode information. User need not to deallocate memory since DisplayConfig python script
#               takes care of memory de-allocation in C DLL.
# @return       None
def cleanup():
    cleanup_prototype = ctypes.PYFUNCTYPE(None)
    cleanup_func = cleanup_prototype(('EDSMemoryCleanup', os_interface_dll))
    cleanup_func()


##
# @brief         Get Registry Key Handle from DLL
# @param[in]     device_id -  DeviceID for which registry should be read
# @param[in]     device_instance_id -  deviceInstanceID for which registry should be read
# @param[in]     guid - GUID object
# @param[in]     filter_type -  Enum Value of ConfigManagerFilterType
# @param[in]     key_type -  Enum Value of ConfigManagerRegKeyType
# @return        (status, handle) - (Get handle status, RegKey Handle for the given gfx adapter)
def get_regkey_handle(device_id: str, device_instance_id: str, guid: GUID, filter_type: int, key_type: int) -> (
        bool, int):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_wchar_p, ctypes.c_wchar_p, GUID, ctypes.c_ulong,
                                  ctypes.c_uint,
                                  ctypes.c_void_p)
    # Passing empty HKey pointer, expecting the C DLL to update the required handle
    ptr = ctypes.c_void_p(0)
    func = prototype(('GetRegKeyHandle', os_interface_dll))
    status = func(device_id, device_instance_id, guid, filter_type, key_type, ctypes.byref(ptr))
    return status, ptr.value


##
# @brief        Get Val-Sim Registry Key Handle from DLL
# @return       (status, int) - (Get handle status,RegKey Handle for val-sim driver)
def get_simdrv_regkey_handle() -> (bool, int):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)
    # Passing empty HKey pointer, expecting the C DLL to update the required handle
    ptr = ctypes.c_void_p(0)
    func = prototype(('GetSimDrvRegKeyHandle', os_interface_dll))
    status = func(ctypes.byref(ptr))
    return status, ptr.value


#####################################################################################


##
# @brief        Get display configuration which includes both active and inactive displays
# @return       get_config - display config object of type DisplayConfig
def os_wrapper_get_config() -> cfg_struct.DisplayConfig():
    get_config = cfg_struct.DisplayConfig()
    get_config.size = ctypes.sizeof(cfg_struct.DisplayConfig)

    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayConfig))
    func = prototype(('GetConfig', os_interface_dll))
    func(ctypes.byref(get_config))
    return get_config


##
# @brief        Set display configuration (SINGLE, CLONE, EXTENDED)
# @param[in]    config - display config object of type DisplayConfig
# @return       config.status - DisplayConfig Status (Error Code of type DISPLAY_CONFIG_ERROR_CODE)
def os_wrapper_set_config(config):
    config.size = ctypes.sizeof(cfg_struct.DisplayConfig)
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayConfig))
    func = prototype(('SetConfig', os_interface_dll))
    func(ctypes.byref(config))
    return config.status


##
# @brief        Set display mode for specified displayAndAdapterInfo
# @param[in]    mode - specify display mode of type DisplayMode
# @param[in]    virtual_mode_set_aware - virtual Mode Set Aware flag
#               (Set this flag as True to enable PLANE scalar else PIPE scalar)
# @param[in]    force_modeset - set to True if no optimization is required while setting display mode else False
# @return       mode.status - mode Status (Error Code of type DISPLAY_CONFIG_ERROR_CODE)
def os_wrapper_set_mode(mode, virtual_mode_set_aware=True, force_modeset = False):
    sdc_delay_in_mills = 10000
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayMode), ctypes.c_bool, ctypes.c_int, ctypes.c_bool)
    func = prototype(('SetMode', os_interface_dll))
    func(ctypes.byref(mode), virtual_mode_set_aware, sdc_delay_in_mills, force_modeset)
    return mode.status


##
# @brief        Get all supported modes for specified panel which are active
# @param[in]    display_and_adapter_info - displayAndAdapterInfo Structure
# @param[in]    rotation_flag - rotation flag to specify whether Rotation Modes to be added or not.
# @return       enumerated_modes - enumerated modes of type EnumeratedDisplayModes
def os_wrapper_get_modes(display_and_adapter_info, rotation_flag):
    enumerated_modes = cfg_struct.EnumeratedDisplayModes()
    enumerated_modes.size = ctypes.sizeof(cfg_struct.EnumeratedDisplayModes)
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayAndAdapterInfo), ctypes.c_bool,
                                  ctypes.POINTER(cfg_struct.EnumeratedDisplayModes))
    get_all_mode_func = prototype(('GetModes', os_interface_dll))
    get_all_mode_func(ctypes.byref(display_and_adapter_info), rotation_flag, ctypes.byref(enumerated_modes))
    return enumerated_modes


##
# @brief        Get current display mode for specified displayAndAdapterInfo Type of DisplayAndAdapterInfo
# @param[in]    display_and_adapter_info - displayAndAdapterInfo Structure
# @return       mode - mode of type DisplayMode
def os_wrapper_get_mode(display_and_adapter_info):
    mode = cfg_struct.DisplayMode()
    mode.DisplayAdapterId = display_and_adapter_info
    prototype = ctypes.PYFUNCTYPE(None, ctypes.POINTER(cfg_struct.DisplayAndAdapterInfo),
                                  ctypes.POINTER(cfg_struct.DisplayMode))
    func = prototype(('GetMode', os_interface_dll))
    func(ctypes.byref(display_and_adapter_info), ctypes.byref(mode))
    return mode


##
# @brief        Get display adapters' BDF information for current environment
# @return       status, bdf_array, adapter_count - Returns error code, array of BdfInfo objects,
#               number of display adapters (both active and inactive)
def get_bdf_details() -> (int, list, int):
    bdf_array_buff = BdfInfo * MAX_GFX_ADAPTER
    bdf_array = bdf_array_buff()
    adapter_count = ctypes.c_uint(0)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_uint, bdf_array_buff, ctypes.POINTER(ctypes.c_uint))
    func = prototype(('GetBDFDetails', os_interface_dll))
    status = func(bdf_array, ctypes.byref(adapter_count))
    return status, bdf_array, adapter_count
