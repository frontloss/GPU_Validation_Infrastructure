#######################################################################################################################
# @file         hf_vsdb_block.py
# @brief        This file contains HdmiForumVendorSpecificDataBlock parser and properties to get the required capability
#               from the HF-VSDB block
# @details      For more information related to the block refer HDMI2.1 Spec E-EDID section
#
# @author       Praburaj Krishnan
#######################################################################################################################

import logging
from typing import Tuple

from Libs.Core import driver_escape
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Feature.hdmi.hf_vsdb_data_mappers import DSC_MAX_SLICES_MAPPING, DSC_FRL_RATE_MAPPING, FRL_RATE_MAPPING
from Libs.Feature.hdmi.sink_caps_data_structures import PayloadByteSix, PayloadByteSeven, PayloadByteEight
from Libs.Feature.hdmi.sink_caps_data_structures import PayloadByteNine, PayloadByteTen
from Libs.Feature.hdmi.sink_caps_data_structures import PayloadByteThree, PayloadByteFour, PayloadByteFive


##
# @brief        This class holds all the SCDS data and exposes properties to get all the required capabilities from the
#               HDMI Forum Vendor Specific Data Block
class HdmiForumVendorSpecificDataBlock:

    ##
    # @brief        Initializes all the data and stores the HDMI file name to be parsed.
    def __init__(self) -> None:
        self._ieee_oui: int = 0xD85DC4
        self._payload_byte_one: int = 0x0
        self._payload_byte_two: int = 0x0
        self._payload_byte_three: PayloadByteThree = PayloadByteThree(Value=0x0)
        self._payload_byte_four: PayloadByteFour = PayloadByteFour(Value=0x0)
        self._payload_byte_five: PayloadByteFive = PayloadByteFive(Value=0x0)
        self._payload_byte_six: PayloadByteSix = PayloadByteSix(Value=0x0)
        self._payload_byte_seven: PayloadByteSeven = PayloadByteSeven(Value=0x0)
        self._payload_byte_eight: PayloadByteEight = PayloadByteEight(Value=0x0)
        self._payload_byte_nine: PayloadByteNine = PayloadByteNine(Value=0x0)
        self._payload_byte_ten: PayloadByteTen = PayloadByteTen(Value=0x0)

    ##
    # @brief        Property to get max TMDS character rate supported by panel
    # @return       Returns int value for max TMDS character rate
    @property
    def max_tmds_character_rate(self) -> int:
        return self._payload_byte_two

    ##
    # @brief        Property to indicate if panels supports RR or not
    # @return       Returns True if panel is RR Capable else False
    @property
    def is_rr_capable(self) -> bool:
        return bool(self._payload_byte_three.rr_capable)

    ##
    # @brief        Property to indicate if LTE_340MHz_scramble bit is enabled or not
    # @return       Returns True if LTE_340MHz_scramble is enabled, else False
    @property
    def is_lte_340mhz_scramble_enabled(self) -> bool:
        return bool(self._payload_byte_three.lte_340MHz_scramble)

    ##
    # @brief        Property to indicate if UHD VIC is set or not
    # @return       Returns True if UHD VIC is set, else False
    @property
    def is_uhd_vic_set(self) -> bool:
        return bool(self._payload_byte_four.uhd_vic)

    ##
    # @brief        Property to indicate Fast VActive Feature is supported or not
    # @return       Returns True if FVA is supported else False
    @property
    def is_fast_v_active_supported(self) -> bool:
        return bool(self._payload_byte_five.fast_v_active)

    ##
    # @brief        Property to indicate if ALLM is supported or not
    # @return       Returns True if ALLM is supported else False
    @property
    def is_allm_supported(self) -> bool:
        return bool(self._payload_byte_five.allm)

    ##
    # @brief        Property to indicate 10BPC feature is supported or not
    # @return       Returns True if 10BPC compression is supported else False
    @property
    def is_10bpc_supported(self) -> bool:
        return bool(self._payload_byte_eight.dsc_10bpc)

    ##
    # @brief        Property to indicate 12BPC feature is supported or not
    # @return       Returns True if 12BPC compression is supported else False
    @property
    def is_12bpc_supported(self) -> bool:
        return bool(self._payload_byte_eight.dsc_12bpc)

    ##
    # @brief        Property to indicate 16BPC feature is supported or not
    # @return       Returns True if 16BPC compression is supported else False
    @property
    def is_16bpc_supported(self) -> bool:
        return bool(self._payload_byte_eight.dsc_16bpc)

    ##
    # @brief        Property to indicate if the panel is capable of handling BPP greater than 12
    # @return       Returns True if panel supports BPP greater than 12
    @property
    def is_dsc_all_bpp_supported(self) -> bool:
        return bool(self._payload_byte_eight.dsc_all_bpp)

    ##
    # @brief        Property to indicate if the panel supports Native 420 color format with compression
    # @return       Returns True if panel supports Native 420 Compression else False
    @property
    def is_dsc_native_420_supported(self) -> bool:
        return bool(self._payload_byte_eight.dsc_native_420)

    ##
    # @brief        Property to indicate if the panel supports DSC1.2a
    # @return       Returns True if panel supports supports DSC1.2a Else False
    @property
    def is_dsc_supported(self) -> bool:
        return bool(self._payload_byte_eight.dsc_1p2)

    ##
    # @brief        Property to indicate if the Panel support HDMI 2.1 FRL
    # @return       Returns a tuple, first field is link rate and second one is lane count
    @property
    def max_frl_rate(self) -> Tuple[int, int]:
        return FRL_RATE_MAPPING[self._payload_byte_four.max_frl_rate]

    ##
    # @brief        Property to get the DSC max link rate and lane count supported by the panel
    # @return       Returns a tuple, first field is link rate and second one is lane count
    @property
    def dsc_max_frl_rate(self) -> Tuple[int, int]:
        return DSC_FRL_RATE_MAPPING[self._payload_byte_nine.dsc_max_frl_rate]

    ##
    # @brief        Property to indicate if the panel supports FRL
    # @return       Returns True if panel supports supports FRL Else False
    @property
    def is_frl_enable(self) -> bool:
        x, y = FRL_RATE_MAPPING[self._payload_byte_four.max_frl_rate]
        return (x, y) != (0, 0)

    ##
    # @brief        Property to get the VRR Min for the panel
    # @return       Return a int value of Vrr Min (Vmin)
    @property
    def vrr_min(self) -> int:
        # Min RR value in payload six from bit 5 to bit 0
        return self._payload_byte_six.vrr_min & 0x3F

    ##
    # @brief        Property to get the VRR max for the panel
    # @return       Return a int value of Vrr Max(Vmax)
    @property
    def vrr_max(self) -> int:
        # Max RR value 2MSB bit comes from six payload six bit sever and eight and 7 LSB from payload seven
        return (self._payload_byte_six.vrr_max_biteightnine << 8 | self._payload_byte_seven.vrr_max_bitzerotoseven) \
               & 0x3FF

    ##
    # @brief        Property to get the DSC max slices and max pixel clock per slice
    # @return       Returns a tuple, first field is slice count and second one is max pixel clock per slice
    @property
    def dsc_max_slices(self) -> Tuple[int, int]:
        return DSC_MAX_SLICES_MAPPING[self._payload_byte_nine.dsc_max_slices]

    ##
    # @brief        Property to get the DSC total chunk bytes
    # @return       Returns the total number of chunk bytes calculated by below formula
    @property
    def dsc_total_chunk_bytes(self) -> int:
        number_of_bytes = 1024 * (1 + self._payload_byte_ten.dsc_total_chunk_bytes)
        return number_of_bytes

    ##
    # @brief        This Member Function Helps to Parse the HF-VSDB Block and Fills the Respective Payload Bytes.
    # @param[in]    gfx_index: str
    #                   Represents the Graphics Adapter to Which the Display is Plugged. E.g. 'gfx_0', 'gfx_1'
    # @param[in]    port_name: str
    #                   Port Name in Which the Display is Plugged. E.g. 'HDMI_B', 'HDMI_C'
    # @return       True if success , False if fail / No VSDB block present.
    def parse_hdmi_forum_vendor_specific_data_block(self, gfx_index: str, port_name: str) -> bool:
        display_adapter_info = DisplayConfiguration().get_display_and_adapter_info_ex(port_name, gfx_index)
        is_success, edid, _ = driver_escape.get_edid_data(display_adapter_info)
        assert is_success, "Driver Escape to Read EDID Failed"

        byte_sequence = bytes(edid)
        index = byte_sequence.find(b'\xD8\x5D\xC4')

        if index == -1:
            logging.error("EDID Doesn't have HDMI Forum Vendor Specific Data Block")
            return False

        # byte_sequence[index - 1] gives Byte zero of HF-VSDB Block where
        # Bit[4:0] = Length of Data Block ; Bit[7:5] = Vendor Specific Tag code

        # Extracting length of HFVSDB block from Bit[4:0]
        length_of_data_block = byte_sequence[index - 1] & 0x1F

        # Fill pay load bytes
        self._payload_byte_one = byte_sequence[index + 3]
        self._payload_byte_two = byte_sequence[index + 4]
        self._payload_byte_three.Value = byte_sequence[index + 5]

        if length_of_data_block > 6:
            self._payload_byte_four.Value = byte_sequence[index + 6]

        if length_of_data_block > 7:
            self._payload_byte_five.Value = byte_sequence[index + 7]

        self._payload_byte_six.Value = byte_sequence[index + 8]
        self._payload_byte_seven.Value = byte_sequence[index + 9]

        # Minimum length of data block should be 11 for DSC fields to be set. Filling DSC fields(_payload_byte_eight)
        # only when length is greater than 10. Without this check, _payload_byte_eight is getting filled with garbage
        # even when DSC fields are not set.
        if length_of_data_block > 10:
            self._payload_byte_eight.Value = byte_sequence[index + 10]

        # Minimum length of data block should be 13 for Additional DSC field to be set.
        if length_of_data_block > 12:
            self._payload_byte_nine.Value = byte_sequence[index + 11]
            self._payload_byte_ten.Value = byte_sequence[index + 12]

        logging.info("HF-VSDB Block Parsed Successfully and Data is Filled")
        return True
