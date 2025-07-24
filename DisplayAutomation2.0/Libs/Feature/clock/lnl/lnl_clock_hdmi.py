##
# @file     lnl_clock_hdmi.py
# @brief    LNL port clock validation base class for HDMI
# @details  Defines methods to verify if HDMI DPLL divider values are programmed correctly
# @author   Kiran Kumar Lakshmanan


import logging

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen15.Pipe import Gen15PipeRegs
from DisplayRegs.Gen15.Transcoder import Gen15TranscoderRegs
from Libs.Feature.clock import clock_helper
from Libs.Feature.display_engine.de_base import display_base


##
# @brief        This class is the base class for LNL HDMI Clock Verifications
# @details      Has bspec Clock Values defined and functions to verify HDMI Clock PLL
class LnlClockHdmi():
    colorFormatDictionary = dict([('RGB_8', 1), ('RGB_10', 1.25),
                                  ('RGB_12', 1.5), ('YUV420_8', 0.5),
                                  ('YUV420_10', 0.625), ('YUV420_12', 0.75)])
    # Map of bit per color
    bit_per_color = dict([
        (8, 0),
        (10, 1),
        (6, 2),
        (12, 3)
    ])
    # Map of color format
    color_format = dict([
        ('RGB', 0),
        ('YUV420', 1)
    ])

    symbol_freq = 0

    ##
    # @brief        Function to find the Symbol Frequency for HDMI
    # @param[in]    port_name - Port name to verify
    # @param[in]    gfx_index - Graphics Adapter to verify
    # @return       int - Symbol Frequency in MHz
    def calculate_symbol_freq(self, gfx_index: str, port_name: str) -> int:
        clock_helper_ = clock_helper.ClockHelper()
        disp_base = display_base.DisplayBase(port_name)
        pipe, ddi = disp_base.GetPipeDDIAttachedToPort(port_name, gfx_index=gfx_index)
        pipe = pipe.split('_')[-1].upper()
        logging.info(f"INFO : {port_name} ENABLED on PIPE{pipe}")

        if pipe == 'A':
            offset = Gen15TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_A
            offset2 = Gen15PipeRegs.OFFSET_PIPE_MISC.PIPE_MISC_A
        elif pipe == 'B':
            offset = Gen15TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_B
            offset2 = Gen15PipeRegs.OFFSET_PIPE_MISC.PIPE_MISC_B
        elif pipe == 'C':
            offset = Gen15TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_C
            offset2 = Gen15PipeRegs.OFFSET_PIPE_MISC.PIPE_MISC_C
        elif pipe == 'D':
            offset = Gen15TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_D
            offset2 = Gen15PipeRegs.OFFSET_PIPE_MISC.PIPE_MISC_D
        else:
            offset, offset2 = 0, 0
            logging.error(f"Invalid Pipe assigned: {pipe}")

        value = DisplayArgs.read_register(offset, gfx_index)
        reg_value = Gen15TranscoderRegs.REG_TRANS_DDI_FUNC_CTL(offset, value)
        bit_per_color_value = reg_value.BitsPerColor
        mapped_bit_per_color = (clock_helper_.map_reg_value_to_dict(bit_per_color_value, self.bit_per_color,
                                                                    "Bits Per Color"))

        value = DisplayArgs.read_register(offset2, gfx_index)
        reg_value = Gen15PipeRegs.REG_PIPE_MISC(offset2, value)
        color_format_value = reg_value.Yuv420Enable
        mapped_color_format_value = (clock_helper_.map_reg_value_to_dict(
            color_format_value, self.color_format, 'Color Format')) + '_' + str(mapped_bit_per_color)

        color_divider = list(self.colorFormatDictionary.values())[
            list(self.colorFormatDictionary).index(mapped_color_format_value)]

        pixel_rate = clock_helper_.get_pixel_rate(port_name, gfx_index)
        self.symbol_freq = (pixel_rate * color_divider)
        logging.info(f"INFO : Symbol Frequency = {str(self.symbol_freq)} MHz Pixel Rate = {str(pixel_rate)} MHz")
        return self.symbol_freq
