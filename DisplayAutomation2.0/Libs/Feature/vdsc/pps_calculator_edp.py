#######################################################################################################################
# @file         pps_calculator_edp.py
# @brief        Contains EdpPictureParameterSetCalculator Used For Calculating DSC Parameters as Per EDP Requirement.
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
from typing import Tuple, List, Dict, Any

from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat
from Libs.Feature.vdsc.dsc_enum_constants import DPCDOffsets, FIXED_POINT_U6_4_CONVERSION, LINE_BUF_DEPTH, TestDataKey
from Libs.Feature.vdsc.dsc_enum_constants import MAX_SLICE_SUPPORTED_HW
from Libs.Feature.vdsc.dsc_definitions import DSCDisplay, BPP
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Feature.vdsc.pps_calculator import PictureParameterSetCalculator


##
# @brief        EdpPictureParameterSetCalculator is Inherited From PictureParameterSetCalculator.
#               It Uses Existing Implementation Present in Base class If the Functionality is Sufficient, Otherwise
#               Overrides it.
class EdpPictureParameterSetCalculator(PictureParameterSetCalculator):

    ##
    # @brief        Initialize the EDP PPS Calculator.
    # @param[in]    edp_dsc_display: DSCDisplay
    #                   Contains Information about the EDP Display For Which PPS Parameter Has to be Calculated.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, edp_dsc_display: DSCDisplay, test_data: Dict[TestDataKey, Any]) -> None:
        super().__init__(edp_dsc_display, test_data)

    ##
    # @brief        Abstract method, to set the info frame header data
    # @return       None
    def _set_info_frame_header(self) -> None:
        # As per DP spec, we need to have fixed header of 0x00, 0x10, 0x7F, 0x00 for PPS DIP packet.
        self._pic_parameter_set.info_frame_header.type = 0x00
        self._pic_parameter_set.info_frame_header.version = 0x10
        self._pic_parameter_set.info_frame_header.length = 0x7F
        self._pic_parameter_set.info_frame_header.checksum = 0x00

    ##
    # @brief    DSC Major and Minor Version is Set Based on the Panel Capability read from DPCD.
    #           Minor Version Might Change Depending on the Hardware Capability.
    # @return   None
    def _set_dsc_major_minor_version(self) -> None:
        reg_value = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_VERSION)[0]
        self._pic_parameter_set.dsc_version_major = DSCHelper.extract_bits(reg_value, 4, 0)
        self._pic_parameter_set.dsc_version_minor = DSCHelper.extract_bits(reg_value, 4, 4)

    ##
    # @brief    Line Buffer Depth is Set Based on the Panel Capability read from DPCD.
    #           LINE_BUF_DEPTH Dict is used to Map the Binary Value to Integer
    # @return   None
    def _set_line_buffer_depth(self) -> None:
        # Hardware Limits the Maximum value to 12 bit depth
        line_buffer_depth = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_LINE_BUFFER_DEPTH)[0]
        self._pic_parameter_set.line_buffer_depth = min(LINE_BUF_DEPTH[line_buffer_depth], 13)

    ##
    # @brief    Block Prediction Enable Status is Set Based on the Panel Capability read from DPCD.
    # @return   None
    def _set_is_block_prediction_enabled(self) -> None:
        # TODO: We need to create DPCD with block predication enabled also as it supported by driver.
        is_bp_supported = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_BLOCK_PREDICTION_SUPPORT)[0]
        self._pic_parameter_set.is_block_prediction_enabled = is_bp_supported

    ##
    # @brief    Pixel Encoding Formats are Updated here Based on the Panel Capability read from DPCD.
    #           RGB, YCbCr 4:4:4, Simple 4:2:2
    #           YCbCr Native 4:2:2, Native 4:2:0 - Supported in DSC 1.2a and Higher
    # @return   None
    def _set_color_format_support(self) -> None:
        dsc_color_supported = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_COLOUR_SUPPORTED)[0]
        rgb_support = DSCHelper.extract_bits(dsc_color_supported, 1, 0)
        ycbcr_444_support = DSCHelper.extract_bits(dsc_color_supported, 1, 1)
        ycbcr_native_422_support = DSCHelper.extract_bits(dsc_color_supported, 1, 3)
        ycbcr_native_420_support = DSCHelper.extract_bits(dsc_color_supported, 1, 4)

        self._pic_parameter_set.simple_422 = 0  # Not supported by driver

        color_format: ColorFormat = self.test_data.get(TestDataKey.COLOR_FORMAT)
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
            logging.debug("Color Format: {}".format(color_format))
            raise AssertionError("Invalid Case")

    ##
    # @brief        For EDP Compression BPP is Programmed Based on the DPCD Register Value. Hence Read the DPCD Value
    #               And Set the Expected BPP.
    # @return   None
    def _set_compression_bpp(self) -> None:
        byte_array = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_MAX_BPP_SUPPORTED_SINK_1, size=2)
        max_supported_by_sink = int('{:x}'.format(0b00000011 & byte_array[-1]) + '{:x}'.format(byte_array[0]), 16)
        if max_supported_by_sink > 15 * FIXED_POINT_U6_4_CONVERSION:
            max_supported_by_sink = 15 * FIXED_POINT_U6_4_CONVERSION

        # BPP will be stored in U6.4 format. 6 integral and 4 fractional.
        self._pic_parameter_set.bits_per_pixel = BPP(value=max_supported_by_sink)

    ##
    # @brief    Bits Per Component is Set by Reading the Programmed Value in Registry. If Registry value is Not
    #           Programmed Default Value of 8 is Set.
    # @return   None
    def _set_bits_per_component(self) -> None:
        bpc: int = DSCHelper.get_bpc_from_registry(self.gfx_index)
        self._pic_parameter_set.bits_per_component = 8 if bpc == 0 else bpc

    ##
    # @brief    For EDP Slice count is Calculated by Finding the Max Slice Supported by the Sink.
    #           Then Find the Min Slice Count between the max Slice Count Supported by the Sink and Max Slice Count
    #           Supported by the Hardware.
    # @return   None
    def _set_slice_count(self) -> None:
        supported_slice_list, max_slices_per_line = self._get_supported_slice_list()

        valid_slice_count = min(MAX_SLICE_SUPPORTED_HW, max_slices_per_line)
        logging.debug("Final Valid Slice Count After Considering H/W Limitation: {}".format(valid_slice_count))

        self._pic_parameter_set.slice_count = valid_slice_count

        # Update No of VDSC Instance to 1 if Slice Count is 1
        if self._pic_parameter_set.slice_count == 1:
            self._pic_parameter_set.vdsc_instances = 1

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
    # @brief    Currently DSC is Enabled by the Driver if the Panel Supports DSC Feature.
    #           DSC Feature Support can be Identified by Reading the Panel Capability From DPCD.
    # @return   None
    def _set_is_dsc_enabled(self) -> None:
        reg_value = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_SUPPORT)[0]
        is_dsc_supported = DSCHelper.extract_bits(reg_value, 1, 0)
        self._pic_parameter_set.is_dsc_enabled = is_dsc_supported

    ##
    # @brief    Returns the List of Slices Supported by the DSC Panel by Reading the DSC Slice Capability Register
    #           Also Computes the Max Slice Count Supported by the DSC Panel.
    # @return   supported_slice_list, max(supported_slice_list): Tuple[List[int], int]
    #               List of Supported Slices by the DSC Panel.
    def _get_supported_slice_list(self) -> Tuple[List[int], int]:
        supported_slice_list: List[int] = []

        slice_caps1 = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_SLICE_CAPABILITIES_1)[0]
        if DSCHelper.extract_bits(slice_caps1, 1, 0) == 1:
            supported_slice_list.append(1)
        if DSCHelper.extract_bits(slice_caps1, 1, 1) == 1:
            supported_slice_list.append(2)
        if DSCHelper.extract_bits(slice_caps1, 1, 3) == 1:
            supported_slice_list.append(4)
        if DSCHelper.extract_bits(slice_caps1, 1, 4) == 1:
            supported_slice_list.append(6)
        if DSCHelper.extract_bits(slice_caps1, 1, 5) == 1:
            supported_slice_list.append(8)
        if DSCHelper.extract_bits(slice_caps1, 1, 6) == 1:
            supported_slice_list.append(10)
        if DSCHelper.extract_bits(slice_caps1, 1, 7) == 1:
            supported_slice_list.append(12)

        # Additional Slice Capabilities for DP Sink Devices.
        slice_caps2 = DSCHelper.read_dpcd(self.gfx_index, self.port, DPCDOffsets.DSC_SLICE_CAPABILITIES_2)[0]
        if DSCHelper.extract_bits(slice_caps2, 1, 0) == 1:
            supported_slice_list.append(16)
        if DSCHelper.extract_bits(slice_caps2, 1, 1) == 1:
            supported_slice_list.append(20)
        if DSCHelper.extract_bits(slice_caps2, 1, 2) == 1:
            supported_slice_list.append(24)

        logging.debug("Panel Supported Slice List: {}".format(supported_slice_list))

        return supported_slice_list, max(supported_slice_list)
