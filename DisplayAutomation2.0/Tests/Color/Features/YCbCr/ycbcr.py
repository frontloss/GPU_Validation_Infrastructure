#################################################################################################
# @file         ycbcr.py
# @brief        This scripts comprises of below functions.
#               1.enable_disable_ycbcr() - enable/disable ycbcr feature
#               2.verify() - To perform register verification OCSC,Coeff,Pre/post off and quantisation range
# @author       Vimalesh D
#################################################################################################
import logging
from Libs.Core import enum
from Libs.Core import registry_access
from DisplayRegs.DisplayOffsets import ColorCtlOffsetsValues
from Libs.Core.display_config import display_config
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock
from Libs.Core.wrapper.driver_escape_args import ColorModel
from Tests.Color.Common import common_utility, color_escapes, color_mmio_interface
from Tests.Color.Verification import gen_verify_pipe
from Tests.Color.Verification import feature_basic_verify
from Tests.Color.Common.color_enums import ColorSpace, ConversionType, RgbQuantizationRange, YuvSampling, SamplingMode


##
# @brief         Wrapper to enable and disable the ycbcr for YUV444, YUV422, YUV420
# @param[in]     port  ConnectorNPortType of the display
# @param[in]     display_and_adapterinfo - adapter info
# @param[in]     enable - Boolean value to be either True or False
# @param[in]     sampling - enum type - YUV420,YUV422,YUV444
# @return        ycbcr_enable_status - True on Success, False otherwise
def enable_disable_ycbcr(port: str, display_and_adapterinfo, enable: bool, sampling: enum,color_model:int=ColorModel.COLOR_MODEL_YCBCR_PREFERRED.value) -> bool:
    ycbcr_enable_status = False

    if sampling == YuvSampling.YUV444:
        ycbcr_enable_status = color_escapes.configure_ycbcr(port, display_and_adapterinfo, enable,color_model)

    elif sampling == YuvSampling.YUV422:
        gfx_index = display_and_adapterinfo.adapterInfo.gfxIndex
        if common_utility.write_registry(gfx_index=gfx_index, reg_name="ForceApplyYUV422Mode",
                                         reg_datatype=registry_access.RegDataType.DWORD, driver_restart_required= True, reg_value=int(enable),
                                         display_and_adapterInfo=display_and_adapterinfo):
            ycbcr_enable_status = True

    elif sampling == YuvSampling.YUV420:
        ycbcr_enable_status = False
        sampling_mode_value = SamplingMode.YUV420.value if enable else SamplingMode.RGB.value
        logging.info("Applying modeset for the registry key to take effect")
        if common_utility.apply_mode(display_and_adapterinfo,sampling_mode=sampling_mode_value) is False:
            logging.error("Fail : Failed to apply modeset after write registry")
            return ycbcr_enable_status
        ycbcr_enable_status = True

    return ycbcr_enable_status


##
# @brief         Wrapper to perform - register verification - OCSC enable/disable, OCSC COEFF, PRE/POST
#                offset verification , avi info - quantisation range verification
# @param[in]    port_type  ConnectorNPortType of the display
# @param[in]     platform - platform Info
# @param[in]     display_and_adapter_info - display_and_adapter_info
# @param[in]     pipe - pipe_info
# @param[in]     plane - plane_info
# @param[in]     transcoder - transcoder info
# @param[in]     sampling - enum type - YUV420,YUV422,YUV444
# @param[in]     enable - bool True/False
# @param[in]     bpc - BPC 8,10,12
# @return        status - True on Success, False otherwise
def verify(port: str, platform: str, display_and_adapter_info: str, pipe: str, plane: str, transcoder: str,
           sampling: enum, enable: bool, bpc: int = 8,color_model: int = ColorModel.COLOR_MODEL_YCBCR_PREFERRED.value,conv_type = ConversionType.FULL_TO_STUDIO) -> bool:
    mmio_interface = color_mmio_interface.ColorMmioInterface()
    gfx_index = display_and_adapter_info.adapterInfo.gfxIndex
    current_mode = display_config.DisplayConfiguration().get_current_mode(display_and_adapter_info)

    if (sampling.name in "YUV420") and (SamplingMode.RGB.value == current_mode.samplingMode.Value):
        logging.info("Skip the verification as Current Mode is RGB")
        return True

    ##
    # Verify ycbcr,output csc enable/disable
    if feature_basic_verify.verify_ycbcr_feature(gfx_index, platform, pipe, enable, sampling) is False:
        return False

    pipe_verification = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)

    ##
    # verify ocsc oceff and pre/post offsets
    color_ctl_offsets = pipe_verification.regs.get_color_ctrl_offsets(pipe)
    csc_mode_data = mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
    color_ctl_value = pipe_verification.regs.get_colorctl_info(pipe, ColorCtlOffsetsValues(CscMode=csc_mode_data))

    if color_ctl_value.PipeOutputCscEnable:
        if enable:
            input = ColorSpace.RGB
            output = ColorSpace.YUV
        else:
            input = ColorSpace.RGB
            output = ColorSpace.RGB

        if pipe_verification.verify_output_csc_programming(pipe, bpc, input, output, conv_type,color_model) is False:
            return False
    ##
    # In case of Ycbcr disable, should not perform quantisation range verification due to default range issue.
    if enable:
        ##
        # Verify the quantization range
        if "HDMI" in port:
            quantisation_range = RgbQuantizationRange
            hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
            hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, port)
            hdmi_2_1_status = hf_vsdb_parser.is_frl_enable
            # WA till HDMI2.1 Quantization Issue resolve HSD-16018765098
            if hdmi_2_1_status is False:
                status, avi_info = color_escapes.get_quantization_range(port, display_and_adapter_info)

                expected_range = avi_info.AVIInfoFrame.QuantRange
                if expected_range == quantisation_range.DEFAULT.value:
                    expected_range = quantisation_range.LIMITED.value

                if pipe_verification.verify_quantization_range(transcoder, plane, pipe, expected_range) is False:
                    return False

    return True
