#######################################################################################################################
# @file         pps_calculator.py
# @brief        Contains PictureParameterSetCalculator Which Acts as Base Class For the PPS Calculator like
#               DpPictureParameterSetCalculator, MipiPictureParameterSetCalculator
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import math
from abc import abstractmethod, ABC
from typing import List, Dict, Any

from Libs.Core.logger import gdhm
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_struct import DisplayTimings
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat
from Libs.Feature.vdsc import dsc_enum_constants as dsc_args
from Libs.Feature.vdsc.dsc_cfg_rc_range_params import RC_PARAM_ROW_INDEX, RC_PARAM_COL_INDEX, RC_PARAMETERS
from Libs.Feature.vdsc.dsc_definitions import DSCDisplay, DSCRequiredPictureParameterSet, RcRangeParameters
from Libs.Feature.vdsc.dsc_enum_constants import DSC_1P2_UNSUPPORTED_PLATFORMS
from Libs.Feature.vdsc.dsc_enum_constants import TestDataKey, DisplayType, AudioPacketType, AudioStandard, AudioLayout
from Libs.Feature.vdsc.dsc_helper import DSCHelper


##
# @brief        PictureParameterSetCalculator Contains Methods to Calculate the PPS Parameters, Some of Which are
#               Abstract Methods that Needs to be Implemented as per the Display Technology and also Based on Driver
#               Implementations. Those Parameter Calculations Which are Common Across all the Display Technology are
#               Implemented Here as per C-Model.
class PictureParameterSetCalculator(ABC):
    is_yuv_input: bool = False

    ##
    # @brief        Initialize the Member Variables.
    # @param[in]    display: DSCDisplay
    #                   Contains All the Information Related to the DSC Display Which are Required For PPS Calculation.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, display: DSCDisplay, test_data: Dict[TestDataKey, Any]) -> None:
        self.test_data: Dict[TestDataKey, Any] = test_data
        self._display: DSCDisplay = display

        # Parse the Data From the Test Script and Assign Default Value if Key is not Present
        color_format: ColorFormat = self.test_data.setdefault(TestDataKey.COLOR_FORMAT, ColorFormat.RGB)
        self.test_data.setdefault(TestDataKey.IS_AUDIO_SUPPORTED, True)
        self.test_data.setdefault(TestDataKey.AUDIO_RATE_HZ, 48000)
        self.test_data.setdefault(TestDataKey.AUDIO_PACKET_TYPE, AudioPacketType.THREE_DIMENSION_AUDIO_SAMPLE_PACKET)
        self.test_data.setdefault(TestDataKey.AUDIO_ALLOCATION_STANDARD, AudioStandard.ALLOCATION_STANDARD_THREE)
        self.test_data.setdefault(TestDataKey.AUDIO_LAYOUT, AudioLayout.LAYOUT_ZERO)

        PictureParameterSetCalculator.is_yuv_input = False if color_format == ColorFormat.RGB else True
        self._pic_parameter_set = DSCRequiredPictureParameterSet()
        self._is_big_joiner_enabled = False
        self._is_ultra_joiner_enabled = False

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns True if big joiner is enabled False otherwise
    @property
    def is_big_joiner_enabled(self):
        return self._is_big_joiner_enabled

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns True if ultra joiner is enabled False otherwise
    @property
    def is_ultra_joiner_enabled(self):
        return self._is_ultra_joiner_enabled

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns graphics index in which the display is plugged in small letters. E.g. gfx_0, gfx_1
    @property
    def gfx_index(self) -> str:
        return self._display.gfx_index

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns the Port Name on Which the Display is Plugged From Display Object.
    @property
    def port(self) -> str:
        return self._display.port_name

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns the Target Id of the Display From Display Object.
    @property
    def target_id(self) -> int:
        return self._display.target_id

    ##
    # @brief        Property to Access the Private Member Variable Outside of Class.
    # @return       Returns DSCRequiredPictureParameterSet object which contains all calculated pps values.
    @property
    def calculated_pic_parameter_set(self) -> DSCRequiredPictureParameterSet:
        return self._pic_parameter_set

    ##
    # @brief        Computed Property to Get the Display Timing Information of the Display For Which PictureParameterSet
    #               Has to be Calculated.
    # @return       display_timing: DisplayTimings
    #                   Returns the timing info at which the display is currently running.
    @property
    def timing_info(self) -> DisplayTimings:
        display_configuration = DisplayConfiguration()

        display_and_adapter_info = display_configuration.get_display_and_adapter_info(self.target_id)
        display_timing = DSCHelper.get_display_timing_from_qdc(display_and_adapter_info)
        logging.info('Pixel Rate: {}hz for Target Id: {}'.format(display_timing.targetPixelRate, self.target_id))

        if self._display.is_tiled_display is True:
            display_timing.targetPixelRate //= 2
            display_timing.hActive //= 2

        return display_timing

    ##
    # @brief    Big Joiner is Enabled Based on the No VDSC Engine that will be required to Drive the DSC Display.
    #           No of VDSC Engine Required is Determined Based on the Slice Count.
    # @return   None
    def _set_is_big_joiner_enabled(self) -> None:

        if self._pic_parameter_set.vdsc_instances >= 4:
            self._is_big_joiner_enabled = True

    ##
    # @brief    Ultra Joiner is Enabled Based on the No VDSC Engine that will be required to Drive the DSC Display.
    #           No of VDSC Engine Required is Determined Based on the Slice Count.
    # @return   None
    def _set_is_ultra_joiner_enabled(self) -> None:

        if self._pic_parameter_set.vdsc_instances == 8:
            self._is_ultra_joiner_enabled = True

    ##
    # @brief        Abstract method, to set the info frame header data
    # @return       None
    @abstractmethod
    def _set_info_frame_header(self) -> None:
        pass

    ##
    # @brief        Abstract Method, to Set DSC Minor and Major Version that Needs to be Implemented by the Sub Class
    #               According to its needs.
    # @return       None
    @abstractmethod
    def _set_dsc_major_minor_version(self) -> None:
        pass

    ##
    # @brief        Abstract Method, to Set Bits Per Component that Needs to be Implemented by the Sub Class According
    #               to its needs.
    # @return       None
    @abstractmethod
    def _set_bits_per_component(self) -> None:
        pass

    ##
    # @brief        Abstract Method, to Set Line Buffer Depth that Needs to be Implemented by the Sub Class According
    #               to its needs.
    # @return       None
    @abstractmethod
    def _set_line_buffer_depth(self) -> None:
        pass

    ##
    # @brief        Abstract Method, to Set Block Prediction Supported Status that Needs to be Implemented by the Sub
    #               Class According to its needs.
    # @return       None
    @abstractmethod
    def _set_is_block_prediction_enabled(self) -> None:
        pass

    ##
    # @brief        Abstract Method, to Set Color Format Supported that Needs to be Implemented by the Sub Class
    #               According to its needs.
    # @return       None
    @abstractmethod
    def _set_color_format_support(self) -> None:
        pass

    ##
    # @brief        Abstract Method, to Set Output Bpp that Needs to be Implemented by the Sub Class According to its
    #               needs.
    # @return       None
    @abstractmethod
    def _set_compression_bpp(self) -> None:
        pass

    ##
    # @brief        Abstract Method, to Set Slice Count that Needs to be Implemented by the Sub Class According to its
    #               needs.
    # @return       None
    @abstractmethod
    def _set_slice_count(self) -> None:
        pass

    ##
    # @brief        Abstract Method, to No of VDSC Instance that Needs to be Implemented by the Sub Class According
    #               to its needs.
    # @return       None
    @abstractmethod
    def _set_no_of_vdsc_instance(self) -> None:
        pass

    ##
    # @brief        Abstract Method, to Set DSC Enabled Status that Needs to be Implemented by the Sub Class According
    #               to its needs.
    # @return       None
    @abstractmethod
    def _set_is_dsc_enabled(self) -> None:
        pass

    ##
    # @brief        Private Member Function to Get the Chunk Size, Computed Using Slice Width and BPP
    # @return       chunk_size: int
    #                   Returns the Chunk Size that are used For Slice Multiplexing.
    def _get_chunk_size(self) -> int:
        is_chroma_sub_sampled = self._pic_parameter_set.native_422 or self._pic_parameter_set.native_420
        slice_width = self._pic_parameter_set.slice_width >> is_chroma_sub_sampled

        bpp: int = self._pic_parameter_set.bits_per_pixel.value
        chunk_size: int = int(math.ceil(slice_width * bpp / (8 * dsc_args.FIXED_POINT_U6_4_CONVERSION)))

        return chunk_size

    ##
    # @brief        Private Member Function to Get Final Offset, Computed as Per DSC Spec.
    # @parm[in]     num_extra_mux_bits: int
    #                   Number of bits that remain at the end of a slice due to sub-stream multiplexing
    # @return       final_offset: int
    #                   Specifies the Maximum End of Slice Value for rcXformOffset
    def _get_final_offset(self, num_extra_mux_bits: int) -> int:

        final_offset: int = (self._pic_parameter_set.initial_xmit_delay * self._pic_parameter_set.bits_per_pixel.value)
        final_offset = (final_offset + 8) // dsc_args.FIXED_POINT_U6_4_CONVERSION
        final_offset = self._pic_parameter_set.rc_model_size - final_offset + num_extra_mux_bits

        return final_offset

    ##
    # @brief        Private Member Function Get the Groups Per Line, Computed as Per DSC Spec.
    # @return       groups_per_line: int
    #                   Specifies Number of Group Used to Code Each Line of Slice.
    def _get_groups_per_line(self, pixels_per_group: int) -> int:

        is_chroma_sub_sampled = self._pic_parameter_set.native_422 or self._pic_parameter_set.native_420
        slice_width = self._pic_parameter_set.slice_width >> is_chroma_sub_sampled

        groups_per_line = (slice_width + pixels_per_group - 1) // pixels_per_group

        return groups_per_line

    ##
    # @brief        Private Member Function to Get the Groups Total, Computed as Per DSC Spec.
    # @param[in]    group_per_line: int
    #                   Specifies Number of Group Used to Code Each Line of Slice.
    # @return       groups_total: int
    #                   Specifies Number of Groups used to Code the Entire Slice.
    def _get_groups_total(self, group_per_line: int) -> int:
        groups_total: int = group_per_line * self._pic_parameter_set.slice_height

        return groups_total

    ##
    # @brief        Private Member Function Get the HRD Delay, Computed as Per DSC Spec.
    # @param[in]    groups_per_line: int
    #                   Specifies Number of Group Used to Code Each Line of Slice.
    # @return       hrd_delay: int
    #                   Specifies Total End-to-End Hypothetical Reference Decoder Delay
    def _get_hrd_delay(self, pixels_per_group, groups_per_line: int) -> int:
        bpp: int = self._pic_parameter_set.bits_per_pixel.value / dsc_args.FIXED_POINT_U6_4_CONVERSION
        min_rate_buffer_size: int = self._get_min_rate_buffer_size(pixels_per_group, groups_per_line)
        hrd_delay: int = int(math.ceil(min_rate_buffer_size / bpp))

        return hrd_delay

    ##
    # @brief        Private Member Function Get the Min Rate Buffer Size, Computed as Per DSC Spec.
    # @param[in]    groups_per_line: int
    #                   Specifies Number of Group Used to Code Each Line of Slice.
    # @return       min_rate_buffer_size: int
    #                   Specifies Min Rate Buffer Size Needed.
    def _get_min_rate_buffer_size(self, pixels_per_group: int, groups_per_line: int) -> int:

        is_chroma_sub_sampled = (self._pic_parameter_set.native_420 or self._pic_parameter_set.native_422)

        if (self._pic_parameter_set.dsc_version_minor == 2) and is_chroma_sub_sampled:
            group_count = int(math.ceil(self._pic_parameter_set.initial_xmit_delay / pixels_per_group))
            max_offset = self._get_offset(pixels_per_group, groups_per_line, group_count)
            max_offset = max(max_offset, self._get_offset(pixels_per_group, groups_per_line, groups_per_line))
            max_offset = max(max_offset, self._get_offset(pixels_per_group, groups_per_line, 2 * groups_per_line))
            min_rate_buffer_size = int(self._pic_parameter_set.rc_model_size - self._pic_parameter_set.initial_offset)
            min_rate_buffer_size = min_rate_buffer_size + max_offset
        else:
            bpp: int = self._pic_parameter_set.bits_per_pixel.value / dsc_args.FIXED_POINT_U6_4_CONVERSION
            min_rate_buffer_size: int = int(math.ceil(self._pic_parameter_set.initial_xmit_delay * bpp))
            min_rate_buffer_size += groups_per_line * self._pic_parameter_set.first_line_bpg_offset
            min_rate_buffer_size += self._pic_parameter_set.rc_model_size - self._pic_parameter_set.initial_offset

        return min_rate_buffer_size

    ##
    # @brief        Private Member function to compute offset value at a specific group
    # @param[in]    pixels_per_group: int
    #                   Number of Pixels Per group
    # @param[in]    groups_per_line: int
    #                   Number of Groups Per Line
    # @param[in]    group_count: int
    #                   Group to compute the offset for
    # return        offset: int
    #                   Offset Value for the group, group_count
    def _get_offset(self, pixels_per_group, groups_per_line: int, group_count: int) -> int:
        group_count_id = int(math.ceil(self._pic_parameter_set.initial_xmit_delay / pixels_per_group))
        bpp: int = self._pic_parameter_set.bits_per_pixel.value / dsc_args.FIXED_POINT_U6_4_CONVERSION

        if group_count <= group_count_id:
            offset = int(math.ceil(group_count * pixels_per_group * bpp))
        else:
            offset = int(math.ceil(group_count_id * pixels_per_group * bpp))
            offset = offset - (((group_count - group_count_id) * self._pic_parameter_set.slice_bpg_offset) >> 11)

        if group_count <= groups_per_line:
            offset = offset + (group_count * self._pic_parameter_set.first_line_bpg_offset)
        else:
            temp = ((group_count - groups_per_line) * self._pic_parameter_set.nfl_bpg_offset) >> 11
            offset = offset + (groups_per_line * self._pic_parameter_set.first_line_bpg_offset) - temp

        if self._pic_parameter_set.native_420:
            if group_count <= groups_per_line:
                offset = offset - ((group_count * self._pic_parameter_set.nsl_bpg_offset) >> 11)
            elif group_count <= 2 * groups_per_line:
                temp = (groups_per_line * self._pic_parameter_set.nsl_bpg_offset) >> 11
                temp = ((group_count - groups_per_line) * self._pic_parameter_set.second_line_bpg_offset) - temp
                offset = offset + temp
            else:
                temp = ((group_count - groups_per_line) * self._pic_parameter_set.nsl_bpg_offset) >> 11
                temp = ((group_count - groups_per_line) * self._pic_parameter_set.second_line_bpg_offset) - temp
                offset = offset + temp

        return offset

    ##
    # @brief        Private Member Function Get the Number of Extra Mux Bits, Computed as Per DSC Spec.
    # @return       num_extra_mux_bits: int
    #                   Specifies Number of Bits that Can Remain at the End of Slice Due to Sub-stream Multiplexing.
    def _get_num_extra_mux_bits(self, num_of_substream_processors: int) -> int:
        bpc: int = self._pic_parameter_set.bits_per_component
        num_extra_mux_bits: int

        if self._pic_parameter_set.convert_rgb == 1:
            num_extra_mux_bits = self._pic_parameter_set.mux_word_size + (4 * bpc + 4) - 2
            num_extra_mux_bits = num_of_substream_processors * num_extra_mux_bits
        elif self._pic_parameter_set.native_422 == 0:  # YCbCr Format
            num_extra_mux_bits = num_of_substream_processors * self._pic_parameter_set.mux_word_size
            num_extra_mux_bits = num_extra_mux_bits + (4 * bpc + 4) + 2 * (4 * bpc) - 2
        else:
            num_extra_mux_bits = num_of_substream_processors * self._pic_parameter_set.mux_word_size
            num_extra_mux_bits = num_extra_mux_bits + (4 * bpc + 4) + 3 * (4 * bpc) - 2

        slice_bits: int = self._get_slice_bits()
        while (num_extra_mux_bits > 0) and ((slice_bits - num_extra_mux_bits) % self._pic_parameter_set.mux_word_size):
            num_extra_mux_bits -= 1

        return num_extra_mux_bits

    ##
    # @brief        Private Member Function Get the Slice Bits, Computed as Per DSC Spec.
    # @return       slice_bits: int
    #                   Specifies Total Number of Bits Allocated For a Slice.
    def _get_slice_bits(self) -> int:
        slice_bits: int = 8 * self._pic_parameter_set.chunk_size * self._pic_parameter_set.slice_height

        return slice_bits

    ##
    # @brief        Private Member Function to Get the First Line BPG Offset, Computed as Per DSC Spec.
    # @param[in]    uncompressed_bpg_rate: int
    # @return       first_line_bpg_offset: int
    #                   Specifies Number of Additional Bits That are Allocated For Each Group on the First Line of Slice
    def _get_first_line_bpg_offset(self, uncompressed_bpg_rate: int) -> int:
        first_line_bpg_offset: int = self._pic_parameter_set.first_line_bpg_offset

        if first_line_bpg_offset < 0:
            lower_bound = 0
            bits_per_pixel = self._pic_parameter_set.bits_per_pixel.value
            upper_bound = uncompressed_bpg_rate * dsc_args.FIXED_POINT_U6_4_CONVERSION - (3 * bits_per_pixel)
            upper_bound = upper_bound // dsc_args.FIXED_POINT_U6_4_CONVERSION

            # As per DSC 1.1 Standard  12 Bpg for 8Bpp and 15Bpg for 12 Bpp. As per Dsc C Model 
            # FirstLineBpgOffset is obtained from slice height as given below. DSC Spec Calls out DSC Cmodel 
            # takes precedence over the DSC Standard.
            if self._pic_parameter_set.slice_height >= 8:
                first_line_bpg_offset = 12 + ((9 * min(34, (self._pic_parameter_set.slice_height - 8))) // 100)
            else:
                first_line_bpg_offset = 2 * (self._pic_parameter_set.slice_height - 1)

            # Limits the value between upper_bound and lower bound. Includes lower and upper bound value as well
            first_line_bpg_offset = min(upper_bound, max(lower_bound, first_line_bpg_offset))
                   
        return first_line_bpg_offset

    ##
    # @brief        Private Member function to get the Second Line BPG Offset, computed as Per DSC Spec.
    # @param[in]    uncompressed_bpg_rate: int
    # @return       second_line_bpg_offset: int
    #                   Specifies Number of Additional Bits That are Allocated For Each Group on the Second Line of
    #                   Slice. Applicable only for native 4:2:0 modes.
    def _get_second_line_bpg_offset(self, uncompressed_bpg_rate: int) -> int:
        second_line_bpg_offset: int = self._pic_parameter_set.second_line_bpg_offset

        if self._pic_parameter_set.dsc_version_minor == 1 or self._pic_parameter_set.native_420 == 0:
            return 0

        if second_line_bpg_offset < 0:
            lower_bound = 0
            bits_per_pixel = self._pic_parameter_set.bits_per_pixel.value
            upper_bound = uncompressed_bpg_rate * dsc_args.FIXED_POINT_U6_4_CONVERSION - (3 * bits_per_pixel)
            upper_bound = upper_bound // dsc_args.FIXED_POINT_U6_4_CONVERSION

            second_line_bpg_offset = 12 if self._pic_parameter_set.native_420 else 0

            # Limits the value between upper_bound and lower bound. Includes lower and upper bound value as well
            second_line_bpg_offset = min(upper_bound, max(lower_bound, second_line_bpg_offset))

        return second_line_bpg_offset

    ##
    # @brief        Private Member Function set the Initial Transmission Delay, Computed as Per DSC Spec.
    #               Specifies the Number of Pixel Times That the Encoder Waits Before Transmitting Data From its Rate
    #               Buffer
    def _set_initial_xmit_delay(self) -> None:
        bits_per_pixel = self._pic_parameter_set.bits_per_pixel.value

        initial_xmit_delay: float = self._pic_parameter_set.rc_model_size * 0.5 * dsc_args.FIXED_POINT_U6_4_CONVERSION
        initial_xmit_delay = initial_xmit_delay / bits_per_pixel
        initial_xmit_delay: int = int(initial_xmit_delay + 0.5)

        is_chroma_sub_sampled = self._pic_parameter_set.native_422 or self._pic_parameter_set.native_420
        if is_chroma_sub_sampled is True:
            slice_width = self._pic_parameter_set.slice_width / 2
        else:
            slice_width = self._pic_parameter_set.slice_width

        padding_pixels = 0 if slice_width % 3 == 0 else (3 - (slice_width % 3))
        padding_pixels = padding_pixels * (initial_xmit_delay / slice_width)

        multiplier = 4 if self._pic_parameter_set.native_422 == 1 else 3
        remainder = (self._pic_parameter_set.initial_xmit_delay + padding_pixels) % 3
        if (3 * bits_per_pixel) >= ((initial_xmit_delay + 2) / 3) * multiplier and (remainder == 1):
            initial_xmit_delay = initial_xmit_delay + 1

        self._pic_parameter_set.initial_xmit_delay = initial_xmit_delay

    ##
    # @brief        Private Member Function Get the Initial Decoding Delay, Computed as Per DSC Spec.
    # @param[in]    hrd_delay: int
    #                   Specifies Total End-to-End Hypothetical Reference Decoder Delay
    # @return       initial_dec_delay: int
    #                   Specifies the Number of Pixel Times That the Decoder Accumulates Data in its Rate Buffer Before
    #                   Starting to Decode and Output Pixels.
    def _get_initial_dec_delay(self, hrd_delay: int) -> int:
        initial_dec_delay: int = hrd_delay - self._pic_parameter_set.initial_xmit_delay

        return initial_dec_delay

    ##
    # @brief        Private Member Function Set the Initial offset, Computed as Per DSC Spec.
    # @return       None
    def _set_initial_offset(self) -> None:
        initial_offset: int = 0
        bits_per_pixel = self._pic_parameter_set.bits_per_pixel.value

        if self._pic_parameter_set.native_422 == 1:  # native 4:2:2
            if bits_per_pixel >= dsc_args.DSC_BPP_16:
                initial_offset = 2048

            elif bits_per_pixel >= dsc_args.DSC_BPP_14:
                # round(compressed bpp - 224) * (1792/16)) - Division by 16 is required as bpp is in u6.4 notation
                initial_offset = 5632 - int((bits_per_pixel - dsc_args.DSC_BPP_14) * 112 + 0.5)

            elif bits_per_pixel >= dsc_args.DSC_BPP_12:
                initial_offset = 5632

        else:  # 4:4:4 or simple 4:2:2 or native 4:2:0
            if bits_per_pixel >= dsc_args.DSC_BPP_12:
                initial_offset = 2048

            elif bits_per_pixel >= dsc_args.DSC_BPP_10:
                # round(compressed bpp - 160) * (1792/16)) - Division by 16 is required as bpp is in u6.4 notation
                initial_offset = 5632 - int((bits_per_pixel - dsc_args.DSC_BPP_10) * 112 + 0.5)

            elif bits_per_pixel >= dsc_args.DSC_BPP_8:
                # round(compressed bpp - 128) * (256/16)) - Division by 16 is required as bpp is in u6.4 notation
                initial_offset = 6144 - int((bits_per_pixel - dsc_args.DSC_BPP_8) * 16 + 0.5)

            elif bits_per_pixel >= dsc_args.DSC_BPP_6:
                initial_offset = 6144

        self._pic_parameter_set.initial_offset = initial_offset

    ##
    # @brief        Private Member Function Get the Initial SCale Value, Computed as Per DSC Spec.
    # @param[in]    groups_per_line: int
    #                   Specifies Number of Group Used to Code Each Line of Slice.
    # @return       initial_scale_value: int
    #                   Specifies the Initial rcXformScale Factor Value used at the Beginning of a Slice.
    def _get_initial_scale_value(self, groups_per_line: int) -> int:
        numerator: int = (8 * self._pic_parameter_set.rc_model_size)
        denominator: int = (self._pic_parameter_set.rc_model_size - self._pic_parameter_set.initial_offset)
        initial_scale_value = numerator // denominator

        if groups_per_line < (initial_scale_value - 8):
            initial_scale_value = groups_per_line + 8

        return initial_scale_value

    ##
    # @brief        Private Member Function Get the Scale Decrement Interval, Computed as Per DSC Spec.
    # @param[in]    groups_per_line: int
    #                   Specifies Number of Group Used to Code Each Line of Slice.
    # @return       scale_decrement_interval: int
    #                   Specifies the Number of Group Times Between Decrementing the rcXformScale Factor at the
    #                   Beginning of a Slice.
    def _get_scale_decrement_interval(self, groups_per_line: int) -> int:
        scale_decrement_interval: int

        if self._pic_parameter_set.initial_scale_value > 8:
            scale_decrement_interval = groups_per_line // (self._pic_parameter_set.initial_scale_value - 8)
        else:
            scale_decrement_interval = 4095

        return scale_decrement_interval

    ##
    # @brief        Private Member Function Get the Final Scale, Computed as Per DSC Spec.
    # @return       final_scale: int
    #                   Specifies a Integer Value Which Helps to Keep the RC Parameter Values in the Right State by
    #                   Increasing the xmit Delay.
    def _get_final_scale(self) -> int:
        final_scale: int = 8 * self._pic_parameter_set.rc_model_size
        final_scale = final_scale // (self._pic_parameter_set.rc_model_size - self._pic_parameter_set.final_offset)

        return final_scale

    ##
    # @brief        Private Member Function Get the Scale Increment Interval, Computed as Per DSC Spec.
    # @param[in]    final_scale: int
    #                   Specifies a Integer Value Which Helps to Keep the RC Parameter Values in the Right State by
    #                   Increasing the xmit Delay.
    # @return       s_increment_interval: int
    #                   Specifies the Number of Group Times Between Incrementing the rcXformScale Factor at the end of
    #                   a Slice.
    def _get_scale_increment_interval(self, final_scale: int) -> int:
        s_increment_interval: int

        if final_scale > 9:
            s_increment_interval = (self._pic_parameter_set.nfl_bpg_offset + self._pic_parameter_set.slice_bpg_offset)
            s_increment_interval += self._pic_parameter_set.nsl_bpg_offset
            s_increment_interval = (s_increment_interval * (final_scale - 9))
            s_increment_interval = int((self._pic_parameter_set.final_offset * (1 << 11)) / s_increment_interval)
        else:
            s_increment_interval = 0

        return s_increment_interval

    ##
    # @brief        Private Member Function Get the NFL BPP Checker, Computed as Per DSC Spec.
    # @return       nfl_bpp_checker: int
    #                   Returns an Integer Value used to Bring the BPG Offset to a Optimal Value.
    def _get_nfl_bpp_checker(self) -> int:
        bpp: int = self._pic_parameter_set.bits_per_pixel.value
        nfl_bpp_checker: int = (self._pic_parameter_set.slice_bpg_offset + self._pic_parameter_set.nfl_bpg_offset)
        nfl_bpp_checker = ((3 * bpp) - (nfl_bpp_checker // (1 << 11)))

        return nfl_bpp_checker

    ##
    # @brief        Private Member Function Get the NFL BPG Offset, Computed as Per DSC Spec.
    # @return       nfl_bpg_offset: int
    #                   Specifies Number of Bits that are Deallocated For Each Group, For Groups After the First Line of
    #                   a Slice.
    def _get_nfl_bpg_offset(self) -> int:
        if self._pic_parameter_set.slice_height > 1:
            temp = (self._pic_parameter_set.first_line_bpg_offset << 11) / (self._pic_parameter_set.slice_height - 1)
            nfl_bpg_offset = int(math.ceil(temp))
        else:
            nfl_bpg_offset = 0

        return nfl_bpg_offset

    ##
    # @brief        Private Member Function Get the NSL BPG Offset, Computed as Per DSC Spec.
    # @return       nsl_bpg_offset: int
    #                   Specifies Number of Bits that are Deallocated For Each Group, For Groups After the Second Line
    #                   of a Slice.
    def _get_nsl_bpg_offset(self) -> int:
        nsl_bpg_offset = 0

        if self._pic_parameter_set.dsc_version_minor == 1 or self._pic_parameter_set.native_420 == 0:
            return nsl_bpg_offset

        if self._pic_parameter_set.slice_height > 2:
            temp = (self._pic_parameter_set.second_line_bpg_offset << 11) / (self._pic_parameter_set.slice_height - 1)
            nsl_bpg_offset = int(math.ceil(temp))

        return nsl_bpg_offset

    ##
    # @brief        Private Member Function Get the Slice BPG Offset, Computed as Per DSC Spec.
    # @param[in]    groups_per_line: int
    #                   Specifies Number of Group Used to Code Each Line of Slice.
    # @param[in]    num_extra_mux_bits: int
    #                   Specifies Number of Bits that Can Remain at the End of Slice Due to Sub-stream Multiplexing.
    # @return       slice_bpg_offset: int
    #                   Specifies Number of Bits that are Deallocated For Each Group to Enforce the Slice Constraint,
    #                   While Allowing a Programmable Initial Offset.
    def _get_slice_bpg_offset(self, groups_per_line: int, num_extra_mux_bits: int):
        groups_total = float(groups_per_line * self._pic_parameter_set.slice_height)
        temp = (self._pic_parameter_set.rc_model_size - self._pic_parameter_set.initial_offset + num_extra_mux_bits)
        slice_bpg_offset = int(math.ceil(((temp << 11) / groups_total)))

        return slice_bpg_offset

    ##
    # @brief        Private Member Function Get the Rate Control Bits, Computed as Per DSC Spec.
    # @param[in]    hrd_delay:
    # @return       rate_control_bits: int
    def _get_rate_control_bits(self, hrd_delay: int) -> int:
        rate_control_bits: int = (hrd_delay * self._pic_parameter_set.bits_per_pixel.value)
        rate_control_bits = int(math.ceil(rate_control_bits / dsc_args.FIXED_POINT_U6_4_CONVERSION))

        return rate_control_bits

    ##
    # @brief        Private Member Function Get the Quantization Parameter Modifier, Computed as Per DSC Spec.
    # @return       qp_bpc_modifier: int
    #                   Specifies a Modifier to Adjust Min, Max Flatness and Also For RC Quant Limits
    def _get_qp_bpc_modifier(self, difference: int) -> int:
        qp_bpc_modifier: int = (self._pic_parameter_set.bits_per_component - 8) * 2 - difference

        return qp_bpc_modifier

    ##
    # TODO: Need to see if this is required. Not used in the algo at all. can be removed
    def _set_flatness_det_threshold(self):
        self._pic_parameter_set.flatness_det_threshold = 2 << (self._pic_parameter_set.bits_per_component - 8)

    ##
    # @brief        Private Member Function to set the Second Line Offset Adjustment. Computed as Per DSC Spec.
    #               Used as an offset adjustment for the second line in native 4:2:0 mode.
    # @return       None
    def _set_second_line_offset_adjustment(self) -> None:

        if self._pic_parameter_set.dsc_version_minor == 1 or self._pic_parameter_set.native_420 == 0:
            self._pic_parameter_set.second_line_offset_adj = 0
        else:
            self._pic_parameter_set.second_line_offset_adj = 512

    ##
    # @brief        Private Member function to get the uncompressed bits per group rate.
    #               Calculated as per C Model algorithm.
    # @return       uncompressed_bpg_rate: int
    def _get_uncompressed_bpg_rate(self) -> int:
        if self._pic_parameter_set.native_422:
            uncompressed_bpg_rate = 3 * self._pic_parameter_set.bits_per_component * 4
        else:
            adder = 0 if PictureParameterSetCalculator.is_yuv_input else 2
            uncompressed_bpg_rate = (3 * self._pic_parameter_set.bits_per_component + adder) * 3

        return uncompressed_bpg_rate

    ##
    # @brief        Algorithm to Computes RC Parameters as Per DSC Spec.
    # @param[in]    pixels_per_group: int
    #                   Each slice is made up of group of pixels. Each group is a set of 3 or 6 pixels in raster scan
    #                   order
    # @param[in]    num_of_substream_processors: int
    #                   Indicates the number of substream processors to process each of the component.
    #                   In Native 4:2:2 mode 4 SSPs are used else 3 SSPs are used
    #                   Y, Cb, Cr - Each component is processed by one SSP. Odd position Y component is processed by
    #                   4th SSP (only for Native 4:2:2) mode.
    # @return       Returns True if Algorithm is Able to Compute the RC Params, False Otherwise.
    def _compute_rc_parameters(self, pixels_per_group: int, num_of_substream_processors: int) -> bool:
        uncompressed_bpg_rate = self._get_uncompressed_bpg_rate()
        self._pic_parameter_set.first_line_bpg_offset = self._get_first_line_bpg_offset(uncompressed_bpg_rate)
        self._pic_parameter_set.second_line_bpg_offset = self._get_second_line_bpg_offset(uncompressed_bpg_rate)

        groups_per_line: int = self._get_groups_per_line(pixels_per_group)
        self._pic_parameter_set.chunk_size = self._get_chunk_size()

        num_extra_mux_bits: int = self._get_num_extra_mux_bits(num_of_substream_processors)

        self._pic_parameter_set.initial_scale_value = self._get_initial_scale_value(groups_per_line)
        self._pic_parameter_set.scale_decrement_interval = self._get_scale_decrement_interval(groups_per_line)

        self._pic_parameter_set.final_offset = self._get_final_offset(num_extra_mux_bits)
        if self._pic_parameter_set.final_offset >= self._pic_parameter_set.rc_model_size:
            logging.error("The FinalOffset must be less than the RcModelSize. Try increasing InitialXmitDelay")
            return False

        final_scale: int = self._get_final_scale()
        if final_scale > 63:
            logging.error("\tfinal_scale value > 63/8 may lead to undefined behavior.increase initial_xmit delay")
            return False

        self._pic_parameter_set.nfl_bpg_offset = self._get_nfl_bpg_offset()
        if self._pic_parameter_set.nfl_bpg_offset > 65535:
            logging.error("NflBpgOffset is too large for this slice height")
            return False

        self._pic_parameter_set.nsl_bpg_offset = self._get_nsl_bpg_offset()
        if self._pic_parameter_set.nsl_bpg_offset > 65535:
            logging.error("NslBpgOffset is too large for this slice height")
            return False

        self._pic_parameter_set.slice_bpg_offset = self._get_slice_bpg_offset(groups_per_line, num_extra_mux_bits)

        nfl_bpp_checker: int = self._get_nfl_bpp_checker()

        if self._pic_parameter_set.slice_height == 1 and self._pic_parameter_set.first_line_bpg_offset > 0:
            logging.error("For Slice height of One, First Line BPG offset should be 0")
            return False
        elif nfl_bpp_checker < 16:
            logging.error("BPP for NflBpgOffset is too low, decrease FirstLineBpgOfs")
            return False

        if final_scale > 9:
            self._pic_parameter_set.scale_increment_interval = self._get_scale_increment_interval(final_scale)

            if self._pic_parameter_set.scale_increment_interval > 65535:
                logging.error("ScaleIncrementInterval value is too large for this slice height")
                return False
        else:
            self._pic_parameter_set.scale_increment_interval = 0

        hrd_delay: int = self._get_hrd_delay(pixels_per_group, groups_per_line)

        self._pic_parameter_set.rate_control_bits = self._get_rate_control_bits(hrd_delay)
        self._pic_parameter_set.initial_dec_delay = self._get_initial_dec_delay(hrd_delay)

        return True

    ##
    # @brief        Private Member Function Set Parameters like Pic Height, Pic Width, Slice Height and Slice Width.
    #               These Parameters are Computed From Display Timing Information.
    # @return       None
    def _set_picture_slice_parameters(self) -> None:
        display_timing: DisplayTimings = self.timing_info

        # Refer Usage guide sheet of DSC Parameter Values VESA V1-2.xlsm file provided by VESA
        # For 4:4:4 and Simple 4:2:2 min pixels per slice should 15000
        # For Native 4:2:2 and Native 4:2:0 min pixels per slice should be 30000
        min_pixels_per_slice = 15000

        if self._pic_parameter_set.native_422 or self._pic_parameter_set.native_420:
            min_pixels_per_slice = 30000

        self._pic_parameter_set.pic_height = display_timing.vActive

        # Dividing hActive with vdsc_instances to get pic_width, since each VDSC engine will compress
        # that fraction of the image
        self._pic_parameter_set.h_active = display_timing.hActive
        self._pic_parameter_set.pic_width = display_timing.hActive / self._pic_parameter_set.vdsc_instances
        self._pic_parameter_set.pic_width = int(math.ceil(self._pic_parameter_set.pic_width))

        # Calculate Slice Height and Slice Width based on vActive and hActive
        self._pic_parameter_set.slice_width = display_timing.hActive / self._pic_parameter_set.slice_count
        self._pic_parameter_set.slice_width = int(math.ceil(self._pic_parameter_set.slice_width))

        # Slice height optimization will now be applied as follows :
        # For eDP: PSR2 + DSC co-existence is true + all DSC versions else same as DP
        # For DP: No optimization. Slice Height = PicHeight
        # For HDMI: Always follow Slice height optimization.
        # For MIPI: No optimization. Slice Height = PicHeight/2
        follow_slice_height_optimization = True
        if (
                self._display.display_type == DisplayType.EMBEDDED_DISPLAY_PORT and
                DSCHelper.is_psr2_dsc_co_existence_supported_platform(self.gfx_index, self._display.platform) is False
        ) or (
                self._display.display_type == DisplayType.DISPLAY_PORT
        ):
            follow_slice_height_optimization = False

        if follow_slice_height_optimization is True:
            slice_height = 96
            while slice_height <= display_timing.vActive:
                if (display_timing.vActive % slice_height) == 0 and (
                        self._pic_parameter_set.slice_width * slice_height) >= min_pixels_per_slice:
                    self._pic_parameter_set.slice_height = slice_height
                    break
                slice_height += 2
        else:
            self._pic_parameter_set.slice_height = self._pic_parameter_set.pic_height

        if self._pic_parameter_set.slice_height == 0:
            gdhm.report_driver_bug_di("[Display_Interfaces][VDSC]Valid Slice Height Not Found")
        assert self._pic_parameter_set.slice_height != 0, "Valid Slice Height Not Found."

    ##
    # @brief        Private Member Function to generate Initial Rate Control Range Parameters for Native 4:2:0 color
    #               format as per DSC Spec.
    # @return       rc_range_parameter_list: List[RcRangeParameters]
    #                   Returns the calculated rc_range_parameter_list based on BPC and BPP
    def _generate_rc_range_params_for_native_420(self) -> List[RcRangeParameters]:
        rc_range_parameter_list: [RcRangeParameters] = []

        bits_per_component = self._pic_parameter_set.bits_per_component
        bits_per_pixel: int = self._pic_parameter_set.bits_per_pixel.value
        column_index = (bits_per_pixel - (8 * dsc_args.FIXED_POINT_U6_4_CONVERSION)) // 16
        range_min_qp420: List[List[int]] = dsc_args.RC_RANGE_PARAMS_420[bits_per_component]['MIN']
        range_max_qp420: List[List[int]] = dsc_args.RC_RANGE_PARAMS_420[bits_per_component]['MAX']

        for index in range(dsc_args.RC_RANGES_BUF_SIZE):

            range_min_qp: int = range_min_qp420[index][column_index]
            range_max_qp: int = range_max_qp420[index][column_index]

            if bits_per_pixel <= dsc_args.DSC_BPP_8:
                bpg_offset = dsc_args.NATIVE_420_OFFSET_UNDER_4BPP[index]
            elif bits_per_pixel <= dsc_args.DSC_BPP_10:
                offset_under_4bpp = dsc_args.NATIVE_420_OFFSET_UNDER_4BPP[index]
                offset_under_5bpp = dsc_args.NATIVE_420_OFFSET_UNDER_5BPP[index]
                add_to_offset = 0.5 * (bits_per_pixel - dsc_args.DSC_BPP_8) * (offset_under_5bpp - offset_under_4bpp)
                add_to_offset = int((add_to_offset / dsc_args.FIXED_POINT_U6_4_CONVERSION) + 0.5)
                bpg_offset = offset_under_4bpp + add_to_offset
            elif bits_per_pixel <= dsc_args.DSC_BPP_12:
                offset_under_5bpp = dsc_args.NATIVE_420_OFFSET_UNDER_5BPP[index]
                offset_under_6bpp = dsc_args.NATIVE_420_OFFSET_UNDER_6BPP[index]
                add_to_offset = 0.5 * (bits_per_pixel - dsc_args.DSC_BPP_10) * (offset_under_6bpp - offset_under_5bpp)
                add_to_offset = int((add_to_offset / dsc_args.FIXED_POINT_U6_4_CONVERSION) + 0.5)
                bpg_offset = offset_under_5bpp + add_to_offset
            elif bits_per_pixel <= dsc_args.DSC_BPP_16:
                offset_under_6bpp = dsc_args.NATIVE_420_OFFSET_UNDER_6BPP[index]
                offset_under_8bpp = dsc_args.NATIVE_420_OFFSET_UNDER_8BPP[index]
                add_to_offset = 0.25 * (bits_per_pixel - dsc_args.DSC_BPP_12) * (offset_under_8bpp - offset_under_6bpp)
                add_to_offset = int((add_to_offset / dsc_args.FIXED_POINT_U6_4_CONVERSION) + 0.5)
                bpg_offset = offset_under_6bpp + add_to_offset
            else:
                bpg_offset = dsc_args.NATIVE_420_OFFSET_UNDER_8BPP[index]

            abs_bpg_offset: int = abs(bpg_offset)

            # Get Two's complement(6 bit) of range_bpg_offset if the offset is a negative number.
            bpg_offset = bpg_offset if bpg_offset > 0 else ((~abs_bpg_offset + 1) & 0x3F)
            rc_range_parameter_list.append(RcRangeParameters(range_min_qp, range_max_qp, bpg_offset))

        return rc_range_parameter_list

    ##
    # @brief        Private Member Function to generate Initial Rate Control Range Parameters for Native 4:2:2 color
    #               format as per DSC Spec.
    # @return       rc_range_parameter_list: List[RcRangeParameters]
    #                   Returns the calculated rc_range_parameter_list based on BPC and BPP
    def _generate_rc_range_params_for_native_422(self) -> List[RcRangeParameters]:
        rc_range_parameter_list: [RcRangeParameters] = []

        bits_per_pixel: int = self._pic_parameter_set.bits_per_pixel.value
        bits_per_component = self._pic_parameter_set.bits_per_component
        column_index = (bits_per_pixel - (12 * dsc_args.FIXED_POINT_U6_4_CONVERSION)) // 16

        range_min_qp422: List[List[int]] = dsc_args.RC_RANGE_PARAMS_422[bits_per_component]['MIN']
        range_max_qp422: List[List[int]] = dsc_args.RC_RANGE_PARAMS_422[bits_per_component]['MAX']

        for index in range(dsc_args.RC_RANGES_BUF_SIZE):

            range_min_qp: int = range_min_qp422[index][column_index]
            range_max_qp: int = range_max_qp422[index][column_index]

            if bits_per_pixel <= dsc_args.DSC_BPP_12:
                bpg_offset = dsc_args.NATIVE_422_OFFSET_UNDER_6BPP[index]
            elif bits_per_pixel <= dsc_args.DSC_BPP_14:
                offset_under_6bpp = dsc_args.NATIVE_422_OFFSET_UNDER_6BPP[index]
                offset_under_7bpp = dsc_args.NATIVE_422_OFFSET_UNDER_7BPP[index]
                add_to_offset = (bits_per_pixel - dsc_args.DSC_BPP_12) * (offset_under_7bpp - offset_under_6bpp)
                add_to_offset = int((add_to_offset / dsc_args.FIXED_POINT_U6_4_CONVERSION * 2.0) + 0.5)
                bpg_offset = offset_under_6bpp + add_to_offset
            elif bits_per_pixel <= dsc_args.DSC_BPP_16:
                bpg_offset = dsc_args.NATIVE_422_OFFSET_UNDER_7BPP[index]
            elif bits_per_pixel <= dsc_args.DSC_BPP_20:
                offset_under_7bpp = dsc_args.NATIVE_422_OFFSET_UNDER_7BPP[index]
                offset_under_10bpp = dsc_args.NATIVE_422_OFFSET_UNDER_10BPP[index]
                add_to_offset = (bits_per_pixel - dsc_args.DSC_BPP_16) * (offset_under_10bpp - offset_under_7bpp)
                add_to_offset = int((add_to_offset / (dsc_args.FIXED_POINT_U6_4_CONVERSION * 4.0)) + 0.5)
                bpg_offset = offset_under_7bpp + add_to_offset
            else:
                bpg_offset = dsc_args.NATIVE_422_OFFSET_UNDER_10BPP[index]

            abs_bpg_offset: int = abs(bpg_offset)

            # Get Two's complement(6 bit) of range_bpg_offset if the offset is a negative number.
            bpg_offset = bpg_offset if bpg_offset > 0 else ((~abs_bpg_offset + 1) & 0x3F)
            rc_range_parameter_list.append(RcRangeParameters(range_min_qp, range_max_qp, bpg_offset))

        return rc_range_parameter_list

    ##
    # @brief        Private Member Function to generate Initial Rate Control Range Parameters for other color formats as
    #               per DSC Spec.
    # @return       rc_range_parameter_list: List[RcRangeParameters]
    #                   Returns the calculated rc_range_parameter_list based on BPC and BPP
    def _generate_rc_range_params_for_other_formats(self, diff: int) -> List[RcRangeParameters]:
        rc_range_parameter_list: [RcRangeParameters] = []

        bits_per_component = self._pic_parameter_set.bits_per_component
        bits_per_pixel: int = self._pic_parameter_set.bits_per_pixel.value
        column_index: int = (2 * (bits_per_pixel - (6 * dsc_args.FIXED_POINT_U6_4_CONVERSION))) // 16

        range_min_qp444: List[List[int]] = dsc_args.RC_RANGE_PARAMS[bits_per_component]['MIN']
        range_max_qp444: List[List[int]] = dsc_args.RC_RANGE_PARAMS[bits_per_component]['MAX']

        for index in range(dsc_args.RC_RANGES_BUF_SIZE):

            range_min_qp: int = max(0, range_min_qp444[index][column_index] - diff)
            range_max_qp: int = max(0, range_max_qp444[index][column_index] - diff)

            bpp: int = self._pic_parameter_set.bits_per_pixel.value
            if bpp <= dsc_args.DSC_BPP_6:
                bpg_offset = dsc_args.OFFSET_UNDER_6BPP[index]
            elif bpp <= dsc_args.DSC_BPP_8:
                offset_under_6: int = dsc_args.OFFSET_UNDER_6BPP[index]
                offset_under_8: int = dsc_args.OFFSET_UNDER_8BPP[index]
                add_to_offset = 0.5 * (bpp - dsc_args.DSC_BPP_6) * (offset_under_8 - offset_under_6)
                add_to_offset = int((add_to_offset / dsc_args.FIXED_POINT_U6_4_CONVERSION) + 0.5)
                bpg_offset = offset_under_6 + add_to_offset
            elif bpp <= dsc_args.DSC_BPP_12:
                bpg_offset = dsc_args.OFFSET_UNDER_8BPP[index]
            elif bpp <= dsc_args.DSC_BPP_15:
                offset_under_12: int = dsc_args.OFFSET_UNDER_12BPP[index]
                offset_under_15: int = dsc_args.OFFSET_UNDER_15BPP[index]
                add_to_offset = (bpp - dsc_args.DSC_BPP_12) * (offset_under_15 - offset_under_12)
                add_to_offset = int((add_to_offset / (3.0 * dsc_args.FIXED_POINT_U6_4_CONVERSION)) + 0.5)
                bpg_offset = offset_under_12 + add_to_offset
            else:
                bpg_offset = dsc_args.OFFSET_UNDER_15BPP[index]

            abs_bpg_offset: int = abs(bpg_offset)

            # Get Two's complement(6 bit) of range_bpg_offset if the offset is a negative number.
            bpg_offset = bpg_offset if bpg_offset > 0 else ((~abs_bpg_offset + 1) & 0x3F)
            rc_range_parameter_list.append(RcRangeParameters(range_min_qp, range_max_qp, bpg_offset))

        return rc_range_parameter_list

    ##
    # @brief        Private Member Function to Set Initial Rate Control Range Parameters as Per DSC Spec.
    # @return       None
    def _set_initial_scale_value(self):
        rc_model_size = self._pic_parameter_set.rc_model_size
        initial_scale_value = 8 * rc_model_size // (rc_model_size - self._pic_parameter_set.initial_offset)
        self._pic_parameter_set.initial_scale_value = initial_scale_value

    ##
    # @brief        Private Member Function to Set Initial Rate Control Range Parameters as Per DSC Spec.
    # @return       None
    def _set_rc_range_parameter_list(self, diff: int) -> None:

        if self._pic_parameter_set.native_420 == 1:
            rc_range_parameter_list = self._generate_rc_range_params_for_native_420()
        elif self._pic_parameter_set.native_422 == 1:
            rc_range_parameter_list = self._generate_rc_range_params_for_native_422()
        else:
            rc_range_parameter_list = self._generate_rc_range_params_for_other_formats(diff)

        self._pic_parameter_set.rc_range_parameter_list = rc_range_parameter_list

    ##
    # @brief        Private Member Function to Set Initial Rate Control Parameters as Per DSC Spec.
    # @return       None
    def _set_initial_rate_control_values(self) -> None:
        # from Table no 4-2 in DSC 1.1 spec
        # six 0s are appended to the lsb of each threshold value internally in h/w
        # Only 8 bits are allowed for programming RcBufThreshold, so we divide RcBufThreshold by 2^6
        self._pic_parameter_set.rc_buf_thresh = [x // 64 for x in dsc_args.RC_BUF_THRESHOLD]

        # @TODO: Need to find why different values for 6BPP
        if self._pic_parameter_set.bits_per_component == dsc_args.DSC_BPP_6 is True:
            self._pic_parameter_set.rc_buf_thresh[12] = 0x7c
            self._pic_parameter_set.rc_buf_thresh[13] = 0x7D

    ##
    # @brief        Private Member Function  Set Mux Word Size as Per DSC Spec.
    # @return       None
    def _set_mux_word_size(self) -> None:
        self._pic_parameter_set.mux_word_size = 48 if self._pic_parameter_set.bits_per_component <= 10 else 64

    ##
    # @brief        Private Member Function to Set Flatness Min and Max Quantization Parameter.
    # @param[in]    qp_bpc_modifier: int
    #                   Computed Value to Adjust the Min and Max Quantization Parameter as per the Algorithm.
    # @return       None
    def _set_qp_min_max_flatness(self, qp_bpc_modifier: int) -> None:
        self._pic_parameter_set.flatness_min_qp = 3 + qp_bpc_modifier
        self._pic_parameter_set.flatness_max_qp = 12 + qp_bpc_modifier

    ##
    # @brief        Private Member Function to Set Quantization Parameter Used in Short Term Rate Control
    # @param[in]    qp_bpc_modifier: int
    #                   Computed Value to Adjust the Limit 0 and Limit 1 Quantization Parameter as per the Algorithm.
    # @return       None
    def _set_rc_quant_limits(self, qp_bpc_modifier: int) -> None:
        self._pic_parameter_set.rc_quant_inc_limit_0 = 11 + qp_bpc_modifier
        self._pic_parameter_set.rc_quant_inc_limit_1 = 11 + qp_bpc_modifier

    ##
    # @brief        Private Member to generate all the rate control parameters based on the color formats.
    # @return       None
    def _generate_rc_parameters(self) -> None:
        diff: int = 0

        if PictureParameterSetCalculator.is_yuv_input and (self._pic_parameter_set.dsc_version_minor == 1):
            diff = 1

        qp_bpc_modifier: int = self._get_qp_bpc_modifier(diff)
        self._set_rc_quant_limits(qp_bpc_modifier)
        self._set_qp_min_max_flatness(qp_bpc_modifier)

        self._set_initial_offset()
        self._set_initial_xmit_delay()

        self._set_flatness_det_threshold()
        self._set_second_line_offset_adjustment()
        self._set_rc_range_parameter_list(diff)

    ##
    # @brief        Set RC Parameters from CFG
    def _set_rc_parameters_from_cfg(self):
        bits_per_pixel = self._pic_parameter_set.bits_per_pixel.value // dsc_args.FIXED_POINT_U6_4_CONVERSION
        row_index = RC_PARAM_ROW_INDEX[bits_per_pixel]
        col_index = RC_PARAM_COL_INDEX[self._pic_parameter_set.bits_per_component]

        if self._pic_parameter_set.dsc_version_minor == 2:
            if self._pic_parameter_set.slice_height >= 8:
                self._pic_parameter_set.first_line_bpg_offset = 12 + (
                        (9 * min(34, (self._pic_parameter_set.slice_height - 8))) / 100)
            else:
                self._pic_parameter_set.first_line_bpg_offset = 2 * (self._pic_parameter_set.slice_height - 1)
        else:
            self._pic_parameter_set.first_line_bpg_offset = RC_PARAMETERS[row_index][col_index].first_line_bpg_offset

        self._pic_parameter_set.initial_xmit_delay = RC_PARAMETERS[row_index][col_index].initial_xmit_delay
        self._pic_parameter_set.initial_offset = RC_PARAMETERS[row_index][col_index].initial_offset
        self._pic_parameter_set.flatness_min_qp = RC_PARAMETERS[row_index][col_index].flatness_min_qp
        self._pic_parameter_set.flatness_max_qp = RC_PARAMETERS[row_index][col_index].flatness_max_qp
        self._pic_parameter_set.rc_quant_inc_limit_0 = RC_PARAMETERS[row_index][col_index].rc_quant_inc_limit_0
        self._pic_parameter_set.rc_quant_inc_limit_1 = RC_PARAMETERS[row_index][col_index].rc_quant_inc_limit_1

        for index in range(dsc_args.RC_RANGES_BUF_SIZE):
            range_min_qp = RC_PARAMETERS[row_index][col_index].rc_range_parameter_list[index].range_min_qp
            range_max_qp = RC_PARAMETERS[row_index][col_index].rc_range_parameter_list[index].range_max_qp
            range_bpg_offset = RC_PARAMETERS[row_index][col_index].rc_range_parameter_list[index].range_bpg_offset

            # Get Two's complement(6 bit) of range_bpg_offset if the offset is a negative number.
            abs_range_bpg_offset: int = abs(range_bpg_offset)
            range_bpg_offset = range_bpg_offset if range_bpg_offset > 0 else ((~abs_range_bpg_offset + 1) & 0x3F)

            rc_range_parameters = RcRangeParameters(range_min_qp, range_max_qp, range_bpg_offset)
            self._pic_parameter_set.rc_range_parameter_list.append(rc_range_parameters)

    ##
    # @brief        Exposed Function to Set the PPS Parameters as Per the C-Model Calculation
    # @return       None
    def set_dsc_picture_parameter_set(self) -> None:

        self._set_info_frame_header()
        self._set_dsc_major_minor_version()
        self._set_color_format_support()

        self._update_pps_based_on_restrictions()

        self._set_bits_per_component()
        self._set_line_buffer_depth()
        self._set_mux_word_size()
        self._set_initial_rate_control_values()
        self._set_no_of_vdsc_instance()

        self._set_slice_count()
        self._set_picture_slice_parameters()
        self._set_compression_bpp()

        self._set_is_block_prediction_enabled()
        self._set_initial_scale_value()
        self._set_is_dsc_enabled()

        slice_pixels = self._pic_parameter_set.slice_width * self._pic_parameter_set.slice_height
        if self._display.display_type == DisplayType.MIPI_DISPLAY or slice_pixels < 15000:
            self._set_rc_parameters_from_cfg()
        else:
            self._generate_rc_parameters()

        num_of_substream_processors = 4 if self._pic_parameter_set.native_422 == 1 else 3
        pixels_per_group = 3

        while self._pic_parameter_set.slice_height != 0:
            if self._compute_rc_parameters(pixels_per_group, num_of_substream_processors) is True:
                break
            else:
                logging.warning("Compute RC Parameters Failed. Retrying by reducing the slice height by half")
                self._pic_parameter_set.slice_height = self._pic_parameter_set.slice_height // 2
                logging.warning("Reduced slice height: {}".format(self._pic_parameter_set.slice_height))
                if self._pic_parameter_set.slice_height == 0:
                    assert False, "Could not find valid PPS for any slice height."

    ##
    # @brief        Private Member Function to Update Picture Parameter Set Based on the Restriction in the H/W.
    # @return       None
    def _update_pps_based_on_restrictions(self) -> None:
        if self._pic_parameter_set.dsc_version_minor == 2 and self._display.platform in DSC_1P2_UNSUPPORTED_PLATFORMS:
            self._pic_parameter_set.dsc_version_minor = 1
