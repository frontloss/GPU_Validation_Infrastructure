#################################################################################################
# @file         quantization.py
# @brief        This scripts comprises of below functions.
#               1.verify() - To perform register verification OCSC,Coeff,Pre/post off and quantization range
# @author       Vimalesh D
#################################################################################################
from DisplayRegs.DisplayOffsets import ColorCtlOffsetsValues
from Tests.Color.Common import color_mmio_interface
from Tests.Color.Common.color_enums import ColorSpace, ConversionType
from Tests.Color.Verification import gen_verify_pipe


##
# @brief         Wrapper to perform - register verification - OCSC enable/disable, OCSC COEFF, PRE/POST
#                offset verification , avi info - quantization range verification
# @param[in]     gfx_index - gfx_0 or gfx_1
# @param[in]     platform - platform Info
# @param[in]     pipe - pipe_info
# @param[in]     plane - plane_info
# @param[in]     transcoder - transcoder info
# @param[in]     bpc - bpc - [10,12]
# @param[in]     conv_type - conv_type - STUDIO_TO_STUDIO,FULL_TO_STUDIO,STUDIO_TO_FULL,FULL_TO_FULL
# @param[in]     expected_range - Expected_range LIMITED, FULL
# @return        status - True on Success, False otherwise
def verify(gfx_index: str, platform: str, pipe: str, plane: str, transcoder: str, bpc: int, conv_type: ConversionType,
           expected_range: int):
    mmio_interface = color_mmio_interface.ColorMmioInterface()
    pipe_verification = gen_verify_pipe.get_pipe_verifier_instance(platform, gfx_index)

    ##
    # Verify the quantization range
    if pipe_verification.verify_quantization_range(transcoder, plane, pipe, expected_range) is False:
        return False

    color_ctl_offsets = pipe_verification.regs.get_color_ctrl_offsets(pipe)
    csc_mode_data = mmio_interface.read(gfx_index, color_ctl_offsets.CscMode)
    color_ctl_value = pipe_verification.regs.get_colorctl_info(pipe, ColorCtlOffsetsValues(CscMode=csc_mode_data))

    if color_ctl_value.PipeOutputCscEnable:
        if pipe_verification.verify_output_csc_programming(pipe, bpc, ColorSpace.RGB, ColorSpace.RGB,
                                                           conv_type) is False:
            return False
    return True
