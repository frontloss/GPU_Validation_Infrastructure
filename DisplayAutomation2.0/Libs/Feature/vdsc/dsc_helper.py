######################################################################################################################
# @file         dsc_helper.py
# @brief        Contains All the Helper Functions For DSC Tests and Verifiers.
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
from typing import List, Tuple, Optional

import DisplayRegs
from DisplayRegs import DisplayArgs, DisplayRegsService
from DisplayRegs.DisplayOffsets import VideoDataIslandPacketPPSOffsets
from Libs.Core import driver_escape, registry_access, display_essential, display_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo, DisplayTimings
from Libs.Core.logger import gdhm
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.clock.adlp.adlp_clock_base import AdlpClock
from Libs.Feature.clock.adls.adls_clock_base import AdlsClock
from Libs.Feature.clock.dg1.dg1_clock_base import Dg1Clock
from Libs.Feature.clock.dg2.dg2_clock_base import Dg2Clock
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.clock.elg.elg_clock_base import ElgClock
from Libs.Feature.clock.lnl.lnl_clock_base import LnlClock
from Libs.Feature.clock.mtl.mtl_clock_base import MtlClock
from Libs.Feature.clock.nvl.nvl_clock_base import NvlClock
from Libs.Feature.clock.ptl.ptl_clock_base import PtlClock
from Libs.Feature.clock.rkl.rkl_clock_base import RklClock
from Libs.Feature.clock.tgl.tgl_clock_base import TglClock
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_128B_132B_PER_100
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_SST_FEC_PER_100
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_SST_PER_100
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock
from Libs.Feature.powercons import registry
from Libs.Feature.vdsc.dsc_enum_constants import BPC_MAPPING, DPCDOffsets, FIXED_POINT_U6_4_CONVERSION
from Libs.Feature.vdsc.dsc_hw_reg_verifier import PipeDssCtlTwoRegister
from registers.mmioregister import MMIORegister


##
# @brief        Helper class which contains all the DSC related helper methods.
class DSCHelper:
    DISPLAY_HARDWARE_INFO_LIST = SystemInfo().get_gfx_display_hardwareinfo()
    display_config = DisplayConfiguration()
    _DSC_HW_IMPROVEMENTS_NOT_IMPLEMENTED_PLATFORMS = ['TGL', 'RKL', 'ADLS', 'DG1', 'DG2', 'ADLP']

    # Contains the platform names which doesn't support PSR2 + DSC Co-existence from Gen12+ onwards.
    _PSR2_DSC_UNSUPPORTED_PLATFORMS = ['TGL', 'RKL', 'ADLS', 'DG1', 'DG2']

    ##
    # @brief        Class Method to Get if the Panel Plugged in a Particular Port is Capable of DSC.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D'
    # @return       is_dsc_supported: bool
    #                   Returns True if DSC is Supported by the Panel, False Otherwise.
    @classmethod
    def is_vdsc_supported_in_panel(cls, gfx_index: str, port: str) -> bool:
        is_dsc_supported = False
        port = port.upper()

        if 'MIPI' in port:
            gfx_vbt = Vbt()
            panel_index = gfx_vbt.get_lfp_panel_type(port)
            logging.debug(f"Panel Index for {port}= {panel_index}")
            data_structure_entry = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[panel_index]
            is_dsc_supported = True if data_structure_entry.CompressionEnable == 1 else False
        elif 'EDP' in port or 'DP' in port:
            if display_utility.get_vbt_panel_type(port, gfx_index) in [display_utility.VbtPanelType.LFP_DP]:
                reg_value = DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.DPCD_REV)[0]
                if DSCHelper.extract_bits(reg_value, 8, 0) < 0x14:
                    logging.info(
                        f"eDP Panel version is less than 0x14. Hence DSC Support for the panel is {is_dsc_supported}")
                    return is_dsc_supported
            reg_value = DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.DSC_SUPPORT)[0]
            is_dsc_supported = True if DSCHelper.extract_bits(reg_value, 1, 0) == 1 else False
        elif "HDMI" in port:
            hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
            hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, port)
            is_dsc_supported = hf_vsdb_parser.is_dsc_supported

        logging.info(f"Is DSC Supported by the Display on {gfx_index} {port}: {is_dsc_supported}")
        return is_dsc_supported

    ##
    # @brief        Class Method to Check if DSC is Enabled in the Panel by the Driver.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D'
    # @return       is_dsc_enabled: bool
    #                   Returns True if DSC is Enabled On the Panel, False Otherwise.
    @classmethod
    def is_vdsc_enabled_in_panel(cls, gfx_index: str, port: str) -> bool:

        # Check Dsc status in sink
        if 'MIPI' in port:
            is_dsc_enabled = cls.is_vdsc_supported_in_panel(gfx_index, port)
        elif 'EDP' in port or 'DP' in port:
            reg_value = DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.DSC_ENABLE)[0]
            decompression_enable = DSCHelper.extract_bits(reg_value, 1, 0)
            is_dsc_enabled = True if decompression_enable == 1 else False
        else:
            # Not applicable for HDMI displays with DSC support
            raise NotImplementedError("In case of HDMI we don't write anything to the panel")

        logging.info(f"Is DSC Enabled in Display on {gfx_index} {port}: {is_dsc_enabled}")
        return is_dsc_enabled

    ##
    # @brief        Class Method to Get the Available Bandwidth Based on the Link Rate, Lane Count Trained. And also
    #               Considering the Bandwidth Efficiency.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D'
    # @return       available_bw_kbps: int
    #                   Returns the Available Bandwidth in kbps.
    @classmethod
    def get_available_bandwidth(cls, gfx_index: str, port: str) -> int:
        display_and_adapter_info = cls.display_config.get_display_and_adapter_info_ex(port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]

        target_id = display_and_adapter_info.TargetID
        available_bw_kbps = 0

        if 'EDP' in port or 'DP' in port:

            link_rate: float = dpcd_helper.DPCD_getLinkRate(target_id)
            logging.debug('Link Rate Trained by Driver: {}'.format(link_rate))

            reg_value: int = DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.MAX_LANE_COUNT)[0]
            lane_count: int = DSCHelper.extract_bits(reg_value, 5, 0)

            reg_value: int = DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.FEC_CAPABILITY_OFFSET)[0]
            is_fec_capable = bool(DSCHelper.extract_bits(reg_value, 1, 0))

            bandwidth_efficiency = DP_DATA_BW_EFFICIENCY_SST_PER_100
            if (link_rate >= 10) is True:
                bandwidth_efficiency = DP_DATA_BW_EFFICIENCY_128B_132B_PER_100
            elif is_fec_capable is True:
                bandwidth_efficiency = DP_DATA_BW_EFFICIENCY_SST_FEC_PER_100

            logging.debug('Bandwidth Efficiency: {}'.format(bandwidth_efficiency))

            available_bw_gbps = (link_rate * lane_count * bandwidth_efficiency) / 100
            available_bw_mbps = available_bw_gbps * 1000
            available_bw_kbps = int(available_bw_mbps * 1000)
        elif "HDMI" in port:
            hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
            hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, port)
            link_rate, lane_count = hf_vsdb_parser.dsc_max_frl_rate

            # HDMI 2.1 Follows 16b/18b Encoding. Hence, the Bandwidth Efficiency comes around 88.888%
            bandwidth_efficiency = (16 / 18) * 100
            logging.debug('Bandwidth Efficiency: {}'.format(bandwidth_efficiency))

            available_bw_gbps = (link_rate * lane_count * bandwidth_efficiency) / 100
            available_bw_mbps = available_bw_gbps * 1000
            available_bw_kbps = int(available_bw_mbps * 1000)

        logging.info("Available Bandwidth to Drive the Display {} is {}kbps".format(target_id, available_bw_kbps))
        return available_bw_kbps

    ##
    # @brief        Class Method to Get the Required Bandwidth to Drive the Display Using the Display Timing Info.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D'
    # @param[in]    color_format: Optional[ColorFormat]
    #                   Color Format of the mode. Default is RGB
    # @return       required_bit_rate_kbps: int
    #                   Returns the Required Bandwidth in kbps.
    @classmethod
    def get_required_bandwidth(cls, gfx_index: str, port: str,
                               color_format: Optional[ColorFormat] = ColorFormat.RGB) -> int:
        div = 1
        if color_format == ColorFormat.YUV420:
            div = 2
        elif color_format == ColorFormat.YUV422:
            div = 1.5

        display_and_adapter_info = cls.display_config.get_display_and_adapter_info_ex(port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]

        target_id = display_and_adapter_info.TargetID

        timing_info: DisplayTimings = cls.get_display_timing_from_qdc(display_and_adapter_info)

        bpc = cls.get_source_bpc(gfx_index, port)

        required_bit_rate_bps = (timing_info.targetPixelRate * bpc * 3) / div
        required_bit_rate_kbps = int(required_bit_rate_bps / 1000)

        logging.info(f"Required Bandwidth to Drive the Display {target_id} is {required_bit_rate_kbps}kbps")
        return required_bit_rate_kbps

    ##
    # @brief        Class Method to Check if DSC Should be Enabled to Drive the Display.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D'
    # @param[in]    color_format: Optional[ColorFormat]
    #                   Color Format of the mode. Default is RGB
    # @return       is_dsc_required: bool
    #                   Returns True if Required Bandwidth is Higher than the Available Bandwidth, False Otherwise.
    @classmethod
    def is_vdsc_required(cls, gfx_index: str, port: str, color_format: Optional[ColorFormat] = ColorFormat.RGB) -> bool:
        available_bw_kbps: int = cls.get_available_bandwidth(gfx_index, port)
        required_bit_rate_kbps: int = cls.get_required_bandwidth(gfx_index, port, color_format)

        is_dsc_required = False if available_bw_kbps >= required_bit_rate_kbps else True

        _, no_of_pipes = DisplayClock.is_pipe_joiner_required(gfx_index, port)
        if no_of_pipes > 2:
            is_dsc_required = True

        logging.info(f"Is DSC Required to Drive the Display on {gfx_index} {port}: {is_dsc_required}")
        return is_dsc_required

    ##
    # @brief        Class Method to Check if DSC is enabled by the driver for given port
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D', 'COLLAGE_0'
    # @param[in]    collage_child_port : str
    #                   Contains child port of collage.
    # @return       is_dsc_enabled_in_driver: bool
    #                   Returns True if DSC is enabled by the driver for the given port, False otherwise.
    @classmethod
    def is_vdsc_enabled_in_driver(cls, gfx_index: str, port: str, collage_child_port: Optional[str] = None) -> bool:

        # We can't pass collage_child_port to DisplayBase because
        # display_config.get_display_and_adapter_info_ex() is called inside DisplayBase will return none
        # because when collage is enabled collage_child_port (E.g. DP_F,DP_G) will be in inactive state.
        display_base = DisplayBase(port, gfx_index=gfx_index)

        # We can't pass port to GetPipeDDIAttachedToPort() when it is equal to COLLAGE_0
        # because at present the GetPipeDDIAttachedToPort() doesn't handle COLLAGE_0 case.
        # Hence, pipe, ddi, transcoder of collage_child_port is retrieved and VDSC verification is done.
        if collage_child_port is not None:
            port = collage_child_port

        pipe, _, transcoder = display_base.GetPipeDDIAttachedToPort(port, True, gfx_index)
        pipe = pipe[-1].upper()
        index = int(gfx_index[-1])
        platform = DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName

        pipe_dss_ctl2_reg = PipeDssCtlTwoRegister()
        pipe_dss_ctl2_reg.fill_actual_pipe_dss_ctl_two_reg(gfx_index, platform, pipe, transcoder)
        left_vdsc_enable_status = pipe_dss_ctl2_reg.is_left_vdsc_engine_enabled
        right_vdsc_enable_status = pipe_dss_ctl2_reg.is_right_vdsc_engine_enabled

        is_dsc_enabled_in_driver = left_vdsc_enable_status or right_vdsc_enable_status

        logging.info(f"Is DSC Enabled in Driver for Display on {gfx_index} {port}: {is_dsc_enabled_in_driver}")
        return is_dsc_enabled_in_driver

    ##
    # @brief        Class Method to Get the Source BPC Programmed in the Transcoder.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D'
    # @return       bpc: int
    #                   Returns BPC Value Based on the Value Programmed in the Transcoder.
    @classmethod
    def get_source_bpc(cls, gfx_index: str, port: str) -> int:

        display_base = DisplayBase(port)
        _, _, transcoder = display_base.GetPipeDDIAttachedToPort(port, transcoder_mapping_details=True)
        transcoder = transcoder.split('_')[-1].upper()

        offset = 'TRANS_DDI_FUNC_CTL_' + transcoder
        index = int(gfx_index[-1])
        platform_name = DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName
        trans_ddi_func_ctl = MMIORegister.read('TRANS_DDI_FUNC_CTL_REGISTER', offset, platform_name)
        bpc = BPC_MAPPING[trans_ddi_func_ctl.bits_per_color]

        logging.info(f"Transcoder is programmed with BPC value of {bpc}")
        return bpc

    ##
    # @brief        Class Method to Enable/Disable PSR. To Enable DSC, PSR Should be Disabled.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    enable_psr2: bool
    #                   Value True Represents  enable PSR2 feature, False Represents disable PSR2 Feature.
    # @return       is_success: bool
    #                   Returns True if the Feature is Successfully Enabled/Disabled or if same value is already
    #                   present, False Otherwise.
    @classmethod
    def enable_disable_psr2(cls, gfx_index: str, enable_psr2: bool) -> bool:

        registry_key = registry.RegKeys.PSR.PSR2_DISABLE
        # if enable_psr2 is True, then update reg key PSR2_DISABLE=0 else update reg key PSR2_DISABLE=1
        is_success = registry.write(gfx_index, registry_key, registry_access.RegDataType.DWORD, int(not enable_psr2))

        if is_success is True:  # Registry write is successful, restart the display driver
            is_success, _ = display_essential.restart_gfx_driver()
            if is_success is False:
                logging.error("Failed to restart display driver after updating {0} registry key".format(registry_key))
        elif is_success is False:  # Registry write is failed.
            gdhm.report_bug(
                title="[Interfaces][DscHelperLib] Failed to update {0} registry value to {1} for {2}".format(
                    registry_key, int(not enable_psr2), gfx_index),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(f"Failed to update {registry_key} registry value to {int(not enable_psr2)} for {gfx_index}")
        else:  # Registry write not done, since same value already exists.
            logging.info(f"Skipping registry write as same value already exists in {registry_key} registry")
            is_success = True

        return is_success

    ##
    # @brief        Class Method to Enable or Disable BPC Registry
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    enable_bpc: int
    #                   If set to 1, Driver reads bpc value from SELECT_BPC_FROM_REGISTRY,
    #                   If set to 0, Driver ignores value in SELECT_BPC_FROM_REGISTRY registry
    # @return       is_success: bool
    #                   Returns True if the SELECT_BPC Registry Value is Set Successfully or if same value is already
    #                   present, False Otherwise.
    @classmethod
    def enable_disable_bpc_registry(cls, gfx_index: str, enable_bpc: int) -> bool:

        registry_key = registry.RegValues.BPC.SELECT_BPC
        is_success = registry.write(gfx_index, registry_key, registry_access.RegDataType.DWORD, enable_bpc)

        if is_success is True:  # Registry write is successful, restart the display driver
            is_success, _ = display_essential.restart_gfx_driver()
            if is_success is False:
                logging.error("Restart display driver failed after updating {} registry".format(registry_key))
        elif is_success is False:  # Registry write is failed.
            logging.error("Registry Write Failed For Registry {}".format(registry_key))
        else:  # Registry write not done, since same value already exists.
            logging.info("Skipping registry write as same value already exists in {} registry".format(registry_key))
            is_success = True

        return is_success

    ##
    # @brief        Class Method to Set the Required BPC in the Registry Which Driver uses for Programming Instead of
    #               the Panel Caps
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    bpc: int
    #                   BPC Value to be Used by the Driver for Driving the Display.
    # @return       is_success: bool
    #                   Returns True if the BPC Value is Set Successfully, False Otherwise.
    @classmethod
    def set_bpc_in_registry(cls, gfx_index: str, bpc: int) -> bool:

        is_success = cls.enable_disable_bpc_registry(gfx_index, enable_bpc=1)
        if is_success is False:
            return is_success

        registry_key = registry.RegValues.BPC.SELECT_BPC_FROM_REGISTRY
        is_success = registry.write(gfx_index, registry_key, registry_access.RegDataType.DWORD, bpc)

        if is_success is True:  # Registry write is successful, restart the display driver.
            logging.info(f"{bpc} BPC set was successful using registry")
            is_success, _ = display_essential.restart_gfx_driver()
            if is_success is False:
                logging.error("Restart display driver failed after updating {} registry".format(registry_key))
        elif is_success is False:  # Registry write is failed.
            logging.error("Registry Write Failed For Registry {}".format(registry_key))
            return is_success
        else:  # Registry write not done, since same value already exists.
            logging.info("Skipping registry write as same value already exists in {} registry".format(registry_key))
            is_success = True

        return is_success

    ##
    # @brief        Class Method to Get the Required BPC in the Registry Which Driver uses for Programming Instead of
    #               the Panel Caps
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @return       read_bpc: int
    #                   Returns BPC Value Set in the Registry
    @classmethod
    def get_bpc_from_registry(cls, gfx_index: str) -> int:
        read_bpc: int = 0
        is_enable = registry.read(gfx_index, registry.RegValues.BPC.SELECT_BPC)
        if is_enable == 1:
            read_bpc = registry.read(gfx_index, registry.RegValues.BPC.SELECT_BPC_FROM_REGISTRY)
            read_bpc = 0 if read_bpc is None else read_bpc

        logging.info('BPC Value From Registry: {}'.format(read_bpc))
        return read_bpc

    ##
    # @brief        Class Method to Read the DPCD Register Based on the Offset and Size Provided.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D'
    # @param[in]    offset: int
    #                   DPCD Offset From Which the Value has to be Read.
    # @param[in]    size: Optional[int]
    #                   No of Bytes of Data that has to be Read.
    # @return       reg_values: List[int]
    #                   Returns List of Integers by Slicing the reg_values According to the Number of Bytes Requested.
    @classmethod
    def read_dpcd(cls, gfx_index: str, port: str, offset: int, size: int = 1) -> List[int]:
        display_and_adapter_info = cls.display_config.get_display_and_adapter_info_ex(port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]

        dpcd_flag, reg_values = driver_escape.read_dpcd(display_and_adapter_info, offset)

        assert dpcd_flag, "DPCD Read Failed For Offset: {} of Display Connected to {} on {}".format(offset, port,
                                                                                                    gfx_index)
        logging.debug(f"DPCD OFFSET: {hex(offset)}, LENGTH: {size}, Value: {reg_values[:size]}")
        return reg_values[:size]

    ##
    # @brief        Static Method to Extract the Required Number of Bits From a Register Value.
    # @param[in]    reg_value: int
    #                   Register Value From Which the Bits have to be Extracted.
    # @param[in]    bits_to_extract: int
    #                   No of Bits that Needs to be Extracted From the Register Value.
    # @param[in]    start_position: int
    #                   Starting Position From Which the Bits have to Extracted From the Register Value.
    # @param[in]    bin_format: str
    #                   This tell the length of the binary that will be generated for the reg value.
    # @return       Returns the integer value for the extracted bits
    @staticmethod
    def extract_bits(reg_value: int, bits_to_extract: int, start_position: int, bin_format: str = '08b') -> int:

        # Convert Number to Binary and keep the leading zeros
        binary = format(reg_value, bin_format)
        end = len(binary) - start_position
        start = end - bits_to_extract
        extracted_bits = binary[start: end]

        return int(extracted_bits, 2)

    ##
    # @brief        Get Supported BPC List Based on the Platform Capability.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @return       supported_bpc_list: List[int]
    #                   Returns List of BPC Supported by the Platform
    @classmethod
    def get_supported_bpc_list(cls, gfx_index: str) -> List[int]:
        index = int(gfx_index[-1])
        platform_name = DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName

        if platform_name in ['JSL', 'EHL', 'ICLLP', 'ICLHP', 'LKF1', 'RKL', 'RYF']:
            supported_bpc_list = [8, 10]
        else:
            supported_bpc_list = [8, 10, 12]

        return supported_bpc_list

    ##
    # @brief        Helper method to check if FEC is supported by the display by reading FEC_CAPABILITY_OFFSET
    # @param[in]    display_and_adapter_info: DisplayAndAdapterInfo
    #                   Contains the information that is required to read the dpcd register of the display, like port
    #                   name, target_id, gfx_index etc.
    # @return       is_fec_supported: bool
    #                   Returns True if FEC is supported by the display, False Otherwise.
    @classmethod
    def is_fec_supported(cls, display_and_adapter_info: DisplayAndAdapterInfo) -> bool:
        target_id = display_and_adapter_info.TargetID

        result: Tuple[bool, List] = driver_escape.read_dpcd(display_and_adapter_info, DPCDOffsets.FEC_CAPABILITY_OFFSET)
        is_success, fec_cap_0 = result[0], result[1]
        assert is_success, "[Test Issue] - Reading FEC CAP DPCD Register Failed"

        is_fec_supported = True if DSCHelper.extract_bits(fec_cap_0[0], 1, 0) == 1 else False
        logging.info(f"Is FEC Supported by the Display with Target ID: {target_id}: {is_fec_supported}")

        return is_fec_supported

    ##
    # @brief        Get FEC status from Display Engine for given transcoder
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    platform: str
    #                   Platform Name in Which the Display is Plugged.
    # @param[in]    transcoder_ddi: str
    #                   Contains Transcoder or DDI Name Depending on the Platform in Which the Display is Plugged.
    # @return       is_fec_enabled: bool
    #                   Returns True if FEC is Enabled, False Otherwise.
    @classmethod
    def get_fec_status(cls, gfx_index: str, platform: str, transcoder_ddi: str) -> bool:
        is_fec_enabled: bool = True
        register = 'DP_TP_CTL_' + transcoder_ddi

        dp_tp_ctl = MMIORegister.read("DP_TP_CTL_REGISTER", register, platform, gfx_index=gfx_index)

        if (dp_tp_ctl.asUint & 0x40000000) != 0x40000000:
            is_fec_enabled = False

        logging.info(f"Is FEC Enable Bit Set in DP TP CTL Register: {is_fec_enabled}")

        return is_fec_enabled

    ##
    # @brief        A class method that acts as an extension to get_fec_status() for any given gfx_index and port_name
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port_name: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D'
    # @return       is_fec_enabled: bool
    #                   Returns True if FEC is Enabled, False Otherwise.
    @classmethod
    def get_fec_status_ex(cls, gfx_index: str, port_name: str) -> bool:
        display_base = DisplayBase(port_name, gfx_index=gfx_index)
        _, ddi, transcoder = display_base.GetPipeDDIAttachedToPort(port_name, True, gfx_index)
        transcoder = transcoder.split('_')[-1].upper()

        # Forward Error Correction (FEC) coding for Display Ports (DP).
        # For pre Gen11.5 platforms DP_TP_CTL is based on DDI and post that it's mapped to transcoder.
        index = int(gfx_index[-1])
        platform = DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName
        transcoder_ddi = ddi[-1] if platform in ['GLK', 'ICLLP', 'EHL', 'JSL'] else transcoder

        is_fec_enabled = cls.get_fec_status(gfx_index, platform, transcoder_ddi)

        return is_fec_enabled

    ##
    # @brief        This method checks if FEC_READY bit is set in the FEC_CONFIGURATION DPCD Register.
    # @param[in]    display_and_adapter_info: DisplayAndAdapterInfo
    #                   Contains the information that is required to read the dpcd register of the display, like port
    #                   name, target_id, gfx_index etc.
    # @return       is_fec_read_bit_set: bool
    #                   Returns True if FEC Configuration is Enabled, False Otherwise.
    @classmethod
    def get_fec_ready_status(cls, display_and_adapter_info: DisplayAndAdapterInfo) -> bool:
        target_id = display_and_adapter_info.TargetID

        result: Tuple[bool, List] = driver_escape.read_dpcd(display_and_adapter_info, DPCDOffsets.FEC_CONFIGURATION)
        is_success, fec_configuration = result[0], result[1]
        assert is_success, "[Test Issue] - Reading FEC CONFIGURATION DPCD Register Failed"

        is_fec_read_bit_set = True if DSCHelper.extract_bits(fec_configuration[0], 1, 0) == 1 else False
        logging.info(f"FEC Ready Bit Status for Display with Target id: {target_id}: {is_fec_read_bit_set}")

        logging.info(f"Is FEC Ready Bit Set in Panel: {is_fec_read_bit_set}")
        return is_fec_read_bit_set

    ##
    # @brief        Class Method to Get the System Clock Using the Graphics Index
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter for Which the System Clock is required. E.g. 'gfx_0', 'gfx_1'
    # @return       _: object
    #                   Returns the Corresponding Clock object for the platform.
    @classmethod
    def get_system_clock(cls, gfx_index: str) -> object:
        index = int(gfx_index[-1])
        platform_name = DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName
        logging.debug(f"Getting System Clock Object for {platform_name}")

        # Once ELG clk module is added, remove it from ignore_platforms list in dsc_helper.is_pipe_joiner_required func
        # TODO    Compute CD Clock Here Instead of Creating Clock Object and Invoking get_system_max_cd_clk
        system_clock = {'TGL': TglClock(),
                        'RKL': RklClock(),
                        'DG1': Dg1Clock(),
                        'DG2': Dg2Clock(),
                        'ADLP': AdlpClock(),
                        'ADLS': AdlsClock(),
                        'MTL': MtlClock(),
                        'ELG': ElgClock(),
                        'LNL': LnlClock(),
                        'PTL': PtlClock(),
                        'NVL': NvlClock(),
                        'CLS': PtlClock(),
                        }

        if platform_name not in system_clock:
            assert False, "[Test Issue] - Platform Not Supported: %s" % platform_name

        return system_clock[platform_name]

    ##
    # @brief            Class Method to Get the Min DSC BPP based on the Pixel Encoding
    # @param[in]        color_format: ColorFormat
    #                       Indicates the Color Format/Pixel Encoding for which Min DSC BPP needs to be Calculated
    # @return           min_bpp: float
    #                       Returns the Minimum DSC BPP Required for Compressed Video Transport for a Given Color
    #                       Format in U6.4 Format
    @classmethod
    def get_min_dsc_bpp_for_pixel_encoding(cls, color_format: ColorFormat) -> int:
        min_bpp = 0

        if color_format == ColorFormat.RGB or color_format == ColorFormat.YUV444:
            min_bpp = 8.0
        elif color_format == ColorFormat.YUV422:
            min_bpp = 7.0
        elif color_format == ColorFormat.YUV420:
            min_bpp = 6.0

        min_bpp = int(min_bpp * FIXED_POINT_U6_4_CONVERSION)
        logging.info(f"Min DSC BPP Supported for the color format: {color_format.name} is {min_bpp}")

        return min_bpp

    ##
    # @brief        Class method to get the max dsc bpp based on the color format and input bpc
    # @param[in]    color_format: ColorFormat
    #                   Pixel Encoding of the current mode that is applied.
    # @param[in]       bpc: int
    #                   Bits per component for the current mode. E.g. 8/10/12
    # @return       max_dsc_bpp: int
    #                       Max DSC BPP that can be supported for the specified color format in U6.4 format
    @classmethod
    def get_max_dsc_bpp_for_pixel_encoding(cls, color_format: ColorFormat, bpc: int) -> int:
        max_dsc_bpp = 0

        if color_format == ColorFormat.RGB or color_format == ColorFormat.YUV444:
            max_dsc_bpp = (3 * bpc) - (1 / FIXED_POINT_U6_4_CONVERSION)
        elif color_format == ColorFormat.YUV422:
            max_dsc_bpp = (2 * bpc) - (1 / FIXED_POINT_U6_4_CONVERSION)
        elif color_format == ColorFormat.YUV420:
            max_dsc_bpp = (1.5 * bpc) - (1 / FIXED_POINT_U6_4_CONVERSION)

        max_dsc_bpp = int(max_dsc_bpp * FIXED_POINT_U6_4_CONVERSION)

        logging.info(f"Max DSC BPP supported for the color format: {color_format.name} is {max_dsc_bpp}")
        return max_dsc_bpp

    ##
    # @brief        A Class Method to get the PPS Header Values Programmed by the Driver in VIDEO DIP PPS DATA
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    platform: str
    #                   Platform Name in Which the Display is Plugged.
    # @param[in]    transcoder_name: str
    #                   Transcoder Name For Which Programmed Register Values Has to be Fetched.
    # @return       None
    @classmethod
    def get_video_dip_pps_byte_array(cls, gfx_index: str, platform: str, transcoder_name: str) -> List[int]:
        byte_array = []

        register_interface: DisplayRegsService = DisplayRegs.get_interface(platform, gfx_index)
        pps_offsets: VideoDataIslandPacketPPSOffsets = register_interface.get_video_dip_pps_offsets(transcoder_name)
        for index in range(0, 33):
            offset = getattr(pps_offsets, 'PPS' + str(index))
            value = DisplayArgs.read_register(offset, gfx_index)
            byte_array.extend(value.to_bytes(4, byteorder="little"))

        logging.debug(f"Video DIP PPS SDP Byte Array: {byte_array}")
        return byte_array

    ##
    # @brief        Get compressed from the PPS Register if the DSC is enabled.
    # @param[in]    gfx_index: str
    #                   Graphics adapter Index on which the display is connected. E.g. gfx_0, gfx_1 etc.
    # @param[in]    pipe: str
    #                   Pipe on which the display is connected. E.g. "A", "B" etc.
    # @return       bits_per_pixel: int
    #                   Compressed Bits Per Pixel in U6.4 Format
    @classmethod
    def get_compressed_bpp(cls, gfx_index: str, pipe: str) -> int:
        bits_per_pixel = 0
        index = int(gfx_index[-1])
        platform = DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName

        if platform in ['ICLLP', 'JSL']:
            reg_dss_ctl2 = MMIORegister.read("DSS_CTL2_REGISTER", "DSS_CTL2", platform, gfx_index=gfx_index)
            if reg_dss_ctl2.left_branch_vdsc_enable:
                reg_dsc_pps_1 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_1", f"PPS1_0_{pipe}", platform,
                                                  gfx_index=gfx_index)
                bits_per_pixel = reg_dsc_pps_1.bits_per_pixel

        else:
            reg_pipe_dss_ctl2 = MMIORegister.read("PIPE_DSS_CTL2_REGISTER", f"PIPE_DSS_CTL2_P{pipe}", platform,
                                                  gfx_index=gfx_index)
            if reg_pipe_dss_ctl2.left_branch_vdsc_enable:
                reg_dsc_pps_1 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_1_REGISTER",
                                                  f"DSC_PICTURE_PARAMETER_SET_1_DSC0_P{pipe}", platform,
                                                  gfx_index=gfx_index)
                bits_per_pixel = reg_dsc_pps_1.bits_per_pixel

        logging.info(f"Compressed Bits Per Pixel [U6.4 Format]: {bits_per_pixel}")

        return bits_per_pixel

    ##
    # @brief        Helper function to know if a platform has implemented MST DSC HW WA or not.
    # @param[in]    gfx_index: str
    #                   Graphics Adapter index for which SKU Name is required. E.g. "gfx_0"
    # @param[in]    platform_name: str
    #                   Name of the platform for which we need to know if WA is implemented or not
    # @return       is_wa_not_implemented: bool
    #                   Returns True if WA is not implemented, False otherwise.
    @classmethod
    def is_dsc_hw_improvements_not_implemented_platform(cls, gfx_index: str, platform_name: str):
        is_hw_improvements_not_implemented = False
        sku_name = SystemInfo().get_sku_name(gfx_index)

        if platform_name in cls._DSC_HW_IMPROVEMENTS_NOT_IMPLEMENTED_PLATFORMS:
            is_hw_improvements_not_implemented = True

            if sku_name in ["RPLP", "ACMP"]:
                is_hw_improvements_not_implemented = False
            elif platform_name in ['ADLP', 'ADLS']:
                status, misc_sys_info = driver_escape.get_misc_system_info(gfx_index=gfx_index)
                assert status, "[Driver Issue] - Get Misc System Info Escape call Failed"
                device_id, rev_id = misc_sys_info.platformInfo.deviceID, misc_sys_info.platformInfo.revID
                logging.info(f"Device ID: {device_id}, Rev ID: {rev_id}")

                # https://gfxspecs.intel.com/Predator/Home/Index/55376?dstFilter=ADL&mode=Filter
                # Audio BW calculations is not yielding right DSC BPP causing audio issue, Hence considering pre ADL-P
                # and pre ADL-P L0 stepping also as DSC HW improvements not implemented platforms.
                # REV ID >= 12 indicates Display Stepping is DO and above, also CPU Stepping is LO and above
                # Driver Change: https://github.com/intel-innersource/drivers.gpu.unified/pull/43856
                if platform_name == 'ADLP' and misc_sys_info.platformInfo.revID >= 12:
                    is_hw_improvements_not_implemented = False

                # For RPLS SKU, devices having rev id as 4 only has DSC HW improvements implemented other devices
                # doesn't have the HW fix.
                # https://gfxspecs.intel.com/Predator/Home/Index/53655?dstFilter=ADLS&mode=Filter
                if sku_name == "RPLS" and misc_sys_info.platformInfo.revID == 0x4:
                    is_hw_improvements_not_implemented = False

        logging.info(f"Is DSC HW Improvements implemented platforms: {not is_hw_improvements_not_implemented}")

        return is_hw_improvements_not_implemented

    ##
    # @brief        Helper function to know if the platform supports PSR2 + DSC co-existence.
    # @param[in]    gfx_index: str
    #                   Graphics adapter Index on which the display is connected. E.g. gfx_0, gfx_1 etc.
    # @param[in]    platform: str
    #                   Platform Name in Which the Display is Plugged
    # @return       is_co_existence_supported: bool
    #                   Returns True if PSR2 + DSC co-existence is supported, False otherwise.
    @classmethod
    def is_psr2_dsc_co_existence_supported_platform(cls, gfx_index: str, platform: str) -> bool:
        is_co_existence_supported = True

        if platform in cls._PSR2_DSC_UNSUPPORTED_PLATFORMS:
            is_co_existence_supported = False
            sku_name = SystemInfo().get_sku_name(gfx_index)
            if sku_name in ["ACMP"]:
                is_co_existence_supported = True

        return is_co_existence_supported

    ##
    # @brief        Class Method to Get if the branch supports DSC Pass through
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in Which the Display is Plugged. E.g. 'EDP_A', 'DP_D'
    # @return       is_dsc_pass_through_supported: bool
    #                   Returns True if DSC passthrough is Supported, False Otherwise.
    @classmethod
    def is_vdsc_pass_through_supported(cls, gfx_index: str, port: str) -> bool:

        reg_value = DSCHelper.read_dpcd(gfx_index, port, DPCDOffsets.DSC_SUPPORT)[0]
        is_dsc_pass_through_supported = True if DSCHelper.extract_bits(reg_value, 1, 1) == 1 else False
        logging.info(
            f"Is DSC Passthrough supported by the Display on {gfx_index} {port}: {is_dsc_pass_through_supported}"
        )

        return is_dsc_pass_through_supported

    ##
    # @brief        Get display timing info from QDC
    # @param[in]    display_and_adapter_info: DisplayAndAdapterInfo
    #                   Display and adapter information for which the timing info is required
    # @return       display_timing: DisplayTimings
    #                   This structure is filled with parameters required for DSC PPS computation. Other members are
    #               not filled.
    @classmethod
    def get_display_timing_from_qdc(cls, display_and_adapter_info: DisplayAndAdapterInfo) -> DisplayTimings:
        query_disp_config = cls.display_config.query_display_config(display_and_adapter_info)
        display_timing = DisplayTimings()
        display_timing.hActive = query_disp_config.targetModeInfo.targetVideoSignalInfo.activeSize.cx
        display_timing.vActive = query_disp_config.targetModeInfo.targetVideoSignalInfo.activeSize.cy
        display_timing.targetPixelRate = query_disp_config.targetModeInfo.targetVideoSignalInfo.hSyncFreq.Numerator * 10
        display_timing.hTotal = query_disp_config.targetModeInfo.targetVideoSignalInfo.hSyncFreq.Denominator * 10
        display_timing.scanlineOrdering = query_disp_config.targetModeInfo.targetVideoSignalInfo.scanlineOrdering

        logging.info(f"Display Timing from QDC: {display_timing.to_string()}")
        return display_timing

    ##
    # @brief        Method to verify if FEC & DSC are not programmed by the driver in negative cases eg. panel reports DSC/FEC errors
    #               Checks dp_tp_ctl & pipe_dss_ctl2 registers
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port: str
    #                   Port Name in which the Display is Plugged. E.g. 'EDP_A', 'DP_F'
    # @return       status
    #                   Returns True if DSC and FEC are not programmed by the driver, False Otherwise.
    @classmethod
    def is_fec_dsc_disabled(cls, gfx_index: str, port: str) -> bool:
        is_fec_enabled = DSCHelper.get_fec_status_ex(gfx_index, port)
        if is_fec_enabled:
            logging.error(f"[Driver Issue] FEC is enabled by the driver even when sink hasn't set FEC_DECODE_EN_DETECTED bit for port {port}.")
            return False

        is_vdsc_enabled_in_driver = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port)
        if is_vdsc_enabled_in_driver:
            logging.error(f"[Driver Issue] DSC is enabled by the driver even when sink hasn't set FEC_DECODE_EN_DETECTED bit for port {port}.")
            return False

        is_vdsc_enabled_in_panel = DSCHelper.is_vdsc_enabled_in_panel(gfx_index, port)
        if is_vdsc_enabled_in_panel:
            logging.error(f"[Driver Issue] DSC is enabled in the sink even when sink hasn't set FEC_DECODE_EN_DETECTED bit for port {port}.")
            return False

        return True


##
# @brief        Class which contains the reg keys grouped under each feature by creating an inner class and also has
#               static methods to do write of those reg keys
class RegKey(object):
    ##
    # @brief        This class contains Registry key values for VDSC keys
    class VDSC:
        EDP_COMPRESSION_DISABLE = "eDPCompressionDisable"
        DP_MST_DSC_DISABLE = "DPMstDscDisable"

    ##
    # @brief        Updates the registry key with the provided value and restarts gfx driver if needed.
    # @param[in]    gfx_index : str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    key_name : str
    #                   Registry key name
    # @param[in]    key_value : int
    #                   Value to be updated in registry
    # @param[in]    key_path : str
    #                   Path of the registry key
    # @return       is_success, is_reboot_required: Tuple[bool, bool]
    #               Returns two values. One to indicate whether the registry write is successful or not
    #               and other to say whether reboot of the system is required or not.
    @staticmethod
    def write(gfx_index: str, key_name: str, key_value: int, key_path=None) -> Tuple[bool, bool]:
        is_restart_driver_required = is_reboot_required = False

        if key_path is None:
            register_arg = registry_access.StateSeparationRegArgs(gfx_index)
        else:
            register_arg = registry_access.LegacyRegArgs(registry_access.HKey.LOCAL_MACHINE, key_path)

        reg_value, _ = registry_access.read(register_arg, key_name)

        # Check if expected value is already set
        if reg_value == key_value:
            logging.debug(f'Skipping registry write as the same value is present in the registry already. '
                          f'Key: {key_name}, Value: {key_value}')
            is_success = True
        else:
            # If expected value is not set, update the registry key
            is_success = registry_access.write(register_arg, key_name, registry_access.RegDataType.DWORD, key_value)
            is_restart_driver_required = is_success

        # Restart the gfx driver if the registry key is changed
        if is_restart_driver_required is True:
            is_success, is_reboot_required = display_essential.restart_gfx_driver()

        logging.info(f'Registry write is successful - {is_success}. System reboot is required - {is_reboot_required}')

        return is_success, is_reboot_required
