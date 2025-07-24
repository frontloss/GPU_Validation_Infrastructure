########################################################################################################################
# @file         driver_escape_wrapper.py
# @brief        Contains wrapper functions calling Driver Escape CDLL exposed APIs only
# @author       Kiran Kumar Lakshmanan, Amit Sau
########################################################################################################################

import ctypes
import os
import time
from typing import List

from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import driver_escape_args as args

_escape_dll = None

##
# @brief        Driver Escape Load Library.
# @return       None
def load_library():
    global _escape_dll
    try:
        _escape_dll = ctypes.cdll.LoadLibrary(os.path.join(test_context.BIN_FOLDER, 'DriverEscape.dll'))
    except IOError as error:
        # captures both File not Found error and LoadLibrary failed errors.
        raise Exception(f'Failed to Load DriverEscape Library : {error}')


##
# @brief        Retrieves DPCD register value based on Given Address offset & DisplayAndAdapterInfo Structure
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    offset - HW Address offset in Hex
# @return       (result, reg_value) - (Escape Call Status, DPCD Buffer)
def read_dpcd(display_and_adapter_info: DisplayAndAdapterInfo, offset: int) -> (bool, bytes):
    reg_value_buffer_size = ctypes.c_ulong * args.DPCD_BUFFER_SIZE
    reg_value = reg_value_buffer_size()
    buffer_size = ctypes.c_uint(args.DPCD_BUFFER_SIZE)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_ulong, ctypes.c_uint,
                                  reg_value_buffer_size)
    func = prototype(('DpcdRead', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), offset, buffer_size, reg_value)
    return result, reg_value


##
# @brief        Retrieves DPCD register value based on Given Address offset & DisplayAndAdapterInfo Structure for
#               downstream devices.
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    offset - HW Address offset in Hex
# @param[in]    bytes_to_read - Indicates the number of bytes to be read starting from the offset.
# @return       (result, buffer) - (Escape Call Status, DPCD Buffer)
def i2c_aux_read(display_and_adapter_info: DisplayAndAdapterInfo, offset: int, bytes_to_read: int) -> (bool, bytes):
    buffer_type = ctypes.c_ulong * bytes_to_read
    buffer = buffer_type()
    buffer_size = ctypes.c_uint(bytes_to_read)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_ulong, ctypes.c_uint,
                                  buffer_type)
    func = prototype(('YangraI2CAuxRead', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), offset, buffer_size, buffer)
    return result, buffer


##
# @brief        Retrieves DPCD register value based on Given Address offset & DisplayAndAdapterInfo Structure
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    offset - HW Address offset in Hex
# @param[in]    dpcd_data - DPCD data to be written
# @return       (result, reg_value) - (Escape Call Status, DPCD Buffer)
def write_dpcd(display_and_adapter_info: DisplayAndAdapterInfo, offset: int, dpcd_data: list) -> bool:
    reg_value_buffer_size = ctypes.c_ulong * args.DPCD_BUFFER_SIZE
    reg_value = reg_value_buffer_size()
    buffer_size = ctypes.c_uint(len(dpcd_data))
    for num in range(len(dpcd_data)):
        reg_value[num] = ctypes.c_ulong(dpcd_data[num])
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_ulong, ctypes.c_uint,
                                  reg_value_buffer_size)
    func = prototype(('DpcdWrite', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), offset, buffer_size, reg_value)
    return result


##
# @brief        Retrieves DPCD register value based on Given Address offset & DisplayAndAdapterInfo Structure for
#               downstream devices.
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    offset - HW Address offset in Hex
# @param[in]    dpcd_data - DPCD data to be written
# @return       is_success - Escape Call Status
def i2c_aux_write(display_and_adapter_info: DisplayAndAdapterInfo, offset: int, dpcd_data: List[int]) -> bool:
    buffer_type = ctypes.c_ulong * len(dpcd_data)
    buffer_size = ctypes.c_uint(len(dpcd_data))
    buffer = (ctypes.c_int * len(dpcd_data))(*dpcd_data)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_ulong, ctypes.c_uint,
                                  buffer_type)
    func = prototype(('YangraI2CAuxWrite', _escape_dll))
    is_success = func(ctypes.byref(display_and_adapter_info), offset, buffer_size, buffer)
    return is_success


##
# @brief        Retrieves EDID information of Given Panel or Port
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @return       (result, edid_data, edid_block_count) - (Escape Call Status, EDID data, EDID blocks count)
def get_edid_data(display_and_adapter_info: DisplayAndAdapterInfo) -> (bool, bytes, int):
    max_edid_buffer_size = ctypes.c_ubyte * (args.MAX_EDID_BLOCK * args.EDID_BLOCK_SIZE)
    edid_data = max_edid_buffer_size()
    edid_block_count = ctypes.c_uint(0)
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), max_edid_buffer_size,
                                  ctypes.POINTER(ctypes.c_uint))
    func = prototype(('GetEdidData', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), edid_data, ctypes.byref(edid_block_count))
    return result, edid_data, edid_block_count


##
# @brief        Get Miscellaneous System Information for a given Adapter
# @param[in]    adapter_info - GfxAdapterInfo object
# @return       (result, misc_system_info) - (Escape Call Status, System Info)
def get_misc_system_info(adapter_info: GfxAdapterInfo) -> (bool, args.MiscEscGetSystemInfoArgs):
    misc_system_info = args.MiscEscGetSystemInfoArgs()
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo),
                                  ctypes.POINTER(args.MiscEscGetSystemInfoArgs))
    func = prototype(('GetMiscSystemInfo', _escape_dll))
    result = func(ctypes.byref(adapter_info), ctypes.byref(misc_system_info))
    return result, misc_system_info


##
# @brief        Gets the hardware LUT info
# @param[in]    adapter_info - GfxAdapterInfo object
# @param[in]    cui_dpp_hw_lut_info - pointer to structure DppHwLutInfo
# @return       (result, cui_dpp_hw_lut_info) - (Escape Call Status, Hardware LUT info)
def get_dpp_hw_lut(adapter_info: GfxAdapterInfo, cui_dpp_hw_lut_info: args.DppHwLutInfo) -> (bool, args.DppHwLutInfo):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.POINTER(args.DppHwLutInfo))
    func = prototype(('GetDPPHWLUTN', _escape_dll))
    result = func(ctypes.byref(adapter_info), ctypes.byref(cui_dpp_hw_lut_info))
    return result, cui_dpp_hw_lut_info


##
# @brief        Sets the Hardware LUT
# @param[in]    adapter_info - GfxAdapterInfo object
# @param[in]    cui_dpp_hw_lut_info - pointer to structure DppHwLutInfo containing HW LUT Info and targetID
# @return       result - Escape Call Status
def set_dpp_hw_lut(adapter_info: GfxAdapterInfo, cui_dpp_hw_lut_info: args.DppHwLutInfo) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.POINTER(args.DppHwLutInfo))
    func = prototype(('SetDPPHWLUTN', _escape_dll))
    result = func(ctypes.byref(adapter_info), ctypes.byref(cui_dpp_hw_lut_info))
    return result


##
# @brief        Enables and disables xvYCC
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    is_enable - Boolean value to either enable or disable xvYCC
# @return       result - Escape Call Status
def configure_xvycc(display_and_adapter_info: DisplayAndAdapterInfo, is_enable: bool) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_ubyte)
    func = prototype(('ConfigureXvYcc', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), is_enable)
    return result


##
# @brief        Enables and disables YCbCr
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    is_enable - Boolean value to either enable or disable YCbCr
# @param[in]    color_model - color_models
# @return       result - Escape Call Status
def configure_ycbcr(display_and_adapter_info: DisplayAndAdapterInfo, is_enable: bool, color_model) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_ubyte, ctypes.c_uint)
    func = prototype(('ConfigureYCbCr', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), is_enable, color_model)
    return result


##
# @brief        Checks if xvYCC is supported by the display
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @return       result - True if xvYcc is supported, False otherwise
def is_xvycc_supported(display_and_adapter_info: DisplayAndAdapterInfo) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('IsXvYccSupported', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        Get or set quantisation operation
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    avi_frame_info - Pointer to structure AviInfoFrameArgs containing quantisation operation Info
# @return       (result, get_set_quantisation) - (Escape Call Status, AviInfoFrame Args info)
def get_set_quantisation_range(display_and_adapter_info: DisplayAndAdapterInfo,
                               avi_frame_info: args.AviInfoFrameArgs) -> (bool, args.AviInfoFrameArgs):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo),
                                  ctypes.POINTER(args.AviInfoFrameArgs))
    func = prototype(('YangraGetSetQuantisationRange', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), ctypes.byref(avi_frame_info))
    return result, avi_frame_info


##
# @brief        Get or set bpc and encoding
# @param[in]    display_and_adapter_info - Target id or DisplayAndAdapterInfo object
# @param[in]    cui_deep_color_args - Pointer to structure CuiDeepColorInfo containing override bpc and encoding Info
# @return       (result, cui_deep_color_args) - (Escape Call Status, CuiDeepColorInfo Args info)
def get_set_output_format(display_and_adapter_info: DisplayAndAdapterInfo,
                          cui_deep_color_args: args.CuiDeepColorInfo) -> (bool, args.CuiDeepColorInfo):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo),
                                  ctypes.POINTER(args.CuiDeepColorInfo))
    func = prototype(('GetSetOutputFormat', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), ctypes.byref(cui_deep_color_args))
    return result, cui_deep_color_args


##
# @brief        Checks if YCbCr is supported by the display
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @return       result - True if YcbCr is supported, False otherwise.
def is_ycbcr_supported(display_and_adapter_info: DisplayAndAdapterInfo) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo))
    func = prototype(('IsYCbCrSupported', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info))
    return result


##
# @brief        Enable or Disable LACE based on the aggressiveness level and lux values
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    lux - lux value
# @param[in]    lux_operation - whether to perform lux operation or not
# @param[in]    aggressiveness_level - between 0-2 (LOW-MEDIUM-HIGH) values
# @param[in]    aggressiveness_operation - whether to perform aggressiveness operation or not
# @return       result - Escape Call Status
def als_aggressiveness_level_override(display_and_adapter_info: DisplayAndAdapterInfo, lux: int = 0,
                                      lux_operation: bool = False,
                                      aggressiveness_level: int = 0, aggressiveness_operation: bool = False) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.c_int, ctypes.c_int,
                                  ctypes.c_int, ctypes.c_int)
    func = prototype(('YangraAlsAggressivenessLevelOverride', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info.adapterInfo), lux_operation, aggressiveness_operation, lux,
                  aggressiveness_level)
    return result


##
# @brief        Apply Linear or Non-Linear CSC
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    csc_operation - Get or Set Operation Type
# @param[in]    csc_matrix_type - Linear or Non-Linear CSC
# @param[in]    csc_pipe_params - pointer to structure CSCPipeMatrixParams containing CSC Matrix, Pre,PostOffsets
# @return       apply_csc_result - Escape Call Status
def apply_csc(display_and_adapter_info: DisplayAndAdapterInfo, csc_operation: int, csc_matrix_type: int,
              csc_pipe_params: args.CSCPipeMatrixParams) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_int, ctypes.c_int,
                                  ctypes.POINTER(args.CSCPipeMatrixParams))
    func = prototype(('YangraApplyCSC', _escape_dll))
    apply_csc_result = func(ctypes.byref(display_and_adapter_info), csc_operation, csc_matrix_type,
                            ctypes.byref(csc_pipe_params))
    return apply_csc_result


##
# @brief        Get or set VRR operation
# @param[in]    adapter_info - GfxAdapterInfo object
# @param[in]    vrr_args - Pointer to structure VrrArgs containing VRR operation Info
# @return       (result, vrr_args) - (Escape Call Status, VRR Args info)
def get_set_vrr(adapter_info: GfxAdapterInfo, vrr_args: args.VrrArgs) -> (bool, args.VrrArgs):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.POINTER(args.VrrArgs))
    func = prototype(('YangraGetSetVrr', _escape_dll))
    result = func(ctypes.byref(adapter_info), ctypes.byref(vrr_args))
    return result, vrr_args


##
# @brief        Plug or Unplug writeback device.
# @param[in]    adapter_info - GfxAdapterInfo object
# @param[in]    wb_hpd_args - Pointer to structure WritebackHpd containing writeback HPD Info
# @param[in]    edid_path - EDID File path
# @return       result - Escape Call Status
def plug_unplug_wb_device(adapter_info: GfxAdapterInfo, wb_hpd_args: args.WritebackHpd, edid_path: None) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), args.WritebackHpd, ctypes.c_char_p)
    func = prototype(('YangraPlugUnplugWBDevice', _escape_dll))
    result = func(ctypes.byref(adapter_info), wb_hpd_args, edid_path)
    return result


##
# @brief        Check if Writeback feature is enabled or not.
# @param[in]    adapter_info - GfxAdapterInfo object
# @param[in]    wb_query_args - Pointer to structure WbQueryArgs containing writeback query info
# @return       (result, wb_hpd_args) - (Escape Call Status, Writeback Hpd Args info)
def query_wb(adapter_info: GfxAdapterInfo, wb_query_args: args.WbQueryArgs) -> (bool, args.WbQueryArgs):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.POINTER(args.WbQueryArgs))
    func = prototype(('YangraQueryWB', _escape_dll))
    result = func(ctypes.byref(adapter_info), ctypes.byref(wb_query_args))
    return result, wb_query_args


##
# @brief        Dump Writeback buffer info
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    instance - Writeback dump instance number
# @param[in]    wb_buffer_info - WbBufferInfo object
# @param[in]    image_bpc - Writeback output dump bpc
# @return       (result, wb_buffer_info) - (Escape Call Status, Writeback Buffer info)
def dump_wb_buffer(display_and_adapter_info: DisplayAndAdapterInfo, instance: int, wb_buffer_info: args.WbBufferInfo,
                   image_bpc: int) -> (bool, args.WbBufferInfo):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_uint,
                                  ctypes.POINTER(args.WbBufferInfo), ctypes.c_uint)
    func = prototype(('YangraDumpWBBuffer', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), instance, ctypes.byref(wb_buffer_info), image_bpc)
    return result, wb_buffer_info


##
# @brief        Get or set CFPS operation
# @param[in]    adapter_info - GfxAdapterInfo object
# @param[in]    cfps_args - Pointer to structure CappedFpsArgs with CappedFps info
# @return       (result, cfps_args) - (Escape call status, Capped FPS Info)
def get_set_cfps(adapter_info: GfxAdapterInfo, cfps_args: args.CappedFpsArgs) -> (bool, args.CappedFpsArgs):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.POINTER(args.CappedFpsArgs))
    func = prototype(('YangraGetSetCfps', _escape_dll))
    result = func(ctypes.byref(adapter_info), ctypes.byref(cfps_args))
    return result, cfps_args


##
# @brief        Get or Set NN Scaling
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    get_set_nn_args - Pointer to structure  NNArgs with NN Scaling info
# @return       (result, get_set_nn_args) - (Escape call status, NN Scaling info)
def get_set_nn_scaling(display_and_adapter_info: GfxAdapterInfo, get_set_nn_args: args.NNArgs) -> (bool, args.NNArgs):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.POINTER(args.NNArgs))
    func = prototype(('YangraGetSetNNScaling', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info.adapterInfo), ctypes.byref(get_set_nn_args))
    return result, get_set_nn_args


##
# @brief        Add provided custom mode
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    hz_res - horizontal resolution of custom mode
# @param[in]    vt_res - vertical resolution of custom mode
# @return       result - Escape call status
def add_custom_mode(display_and_adapter_info: DisplayAndAdapterInfo, hz_res: int, vt_res: int) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.c_ulong, ctypes.c_ulong)
    func = prototype(('YangraAddCustomMode', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), hz_res, vt_res)
    return result


##
# @brief        Invoke Collage Functionality - IsCollagePossible, EnableCollage, ValidateCollage, DisableCollage
# @param[in]    adapter_info - GfxAdapterInfo object
# @param[in]    collage_mode_args - Pointer to Structure CollageModeArgs with collage mode args and operation
# @return       (result, collage_mode_args) - (Escape call status, collage mode args info)
def invoke_collage(adapter_info: GfxAdapterInfo, collage_mode_args: args.CollageModeArgs) -> (
bool, args.CollageModeArgs):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.POINTER(args.CollageModeArgs))
    func = prototype(('YangraInvokeCollage', _escape_dll))
    result = func(ctypes.byref(adapter_info), ctypes.byref(collage_mode_args))
    return result, collage_mode_args


##
# @brief        To generate TDR
# @param[in]    adapter_info - GfxAdapterInfo object
# @param[in]    is_displaytdr - To specify VSYNC TDR or KMD TDR
# @return       result - True if TDR generated, False otherwise
def generate_adapter_tdr(adapter_info: GfxAdapterInfo, is_displaytdr: bool) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.c_ubyte)
    func = prototype(('GenerateTdr', _escape_dll))
    result = func(ctypes.byref(adapter_info), is_displaytdr)
    time.sleep(10)
    return result


##
# @brief        Get or Set Custom Scaling
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    get_set_scaling_args - Pointer to structure CustomScalingArgs with Custom Scaling info
# @return       (result, get_set_scaling_args) - (Escape call status, Custom Scaling info)
def get_set_custom_scaling(display_and_adapter_info: DisplayAndAdapterInfo,
                           get_set_scaling_args: args.CustomScalingArgs) -> (bool, args.CustomScalingArgs):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.POINTER(args.CustomScalingArgs))
    func = prototype(('YangraGetSetCustomScaling', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info.adapterInfo), ctypes.byref(get_set_scaling_args))
    return result, get_set_scaling_args


##
# @brief        Configure Power Component
# @param[in]    adapter_info - GfxAdapterInfo object
# @param[in]    enable - Boolean value to activate or idle power component
# @return       result - Escape call status
def configure_power_component(adapter_info: GfxAdapterInfo, enable: bool) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.c_bool)
    func = prototype(('CfgDxgkPowerComponent', _escape_dll))
    return func(ctypes.byref(adapter_info), enable)


##
# @brief        get_set_display_pc_feature_state
# @param[in]    adapter_info - Target id or DisplayAndAdapterInfo object
# @param[in]    feature_args - Pointer to structure ComEscPowerConservationArgs
# @return       (result, feature_args) - (Escape call status, ComEscPowerConservationArgs)
def get_set_display_pc_feature_state(adapter_info: GfxAdapterInfo, feature_args: args.ComEscPowerConservationArgs) -> (bool, args.ComEscPowerConservationArgs):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.POINTER(args.ComEscPowerConservationArgs))
    func = prototype(('YangraGetSetPcFeatures', _escape_dll))
    result = func(ctypes.byref(adapter_info), ctypes.byref(feature_args))
    return result, feature_args


##
# @brief        Get/Set Genlock
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    enable enable or disable genlock
# @param[in]    genlock_args object of type DdCapiEscGetSetGenlockArgs containing filled-in genlock arguments.
# @return       returns True if escape operation successful, False otherwise.
def get_set_genlock(display_and_adapter_info: DisplayAndAdapterInfo, enable, genlock_args: args.DdCapiEscGetSetGenlockArgs) -> bool:
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(GfxAdapterInfo), ctypes.c_bool,
                                  ctypes.POINTER(args.DdCapiEscGetSetGenlockArgs))
    func = prototype(('YangraGetSetGenlockMode', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info.adapterInfo), enable, ctypes.byref(genlock_args))
    return result

##
# @brief        Get Custom mode details
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    get_custom_mode_args - Pointer to structure CustomModeArgs with Custom Mode info
# @return       returns True if escape operation successful, False otherwise.
def get_custom_mode(display_and_adapter_info: DisplayAndAdapterInfo, get_custom_mode_args: args.CustomModeArgs) ->(bool, args.CustomModeArgs):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo),ctypes.POINTER(args.CustomModeArgs))
    func = prototype(('YangraGetCustomMode',_escape_dll))
    result = func(ctypes.byref(display_and_adapter_info),ctypes.byref(get_custom_mode_args))
    return result, get_custom_mode_args


##
# @brief        Get/Set Genlock Vblank TS
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    genlock_args object of type DdCapiGetVblankTimestampForTarget containing filled-in genlock arguments.
# @return       returns True if escape operation successful, False otherwise.
def get_set_genlock_vblank_ts(display_and_adapter_info: DisplayAndAdapterInfo, genlock_args: args.DdCapiGetVblankTimestampForTarget):
    prototype = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.POINTER(DisplayAndAdapterInfo), ctypes.POINTER(args.DdCapiGetVblankTimestampForTarget))
    func = prototype(('YangraGetSetVblankTs', _escape_dll))
    result = func(ctypes.byref(display_and_adapter_info), ctypes.byref(genlock_args))
    return result, genlock_args
