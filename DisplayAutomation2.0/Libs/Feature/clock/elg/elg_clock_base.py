##
# @file     elg_clock_base.py
# @brief    Base class for doing ELG CD clock and port clock validation
# @author   Nainesh P, Doriwala, Sri Sumanth Geesala, Goutham N


import logging
import math
from typing import List

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen14 import Gen14Regs
from DisplayRegs.Gen14.Ddi import Gen14DdiRegs
from DisplayRegs.Gen14.Pll import Gen14PllRegs
from DisplayRegs.Gen14.Transcoder import Gen14TranscoderRegs
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.logger import gdhm
from Libs.Core.vbt import vbt
from Libs.Core.wrapper.driver_escape_args import IGCCSupportedEncoding, IGCCSupportedBpc
from Libs.Feature.clock import clock_helper
from Libs.Feature.clock.elg import elg_clock_dp_snps_phy, elg_clock_helper
from Libs.Feature.clock.elg import elg_clock_hdmi_snps_phy
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock


##
# @brief    This class is the base class for ELG Clock Verifications
# @details  Has bspec Clock Values defined and functions to verify CD Clock Sanity and Phy Test Mode
class ElgClock:
    # CD Clock map as per Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/49419
    cdclock_ctl_freq_dict = dict([
        (163.2, 324),
        (204, 406),
        (244.8, 488),
        (285.6, 569),
        (326.4, 651),
        (367.2, 732),
        (408, 814),
        (448.8, 896),
        (489.6, 977),
        (530.4, 1059),
        (571.2, 1140),
        (612, 1222),
        (652.8, 1304)
    ])

    # DDI values map as in TRANS_DDI_FUNC_CTL register
    ddi_clock_map = dict([
        ('A', 1024),
        ('B', 2048),
        ('C', 4096),
        ('D', 8192),
        ('E', 16384),
        ('F', 2097152),
        ('G', 4194304),
        ('H', 8388608)
    ])
    # DDI PLL map
    ddi_pll_map = dict([
        ('DPLL0', 0),
        ('DPLL1', 1),
        ('DPLL4', 2)
    ])

    # Reference frequency to CD Clock divider map
    cd2x_divider_map = dict([
        (38.4, dict([(172.8, 1), (192, 1), (307.2, 1), (480, 1), (556.8, 1), (652.8, 1)]))
    ])

    # CD Clock squash control squash wave dictionary
    squash_wave_dict = dict([
        (163.2, 34952),
        (204, 37448),
        (244.8, 42148),
        (285.6, 42314),
        (326.4, 43690),
        (367.2, 44378),
        (408, 46774),
        (448.8, 56246),
        (489.6, 61166),
        (530.4, 63454),
        (571.2, 65278),
        (612, 65534),
        (652.8, 65535)
    ])

    # Ref frequency mapping dictionary
    dssm_ref_freq_map = dict([
        (24, 0),
        (19.2, 1),
        (38.4, 2),
        (25, 3)
    ])
    # CD clk pipe mapping dictionary
    cdclock_pipe_dict = dict([
        ('Pipe_A', 0),
        ('Pipe_B', 2),
        ('Pipe_C', 4),
        ('Pipe_D', 6),
        ('None', 7)
    ])

    cdclock_ctl_freq = 0
    expected_cdclock = 168

    ##
    # @brief        Generic function for verifying ELG clock
    # @param[in]    port_name - Port to verify
    # @param[in]    gfx_index - Adapter to verify
    # @return       bool - Returns True if verification is successful, False otherwise
    def verify_clock(self, port_name: str, gfx_index: str) -> bool:
        _clock_helper = clock_helper.ClockHelper()
        target_id = _clock_helper.get_target_id(port_name)
        logging.info(f"******* Clock and PLL Verification of Port : {port_name} (Target ID : 0x{target_id:X}) *******")
        verify = self.verify_sanity(port_name, gfx_index)
        verify = verify and self.verify_phyTestMode(port_name, gfx_index)

        # PICA or port slice verification. Common for DP and HDMI for all ports (A, TC1, TC2, TC3, TC4)
        verify = verify and self.verify_port_slice(port_name, gfx_index)

        # PHY and PLL verification
        clock = None
        if 'HDMI' in str(port_name).upper():
            clock = elg_clock_hdmi_snps_phy.ElgClockHdmiSnpsPhy()
        elif 'DP' in str(port_name).upper():  # Common for eDP and DP
            clock = elg_clock_dp_snps_phy.ElgClockDpSnpsPhy()

        if clock is None:
            logging.error("Clock object is none!")
            gdhm.report_test_bug_di(
                "[Interfaces][Display_Engine][ELG] Clock object is None!")
            return False

        verify &= clock.verify_clock(gfx_index, port_name)

        return verify

    ##
    # @brief        Verify the generic sanity for clock for all the displays
    # @param[in]    port_name - Port to verify
    # @param[in]    gfx_index - Adapter to verify
    # @return       bool - Returns True if verification is successful, False otherwise
    def verify_sanity(self, port_name: str, gfx_index: str) -> bool:
        verify = True
        _clock_helper = clock_helper.ClockHelper()
        offset = Gen14PllRegs.OFFSET_CDCLK_CTL.CDCLK_CTL
        value = DisplayArgs.read_register(offset, gfx_index)
        cdclk_ctl_reg_value = Gen14PllRegs.REG_CDCLK_CTL(offset, value)
        cd2x_divider = cdclk_ctl_reg_value.Cd2XDividerSelect
        logging.debug("{0}-> Offset Value :{1}".format("CDCLK_CTL: CD2X_Divider_Select", cd2x_divider))

        mapped_cd2x_divider = 1 if cd2x_divider == 0 else 'Not a valid Divider'
        cd2x_pipe = cdclk_ctl_reg_value.Cd2XPipeSelect
        mapped_cd2x_pipe = _clock_helper \
            .map_reg_value_to_dict(cd2x_pipe, self.cdclock_pipe_dict, "CDCLK_CTL: CD2X_Pipe_Select")

        offset = Gen14PllRegs.OFFSET_CDCLK_PLL_ENABLE.CDCLK_PLL_ENABLE
        value = DisplayArgs.read_register(offset, gfx_index)
        cdclk_pll_enable_reg_value = Gen14PllRegs.REG_CDCLK_PLL_ENABLE(offset, value)
        pll_enable = cdclk_pll_enable_reg_value.PllEnable

        pll_enable_str = 'ENABLED' if pll_enable == 1 else 'DISABLED'
        pll_lock = cdclk_pll_enable_reg_value.PllLock
        pll_lock_str = 'LOCKED' if pll_lock == 1 else 'UNLOCKED'
        pll_ratio = cdclk_pll_enable_reg_value.PllRatio
        calculated_pll_ratio = 34  # only one supported PLL ratio
        calculated_cd2x_divider = 1

        # check for squashing enabling condition and get expected CD CLK value
        squash_reg_value = _clock_helper. \
            clock_register_read('CDCLK_SQUASH_CTL_REGISTER', 'CDCLK_SQUASH_CTL', gfx_index)
        squash_enable = _clock_helper \
            .get_value_by_range(squash_reg_value, 31, 31, '', "squashing enable")

        if squash_enable:
            squash_window_size = _clock_helper \
                .get_value_by_range(squash_reg_value, 24, 27, '', "squashing enable")
            squash_waveform = _clock_helper \
                .get_value_by_range(squash_reg_value, 0, 15, '', "squashing waveform")

            calculated_squash_waveform = list(self.squash_wave_dict.values())[list(
                self.squash_wave_dict).index(self.expected_cdclock)]

            verify &= _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_SQUASH_CTL",
                                                                   parameter=["Squash Window Size", "Squash Waveform"],
                                                                   expected=[15, calculated_squash_waveform],
                                                                   actual=[squash_window_size, squash_waveform])

        verify &= _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_CTL",
                                                               parameter=["CD2X Div Select", "CD2X Pipe Select"],
                                                               expected=[calculated_cd2x_divider, mapped_cd2x_pipe],
                                                               actual=[mapped_cd2x_divider, mapped_cd2x_pipe])

        # if dc3c0 possible , then HW may dynamically disable CDCLK PLL, so skip this verification
        if not _clock_helper.is_dc3c0_supported(port_name, gfx_index):
            verify &= _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_PLL_ENABLE",
                                                                   parameter=["PLL Enable", "PLL Lock", "PLL Ratio"],
                                                                   expected=['ENABLED', 'LOCKED', calculated_pll_ratio],
                                                                   actual=[pll_enable_str, pll_lock_str, pll_ratio])

        return verify

    ##
    # @brief        Generic function for getting current cd clock
    # @param[in]    gfx_index: str - Graphics index of Graphics adapter
    # @return       current cd clock
    def get_current_cd_clock(self, gfx_index: str):

        # @todo: WA added in driver to disable squashing and always programming max CD clock frequency.
        return max(self.cdclock_ctl_freq_dict.keys())

        # _clock_helper = clock_helper.ClockHelper()
        # offset = Gen14PllRegs.OFFSET_CDCLK_CTL.CDCLK_CTL
        # value = DisplayArgs.read_register(offset, gfx_index)
        # reg_value = Gen14PllRegs.REG_CDCLK_CTL(offset, value)
        # cdclock_ctl_freq = reg_value.CdFrequencyDecimal
        # mapped_cdclock_ctl_freq = _clock_helper \
        #     .map_reg_value_to_dict(cdclock_ctl_freq, self.cdclock_ctl_freq_dict, "CDCLK_CTL: CD Frequency Decimal")
        # logging.info("INFO : Current CD CLOCK : {0} MHz".format(mapped_cdclock_ctl_freq))
        # return mapped_cdclock_ctl_freq

    ##
    # @brief        Generic function for verifying ELG clock
    # @param[in]    display_list - List of active displays
    # @param[in]    gfx_index - Adapter to verify
    # @return       bool - Returns True if verification is successful, False otherwise
    def verify_cdclock(self, display_list: List[str], gfx_index: str) -> bool:
        verify = True
        _clock_helper = clock_helper.ClockHelper()
        mapped_cdclock_ctl_freq = self.get_current_cd_clock(gfx_index)

        # if dynamic cd clk is not enabled, CD CLk value should be programmed as max CD CLK value.
        if not _clock_helper.is_dynamic_cdclock_enabled():
            logging.info(
                "INFO : Dynamic CD Clock NOT Enabled. Current CD CLOCK : {0} MHz".format(mapped_cdclock_ctl_freq))
            self.expected_cdclock = 652.8
            verify &= _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_CTL",
                                                                   parameter="Dynamic CD Clock in MHz",
                                                                   expected=[self.expected_cdclock],
                                                                   actual=[mapped_cdclock_ctl_freq])

            return True

        self.expected_cdclock = self.get_optimal_cdclock(gfx_index, display_list)
        # We can't program cd clk greater than system max cd clk
        if self.expected_cdclock > clock_helper.GEN14PLUS_MAX_CD_CLOCK_MHZ:
            self.expected_cdclock = clock_helper.GEN14PLUS_MAX_CD_CLOCK_MHZ

        verify &= _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_CTL",
                                                               parameter="Dynamic CD Clock in MHz",
                                                               expected=[self.expected_cdclock],
                                                               actual=[mapped_cdclock_ctl_freq])

        return verify

    ##
    # @brief        Function for verifying Phy Test Mode
    # @param[in]    port_name - Port to verify
    # @param[in]    gfx_index - Adapter to verify
    # @return       bool - Returns True if verification is successful, False otherwise
    def verify_phyTestMode(self, port_name: str, gfx_index: str) -> bool:
        from Libs.Feature.vdsc.dsc_helper import DSCHelper
        from Tests.ModeEnumAndSet.display_mode_enumeration_base import ModeEnumAndSetBase
        verify = True
        rounded_pixel_rate, link_symbol_clock = 0, 0
        _clock_helper = clock_helper.ClockHelper()
        is_hdmi_2_1 = _clock_helper.is_hdmi_2_1(port_name, gfx_index)
        hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
        hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, port_name)
        config = display_config.DisplayConfiguration()
        enumerated_displays = config.get_enumerated_display_info()
        display_and_adapter_info = []
        for count in range(enumerated_displays.Count):
            display_name = ((cfg_enum.CONNECTOR_PORT_TYPE(
                enumerated_displays.ConnectedDisplays[count].ConnectorNPortType)).name)
            gfx_adapter = enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo.adapterInfo.gfxIndex
            if (display_name == port_name) and (gfx_adapter == gfx_index):
                if 'HDMI' in str(port_name).upper():
                    display_and_adapter_info.append(enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo)
                    pixel_rate = _clock_helper.get_pixel_rate(port_name)
                    # If HDMI 2.1 is Connected calculate the Rounded Pixel Rate with Div18 Factor
                    # Div18 = MaxFrlBwInMbps * MEGA_HERTZ /18
                    if is_hdmi_2_1:
                        frl_rate_in_gbps = hf_vsdb_parser.max_frl_rate[0]
                        is_compression_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, port_name)

                        # If DSC is enabled in driver, driver trains the link using DSC Max FRL Rate. Take minimum of
                        # Max FRL Rate and DSC Max FRL Rate
                        if is_compression_enabled:
                            frl_rate_in_gbps = min(hf_vsdb_parser.dsc_max_frl_rate[0], frl_rate_in_gbps)

                        frl_rate_in_vbt = ModeEnumAndSetBase.get_hdmi_2_1_frl_rate_in_vbt(port_name)
                        frl_rate_in_gbps = min(frl_rate_in_vbt, frl_rate_in_gbps)

                        # Todo: Use current FRL to calculate pixel rate instead of Max FRL - VSDI-32589
                        # due to rounding-off issue, there might be a precision mismatch
                        # FRL rate returns GBPS data. Convert to KHz and divide / 18, get ceil of this value
                        rounded_pixel_rate = math.ceil(frl_rate_in_gbps * (10 ** 6) / 18)  # in KHz
                        # There is a precision mismatch due to which below rounding off is done.
                        # Eg. Expected value = 92.8125 and actual value = 92.813, so will only compare till 2 digits
                        rounded_pixel_rate = round(rounded_pixel_rate / (10 ** 3), 2)  # convert to MHz
                    else:
                        rounded_pixel_rate = math.ceil(pixel_rate * (10 ** 3)) / (10 ** 3)

                        ##
                        # Get current bpc and encoding for computing rounded pixel rate
                        # More details in Appendix J (Supported video timing limits) of HDMI specs.
                        # HSD-18026517689
                        color_format, bpc, status = _clock_helper.get_bpc_encoding(port_name, gfx_index)

                        # GDHM logging handled inside _clock_helper.get_bpc_encoding().
                        if status is False:
                            return False
                        # YUV420
                        if IGCCSupportedEncoding(color_format) == IGCCSupportedEncoding.YCBCR420:
                            # for Yuv420, pixel clock is 0.5 of pixel clock we get from edid as defined in appendix J of HDMI spec.
                            rounded_pixel_rate = rounded_pixel_rate / 2
                        # No change for other color formats

                        # In case of YCbCr 422, for all BPCs 8/10/12, TMDS Character Rate equals the Pixel Clock Rate.
                        # So, for 10/12 BPC TMDS Character Rate doesn't change.
                        if IGCCSupportedEncoding(color_format) != IGCCSupportedEncoding.YCBCR422:
                            if IGCCSupportedBpc(bpc) == IGCCSupportedBpc.BPC10:
                                rounded_pixel_rate += rounded_pixel_rate / 4
                            elif IGCCSupportedBpc(bpc) == IGCCSupportedBpc.BPC12:
                                rounded_pixel_rate += rounded_pixel_rate / 2
                            # No change for other BPCs

                        # There is a precision mismatch due to which below rounding off is done.
                        # Eg. Expected value = 92.8125 and actual value = 92.813, so will only compare till 2 digits
                        rounded_pixel_rate = round(rounded_pixel_rate, 2)
                elif 'DP' in str(port_name).upper():
                    link_rate = dpcd_helper.DPCD_getLinkRate(
                        enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo)
                    # Control link symbols and data link symbols are of size 32 bits in case of 128b/132b encoding.
                    link_symbol_clock = round(link_rate * 1000 / 32, 2) if link_rate >= 10 else round(link_rate * 100,
                                                                                                      2)

        valfreq_offset = 0
        if str(port_name).upper().__contains__('_A'):
            valfreq_offset = Gen14DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_A
        elif str(port_name).upper().__contains__('_F'):
            valfreq_offset = Gen14DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_USBC1
        elif str(port_name).upper().__contains__('_G'):
            valfreq_offset = Gen14DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_USBC2
        elif str(port_name).upper().__contains__('_H'):
            valfreq_offset = Gen14DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_USBC3
        elif str(port_name).upper().__contains__('_I'):
            valfreq_offset = Gen14DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_USBC4

        value = DisplayArgs.read_register(valfreq_offset, gfx_index)
        reg_value_valfreq = Gen14DdiRegs.REG_DDI_CLK_VALFREQ(valfreq_offset, value)
        valfreq = reg_value_valfreq.DdiValidationFrequency
        # There is a precision mismatch due to which below rounding off is done.
        # Eg. Expected value = 92.8125 and actual value = 92.813, so will only compare till 2 digits
        pixel_rate_Mhz = round((valfreq / 1000), 2)
        calculate_pixel_rate_Mhz = rounded_pixel_rate if str(port_name).upper().__contains__(
            'HDMI') else link_symbol_clock
        verify &= _clock_helper.verify_port_clock_programming_ex(feature="PHY TEST MODE",
                                                                 parameter="Phy Test Mode Val Frequency in MHz",
                                                                 expected=[calculate_pixel_rate_Mhz],
                                                                 actual=[pixel_rate_Mhz])

        return verify

    ##
    # @brief        This function gets the lane count allotted by IOM to display controller on a TC PHY.
    # @details      Note: Even if display is using 2 lanes only, if IOM allots 4 lanes for display, then we get 4 lanes.
    # @param[in]    port_name - Port name like DP_F, HDMI_B, etc
    # @param[in]    gfx_index - Adapter index like 'gfx_0'
    # @return       lane_count - the lane count in integer value.
    def elg_snps_c20_get_lane_count_given_by_IOM(self, port_name: str, gfx_index: str) -> int:
        lane_count = None
        _clock_helper = clock_helper.ClockHelper()

        # if VBT is configured to NATIVE/PLUS/TBT (not TC), always use 4 lanes.
        if not _clock_helper.get_port_type_for_port(port_name).__contains__('TC'):
            lane_count = 4
            return lane_count

        ddi_name = str(port_name).split('_')[1]
        if ddi_name in ['F', 'G']:
            offset = Gen14DdiRegs.OFFSET_PORT_TX_DFLEXPA1.PORT_TX_DFLEXPA1_FIA1
        elif ddi_name in ['H', 'I']:
            offset = Gen14DdiRegs.OFFSET_PORT_TX_DFLEXPA1.PORT_TX_DFLEXPA1_FIA2
        else:
            logging.error(f'Wrong port passed. {port_name} not supported by ELG C20 PHY')
            return None
        value = DisplayArgs.read_register(offset, gfx_index)
        port_tx_dflexpa1 = Gen14DdiRegs.REG_PORT_TX_DFLEXPA1(offset, value)

        if ddi_name in ['F', 'H']:
            pin_assignment = port_tx_dflexpa1.DisplayportPinAssignmentForTypeCConnector0
        else:
            pin_assignment = port_tx_dflexpa1.DisplayportPinAssignmentForTypeCConnector1

        # Assignments D has 2 lanes for DP alternate mode.
        if pin_assignment == Gen14DdiRegs.ENUM_DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0. \
                DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_D.value:
            lane_count = 2
        # Assignments C and E have 4 lanes for DP alternate mode.
        elif pin_assignment in [
            Gen14DdiRegs.ENUM_DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0.
                    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C.value,
            Gen14DdiRegs.ENUM_DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0.
                    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_E.value]:
            lane_count = 4
        else:
            logging.error(f'For {port_name}, unsupported pin_assignment ({pin_assignment}) programmed in '
                          f'PORT_TX_DFLEXPA1 register')
            return None

        return lane_count

    ##
    # @brief        Verification logic for port slice block (PICA registers) for ELG
    # @param[in]    port_name - port name like DP_F, HDMI_B, etc
    # @param[in]    gfx_index - adapter index like 'gfx_0'
    # @return       ret - returns True if all verification passed, False otherwise
    def verify_port_slice(self, port_name: str, gfx_index: str) -> bool:
        ret = True
        _clock_helper = clock_helper.ClockHelper()
        _elg_clock_helper = elg_clock_helper.ElgClockHelper()
        hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
        hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, port_name)
        self.hdmi_2_1_status = hf_vsdb_parser.is_frl_enable
        is_port_dp = True if 'DP' in port_name else False
        is_port_hdmi = True if 'HDMI' in port_name else False
        is_hdmi_2_1_FRL = _clock_helper.is_hdmi_2_1(port_name, gfx_index)
        is_dp_2_0 = _clock_helper.is_dp_2_0(port_name, gfx_index)
        ddi_clock_select_expected = 'div18clk' if is_hdmi_2_1_FRL else 'Maxpclk'
        target_id = _clock_helper.get_target_id(port_name, gfx_index)
        current_link_rate = dpcd_helper.DPCD_getLinkRate(target_id) if is_port_dp else None
        number_of_lanes = dpcd_helper.DPCD_getNumOfLanes(target_id) if is_port_dp else None
        if is_hdmi_2_1_FRL:
            number_of_lanes = hf_vsdb_parser.max_frl_rate[1]
        gfx_vbt = vbt.Vbt(gfx_index)
        vbt_panel_index = gfx_vbt.get_panel_index_for_port(port_name)
        expected_port_reversal = 1 if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[vbt_panel_index].Flags1 \
                                      & 0b10 else 0
        get_ddi = display_base.DisplayBase(port_name, 'ELG', gfx_index)
        pipe_ddi = get_ddi.GetPipeDDIAttachedToPort(port_name, gfx_index=gfx_index)
        pipe = (pipe_ddi[0])[-1]
        offset = eval('Gen14TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_' + pipe)
        value = DisplayArgs.read_register(offset, gfx_index)
        trans_hdmi_port_width = Gen14TranscoderRegs.REG_TRANS_DDI_FUNC_CTL(offset, value)
        transcoder_port_width_value = trans_hdmi_port_width.PortWidthSelection

        # map based on values of 'DDI Clock Select' of register PORT_CLOCK_CTL in bspec:
        # https://gfxspecs.intel.com/Predator/Home/Index/65103?dstFilter=ELG&mode=Filter
        ddi_clk_select_map = {
            0b1000: 'Maxpclk',
            0b1001: 'div18clk',
            0b1100: 'TBT 162',
            0b1101: 'TBT 270',
            0b1110: 'TBT 540',
            0b1111: 'TBT 810'
        }
        # map based on values of 'Port Width' of register PORT_BUF_CTL1 in bspec:
        # https://gfxspecs.intel.com/Predator/Home/Index/65091?dstFilter=ELG&mode=Filter
        port_width_lanes_map = {
            0b000: 1,
            0b001: 2,
            0b011: 4,
            0b100: 3
        }

        ddi_name = str(port_name).split('_')[1]
        bspec_port_name = _elg_clock_helper.ddi_to_bspec_name_map[ddi_name.upper()]
        # determine which msgbus PHY lanes are owned by display controller
        if bspec_port_name.__contains__('USBC'):
            no_of_lanes_given_by_IOM = self.elg_snps_c20_get_lane_count_given_by_IOM(port_name, gfx_index)
            logging.info(f'For {port_name}, IOM has given {no_of_lanes_given_by_IOM} lanes to display controller.')
            if no_of_lanes_given_by_IOM == 4:
                msgbus_phy_lanes_owned = ['0', '1']
            elif expected_port_reversal:
                msgbus_phy_lanes_owned = ['1']
            else:
                msgbus_phy_lanes_owned = ['0']
        else:
            msgbus_phy_lanes_owned = ['0', '1']

        offset = eval('Gen14DdiRegs.OFFSET_PORT_BUF_CTL1.PORT_BUF_CTL1_' + bspec_port_name)
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl1 = Gen14DdiRegs.REG_PORT_BUF_CTL1(offset, value)

        offset = eval('Gen14DdiRegs.OFFSET_PORT_BUF_CTL2.PORT_BUF_CTL2_' + bspec_port_name)
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl2 = Gen14DdiRegs.REG_PORT_BUF_CTL2(offset, value)

        offset = eval('Gen14DdiRegs.OFFSET_PORT_BUF_CTL3.PORT_BUF_CTL3_' + bspec_port_name)
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl3 = Gen14DdiRegs.REG_PORT_BUF_CTL3(offset, value)

        offset = eval('Gen14PllRegs.OFFSET_PORT_CLOCK_CTL.PORT_CLOCK_CTL_' + bspec_port_name)
        value = DisplayArgs.read_register(offset, gfx_index)
        port_clock_ctl = Gen14PllRegs.REG_PORT_CLOCK_CTL(offset, value)

        # Dictionary to map the Decimal Value of Port Width from Register and Transcoder
        # Ref: https://gfxspecs.intel.com/Predator/Home/Index/50493
        port_width_transcoder_map = {
            0b000: 1,
            0b001: 2,
            0b010: 3,
            0b011: 4
        }

        # verify PORT_BUF_CTL1 register
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                              parameter="IO Select",
                                                              expected=[0], actual=[port_buf_ctl1.IoSelect])
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                              parameter="D2D Link Enable",
                                                              expected=[1], actual=[port_buf_ctl1.D2DLinkEnable])
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                              parameter="Data Width",
                                                              expected=[
                                                                  1 if is_hdmi_2_1_FRL else 2 if is_dp_2_0 else 0],
                                                              actual=[port_buf_ctl1.DataWidth])
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                              parameter="Port Reversal",
                                                              expected=[expected_port_reversal],
                                                              actual=[port_buf_ctl1.PortReversal])
        if is_port_dp:  # TODO: Need to get lane count for HDMI and add verification for it also
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                                  parameter="Port Width",
                                                                  expected=[number_of_lanes],
                                                                  actual=[
                                                                      port_width_lanes_map[port_buf_ctl1.PortWidth]])
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                              parameter="HDMI FRL Shifter Enable",
                                                              expected=[1 if is_hdmi_2_1_FRL else 0],
                                                              actual=[port_buf_ctl1.HdmiFrlShifterEnable])
        if is_hdmi_2_1_FRL:
            if port_width_lanes_map[port_buf_ctl1.PortWidth] == port_width_transcoder_map[transcoder_port_width_value]:
                ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                                      parameter="Port Width",
                                                                      expected=[number_of_lanes],
                                                                      actual=[port_width_lanes_map[
                                                                                  port_buf_ctl1.PortWidth]])
            else:
                ret = False
                logging.error(
                    "Port Width Verification Failed. PORT_BUF_CTL register and Transcoder Port Width values did not match")

        # verify PORT_BUF_CTL2 register
        # Clear PORT_BUF_CTL2<port> Lane<PHY Lanes Owned*> Pipe Reset to 0.
        # (part of "Bring owned* PHY lanes out of Reset."
        for lane in msgbus_phy_lanes_owned:
            param = "Lane" + lane + "PipeReset"
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL2_" + bspec_port_name,
                                                                  parameter=param,
                                                                  expected=[0],
                                                                  actual=[eval('port_buf_ctl2.' + param)])

        # Set PORT_BUF_CTL2<port> Lane<0/1> Powerdown New State = 0x2
        # (part of "Change owned* PHY lanes power to Ready state (PHY power control)")
        for lane in msgbus_phy_lanes_owned:
            param = "Lane" + lane + "PowerdownNewState"
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL2_" + bspec_port_name,
                                                                  parameter=param,
                                                                  expected=[2],
                                                                  actual=[eval('port_buf_ctl2.' + param)])

        # PORT_BUF_CTL2<port> Power State in Ready = Ready value (2) for this PHY type
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL2_" + bspec_port_name,
                                                              parameter="PowerStateInReady",
                                                              expected=[2],
                                                              actual=[port_buf_ctl2.PowerStateInReady])

        # verify PORT_BUF_CTL3 register
        # PORT_BUF_CTL3<port> Power State in Active = Active value (0) for this PHY type
        # (part of "Change owned* PHY lanes power to Ready state (PHY power control)")
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL3_" + bspec_port_name,
                                                              parameter="PowerStateInActive",
                                                              expected=[0],
                                                              actual=[port_buf_ctl3.PowerStateInActive])

        # verify PORT_CLOCK_CTL register
        # PHY Clock Lane Select = 1 for PORT_BUF_CTL1 Port Reversal set, else 0
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                              parameter="PHY Clock Lane Select",
                                                              expected=[port_buf_ctl1.PortReversal],
                                                              actual=[port_clock_ctl.PhyClockLaneSelect])
        # DDI Clock Select = div18clk for HDMI 2.1 FRL, else Maxpclk
        if port_clock_ctl.DdiClockSelect in ddi_clk_select_map.keys():
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                                  parameter="DDI Clock Select",
                                                                  expected=[ddi_clock_select_expected],
                                                                  actual=[ddi_clk_select_map[
                                                                              port_clock_ctl.DdiClockSelect]])
        else:
            logging.error(f'PORT_CLOCK_CTL_{bspec_port_name}.DdiClockSelect value is invalid. Value = '
                          f'{port_clock_ctl.DdiClockSelect}')
            ret &= False
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                              parameter="Forward Clock Ungate",
                                                              expected=[1],
                                                              actual=[port_clock_ctl.ForwardClockUngate])

        if 'DP' in port_name:
            is_ssc_enabled = display_base.GetSSC(port_name, gfx_index)

            # But as HW response is buggy today, DP 2.1 SSC will be enabled based on VBT & DPCD support.
            expected_ssc_on_pll_a = 0
            if is_ssc_enabled and current_link_rate in [10.0, 20.0]:
                expected_ssc_on_pll_a = 1

            # SSC Enable PLL A = 1 for DP 2.0 (always uses PLL A and SSC), else 0
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                                  parameter="SSC Enable PLL A",
                                                                  expected=[expected_ssc_on_pll_a],
                                                                  actual=[port_clock_ctl.SscEnablePllA])

            # For PLL B Set SSC Enable as required for DP 1.4 or eDP or DP 2.0 UHBR 13.5 (1 for SSC and 0 for no SSC).
            expected_ssc_on_pll_b = 0
            if is_ssc_enabled and current_link_rate not in [10.0, 20.0]:
                expected_ssc_on_pll_b = 1

            # SSC Enable PLL B = 1 if SSC is needed with DP 1.4 or eDP, else 0
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                                  parameter="SSC Enable PLL B",
                                                                  expected=[expected_ssc_on_pll_b],
                                                                  actual=[port_clock_ctl.SscEnablePllB])

        # Set PORT_CLOCK_CTL PCLK Refclk Request LN<Lane for maxPCLK**> = 1.
        # (part of "Bring owned* PHY lanes out of Reset.")
        if ddi_clock_select_expected == 'Maxpclk':
            # if port reversal is set, lane for maxPCLK will be Lane_1, else Lane_0.
            if expected_port_reversal:
                param = "PclkRefclkRequestLn1"
            else:
                param = "PclkRefclkRequestLn0"
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                                  parameter=param,
                                                                  expected=[1],
                                                                  actual=[eval('port_clock_ctl.' + param)])

        # Set PORT_CLOCK_CTL register PCLK PLL Request LN<Lane for maxPCLK**> to "1" to enable PLL.
        if ddi_clock_select_expected == 'Maxpclk':
            # if port reversal is set, lane for maxPCLK will be Lane_1, else Lane_0.
            if expected_port_reversal:
                param = "PclkPllRequestLn1"
            else:
                param = "PclkPllRequestLn0"
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                                  parameter=[param],
                                                                  expected=[1],
                                                                  actual=[eval('port_clock_ctl.' + param)])

        return ret

    ##
    # @brief        Function for calculating optimal cd clock with given pixel_rate
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @param[in]    max_pixel_rate: float
    #                   Maximum pixel rate
    # @param[in]    display_list: list
    #                   List of Display
    # @return       optimal_cdclock: float
    #                   returns the optimal cd clock in MHz
    def get_optimal_cd_clock_from_pixelclock(self, gfx_index: str, max_pixel_rate: float,
                                             display_list: List[str]) -> float:

        # @todo: WA added in driver to disable squashing and always programming max CD clock frequency.
        return max(self.cdclock_ctl_freq_dict.keys())

        #  Below code is commented for that purpose.
        # optimal_cdclock = 0
        # _clock_helper = clock_helper.ClockHelper()
        # max_dsc_slice_one_pixel_clock = _clock_helper.get_max_dsc_slice_1_pixel_clock('gfx_0', display_list)
        #
        # # For DSC Displays with Slice Count of 1, Optimal Cd Clock using 2ppc method will not be sufficient to drive the
        # # Display as only one DSC Engine will be active and this DSC Engine Clock will be synchronized with the CD Clock
        # # not CD Clock x 2. Hence For DSC Displays with Slice Count 1 optimal cd clock will be determined with 1ppc
        # # method. For this purpose, pixel clock of dsc display will be multiplied by 2 and the resultant max pixel rate
        # # will be used to determine optimal cd clock
        # supported_pixel_rate = max(max_pixel_rate, max_dsc_slice_one_pixel_clock * 2)
        #
        # # reference_freq currently hardcoded in driver, as DSSM Register is not recommended for Yet. Only
        # # value possible for ELG is 2 as per BSpec which is 38.4MHz
        # reference_freq = 2
        # mapped_ref_freq = _clock_helper \
        #     .map_reg_value_to_dict(reference_freq, self.dssm_ref_freq_map, "CD Clock Frequency")
        #
        # # Cd Clock values for 38.4 Mhz Reference Frequency
        # if mapped_ref_freq == 38.4:
        #     # check for squashing enabling condition and get expected CD CLK value
        #     squash_reg_value = _clock_helper. \
        #         clock_register_read('CDCLK_SQUASH_CTL_REGISTER', 'CDCLK_SQUASH_CTL', gfx_index)
        #     squash_enable = _clock_helper \
        #         .get_value_by_range(squash_reg_value, 31, 31, '', "squashing enable")
        #
        #     # if dynamic cd clk is not enabled, CD CLk value should be programmed as max CD CLK value.
        #     # TODO: Remove is_dynamic_cdclock_enabled() check, once GOP is updated for BMG - VSDI-42558
        #     if squash_enable and _clock_helper.is_dynamic_cdclock_enabled():
        #         optimal_cdclock = 163.2 if supported_pixel_rate < 326.4 else \
        #             204 if supported_pixel_rate < 408 else \
        #                 244.8 if supported_pixel_rate < 489.6 else \
        #                     285.6 if supported_pixel_rate < 571.2 else \
        #                         326.4 if supported_pixel_rate < 652.8 else \
        #                             367.2 if supported_pixel_rate < 734.4 else \
        #                                 408 if supported_pixel_rate < 816 else \
        #                                     448.8 if supported_pixel_rate < 897.6 else \
        #                                         489.6 if supported_pixel_rate < 979.2 else \
        #                                             530.4 if supported_pixel_rate < 1060.8 else \
        #                                                 571.2 if supported_pixel_rate < 1142.4 else \
        #                                                     612 if supported_pixel_rate < 1224 else 652.8
        #     else:
        #         optimal_cdclock = 652.8  # Max platform supported CD clock
        #
        # logging.info("Optimal Cd clock: {}MHz".format(optimal_cdclock))
        # return optimal_cdclock

    ##
    # @brief        function for calculating optimal cd clock
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @param[in]    display_list: list
    #                   List of Display
    # @return       optimal_cdclock: float
    #                   returns the optimal cd clock in MHz
    def get_optimal_cdclock(self, gfx_index: str, display_list: list) -> float:

        # @todo: WA added in driver to disable squashing and always programming max CD clock frequency.
        return max(self.cdclock_ctl_freq_dict.keys())

        # _clock_helper = clock_helper.ClockHelper()
        #
        # supported_pixel_rate = _clock_helper.get_max_pixel_rate(display_list)
        #
        # # Check if the mode is pipe ganged modeset and get the number of pipes required to drive the mode.
        # is_pipe_joiner_required, no_of_pipe_required = False, 1
        # effective_cd_clock_hz = clock_helper.GEN14PLUS_EFFECTIVE_CD_CLOCK_MHZ * 1000000
        # for disp in display_list:
        #     logging.info("disp:{}".format(disp))
        #     is_pipe_joiner_required, no_of_pipe_required = _clock_helper.is_pipe_joiner_required(
        #         gfx_index, disp, effective_cd_clock_hz)
        #     if is_pipe_joiner_required is True:
        #         break
        #
        # # Divide the pixel rate by no of pipes to get the correct pixel rate for each of the pipe.
        # supported_pixel_rate = supported_pixel_rate / no_of_pipe_required
        # optimal_cdclock = self.get_optimal_cd_clock_from_pixelclock(gfx_index, supported_pixel_rate, display_list)
        #
        # return optimal_cdclock

    ##
    # @brief        Verifies PCode notified Voltage Level as part of CD clock programming
    # @param[in]    gfx_index: Graphics Adapter Index
    # @param[in]    ports: List of port names of active displays
    # @return       bool - True if verification is successful, False otherwise
    def verify_voltage_level_notified_to_pcode(self, gfx_index: str, ports: List[str]) -> bool:
        _clock_helper = clock_helper.ClockHelper()
        _display_config = display_config.DisplayConfiguration()
        _elg_clock_helper = elg_clock_helper.ElgClockHelper()

        port_scaling = {}
        for port_name in ports:
            display_and_adapter_info = _display_config.get_display_and_adapter_info_ex(port_name, gfx_index)
            if type(display_and_adapter_info) is list:
                display_and_adapter_info = display_and_adapter_info[0]
            current_mode = _display_config.get_current_mode(display_and_adapter_info)
            port_scaling[port_name] = current_mode.scaling == enum.MDS
        # Check if all displays connected have MDS modes.
        # If only scaled mode is present, driver would not have calculated DVFS Voltage requirement
        if all(v for v in port_scaling.values()) is False:
            logging.warning("Skipping DVFS verification for scaled modes across panels!!")
            # gdhm.report_test_bug_pc("Skipping DVFS verification for scaled modes across panels!!",
            #                         priority=gdhm.Priority.P4, exposure=gdhm.Exposure.E3)
            logging.info(f"Displays over {gfx_index} = {port_scaling.keys()}")
            return True  # Skip DVFS verification
        expected_cdclock = self.get_optimal_cdclock(gfx_index, ports)

        # @todo: Driver is currently programming based on source resolution. Need to confirm with bspec recommendation.
        # Driver recommended flow - Check if MDS scaling is applied,
        #   If MDS, calculate VoltageLevel and verify the same.
        #   Else, ensure previously configured VoltageLevel is maintained.
        # VoltageLevel programming will not happen when scaled modes are applied for same src mode/active desktop signal

        # Bspec recommended flow - yet to be identified.
        #   Assuming it should be based on max pixel clock of active panels and symbol frequency requirements.

        # MMIO based verification for checking DVFS level from Gen14+ platforms
        pm_dmd_req_offset = Gen14Regs.OFFSET_INITIATE_PM_DMD_REQ.INITIATE_PM_DMD_REQ
        pm_dmd_req_register = DisplayArgs.read_register(pm_dmd_req_offset, gfx_index)
        pm_dmd_req_reg_value = Gen14Regs.REG_INITIATE_PM_DMD_REQ(pm_dmd_req_offset, pm_dmd_req_register)
        logging.debug(f"INITIATE_PM_DMD_REQ register value - 0x{pm_dmd_req_reg_value.value:X}")
        actual_voltage_level_index = pm_dmd_req_reg_value.VoltageLevelIndex
        actual_ddi_clk_freq = pm_dmd_req_reg_value.DdiclkFreq
        logging.info(f"Programmed [VoltageLevelIndex, DdiclkFreq] = [{actual_voltage_level_index}, "
                     f"{actual_ddi_clk_freq}]")

        # @todo: WA added in driver to disable squashing and always programming max CD clock frequency.

        # max_ddi_freq_target, max_ddi_freq = _elg_clock_helper.get_max_ddi_symbol_clock_frequency(gfx_index, ports)
        # logging.info(f"Target {max_ddi_freq_target} with max DDI freq = {max_ddi_freq}")
        #
        # # Ref: DVFS programming expectation - https://gfxspecs.intel.com/Predator/Home/Index/65565
        # if expected_cdclock <= 307.2 and max_ddi_freq <= 594:
        #     expected_voltage_level_index = Gen14Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_0.value
        #     if actual_voltage_level_index != expected_voltage_level_index:
        #         # logging.warning("Assigning next VoltageLevel since it should not have any power functionality issue")
        #         # expected_voltage_level_index = actual_voltage_level_index
        #         gdhm.report_test_bug_pc("[Interfaces][Display_Engine][CD Clock][WARNING] Lower VoltageLevel calculated",
        #                                 priority=gdhm.Priority.P3, exposure=gdhm.Exposure.E3)
        # elif expected_cdclock <= 480:
        #     expected_voltage_level_index = Gen14Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_1.value
        # elif expected_cdclock <= 556.8:
        #     expected_voltage_level_index = Gen14Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_2.value
        # else:
        #     # Max CD Clock frequency requires Voltage Level 3 to be programmed
        #     expected_voltage_level_index = Gen14Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_3.value
        # logging.info(f"Expected VoltageLevel = {expected_voltage_level_index}")

        expected_voltage_level_index = Gen14Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_3.value
        logging.info(f"Expected VoltageLevel = {expected_voltage_level_index}")

        return _clock_helper.verify_cd_clock_programming_ex(feature="INITIATE_PM_DMD_REQ",
                                                            parameter=["VoltageLevelIndex"],
                                                            expected=[expected_voltage_level_index],
                                                            actual=[actual_voltage_level_index])
