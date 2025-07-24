# @file         dp_helper.py
# @brief        Contains All the Helper Functions For MST Related Tests and Verification
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
import math
from typing import Tuple

from Libs.Core import display_utility
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.display_config.display_config_struct import DisplayAndAdapterInfo
from Libs.Core.sw_sim.dp_mst import LENGTH, MST_RELATIVEADDRESS
from Libs.Core.vbt.vbt import Vbt
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ColorFormat
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_128B_132B_PER_100, \
    AVAILABLE_MTP_TIMESLOTS_8B_10B, AVAILABLE_MTP_TIMESLOTS_128B_132B, DP_DATA_BW_EFFICIENCY_MST_DSC_PER_100
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_SST_DSC_PER_100
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_SST_FEC_PER_100
from Libs.Feature.display_port.dp_enum_constants import DP_DATA_BW_EFFICIENCY_SST_PER_100
from Libs.Feature.vdsc.dsc_enum_constants import DSCEngine, FIXED_POINT_U6_4_CONVERSION
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from registers.mmioregister import MMIORegister
from Libs.Core.machine_info import machine_info


##
# @brief        Helper class that can be imported whenever any displayport related helper functions are required.
class DPHelper:

    ##
    # @brief        A class method that helps to get the port number based on the relative address of the device
    # @param[in]    relative_address: MST_RELATIVEADDRESS
    #                   Relative address of the device for which the port number is required
    # @return
    @classmethod
    def get_port_number(cls, relative_address: MST_RELATIVEADDRESS) -> int:
        port_number = 0

        total_link_count = int.from_bytes(relative_address.TotalLinkCount, "little")
        if 0 <= ((total_link_count / 2) - 1) < LENGTH:
            if total_link_count == 1:
                port_number = 0
            elif total_link_count % 2 == 0:
                port_number = (relative_address.Address[(total_link_count // 2) - 1] & 0xF0) >> 4
            else:
                port_number = relative_address.Address[(total_link_count // 2) - 1] & 0x0F

        logging.info(f"Port Number: {port_number}")
        return port_number

    ##
    # @brief        A class method that returns if the port is a logical port or not.
    #               As per DP spec physical port ranges from 0x0 to 0x7 and logical port ranges from 0x8 to 0xF
    # @param[in]    port_number: int
    #                   port number in which the device is connected
    # @return       logical_port: bool
    #                   Returns True if it's a logical port else False
    @classmethod
    def is_logical_port(cls, port_number: int) -> bool:
        logical_port = False
        if 0x8 <= port_number <= 0xF:
            logical_port = True

        logging.info(f"Port Number: {port_number}, Logical Port: {logical_port}")
        return logical_port

    ##
    # @brief        Computes Link_M, Link_N, Data_M, Data_N for MST Displays
    # @param[in]    display_and_adapter_info: DisplayAndAdapterInfo
    #                   Display and Graphics adapter info on which the display is connected.
    # @param[in]    pipe: str
    #                   Name of the pipe to which the display is connected. E.g. 'A', 'B'
    # @param[in]    pixel_clock_hz: int
    #                   Pixel clock of the MST display in units of hertz
    # @param[in]    color_format: ColorFormat
    #                   Pixel encoding of the current mode that is applied. E.g. RGB, YUV420 etc.
    # @param[in]    bpc: int
    #                   Represents bits per component or color. Indicates number of bits required to represent per color
    #                   in a pixel
    # @param[in]    bytes_per_pixel: float
    #                   Indicates the number of bytes required to represent the pixel data.
    # @param[in]    bits_per_pixel: int
    #                   The bpp should be in U6.4 Format (Just to Keep common across all mn values calculations)
    #                   We should use the provided bpp value to compute whether that BPP is possible
    #                   on the link. This is required to know what is the max DSC bpp that can be programmed on the link
    #                   and also to compute mn values.
    # @return       link_m, link_n, data_m, data_n: Tuple[int, int, int, int]
    #                   Returns The computed link m, link n, data m and data n based on link rate, lane count, bpp,
    #                   encoding format, pixel clock etc.
    @classmethod
    def get_sst_link_data_mn_values(cls, display_and_adapter_info: DisplayAndAdapterInfo, pipe: str,
                                    pixel_clock_hz: int, color_format: ColorFormat, bpc: int, bytes_per_pixel: float,
                                    bits_per_pixel: int) -> Tuple[bool, int, int, int, int]:
        is_link_bw_sufficient = True
        compression_ratio = 1
        uncompressed_bits_per_pixel = bpc * 3
        bits_per_pixel = bits_per_pixel / FIXED_POINT_U6_4_CONVERSION
        gfx_index = display_and_adapter_info.adapterInfo.gfxIndex
        port = CONNECTOR_PORT_TYPE(display_and_adapter_info.ConnectorNPortType).name
        index = int(gfx_index[-1])

        platform = DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName
        port_name = str(port).split('_')[1]

        # As per DP spec, overhead of 0.25% has to be added while SSC is enabled, pixel_clock_hz = pixel_clock_hz * 1.0025
        # On MTL+ C20 PHY, SSC overhead is 0.45% compared to typical 0.5%.
        # With SSC overhead there will be reduction in average link rate by 0.225%.
        # Rather than decreasing the link rate, raising the pixel clock by same percentage.
        # Average LinkRate = LinkRateMbps * (1 - 0.00225)
        # Average LinkRate = LinkRateMbps * 0.99775
        # 1/0.99775 approx is 1.002255
        # PixelClockHz = PixelClockHz * (1.002255)
        # PixelClockHz = (PixelClockHz * 1002255)/1000000
        logging.info("port = {}".format(port))
        logging.info("Pixel clock without any SSC overhead : {}".format(pixel_clock_hz))

        ssc_enable = cls.get_ssc(gfx_index, port)
        if ssc_enable:
            if platform in machine_info.PRE_GEN_14_PLATFORMS:
                pixel_clock_hz = pixel_clock_hz * (1.002506)
                logging.info("pixel clock on Pre gen 14 platforms with 0.2506 ssc overhead = {}".format(pixel_clock_hz))
            else:
                if "A" in port_name or "B" in port_name:
                    pixel_clock_hz =  pixel_clock_hz * (1.002506)
                    logging.info("pixel clock on gen 14 platforms + C10 PHY with 0.2506 ssc overhead = {}".format(pixel_clock_hz))
                else:
                    pixel_clock_hz =  pixel_clock_hz * (1.002255)
                    logging.info("pixel clock on gen 14 platforms + C20 PHY with 0.2255 ssc overhead = {}".format(pixel_clock_hz))

            logging.info(f"Updated pixel clock with SSC Enabled: {pixel_clock_hz}")

        link_clock_gbps = dpcd_helper.DPCD_getLinkRate(display_and_adapter_info)
        lane_count = dpcd_helper.DPCD_getNumOfLanes(display_and_adapter_info)

        link_clock_mhz = link_clock_gbps * 100

        compression_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port)
        if compression_enabled is True:
            if color_format == ColorFormat.YUV422:
                uncompressed_bits_per_pixel = 16
            elif color_format == ColorFormat.YUV420:
                uncompressed_bits_per_pixel = 12
            compression_ratio = uncompressed_bits_per_pixel / bits_per_pixel
            logging.debug(f"Uncompressed BPP: {uncompressed_bits_per_pixel}, DSC BPP: {bits_per_pixel}, "
                          "compression_ratio: {compression_ratio}")

        if (pixel_clock_hz * bits_per_pixel) > (link_clock_mhz * 1000 * 1000 * 8 * lane_count):
            is_link_bw_sufficient = False
            return is_link_bw_sufficient, 0, 0, 0, 0

        link_n = 0x80000  # 524288
        data_n = 0x800000  # 8388608
        pixel_clock_100hz = pixel_clock_hz / 100
        link_m = (int(pixel_clock_100hz) * link_n) / (link_clock_mhz * 10000)

        fec_link_rate = link_clock_mhz
        is_fec_enabled: bool = DSCHelper.get_fec_status_ex(gfx_index, port)
        if is_fec_enabled:
            # driver considers integer part as effective link rate
            fec_link_rate = int(fec_link_rate * 972261 / 1000000)

        # As per BSpec: Data M/N = (stream_clk * bytes per pixel) / (CR * ls_clk * number of lanes)
        # Bspec link: https://gfxspecs.intel.com/Predator/Home/Index/49266
        data_m = int(pixel_clock_100hz) * float(bytes_per_pixel) * data_n
        data_m /= (compression_ratio * fec_link_rate * lane_count * 10000)

        return is_link_bw_sufficient, int(link_m), link_n, int(data_m), data_n

    ##
    # @brief        Computes Link_M, Link_N, Data_M, Data_N for MST Displays
    # @param[in]    display_and_adapter_info: DisplayAndAdapterInfo
    #                   Display and Graphics adapter info on which the display is connected.
    # @param[in]    pixel_clock_hz: int
    #                   Pixel clock of the MST display in units of hertz
    # @param[in]    bits_per_pixel: int
    #                   The bpp should be in U6.4 Format
    #                   We should use the provided bpp value to compute whether that BPP is possible
    #                   on the link. This is required to know what is the max DSC bpp that can be programmed on the link
    #                   and also to compute mn values.
    # @return       is_link_bw_sufficient, link_m, link_n, data_m, data_n: Tuple[bool, int, int, int, int]
    #                   is_link_bw_sufficient - Set to True if that mode can be driven with the bpp programmed or bpp
    #                   given as input.
    #                   link_m, link_n, data_m, data_n - The computed link m, link n, data m and data n based on
    #                   link rate, lane count, bpp, encoding format, pixel clock etc.
    @classmethod
    def get_mst_link_data_m_n_values(cls, display_and_adapter_info: DisplayAndAdapterInfo, pixel_clock_hz: int,
                                     bits_per_pixel: int) -> Tuple[bool, int, int, int, int]:
        is_link_bw_sufficient = True
        max_value = (16 * 1024 * 1024) - 1  # max size in the register 24 bits.
        gfx_index = display_and_adapter_info.adapterInfo.gfxIndex
        port = CONNECTOR_PORT_TYPE(display_and_adapter_info.ConnectorNPortType).name
        bits_per_pixel = bits_per_pixel // FIXED_POINT_U6_4_CONVERSION
        index = int(gfx_index[-1])

        platform = DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName
        port_name = str(port).split('_')[1]

        is_compression_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port)
        link_rate_gbps = dpcd_helper.DPCD_getLinkRate(display_and_adapter_info)
        lane_count = dpcd_helper.DPCD_getNumOfLanes(display_and_adapter_info)

        is_128_132_bit_encoding = True if link_rate_gbps >= 10 else False

        if is_128_132_bit_encoding is True:
            data_bandwidth_efficiency = DP_DATA_BW_EFFICIENCY_128B_132B_PER_100 * 100
            # Control link symbols and data link symbols are of size 32 bits in case of 128b/132b encoding.
            # link_clock_ghz = link_rate_gbps / 32
            # link_clock_mhz = link_rate_gbps * 1000 / 32
            # link_clock_khz = link_rate_gbps * 1000  * 1000 / 32
            # link_clock_100hz = link_rate_gbps * 1000  * 1000 * 1000 / (32 * 100)
            # link_clock_100hz = link_rate_gbps * 1000  * 10000 / 32
            # link_clock_100hz = link_rate_gbps * 1000  * 625 / 2
            link_clock_100hz = int((link_rate_gbps * 1000 * 625) / 2)
        else:
            # For 8b / 10b MST DataBandwidthEfficiency is considered as 80.00% instead of actual 78.75%.
            # (as the hardware internally multiplies programmed Data M/N with "64 time-slots" for rate-governing
            # instead of 63 hence we are not considering actual bandwidth efficiency of 78.75%)
            data_bandwidth_efficiency = DP_DATA_BW_EFFICIENCY_SST_PER_100 * 100

            is_fec_enabled: bool = DSCHelper.get_fec_status_ex(gfx_index, port)
            if is_fec_enabled is True:
                data_bandwidth_efficiency = DP_DATA_BW_EFFICIENCY_SST_FEC_PER_100 * 100
                if is_compression_enabled is True:
                    data_bandwidth_efficiency = DP_DATA_BW_EFFICIENCY_SST_DSC_PER_100 * 100

            # Control link symbols and data link symbols are of size 10 bits in case of 8b/10b encoding
            # link_clock_ghz = link_rate_gbps / 10
            # link_clock_mhz = link_rate_gbps * 1000 / 10
            # link_clock_khz = link_rate_gbps * 1000 * 1000 / 10
            # link_clock_100hz = link_rate_gbps * 1000 * 1000  * 1000 / (10 * 100)
            link_clock_100hz = int(link_rate_gbps * 1000 * 1000)

        logging.info("Data Bandwidth Efficiency: {}".format(data_bandwidth_efficiency))

        # On MTL+ C20 PHY, SSC overhead is 0.45% compared to typical 0.5%.
        # With SSC overhead there will be reduction in average link rate by 0.225%.
        # Rather than decreasing the link rate, raising the pixel clock by same percentage.
        # Average LinkRate = LinkRateMbps * (1 - 0.00225)
        # Average LinkRate = LinkRateMbps * 0.99775
        # 1/0.99775 approx is 1.002255
        # PixelClockHz = PixelClockHz * (1.002255)
        # PixelClockHz = (PixelClockHz * 1002255)/1000000
        logging.info("Pixel clock without any SSC overhead : {}".format(pixel_clock_hz))

        is_ssc_enabled = cls.get_ssc(gfx_index, port)
        # As per DP spec, overhead of 0.25% has to be added while SSC is enabled, pixel_clock_hz = pixel_clock_hz * 1.0025
        if is_ssc_enabled:
            if platform in machine_info.PRE_GEN_14_PLATFORMS:
                pixel_clock_hz =  pixel_clock_hz * (1.002506)
                logging.info("pixel clock on Pre gen 14 platforms with 0.2506 ssc overhead = {}".format(pixel_clock_hz))
            else:
                if "A" in port_name or "B" in port_name:
                     pixel_clock_hz =  pixel_clock_hz * (1.002506)
                     logging.info("pixel clock on gen 14 platforms + C10 PHY with 0.2506 ssc overhead = {}".format(pixel_clock_hz))
                else:
                    pixel_clock_hz =  pixel_clock_hz * (1.002255)
                    logging.info("pixel clock on gen 14 platforms + C20 PHY with 0.2255 ssc overhead = {}".format(pixel_clock_hz))

        pixel_clock_100hz = int(pixel_clock_hz // 100)

        gcd = math.gcd(link_clock_100hz, pixel_clock_100hz)
        link_m = pixel_clock_100hz // gcd
        link_n = link_clock_100hz // gcd

        # When values of LinkM or LinkN exceeds (2^24-1), fix LinkN to 0x8000 and calculate the LinkM value from the ratio already calculated.
        if (link_m > max_value) or (link_n > max_value):
            temp_link_m = (link_m * 0x8000) // link_n
            link_m = temp_link_m
            link_n = 0x8000

        n1 = int(pixel_clock_100hz * bits_per_pixel)
        n2 = int(link_rate_gbps * 1000 * lane_count * data_bandwidth_efficiency)
        if n1 > n2:
            is_link_bw_sufficient = False
            return is_link_bw_sufficient, 0, 0, 0, 0

        gcd = math.gcd(n1, n2)
        data_m = n1 / gcd
        data_n = n2 / gcd

        if (data_m > max_value) or (data_n > max_value):
            data_n = 80000
            data_m = (n1 * 80000) // n2

        if 0 < link_m < 1000:
            multiplier = (1000 // link_m) + 1
            if (link_n * multiplier) < max_value:
                link_m *= multiplier
                link_n *= multiplier

        if 0 < data_m < 1000:
            multiplier = (1000 // data_m) + 1
            if (data_n * multiplier) < max_value:
                data_m *= multiplier
                data_n *= multiplier

        link_m, link_n, data_m, data_n = int(link_m), int(link_n), int(data_m), int(data_n)
        logging.info(f"link_m: {link_m}, link_n: {link_n}, data_m: {data_m}, data_n: {data_n}")

        return is_link_bw_sufficient, link_m, link_n, data_m, data_n

    ##
    # @brief        Computes Link_M, Link_N, Data_M, Data_N for MST and DP 2.0 Displays by considering EOC overhead when
    #               DSC is enabled. Refer: https://gfxspecs.intel.com/Predator/Home/Index/49266
    # @param[in]    display_and_adapter_info: DisplayAndAdapterInfo
    #                   Display and Graphics adapter info on which the display is connected.
    # @param[in]    pipe: str
    #                   Name of the pipe to which the display is connected. E.g. 'A', 'B'
    # @param[in]    h_active: int
    #                   H_ACTIVE of the current mode
    # @param[in]    pixel_clock_hz: int
    #                   Pixel clock of the MST display in units of hertz
    # @param[in]    bits_per_pixel: int
    #                   The bpp should be in U6.4 Format
    #                   We should use the provided bpp value to compute whether that BPP is possible
    #                   on the link. This is required to know what is the max DSC bpp that can be programmed on the link
    #                   and also to compute mn values.
    # @return       is_link_bw_sufficient, link_m, link_n, data_m, data_n: Tuple[bool, int, int, int, int]
    #                   is_link_bw_sufficient - Set to True if that mode can be driven with the bpp programmed or bpp
    #                   given as input.
    #                   link_m, link_n, data_m, data_n - The computed link m, link n, data m and data n based on
    #                   link rate, lane count, bpp, encoding format, pixel clock etc.
    @classmethod
    def get_link_data_m_n_values_considering_eoc(cls, display_and_adapter_info: DisplayAndAdapterInfo, pipe: str,
                                                 h_active: int, pixel_clock_hz: int, bits_per_pixel: int
                                                 ) -> Tuple[bool, int, int, int, int]:
        is_link_bw_sufficient = True
        gfx_index = display_and_adapter_info.adapterInfo.gfxIndex
        index = int(gfx_index[-1])
        platform = DSCHelper.DISPLAY_HARDWARE_INFO_LIST[index].DisplayAdapterName
        port = CONNECTOR_PORT_TYPE(display_and_adapter_info.ConnectorNPortType).name

        max_value = (16 * 1024 * 1024) - 1  # max size in the register 24 bits.
        bits_per_pixel = bits_per_pixel / FIXED_POINT_U6_4_CONVERSION

        port_name = str(port).split('_')[1]

        is_ssc_enabled = cls.get_ssc(gfx_index, port)
        link_rate_gbps = dpcd_helper.DPCD_getLinkRate(display_and_adapter_info)
        lane_count = dpcd_helper.DPCD_getNumOfLanes(display_and_adapter_info)
        transport_mode = dpcd_helper.DPCD_getTransportModeSelect(display_and_adapter_info)
        is_compression_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port)
        is_fec_enabled = DSCHelper.get_fec_ready_status(display_and_adapter_info)

        is_mst_mode = False
        if transport_mode is not None and transport_mode in ["DP_128_132_BIT_SYMBOL_MODE", "MST"]:
            is_mst_mode = True

        # On MTL+ C20 PHY, SSC overhead is 0.45% compared to typical 0.5%.
        # With SSC overhead there will be reduction in average link rate by 0.225%.
        # Rather than decreasing the link rate, raising the pixel clock by same percentage.
        # Average LinkRate = LinkRateMbps * (1 - 0.00225)
        # Average LinkRate = LinkRateMbps * 0.99775
        # 1/0.99775 approx is 1.002255
        # PixelClockHz = PixelClockHz * (1.002255)
        # PixelClockHz = (PixelClockHz * 1002255)/1000000
        logging.info("Pixel clock without any SSC overhead: {}".format(pixel_clock_hz))

        # As per DP spec, overhead of 0.25% has to be added while SSC is enabled, pixel_clock_hz = pixel_clock_hz * 1.0025
        if is_ssc_enabled is True:
            if platform in machine_info.PRE_GEN_14_PLATFORMS:
                pixel_clock_hz = pixel_clock_hz * 1.002506
                logging.info("pixel clock on Pre gen 14 platforms with 0.2506 ssc overhead = {}".format(pixel_clock_hz))
            else:
                if "A" in port_name or "B" in port_name:
                    pixel_clock_hz = pixel_clock_hz * 1.002506
                    logging.info("pixel clock on gen 14 platforms + C10 PHY with 0.2506 ssc overhead = {}".format(pixel_clock_hz))
                else:
                    pixel_clock_hz = pixel_clock_hz * 1.002255
                    logging.info("pixel clock on gen 14 platforms + C20 PHY with 0.2255 ssc overhead = {}".format(pixel_clock_hz))

        pixel_clock_100hz = int(pixel_clock_hz / 100)
        pixel_clock_khz = int(pixel_clock_100hz/10)
        logging.info(f"Updated pixel clock(100Hz) with SSC Enabled: {pixel_clock_100hz}")

        is_128_132_bit_encoding = True if link_rate_gbps >= 10 else False
        if is_128_132_bit_encoding is True:
            # Control link symbols and data link symbols are of size 32 bits in case of 128b/132b encoding.
            # link_clock_ghz = link_rate_gbps / 32
            # link_clock_mhz = link_rate_gbps * 1000 / 32
            link_clock_100hz = int(link_rate_gbps * 1000 * 10000 / 32)

            # For DP 2.0 the bandwidth efficiency is 96.71%.
            # Hence, the overhead percentage will be 100 - 96.71 = 3.29%
            # Therefore, overhead = 3.29 / 100
            # Therefore, efficiency = 1 - 0.0329 = 0.9671
            data_bandwidth_efficiency = DP_DATA_BW_EFFICIENCY_128B_132B_PER_100 / 100
            byte_multiplier = 4
            eoc_symbol = 128
            overhead_symbol = 128
            dp_symbol = 32
            max_mtp_slots = AVAILABLE_MTP_TIMESLOTS_128B_132B

            # MST always operates in 4 main link channels irrespective of the physical lane count
            bytes_per_link_clock = 4 * byte_multiplier

        else:
            # When FEC is enabled, the additional overhead is 2.4%
            # Therefore, overhead = 2.4 / 100 = 0.024
            # Therefore, efficiency = 1 - overhead = 0.976
            # Encoding overhead is taken care in the data_n calculation formula
            data_bandwidth_efficiency = (1 - 0.024) if is_fec_enabled is True else 1

            # Control link symbols and data link symbols are of size 10 bits in case of 8b/10b encoding
            # link_clock_ghz = link_rate_gbps / 10
            # link_clock_mhz = link_rate_gbps * 1000 / 10
            link_clock_100hz = int(link_rate_gbps * 100 * 10000)

            byte_multiplier = 1
            eoc_symbol = 32
            overhead_symbol = 32
            dp_symbol = 8
            max_mtp_slots = AVAILABLE_MTP_TIMESLOTS_8B_10B

            # MST always operates in 4 main link channels irrespective of the physical lane count
            # SST depends on physical lane count
            bytes_per_link_clock = 4 * byte_multiplier if is_mst_mode else lane_count * byte_multiplier

        link_clock_khz = int(link_clock_100hz / 10)
        logging.info("Data Bandwidth Efficiency: {}".format(data_bandwidth_efficiency))
        gcd = math.gcd(pixel_clock_100hz, link_clock_100hz)
        link_m = pixel_clock_100hz / gcd
        link_n = link_clock_100hz / gcd

        # When values of LinkM or LinkN exceeds (2^24-1), fix LinkN to 0x8000 and calculate the LinkM value from the
        # ratio already calculated.
        if (link_m > max_value) or (link_n > max_value):
            temp_link_m = (link_m * 0x8000) // link_n
            link_m = temp_link_m
            link_n = 0x8000

        if 0 < link_m < 1000:
            multiplier = (1000 // link_m) + 1
            if (link_n * multiplier) < max_value:
                link_m *= multiplier
                link_n *= multiplier

        if is_compression_enabled is True:
            # Reading the register directly since slice width will be verified in the DSC programming.
            r_offset = 'PPS3_' + str(DSCEngine.LEFT.value) + '_' + pipe
            dsc_pps3 = MMIORegister.read("DSC_PICTURE_PARAMETER_SET_3", r_offset, platform, gfx_index=gfx_index)
            num_of_slices = math.ceil(h_active / dsc_pps3.slice_width)
            chunk_size = math.ceil(dsc_pps3.slice_width * (bits_per_pixel / 8))
            num_of_link_clk_per_slice = math.ceil(chunk_size / bytes_per_link_clock)
            padding_bytes = (num_of_link_clk_per_slice * bytes_per_link_clock) - chunk_size
            extract_bits_in_h_active = (num_of_slices * eoc_symbol) + (1 * overhead_symbol)
            extract_bits_in_h_active += (num_of_slices * padding_bytes * 8)

            data_m = int(pixel_clock_khz * (chunk_size * num_of_slices * 8 + extract_bits_in_h_active))
            data_n = int(link_clock_khz * lane_count * data_bandwidth_efficiency * dp_symbol * h_active)
        else:
            data_m = int(pixel_clock_100hz * bits_per_pixel)
            data_n = int(link_clock_100hz * lane_count * data_bandwidth_efficiency * dp_symbol)

        if data_m > data_n:
            logging.debug(f"Data M is greater than Data N for bpp of {bits_per_pixel}")
            is_link_bw_sufficient = False
            return is_link_bw_sufficient, 0, 0, 0, 0

        gcd = math.gcd(data_m, data_n)
        data_m = data_m / gcd
        data_n = data_n / gcd
        logging.info(f"link_m: {link_m}, link_n: {link_n}, data_m: {data_m}, data_n: {data_n}")

        if (data_m > max_value) or (data_n > max_value):
            data_m = math.ceil((data_m * 80000) / data_n)
            data_n = 80000

        if 0 < data_m < 1000:
            multiplier = (1000 // data_m) + 1
            if (data_n * multiplier) < max_value:
                data_m *= multiplier
                data_n *= multiplier

        transfer_unit = int(math.ceil(data_m * 64 / data_n))
        if is_128_132_bit_encoding is False:
            remainder = (transfer_unit * lane_count) % 4
            if remainder != 0:
                transfer_unit += ((4 - remainder) / lane_count)

        if is_mst_mode:
            pbn_per_slot = DPHelper.get_pbn_per_slot(link_rate_gbps, lane_count)
            actual_pbn = DPHelper._get_actual_pbn(data_m, data_n, pbn_per_slot, is_ssc_enabled)
            available_link_pbn = max_mtp_slots * pbn_per_slot

            if actual_pbn > available_link_pbn:
                logging.debug(f"Actual PBN is greater than available link PBN for bpp of {bits_per_pixel}")
                is_link_bw_sufficient = False
                return is_link_bw_sufficient, 0, 0, 0, 0

        logging.info(f"link_m: {link_m}, link_n: {link_n}, data_m: {data_m}, data_n: {data_n}")

        return is_link_bw_sufficient, int(link_m), int(link_n), int(data_m), int(data_n)

    ##
    # @brief Get the SSC is supported
    # @param[in] display_port display to verify
    # @param[in] gfx_index Graphics adapter
    # @return True if SSC is enabled in VBT & DPCD
    @classmethod
    def get_ssc(cls, gfx_index, display_port) -> bool:
        vbt = Vbt(gfx_index)
        display_config = DisplayConfiguration()
        display_and_adapter_info = display_config.get_display_and_adapter_info_ex(display_port, gfx_index)
        if type(display_and_adapter_info) is list:
            display_and_adapter_info = display_and_adapter_info[0]

        # Get Port Type
        port_type = None
        enumerated_displays = display_config.get_enumerated_display_info()

        for display_index in range(enumerated_displays.Count):
            port = (CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)).name
            if port == display_port:
                port_type = enumerated_displays.ConnectedDisplays[display_index].PortType

        # SSC is disabled by default for TBT ports. Return false if port is TBT
        if port_type == "TBT":
            return False

        ssc_enable_dpcd = dpcd_helper.DPCD_getSSC(display_and_adapter_info)
        # LFP case
        if display_utility.get_vbt_panel_type(display_port, gfx_index) in [display_utility.VbtPanelType.LFP_DP,
                                                                           display_utility.VbtPanelType.LFP_MIPI]:
            logging.debug("INFO : VBT Panel Type:" + str(vbt.block_40.PanelType))
            logging.debug("INFO : VBT SSC Enabled Bits:" + str(vbt.block_40.LvdsSscEnableBits))
            ssc_enable_vbt = (vbt.block_40.LvdsSscEnableBits & (
                    (1 << (vbt.block_40.PanelType + 1)) - 1)) >> vbt.block_40.PanelType
        else:
            # DP case
            # 0x8 : bit[3] for SSC enable check
            ssc_enable_vbt = vbt.block_1.IntegratedDisplaysSupported.DP_SSC_Enable
            logging.debug(
                "VBT DP SSC Enable Bit is bit 3 in block1.IntegratedDisplaysSupported; its value = {0}".format(
                    vbt.block_1.IntegratedDisplaysSupported.value))
        ssc_dpcd = "ENABLED" if ssc_enable_dpcd else "DISABLED"
        ssc_vbt = "ENABLED" if ssc_enable_vbt else "DISABLED"
        logging.info("INFO : SSC - VBT ({0}) DPCD ({1})".format(ssc_vbt, ssc_dpcd))

        return bool(ssc_enable_dpcd and ssc_enable_vbt)

    ##
    # @brief        Private Helper function to get bits_per_pixel and bytes_per_pixel data for uncompressed and
    #               compressed cases.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    pipe: str
    #                   Name of the pipe to which the display is connected. E.g. 'A', 'B'
    # @param[in]    bpc: int
    #                   Represents bits per component or color. Indicates number of bits required to represent per color
    #               in a pixel
    # @param[in]    color_format: ColorFormat
    #                   Pixel Encoding of the current mode that is applied.
    # @param[in]    is_compression_enabled: bool
    #                   Indicates whether compression is enabled for the applied mode.
    # @return       (bits_per_pixel, bytes_per_pixel): Tuple[int, float]
    #                   bits_per_pixel - Returns the number of bits required to represent the pixel
    #                   bytes_per_pixel - Returns the number of bytes required to represent the pixel
    @staticmethod
    def get_bits_and_bytes_per_pixel(gfx_index: str, pipe: str, bpc: int, color_format: ColorFormat,
                                     is_compression_enabled: bool) -> Tuple[int, float]:
        bytes_per_pixel = (bpc * 3) / 8
        bits_per_pixel = bpc * 3 * FIXED_POINT_U6_4_CONVERSION

        if is_compression_enabled is True:
            bits_per_pixel = DSCHelper.get_compressed_bpp(gfx_index, pipe)
            if color_format in [ColorFormat.YUV422, ColorFormat.YUV420]:
                bits_per_pixel /= 2

        if ColorFormat.YUV422 == color_format:
            if is_compression_enabled is False:
                bits_per_pixel *= 2.0 / 3
            bytes_per_pixel *= 2.0 / 3
        elif ColorFormat.YUV420 == color_format:
            if is_compression_enabled is False:
                bits_per_pixel /= 2
            bytes_per_pixel /= 2

        logging.debug(f"BPC: {bpc}, Bits Per Pixel (U6.4 Format): {bits_per_pixel}, Bytes Per Pixel: {bytes_per_pixel}")
        return bits_per_pixel, bytes_per_pixel

    ##
    # @brief        Gives the occupied PBN for each of he Time slot by dividing the max available link PBN by the max
    #               possible time slot for the specified encoding.
    # @param[in]    link_rate_gbps: int
    #                   Link at which the display is trained.
    # @param[in]    lane_count: int
    #                   Number of lanes trained as part of link training.
    # @return       pbn_per_time_slot: float
    #                   Returns the PBN that fits in 1 time slot
    @staticmethod
    def get_pbn_per_slot(link_rate_gbps: float, lane_count: int) -> float:
        max_mtp_slots = AVAILABLE_MTP_TIMESLOTS_128B_132B if link_rate_gbps >= 10 else AVAILABLE_MTP_TIMESLOTS_8B_10B
        available_link_pbn = DPHelper.get_available_link_pbn(link_rate_gbps, lane_count)

        pbn_per_time_slot = math.floor((available_link_pbn / max_mtp_slots) * 100) / 100
        logging.info(f"PBN Per Time Slot: {pbn_per_time_slot}")

        return pbn_per_time_slot

    ##
    # @brief        Gives the available PBN by using the link rate and lane count. PBN is another way of denoting the
    #               the bandwidth (required or available)
    #               Refer section 2.6.4.1 in DP 2.1 Spec
    # @param[in]    link_rate_gbps: int
    #                   Link at which the display is trained.
    # @param[in]    lane_count: int
    #                   Number of lanes trained as part of link training.
    # @return       available_pbn: float
    #                   Returns the total available PBN based on the link rate, lane count and BW efficiency.
    @staticmethod
    def get_available_link_pbn(link_rate_gbps: float, lane_count: int) -> int:
        efficiency = DP_DATA_BW_EFFICIENCY_MST_DSC_PER_100
        if link_rate_gbps >= 10:
            efficiency = DP_DATA_BW_EFFICIENCY_128B_132B_PER_100

        available_pbn = int((link_rate_gbps * 1000 * lane_count * efficiency) / 675)
        logging.info(f"Available PBN: {available_pbn}")

        return available_pbn

    ##
    # @brief        Gives the actual PBN that is required for the display. This is calculating using data m and data n
    #               values which in turn is derived from pixel clock, link clock and other link related parameters.
    # @param[in]    data_m: int
    #                   At high level data m refers the amount of data that has to be sent through the link, it includes
    #                the overhead as well.
    # @param[in]    data_n: int
    #                   At high leve data n refers to total bandwidth available considering the link rate, lane count
    #               and bandwidth efficiency.
    # @param[in]    pbn_per_time_slot: float
    #                   PBN occupied by 1 time slot
    # @param[in]    is_ssc_enabled: bool
    #                   True if spread spectrum clock is enabled in VBT and DPCD else False
    # @return       actual_pbn: int
    #                   Returns the actual PBN required for the display to be enabled at the specified data m and data n
    @staticmethod
    def _get_actual_pbn(data_m: int, data_n: int, pbn_per_time_slot: float, is_ssc_enabled: bool) -> int:
        # When SSC is enabled, data m/n factors to 0.25% overhead in pixel clock. So need to add 0.35% overhead while
        # calculating pbn. Required Pixel Bandwidth in PBN = Ceil((data_m/ data_n) * 64 * pbn_per_time_slot * 1.0035)
        if is_ssc_enabled is True:
            actual_pbn = math.ceil((data_m * 64 * pbn_per_time_slot * 1.0035) / data_n)
        else:
            actual_pbn = math.ceil((data_m * 64 * pbn_per_time_slot * 1.006) / data_n)
        logging.info(f"Actual PBN: {actual_pbn}")

        return int(actual_pbn)

    ##
    # @brief        Function to know if the h_blank is less than 1 MTP or not
    # @param[in]    pixel_clock_hz: int
    # @param[in]    h_total: int
    # @param[in]    h_active: int
    # @param[in]    max_link_rate_mbps: int
    # @param[in]    max_lane_count: int
    # @return       True if h_blank is less than 1 MTP else False
    @classmethod
    def is_h_blank_less_than_1_mtp(cls, pixel_clock_hz: int, h_total: int, h_active: int, max_link_rate_mbps: int,
                                   max_lane_count: int) -> bool:
        logging.info(f"pixel clock: {pixel_clock_hz}, h_total: {h_total}, h_active: {h_active}")
        logging.info(f"max_link_rate_mbps: {max_link_rate_mbps}, max_lane_count: {max_lane_count}")

        h_blank = h_total - h_active
        pixel_clock_khz = pixel_clock_hz / 1000
        mtp_size_clocks = 256 / max_lane_count

        mtp_size_fs = round((mtp_size_clocks * (32 * 1000000000)) / max_link_rate_mbps)
        h_blank_fs = round((h_blank * (1000000000 * 1000)) / pixel_clock_khz)

        is_less_than_1_mtp = True if (h_blank_fs <= mtp_size_fs) else False
        logging.info(f"Is Hblank less than 1 MTP: {is_less_than_1_mtp}")

        return is_less_than_1_mtp
