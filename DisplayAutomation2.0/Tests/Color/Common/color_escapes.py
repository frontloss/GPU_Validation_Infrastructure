######################################################################################################
# @file         color_escapes.py
# @brief        Contains APIs which interfaces between the test and the driver_escape wrapper/ OS interfaces.
#               These interfaces receive the input parameters from the test and invokes the driver escape call.
#               The functions processes the return status of the escape call, log the information along with GDHM logging
#               and return the status to the tests.
#               In functions like configure_aviinfo, configure_dpp_hw_lut, after the SET operation,
#               GET operation is performed to verify if the parameters are programmed correctly even before register level verification is performed.
#               Interfacing functions are :
#               1. ycbcr_support
#               2. configure_ycbcr
#               3. configure_pipe_csc
#               4. configure_hdr
#               5. configure_als_aggressiveness_level
#               6. get_quantization_range
#               7. configure_aviinfo
#               8. configure_dpp_hw_lut
#               Note : All the escape calls are those supported on Yangra.
# @author       Vimalesh D
######################################################################################################
import ctypes
import itertools
import time
import logging
from copy import deepcopy

from Libs.Core import enum, registry_access
from Libs.Core import driver_escape
from Libs.Core.display_config import display_config
from Libs.Core.wrapper.control_api_args import *
from Libs.Core.wrapper.driver_escape_args import CuiDeepColorInfo, IgccEscOverrideOperation, IGCCSupportedBpc, \
    IGCCSupportedEncoding, CuiEscOperationType, LinearCscOperation, ColorModel, Color3DLUTStatus
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Libs.Core.test_env.context import GfxDriverType
from Libs.Core.logger import gdhm
from Tests.Color.Common import color_enums, common_utility, color_constants
from Tests.Color.Common.color_enums import RgbQuantizationRange, CscMatrixType
from Tests.Color.Common.csc_utility import create_15_16_format_csc_matrix
from Tests.Color.Common.common_utility import gdhm_report_app_color


ESCAPE_PARAM_DICT = {True: "Enable", False: "Disable"}


##
# @brief        Checks if YCbCr is supported by the display
# @param[in]    port_name  ConnectorNPortType of the display
# @param[in]    display_and_adapter_info  DisplayAndAdapterInfo Struct of the display
# @return       status - Returns True if YcbCr is supported else False
def ycbcr_support(port_name: str, display_and_adapter_info: DisplayAndAdapterInfo) -> bool:
    status = False
    platform_name = display_and_adapter_info.adapterInfo.get_platform_info().PlatformName.upper()
    if platform_name in color_constants.PRE_GEN_13_PLATFORMS:
        if driver_escape.is_ycbcr_supported(display_and_adapter_info):
            status = True
            logging.info("YCbCr is supported on {0} : {1}".format
                         (display_and_adapter_info.adapterInfo.gfxIndex, port_name))
        else:
            logging.info("YCbCr is not supported on {0} : {1}".format
                         (display_and_adapter_info.adapterInfo.gfxIndex, port_name))
    elif platform_name in color_constants.POST_GEN_12_PLATFORMS:
        #Mark status to true for phase1 - otherwise for YUV444 mode it won't call the mmio verification.
        #Post removal of YUV444 mode in phase2 check-in VSDI-28243.need to update logic as mode will get removed.
        status = True
    return status


##
# @brief        Enables and disables YCbCr
# @param[in]    port_name  ConnectorNPortType of the display
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    enable - Boolean value to either enable or disable YCbCr
# @return       status - True on Success, False otherwise
def configure_ycbcr(port_name: str, display_and_adapter_info: DisplayAndAdapterInfo, enable: bool, color_model: int = ColorModel.COLOR_MODEL_YCBCR_PREFERRED.value) -> bool:
    status = False
    if driver_escape.configure_ycbcr(display_and_adapter_info, enable, color_model):
        status = True
        logging.info("Driver escape call to {0} YCbCr on {1} : {2} is successful".format(
            ESCAPE_PARAM_DICT[enable], display_and_adapter_info.adapterInfo.gfxIndex,
            port_name))
    else:
        title = "Driver escape call to {0} YCbCr on {1} : {2} failed".format(
            ESCAPE_PARAM_DICT[enable], display_and_adapter_info.adapterInfo.gfxIndex,
            port_name)
        logging.error("FAIL :" + title)
        common_utility.gdhm_report_app_color(title=title)
    return status


##
# @brief        Apply Linear or Non-Linear CSC
# @param[in]    port_name  ConnectorNPortType of the display
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    csc_matrix_type - Linear or Non-Linear CSC
# @param[in]    coefficients - will contain CSC Matrix
# @param[in]    enable - True or False
# @param[in]    matrix_name - None if valid matrix to set , matrix_name if invalid
# @return       status - True on Success, False otherwise
def configure_pipe_csc(port_name: str, display_and_adapter_info: DisplayAndAdapterInfo, csc_matrix_type: int,
                       coefficients: list, enable: bool, matrix_name=None) -> bool:
    from Libs.Core.wrapper.driver_escape_args import CSCPipeMatrixParams
    status = False
    csc_operation = LinearCscOperation.SET.value
    csc_params = create_15_16_format_csc_matrix(deepcopy(coefficients))
    params = CSCPipeMatrixParams(enable, csc_params)
    # Should disable HDR before configuring for Linear Csc
    if CscMatrixType.LINEAR_CSC.value == csc_matrix_type:
        logging.info("Verify the HDR Registry key status before configuring Linear CSC")
        reg_read_status, reg_value = common_utility.read_registry(gfx_index="GFX_0", reg_name="ForceHDRMode")
        if reg_value:
            logging.info("ForceHDR Mode registry key was enabled.Need to disable it to configure Linear CSC")
            if common_utility.write_registry(gfx_index="GFX_0", reg_name="ForceHDRMode",
                                             reg_datatype=registry_access.RegDataType.DWORD, reg_value=0,
                                             driver_restart_required=True) is False:
                logging.error("Registry key add to disable ForceHDRMode failed")
                return reg_read_status
            logging.info("Registry key add to disable ForceHDRMode is successful and test proceeds to configure "
                         "Linear CSC")
        else:
            logging.info("ForceHDRMode Registry key is either not preset or not enabled")
    if driver_escape.apply_csc(display_and_adapter_info, csc_operation, csc_matrix_type, params):
        status = True
        if matrix_name is not None:
            title = "Driver escape call to apply {0} {1} on {2} : {3} passed".format(
                CscMatrixType(csc_matrix_type).name, matrix_name, display_and_adapter_info.adapterInfo.gfxIndex,
                port_name)
            logging.error("FAIL :" + title)
            common_utility.gdhm_report_app_color(title=title)
        else:
            logging.info("Driver escape call to apply {0} on {1} : {2} is successful".format(
                CscMatrixType(csc_matrix_type).name, display_and_adapter_info.adapterInfo.gfxIndex,
                port_name))

    else:
        status = False
        if matrix_name is None:
            title = "Driver escape call to apply {0} on {1} : {2} failed".format(
                CscMatrixType(csc_matrix_type).name, display_and_adapter_info.adapterInfo.gfxIndex,
                port_name)
            logging.error("FAIL :" + title)
            common_utility.gdhm_report_app_color(title=title)
        else:
            logging.info("Driver escape call to apply {0} on {1} : {2} is successful".format(
                CscMatrixType(csc_matrix_type).name, display_and_adapter_info.adapterInfo.gfxIndex,
                port_name))
    return status


##
# @brief        Enable or Disable LACE based on the aggressiveness level and lux values
# @param[in]    port_name  ConnectorNPortType of the display
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    lux - lux value
# @param[in]    lux_operation - whether to perform lux operation or not
# @param[in]    aggressiveness_level - between 0-2 (LOW-MEDIUM-HIGH) values
# @param[in]    aggressiveness_operation - whether to perform aggressiveness operation or not
# @return       status - True on Success, False otherwise
def configure_als_aggressiveness_level(port_name: str, display_and_adapter_info: DisplayAndAdapterInfo, lux: int = 0,
                                       lux_operation: bool = False, aggressiveness_level: int = 0,
                                       aggressiveness_operation: bool = False) -> bool:
    status = False
    target_id = display_and_adapter_info.TargetID
    logging.info(" Lux Operation : {0} AggrLevel operation : {1}".format(lux_operation, aggressiveness_operation))
    if driver_escape.als_aggressiveness_level_override(target_id, lux, lux_operation, aggressiveness_level,
                                                       aggressiveness_operation):
        logging.info("Driver escape call for applying AlsLux :{0} AggrLevel : {1} on {2} :{3} is successful"
                     .format(lux, aggressiveness_level, display_and_adapter_info.adapterInfo.gfxIndex, port_name))
        status = True
    else:
        title = "Driver escape call for applying AlsLux :{0} AggrLevel : {1} on " \
                "{2} :{3} failed".format(lux, aggressiveness_level,
                                         display_and_adapter_info.adapterInfo.gfxIndex, port_name)
        logging.error("FAIL :" + title)
        common_utility.gdhm_report_app_color(title=title)
    return status


##
# @brief        Enables or Disables HDR
# @param[in]    port_name  ConnectorNPortType of the display
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    enable - Boolean value to either enable or disable
# @param[in]    feature - str value of the feature to be enabled, be default will be HDR, can also be used for WCG
# @return       status - True on Success, False otherwise
def configure_hdr(port_name: str, display_and_adapter_info: DisplayAndAdapterInfo, enable: bool,
                  feature: str = 'HDR') -> bool:
    from Libs.Core.display_config.display_config_enums import HDRErrorCode
    from Libs.Core.wrapper import os_interfaces as os_interfaces_dll

    status = False
    ERROR_SUCCESS = 0
    hdr_error_code = os_interfaces_dll.configure_hdr(display_and_adapter_info, enable)
    if hdr_error_code == HDRErrorCode(ERROR_SUCCESS).value:
        logging.info("OS API call for {0} {1} on {2} : {3} is successful".format(feature,
            ESCAPE_PARAM_DICT[enable], display_and_adapter_info.adapterInfo.gfxIndex,
            port_name))
        status = True
    else:
        title = "OS API call for {0} {1} on {2} : {3} failed".format(feature,
            ESCAPE_PARAM_DICT[enable], display_and_adapter_info.adapterInfo.gfxIndex,
            port_name)
        logging.error("FAIL : " + title)
    return status


##
# @brief        To get or set quantization range
# @param[in]    port_name  ConnectorNPortType of the display
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @return       status and avi_info - True on Success, False otherwise and avi_info
def get_quantization_range(port_name: str, display_and_adapter_info: DisplayAndAdapterInfo):
    from Libs.Core.wrapper.driver_escape_args import AviInfoFrameArgs, AviInfoOperation
    avi_info = AviInfoFrameArgs()
    # GET custom_avi_infoframe_args
    avi_info.TargetID = display_and_adapter_info.TargetID
    avi_info.Operation = AviInfoOperation.GET.value
    status, avi_info = driver_escape.get_set_quantisation_range(display_and_adapter_info.TargetID, avi_info)
    if status:
        logging.info("Driver escape call to GET AviInfo on {0} : {1} is successful"
                     .format(display_and_adapter_info.adapterInfo.gfxIndex, port_name))

    else:
        title = "Driver escape call to GET AviInfo on {0} : {1} failed".format(
            display_and_adapter_info.adapterInfo.gfxIndex, port_name)
        logging.error("FAIL : " + title)
        common_utility.gdhm_report_app_color(title=title)
    return status, avi_info


##
# @brief        To get or set quantization range
# @param[in]    port_name  ConnectorNPortType of the display
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    quantization_range - DEFAULT or LIMITED or FULL
# @return       status - True on Success, False otherwise
def configure_aviinfo(port_name: str, display_and_adapter_info: DisplayAndAdapterInfo,
                      quantization_range: RgbQuantizationRange) -> bool:
    from Libs.Core.wrapper.driver_escape_args import AviInfoFrameArgs, AviInfoOperation

    AVIFRAME_INFO_QUANTIZATION_RANGE_MASK = 0x0000FFFF
    status, avi_info = get_quantization_range(port_name, display_and_adapter_info)
    if status:
        ##
        # SET Quantization range
        avi_info.AVIInfoFrame.QuantRange = quantization_range
        avi_info.Operation = AviInfoOperation.SET.value
        status, avi_info = driver_escape.get_set_quantisation_range(
            display_and_adapter_info, avi_info)

        if status:
            logging.info("Driver escape call to SET Quant Range {0} on {1} : {2} is successful".format(
                RgbQuantizationRange(quantization_range).name,
                display_and_adapter_info.adapterInfo.gfxIndex, port_name))
            if quantization_range == color_enums.RgbQuantizationRange.DEFAULT.value:
                return True
            ##
            # Verify quantization range through escape
            # GET custom_avi_infoframe_args
            status, avi_info_2 = get_quantization_range(port_name, display_and_adapter_info)
            if status:
                # Below if check need to modified to edid based will take care once driver end fix proposed
                # but currently not planned for long term fix.
                if avi_info_2.AVIInfoFrame.QuantRange not in [color_enums.RgbQuantizationRange.DEFAULT.value,
                                                              color_enums.RgbQuantizationRange.FULL.value,
                                                              color_enums.RgbQuantizationRange.LIMITED.value]:
                    # For HDMI EDID having YCC Quantization range -> Both No Video Data and YQ
                    # For HDMI EDID having RGB Quantization range -> For RGB Q
                    # Suggested to have below WA to mask the MaskQuantizationRange
                    # Driver is handling the QuantRange (32 bit uint variable) in the following format:
                    # Bits [31 - 16] - Represent the Display Qunatization Caps reported from the EDID
                    # Bits [15 - 0] - Represent the Quantization Range
                    avi_info_2.AVIInfoFrame.QuantRange  = avi_info_2.AVIInfoFrame.QuantRange & AVIFRAME_INFO_QUANTIZATION_RANGE_MASK

                if avi_info.AVIInfoFrame.QuantRange != avi_info_2.AVIInfoFrame.QuantRange:
                    title = " QuantRange mismatch in GET post SET escape call " \
                            "Expected : {0} Actual: {1} on {2} : {3}".format(
                        RgbQuantizationRange(avi_info.AVIInfoFrame.QuantRange).name,
                        RgbQuantizationRange(avi_info_2.AVIInfoFrame.QuantRange).name,
                        display_and_adapter_info.adapterInfo.gfxIndex, port_name)
                    logging.error("FAIL " + title)
                    common_utility.gdhm_report_app_color(title=title)
                    return status
                logging.debug("Verification of quantisation range with get escape call, post set escape call "
                              "is successful")
                status = True
        else:
            title = "Driver escape call to SET Quant Range {0} on {1} : {2} failed".format(
                RgbQuantizationRange(quantization_range).name,
                display_and_adapter_info.adapterInfo.gfxIndex, port_name)
            logging.error("FAIL : " + title)
            common_utility.gdhm_report_app_color(title=title)

    return status


##
# @brief        Gets and Set the hardware LUT info
# @param[in]    port_name  ConnectorNPortType of the display
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    bin_file_path - CustomLUT bin path for r,g,b
# @param[in]    enable - True or False to enable HW_3D_LUT
# @return       status - True on Success, False otherwise
def configure_dpp_hw_lut(port_name: str, display_and_adapter_info: DisplayAndAdapterInfo, bin_file_path: str,
                         enable: bool) -> bool:
    from Libs.Core.wrapper.driver_escape_args import DppHwLutInfo, DppHwLutOperation

    status = False
    target_id = display_and_adapter_info.TargetID
    gfx_index = display_and_adapter_info.adapterInfo.gfxIndex
    cui_dpp_hw_lut_info_1 = DppHwLutInfo(target_id, DppHwLutOperation.UNKNOWN.value, 0)

    if enable:
        cui_dpp_hw_lut_info_1.opType = DppHwLutOperation.APPLY_LUT.value
    else:
        cui_dpp_hw_lut_info_1.opType = DppHwLutOperation.DISABLE_LUT.value

    if cui_dpp_hw_lut_info_1.convert_lut_data(bin_file_path) is False:
        logging.error("Invalid bin file path provided : %s " % bin_file_path)
        return status

    ##
    # Set the DPP Hw LUT Info
    if driver_escape.set_dpp_hw_lut(gfx_index, cui_dpp_hw_lut_info_1) is True:
        logging.info("Driver escape call to SET DPP Hw LUT with Bin : {0} on {1} : {2} is successful"
                     .format(bin_file_path, display_and_adapter_info.adapterInfo.gfxIndex, port_name))
        status = True
    else:
        title = "Driver escape call to SET DPP Hw LUT with Bin : {0} on {1} : {2} failed with {3} status".format(
            bin_file_path, display_and_adapter_info.adapterInfo.gfxIndex, port_name,
            Color3DLUTStatus(cui_dpp_hw_lut_info_1.status).name)
        logging.error("FAIL : " + title)
        common_utility.gdhm_report_app_color(title=title)

    return status


##
# Fetch DPCD_data from the required dpcd_address
def fetch_dpcd_data(dpcd_address, display_and_adapter_info):
    flag, dpcd_value = driver_escape.read_dpcd(display_and_adapter_info, dpcd_address)
    if flag is False:
        logging.error("Failed to read DPCD Address %s" % dpcd_address)
    logging.debug("DPCD Address %s : %s" % (hex(dpcd_address), dpcd_value[0]))
    return dpcd_value[0]


##
# @brief        Gets deep color info
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    platform_type  yangra or legacy platform
# @param[in]    feature  - Color/PowerCons
# @return       status - True on Success, False otherwise, combo_bpc_encoding_list
def get_bpc_encoding(displayAndAdapterInfo, platform_type: str, feature="Color"):
    # For both legacy and yangra same structure definition
    deep_color_info_obj = CuiDeepColorInfo()
    # @todo need to modify platform_type str to GfxDriverType
    if platform_type == GfxDriverType.YANGRA:
        deep_color_info_obj.opType = IgccEscOverrideOperation.GET.value
    else:
        deep_color_info_obj.opType = CuiEscOperationType.GET.value

    # Variable name mismatch between Color and PC displayAdapterInfo to get targetID
    if feature == "Color":
        deep_color_info_obj.display_id = displayAndAdapterInfo.TargetID
    else:
        deep_color_info_obj.display_id = displayAndAdapterInfo

    ##
    # Get escape call
    status, deep_color_info_obj = driver_escape.get_set_output_format(displayAndAdapterInfo, deep_color_info_obj)

    bpc_mask = int(deep_color_info_obj.supportedBpcMask)
    encoding_mask = int(deep_color_info_obj.supportedEncodingMask)

    bpc_mask_value_dict = {"BPCDEFAULT": 0, "BPC6": 0, "BPC8": 0, "BPC10": 0, "BPC12": 0}
    encoding_mask_value_dict = {"DEFAULT": 0, "RGB": 0, "YCBCR420": 0, "YCBCR422": 0, "YCBCR444": 0}

    ##
    # Get mask value from bits
    # Based on mask , set bit value to do set_call:
    bit_index = 0
    for bpc, bit_value in bpc_mask_value_dict.items():
        mask_value = common_utility.get_bit_value(bpc_mask, bit_index, bit_index)
        if mask_value == 1:
            bpc_mask_value_dict[bpc] = 1
        bit_index = bit_index + 1

    bit_index = 0
    for encoding, bit_value in encoding_mask_value_dict.items():
        mask_value = common_utility.get_bit_value(encoding_mask, bit_index, bit_index)
        if mask_value == 1:
            encoding_mask_value_dict[encoding] = 1
        bit_index = bit_index + 1

    bpc_mask_list = [i for i, j in bpc_mask_value_dict.items() if j == 1]
    encoding_mask_list = [i for i, j in encoding_mask_value_dict.items() if j == 1]

    combo_bpc_encoding_list = list(itertools.product(bpc_mask_list, encoding_mask_list))
    logging.info("Combo bpc_encoding pair list %s" % combo_bpc_encoding_list)

    return status, combo_bpc_encoding_list, IGCCSupportedBpc(
        deep_color_info_obj.overrideBpcValue).name, IGCCSupportedEncoding(
        deep_color_info_obj.overrideEncodingFormat).name


##
# @brief        Gets and Set deep color info
# @param[in]    display_and_adapter_info - DisplayAndAdapterInfo Struct of the display
# @param[in]    bpc  BPC 6,8,10,12
# @param[in]    encoding  RGB,YUB420,YUV444,YUV422
# @param[in]    platform_type  yangra or legacy platform
# @param[in]    feature  - Color/PowerCons
# @param[in]    is_lfp  True or False
# @return       status - True on Success, False otherwise
def set_bpc_encoding(displayAndAdapterInfo, bpc: str, encoding: str, platform_type: str, is_lfp: bool, feature="Color"):
    deep_color_info_obj = CuiDeepColorInfo()
    # @todo need to modify platform_type str to GfxDriverType
    if platform_type == GfxDriverType.YANGRA:
        deep_color_info_obj.opType = IgccEscOverrideOperation.GET.value
    else:
        deep_color_info_obj.opType = CuiEscOperationType.GET.value

    # Variable name mismatch between Color and PC displayAdapterInfo to get targetID
    if feature in ["Color", "ModeEnum"]:
        deep_color_info_obj.display_id = displayAndAdapterInfo.TargetID
    else:
        deep_color_info_obj.display_id = displayAndAdapterInfo

    ##
    # Get escape call
    status, deep_color_info_obj = driver_escape.get_set_output_format(displayAndAdapterInfo, deep_color_info_obj)

    if status:
        logging.info("Pass: BPC : {0} and Encoding : {1} get via escape call".format(bpc, encoding))
    else:
        gdhm.report_driver_bug_os("Escape call failed to Get BPC and Encoding")
        return status

    if platform_type == GfxDriverType.YANGRA:
        deep_color_info_obj.opType = IgccEscOverrideOperation.SET.value
    else:
        deep_color_info_obj.opType = CuiEscOperationType.SET.value
    deep_color_info_obj.overrideBpcValue = IGCCSupportedBpc[bpc].value
    deep_color_info_obj.overrideEncodingFormat = IGCCSupportedEncoding[encoding].value

    # Add delay to update the structure params
    time.sleep(5)

    ##
    # Set escape call
    status, deep_color_info_obj = driver_escape.get_set_output_format(displayAndAdapterInfo, deep_color_info_obj)

    if status:
        logging.info("Pass: BPC : {0} and Encoding : {1} set via escape call".format(bpc, encoding))
    else:
        gdhm.report_driver_bug_os("Escape call failed to Set BPC and Encoding".format(bpc, encoding))
        logging.error("Failed to set BPC and Encoding via escape call")
        return status

    ##
    # verify the bpc and encoding through escape
    if platform_type == GfxDriverType.YANGRA:
        deep_color_info_obj.opType = IgccEscOverrideOperation.GET.value
    else:
        deep_color_info_obj.opType = CuiEscOperationType.GET.value

    # RCR: VSRI-5011 - BPC change for lfp panel does not happen with a unplug-plug case as RecommendMonitorModes is not called and For
    # lfp we need to change the driver mode table and so we replicate same as how IGCC is responsible to do a QDC
    # and SDC call so that OS queries the mode table again and we can change with this below scenario

    display_config_ = display_config.DisplayConfiguration()
    get_config = display_config_.get_current_display_configuration()
    display_config_.set_display_configuration(get_config, add_force_mode_enum_flag = True)

    # Add delay to update the structure params.
    time.sleep(5)

    # Disabling below verification post set escape call for ModeEnum Tests. HSD: 18031834747
    if feature == "ModeEnum":
        return True

    # Get escape call
    status, deep_color_info_obj = driver_escape.get_set_output_format(displayAndAdapterInfo, deep_color_info_obj)

    if status:
        logging.info("Pass: BPC : {0} and Encoding : {1} get via escape call".format(bpc, encoding))
    else:
        gdhm.report_driver_bug_os("Failed to get BPC: {0} and Encoding: {1} via escape call".format(bpc, encoding))
        return status

    ##
    # Checking for BPC value
    if IGCCSupportedBpc(deep_color_info_obj.overrideBpcValue).name == bpc:
        logging.debug("Verification of bpc with get escape call, post set escape call "
                      "is successful")
    else:
        logging.error(
            "Verification of bpc with get escape call, post set escape call failed due to mismatch "
            "Expected BPC : {0} and Actual BPC: {1} ".format(bpc, IGCCSupportedBpc(deep_color_info_obj.overrideBpcValue).name))
        gdhm.report_driver_bug_os("Verification of BPC failed post set escape call")
        return status

    ##
    # Checking for Encoding value
    if IGCCSupportedEncoding(deep_color_info_obj.overrideEncodingFormat).name == encoding:
        logging.debug("Verification of encoding with get escape call, post set escape call "
                      "is successful")
    else:
        logging.error(
            "Verification of encoding with get escape call, post set escape call failed due to mismatch "
            "Expected encoding : {0} and Actual encoding: {1} ".format(encoding, IGCCSupportedEncoding(deep_color_info_obj.overrideEncodingFormat).name))
        gdhm.report_driver_bug_os("Verification of encoding failed post set escape call")
        return status

    return True
