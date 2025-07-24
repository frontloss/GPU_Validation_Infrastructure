########################################################################################################################
# @file         driver_escape.py
# @brief        Contains functions calling Driver Escape wrapper APIs
# @author       Kiran Kumar Lakshmanan, Amit Sau
########################################################################################################################
import logging
from typing import List
from typing import Union

from Libs.Core.display_config.adapter_info_struct import GfxAdapterInfo
from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core.wrapper import driver_escape_args as args
from Libs.Core.wrapper import driver_escape_wrapper as escape

##
# @brief        Retrieves DPCD register value based on Given Address offset & DisplayAndAdapterInfo Structure
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    offset - HW Address offset in Hex
# @return       (result, reg_list) - (Escape Call Status, DPCD Buffer value)
def read_dpcd(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], offset: int) -> (bool, list):
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    result, reg_value = escape.read_dpcd(display_and_adapter_info, offset)
    reg_list = list(reg_value)
    if not result:
        logging.error(f"Failed to read DPCD : {offset} for display with target id: {display_and_adapter_info.TargetID}")
        gdhm.report_bug(
            f"[DriverEscape] Failed to read DPCD : {offset} for display with target id: "
            f"{display_and_adapter_info.TargetID}",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )

    return result, reg_list


##
# @brief        Retrieves DPCD register value based on Given offset & DisplayAndAdapterInfo Structure for downstream
#               devices
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Object
# @param[in]    offset - HW Address offset in Hex
# @param[in]    bytes_to_read - Indicates the number of bytes to be read starting from the offset.
# @return       (is_success, dpcd_value_list) - (Escape Call Status, DPCD Buffer value)
def i2c_aux_read(display_and_adapter_info: DisplayAndAdapterInfo, offset: int, bytes_to_read: int) -> (bool, int):
    is_success, read_values = escape.i2c_aux_read(display_and_adapter_info, offset, bytes_to_read)
    dpcd_value_list = list(read_values)
    return is_success, dpcd_value_list


##
# @brief        Writes DPCD register value based on Given Address offset & DisplayAndAdapterInfo Structure
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    offset - HW Address offset in Hex
# @param[in]    dpcd_data - DPCD data to be written
# @return       result - Escape Call Status
def write_dpcd(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], offset: int, dpcd_data: list) -> bool:
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    result = escape.write_dpcd(display_and_adapter_info, offset, dpcd_data)
    return result


##
# @brief        Writes DPCD register value based on Given offset & DisplayAndAdapterInfo Structure for downstream
#               devices.
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Object
# @param[in]    offset - HW Address offset in Hex
# @param[in]    dpcd_data - DPCD data to be written
# @return       is_success - Escape call status
def i2c_aux_write(display_and_adapter_info: DisplayAndAdapterInfo, offset: int, dpcd_data: List[int]) -> bool:
    is_success = escape.i2c_aux_write(display_and_adapter_info, offset, dpcd_data)
    return is_success


##
# @brief        Retrieves EDID information of Given Panel  or  Port
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @return       (result, edid_data, edid_block_count) - (Escape Call Status, EDID data blocks, EDID blocks count)
def get_edid_data(display_and_adapter_info: Union[DisplayAndAdapterInfo, int]) -> (bool, list, int):
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    result, edid_data, edid_block_count = escape.get_edid_data(display_and_adapter_info)
    edid_list = list(edid_data)
    if not result:
        logging.error(f"Failed to get EDID data {display_and_adapter_info.TargetID}")
        gdhm.report_bug(
            f"[DriverEscape] Failed to get EDID data",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
    return result, edid_list, edid_block_count.value


##
# @brief        Get Miscellaneous System Information for a given Adapter
# @param[in]    gfx_index - Graphics Adapter Index
# @return       (bool, object) - (Escape Call Status, MiscEscGetSystemInfoArgs object)
def get_misc_system_info(gfx_index: str) -> (bool, args.MiscEscGetSystemInfoArgs):
    # Get Adapter Info from GFX Adapter Details (Default it takes First Adapter Info from the list)
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    return escape.get_misc_system_info(adapter_info)


##
# @brief        Gets the hardware LUT info
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    cui_dpp_hw_lut_info - pointer to structure DppHwLutInfo containing HW LUT Info and targetID
# @return       (bool, object) - (Escape Call Status, DppHwLutInfo object)
def get_dpp_hw_lut(gfx_index: str, cui_dpp_hw_lut_info: args.DppHwLutInfo) -> (bool, args.DppHwLutInfo):
    # Get Adapter Info from GFX Adapter Details
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    return escape.get_dpp_hw_lut(adapter_info, cui_dpp_hw_lut_info)


##
# @brief        Sets the Hardware LUT
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    cui_dpp_hw_lut_info - pointer to structure DppHwLutInfo containing HW LUT Info and targetID
# @return       bool - Escape Call Status
def set_dpp_hw_lut(gfx_index: str, cui_dpp_hw_lut_info: args.DppHwLutInfo) -> bool:
    # Get Adapter Info from GFX Adapter Details
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    return escape.set_dpp_hw_lut(adapter_info, cui_dpp_hw_lut_info)


##
# @brief        Enables and disables xvYCC
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    is_enable - Boolean value to either enable or disable xvYCC
# @return       bool - Escape Call Status
def configure_xvycc(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], is_enable: bool) -> bool:
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.configure_xvycc(display_and_adapter_info, is_enable)


##
# @brief        Enables and disables YCbCr
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    is_enable - Boolean value to either enable or disable YCbCr
# @param[in]     color_model - int value for YCBCR Preferred Value
# @return       bool - Escape Call Status
def configure_ycbcr(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], is_enable: bool,
                    color_model: int = args.ColorModel.COLOR_MODEL_YCBCR_PREFERRED.value) -> bool:
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.configure_ycbcr(display_and_adapter_info, is_enable, color_model)


##
# @brief        Checks if xvYCC is supported by the display
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @return       bool - True if xvYcc is supported, False otherwise
def is_xvycc_supported(display_and_adapter_info: Union[DisplayAndAdapterInfo, int]) -> bool:
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.is_xvycc_supported(display_and_adapter_info)


##
# @brief        To get or set quantisation operation
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    avi_frame_info - Pointer to structure AviInfoFrameArgs containing quantisation operation Info
# @return       (bool, object) - (Escape Call Status, AviInfoFrameArgs object)
def get_set_quantisation_range(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], avi_frame_info: args.AviInfoFrameArgs) -> (bool, args.AviInfoFrameArgs):
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.get_set_quantisation_range(display_and_adapter_info, avi_frame_info)


##
# @brief        To get or set bpc and encoding
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    cui_deep_color_args - Pointer to structure CuiDeepColorInfo containing override bpc and encoding Info
# @return       (bool, object) - (Escape Call Status, CuiDeepColorInfo object)
def get_set_output_format(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], cui_deep_color_args: args.CuiDeepColorInfo) -> (bool, args.CuiDeepColorInfo):
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.get_set_output_format(display_and_adapter_info, cui_deep_color_args)


##
# @brief        Checks if YCbCr is supported by the display
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @return       bool - True if YcbCr is supported, False otherwise
def is_ycbcr_supported(display_and_adapter_info: Union[DisplayAndAdapterInfo, int]) -> bool:
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.is_ycbcr_supported(display_and_adapter_info)


##
# @brief        Enable or Disable LACE based on the aggressiveness level and lux values
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    lux - lux value
# @param[in]    lux_operation - whether to perform lux operation or not
# @param[in]    aggressiveness_level - between 0-2 (LOW-MEDIUM-HIGH) values
# @param[in]    aggressiveness_operation - whether to perform aggressiveness operation or not
# @return       bool - Escape Call Status
def als_aggressiveness_level_override(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], lux: int = 0,
                                      lux_operation: bool = False,
                                      aggressiveness_level: int = 0,
                                      aggressiveness_operation: bool = False) -> bool:
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.als_aggressiveness_level_override(display_and_adapter_info, lux, lux_operation,
                                                    aggressiveness_level, aggressiveness_operation)


##
# @brief        Apply Linear or Non-Linear CSC
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo object
# @param[in]    csc_operation - Get or Set Operation Type
# @param[in]    csc_matrix_type - Linear or Non-Linear CSC
# @param[in]    csc_pipe_params - pointer to structure CSCPipeMatrixParams containing CSC Matrix, Pre and PostOffsets
# @return       bool - Escape Call Status
def apply_csc(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], csc_operation: int, csc_matrix_type: int,
              csc_pipe_params: args.CSCPipeMatrixParams) -> bool:
    return escape.apply_csc(display_and_adapter_info, csc_operation, csc_matrix_type, csc_pipe_params)


##
# @brief        To get or set VRR operation
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    vrr_args - Pointer to structure VrrArgs containing VRR operation Info
# @return       (bool, object) - (Escape Call Status, VrrArgs Object)
def get_set_vrr(gfx_index: str, vrr_args: args.VrrArgs) -> (bool, args.VrrArgs):
    # Get Adapter Info from GFX Adapter Details
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    return escape.get_set_vrr(adapter_info, vrr_args)


##
# @brief        Plug or Unplug writeback device.
# @param[in]    adapter_info - Graphics Adapter Info
# @param[in]    wb_hpd_args - Pointer to structure WritebackHpd containing writeback HPD Info
# @param[in]    edid_path - EDID file path
# @return       bool - Escape Call Status
def plug_unplug_wb_device(adapter_info: GfxAdapterInfo, wb_hpd_args: args.WritebackHpd, edid_path: None) -> bool:
    return escape.plug_unplug_wb_device(adapter_info, wb_hpd_args, edid_path)


##
# @brief        Check if Writeback feature is enabled or not.
# @param[in]    adapter_info - Graphics Adapter Info
# @param[in]    wb_query_args - Pointer to structure WbQueryArgs containing writeback query info
# @return       (bool, object) - (Escape Call Status, WbQueryArgs Object)
def query_wb(adapter_info: GfxAdapterInfo, wb_query_args: args.WbQueryArgs) -> (bool, args.WbQueryArgs):
    return escape.query_wb(adapter_info, wb_query_args)


##
# @brief        Dump Writeback buffer info.
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    instance - write back dump instance number
# @param[in]    wb_buffer_info - WbBufferInfo object
# @param[in]    image_bpc - Image BPC value
# @return       (result, wb_buffer_info) - (Escape Call Status, WbBufferInfo Object)
def dump_wb_buffer(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], instance: int, wb_buffer_info: args.WbBufferInfo, image_bpc: int) -> (bool, args.WbBufferInfo):
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    result, wb_buffer_info = escape.dump_wb_buffer(display_and_adapter_info, instance, wb_buffer_info, image_bpc)
    return result, wb_buffer_info


##
# @brief        Get or set CFPS operation
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    cfps_args - Pointer to structure CappedFpsArgs with CappedFps info
# @return       (bool, object) - (Escape call status, CappedFpsArgs Object)
def get_set_cfps(gfx_index: str, cfps_args: args.CappedFpsArgs) -> (bool, args.CappedFpsArgs):
    # Get Adapter Info from GFX Adapter Details
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    return escape.get_set_cfps(adapter_info, cfps_args)


##
# @brief        Get or Set NN Scaling
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    get_set_nn_args - Pointer to structure NNArgs with NN Scaling info
# @return       (bool, object) - (Escape call status, NNArgs Object)
def get_set_nn_scaling(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], get_set_nn_args: args.NNArgs) -> (bool, args.NNArgs):
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.get_set_nn_scaling(display_and_adapter_info, get_set_nn_args)

##
# @brief        Get custom mode
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    get_custom_mode_args - Pointer to structure CustomModeArgs with Custom mode  info
# @return       (bool, object) - (Escape call status, CustomModeArgs Object)
def get_custom_mode(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], get_custom_mode_args: args.CustomModeArgs) -> (bool, args.CustomModeArgs):
    #Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.get_custom_mode(display_and_adapter_info, get_custom_mode_args)
##
# @brief        Add provided custom mode
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    hz_res - horizontal resolution of custom mode
# @param[in]    vt_res - vertical resolution of custom mode
# @return       bool - Escape call status
def add_custom_mode(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], hz_res: int, vt_res: int) -> bool:
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.add_custom_mode(display_and_adapter_info, hz_res, vt_res)


##
# @brief        Invoke Collage Functionality - IsCollagePossible, EnableCollage, ValidateCollage, DisableCollage
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    collage_mode_args - Pointer to Structure CollageModeArgs with collage mode args and operation
# @return       (bool, object) - (Escape call status, CollageModeArgs Object)
def invoke_collage(gfx_index: str, collage_mode_args: args.CollageModeArgs) -> (bool, args.CollageModeArgs):
    # Get Adapter Info from GFX Adapter Details
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    return escape.invoke_collage(adapter_info, collage_mode_args)


##
# @brief        To generate TDR
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    is_displaytdr - To specify VSYNC TDR or KMD TDR
# @return       bool - True or False on success and failure respectively
def generate_adapter_tdr(gfx_index: str, is_displaytdr: bool) -> bool:
    # Get Adapter Info from GFX Adapter Details
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    return escape.generate_adapter_tdr(adapter_info, is_displaytdr)


##
# @brief        Get or Set Custom Scaling
# @param[in]    display_and_adapter_info - Target ID or DisplayAndAdapterInfo Object
# @param[in]    get_set_custom_args - Pointer to structure CustomScalingArgs with Custom Scaling info
# @return       (bool, object) - (Escape call status, CustomScalingArgs object)
def get_set_custom_scaling(display_and_adapter_info: Union[DisplayAndAdapterInfo, int], get_set_custom_args: args.CustomScalingArgs) -> (bool, args.CustomScalingArgs):
    # Get DisplayAndAdapterInfo based on TargetID
    if type(display_and_adapter_info) is not DisplayAndAdapterInfo:
        display_and_adapter_info = display_config.DisplayConfiguration().get_display_and_adapter_info(
            display_and_adapter_info)
    return escape.get_set_custom_scaling(display_and_adapter_info, get_set_custom_args)


##
# @brief        Configure an Adapter's Power Component
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    enable - Boolean value to activate or idle power component
# @return       bool - Escape call status
def configure_adapter_power_component(gfx_index: str, enable: bool) -> any:
    DG_PLATFORMS = ["DG1", "DG2", "DG3", "ELG"]

    # Get Adapter Info from GFX Adapter Details
    adapter_info_dict = test_context.TestContext.get_gfx_adapter_details()
    adapter_info = adapter_info_dict[gfx_index]

    if len(adapter_info_dict) == 1 and (adapter_info.get_platform_info().PlatformName.upper() not in DG_PLATFORMS):
        return None

    # Skip configuring Power component if current adapter does not have LUID data
    if adapter_info.adapterLUID.LowPart == 0 and adapter_info.adapterLUID.HighPart == 0:
        return None
    return escape.configure_power_component(adapter_info, enable)


##
# @brief        get_set_display_pc_feature_state
# @param[in]    gfx_index - Graphic Adapter Index
# @param[in]    feature_args - Pointer to structure referring ComEscPowerConservationArgs
# @return       (bool, object) - (Escape call status, ComEscPowerConservationArgs object)
def get_set_display_pc_feature_state(gfx_index: str, feature_args: args.ComEscPowerConservationArgs) -> (bool, args.ComEscPowerConservationArgs):
    # Get Adapter Info from GFX Adapter Details
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    return escape.get_set_display_pc_feature_state(adapter_info, feature_args)


##
# @brief        Get/Set Genlock
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    enable enable or disable genlock
# @param[in]    genlock_args object of type DdCapiEscGetSetGenlockArgs containing filled-in genlock arguments.
# @return       returns True if escape operation successful, False otherwise.
def get_set_genlock(display_and_adapter_info: DisplayAndAdapterInfo, enable: bool, genlock_args: args.DdCapiEscGetSetGenlockArgs) -> bool:
    return escape.get_set_genlock(display_and_adapter_info, enable, genlock_args)


##
# @brief        Get/Set Genlock vblank timestamp
# @param[in]    display_and_adapter_info DisplayAndAdapterInfo
# @param[in]    genlock_args object of type DdCapiGetVblankTimestampForTarget containing filled-in genlock arguments.
# @return       returns True if escape operation successful, False otherwise.
def get_set_genlock_vblank_ts(display_and_adapter_info: DisplayAndAdapterInfo, genlock_args: args.DdCapiGetVblankTimestampForTarget):
    return escape.get_set_genlock_vblank_ts(display_and_adapter_info, genlock_args)
