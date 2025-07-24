##
# @file     elg_clock_hdmi.py
# @brief    Python class to validate HDMI DPLL divider values are programmed correctly
# @author   Nainesh P, Doriwala

import logging

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen14.Pipe import Gen14PipeRegs
from DisplayRegs.Gen14.Transcoder import Gen14TranscoderRegs
from Libs.Feature.clock import clock_helper
from Libs.Feature.display_engine.de_base import display_base


##
# @brief    This class is the base class for ELG HDMI Clock Verifications
# @details  Has bspec Clock Values defined and functions to verify HDMI Clock PLL
class ElgClockHdmi:
    colorFormatDictionary = dict([('RGB_8', 1), ('RGB_10', 1.25), ('RGB_12', 1.5),
                                  ('YUV420_8', 0.5), ('YUV420_10', 0.625), ('YUV420_12', 0.75)])

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
    # @param[in]    port_name - Port to verify
    # @param[in]    gfx_index - Adapter to verify
    # @return       symbol_freq - Symbol Frequency in MHz
    def calculate_symbol_freq(self, port_name: str, gfx_index: str) -> float:
        self.symbol_freq = 0
        _clock_helper = clock_helper.ClockHelper()
        disp_base = display_base.DisplayBase(port_name)
        pipe, ddi = disp_base.GetPipeDDIAttachedToPort(port_name, gfx_index=gfx_index)
        pipe = pipe.split('_')[-1].upper()
        logging.info("INFO : {0} ENABLED on PIPE{1}".format(port_name, pipe))

        if pipe == 'A':
            offset = Gen14TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_A
            offset2 = Gen14PipeRegs.OFFSET_PIPE_MISC.PIPE_MISC_A
        elif pipe == 'B':
            offset = Gen14TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_B
            offset2 = Gen14PipeRegs.OFFSET_PIPE_MISC.PIPE_MISC_B
        elif pipe == 'C':
            offset = Gen14TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_C
            offset2 = Gen14PipeRegs.OFFSET_PIPE_MISC.PIPE_MISC_C
        elif pipe == 'D':
            offset = Gen14TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_D
            offset2 = Gen14PipeRegs.OFFSET_PIPE_MISC.PIPE_MISC_D
        else:
            logging.error("Invalid Pipe assigned: {}".format(pipe))
            return self.symbol_freq

        value = DisplayArgs.read_register(offset, gfx_index)
        reg_value = Gen14TranscoderRegs.REG_TRANS_DDI_FUNC_CTL(offset, value)
        bit_per_color_value = reg_value.BitsPerColor
        mapped_bit_per_color = (_clock_helper.map_reg_value_to_dict(bit_per_color_value, self.bit_per_color,
                                                                    "Bits Per Color"))

        value = DisplayArgs.read_register(offset2, gfx_index)
        reg_value = Gen14PipeRegs.REG_PIPE_MISC(offset2, value)
        color_format_value = reg_value.Yuv420Enable
        mapped_color_format_value = (_clock_helper.map_reg_value_to_dict(color_format_value, self.color_format,
                                                                         'Color Format')) + '_' + str(
            mapped_bit_per_color)

        color_divider = list(self.colorFormatDictionary.values())[
            list(self.colorFormatDictionary).index(mapped_color_format_value)]

        pixel_rate = _clock_helper.get_pixel_rate(port_name, gfx_index)
        self.symbol_freq = (pixel_rate * color_divider)
        logging.info(
            "INFO : Symbol Frequency = {0} MHz Pixel Rate = {1} MHz".format(str(self.symbol_freq), (str(pixel_rate))))
        return self.symbol_freq
