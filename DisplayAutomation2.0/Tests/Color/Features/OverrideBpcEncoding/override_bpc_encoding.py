#################################################################################################
# @file         override_bpc_encoding.py
# @brief        This scripts comprises of below functions.
#               1.verify() - To perform register verification transcoder bpc and pixel encoding
# @author       Vimalesh D
#################################################################################################
from dataclasses import dataclass

from DisplayRegs.DisplayOffsets import ColorCtlOffsetsValues
from Libs.Core import system_utility
from Libs.Core.wrapper.driver_escape_args import IGCCSupportedBpc, IGCCSupportedEncoding,AviEncodingMode
from Tests.Color.Common.color_enums import ColorSpace, RgbQuantizationRange
from registers.mmioregister import MMIORegister
from Tests.Color.Common import hdr_utility, color_mmio_interface, common_utility, csc_utility, color_enums
from Tests.Color.Common.color_enums import ColorSpace, ConversionType
from Tests.Color.Verification import gen_verify_pipe, feature_basic_verify
from Libs.Feature.presi.presi_crc import start_plane_processing
from Libs.Core import system_utility
from Tests.Planes.Common import planes_helper


##
# @brief BpcEncoding supported by a Panel.Initialize with default bpc and encoding
@dataclass
class BpcEncoding:
    Bpc: str = "BPC8"
    Encoding: str = "RGB"
    DefaultBpc: str=""
    DefaultEncoding: str=""


##
# @brief         Wrapper to - verify the register for bpc and encoding
# @param[in]     platform - platform Info
# @param[in]     pipe - pipe_info
# @param[in]     plane - 1,2,3,4,5,6
# @param[in]     transcoder - 0,1,2,3,4
# @param[in]     bpc - 8,10,12
# @param[in]     encoding - RGB,YUV
# @param[in]     conv_type - Limited/Full
# @return        None
def verify(gfx_index: str, platform: str, pipe: str, plane: str, transcoder: str, expected_bpc: str,
           expected_encoding: str, conv_type=None, enable_regkey_dithering = False, is_lfp = False, is_igcl= False):
    sys_util = system_utility.SystemUtility()
    exec_env = sys_util.get_execution_environment_type()
    if exec_env == 'SIMENV_FULSIM' and planes_helper.get_flipq_status(gfx_index):
        start_plane_processing()
    mmio_interface = color_mmio_interface.ColorMmioInterface()

    if enable_regkey_dithering and is_lfp:
        if feature_basic_verify.verify_dithering_feature(gfx_index, platform, pipe, transcoder,
                                                         True) is False:
            return False
    if feature_basic_verify.verify_transcoder_bpc(gfx_index, platform, transcoder,
                                                  int(str(expected_bpc).split("BPC")[1])) is False:
        return False

    if hdr_utility.verify_pixel_encoding(gfx_index, platform, plane, pipe, AviEncodingMode[expected_encoding].value) \
            is False:
        return False
    
    # it was valid for both the cases but below was already covered in major commandlines and costly operation 
    # for refactor.
    if is_igcl is False:
        pipe_verification = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)

        ##
        # verify ocsc coeff and pre/post offsets
        color_ctl_offsets = pipe_verification.regs.get_color_ctrl_offsets(pipe)
        csc_mode_data = mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
        color_ctl_value = pipe_verification.regs.get_colorctl_info(pipe, ColorCtlOffsetsValues(CscMode=csc_mode_data))
        output_range = csc_utility.get_output_range(gfx_index, platform, 1,
                                                    pipe, transcoder, mmio_interface)

        if color_ctl_value.PipeOutputCscEnable:
            if conv_type is None:
                conv_type = ConversionType.FULL_TO_STUDIO if output_range == color_enums.RgbQuantizationRange.LIMITED.value else ConversionType.FULL_TO_FULL
            if "YCBCR" in expected_encoding:
                input = ColorSpace.RGB
                output = ColorSpace.YUV
            else:
                input = ColorSpace.RGB
                output = ColorSpace.RGB

            if pipe_verification.verify_output_csc_programming(pipe, int(str(expected_bpc).split("BPC")[1]), input,
                                                               output, conv_type) is False:
                return False
        elif not color_ctl_value.PipeOutputCscEnable and "YCBCR" in expected_encoding:
            return False

        return True
    return True
