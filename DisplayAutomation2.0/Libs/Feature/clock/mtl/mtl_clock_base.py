##
# @file    mtl_clock_base.py
# @brief   Base class for doing MTL CD clock and port clock validation
# @author  Veena Veluru, Sri Sumanth Geesala


import logging
import math
from typing import List

from DisplayRegs import DisplayArgs, NonAutoGenRegs
from DisplayRegs.Gen14 import Gen14Regs
from DisplayRegs.Gen14.Ddi import Gen14DdiRegs
from DisplayRegs.Gen14.Pll import Gen14PllRegs
from DisplayRegs.Gen14.Transcoder import Gen14TranscoderRegs
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.logger import gdhm
from Libs.Core.system_utility import SystemUtility
from Libs.Core.vbt import vbt
from Libs.Core.wrapper.driver_escape_args import IGCCSupportedEncoding, IGCCSupportedBpc
from Libs.Feature.clock import clock_helper, display_clock
from Libs.Feature.clock.clock_helper import DEFAULT_REFERENCE_CLOCK_FREQUENCY
from Libs.Feature.clock.mtl import mtl_clock_dp_snps_phy
from Libs.Feature.clock.mtl import mtl_clock_hdmi_snps_phy
from Libs.Feature.clock.mtl import mtl_clock_helper
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.hdmi.hf_vsdb_block import HdmiForumVendorSpecificDataBlock


##
# @brief    This class is the base class for MTL Clock Verifications
# @details  Has bspec Clock Values defined and functions to verify CD Clock and Phy Test Mode
class MtlClock:
    # CD Clock map as per Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/49419
    cdclock_ctl_freq_dict = dict([
        (172.8, 344),
        (192, 382),
        (307.2, 612),
        (480, 958),
        (556.8, 1112),
        (652.8, 1304)
    ])

    # Reference Frequency to Cd Clock map as per bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/49419
    cdclock_map = dict([
        (DEFAULT_REFERENCE_CLOCK_FREQUENCY,
         dict([(172.8, 16), (192, 16), (307.2, 16), (480, 25), (556.8, 29), (652.8, 34)]))
    ])

    # CD Clock squash enable mapping
    squash_enable_dict = dict([
        (172.8, 1),
        (192, 1),
        (307.2, 1),
        (480.0, 0),
        (556.8, 0),
        (652.8, 0)]
    )

    # CD Clock squash control squash wave dictionary
    squash_wave_dict = dict([
        (172.8, 44378),
        (192, 46774),
        (307.2, 65535),
        (480.0, 65535),
        (556.8, 65535),
        (652.8, 65535)
    ])

    ##
    # @brief        Generic function for verifying MTL clock
    # @param[in]    port_name - Port to verify
    # @param[in]    gfx_index - Adapter to verify
    # @return       bool - Returns True if verification is successful, False otherwise
    @staticmethod
    def verify_clock(port_name: str, gfx_index: str) -> bool:
        _clock_helper = clock_helper.ClockHelper()
        _system_utility = SystemUtility()
        target_id = _clock_helper.get_target_id(port_name)
        logging.info(f"******* Clock and PLL Verification of Port : {port_name} (Target ID : 0x{target_id:X}) *******")
        verify = MtlClock.verify_phy_test_mode(port_name, gfx_index)

        # PICA or port slice verification. Common for DP and HDMI for all ports (A, B, TC1, TC2, TC3, TC4)
        verify = verify and MtlClock.verify_port_slice(port_name, gfx_index)

        # PHY and PLL verification. As Snps Phy is not modeled in pre-si, this verification enabled only for post-si
        execution_environment_type = _system_utility.get_execution_environment_type()
        if execution_environment_type is not None and execution_environment_type == "POST_SI_ENV":
            clock = None
            if str(port_name).upper().__contains__('HDMI'):
                clock = mtl_clock_hdmi_snps_phy.MtlClockHdmiSnpsPhy()
            elif str(port_name).upper().__contains__('DP'):  # Common for eDP and DP
                clock = mtl_clock_dp_snps_phy.MtlClockDpSnpsPhy()
            verify = verify and clock.verify_clock(port_name, gfx_index)

        return verify

    ##
    # @brief        Generic function for getting current cd clock
    # @param[in]    gfx_index: str - Graphics index of Graphics adapter
    # @param[in]    reference_clock: float - [Optional] Reference clock frequency in MHz
    # @return       current cd clock
    def get_current_cd_clock(self, gfx_index: str, reference_clock: float = 0) -> float:
        current_cd_clock_freq = 0
        _clock_helper = clock_helper.ClockHelper()

        # Fetch reference clock if not passed
        if reference_clock == 0:
            reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)
            logging.debug(f"Programmed Reference clock = {reference_clock} MHz")

        # Only supported reference clock is 38.4 MHz
        if reference_clock != DEFAULT_REFERENCE_CLOCK_FREQUENCY:
            logging.error(f"Invalid Reference clock programmed. Expected: DEFAULT_REFERENCE_CLOCK_FREQUENCY MHz, "
                          f"Actual: {reference_clock} MHz")
            return current_cd_clock_freq

        offset = Gen14PllRegs.OFFSET_CDCLK_CTL.CDCLK_CTL
        value = DisplayArgs.read_register(offset, gfx_index)
        reg_value = Gen14PllRegs.REG_CDCLK_CTL(offset, value)
        cdclk_freq_decimal = reg_value.CdFrequencyDecimal
        current_cd_clock_freq = _clock_helper \
            .map_reg_value_to_dict(cdclk_freq_decimal, self.cdclock_ctl_freq_dict, "CDCLK_CTL: CD Frequency Decimal")
        logging.info(f"INFO : Current CD CLOCK : {current_cd_clock_freq} MHz")
        return current_cd_clock_freq

    ##
    # @brief        Generic function for verifying MTL clock
    # @param[in]    display_list - List of active displays
    # @param[in]    gfx_index - Adapter to verify
    # @return       bool - Returns True if verification is successful, False otherwise
    def verify_cdclock(self, display_list: List[str], gfx_index: str) -> bool:
        _clock_helper = clock_helper.ClockHelper()
        _display_clock = display_clock.DisplayClock()

        # Get Reference Frequency
        reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)
        logging.info(f"Programmed Reference clock = {reference_clock} MHz")

        # Only supported reference clock is DEFAULT_REFERENCE_CLOCK_FREQUENCY MHz
        if reference_clock != DEFAULT_REFERENCE_CLOCK_FREQUENCY:
            logging.error(
                f"Invalid Reference clock programmed. Expected: DEFAULT_REFERENCE_CLOCK_FREQUENCY MHz, "
                f"Actual: {reference_clock} MHz")
            gdhm.report_test_bug_pc(
                title=f"[Interfaces][Display_Engine][CD Clock] Invalid reference clock frequency programmed",
            )
            return False

        expected_cdclock = self.get_optimal_cdclock(gfx_index, display_list)

        # Read CDCLK_CTL register
        cdclk_ctl_offset = Gen14PllRegs.OFFSET_CDCLK_CTL.CDCLK_CTL
        cdclk_ctl_value = DisplayArgs.read_register(cdclk_ctl_offset, gfx_index)
        cdclk_ctl_reg_value = Gen14PllRegs.REG_CDCLK_CTL(cdclk_ctl_offset, cdclk_ctl_value)
        cdclk_freq_decimal = cdclk_ctl_reg_value.CdFrequencyDecimal
        cd2x_divider_select = cdclk_ctl_reg_value.Cd2XDividerSelect
        cd2x_pipe_select = cdclk_ctl_reg_value.Cd2XPipeSelect
        logging.debug(f"Programmed [CdFrequencyDecimal, Cd2XDividerSelect, Cd2XPipeSelect] = [{cdclk_freq_decimal}, "
                      f"{cd2x_divider_select}, {cd2x_pipe_select}]")

        # CDCLK_PLL_ENABLE register
        cdclk_pll_enable_offset = Gen14PllRegs.OFFSET_CDCLK_PLL_ENABLE.CDCLK_PLL_ENABLE
        cdclk_pll_enable_value = DisplayArgs.read_register(cdclk_pll_enable_offset, gfx_index)
        cdclk_pll_enable_reg_value = Gen14PllRegs.REG_CDCLK_PLL_ENABLE(cdclk_pll_enable_offset, cdclk_pll_enable_value)
        pll_enable = cdclk_pll_enable_reg_value.PllEnable
        pll_lock = cdclk_pll_enable_reg_value.PllLock
        pll_ratio = cdclk_pll_enable_reg_value.PllRatio
        freq_change_request = cdclk_pll_enable_reg_value.FreqChangeReq
        logging.debug(f"Programmed [PllEnable, PllLock, PllRatio, FreqChangeReq] = [{pll_enable}, {pll_lock}, "
                      f"{pll_ratio}, {freq_change_request}]")

        # CDCLK_SQUASH_CTL register
        squash_ctl_value = _clock_helper.clock_register_read('CDCLK_SQUASH_CTL_REGISTER', 'CDCLK_SQUASH_CTL', gfx_index)
        squash_enable = _clock_helper.get_value_by_range(squash_ctl_value, 31, 31, '', "squashing enable")
        squash_window_size = _clock_helper.get_value_by_range(squash_ctl_value, 24, 27, '', "squashing window size")
        squash_waveform = _clock_helper.get_value_by_range(squash_ctl_value, 0, 15, '', "squashing waveform")
        logging.debug(f"Programmed [SquashEnable, SquashWaveform, SquashWindowSize] = [{squash_enable}, "
                      f"{squash_waveform}, {squash_window_size}]")

        # get bios-programmed max cd clock supported by the system
        system_max_cd_clk = self.get_system_max_cd_clk(gfx_index)
        logging.debug(f"System max CD clock: {system_max_cd_clk} MHz")

        # String computation for verification purpose
        expected_cd2x_divider_str = Gen14PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.name
        # Todo: Pipe select programming to be fixed
        # expected_cd2x_pipe_select_str = Gen14PllRegs.ENUM_CD2X_PIPE_SELECT.CD2X_PIPE_SELECT_NONE.name
        expected_pll_enable_str = Gen14PllRegs.ENUM_PLL_ENABLE.PLL_ENABLE.name
        expected_pll_lock_str = Gen14PllRegs.ENUM_PLL_LOCK.PLL_LOCK_LOCKED.name
        expected_freq_change_request_str = Gen14PllRegs.ENUM_FREQ_CHANGE_ACK. \
            FREQ_CHANGE_ACK_NO_PENDING_REQUEST_OR_REQUEST_NOT_FINISHED.name

        current_cd_clock_freq = _clock_helper \
            .map_reg_value_to_dict(cdclk_freq_decimal, self.cdclock_ctl_freq_dict, "CDCLK_CTL: CD Frequency Decimal")
        logging.info(f"INFO : Current CD CLOCK : {current_cd_clock_freq} MHz")

        cd2x_divider_select_str = Gen14PllRegs.ENUM_CD2X_DIVIDER_SELECT(cd2x_divider_select).name
        cd2x_pipe_select_str = Gen14PllRegs.ENUM_CD2X_PIPE_SELECT(cd2x_pipe_select).name \
            if any(cd2x_pipe_select == x.value for x in Gen14PllRegs.ENUM_CD2X_PIPE_SELECT.__members__.values()) \
            else f"PIPE_INVALID_{cd2x_pipe_select}"
        pll_enable_str = Gen14PllRegs.ENUM_PLL_ENABLE(pll_enable).name
        pll_lock_str = Gen14PllRegs.ENUM_PLL_LOCK(pll_lock).name
        freq_change_request_str = Gen14PllRegs.ENUM_FREQ_CHANGE_ACK(freq_change_request).name

        pll_ratio_map = list(self.cdclock_map.values())[list(self.cdclock_map).index(reference_clock)]
        expected_pll_ratio = list(pll_ratio_map.values())[list(pll_ratio_map).index(expected_cdclock)]

        expected_squash_enable = list(self.squash_enable_dict.values())[
            list(self.squash_enable_dict).index(expected_cdclock)]
        expected_squash_waveform = list(self.squash_wave_dict.values())[
            list(self.squash_wave_dict).index(expected_cdclock)]
        expected_squash_window_size = 15

        # if dynamic cd clk is not enabled, return without verification
        if not _clock_helper.is_dynamic_cdclock_enabled():
            logging.info(f"INFO : Dynamic CD Clock NOT Enabled. Current CD CLOCK : {current_cd_clock_freq} MHz")
            return True

        verify = _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_CTL", parameter="Dynamic CD Clock in MHz",
                                                              expected=[expected_cdclock],
                                                              actual=[current_cd_clock_freq])

        # check for squashing enabling condition and get expected CD CLK value
        verify = verify and _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_SQUASH_CTL",
                                                                         parameter=["Squash Enable",
                                                                                    "Squash Window Size",
                                                                                    "Squash Waveform"],
                                                                         expected=[expected_squash_enable,
                                                                                   expected_squash_window_size,
                                                                                   expected_squash_waveform],
                                                                         actual=[squash_enable, squash_window_size,
                                                                                 squash_waveform])

        # for MTL divider can be mapped to reference frequency,
        # i.e. a reference frequency will always have a constant divider which can be verified as per bspec.
        verify = verify and _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_CTL",
                                                                         parameter=["CD2X Divider Select",
                                                                                    "CD2X Pipe Select"],
                                                                         expected=[expected_cd2x_divider_str,
                                                                                   cd2x_pipe_select_str],
                                                                         actual=[cd2x_divider_select_str,
                                                                                 cd2x_pipe_select_str])

        verify = verify and _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_PLL_ENABLE",
                                                                         parameter=["PLL Enable", "PLL Lock",
                                                                                    "PLL Ratio",
                                                                                    "freq_change_req"],
                                                                         expected=[expected_pll_enable_str,
                                                                                   expected_pll_lock_str,
                                                                                   expected_pll_ratio,
                                                                                   expected_freq_change_request_str],
                                                                         actual=[pll_enable_str, pll_lock_str,
                                                                                 pll_ratio,
                                                                                 freq_change_request_str])

        return verify

    ##
    # @brief        Function for verifying Phy Test Mode
    # @param[in]    port_name - Port to verify
    # @param[in]    gfx_index - Adapter to verify
    # @return       bool - Returns True if verification is successful, False otherwise
    @staticmethod
    def verify_phy_test_mode(port_name: str, gfx_index: str) -> bool:
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
                if str(port_name).upper().__contains__('HDMI'):
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

                        # due to rounding-off issue, there might be a precision mismatch
                        # FRL rate returns GBPS data. Convert to KHz and divide / 18, get ceil of this value
                        rounded_pixel_rate = math.ceil(frl_rate_in_gbps * (10 ** 6) / 18)  # in KHz
                        # There is a precision mismatch due to which below rounding off is done.
                        # E.g. Expected value = 92.8125 and actual value = 92.813, so will only compare till 2 digits
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
                            # for Yuv420, pixel clock is 0.5 of pixel clock we get from
                            # edid as defined in appendix J of HDMI spec.
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
                        # E.g. Expected value = 92.8125 and actual value = 92.813, so will only compare till 2 digits
                        rounded_pixel_rate = round(rounded_pixel_rate, 2)

                elif str(port_name).upper().__contains__('DP'):
                    link_rate = dpcd_helper.DPCD_getLinkRate(
                        enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo)
                    # Control link symbols and data link symbols are of size 32 bits in case of 128b/132b encoding.
                    link_symbol_clock = round(link_rate * 1000 / 32, 2) if link_rate >= 10 else round(link_rate * 100,
                                                                                                      2)

        valfreq_offset = 0
        if str(port_name).upper().__contains__('_A'):
            valfreq_offset = Gen14DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_A
        elif str(port_name).upper().__contains__('_B'):
            valfreq_offset = Gen14DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_B
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
        # E.g. Expected value = 92.8125 and actual value = 92.813, so will only compare till 2 digits
        pixel_rate_mhz = round((valfreq / 1000), 2)

        verify &= _clock_helper.verify_port_clock_programming_ex(feature="PHY TEST MODE",
                                                                 parameter="Phy Test Mode Val Frequency in MHz",
                                                                 expected=[rounded_pixel_rate] if str(
                                                                     port_name).upper().__contains__(
                                                                     'HDMI') else [link_symbol_clock],
                                                                 actual=[pixel_rate_mhz])

        return verify

    ##
    # @brief        This function gets the lane count allotted by IOM to display controller on a TC PHY.
    # @details      Note: Even if display is using 2 lanes only, if IOM allots 4 lanes for display, then we get 4 lanes.
    # @param[in]    port_name - Port name like DP_F, HDMI_B, etc.
    # @param[in]    gfx_index - Adapter index like 'gfx_0'
    # @return       lane_count - the lane count in integer value.
    @staticmethod
    def mtl_snps_c20_get_lane_count_given_by_iom(port_name: str, gfx_index: str) -> int:
        lane_count = 0
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
            logging.error(f'Wrong port passed. {port_name} not supported by MTL C20 PHY')
            return lane_count
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
            return lane_count

        return lane_count

    ##
    # @brief        verification logic for port slice block (PICA registers) for MTL.
    # @param[in]    port_name - port name like DP_F, HDMI_B, etc.
    # @param[in]    gfx_index - adapter index like 'gfx_0'
    # @return       ret - returns True if all verification passed, False otherwise
    @staticmethod
    def verify_port_slice(port_name: str, gfx_index: str) -> bool:
        from Tests.ModeEnumAndSet.display_mode_enumeration_base import ModeEnumAndSetBase
        ret = True
        _clock_helper = clock_helper.ClockHelper()
        mtl_clock_helper_ = mtl_clock_helper.MtlClockHelper()
        hf_vsdb_parser = HdmiForumVendorSpecificDataBlock()
        hf_vsdb_parser.parse_hdmi_forum_vendor_specific_data_block(gfx_index, port_name)
        is_port_dp = True if 'DP' in port_name else False
        is_hdmi_2_1_frl = _clock_helper.is_hdmi_2_1(port_name, gfx_index)
        is_dp_2_0 = _clock_helper.is_dp_2_0(port_name, gfx_index)
        ddi_clock_select_expected = 'div18clk' if is_hdmi_2_1_frl else 'Maxpclk'
        target_id = _clock_helper.get_target_id(port_name, gfx_index)
        current_link_rate = dpcd_helper.DPCD_getLinkRate(target_id) if is_port_dp else None
        number_of_lanes = dpcd_helper.DPCD_getNumOfLanes(target_id) if is_port_dp else None

        if is_hdmi_2_1_frl:
            frl_rate_in_vbt = ModeEnumAndSetBase.get_hdmi_2_1_frl_rate_in_vbt(port_name)
            number_of_lanes = 3 if (frl_rate_in_vbt == 3) else hf_vsdb_parser.max_frl_rate[1]
        gfx_vbt = vbt.Vbt(gfx_index)
        vbt_panel_index = gfx_vbt.get_panel_index_for_port(port_name)
        expected_port_reversal = 1 if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[
                                          vbt_panel_index].Flags1 & 0b10 else 0
        get_ddi = display_base.DisplayBase(port_name, 'MTL', gfx_index)
        pipe_ddi = get_ddi.GetPipeDDIAttachedToPort(port_name, gfx_index=gfx_index)
        pipe = (pipe_ddi[0])[-1]
        offset = eval('Gen14TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_' + pipe)
        value = DisplayArgs.read_register(offset, gfx_index)
        trans_hdmi_port_width = Gen14TranscoderRegs.REG_TRANS_DDI_FUNC_CTL(offset, value)
        transcoder_port_width_value = trans_hdmi_port_width.PortWidthSelection

        # map based on values of 'DDI Clock Select' of register PORT_CLOCK_CTL in bspec:
        # https://gfxspecs.intel.com/Predator/Home/Index/65103?dstFilter=MTL&mode=Filter
        ddi_clk_select_map = {
            0b1000: 'Maxpclk',
            0b1001: 'div18clk',
            0b1100: 'TBT 162',
            0b1101: 'TBT 270',
            0b1110: 'TBT 540',
            0b1111: 'TBT 810'
        }
        # map based on values of 'Port Width' of register PORT_BUF_CTL1 in bspec:
        # https://gfxspecs.intel.com/Predator/Home/Index/65091?dstFilter=MTL&mode=Filter
        port_width_lanes_map = {
            0b000: 1,
            0b001: 2,
            0b011: 4,
            0b100: 3
        }

        ddi_name = str(port_name).split('_')[1]
        bspec_port_name = mtl_clock_helper_.ddi_to_bspec_name_map[ddi_name.upper()]
        # determine which msgbus PHY lanes are owned by display controller
        if bspec_port_name.__contains__('USBC'):
            no_of_lanes_given_by_iom = MtlClock.mtl_snps_c20_get_lane_count_given_by_iom(port_name, gfx_index)
            logging.info(f'For {port_name}, IOM has given {no_of_lanes_given_by_iom} lanes to display controller.')
            if no_of_lanes_given_by_iom == 4:
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
        port_width_transcoder_map = {
            0b000: 1,
            0b001: 2,
            0b010: 3,
            0b011: 4
        }

        # verify PORT_BUF_CTL1 register
        if _clock_helper.get_port_type_for_port(port_name).__contains__('TBT'):
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                                  parameter="IO Select",
                                                                  expected=[1], actual=[port_buf_ctl1.IoSelect])
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                              parameter="D2D Link Enable",
                                                              expected=[1], actual=[port_buf_ctl1.D2DLinkEnable])
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                              parameter="Data Width",
                                                              expected=[
                                                                  1 if is_hdmi_2_1_frl else 2 if is_dp_2_0 else 0],
                                                              actual=[port_buf_ctl1.DataWidth])

        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                              parameter="Port Reversal",
                                                              expected=[expected_port_reversal],
                                                              actual=[port_buf_ctl1.PortReversal])
        if is_port_dp:
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                                  parameter="Port Width",
                                                                  expected=[number_of_lanes],
                                                                  actual=[
                                                                      port_width_lanes_map[port_buf_ctl1.PortWidth]])
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                              parameter="HDMI FRL Shifter Enable",
                                                              expected=[1 if is_hdmi_2_1_frl else 0],
                                                              actual=[port_buf_ctl1.HdmiFrlShifterEnable])
        if is_hdmi_2_1_frl:
            if port_width_lanes_map[port_buf_ctl1.PortWidth] == port_width_transcoder_map[transcoder_port_width_value]:
                ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                                      parameter="Port Width",
                                                                      expected=[number_of_lanes],
                                                                      actual=[port_width_lanes_map[
                                                                                  port_buf_ctl1.PortWidth]])
            else:
                ret = False
                logging.error("Port Width Verification Failed. "
                              "PORT_BUF_CTL register and Transcoder Port Width values did not match")

        # Programming specific to TBT case
        if _clock_helper.get_port_type_for_port(port_name).__contains__('TBT'):
            # verify PORT_CLOCK_CTL register
            if is_port_dp:
                if port_clock_ctl.DdiClockSelect in ddi_clk_select_map.keys():
                    ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                                          parameter="DDI Clock Select",
                                                                          expected=[
                                                                              'TBT ' + str(
                                                                                  int(current_link_rate * 100))],
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
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                                  parameter="TBT Clock Request",
                                                                  expected=[1],
                                                                  actual=[port_clock_ctl.TbtClockRequest])

        # Programming specific to non-TBT case
        else:
            # verify PORT_BUF_CTL2 register
            # Clear PORT_BUF_CTL2<port> Lane<PHY Lanes Owned*> Pipe Reset to 0.
            # Due to FIA HW bug in MFD DP case on C20 PHY, driver has to do both lanes pipe reset as WA even though
            # it owns only lane_0 (bugeco HSD: 14017178556)
            # (part of "Bring owned* PHY lanes out of Reset.")
            # This bug is getting fixed in IOE B step.
            # So Gfx driver has to apply this WA only for IOE A step.
            ioe_stepping = MtlClock.get_ioe_stepping_info(gfx_index, port_name)
            lanes_to_program_pipe_reset = ['0', '1'] if 'USBC' in bspec_port_name and (
                    ioe_stepping == Gen14DdiRegs.ENUM_IOE_STEPPING.IOE_STEPPING_A_STEP) else msgbus_phy_lanes_owned
            for lane in lanes_to_program_pipe_reset:
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
                                                                      actual=[
                                                                          ddi_clk_select_map[
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

                # SSC Enable PLL A = 1 for UHBR10 and UHBR20 (always uses PLL A and SSC), else 0
                # But as HW response is buggy today, DP 2.1 SSC will be enabled based on VBT & DPCD support.
                expected_ssc_on_pll_a = 0
                if current_link_rate in [10.0, 20.0] and is_ssc_enabled:
                    expected_ssc_on_pll_a = 1
                ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_CLOCK_CTL_" + bspec_port_name,
                                                                      parameter="SSC Enable PLL A",
                                                                      expected=[expected_ssc_on_pll_a],
                                                                      actual=[port_clock_ctl.SscEnablePllA])
                # SSC Enable PLL B = 1 always if link rate is UHBR13.5
                if current_link_rate == 13.5:
                    expected_ssc_on_pll_b = 1
                # SSC Enable PLL B = 1 if SSC is needed with DP 1.4 or eDP, else 0
                elif current_link_rate not in [10.0, 20.0] and is_ssc_enabled:
                    expected_ssc_on_pll_b = 1
                else:
                    expected_ssc_on_pll_b = 0
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
    # @brief        Function to get Max CD Clock
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       float - Max System CD Clock
    def get_system_max_cd_clk(self, gfx_index: str) -> float:
        _clock_helper = clock_helper.ClockHelper()
        offset = NonAutoGenRegs.OFFSET_SWF06.SW06
        value = DisplayArgs.read_register(offset, gfx_index)
        swf06 = NonAutoGenRegs.REG_SWF06(offset, value)
        max_value = swf06.MaxCdClockSupported
        logging.debug(f"Max CD clock frequency decimal supported from SW06 register: {max_value} MHz")
        _clock_helper = clock_helper.ClockHelper()

        reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)
        logging.debug(f"Reference clock = {reference_clock} MHz")

        if max_value == 0 and reference_clock == DEFAULT_REFERENCE_CLOCK_FREQUENCY:
            max_cd_clock = max(self.cdclock_ctl_freq_dict.keys())
        else:
            max_cd_clock = list(self.cdclock_ctl_freq_dict)[list(self.cdclock_ctl_freq_dict.values()).index(max_value)]

        if max_cd_clock == 0:
            logging.error(f"Failed to fetch max CD clock with max value ({max_value}) from SWF06 register")
            gdhm.report_test_bug_pc(
                "[Interfaces][Display_Engine][MTL] Failed to fetch max CD clock with max value from SWF06 register")

        return max_cd_clock

    ##
    # @brief        Function for calculating optimal cd clock with given pixel_rate
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @param[in]    max_pixel_rate: float
    #                   Maximum pixel rate
    # @param[in]    display_list: list
    #                   Display list
    # @return       optimal_cdclock: float
    #                   returns the optimal cd clock in MHz
    @classmethod
    def get_optimal_cd_clock_from_pixelclock(cls, gfx_index: str, max_pixel_rate: float,
                                             display_list: List[str]) -> float:
        optimal_cdclock: float = 0
        _clock_helper = clock_helper.ClockHelper()

        reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)

        max_dsc_slice_one_pixel_clock = _clock_helper.get_max_dsc_slice_1_pixel_clock(gfx_index, display_list)

        # For DSC Displays with Slice Count of 1, Optimal Cd Clock using 2ppc method will not be sufficient to drive the
        # Display as only one DSC Engine will be active and this DSC Engine Clock will be synchronized with the CD Clock
        # not CD Clock x 2. Hence, For DSC Displays with Slice Count 1 optimal cd clock will be determined with 1ppc
        # method. For this purpose, pixel clock of dsc display will be multiplied by 2 and the resultant max pixel rate
        # will be used to determine optimal cd clock
        supported_pixel_rate = max(max_pixel_rate, max_dsc_slice_one_pixel_clock * 2)

        # Cd Clock values for 38.4 Mhz Reference Frequency
        if reference_clock == DEFAULT_REFERENCE_CLOCK_FREQUENCY:
            optimal_cdclock = 172.8 if supported_pixel_rate < 345.6 \
                else 192 if supported_pixel_rate < 384 \
                else 307.2 if supported_pixel_rate < 614.4 \
                else 480 if supported_pixel_rate < 958 \
                else 556.8 if supported_pixel_rate < 1113.6 else 652.8

        logging.info("Optimal Cd clock: {}MHz".format(optimal_cdclock))
        return optimal_cdclock

    ##
    # @brief        Function for calculating optimal cd clock
    # @param[in]    display_list: list
    #                   Display list
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @return       optimal_cdclock: float
    #                   returns the optimal cd clock in MHz
    def get_optimal_cdclock(self, gfx_index: str, display_list: List[str]) -> float:
        _clock_helper = clock_helper.ClockHelper()

        # Check if the mode is pipe ganged modeset and get the number of pipes required to drive the mode.
        is_pipe_joiner_required, no_of_pipe_required, pipe_joiner_ports = False, 1, {}
        effective_cd_clock_hz = clock_helper.GEN14PLUS_EFFECTIVE_CD_CLOCK_MHZ * 1000000
        for port_name in display_list:
            logging.info(f"Port name: {port_name}")
            is_pipe_joiner_required, no_of_pipe_required = _clock_helper.is_pipe_joiner_required(gfx_index, port_name,
                                                                                                 effective_cd_clock_hz)
            if is_pipe_joiner_required is True:
                pipe_joiner_ports[port_name] = {'gfx_index': gfx_index, 'no_of_pipe_required': no_of_pipe_required}

        supported_pixel_rate, target_id = _clock_helper.get_max_pixel_rate(display_list, gfx_index, True,
                                                                           pipe_joiner_ports)

        optimal_cdclock = self.get_optimal_cd_clock_from_pixelclock(gfx_index, supported_pixel_rate, display_list)
        return optimal_cdclock

    ##
    # @brief       Mtl Snps C20 Phy function to Get IOE stepping info
    # @param[in]   port: str
    # @param[in]   gfx_index: str
    # @return      IoeStepping
    @staticmethod
    def get_ioe_stepping_info(gfx_index: str, port: str) -> Gen14DdiRegs.ENUM_IOE_STEPPING:
        # TC1 and TC2
        if "F" in port or "G" in port:
            port_tx_dflex_dpsp_addr = Gen14DdiRegs.OFFSET_PORT_TX_DFLEXDPSP.PORT_TX_DFLEXDPSP_FIA1
        # TC3 and TC4
        else:
            port_tx_dflex_dpsp_addr = Gen14DdiRegs.OFFSET_PORT_TX_DFLEXDPSP.PORT_TX_DFLEXDPSP_FIA2
        value = DisplayArgs.read_register(port_tx_dflex_dpsp_addr, gfx_index)
        port_tx_dflex_dpsp = Gen14DdiRegs.REG_PORT_TX_DFLEXDPSP(port_tx_dflex_dpsp_addr, value)

        return port_tx_dflex_dpsp.IoeStepping

    ##
    # @brief        Verifies PCode notified Voltage Level as part of CD clock programming
    # @param[in]    gfx_index: Graphics Adapter Index
    # @param[in]    ports: List of port names of active displays
    # @return       bool - True if verification is successful, False otherwise
    def verify_voltage_level_notified_to_pcode(self, gfx_index: str, ports: List[str]) -> bool:
        _clock_helper = clock_helper.ClockHelper()
        _display_config = display_config.DisplayConfiguration()
        _mtl_clock_helper = mtl_clock_helper.MtlClockHelper()

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
            gdhm.report_test_bug_pc("Skipping DVFS verification for scaled modes across panels!!",
                                    priority=gdhm.Priority.P4, exposure=gdhm.Exposure.E3)
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

        max_ddi_freq_target, max_ddi_freq = _mtl_clock_helper.get_max_ddi_symbol_clock_frequency(gfx_index, ports)
        logging.info(f"Target {max_ddi_freq_target} with max DDI freq = {max_ddi_freq}")

        # Ref: DVFS programming expectation - https://gfxspecs.intel.com/Predator/Home/Index/65565
        if expected_cdclock <= 307.2 and max_ddi_freq <= 594:
            expected_voltage_level_index = Gen14Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_0.value
            if actual_voltage_level_index != expected_voltage_level_index:
                # logging.warning("Assigning next VoltageLevel since it should not have any power functionality issue")
                # expected_voltage_level_index = actual_voltage_level_index
                gdhm.report_test_bug_pc("[Interfaces][Display_Engine][CD Clock][WARNING] Lower VoltageLevel calculated",
                                        priority=gdhm.Priority.P3, exposure=gdhm.Exposure.E3)
        elif expected_cdclock <= 480:
            expected_voltage_level_index = Gen14Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_1.value
        elif expected_cdclock <= 556.8:
            expected_voltage_level_index = Gen14Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_2.value
        else:
            # Max CD Clock frequency requires Voltage Level 3 to be programmed
            expected_voltage_level_index = Gen14Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_3.value
        logging.info(f"Expected VoltageLevel = {expected_voltage_level_index}")
        return _clock_helper.verify_cd_clock_programming_ex(feature="INITIATE_PM_DMD_REQ",
                                                            parameter=["VoltageLevelIndex"],
                                                            expected=[expected_voltage_level_index],
                                                            actual=[actual_voltage_level_index])
