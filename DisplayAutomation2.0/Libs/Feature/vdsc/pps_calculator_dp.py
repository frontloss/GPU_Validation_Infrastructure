#######################################################################################################################
# @file         pps_calculator_dp.py
# @brief        Contains DPictureParameterSetCalculator Used For Calculating DSC Parameters as Per DP Requirement.
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import math
from typing import Any, Dict, Tuple, List

from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Feature.display_audio import DisplayAudio
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_128B_132B_PER_100
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_MST_DSC_PER_100
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_SST_DSC_PER_100
from Libs.Feature.display_port.dp_helper import DPHelper
from Libs.Feature.vdsc.dsc_definitions import DSCDisplay, BPP
from Libs.Feature.vdsc.dsc_enum_constants import FIXED_POINT_U6_4_CONVERSION, DPCDOffsets, MAX_SLICE_SUPPORTED_HW
from Libs.Feature.vdsc.dsc_enum_constants import FRACTIONAL_BPP_UNSUPPORTED_PLATFORMS, DPT_BW_CHECK_REQUIRED_PLATFORMS
from Libs.Feature.vdsc.dsc_enum_constants import MAX_BPP_SUPPORTED_BPP_D13_PLUS, MAX_BPP_SUPPORTED_BPP_PRE_D13
from Libs.Feature.vdsc.dsc_enum_constants import TestDataKey, DSC_THROUGHPUT_MAPPING, DP_LINK_RATE_DDI_CLK_MAPPING
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Feature.vdsc.pps_calculator_edp import EdpPictureParameterSetCalculator
from registers.mmioregister import MMIORegister


##
# @brief        DpPictureParameterSetCalculator is Inherited From EdpPictureParameterSetCalculator as Most of the
#               PPS Calculation is Same as EDP and Can be Re-Used. Only Functions That are Different For DP is
#               Overridden Here.
class DpPictureParameterSetCalculator(EdpPictureParameterSetCalculator):

    ##
    # @brief        Initialize the DP PPS Calculator.
    # @param[in]    dp_dsc_display: DSCDisplay
    #                   Contains Information about the DP Display For Which PPS Parameter Has to be Calculated.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, dp_dsc_display: DSCDisplay, test_data: Dict[TestDataKey, Any]) -> None:
        super().__init__(dp_dsc_display, test_data)

    ##
    # @brief    Maximum Possible Bits Per Pixel is the Minimum of Maximum Possible Bits Per Pixel on Link, Max Supported
    #           by the Big Joiner RAM
    # @return   None
    def _set_compression_bpp(self) -> None:
        max_dsc_supported_bpp: BPP = BPP()
        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)

        self._set_is_big_joiner_enabled()
        self._set_is_ultra_joiner_enabled()

        min_dsc_bpp = self.get_min_dsc_bpp()
        max_dsc_bpp = self.get_max_dsc_bpp()

        max_dsc_bpp = self.get_max_supported_bpp_on_link(min_dsc_bpp, max_dsc_bpp)

        # BPP will be stored in U6.4 format. 6 integral and 4 fractional.
        max_dsc_supported_bpp.value = max_dsc_bpp

        # For MST BPP is calculated based on the Audio Support.
        if self._display.is_mst_display is True:
            is_audio_capable = DisplayAudio().is_audio_capable(self._display.target_id)
            if is_audio_capable:
                min_bpp, max_bpp = min_dsc_bpp, max_dsc_bpp
                is_mst_dsc_supported_with_audio, min_dsc_bpp = self.is_min_mst_dsc_audio_supported(min_bpp, max_bpp)
                assert is_mst_dsc_supported_with_audio, "Minimum Audio Requirement is Not met for the current DSC mode"

            max_dsc_supported_bpp.value = min_dsc_bpp

        if self._display.is_sst_sbm_display is True:
            max_dsc_supported_bpp.value = max_dsc_bpp

        # Fractional BPP is supported from Gen14 and above.
        dsc_bpp_increment_fields = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_BPP_INCREMENT)[0]
        dsc_bpp_increment = DSCHelper.extract_bits(dsc_bpp_increment_fields, 3, 0)
        is_fractional_bpp_supported: bool = False if dsc_bpp_increment == 4 else True
        logging.info('DSC BPP Increment Field: {}'.format(dsc_bpp_increment))

        # Clear the Fractional part if fractional bpp is not supported by the platform.
        is_fractional_bpp_supported &= self._display.platform not in FRACTIONAL_BPP_UNSUPPORTED_PLATFORMS
        if is_fractional_bpp_supported is False:
            max_dsc_supported_bpp.fractional_part = 0

        if color_format == ColorFormat.YUV420 or color_format == ColorFormat.YUV422:
            logging.info(f"Doubling the BPP since the pixel encoding is {color_format.name}")
            max_dsc_supported_bpp.value = 2 * max_dsc_supported_bpp.value
            min_dsc_bpp = 2 * min_dsc_bpp

        logging.info(f"Final DSC BPP considering all limitations [U6.4 Format]: {max_dsc_supported_bpp.value} "
                     f"({max_dsc_supported_bpp.value / 16})")

        assert max_dsc_supported_bpp.value >= min_dsc_bpp, "DSC is not supported."

        self._pic_parameter_set.bits_per_pixel = max_dsc_supported_bpp

    ##
    # @brief        Gets the minimum possible DSC BPP based on the color formats and hardware restriction on different
    #               platforms.
    # @return       min_dsc_bpp: int
    #                   Returns the minimum possible DSC BPP [U6.4 Format]
    def get_min_dsc_bpp(self) -> int:
        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)
        min_dsc_bpp = DSCHelper.get_min_dsc_bpp_for_pixel_encoding(color_format)

        if (self._display.is_mst_display or self._display.is_sst_sbm_display) and color_format == ColorFormat.RGB:
            is_mst_dsc_wa_not_implemented_platform = DSCHelper.is_dsc_hw_improvements_not_implemented_platform(
                self.gfx_index, self._display.platform
            )

            # Assign min DSC bpp as 10 if platform doesn't implement the MST DSC HW WA.
            if is_mst_dsc_wa_not_implemented_platform is True:
                min_dsc_bpp = 10 * FIXED_POINT_U6_4_CONVERSION

        logging.info(f"Minimum Possible DSC BPP [U6.4 Format]: {min_dsc_bpp}")

        return min_dsc_bpp

    ##
    # @brief        Gets the maximum possible DSC BPP based on the color formats, link bandwidth and other hardware
    #               restrictions.
    # @return       max_dsc_bpp: int
    #                   Returns the maximum possible DSC BPP [U6.4 Format]
    def get_max_dsc_bpp(self) -> int:
        bpc = self._pic_parameter_set.bits_per_component
        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)

        max_bpp_on_link = self.get_max_bpp_supported_on_link()
        max_supported_by_hardware = self.get_max_bpp_supported_by_hardware()
        max_possible_bpp_from_color_format = DSCHelper.get_max_dsc_bpp_for_pixel_encoding(color_format, bpc)

        max_dsc_bpp = min(max_bpp_on_link, max_supported_by_hardware, max_possible_bpp_from_color_format)

        logging.info(f"Maximum Possible DSC BPP [U6.4 Format]: {max_dsc_bpp}")

        return max_dsc_bpp

    ##
    # @brief        Member function to get the maximum BPP supported by the hardware. Hardware here includes the
    #               panel, our internal DSC related HW. It also considers platform limitation.
    # @return       max_supported_bpp: int [U6.4 Format]
    #                   Returns the maximum bpp supported by the platform
    def get_max_bpp_supported_by_hardware(self) -> int:
        max_bpp_supported_by_ultra_joiner = max_bpp_supported_by_big_joiner = max_bpp_supported_by_dpt = 0xFFF

        link_rate: float = dpcd_helper.DPCD_getLinkRate(self.target_id)
        lane_count: int = dpcd_helper.DPCD_getNumOfLanes(self.target_id)
        target_pixel_rate = self.timing_info.targetPixelRate

        system_clock = DSCHelper.get_system_clock(self.gfx_index)

        # Optimal cd clock is used to calculate big joiner bpp for all platforms except LNL.
        optimal_cd_clock_mhz = system_clock.get_optimal_cdclock(self.gfx_index, [self._display.port_name])
        optimal_cd_clock_hz = optimal_cd_clock_mhz * 1000000

        if self._display.platform in ["DG2", "ADLP", "MTL", "ELG", "LNL", "PTL", "NVL", "CLS"]:
            small_joiner_ram_bits = 17280 * 8
            big_joiner_bits = 36
            max_output_compressed_bpp = MAX_BPP_SUPPORTED_BPP_D13_PLUS
        else:
            small_joiner_ram_bits = 7680 * 8
            big_joiner_bits = 24
            max_output_compressed_bpp = MAX_BPP_SUPPORTED_BPP_PRE_D13

        # Get Max BPP Supported by the Sink.
        byte_array = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_MAX_BPP_SUPPORTED_SINK_1, size=2)
        max_bpp_supported_by_sink = int('{:x}'.format(0b00000011 & byte_array[-1]) + '{:x}'.format(byte_array[0]), 16)
        logging.info("Max BPP Supported by the Sink: {}".format(max_bpp_supported_by_sink))

        if max_bpp_supported_by_sink == 0:
            max_bpp_supported_by_sink = max_output_compressed_bpp

        if self.is_big_joiner_enabled is True:
            max_bpp_supported_by_small_joiner = (2 * small_joiner_ram_bits) / self.timing_info.hActive
            max_bpp_supported_by_small_joiner = int(max_bpp_supported_by_small_joiner * FIXED_POINT_U6_4_CONVERSION)
            max_bpp_supported_by_big_joiner = (2 * optimal_cd_clock_hz * big_joiner_bits) / target_pixel_rate
            max_bpp_supported_by_big_joiner = int(max_bpp_supported_by_big_joiner * FIXED_POINT_U6_4_CONVERSION)
        else:
            max_bpp_supported_by_small_joiner = small_joiner_ram_bits / self.timing_info.hActive
            max_bpp_supported_by_small_joiner = int(max_bpp_supported_by_small_joiner * FIXED_POINT_U6_4_CONVERSION)

        if self._display.platform in DPT_BW_CHECK_REQUIRED_PLATFORMS:
            ddi_clock_hz = DP_LINK_RATE_DDI_CLK_MAPPING[link_rate] * 1000000
            max_bpp_supported_by_dpt = int(((ddi_clock_hz * 9 * 8) / target_pixel_rate) * FIXED_POINT_U6_4_CONVERSION)
            logging.info(f"Max BPP Supported by DPT: {max_bpp_supported_by_dpt}")

            link_rate_mbps = int(link_rate * 1000)
            logging.info(f"Timing: {self.timing_info.to_string()}")
            if link_rate_mbps > 8100:
                if DPHelper.is_h_blank_less_than_1_mtp(self.timing_info.targetPixelRate, self.timing_info.hTotal,
                                                       self.timing_info.hActive, link_rate_mbps, lane_count):
                    max_bpp_supported_by_dpt = int((max_bpp_supported_by_dpt * 85) / 100)

        if self._is_ultra_joiner_enabled is True:
            ultra_joiner_ram_bits = 4 * 72 * 512
            max_bpp_supported_by_ultra_joiner = ultra_joiner_ram_bits / self.timing_info.hActive
            max_bpp_supported_by_ultra_joiner = int(max_bpp_supported_by_ultra_joiner * FIXED_POINT_U6_4_CONVERSION)

        logging.info(f"Max BPP Supported by DPT: {max_bpp_supported_by_dpt}")
        logging.info(f"Max BPP Supported by Joiner RAM: {max_bpp_supported_by_small_joiner}")
        logging.info(f"Max Bpp Supported by Big Joiner: {max_bpp_supported_by_big_joiner}")
        logging.info(f"Max BPP Supported by Ultra Joiner: {max_bpp_supported_by_ultra_joiner}")

        # BPP will be stored in U6.4 format. 6 integral and 4 fractional.
        max_supported_bpp = min(max_output_compressed_bpp, max_bpp_supported_by_sink)
        max_supported_bpp = min(max_supported_bpp, max_bpp_supported_by_small_joiner)
        max_supported_bpp = min(max_supported_bpp, max_bpp_supported_by_big_joiner)
        max_supported_bpp = min(max_supported_bpp, max_bpp_supported_by_ultra_joiner)
        max_supported_bpp = min(max_supported_bpp, max_bpp_supported_by_dpt)

        logging.info(f"Max DSC BPP Supported by HW [U6.4 Format]: {max_supported_bpp}")

        return max_supported_bpp

    ##
    # @brief        Member function to calculate the maximum BPP that is possible on the link based on the link rate,
    #               lane count, bandwidth efficiency
    # @return       max_bpp_on_link: int
    #                   Return the maximum bpp possible on the link in U6.4 Format
    def get_max_bpp_supported_on_link(self) -> int:
        link_rate: float = dpcd_helper.DPCD_getLinkRate(self.target_id)
        logging.debug('Link Rate Trained by Driver: {}'.format(link_rate))

        reg_value = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.MAX_LANE_COUNT)[0]
        max_lane_count = DSCHelper.extract_bits(reg_value, 5, 0)
        logging.debug('Max Lane Count Supported by the Panel: {}'.format(max_lane_count))

        # Available Link Bandwidth = NumberOfLanes * LinkSymbolClock * ((100 - FECOverhead) / 100) * (TimeSlotsPerMTP)
        # for SST-> FECOverhead = 2.4%,, TimeSlotsPerMTP is 1.
        # for MST-> FECOverhead = 2.4% + 1.562% (MST Overhead), TimeSlotsPerMTP is 64
        # bandwidth_efficiency for 128b/132b encoding is 96.71% (for UHBR+ link rates channel encoding is 128b/132b)
        if link_rate >= 10:
            bandwidth_efficiency = DP_DATA_BW_EFFICIENCY_128B_132B_PER_100
        else:
            is_sbm_supported = self._display.is_mst_display or self._display.is_sst_sbm_display
            bandwidth_efficiency = (DP_DATA_BW_EFFICIENCY_MST_DSC_PER_100 if is_sbm_supported is True else
                                    DP_DATA_BW_EFFICIENCY_SST_DSC_PER_100)
        logging.debug('Bandwidth Efficiency : {}'.format(bandwidth_efficiency))

        """
            available_link_bw_Gbps = ((max_lane_count * link_rate_Gbps * bandwidth_efficiency) / 100)
            available_link_bw_Mbps = available_link_bw_Gbps * 1000 * bandwidth_efficiency
            available_link_bw_kbps = available_link_bw_Mbps * 1000 * bandwidth_efficiency
        """
        available_link_bw_kbps: int = int((max_lane_count * link_rate * 1000000 * bandwidth_efficiency) / 100)
        logging.debug('Available Link Bandwidth[Kbps]: {}'.format(available_link_bw_kbps))

        target_pixel_rate = self.timing_info.targetPixelRate

        # Multiply 16 to keep U6.4 format
        max_bpp_on_link: int = available_link_bw_kbps * FIXED_POINT_U6_4_CONVERSION
        max_bpp_on_link = int(max_bpp_on_link / (target_pixel_rate / 1000))

        logging.info(f"Maximum BPP Possible On Link Considering only Efficiency [U6.4 Format]: {max_bpp_on_link}")

        return max_bpp_on_link

    ##
    # @brief        This function helps to compute the max DSC BPP on link considering all the overheads related to MST.
    # @param[in]    min_dsc_bpp: int
    #                   Minimum required BPP to enabled DSC for the given mode.
    # @param[in]    max_dsc_bpp_on_link: int
    #                   Maximum possible BPP on link considering only the bandwidth efficiency
    # @return       max_dsc_bpp_on_link: int
    #                   Maximum possible BPP on link considering all the overheads related to MST
    def get_max_supported_bpp_on_link(self, min_dsc_bpp: int, max_dsc_bpp_on_link: int) -> int:
        bpp_decrement = 1
        status = False
        pixel_clock_hz = self.timing_info.targetPixelRate
        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)

        link_rate_mbps: int = int(dpcd_helper.DPCD_getLinkRate(self.target_id) * 1000)
        lane_count: int = dpcd_helper.DPCD_getNumOfLanes(self.target_id)
        is_128b_132b_encoding = True if link_rate_mbps >= 10000 else False

        is_dsc_hw_improvements_not_implemented = DSCHelper.is_dsc_hw_improvements_not_implemented_platform(
            self.gfx_index, self._display.platform
        )

        while max_dsc_bpp_on_link >= min_dsc_bpp:
            display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info_ex(self.port, self.gfx_index)

            if is_128b_132b_encoding is True or is_dsc_hw_improvements_not_implemented is False:
                status, *mn_tuple = DPHelper.get_link_data_m_n_values_considering_eoc(
                    display_and_adapter_info, self._display.pipe_list[0], self.timing_info.hActive, pixel_clock_hz,
                    max_dsc_bpp_on_link
                )

                if is_128b_132b_encoding and self._display.platform in DPT_BW_CHECK_REQUIRED_PLATFORMS and status:
                    result = DPHelper.is_h_blank_less_than_1_mtp(self.timing_info.targetPixelRate,
                                                                 self.timing_info.hTotal, self.timing_info.hActive,
                                                                 link_rate_mbps, lane_count)
                    if result is False:
                        status = self.handle_dpt_limitation(lane_count, mn_tuple[2], mn_tuple[3], max_dsc_bpp_on_link)

            elif self._display.is_mst_display is True:
                status, *mn_tuple = DPHelper.get_mst_link_data_m_n_values(
                    display_and_adapter_info, pixel_clock_hz, max_dsc_bpp_on_link
                )
            else:
                bits_per_pixel, bytes_per_pixel = DPHelper.get_bits_and_bytes_per_pixel(
                    self.gfx_index, self._display.pipe_list[0], self._pic_parameter_set.bits_per_component,
                    color_format, True
                )
                status, *mn_tuple = DPHelper.get_sst_link_data_mn_values(
                    display_and_adapter_info, self._display.pipe_list[0], pixel_clock_hz, color_format,
                    self._pic_parameter_set.bits_per_component, bytes_per_pixel, bits_per_pixel
                )

            if status is True:
                break

            max_dsc_bpp_on_link -= bpp_decrement

        if status is False:
            max_dsc_bpp_on_link = 0
            assert True, "[Driver Issue] - Couldn't find Valid BPP"

        logging.info(f'Maximum MST DSC BPP Possible On Link [U6.4 Format]: {max_dsc_bpp_on_link}')

        return max_dsc_bpp_on_link

    ##
    # @brief        Checks if min audio is supported with MST + DSC
    # @param[in]    min_dsc_bpp: int [U6.4 Format]
    #                   It's the minimum bpp with which DSC will be supported.
    # @param[in]    max_dsc_bpp: int [U6.4 Format]
    #                   It's the maximum bpp that can be supported considering all the limitations.
    # @return       is_min_audio_supported, min_supported_bpp : Tuple [bool, int]
    #                   is_audio_supported - True if audio is supported with DSC, False otherwise
    #                   min_dsc_bpp - Min BPP that is required to support audio
    def is_min_mst_dsc_audio_supported(self, min_dsc_bpp: int, max_dsc_bpp: int) -> Tuple[bool, int]:
        while min_dsc_bpp <= max_dsc_bpp:
            is_audio_supported = self.is_audio_supported_with_mst_dsc(min_dsc_bpp, 48, 2)
            if is_audio_supported is True:
                break

            # Increment by 1/16 precision
            min_dsc_bpp = min_dsc_bpp + FIXED_POINT_U6_4_CONVERSION

        is_audio_supported = min_dsc_bpp <= max_dsc_bpp

        logging.info(f"Is Min Audio Supported with MST DSC: {is_audio_supported}, DSC BPP [U6.4 Format]: {min_dsc_bpp}")

        return is_audio_supported, min_dsc_bpp

    ##
    # @brief    Slice Count is Set by Calculating the Minimum Slice Count Needed for Peak Pixel Rate.
    #           This Min Slice Count is used to Get the Valid Slice Count as Supported by the DSC Panel.
    #           Then Find the Min Slice Count between the Obtained Min Slice Count and Max H/W Supported Slice Count.
    # @return   None
    def _set_slice_count(self) -> None:
        supported_slice_list, max_slices_per_line = self._get_supported_slice_list()
        min_slice_count: int = self._get_min_slice_count_from_ppr(max_slices_per_line)
        valid_slice_count: int = self._get_valid_slice_count(supported_slice_list, max_slices_per_line, min_slice_count)

        valid_slice_count = min(MAX_SLICE_SUPPORTED_HW, valid_slice_count)
        logging.debug("Final Valid Slice Count After Considering H/W Limitation: {}".format(valid_slice_count))

        self._pic_parameter_set.slice_count = valid_slice_count

        # Update No of Vdsc Instances to 12 if and only if slice count is 12
        # 3 DSC Engine per pipe will be enabled only in this case.
        if self._pic_parameter_set.slice_count == 12:
            self._pic_parameter_set.vdsc_instances = 12

        # Update No of VDSC Instance to 1 if and only if slice count is 1
        # 1 DSC Engine only will be enabled when slice count is 1
        if self._pic_parameter_set.slice_count == 1:
            self._pic_parameter_set.vdsc_instances = 1

    ##
    # @brief        Calculate the Minimum Needed Slice Count for the Peak Pixel Rate of the Display.
    # @param[in]    max_slices_per_line: int
    #                   Indicates the maximum slices per line supported by the panel
    # @return       min_slice_count: int
    #                   Returns the minimum no of slice a frame has to be divided based on the pixel clock.
    def _get_min_slice_count_from_ppr(self, max_slices_per_line: int) -> int:
        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)

        # Peak Pixel Rate(PPR) = HTotal * VTotal*FrameRate  PPR is nothing but pixel clock. (in MP / s)
        ppr_in_khz: int = self.timing_info.targetPixelRate // 1000

        # https://swecore.amr.corp.intel.com/embargoed/display/vdsc_hld.html
        if ppr_in_khz <= 2720000:
            min_slice_count: int = math.ceil((ppr_in_khz / 340000))
            # For Peak Pixel Rates less than 340, MinSliceCount will come as 1 which will pose restriction on CD_CLK
            # If we use 1 Slice Count, one DSC instance must be used, which will pose bottleneck in the display pipeline
            # (max pixel clock <= 1 * CD_CLK when one DSC instance is used)
            # Hence always choose MinSliceCount >= 2 for external DP Display whenever panels supports more than 1 slice.
            if max_slices_per_line > 1:
                min_slice_count = max(min_slice_count, 2)
        elif ppr_in_khz <= 4800000:
            min_slice_count: int = math.ceil((ppr_in_khz / 400000))
        else:
            # As per DP 2.0 SCR, if ppr is > 4800, then spec mandates to support minimum of 600 MP/S DSC peak
            # throughput.
            min_slice_count: int = math.ceil((ppr_in_khz / 600000))

        # Choose alternate slice count only when the sink supports Native 420/Native 422.
        # Also sink shouldn't support RGB or simple 4:2:2 or YUV 4:4:4
        # Alternate slice doesn't apply for UHBR link rates as spec mandates RGB support with UHBR link rates.
        # So any YUV mode will have a corresponding RGB modes. Hence, alternate slice/display is not required.
        link_rate: float = dpcd_helper.DPCD_getLinkRate(self.target_id)
        if link_rate < 10 and ((color_format == ColorFormat.YUV420) or (color_format == color_format.YUV422)):
            dsc_color_supported = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_COLOUR_SUPPORTED)[0]
            rgb_support = bool(DSCHelper.extract_bits(dsc_color_supported, 1, 0))
            ycbcr_444_support = bool(DSCHelper.extract_bits(dsc_color_supported, 1, 1))
            if rgb_support is False and ycbcr_444_support is False:
                min_slice_count = math.ceil(min_slice_count / 2)

        peak_dsc_throughput = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_PEAK_DSC_THROUGHPUT)[0]
        throughput_mode_0 = DSCHelper.extract_bits(peak_dsc_throughput, 4, 0)
        throughput_mode_0 = DSC_THROUGHPUT_MAPPING[throughput_mode_0]
        logging.debug('PEAK_DSC_THROUGHPUT.throughput_mode_0: {}'.format(throughput_mode_0))

        if throughput_mode_0 >= 400:
            slice_count_from_throughput: int = ppr_in_khz / (throughput_mode_0 * 1000)
            slice_count_from_throughput = max(self._pic_parameter_set.vdsc_instances, slice_count_from_throughput)
            min_slice_count = min(min_slice_count, slice_count_from_throughput)

        logging.debug("Minimum Needed Slice Count based on Pixel Rate As Per Spec: {}".format(min_slice_count))

        return min_slice_count

    ##
    # @brief        Slice Width Should not Exceed Max Slice Width Supported by the Panel. So, Optimal Slice Count has to
    #               be Identified from the List of Supported Slices. This Slice Count Should also be Greater than or
    #               Equal to Min Slice Count Calculated Using Peak Pixel Rate.
    # @param[in]    supported_slice_list: List[int]
    #                   List of Supported Slices by the DSC Panel.
    # @param[in]    max_slice_count: int
    #                   Maximum slice count supported by the DSC Panel
    # @param[in]    min_slice_count: int
    #                   It's the minimum required Slice Count to Drive the Display which is Computed using PPR
    # @return       valid_slice_count: int
    #                   Minimum Valid Slice Count Supported by the Panel.
    def _get_valid_slice_count(self, supported_slice_list: List[int], max_slice_count: int,
                               min_slice_count: int) -> int:
        valid_slice_count: int = 0

        for slice_value in supported_slice_list:
            if slice_value >= min_slice_count <= max_slice_count:
                valid_slice_count = slice_value
                break

        # To get the Actual Max Slice Width, the DPCD Value Has to be Multiplied by 320
        # Check ox6cH DPCD Register for More Information
        max_slice_width = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_MAX_SLICE_WIDTH)[0]
        max_slice_width = max_slice_width * 320
        logging.debug('Max Slice Width Supported by DSC Panel: {}'.format(max_slice_width))

        # If Slice Width is Greater than the Max Slice Width, Next Higher Allowed Slice Count Should be used in Place.
        # This Adjustment Repeats Until the Slice Width is Less than or Equal to the Max Slice Width Supported by the
        # Panel.
        if max_slice_width != 0:
            for slice_value in supported_slice_list:
                if slice_value >= min_slice_count <= max_slice_count:
                    slice_width = self.timing_info.hActive // slice_value
                    if slice_width <= max_slice_width:
                        valid_slice_count = slice_value
                        break

        if valid_slice_count == 0:
            assert False, "Failed to get valid slice count value"

        logging.debug("Maximum Possible Slice Count as Per DSC Spec: {}".format(valid_slice_count))

        return valid_slice_count

    ##
    # @brief        Function that helps to check if given audio frequency and channels can be supported with the given
    #               output dsc bpp
    #               Refer Audio Bandwidth Checks Section - https://gfxspecs.intel.com/Predator/Home/Index/67768
    # @param[in]    output_dsc_bpp: int
    #                   DSC BPP for which we need to check if audio can be supported
    # @param[in]    audio_khz: int
    #                   Audio Frequency to be used to check if audio can be supported with that frequency in KHz
    # @param[in]    no_of_audio_channels: int
    #                   No Of Audio Channels used to check if audio can be supported with those no of channels
    # @return       is_audio_supported: bool
    #                   Returns True if Audio can be transmitted within the HBlank else False
    def is_audio_supported_with_mst_dsc(self, output_dsc_bpp: int, audio_khz: int, no_of_audio_channels: int) -> bool:
        mtp_size_clks = 64
        link_overhead = 0.03
        h_blank_bytes_avail_overhead = 48
        h_blank_bytes_req_overhead = 56

        link_rate_gbps = dpcd_helper.DPCD_getLinkRate(self.target_id)
        reg_value = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.MAX_LANE_COUNT)[0]
        max_lane_count = DSCHelper.extract_bits(reg_value, 5, 0)

        h_blank = self.timing_info.hTotal - self.timing_info.hActive
        pixel_clock_mhz = self.timing_info.targetPixelRate / 1000000

        link_clk_mhz = (link_rate_gbps / 10) * 1000
        line_freq_khz = (pixel_clock_mhz / self.timing_info.hTotal) * 1000

        pixel_bw_gbps = (pixel_clock_mhz * (output_dsc_bpp / (8 * FIXED_POINT_U6_4_CONVERSION))) / 1000
        link_bw_gbps = ((link_clk_mhz * max_lane_count) * (1 - link_overhead)) / 1000
        mtp_size_ns = (mtp_size_clks / link_clk_mhz) * 1000
        h_blank_size_ns = (h_blank / pixel_clock_mhz) * 1000
        vc_slots = math.ceil(64 * (pixel_bw_gbps / link_bw_gbps))
        audio_samples_per_line = math.ceil(audio_khz / line_freq_khz) + 1

        is_wa_not_implemented = DSCHelper.is_dsc_hw_improvements_not_implemented_platform(
            self.gfx_index, self._display.platform
        )

        if is_wa_not_implemented is True:
            h_blank_reduced_ns = h_blank_size_ns - (((64 - vc_slots) / link_clk_mhz) * 1000)
            h_blank_slots_full_mtps = math.floor(h_blank_reduced_ns / mtp_size_ns) * vc_slots
            h_blank_slots_partial_mtps = math.ceil(((h_blank_reduced_ns % mtp_size_ns) * link_clk_mhz)) / 1000
            h_blank_slots_partial_mtps = min(h_blank_slots_partial_mtps, vc_slots)
            h_blank_slots = h_blank_slots_full_mtps + h_blank_slots_partial_mtps
        else:
            h_blank_bytes_avail_overhead = 16
            h_blank_bytes_req_overhead = 0

            data_m_register = "TRANS_DATAM1_" + self._display.transcoder_list[0]
            data_m = MMIORegister.read("DATAM_REGISTER", data_m_register, self._display.platform,
                                       gfx_index=self.gfx_index)

            data_n_register = "TRANS_DATAN1_" + self._display.transcoder_list[0]
            data_n = MMIORegister.read("DATAN_REGISTER", data_n_register, self._display.platform,
                                       gfx_index=self.gfx_index)

            mtps_in_h_blank = h_blank_size_ns / mtp_size_ns
            h_blank_slots = math.floor(mtps_in_h_blank * mtp_size_clks * (data_m.data_m_value / data_n.data_n_value))

        h_blank_bytes_available = (h_blank_slots * max_lane_count) - h_blank_bytes_avail_overhead

        if no_of_audio_channels > 2:
            h_blank_bytes_required = (audio_samples_per_line * 10 + 4) * 4 + h_blank_bytes_req_overhead
        else:
            h_blank_bytes_required = (math.ceil(audio_samples_per_line / 2) * 5 + 4) * 4 + h_blank_bytes_req_overhead

        is_audio_supported = True if h_blank_bytes_available > h_blank_bytes_required else False
        logging.debug(f"Audio Frequency: {audio_khz}KHz, Channels: {no_of_audio_channels} : {is_audio_supported}")

        return is_audio_supported

    ##
    # @brief        Function to know the computed DSC bpp is possible without causing underrun or corruption because of.
    #               DPT HW restriction.
    # @param[in]     lane_count: int
    # @param[in]     data_m: int
    # @param[in]     data_n: int
    # @param[in]     bpp: int
    #                   BPP in U6.4 Format
    # @return       Returns True if the DSC bpp is supported by the DPT HW else False.
    def handle_dpt_limitation(self, lane_count: int, data_m: int, data_n: int, bpp: int) -> bool:
        is_possible = True

        transfer_unit = int(math.ceil(data_m * 64 / data_n))
        logging.info(f"data_m: {data_m}, data_n: {data_n}, Transfer unit: {transfer_unit}")
        logging.info(f"slice_count: {self._pic_parameter_set.slice_count}")

        if lane_count == 4 and transfer_unit > 32:
            chunk_size = math.ceil((self._pic_parameter_set.slice_width * bpp) / (8 * FIXED_POINT_U6_4_CONVERSION))
            compressed_bytes_in_frame = chunk_size * self._pic_parameter_set.slice_count
            diff_in_vc_slots = transfer_unit - 32
            max_supported_compressed_bytes = int((64 * transfer_unit * 16) / diff_in_vc_slots)

            if max_supported_compressed_bytes < compressed_bytes_in_frame:
                is_possible = False

        return is_possible
