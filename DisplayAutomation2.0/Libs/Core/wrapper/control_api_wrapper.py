########################################################################################################################
# @file         control_api_wrapper.py
# @brief        Module contains Control API wrapper methods
# @author       Prateek Joshi
########################################################################################################################

import ctypes
import logging
import os
from typing import Union, Tuple

from Libs.Core.display_config import adapter_info_struct
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.display_config.display_config_struct import MultiDisplayAndAdapterInfo
from Libs.Core.test_env.test_context import BIN_FOLDER
from Libs.Core.wrapper import control_api_args as ctl_args

_control_api_dll: Union[ctypes.CDLL, None] = None


##
# @brief        Control API Load Library.
# @return       None
def load_library():
    global _control_api_dll
    try:
        _control_api_dll = ctypes.cdll.LoadLibrary(os.path.join(BIN_FOLDER, 'ControlAPI.dll'))
    except IOError as error:
        # captures both File not Found error and LoadLibrary failed errors.
        raise Exception(f'Failed to Load Control API Library : {error}')


##
# @brief        Configures Control API
# @param[in]    flag - True to initialize, False to close
# @return       True if Initialize/Close is successful, False otherwise
def configure_control_api(flag: bool) -> bool:
    if flag:
        default_version = ctl_args.CTL_MAKE_VERSION(ctl_args.CTL_IMPL_MAJOR_VERSION, ctl_args.CTL_IMPL_MINOR_VERSION)
        default_uid = \
            ctl_args.ctl_application_id_t(0x372464b5, 0xd1b4, 0x419d, [0x82, 0xe7, 0xef, 0xe5, 0x1b, 0x84, 0xfd, 0x8b])
        initargs = ctl_args.ctl_init_args(default_version, default_uid)
        if init_ctl_api(initargs):
            logging.info(" Init CTL API ".center(64, "-"))
            return True
        logging.warning("Init CTL API Failed")
        return False
    # Considering Flag is false and closing control api
    if close_ctl_api():
        logging.info(" Close CTL API ".center(64, "-"))
        return True
    logging.warning("Close CTL API Failed")
    return False


##
# @brief        Initialises Control API
# @param[in]    initargs - init args structure
# @return       result - True if Initialize is successful, False otherwise
def init_ctl_api(initargs: ctl_args.ctl_init_args) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_init_args))
    func = prototype(('ControlAPIInitialize', _control_api_dll))
    result = func(ctypes.byref(initargs))
    return result


##
# @brief        Cleanup control API
# @return       result - True if Cleanup is successful, False otherwise
def close_ctl_api() -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool)
    func = prototype(('ControlAPICleanup', _control_api_dll))
    result = func()
    return result


##
# @brief        API to Get Display Properties
# @param[in]    display_properties - display properties structure
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if display properties fetched successfully, False otherwise
def get_display_properties(display_properties: ctl_args.ctl_display_properties_t,
                           display_and_adapter_info: Union[DisplayAndAdapterInfo, int]) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_display_properties_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetDisplayProperties', _control_api_dll))
    result = func(ctypes.byref(display_properties), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Display Properties
# @param[in]    display_encoder_properties - display encoder properties structure
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if display properties fetched successfully, False otherwise
def get_display_encoder_properties(display_encoder_properties: ctl_args.ctl_adapter_display_encoder_properties_t,
                                   display_and_adapter_info: Union[DisplayAndAdapterInfo, int]) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_adapter_display_encoder_properties_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetDisplayEncoderProperties', _control_api_dll))
    result = func(ctypes.byref(display_encoder_properties), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        Display shift
# @param[in]    mux_properties - Mux properties structure
# @return       result - True if device properties obtained successfully, False otherwise
def display_shift() -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool)
    func = prototype(('ControlAPISwitchMux', _control_api_dll))
    result = func()
    return result


##
# @brief        Get Graphics Adapter Device Properties
# @param[in]    device_properties - device properties structure
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if device properties obtained successfully, False otherwise
def get_device_properties(device_properties: ctl_args.ctl_device_adapter_properties,
                          display_and_adapter_info: Union[DisplayAndAdapterInfo, int]) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_device_adapter_properties),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetDeviceProperties', _control_api_dll))
    result = func(ctypes.byref(device_properties), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Ze Device (Level0 API)
# @param[in]    ze_properties - ze properties structure
# @return       result - True if Ze Device is successfully, False otherwise
def get_zedevice(ze_properties: ctl_args.ze_device_module_properties_t) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ze_device_module_properties_t))
    func = prototype(('ControlAPIGetZeDevice', _control_api_dll))
    result = func(ctypes.byref(ze_properties))
    return result


##
# @brief        API to Get/Set I2C Access
# @param[in]    i2c_args - I2c Args Info
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if enumerated displays fetched successfully, False otherwise
def i2c_access(i2c_args: ctl_args.ctl_i2c_access_args,
               display_and_adapter_info: Union[DisplayAndAdapterInfo, int]) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_i2c_access_args),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPII2CAccess', _control_api_dll))
    result = func(ctypes.byref(i2c_args), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get/Set Aux Access
# @param[in]    aux_args - Aux Args Info
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if enumerated displays fetched successfully, False otherwise
def aux_access(aux_args: ctl_args.ctl_aux_access_args,
               display_and_adapter_info: Union[DisplayAndAdapterInfo, int]) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_aux_access_args),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIAuxAccess', _control_api_dll))
    result = func(ctypes.byref(aux_args), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Sharpness Caps
# @param[in]    sharpnessCaps - Sharpness Caps Info
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get sharpness caps is successfully, False otherwise
def get_sharpness_caps(sharpnessCaps: ctl_args.ctl_sharpness_caps, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_sharpness_caps),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetSharpnessCaps', _control_api_dll))
    result = func(ctypes.byref(sharpnessCaps), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Sharpness
# @param[in]    getSharpness - Sharpness settings
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get sharpness is successfully, False otherwise
def get_sharpness(getSharpness: ctl_args.ctl_sharpness_settings, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_sharpness_settings),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetCurrentSharpness', _control_api_dll))
    result = func(ctypes.byref(getSharpness), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set Sharpness
# @param[in]    setSharpness - Sharpness settings
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if set sharpness is successfully, False otherwise
def set_sharpness(setSharpness: ctl_args.ctl_sharpness_settings, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_sharpness_settings),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetCurrentSharpness', _control_api_dll))
    result = func(ctypes.byref(setSharpness), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Panel Descriptor / EDID
# @param[in]    argsPanelDescriptor - Panel Descriptor Args
# @param[in]    argsExtPanelDescriptor - Panel Descriptor Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_panel_descriptor(argsPanelDescriptor: ctl_args.ctl_panel_descriptor_access_args_t,
                         argsExtPanelDescriptor: ctl_args.ctl_panel_descriptor_access_args_t,
                         display_and_adapter_info) -> (bool, bytes):
    from Libs.Core.display_config.display_config import DisplayConfiguration
    max_edid_buffer_size = ctypes.c_ubyte * (ctl_args.MAX_EDID_BLOCK * ctl_args.EDID_BLOCK_SIZE)
    edid_data = max_edid_buffer_size()
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_panel_descriptor_access_args_t),
                                  ctypes.POINTER(ctl_args.ctl_panel_descriptor_access_args_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo), max_edid_buffer_size)
    func = prototype(('ControlAPIGetPanelDescriptorAccess', _control_api_dll))
    result = func(ctypes.byref(argsPanelDescriptor), ctypes.byref(argsExtPanelDescriptor),
                  ctypes.byref(display_and_adapter_info), edid_data)
    return result, edid_data


##
# @brief        API to Get Power Optimization Caps
# @param[in]    argsGetPowerCaps - Power Optimization Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_power_caps(argsGetPowerCaps: ctl_args.ctl_power_optimization_caps_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_power_optimization_caps_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetPowerCaps', _control_api_dll))
    result = func(ctypes.byref(argsGetPowerCaps), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get PSR Status
# @param[in]    argsGetPSR - Power Optimization Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_psr(argsGetPSR: ctl_args.ctl_power_optimization_settings_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_power_optimization_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetPSR', _control_api_dll))
    result = func(ctypes.byref(argsGetPSR), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set PSR
# @param[in]    argsSetPSR - Power Optimization Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_psr(argsSetPSR: ctl_args.ctl_power_optimization_settings_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_power_optimization_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetPSR', _control_api_dll))
    result = func(ctypes.byref(argsSetPSR), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get UBRR
# @param[in]    argsGetUBRR - Power Optimization Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_ubrr(argsGetUBRR: ctl_args.ctl_power_optimization_settings_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_power_optimization_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetUBRR', _control_api_dll))
    result = func(ctypes.byref(argsGetUBRR), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set UBRR
# @param[in]    argsSetUBRR - Power Optimization Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_ubrr(argsSetUBRR: ctl_args.ctl_power_optimization_settings_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_power_optimization_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetUBRR', _control_api_dll))
    result = func(ctypes.byref(argsSetUBRR), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Pixel Transformation (Get Capability)
# @param[in]    argsGetCaps - Pixel Transformation Pipe Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_color_capability(argsGetCaps: ctl_args.ctl_pixtx_pipe_get_config_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_pixtx_pipe_get_config_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIColorGetCapability', _control_api_dll))
    result = func(ctypes.byref(argsGetCaps), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Pixel Transformation (Get Gamma)
# @param[in]    argsGetGamma - Pixel Transformation Pipe Config Args
# @param[in]    block_cfg - Pixel Transformation Block Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_gamma(argsGetGamma: ctl_args.ctl_pixtx_pipe_get_config_t, block_cfg: ctl_args.ctl_pixtx_block_config_t,
              display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_pixtx_pipe_get_config_t),
                                  ctypes.POINTER(ctl_args.ctl_pixtx_block_config_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetGamma', _control_api_dll))
    result = func(ctypes.byref(argsGetGamma), ctypes.byref(block_cfg), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set Pixel Transformation (Set Gamma)
# @param[in]    argsSetGamma - Pixel Transformation Pipe Config Args
# @param[in]    block_cfg - Pixel Transformation Block Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_gamma(argsSetGamma: ctl_args.ctl_pixtx_pipe_set_config_t, block_cfg: ctl_args.ctl_pixtx_block_config_t,
              display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_pixtx_pipe_set_config_t),
                                  ctypes.POINTER(ctl_args.ctl_pixtx_block_config_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetGamma', _control_api_dll))
    result = func(ctypes.byref(argsSetGamma), ctypes.byref(block_cfg), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set Pixel Transformation (Set CSC)
# @param[in]    argsSetCSC - Pixel Transformation Pipe Config Args
# @param[in]    block_cfg - Pixel Transformation Block Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_csc(argsSetCSC: ctl_args.ctl_pixtx_pipe_set_config_t, block_cfg: ctl_args.ctl_pixtx_block_config_t,
            display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_pixtx_pipe_set_config_t),
                                  ctypes.POINTER(ctl_args.ctl_pixtx_block_config_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetCSC', _control_api_dll))
    result = func(ctypes.byref(argsSetCSC), ctypes.byref(block_cfg), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set Pixel Transformation (Set the Color Blocks)
# @param[in]    args_set_feature - Pixel Transformation Pipe Config Args
# @param[in]    blk_cfg - Pixel Transformation Block Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @param[in]    set_num_blocks - Number of blocks to be set
# @param[in]    mode - to identify whether it is SDR/HDR/WCG modes
# @return       result - True if get call is successfully, False otherwise
def set_igcl_color_feature(args_set_feature: ctl_args.ctl_pixtx_pipe_set_config_t,
                           blk_cfg: ctl_args.ctl_pixtx_pipe_get_config_t, display_and_adapter_info, set_num_blocks,
                           mode) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_pixtx_pipe_set_config_t),
                                  ctypes.POINTER(ctl_args.ctl_pixtx_pipe_get_config_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_ulong, ctypes.c_uint8)
    func = prototype(('ControlAPISetColorFeature', _control_api_dll))
    result = func(ctypes.byref(args_set_feature), ctypes.byref(blk_cfg), ctypes.byref(display_and_adapter_info),
                  set_num_blocks, mode)
    logging.debug("SetCall Result {0}".format(result))
    return result


##
# @brief        API to Set Pixel Transformation (Restore Default)
# @param[in]    argsRestoreDefault - Pixel Transformation Pipe Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def restore_default(argsRestoreDefault: ctl_args.ctl_pixtx_pipe_set_config_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_pixtx_pipe_set_config_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIRestoreDefault', _control_api_dll))
    result = func(ctypes.byref(argsRestoreDefault), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set Pixel Transformation (Set Hue Saturation)
# @param[in]    argsSetCSC - Pixel Transformation Pipe Config Args
# @param[in]    block_cfg - Pixel Transformation Block Config Args
# @param[in]    hue - Hue Value
# @param[in]    sat - Saturation Value
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_hue_saturation(argsSetCSC: ctl_args.ctl_pixtx_pipe_set_config_t, block_cfg: ctl_args.ctl_pixtx_block_config_t,
                       hue: ctypes.c_double, sat: ctypes.c_double, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_pixtx_pipe_set_config_t),
                                  ctypes.POINTER(ctl_args.ctl_pixtx_block_config_t), ctypes.c_double, ctypes.c_double,
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIHueSaturation', _control_api_dll))
    result = func(ctypes.byref(argsSetCSC), ctypes.byref(block_cfg), hue, sat,
                  ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set Pixel Transformation (Set 3DLUT)
# @param[in]    argsSet3DLUT - Pixel Transformation Pipe Config Args
# @param[in]    block_cfg - Pixel Transformation Block Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_3dlut(argsSet3DLUT: ctl_args.ctl_pixtx_pipe_set_config_t, block_cfg: ctl_args.ctl_pixtx_block_config_t,
              display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_pixtx_pipe_set_config_t),
                                  ctypes.POINTER(ctl_args.ctl_pixtx_block_config_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISet3DLUT', _control_api_dll))
    result = func(ctypes.byref(argsSet3DLUT), ctypes.byref(block_cfg), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set DPST
# @param[in]    argsSetDPST - Power Optimization Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_dpst(argsSetDPST: ctl_args.ctl_power_optimization_settings_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_power_optimization_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetDPST', _control_api_dll))
    result = func(ctypes.byref(argsSetDPST), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get DPST
# @param[in]    argsGetDPST - Power Optimization Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_dpst(argsGetDPST: ctl_args.ctl_power_optimization_settings_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_power_optimization_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetDPST', _control_api_dll))
    result = func(ctypes.byref(argsGetDPST), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Scaling Caps
# @param[in]    argsGetScalingCaps - Scaling Caps Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_scaling_caps(argsGetScalingCaps: ctl_args.ctl_scaling_settings_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_scaling_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetScalingCaps', _control_api_dll))
    result = func(ctypes.byref(argsGetScalingCaps), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Scaling
# @param[in]    argsGetScaling - Scaling Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_scaling(argsGetScaling: ctl_args.ctl_scaling_settings_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_scaling_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetScaling', _control_api_dll))
    result = func(ctypes.byref(argsGetScaling), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set Scaling
# @param[in]    argsSetScaling - Scaling Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_scaling(argsSetScaling: ctl_args.ctl_scaling_settings_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_scaling_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetScaling', _control_api_dll))
    result = func(ctypes.byref(argsSetScaling), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Retro Scaling Caps
# @param[in]    argsGetScalingCaps - Retro Scaling Caps Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_retro_scaling_caps(argsGetScalingCaps: ctl_args.ctl_retro_scaling_caps_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_retro_scaling_caps_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetRetroScalingCaps', _control_api_dll))
    result = func(ctypes.byref(argsGetScalingCaps), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get-Set Retro Scaling
# @param[in]    argsGetSetRetroScaling - Retro Scaling Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_set_retro_scaling(argsGetSetRetroScaling: ctl_args.ctl_retro_scaling_settings_t,
                          display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_retro_scaling_settings_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetSetRetoScaling', _control_api_dll))
    result = func(ctypes.byref(argsGetSetRetroScaling), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get-Set Endurance Gaming
# @param[in]    argsGetSet3DFeature - 3D Feature Setting Args
# @param[in]    argsGetSetEnduranceGaming - Endurance Gaming Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get/set call is successful, False otherwise
def get_set_endurance_gaming(argsGetSet3DFeature: ctl_args.ctl_3d_feature_getset_t,
                             argsGetSetEnduranceGaming: ctl_args.ctl_endurance_gaming_t,
                             display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_3d_feature_getset_t),
                                  ctypes.POINTER(ctl_args.ctl_endurance_gaming_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetSetEnduranceGaming', _control_api_dll))
    result = func(ctypes.byref(argsGetSet3DFeature), ctypes.byref(argsGetSetEnduranceGaming),
                  ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Gaming Flips Caps
# @param[in]    argsGetSet3DFeature - 3D Feature Setting Args
# @param[in]    setFlipMode - Gaming Flip Modes Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_set_gaming_flip_modes(argsGetSet3DFeature: ctl_args.ctl_3d_feature_getset_t, setFlipMode: ctypes.c_int,
                              display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_3d_feature_getset_t), ctypes.c_int,
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetGamingFlipModes', _control_api_dll))
    result = func(ctypes.byref(argsGetSet3DFeature), ctypes.c_int(setFlipMode), ctypes.byref(
        display_and_adapter_info))
    return result


##
# @brief        API to Get Lace config
# @param[in]    argsGetLace - Lace Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_lace(argsGetLace: ctl_args.ctl_lace_config_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)

    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_lace_config_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetLace', _control_api_dll))
    result = func(ctypes.byref(argsGetLace), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to set Lace config
# @param[in]    argsSetLace - Lace Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_lace(argsSetLace: ctl_args.ctl_lace_config_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)

    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_lace_config_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetLace', _control_api_dll))
    result = func(ctypes.byref(argsSetLace), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get WireFormat config
# @param[in]    GetSetWireFormatSetting - WireFormat Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_wireformat(GetSetWireFormatSetting: ctl_args.ctl_get_set_wireformat, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)

    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_get_set_wireformat),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetOutputFormat', _control_api_dll))
    result = func(ctypes.byref(GetSetWireFormatSetting), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to set WireFormat config
# @param[in]    argsSetWireFormat - WireFormat Config Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_wireformat(argsSetWireFormat: ctl_args.ctl_get_set_wireformat, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)

    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_get_set_wireformat),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetOutputFormat', _control_api_dll))
    result = func(ctypes.byref(argsSetWireFormat), ctypes.byref(display_and_adapter_info))
    return result

##
# @brief        API to Get arc_sync monitor parameters
# @param[in]    argsGetMonitorParams - Monitor Parameters
# @param[in]    display_and_adapter_info - display and adapter info structure
# @return       result - True if get call is successfully, False otherwise
def get_intel_arc_sync_info(argsGetMonitorParams: ctl_args.ctl_intel_arc_sync_monitor_params_t,
                            display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_intel_arc_sync_monitor_params_t))
    func = prototype(('ControlAPIGetIntelArcSyncInfo', _control_api_dll))
    result = func(ctypes.byref(argsGetMonitorParams), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get current arc_sync monitor profile
# @param[in]    argsGetProfileParams - Monitor Parameters
# @param[in]    display_and_adapter_info - display and adapter info structure
# @return       result - True if get call is successfully, False otherwise
def get_current_intel_arc_sync_profile(argsGetProfileParams: ctl_args.ctl_intel_arc_sync_profile_params_t,
                                       display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_intel_arc_sync_profile_params_t))
    func = prototype(('ControlAPIGetCurrentArcSyncProfile', _control_api_dll))
    result = func(ctypes.byref(argsGetProfileParams), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set custom Intel Arc sync profile
# @param[in]    argsSetProfileParams - Monitor Parameters
# @param[in]    display_and_adapter_info - display and adapter info structure
# @return       result - True if get call is successfully, False otherwise
def set_intel_arc_sync_profile(argsSetProfileParams: ctl_args.ctl_intel_arc_sync_profile_params_t,
                               display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_intel_arc_sync_profile_params_t))
    func = prototype(('ControlAPISetIntelArcSyncProfile', _control_api_dll))
    result = func(ctypes.byref(argsSetProfileParams), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get brightness via IGCL
# @param[in]    argsGetBrightness - Brightness Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def get_brightness_via_igcl(argsGetBrightness: ctl_args.ctl_get_brightness_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_get_brightness_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetBrightnessSetting', _control_api_dll))
    result = func(ctypes.byref(argsGetBrightness), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Set brightness via IGCL
# @param[in]    argsSetBrightness - Brightness Setting Args
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise
def set_brightness_via_igcl(argsSetBrightness: ctl_args.ctl_set_brightness_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_set_brightness_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPISetBrightnessSetting', _control_api_dll))
    result = func(ctypes.byref(argsSetBrightness), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Perform EDID Management operations
# @param[in]    edid_mgmt_args of type ctl_edid_management_args_t
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if enumerated displays fetched successfully, False otherwise
def edid_mgmt(edid_mgmt_args: ctl_args.ctl_edid_management_args_t,
              display_and_adapter_info: Union[DisplayAndAdapterInfo, int]) -> (bool, bytes):
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        logging.error("ERROR: Caller expected to Pass DisplayAndAdaptorInfo Struct instead of TargetID")
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_edid_management_args_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIEDIDManagement', _control_api_dll))
    result = func(ctypes.byref(edid_mgmt_args), ctypes.byref(display_and_adapter_info))
    return result, edid_mgmt_args.OutFlags


##
# @brief        API to Perform Display Genlock Operations
# @param[in]    display_genlock_args of type ctl_genlock_args_t
# @param[in]    display_and_adapter_info - target-id / display_and_adapter_info structure
# @return       result - True if get call is successfully, False otherwise

def display_genlock(display_genlock_args: ctl_args.ctl_genlock_args_t, display_and_adapter_info) -> bool:
    from Libs.Core.display_config.display_config import DisplayConfiguration
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info(display_and_adapter_info)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_genlock_args_t),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetSetDisplayGenlock', _control_api_dll))
    result = func(ctypes.byref(display_genlock_args), ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        API to Get Display timings for all active displays
# @param[in]    display_genlock_args of type ctl_genlock_args_t
# @param[in]    adapter_info - gfx_adapter_info structure
# @return       result - returns True if fetch is successful, False otherwise
def display_genlock_get_all_displays_timings(display_genlock_args: ctl_args.ctl_genlock_args_t,
                                             adapter_info: adapter_info_struct.GfxAdapterInfo) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_genlock_args_t),
                                  adapter_info_struct.GfxAdapterInfo)
    func = prototype(('ControlAPIGetAllDisplayTimingsGenlock', _control_api_dll))
    result = func(ctypes.byref(display_genlock_args), adapter_info)
    return result


##
# @brief        API to Get Display timings for all active displays
# @param[in]    display_and_adapter_info - display_and_adapter_info structure
# @return       result - returns True if fetch is successful, False otherwise
def get_target_display_handle(display_and_adapter_info: DisplayAndAdapterInfo) -> Tuple[bool, int]:
    handle = ctypes.c_ulonglong(0)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_ulonglong),
                                  ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('GetTargetDisplayHandle', _control_api_dll))
    result = func(ctypes.byref(handle), display_and_adapter_info)
    logging.info(f"returned handle - {handle}")
    return result, handle.value

##
# @brief        API to Perform Combined Display operations
# @param[in]    combined_display_args of type ctl_combined_display_args_t
# @param[in]    display_adaptor_buffer - buffer of display_and_adapter_info structure
# @return       result - True if call is successful, False otherwise
def get_set_combined_display(combined_display_args: ctl_args.ctl_combined_display_args_t, display_adaptor_buffer) -> bool:
    display_adaptor_buffer.size = ctypes.sizeof(MultiDisplayAndAdapterInfo)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctl_args.ctl_combined_display_args_t), ctypes.POINTER(MultiDisplayAndAdapterInfo))
    func = prototype(('ControlAPIGetSetCombinedDisplay', _control_api_dll))
    result = func(ctypes.byref(combined_display_args), ctypes.byref(display_adaptor_buffer))
    return result
