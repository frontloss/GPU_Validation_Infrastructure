#######################################################################################################################
# @file         pps_calculator_mipi.py
# @brief        Contains MipiPictureParameterSetCalculator Used For Calculating DSC Parameters as Per MIPI.
#
# @author       Praburaj Krishnan
#######################################################################################################################
import math
from typing import Dict, Any

from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Feature.vdsc.dsc_enum_constants import TestDataKey
from Libs.Feature.mipi.mipi_helper import MipiHelper
from Libs.Feature.vdsc import dsc_enum_constants as dsc_args
from Libs.Feature.vdsc.dsc_definitions import DSCDisplay, BPP
from Libs.Feature.vdsc.pps_calculator import PictureParameterSetCalculator


##
# @brief        MipiPictureParameterSetCalculator is Inherited From PictureParameterSetCalculator and Most Of the
#               MIPI Expected PPS Parameters are Read From VBT or Calculated Using the VBT Fields.
class MipiPictureParameterSetCalculator(PictureParameterSetCalculator):

    def _set_info_frame_header(self) -> None:
        pass

    ##
    # @brief        Initialize the MIPI PPS Calculator.
    # @param[in]    mipi_dsc_display: DSCDisplay
    #                   Contains Information about the MIPI Display For Which PPS Parameter Has to be Calculated.
    # @param[in]    test_data: Dict[TestDataKey, Any]
    #                   Contains any data that is needed for verification from the test scripts can be passed using this
    #                   dictionary. Key has to be of type TestDataKey. Value can be anything.
    def __init__(self, mipi_dsc_display: DSCDisplay, test_data: Dict[TestDataKey, Any]):
        super().__init__(mipi_dsc_display, test_data)
        self._mipi_helper = MipiHelper(self._display.platform.lower())
        self._mipi_panel_index: int = self.get_mipi_panel_index()
        self._vbt_block_56 = self._mipi_helper.gfx_vbt.block_56.CompressionParamDataStructEntry[self._mipi_panel_index]
        self._vbt_block_2 = self._mipi_helper.gfx_vbt.block_2.DisplayDeviceDataStructureEntry[self._mipi_panel_index]

    ##
    # @brief        Get MIPI Panel Index Using the Target ID of the Display.
    # @return       panel_index: int
    #                   Panel1 Index is Retrieved From MIPI Helper and Returned If Port Type is MIPI_A,
    #                   Panel2 Index Otherwise.
    def get_mipi_panel_index(self) -> int:
        enum_displays = DisplayConfiguration().get_enumerated_display_info()
        port_target_id_map = dict()
        for display_index in range(enum_displays.Count):
            display = enum_displays.ConnectedDisplays[display_index]
            if self._display.gfx_index == display.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
                port_target_id_map[display.TargetID] = CONNECTOR_PORT_TYPE(display.ConnectorNPortType).name

        port: str = port_target_id_map[self.target_id].lower()
        return self._mipi_helper.panel1_index if 'mipi_a' in port else self._mipi_helper.panel2_index

    ##
    # @brief        Set Major and Minor DSC Version By Reading the VBT Fields.
    # @return       None
    def _set_dsc_major_minor_version(self) -> None:
        major_version: int = self._vbt_block_56.DSCAlgorithmRevision & 0xF
        minor_version: int = (self._vbt_block_56.DSCAlgorithmRevision & 0xF0) >> 4

        self._pic_parameter_set.dsc_version_major = major_version
        self._pic_parameter_set.dsc_version_minor = minor_version

    ##
    # @brief        Set Bits Per Component By Reading the VBT Field.
    # @return       None
    def _set_bits_per_component(self) -> None:
        self._pic_parameter_set.bits_per_component = self._mipi_helper.get_bpp(self._mipi_panel_index) // 3

    ##
    # @brief        Set Line Buffer Depth By Reading the VBT Field and Mapping the VBT Field Value to Equivalent Line
    #               Buffer Depth Value.
    # @return       None
    def _set_line_buffer_depth(self) -> None:
        self._pic_parameter_set.line_buffer_depth = dsc_args.LINE_BUF_DEPTH[self._vbt_block_56.DSCLineBufferDepth - 1]

    ##
    # @brief        Set Is Block Prediction Enabled By Reading the VBT Field Block Prediction Enable.
    # @return       None
    def _set_is_block_prediction_enabled(self) -> None:
        # @TODO: We need to create DPCD with block predication enabled also as it supported by driver.
        self._pic_parameter_set.is_block_prediction_enabled = self._vbt_block_56.BlockPredictionEnable

    ##
    # @brief        Set Color Format To RGB As Current Driver Supports Only RGB
    # @return       None
    def _set_color_format_support(self) -> None:
        # TODO: Need to check what values to set for convert_rgb and simple_422 for MIPI
        self._pic_parameter_set.convert_rgb = 1
        self._pic_parameter_set.simple_422 = 0

    ##
    # @brief        Set Compression BPP By Reading the VBT Field and Mapping to Equivalent BPP Value.
    # @return       None
    def _set_compression_bpp(self) -> None:
        dsc_maximum_bits_per_pixel = self._vbt_block_56.DSCMaximumBitsPerPixel
        dsc_maximum_bits_per_pixel: int = dsc_args.VBT_MAX_BPP_MAPPING[
                                              dsc_maximum_bits_per_pixel] * dsc_args.FIXED_POINT_U6_4_CONVERSION
        self._pic_parameter_set.bits_per_pixel = BPP(value=dsc_maximum_bits_per_pixel)

    ##
    # @brief        Set Slice Count Value By Reading the VBT Field and Mapping to Equivalent Slices Per Line.
    # @return       None
    def _set_slice_count(self) -> None:
        # slices per line is stored as binary number with bit definition as [9:0] representing [24 to 1] slices per line
        # the most significant bit set tells the max slice count supported. Lower bits might also be set,
        # but we should consider most significant bit set. Hence applying log with base 2 and then applying the MAP.
        dsc_slices_per_line = self._vbt_block_56.DSCSlicesPerLine
        slice_count: int = dsc_args.VBT_SLICES_PER_LINE_MAPPING[pow(2, int(math.log(dsc_slices_per_line, 2)))]

        self._pic_parameter_set.slice_count = slice_count

        # Update No of VDSC Instance to 1 if Slice Count is 1
        if self._pic_parameter_set.slice_count == 1:
            self._pic_parameter_set.vdsc_instances = 1

    ##
    # @brief        Set Expected No Of DSC Instance/Engine to be Enabled Based on the Slice Count.
    # @return       None
    def _set_no_of_vdsc_instance(self) -> None:
        self._pic_parameter_set.vdsc_instances = 2

    ##
    # @brief        Pic Width, Height and Slice Width Are Computed in the Base Class as These Fields Follow Same
    #               Logic For Computation Across Different Display Technology.
    #               Slice Height is Overridden With the VBT Field Value.
    # @return       None
    def _set_picture_slice_parameters(self) -> None:
        super()._set_picture_slice_parameters()
        self._pic_parameter_set.slice_height = self._vbt_block_56.DSCSliceHeight

    ##
    # @brief        Set DSC Enable Field by Reading Compression Enable Bit In the VBT.
    # @return       None
    def _set_is_dsc_enabled(self) -> None:
        self._pic_parameter_set.is_dsc_enabled = (1 if self._vbt_block_2.CompressionEnable == 1 else 0)
