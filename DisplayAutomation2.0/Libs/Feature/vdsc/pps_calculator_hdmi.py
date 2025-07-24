#######################################################################################################################
# @file         pps_calculator_hdmi.py
# @brief        Contains HDMIPictureParameterSetCalculator Used For Calculating DSC Parameters as Per HDMI2.1 + DSC
#               Requirement.
#
# @author       Praburaj Krishnan
#######################################################################################################################
import logging
import math
from typing import Dict, Any

from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.clock.lnl.lnl_clock_base import LnlClock
from Libs.Feature.clock.ptl.ptl_clock_base import PtlClock
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat, ModeEnumHelper
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock
from Libs.Feature.vdsc.dsc_definitions import BPP, DSCDisplay
from Libs.Feature.vdsc.dsc_enum_constants import AUDIO_OVERHEAD_IN_TB_4, EMP_HEADER_BYTE0, CVTEM_DATA_SET_LENGTH
from Libs.Feature.vdsc.dsc_enum_constants import DATA_SET_TYPE_PERIODIC_PSEUDO_STATIC_EM_DATA_SET
from Libs.Feature.vdsc.dsc_enum_constants import DPT_BW_CHECK_REQUIRED_PLATFORMS
from Libs.Feature.vdsc.dsc_enum_constants import HDMI2P1_AUDIO_WA_REQUIRED_PLATFORMS
from Libs.Feature.vdsc.dsc_enum_constants import MAX_BPP_SUPPORTED_BPP_D13_PLUS, MAX_SLICE_SUPPORTED_HW
from Libs.Feature.vdsc.dsc_enum_constants import MAX_TB_DELTA_453_BYTES_444_SET, NORMATIVE_TABLE_444_BPP
from Libs.Feature.vdsc.dsc_enum_constants import MAX_TB_DELTA_453_BYTES_YUV420_SET, NORMATIVE_TABLE_YUV420_BPP
from Libs.Feature.vdsc.dsc_enum_constants import MAX_TB_DELTA_453_BYTES_YUV422_SET, NORMATIVE_TABLE_YUV422_BPP
from Libs.Feature.vdsc.dsc_enum_constants import NUM_EMP_CONTROL_BYTES, DATA_SET_FRAGMENT_LENGTH
from Libs.Feature.vdsc.dsc_enum_constants import TestDataKey, HDMIDSC, FIXED_POINT_U6_4_CONVERSION, AudioPacketType
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Feature.vdsc.pps_calculator import PictureParameterSetCalculator


##
# @brief        HDMIPictureParameterSetCalculator is Inherited From PictureParameterSetCalculator.
#               It Uses Existing Implementation Present in Base class If the Functionality is Sufficient, Otherwise
#               Overrides it.
class HDMIPictureParameterSetCalculator(PictureParameterSetCalculator):

    ##
    # @brief        Initialize the HDMI PPS Calculator.
    # @param[in]    hdmi_dsc_display: DSCDisplay
    #                   Contains Information about the HDMI Display For Which PPS Parameter Has to be Calculated.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, hdmi_dsc_display: DSCDisplay, test_data: Dict[TestDataKey, Any]) -> None:
        super().__init__(hdmi_dsc_display, test_data)
        self._is_big_joiner_enabled: bool = False
        self.hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
        self.hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(self.gfx_index, self.port)

    ##
    # @brief        Abstract method, to set the info frame header data
    # @return       None
    def _set_info_frame_header(self) -> None:
        num_of_packets = math.ceil((CVTEM_DATA_SET_LENGTH + NUM_EMP_CONTROL_BYTES) / DATA_SET_FRAGMENT_LENGTH)

        # As per Bspec, program header same as "HDMI_EMP_REGISTER"
        info_frame_header = EMP_HEADER_BYTE0
        info_frame_header = info_frame_header | (num_of_packets << 16)
        info_frame_header = info_frame_header | (DATA_SET_TYPE_PERIODIC_PSEUDO_STATIC_EM_DATA_SET << 24)

        self._pic_parameter_set.info_frame_header.value = info_frame_header

    ##
    # @brief    DSC Major and Minor Version is Set Based on the Panel Capability Read from SCDC register.
    #           Minor Version Might Change Depending on the Hardware Capability.
    # @return   None
    def _set_dsc_major_minor_version(self) -> None:
        # HDMI 2.1 Spec mandates DSC1.2a support to support DSC
        self._pic_parameter_set.dsc_version_major = 1
        self._pic_parameter_set.dsc_version_minor = 2

    ##
    # @brief    Line Buffer Depth is Hard-Coded as per HDMI2.1 Spec. Might change in the future
    #           LINE_BUF_DEPTH Dict is used to Map the Binary Value to Integer
    # @return   None
    def _set_line_buffer_depth(self) -> None:
        # Hard-Coded to 13 based on HDMI2.1 spec
        self._pic_parameter_set.line_buffer_depth = 13

    ##
    # @brief    Block Prediction Enable Status is Should Always Set to True In Case of HDMI2.1 + DSC
    # @return   None
    def _set_is_block_prediction_enabled(self) -> None:
        self._pic_parameter_set.is_block_prediction_enabled = True

    ##
    # @brief    Pixel Encoding Formats are Updated here Based on the Pixel Encoding from the Test case RGB, YCbCr 4:4:4
    #           YCbCr Native 4:2:2, Native 4:2:0 - Supported in DSC 1.2a and Higher
    # @return   None
    def _set_color_format_support(self) -> None:
        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)

        rgb_support = True  # Always supported if DSC Support is mentioned
        ycbcr_444_support = color_format == ColorFormat.YUV444  # Test Should tell if 4:4:4 is supported or not
        ycbcr_native_422_support = color_format == ColorFormat.YUV422  # Test Should tell if 4:2:2 is supported or not
        ycbcr_native_420_support = self.hf_vsdb_parser.is_dsc_native_420_supported
        self._pic_parameter_set.simple_422 = 0  # Not supported by driver

        if color_format == ColorFormat.RGB and rgb_support == 1:
            self._pic_parameter_set.convert_rgb = 1
            self._pic_parameter_set.native_422 = self._pic_parameter_set.native_420 = 0
        elif color_format == ColorFormat.YUV420 and ycbcr_native_420_support == 1:
            self._pic_parameter_set.native_420 = 1
            self._pic_parameter_set.native_422 = self._pic_parameter_set.convert_rgb = 0
        elif color_format == ColorFormat.YUV444 and ycbcr_444_support == 1:
            self._pic_parameter_set.convert_rgb = 0
            self._pic_parameter_set.native_422 = self._pic_parameter_set.native_420 = 0
        elif color_format == ColorFormat.YUV422 and ycbcr_native_422_support == 1:
            self._pic_parameter_set.native_422 = 1
            self._pic_parameter_set.native_420 = self._pic_parameter_set.convert_rgb = 0
        else:
            raise AssertionError("Invalid Case")

    ##
    # @brief    Slice Count is Set by Calculating the Minimum Slice Count Needed for Peak Pixel Rate.
    #           This Min Slice Count is used to Get the Max Slice Count as Supported by the HDMI 2.1 DSC Panel.
    #           Then Find the Min Slice Count between the Obtained Min Slice Count and Max H/W Supported Slice Count.
    # @return   None
    def _set_slice_count(self) -> None:

        # TODO: Minimum Slice Count can be Increased to 12 Once 12 Slice DCN is implemented.
        min_slice_count = self._get_min_slice_count_from_ppr()
        assert min_slice_count <= 16, f"Min Slice count of {min_slice_count} required is not supported by HW"

        max_slice_count: int = self._get_max_slice_count(min_slice_count)

        max_slice_count = min(MAX_SLICE_SUPPORTED_HW, max_slice_count)
        logging.debug("Final Valid Slice Count After Considering H/W Limitation: {}".format(max_slice_count))

        self._pic_parameter_set.slice_count = max_slice_count

        # Update No of Vdsc Instances to 12 if and only if slice count is 12
        # 3 DSC Engine per pipe will be enabled only in this case.
        if self._pic_parameter_set.slice_count == 12:
            self._pic_parameter_set.vdsc_instances = 12

    ##
    # @brief    No VDSC Instance is Determined by the resolution, pixel clock and platform max cd clock.
    #           Each DSC Engine is Capable of Processing 2 Slices.Two DSC Engine is Available Per Pipe.
    #           In Case of Big Joiner and Ultra joiner Two Pipes and Four pipe can be Combined respectively.
    #           Hence a Total of Four and Eight DSC Engine will be Active which can process maximum of 8 or 16 Slices
    #           respectively.
    # @return   None
    def _set_no_of_vdsc_instance(self) -> None:
        self._pic_parameter_set.vdsc_instances = 2
        is_pipe_joiner_required, no_of_pipe_required = DisplayClock.is_pipe_joiner_required(self.gfx_index, self.port)

        if is_pipe_joiner_required is True:
            if no_of_pipe_required == 2:
                self._pic_parameter_set.vdsc_instances = 4
            elif no_of_pipe_required == 4:
                self._pic_parameter_set.vdsc_instances = 8

        # Note: VDSC instances will be updated to 12 if the slice count is 12 and is done in slice count calc function.

    ##
    # @brief    DSC Feature Support can be Identified by Reading the Panel Capability From SCDC Register.
    # @return   None
    def _set_is_dsc_enabled(self) -> None:
        self._pic_parameter_set.is_dsc_enabled = self.hf_vsdb_parser.is_dsc_supported

    ##
    # @brief    Bits Per Component is Set by Reading the Programmed Value in Registry. If Registry value is Not
    #           Programmed Default Value of 8 is Set.
    # @return   None
    def _set_bits_per_component(self) -> None:
        # TODO:  Need to read the CAPS from SCDC register. Does Driver uses BPC from EDID if not have to go with Reg
        #        Key method
        self._pic_parameter_set.bits_per_component = 8

        if self.hf_vsdb_parser.is_16bpc_supported is True:
            self._pic_parameter_set.bits_per_component = 16
        elif self.hf_vsdb_parser.is_12bpc_supported is True:
            self._pic_parameter_set.bits_per_component = 12
        elif self.hf_vsdb_parser.is_10bpc_supported is True:
            self._pic_parameter_set.bits_per_component = 10

    ##
    # @brief    Maximum Possible Bits Per Pixel is the Minimum of Maximum Possible Bits Per Pixel on Link such that it
    #           Supports Min Audio Possible on the Link and the Maximum Supported by HW. It also Considers the Panel
    #           Limitations and Pixel Encoding Formats.
    # @return   None
    def _set_compression_bpp(self) -> None:
        max_supported_bpp = BPP(value=0)

        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)

        self._set_is_big_joiner_enabled()
        self._set_is_ultra_joiner_enabled()

        min_bpp = DSCHelper.get_min_dsc_bpp_for_pixel_encoding(color_format)
        assert min_bpp != 0, "Invalid Min BPP."

        bpc = self._pic_parameter_set.bits_per_component
        max_bpp = DSCHelper.get_max_dsc_bpp_for_pixel_encoding(color_format, bpc)
        assert max_bpp != 0, "Invalid Max BPP."

        max_supported_by_hardware = self.get_max_bpp_supported_by_hardware()
        max_bpp = min(max_bpp, max_supported_by_hardware)
        logging.debug("Max Possible BPP Considering H/W Limitation: {}".format(max_bpp))

        # HDMI2.1 Spec Limits Max BPP to 12 if is_dsc_all_bpp_supported is set to 0
        if self.hf_vsdb_parser.is_dsc_all_bpp_supported is False:
            max_bpp = min(max_bpp, 12 * FIXED_POINT_U6_4_CONVERSION)

        max_supported_bpp.value = self._get_max_supported_bpp(min_bpp, max_bpp)
        logging.info(f"Max Possible BPP Considering Audio and Bandwidth: {max_supported_bpp.value} ")

        # As pert DSC1.2a Spec for YUV420 and YU422 BPP Should be doubled
        if color_format == ColorFormat.YUV420 or color_format == ColorFormat.YUV422:
            logging.debug(f"Doubling the BPP since the pixel encoding is {color_format.name}")
            max_supported_bpp.value = 2 * max_supported_bpp.value
        logging.info(f"Max Support BPP Considering Pixel Encoding is: {max_supported_bpp.value}")

        self._pic_parameter_set.bits_per_pixel = max_supported_bpp

    ##
    # @brief        Member function to get the maximum BPP supported by the hardware. Hardware here includes the
    #               panel, our internal DSC related HW. It also considers platform limitation.
    # @return       max_supported_bpp: int [U6.4 Format]
    #                   Returns the maximum bpp supported by the platform
    def get_max_bpp_supported_by_hardware(self) -> int:
        max_bpp_supported_by_ultra_joiner = max_bpp_supported_by_big_joiner = max_bpp_supported_by_dpt = 0xFFF

        big_joiner_bits = 36
        small_joiner_ram_bits = 17280 * 8

        link_rate_gbps, lane_count = self.hf_vsdb_parser.dsc_max_frl_rate
        ddi_clock_hz = ((link_rate_gbps * (1 - 300 / 1000000)) / 18) * 1000000000

        target_pixel_rate = self.timing_info.targetPixelRate

        system_clock = DSCHelper.get_system_clock(self.gfx_index)

        # CD clock and port clock validation is not implemented for LNL
        # Optimal cd clock is used to calculate big joiner bpp for all platforms except LNL.
        if isinstance(system_clock, LnlClock) or isinstance(system_clock, PtlClock):
            optimal_cd_clock_mhz = system_clock.get_system_max_cd_clk(self.gfx_index)
        else:
            optimal_cd_clock_mhz = system_clock.get_optimal_cdclock(self.gfx_index, [self._display.port_name])

        optimal_cd_clock_hz = optimal_cd_clock_mhz * 1000000

        if self.is_big_joiner_enabled is True:
            max_bpp_supported_by_small_joiner = (2 * small_joiner_ram_bits) / self.timing_info.hActive
            max_bpp_supported_by_small_joiner = int(max_bpp_supported_by_small_joiner * FIXED_POINT_U6_4_CONVERSION)
            max_bpp_supported_by_big_joiner = (2 * optimal_cd_clock_hz * big_joiner_bits) / target_pixel_rate
            max_bpp_supported_by_big_joiner = int(max_bpp_supported_by_big_joiner * FIXED_POINT_U6_4_CONVERSION)
        else:
            max_bpp_supported_by_small_joiner = small_joiner_ram_bits / self.timing_info.hActive
            max_bpp_supported_by_small_joiner = int(max_bpp_supported_by_small_joiner * FIXED_POINT_U6_4_CONVERSION)

        if self._display.platform in DPT_BW_CHECK_REQUIRED_PLATFORMS:
            max_bpp_supported_by_dpt = int(((ddi_clock_hz * 9 * 8) / target_pixel_rate) * FIXED_POINT_U6_4_CONVERSION)

        if self._is_ultra_joiner_enabled is True:
            ultra_joiner_ram_bits = 4 * 72 * 512
            max_bpp_supported_by_ultra_joiner = ultra_joiner_ram_bits / self.timing_info.hActive
            max_bpp_supported_by_ultra_joiner = int(max_bpp_supported_by_ultra_joiner * FIXED_POINT_U6_4_CONVERSION)

        logging.info(f"Max BPP Supported by DPT: {max_bpp_supported_by_dpt}")
        logging.info(f"Max BPP Supported by Joiner RAM: {max_bpp_supported_by_small_joiner}")
        logging.info(f"Max Bpp Supported by Big Joiner: {max_bpp_supported_by_big_joiner}")
        logging.info(f"Max BPP Supported by Ultra Joiner: {max_bpp_supported_by_ultra_joiner}")

        # BPP will be stored in U6.4 format. 6 integral and 4 fractional.
        max_supported_bpp = min(max_bpp_supported_by_small_joiner, max_bpp_supported_by_big_joiner)
        max_supported_bpp = min(max_supported_bpp, max_bpp_supported_by_ultra_joiner)
        max_supported_bpp = min(max_supported_bpp, max_bpp_supported_by_dpt)
        max_supported_bpp = min(max_supported_bpp, MAX_BPP_SUPPORTED_BPP_D13_PLUS)

        return max_supported_bpp

    ##
    # @brief        Maximum Possible BPP on Link with Min Audio Support is Calculated here as per HDMI2.1 + DSC Spec.
    #               It Considers Multiple Parameters like FRL Rate, FRL Lane Count, Total, Chunk Bytes, Pixel Clock,
    #               HActive, HTotal, HBlank, Min BPP Required for Pixel Encoding, Slice Count, Slice Width
    # @param[in]    min_bpp: int
    #                   Minimum bpp at which the mode will be supported. Typically based on the pixel encoding.
    # @param[in]    max_bpp: int
    #                   Maximum bpp considering all the limitations like pixel encoding, HW, EDID support etc
    # @return       max_bpp_target: float
    #                   Returns the Max BPP Target for a Particular Mode in U6.4 Format
    def _get_max_supported_bpp(self, min_bpp: int, max_bpp: int) -> int:
        normative_bpp = 0
        frl_rate, frl_lane_count = self.hf_vsdb_parser.dsc_max_frl_rate
        dsc_total_chunk_bytes = self.hf_vsdb_parser.dsc_total_chunk_bytes
        fva_factor = 1

        # TODO: Need to compute FVA factor for Compressed Video Format.
        if self.hf_vsdb_parser.is_fast_v_active_supported is True:
            fva_factor = 1

        h_active, h_total = self.timing_info.hActive, self.timing_info.hTotal
        h_blank = (h_total - h_active)

        total_maximum_overhead = 2.184 if frl_lane_count == 4 else 2.136

        # Collect Link Characteristics
        pixel_clock_hz = fva_factor * self.timing_info.targetPixelRate * (1 + HDMIDSC.PIXEL_CLOCK_RATE_TOLERANCE)
        t_line_seconds = self.timing_info.hTotal / pixel_clock_hz
        frl_bit_rate_bps = frl_rate * 1000000000
        min_frl_bit_rate_bps = frl_bit_rate_bps * (1 - (HDMIDSC.FRL_BIT_RATE_TOLERANCE / 1000000))
        min_frl_char_rate_bps = min_frl_bit_rate_bps / 18
        min_frl_characters = math.floor(t_line_seconds * min_frl_char_rate_bps * frl_lane_count)
        logging.debug(f"Minimum FRL Characters: {min_frl_characters}")

        # Determine the Number of Available FRL Payload Characters Transmitted during HActive and HBlank
        available_frl_characters = math.floor((1 - (total_maximum_overhead / 100)) * min_frl_characters)

        min_h_c_blank_for_audio, avg_audio_packet_rate = self._get_min_h_c_blank_avg_pkt_rate_for_audio(t_line_seconds)

        max_bpp_target = 0
        min_bpp = min_bpp / FIXED_POINT_U6_4_CONVERSION
        max_bpp = max_bpp / FIXED_POINT_U6_4_CONVERSION

        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)
        vic_id = ModeEnumHelper.get_vic_data(self.timing_info)

        # All the Normative Table VICs assumes audio packet rate with 32 Channels at 48KHz SamplingRate LPCM.
        # For other Audio configurations we should calculate as mentioned in the pseudo code
        if avg_audio_packet_rate <= AudioPacketType.AVERAGAE_AUDIO_DATA_RATE_FOR_32CHANNEL_48SAMPLINGRATE:
            normative_bpp = self._get_normative_bpp_vic_info(vic_id, color_format)
            if normative_bpp != 0:
                logging.info(f'VIC present in normative table. Target BPP: {normative_bpp}')
                normative_bpp /= FIXED_POINT_U6_4_CONVERSION
                min_bpp = max_bpp = normative_bpp

            else:
                logging.info("VIC does not have Normative BPP defined in HDMI 2.1 Spec, "
                             "following DSC Pseudocode for calculating BPP")

        bpp_target = min_bpp
        while bpp_target <= max_bpp:
            slice_count, slice_width = self._pic_parameter_set.slice_count, self._pic_parameter_set.slice_width
            bytes_target = slice_count * math.ceil((bpp_target * slice_width) / 8)
            logging.info(f"bytes_target: {bytes_target}, dsc_total_chunk_bytes: {dsc_total_chunk_bytes}")
            if bytes_target > dsc_total_chunk_bytes:
                logging.error("Compression not supported as bytes target exceeded total chunk bytes")
                break

            h_c_active_target = math.ceil(bytes_target / 3)
            logging.debug(f"h_c_active_target: {h_c_active_target}")

            # Determine HCBlank Target for a specific bpp target setting
            h_c_blank_target_est1 = math.ceil((h_c_active_target * (h_blank / h_active)))
            logging.debug(f"h_c_blank_target_est1: {h_c_blank_target_est1}")

            h_c_blank_target_est2 = max(h_c_blank_target_est1, min_h_c_blank_for_audio)
            logging.debug(f"h_c_blank_target_est2: {h_c_blank_target_est2}")

            h_c_blank_target = available_frl_characters - ((3 / 2) * h_c_active_target)
            h_c_blank_target = min(float(h_c_blank_target_est2), h_c_blank_target)
            h_c_blank_target = 4 * math.floor(h_c_blank_target / 4)
            logging.debug(f"h_c_blank_target: {h_c_blank_target}")
            logging.debug(f"min_h_c_blank_audio: {min_h_c_blank_for_audio}")

            # Refer B-Spec: https://gfxspecs.intel.com/Predator/Home/Index/68944 (HDMI FRL Mode and Audio Support)
            platform = self._display.platform
            if platform in HDMI2P1_AUDIO_WA_REQUIRED_PLATFORMS:
                tb_overhead = AUDIO_OVERHEAD_IN_TB_4

                h_c_blank_target = h_c_blank_target - tb_overhead
                logging.debug(f"h_c_blank_target post WA: {h_c_blank_target}")

            if min_h_c_blank_for_audio > h_c_blank_target:
                logging.error("Audio not supported with current configuration")
                break

            # Verify h_c_active target and h_c_blank target for a specific bpp target setting meet data flow
            # metering requirements for the FRL configuration
            average_tri_byte_rate_hz = pixel_clock_hz / (h_active + h_blank)
            average_tri_byte_rate_hz = average_tri_byte_rate_hz * (h_c_active_target + h_c_blank_target)
            logging.debug(f"average_tri_byte_rate_hz: {average_tri_byte_rate_hz}")

            t_active_ref = t_line_seconds * (h_active / (h_active + h_blank))
            logging.debug(f"t_active_ref: {t_active_ref}")

            t_blank_ref = t_line_seconds * (h_blank / (h_active + h_blank))
            logging.debug(f"t_blank_ref: {t_blank_ref}")

            t_active_target1 = h_c_active_target / average_tri_byte_rate_hz
            t_active_target2 = ((3 / 2) * h_c_active_target) / (frl_lane_count * min_frl_char_rate_bps)
            t_active_target2 = t_active_target2 / (1 - (total_maximum_overhead / 100))
            t_active_target = max(t_active_target1, t_active_target2)
            logging.debug(f"t_active_target: {t_active_target}")

            t_blank_target = t_line_seconds - t_active_target
            logging.debug(f"t_blank_target: {t_blank_target}")

            tb_borrowed = t_active_target * average_tri_byte_rate_hz - h_c_active_target
            logging.debug(f"tb_borrowed: {tb_borrowed}")

            tb_delta = abs(t_active_target - t_active_ref)
            tb_delta = tb_delta * ((h_c_active_target + h_c_blank_target_est1) / t_line_seconds)
            logging.debug(f"tb_delta: {tb_delta}")

            if t_blank_ref < t_blank_target:
                tb_delta_limit = t_active_ref - (h_c_active_target / average_tri_byte_rate_hz)
                tb_delta_limit = tb_delta_limit * ((h_c_active_target + h_c_blank_target_est1) / t_line_seconds)
            else:
                tb_delta_limit = tb_delta
            logging.debug(f"tb_delta_limit: {tb_delta_limit}")

            tb_worst = math.ceil(max(tb_borrowed, tb_delta_limit))
            logging.debug(f"tb_worst: {tb_worst}")

            # TB worst max for some of the modes present in HDMI2.1 Spec Normative Table is 453 Tribytes.
            # For all other configs, it is 400 tri bytes.
            max_borrowed_tri_bytes = HDMIDSC.MAX_BORROWED_400_TRI_BYTES
            if avg_audio_packet_rate <= AudioPacketType.AVERAGAE_AUDIO_DATA_RATE_FOR_32CHANNEL_48SAMPLINGRATE:
                max_borrowed_tri_bytes = self._get_max_borrowed_tri_bytes(vic_id, color_format)

            if tb_worst > max_borrowed_tri_bytes:
                logging.error(f"Insufficient bandwidth to driver the display at {bpp_target}")
                break

            actual_no_frl_characters = math.ceil((3 / 2) * h_c_active_target) + h_c_blank_target
            logging.debug(f"actual_no_frl_characters: {actual_no_frl_characters}")

            utilization_targeted = actual_no_frl_characters / min_frl_characters
            logging.debug(f"utilization_targeted: {utilization_targeted}")

            margin_target = 1 - (utilization_targeted + (total_maximum_overhead / 100))
            logging.debug(f"margin_target: {margin_target}")

            if margin_target < 0:
                logging.debug("No unused bandwidth left. Max BPP reached")
                break

            max_bpp_target = bpp_target
            bpp_target = bpp_target + (1 / 16)

        assert max_bpp_target != 0, "Valid BPP Not Found"

        max_bpp_target = int(max_bpp_target * FIXED_POINT_U6_4_CONVERSION)

        return max_bpp_target

    ##
    # @brief        Get the Number of Audio Packets Required based on Audio Packet Type, Audio Layout and Audio
    #               Channel Allocate Standard.
    # @return       number_of_audio_packets: int
    #                   Returns Zero if Audio is not supported
    #                   Else Returns a Number based on the Audio Parameters
    def _get_audio_packets_required(self) -> int:
        is_audio_supported = self.test_data.get(TestDataKey.IS_AUDIO_SUPPORTED)

        if is_audio_supported is False:
            number_of_audio_packets = 0
            logging.info(f"number_of_audio_packets: {number_of_audio_packets}")
            return number_of_audio_packets

        # 0x02 - Audio Sample Packet
        # 0x07 - One Bit Audio Sample packet
        # 0x08 - DST Audio Packet
        # 0x09 - HBR Audio Packet
        # 0x0E - Multi-Stream Audio Sample Packet
        # 0x0F - One Bit Multi-Stream Audio Sample Packet
        # 0x0B - 3D Audio Sample Packet
        # 0x0C - One Bit 3D Audio Sample Packet
        audio_packet_type = self.test_data.get(TestDataKey.AUDIO_PACKET_TYPE)

        layout = self.test_data.get(TestDataKey.AUDIO_LAYOUT)  # 0 and 1 - Possible values

        # 0x01 - Type 1
        # 0x02 - Type 2
        # 0x03 - Type 3
        audio_channel_alloc_standard = self.test_data.get(TestDataKey.AUDIO_ALLOCATION_STANDARD)

        if audio_packet_type == 0x02 or audio_packet_type == 0x07:
            number_of_audio_packets = 0.25 if layout == 0 else 1
        elif audio_packet_type == 0x08:
            number_of_audio_packets = 0.25
        elif audio_packet_type in [0x09, 0x0E, 0x0F]:
            number_of_audio_packets = 1
        elif audio_packet_type in [0x0B, 0x0C]:
            if audio_channel_alloc_standard == 0x01:
                number_of_audio_packets = 2
            elif audio_channel_alloc_standard == 0x02:
                number_of_audio_packets = 3
            elif audio_channel_alloc_standard == 0x03:
                number_of_audio_packets = 4
            else:
                raise AssertionError("Invalid Audio Allocation Standard")
        else:
            raise AssertionError("Invalid Audio Packet Type")

        logging.info(f"number_of_audio_packets: {number_of_audio_packets}")

        return number_of_audio_packets

    ##
    # @brief        Computes the Minimum Required HCblank assuming no Control Period RC Compression. This includes
    #               Video Guard Band, Two Data Island Guard Bands, Two 12-Character Control Periods, Two More Characters
    #               for Margin(32 total), and 32 * number_of_audio_packets_h_c_blank
    # @return       min_h_c_blank_for_audio: int
    #               Returns the Min HBlank Required for Audio and average packer rate considering the above Parameters.
    def _get_min_h_c_blank_avg_pkt_rate_for_audio(self, t_line_seconds: int) -> int:
        # Audio Support Verification Computations
        number_of_audio_packets = self._get_audio_packets_required()
        audio_rate_hz = self.test_data.get(TestDataKey.AUDIO_RATE_HZ)
        average_audio_packet_hz = max(192000, audio_rate_hz * number_of_audio_packets)
        average_audio_packet_hz += 2 * HDMIDSC.MAX_ACR_PACKETS_RATE
        average_audio_packet_hz = average_audio_packet_hz * (1 + HDMIDSC.AUDIO_CLOCK_RATE_TOLERANCE / 1000000)

        average_number_of_audio_packets_per_line = average_audio_packet_hz * t_line_seconds
        number_of_audio_packets_h_c_blank = math.ceil(average_number_of_audio_packets_per_line)

        min_h_c_blank_for_audio = 32 + 32 * number_of_audio_packets_h_c_blank

        logging.info(f"Minimum HBlank Required for Driving Audio: {min_h_c_blank_for_audio}")

        return min_h_c_blank_for_audio, average_audio_packet_hz

    ##
    # @brief    Calculate the Minimum Needed Slice Count for the Peak Pixel Rate of the Display.
    # @return   min_slice_count: int
    #               Returns the minimum no of slice a frame has to be divided based on the pixel clock.
    def _get_min_slice_count_from_ppr(self) -> int:
        slice_adjust = 0
        fva_factor = 1

        # TODO: Need to compute FVA factor for Compressed Video Format.
        if self.hf_vsdb_parser.is_fast_v_active_supported is True:
            fva_factor = 1

        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)
        if color_format == ColorFormat.RGB or color_format == ColorFormat.YUV444:
            slice_adjust = 1
        elif color_format == ColorFormat.YUV422 or color_format == ColorFormat.YUV420:
            slice_adjust = 0.5

        pixel_clock_mhz = (fva_factor * self.timing_info.targetPixelRate) / 1000000
        if slice_adjust * pixel_clock_mhz <= 2720:
            min_slice_count = (slice_adjust * pixel_clock_mhz) / 340
        else:
            min_slice_count = (slice_adjust * pixel_clock_mhz) / 400

        logging.info("Minimum Needed Slice Count based on Pixel Rate As Per Spec: {}".format(min_slice_count))

        return min_slice_count

    ##
    # @brief        Slice Width Should not Exceed Max Slice Width Supported by HDMI2.1 spec which is 2720. So, Optimal
    #               Slice Count has to to be Identified by iterating until we arrive at a slice width less than or equal
    #               to the max slice width supported by HDMI2.1 spec. This Slice Count Should also be Greater than or
    #               Equal to Min Slice Count Calculated Using Peak Pixel Rate.
    # @param[in]    min_slice_count: int
    #                   It's the Minimum Needed Slice Count to Drive the Display which is Computed using PPR
    # @return       max_slice_count: int
    #                   Maximum Valid Slice Count that can be used to driver the panel.
    def _get_max_slice_count(self, min_slice_count: int) -> int:
        panel_supported_slice_count, _ = self.hf_vsdb_parser.dsc_max_slices
        logging.info(f"Panel supported slice count: {panel_supported_slice_count}")

        while True:
            if min_slice_count <= 1:
                slice_target = 1
            elif min_slice_count <= 2:
                slice_target = 2
            elif min_slice_count <= 4:
                slice_target = 4
            elif min_slice_count <= 8:
                slice_target = 8
            elif min_slice_count <= 12:
                slice_target = 12
            elif min_slice_count <= 16:
                slice_target = 16
            else:
                logging.error("VESA DSC1.2a not supported")
                max_slice_count = 0
                break

            slice_width = math.ceil(self.timing_info.hActive / slice_target)

            if slice_width <= 2720:
                max_slice_count = slice_target
                break
            else:
                min_slice_count = slice_target + 1

        if max_slice_count == 0:
            assert True, "[Panel Issue] - Failed to get valid slice count value"

        if panel_supported_slice_count < max_slice_count:
            assert True, "[Panel Issue] - Panel doesn't support the required slice count"

        logging.info("Maximum Possible Slice Count as Per HDMI2.1 + DSC Spec: {}".format(max_slice_count))

        return max_slice_count

    ##
    # @brief        Member function to get the BPP defined as per HDMI2.1 Spec normative Table for some VICs
    # @param[in]    vic_id to get the normative table
    # @param[in]    color_format to get the normative table
    # @return       target_bpp: Returns target BPP(in U64 format) if VIC present in Normative Table, else 0
    def _get_normative_bpp_vic_info(self, vic_id: int, color_format: ColorFormat) -> int:
        vic_dict = {}
        target_bpp = 0

        if color_format == ColorFormat.RGB or color_format == ColorFormat.YUV444:
            vic_dict = NORMATIVE_TABLE_444_BPP
        elif color_format == ColorFormat.YUV420:
            vic_dict = NORMATIVE_TABLE_YUV420_BPP
        elif color_format == color_format.YUV422:
            vic_dict = NORMATIVE_TABLE_YUV422_BPP

        link_rate, lane_count = self.hf_vsdb_parser.dsc_max_frl_rate
        vic_tuple_to_fetch_bpp = (vic_id, link_rate, lane_count)

        for vic_tuple_key, normative_bpp in vic_dict.items():
            # config(VIC_ID, LINK_RAGE_GBPS, LANE_COUNT) mentioned in the max_tb_delta_set is the min supported config for that VIC.
            # All higher configs for that vic will take the same normative BPP
            if vic_tuple_to_fetch_bpp[0] == vic_tuple_key[0]:
                if vic_tuple_to_fetch_bpp[1] >= vic_tuple_key[1] and vic_tuple_to_fetch_bpp[2] >= vic_tuple_key[2]:
                    target_bpp = normative_bpp
                    break

        return target_bpp

    ##
    # @brief        Member function to Get max borrowed tri bytes limit
    # @param[in]    vic_id to get the normative table
    # @param[in]    color_format to get the max tb delta set
    # @return       max_borrowed_tri_bytes: Returns max borrowed tri bytes for current mode
    def _get_max_borrowed_tri_bytes(self, vic_id: int, color_format: ColorFormat) -> int:
        max_tb_delta_set = {}
        max_borrowed_tri_bytes = HDMIDSC.MAX_BORROWED_400_TRI_BYTES

        if color_format == ColorFormat.RGB or color_format == ColorFormat.YUV444:
            max_tb_delta_set = MAX_TB_DELTA_453_BYTES_444_SET
        elif color_format == ColorFormat.YUV420:
            max_tb_delta_set = MAX_TB_DELTA_453_BYTES_YUV420_SET
        elif color_format == color_format.YUV422:
            max_tb_delta_set = MAX_TB_DELTA_453_BYTES_YUV422_SET

        link_rate, lane_count = self.hf_vsdb_parser.dsc_max_frl_rate
        vic_tuple_to_fetch_tb_borrowed = (vic_id, link_rate, lane_count)

        for vic_tuple in max_tb_delta_set:
            # config(VIC_ID, LINK_RAGE_GBPS, LANE_COUNT) mentioned in the max_tb_delta_set is the min supported config
            # for that VIC.All higher configs for that vic will take the same max borrowed tri bytes
            if vic_tuple_to_fetch_tb_borrowed[0] == vic_tuple[0]:
                if vic_tuple_to_fetch_tb_borrowed[1] >= vic_tuple[1] and vic_tuple_to_fetch_tb_borrowed[2] >= vic_tuple[2]:
                    max_borrowed_tri_bytes = HDMIDSC.MAX_BORROWED_453_TRI_BYTES
                    logging.info("Max Tri Bytes borrowed for the VIC: {}".format(max_borrowed_tri_bytes))
                    break

        return max_borrowed_tri_bytes
