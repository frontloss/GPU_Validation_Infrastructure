##
# @file     lnl_clock_base.py
# @brief    LNL clock validation base class
# @details  Defines methods to handle CD clock and port clock verification
# @author   Kiran Kumar Lakshmanan, Gouthamn

import logging
import math
from typing import Dict, List

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen15 import Gen15Regs
from DisplayRegs.Gen15.Ddi import Gen15DdiRegs
from DisplayRegs.Gen15.Pll import Gen15PllRegs
from DisplayRegs.Gen15.Transcoder import Gen15TranscoderRegs
from Libs.Core import system_utility, enum
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.logger import gdhm
from Libs.Core.vbt import vbt
from Libs.Core.wrapper.driver_escape_args import IGCCSupportedEncoding, IGCCSupportedBpc
from Libs.Feature.clock import clock_helper
from Libs.Feature.clock.clock_helper import CdClockMap, DEFAULT_REFERENCE_CLOCK_FREQUENCY, VoltageFrequencyLevel, \
    MBusType
from Libs.Feature.clock.lnl import lnl_clock_dp_snps_phy
from Libs.Feature.clock.lnl import lnl_clock_hdmi_snps_phy
from Libs.Feature.clock.lnl import lnl_clock_helper
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_port import dpcd_helper
from Libs.Feature.hdmi import hf_vsdb_block


##
# @brief        Base class for LNL Clock Verification
# @details      CD clock and port clock verification methods are defined under this class
class LnlClock:
    # Registers used for verification - CD Clock Programming
    # CDCLK_CTL: https://gfxspecs.intel.com/Predator/Home/Index/69090
    # CDCLK_PLL_ENABLE: https://gfxspecs.intel.com/Predator/Home/Index/69091
    # CDCLK_SQUASH_CTL: https://gfxspecs.intel.com/Predator/Home/Index/69092
    # DDI_CLK_VALFREQ: https://gfxspecs.intel.com/Predator/Home/Index/69180
    # DSSM: https://gfxspecs.intel.com/Predator/Home/Index/69476

    # CD Clock frequency to BSpec value mapping dict
    # Only to be used to fetch System Max CD clock value from SWF06 register
    cdclock_register_freq_dict = dict([
        (344, 172.8),
        (382, 192),
        (612, 307.2),
        (958, 480),
        (1112, 556.8),
        (1304, 652.8)
    ])

    # This dictionary contains mapping values for each requirement for identifying CD clock frequency being programmed
    cdclk_ctl_dict: Dict[float, Dict[float, CdClockMap]] = {
        # Currently only possible ref clk is 38.4 MHz, supported on SoC. The frequency is selected by the SoC.
        DEFAULT_REFERENCE_CLOCK_FREQUENCY: {
            # VoltageLevel VF0
            153.6: CdClockMap(153.6, 16, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              614.4, 0xAAAA, VoltageFrequencyLevel.VF0),
            172.8: CdClockMap(172.8, 16, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              614.4, 0xAD5A, VoltageFrequencyLevel.VF0),
            192: CdClockMap(192, 16, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            614.4, 0xB6B6, VoltageFrequencyLevel.VF0),
            211.2: CdClockMap(211.2, 16, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              614.4, 0xDBB6, VoltageFrequencyLevel.VF0),
            230.4: CdClockMap(230.4, 16, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              614.4, 0xEEEE, VoltageFrequencyLevel.VF0),
            249.6: CdClockMap(249.6, 16, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              614.4, 0xF7DE, VoltageFrequencyLevel.VF0),
            268.8: CdClockMap(268.8, 16, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              614.4, 0xFEFE, VoltageFrequencyLevel.VF0),
            288: CdClockMap(288, 16, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            614.4, 0xFFFE, VoltageFrequencyLevel.VF0),
            307.2: CdClockMap(307.2, 16, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              614.4, 0xFFFF, VoltageFrequencyLevel.VF0),

            # VoltageLevel VF1
            330: CdClockMap(330, 25, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            960, 0xDBB6, VoltageFrequencyLevel.VF1),
            360: CdClockMap(360, 25, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            960, 0xEEEE, VoltageFrequencyLevel.VF1),
            390: CdClockMap(390, 25, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            960, 0xF7DE, VoltageFrequencyLevel.VF1),
            420: CdClockMap(420, 25, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            960, 0xFEFE, VoltageFrequencyLevel.VF1),
            450: CdClockMap(450, 25, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            960, 0xFFFE, VoltageFrequencyLevel.VF1),
            480: CdClockMap(480, 25, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            960, 0xFFFF, VoltageFrequencyLevel.VF1),

            # VoltageLevel VF2
            487.2: CdClockMap(487.2, 29, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1113.6, 0xFEFE, VoltageFrequencyLevel.VF2),
            522: CdClockMap(522, 29, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            1113.6, 0xFFFE, VoltageFrequencyLevel.VF2),
            556.8: CdClockMap(556.8, 29, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1113.6, 0xFFFF, VoltageFrequencyLevel.VF2),

            # VoltageLevel VF3
            571.2: CdClockMap(571.2, 34, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1305.6, 0xFEFE, VoltageFrequencyLevel.VF3),
            612: CdClockMap(612, 34, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            1305.6, 0xFFFE, VoltageFrequencyLevel.VF3),
            652.8: CdClockMap(652.8, 34, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1305.6, 0xFFFF, VoltageFrequencyLevel.VF3),
        }
    }

    # Todo: Refactor below dictionaries as part of port clock verification content change. Tracked in VSDI-28881
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

    ##
    # @brief        Verification method to check for port clock programming in LNL
    # @param[in]    gfx_index - Graphics adapter to verify
    # @param[in]    port_name - Connector port to verify
    # @return       bool - Returns True if port clock verification is successful, False otherwise
    @staticmethod
    def verify_clock(gfx_index: str, port_name: str) -> bool:
        system_utility_ = system_utility.SystemUtility()
        _clock_helper = clock_helper.ClockHelper()
        target_id = _clock_helper.get_target_id(port_name, gfx_index)
        logging.info(f"******* Clock and PLL Verification of Port : {port_name} (Target ID : 0x{target_id:X}) *******")

        verify = True

        # PHY and PLL verification. As Snps Phy is not modeled in pre-si, this verification enabled only for post-si
        execution_environment_type = system_utility_.get_execution_environment_type()
        if execution_environment_type is not None and execution_environment_type == "POST_SI_ENV":
            verify = verify and LnlClock.verify_phy_test_mode(port_name, gfx_index)

            # PICA or port slice verification. Common for DP and HDMI for all ports (A, B, TC1, TC2, TC3, TC4)
            verify = verify and LnlClock.verify_port_slice(port_name, gfx_index)
            clock = None
            if 'HDMI' in str(port_name).upper():
                clock = lnl_clock_hdmi_snps_phy.LnlClockHdmiSnpsPhy()
            elif 'DP' in str(port_name).upper():  # Common for eDP and DP
                clock = lnl_clock_dp_snps_phy.LnlClockDpSnpsPhy()

            if clock is None:
                logging.error("Clock object is none!")
                gdhm.report_test_bug_di(
                    "[Interfaces][Display_Engine][LNL] Invalid clock object used to perform port clock verification")
                return False

            verify = verify and clock.verify_clock(port_name, gfx_index)

        return verify

    ##
    # @brief        Generic function for getting current cd clock
    # @param[in]    gfx_index: str - Graphics index of Graphics adapter
    # @return       current cd clock
    def get_current_cd_clock(self, gfx_index: str):
        # Get Reference Frequency
        _clock_helper = clock_helper.ClockHelper()
        reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)
        logging.info(f"Programmed Reference clock = {reference_clock} MHz")

        # Only supported reference clock is 38.4 MHz
        if reference_clock not in self.cdclk_ctl_dict.keys() or reference_clock != DEFAULT_REFERENCE_CLOCK_FREQUENCY:
            logging.error(f"Invalid Reference clock programmed. Expected: 38.4 MHz, Actual: {reference_clock} MHz")
            return False
        logging.info(f"Programmed Reference clock = {reference_clock} MHz")

        # CDCLK_PLL_ENABLE register
        cdclk_pll_enable_offset = Gen15PllRegs.OFFSET_CDCLK_PLL_ENABLE.CDCLK_PLL_ENABLE
        cdclk_pll_enable_value = DisplayArgs.read_register(cdclk_pll_enable_offset, gfx_index)
        cdclk_pll_enable_reg_value = Gen15PllRegs.REG_CDCLK_PLL_ENABLE(cdclk_pll_enable_offset, cdclk_pll_enable_value)
        pll_ratio = cdclk_pll_enable_reg_value.PllRatio
        logging.debug(f"Programmed PllRatio = {pll_ratio}")

        # CDCLK_SQUASH_CTL register
        squash_ctl_offset = Gen15PllRegs.OFFSET_CDCLK_SQUASH_CTL.CDCLK_SQUASH_CTL
        squash_ctl_value = DisplayArgs.read_register(squash_ctl_offset, gfx_index)
        squash_ctl_reg_value = Gen15PllRegs.REG_CDCLK_SQUASH_CTL(squash_ctl_offset, squash_ctl_value)
        squash_waveform = squash_ctl_reg_value.SquashWaveform
        logging.debug(f"Programmed SquashWaveform = {squash_waveform}")

        supported_cdclock_ctl_freq: Dict[float, CdClockMap] = {cdclock_freq: current_cdclk_map for
                                                               cdclock_freq, current_cdclk_map in
                                                               self.cdclk_ctl_dict[reference_clock].items() if
                                                               current_cdclk_map.pll_ratio == pll_ratio and
                                                               current_cdclk_map.squash_wave == squash_waveform}

        # First key of supported_cdclock_ctl_freq will be the current CD clock.
        current_cdclk = list(supported_cdclock_ctl_freq.keys())[0]
        logging.debug(f"Current CD clock = {current_cdclk}")
        return current_cdclk

    ##
    # @brief        Verification method to check for CD clock programming in LNL
    # @param[in]    gfx_index - Graphics adapter to verify
    # @param[in]    display_list - active port list for adapter in gfx_index param
    # @return       bool - Returns True if CD clock verification is successful, False otherwise
    def verify_cdclock(self, gfx_index: str, display_list: List[str]) -> bool:
        verify = True
        _clock_helper = clock_helper.ClockHelper()

        # Get Reference Frequency
        reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)
        logging.info(f"Programmed Reference clock = {reference_clock} MHz")

        # Only supported reference clock is 38.4 MHz
        if reference_clock not in self.cdclk_ctl_dict.keys() or reference_clock != DEFAULT_REFERENCE_CLOCK_FREQUENCY:
            logging.error(f"Invalid Reference clock programmed. Expected: 38.4 MHz, Actual: {reference_clock} MHz")
            gdhm.report_bug(
                title=f"[Interfaces][Display_Engine] Invalid reference clock frequency programmed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False
        logging.info(f"Programmed Reference clock = {reference_clock} MHz")

        # Read CDCLK_CTL register
        cdclk_ctl_offset = Gen15PllRegs.OFFSET_CDCLK_CTL.CDCLK_CTL
        cdclk_ctl_value = DisplayArgs.read_register(cdclk_ctl_offset, gfx_index)
        cdclk_ctl_reg_value = Gen15PllRegs.REG_CDCLK_CTL(cdclk_ctl_offset, cdclk_ctl_value)
        cd2x_divider_select = cdclk_ctl_reg_value.Cd2XDividerSelect
        cd2x_pipe_select = cdclk_ctl_reg_value.Cd2XPipeSelect
        mdclk_src_select = cdclk_ctl_reg_value.MdclkSourceSelect
        logging.debug(f"Programmed [CD2XDividerSelect, Cd2XPipeSelect, MdclkSourceSelect] = [{cd2x_divider_select}, "
                      f"{cd2x_pipe_select}, {mdclk_src_select}]")

        # CDCLK_PLL_ENABLE register
        cdclk_pll_enable_offset = Gen15PllRegs.OFFSET_CDCLK_PLL_ENABLE.CDCLK_PLL_ENABLE
        cdclk_pll_enable_value = DisplayArgs.read_register(cdclk_pll_enable_offset, gfx_index)
        cdclk_pll_enable_reg_value = Gen15PllRegs.REG_CDCLK_PLL_ENABLE(cdclk_pll_enable_offset, cdclk_pll_enable_value)
        pll_enable = cdclk_pll_enable_reg_value.PllEnable
        pll_lock = cdclk_pll_enable_reg_value.PllLock
        pll_ratio = cdclk_pll_enable_reg_value.PllRatio
        freq_change_request = cdclk_pll_enable_reg_value.FreqChangeReq
        logging.debug(f"Programmed [PllEnable, PllLock, PllRatio, FreqChangeReq] = [{pll_enable}, {pll_lock}, "
                      f"{pll_ratio} {freq_change_request}]")

        # CDCLK_SQUASH_CTL register
        squash_ctl_offset = Gen15PllRegs.OFFSET_CDCLK_SQUASH_CTL.CDCLK_SQUASH_CTL
        squash_ctl_value = DisplayArgs.read_register(squash_ctl_offset, gfx_index)
        squash_ctl_reg_value = Gen15PllRegs.REG_CDCLK_SQUASH_CTL(squash_ctl_offset, squash_ctl_value)
        squash_enable = squash_ctl_reg_value.SquashEnable
        squash_window_size = squash_ctl_reg_value.SquashWindowSize
        squash_waveform = squash_ctl_reg_value.SquashWaveform
        logging.debug(f"Programmed [SquashEnable, SquashWaveform, SquashWindowSize] = [{squash_enable}, "
                      f"{squash_waveform}, {squash_window_size}]")

        # Fetch programmed CD clock frequency value based on PLL Ratio and Squash Waveform
        supported_cdclock_ctl_freq: Dict[float, CdClockMap] = {cdclock_freq: current_cdclk_map for
                                                               cdclock_freq, current_cdclk_map in
                                                               self.cdclk_ctl_dict[reference_clock].items() if
                                                               current_cdclk_map.pll_ratio == pll_ratio and
                                                               current_cdclk_map.squash_wave == squash_waveform}

        # If no such CD clock frequency is available for given PLL ratio and reference frequency, exit verification
        if bool(supported_cdclock_ctl_freq) is False:
            logging.error(f"No possible CdClockMap data available for PLL ratio: {pll_ratio}")
            gdhm.report_bug(
                title="[Interfaces][Display_Engine] CD clock mapping unavailable for PLL ratio and Squash Waveform",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            return False

        cdclock_ctl_freq = supported_cdclock_ctl_freq[min(list(supported_cdclock_ctl_freq.keys()))]

        programmed_cdclock_freq = cdclock_ctl_freq.cdclk_freq
        programmed_pll_ratio = cdclock_ctl_freq.pll_ratio
        programmed_pll_output = cdclock_ctl_freq.pll_output
        programmed_cd2x_divider = cdclock_ctl_freq.cd2x_divider
        programmed_squash_wave = cdclock_ctl_freq.squash_wave
        programmed_vf_level = cdclock_ctl_freq.vf_level
        logging.info(f"Programmed values = {cdclock_ctl_freq}; "
                     f"Programmed VF Level = {VoltageFrequencyLevel(programmed_vf_level).name}")

        # if dynamic cd clk is not enabled, return without verification
        if not _clock_helper.is_dynamic_cdclock_enabled():
            logging.info(f"INFO : Dynamic CD Clock NOT Enabled. Current CD CLOCK : {programmed_cdclock_freq} MHz")
            return True

        optimal_cd_clock = self.get_optimal_cdclock(gfx_index, display_list)

        platform = clock_helper.ClockHelper.get_platform_name(gfx_index)
        if platform == "LNL":
            system_max_cd_clk = clock_helper.GEN14PLUS_MAX_CD_CLOCK_MHZ
        else:
            # Higher CD clock supported on PTL
            system_max_cd_clk = clock_helper.PTL_MAX_CD_CLOCK_MHZ
        logging.info(f"System max CD clock: {system_max_cd_clk} MHz")

        expected_cdclock = optimal_cd_clock
        logging.info(f"Expected CD clock: {expected_cdclock} MHz")

        # String computation for verification purpose
        expected_cd2x_divider_str = Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT(programmed_cd2x_divider).name
        # Todo: Pipe select not yet programmed by driver
        # expected_cd2x_pipe_select_str = Gen15PllRegs.ENUM_CD2X_PIPE_SELECT.CD2X_PIPE_SELECT_NONE.name
        expected_pll_enable_str = Gen15PllRegs.ENUM_PLL_ENABLE.PLL_ENABLE.name
        expected_pll_lock_str = Gen15PllRegs.ENUM_PLL_LOCK.PLL_LOCK_LOCKED.name
        expected_freq_change_request_str = Gen15PllRegs.ENUM_FREQ_CHANGE_ACK. \
            FREQ_CHANGE_ACK_NO_PENDING_REQUEST_OR_REQUEST_NOT_FINISHED.name
        expected_mdclk_src_select = Gen15PllRegs.ENUM_MDCLK_SOURCE_SELECT.MDCLK_SOURCE_SELECT_CDCLK_PLL.value

        cd2x_divider_select_str = Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT(cd2x_divider_select).name
        cd2x_pipe_select_str = Gen15PllRegs.ENUM_CD2X_PIPE_SELECT(cd2x_pipe_select).name \
            if any(cd2x_pipe_select == x.value for x in Gen15PllRegs.ENUM_CD2X_PIPE_SELECT.__members__.values()) \
            else f"PIPE_INVALID_{cd2x_pipe_select}"
        pll_enable_str = Gen15PllRegs.ENUM_PLL_ENABLE(pll_enable).name
        pll_lock_str = Gen15PllRegs.ENUM_PLL_LOCK(pll_lock).name
        freq_change_request_str = Gen15PllRegs.ENUM_FREQ_CHANGE_ACK(freq_change_request).name

        # We can't program cd clk greater than system max cd clk
        if expected_cdclock > system_max_cd_clk:
            logging.error(f"Expected CD clock exceeding system max CD clock")
            expected_cdclock = system_max_cd_clk
            gdhm.report_bug(
                title=f"[Interfaces][Display_Engine] Expected CD clock exceeding system max CD clock",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        # Todo: Remove GDHM logging and add verification for CD clock frequency verification.
        # Note: Keeping GDHM WA to catch driver enum based programming issue and track the same
        dict_keys = list(self.cdclk_ctl_dict[reference_clock])
        expected_cdclock_index = dict_keys.index(expected_cdclock)

        # Verify CD clock frequency programming
        verify &= _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_CTL", parameter="Dynamic CD Clock in MHz",
                                                               expected=[expected_cdclock],
                                                               actual=[programmed_cdclock_freq])

        verify &= _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_CTL",
                                                               parameter=["CD2X Div Select", "CD2X Pipe Select",
                                                                          "MDCLK Source Select"],
                                                               expected=[expected_cd2x_divider_str,
                                                                         cd2x_pipe_select_str,
                                                                         expected_mdclk_src_select],
                                                               actual=[cd2x_divider_select_str, cd2x_pipe_select_str,
                                                                       mdclk_src_select])

        # Verify CD clock PLL programming
        verify &= _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_PLL_ENABLE",
                                                               parameter=["PLL Enable", "PLL Lock", "PLL Ratio",
                                                                          "Frequency Change Request"],
                                                               expected=[expected_pll_enable_str, expected_pll_lock_str,
                                                                         programmed_pll_ratio,
                                                                         expected_freq_change_request_str],
                                                               actual=[pll_enable_str, pll_lock_str, pll_ratio,
                                                                       freq_change_request_str])

        # Verify CD clock squash register programming
        if squash_enable == 1:
            verify &= _clock_helper.verify_cd_clock_programming_ex(feature="CDCLK_SQUASH_CTL",
                                                                   parameter=["Squash Window Size", "Squash Waveform"],
                                                                   expected=[15, programmed_squash_wave],
                                                                   actual=[squash_window_size, squash_waveform])
        else:
            logging.warning("Squashing is disabled. Driver must enable squashing.")
            gdhm.report_bug(
                title="[Interfaces][Display_Engine] CD clock squashing disabled",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
        # [LNL DCN - 14012932687] Verify MBUS programming during CD clock program sequence
        verify &= LnlClock.__verify_mbus_programming(gfx_index, display_list, programmed_cdclock_freq,
                                                     programmed_pll_output)

        return verify

    ##
    # @brief        Function to get Max CD Clock
    # @param[in]    gfx_index - Adapter to verify
    # @return       max_cd_clock - Max System CD Clock
    def get_system_max_cd_clk(self, gfx_index: str) -> float:
        from DisplayRegs import NonAutoGenRegs

        max_cd_clock = 0
        _clock_helper = clock_helper.ClockHelper()

        reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)
        logging.debug(f"Reference clock identified as : {reference_clock} MHz")

        offset = NonAutoGenRegs.OFFSET_SWF06.SW06
        value = DisplayArgs.read_register(offset, gfx_index)
        swf06 = NonAutoGenRegs.REG_SWF06(offset, value)
        max_value = swf06.MaxCdClockSupported
        logging.debug(f"Max CD clock supported from SW06 register: {max_value} MHz")

        # on pre-si, swf06 register may not be modeled, and correct value won't be read. Then assume max.
        if max_value == 0 and reference_clock in self.cdclk_ctl_dict.keys():
            max_cd_clock = max(self.cdclk_ctl_dict[reference_clock].keys())
        elif max_value in self.cdclock_register_freq_dict.keys():
            max_cd_clock = self.cdclock_register_freq_dict[max_value]
        else:
            logging.error(f"Failed to fetch max CD clock with max value ({max_value}) from SWF06 register")
            gdhm.report_test_bug_di(
                "[Interfaces][Display_Engine][LNL] Failed to fetch max CD clock with max value from SWF06 register")

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
    def get_optimal_cd_clock_from_pixelclock(self, gfx_index: str, max_pixel_rate: float,
                                             display_list: List[str]) -> float:
        _clock_helper = clock_helper.ClockHelper()
        optimal_cd_clock: float = 0
        max_dsc_slice_one_pixel_clock = _clock_helper.get_max_dsc_slice_1_pixel_clock(gfx_index, display_list)

        # For DSC Displays with Slice Count of 1, Optimal Cd Clock using 2ppc method will not be sufficient to drive the
        # Display as only one DSC Engine will be active and this DSC Engine Clock will be synchronized with the CD Clock
        # not CD Clock x 2. Hence, For DSC Displays with Slice Count 1 optimal cd clock will be determined with 1ppc
        # method. For this purpose, pixel clock of dsc display will be multiplied by 2 and the resultant max pixel rate
        # will be used to determine optimal cd clock
        supported_pixel_rate = max(max_pixel_rate, max_dsc_slice_one_pixel_clock * 2)

        reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)
        if reference_clock in self.cdclk_ctl_dict.keys():
            # Assuming CD clock programming is done with 2ppc
            cd_clock_freq_list = sorted(list(self.cdclk_ctl_dict[reference_clock].keys()))
            supported_cd_clocks = [cd_clock for cd_clock in cd_clock_freq_list if cd_clock * 2 > supported_pixel_rate]
            logging.info(f"Supported CD clocks for pixel_rate:{supported_pixel_rate} = {supported_cd_clocks}")
            # Get first element from sorted list if list is non-empty or take max CD clock
            optimal_cd_clock = supported_cd_clocks[0] if bool(supported_cd_clocks) else max(cd_clock_freq_list)
        else:
            logging.error("Invalid reference clock frequency programmed. Failed to get optimal CD clock programmed")

        logging.info(f"Optimal Cd clock: {optimal_cd_clock} MHz")
        return optimal_cd_clock

    ##
    # @brief        Function for calculating optimal cd clock
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    display_list - List of Display
    # @return       optimal_cd_clock - Returns the optimal cd clock in MHz
    def get_optimal_cdclock(self, gfx_index: str, display_list: List[str]) -> float:
        _clock_helper = clock_helper.ClockHelper()

        platform = _clock_helper.get_platform_name(gfx_index)

        # Check if the mode is pipe ganged modeset and get the number of pipes required to drive the mode.
        is_pipe_joiner_required, no_of_pipe_required, pipe_joiner_ports = False, 1, {}
        effective_cd_clock_hz = clock_helper.GEN14PLUS_EFFECTIVE_CD_CLOCK_MHZ * 1000000 if platform == "LNL" else \
            clock_helper.PTL_EFFECTIVE_CD_CLOCK_MHZ * 1000000
        for port_name in display_list:
            logging.info(f"Port name: {port_name}")
            is_pipe_joiner_required, no_of_pipe_required = _clock_helper.is_pipe_joiner_required(gfx_index, port_name,
                                                                                                 effective_cd_clock_hz)
            if is_pipe_joiner_required is True:
                pipe_joiner_ports[port_name] = {'gfx_index': gfx_index, 'no_of_pipe_required': no_of_pipe_required}

        supported_pixel_rate = _clock_helper.get_max_pixel_rate(display_list, gfx_index,
                                                                pipe_joiner_ports=pipe_joiner_ports)
        optimal_cdclock = self.get_optimal_cd_clock_from_pixelclock(gfx_index, supported_pixel_rate, display_list)

        return optimal_cdclock

    ##
    # @brief        Method to get MBUS programming
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    display_list - List of Display
    # @param[in]    cdclk_freq - Input CDCLK frequency
    # @param[in]    mdclk_freq - Input MDCLK frequency
    # @return       Return True if MBUS verification is successful, False otherwise
    @staticmethod
    def __verify_mbus_programming(gfx_index: str, display_list: list, cdclk_freq: float, mdclk_freq: float) -> bool:
        _clock_helper = clock_helper.ClockHelper()
        verify = True
        platform = _clock_helper.get_platform_name(gfx_index)

        # Get programmed MBUS CTL register data
        mbus_ctl_offset = Gen15Regs.OFFSET_MBUS_CTL.MBUS_CTL
        mbus_ctl_value = DisplayArgs.read_register(mbus_ctl_offset, gfx_index)
        mbus_ctl_reg_value = Gen15Regs.REG_MBUS_CTL(mbus_ctl_offset, mbus_ctl_value)
        programmed_tt_min = mbus_ctl_reg_value.TranslationThrottleMin
        programmed_hashing_mode = mbus_ctl_reg_value.HashingMode
        programmed_mbus_joining = Gen15Regs.ENUM_MBUS_JOINING(mbus_ctl_reg_value.MbusJoining).name
        logging.debug(f"Programmed [TranslationThrottleMin, HashingMode, MbusJoining] = [{programmed_tt_min},"
                      f" {programmed_hashing_mode}, {programmed_mbus_joining}]")

        # Get programmed DBUF CTL registers' data
        dbuf_ctl0_offset = Gen15Regs.OFFSET_DBUF_CTL.DBUF_CTL_S0
        dbuf_ctl0_value = DisplayArgs.read_register(dbuf_ctl0_offset, gfx_index)
        dbuf_ctl0_reg_value = Gen15Regs.REG_DBUF_CTL(dbuf_ctl0_offset, dbuf_ctl0_value)
        programmed_min_tracker_state_service0 = dbuf_ctl0_reg_value.MinTrackerStateService

        dbuf_ctl1_offset = Gen15Regs.OFFSET_DBUF_CTL.DBUF_CTL_S1
        dbuf_ctl1_value = DisplayArgs.read_register(dbuf_ctl1_offset, gfx_index)
        dbuf_ctl1_reg_value = Gen15Regs.REG_DBUF_CTL(dbuf_ctl1_offset, dbuf_ctl1_value)
        programmed_min_tracker_state_service1 = dbuf_ctl1_reg_value.MinTrackerStateService

        dbuf_ctl2_offset = Gen15Regs.OFFSET_DBUF_CTL.DBUF_CTL_S2
        dbuf_ctl2_value = DisplayArgs.read_register(dbuf_ctl2_offset, gfx_index)
        dbuf_ctl2_reg_value = Gen15Regs.REG_DBUF_CTL(dbuf_ctl2_offset, dbuf_ctl2_value)
        programmed_min_tracker_state_service2 = dbuf_ctl2_reg_value.MinTrackerStateService

        dbuf_ctl3_offset = Gen15Regs.OFFSET_DBUF_CTL.DBUF_CTL_S3
        dbuf_ctl3_value = DisplayArgs.read_register(dbuf_ctl3_offset, gfx_index)
        dbuf_ctl3_reg_value = Gen15Regs.REG_DBUF_CTL(dbuf_ctl3_offset, dbuf_ctl3_value)
        programmed_min_tracker_state_service3 = dbuf_ctl3_reg_value.MinTrackerStateService

        logging.debug(f"Programmed [MinTrackerStateService0, MinTrackerStateService1, MinTrackerStateService2,"
                      f" MinTrackerStateService3] = [{programmed_min_tracker_state_service0},"
                      f" {programmed_min_tracker_state_service1}, {programmed_min_tracker_state_service2},"
                      f" {programmed_min_tracker_state_service3}]")

        expected_translated_throttle_min = 0  # Invalid data, not expected to be programmed
        expected_min_tracker_state_service = 0  # Invalid data, not expected to be programmed
        # Default hashing mode, except for single display over Pipe A/B
        expected_hashing_mode = Gen15Regs.ENUM_HASHING_MODE.HASHING_MODE_2X2_HASHING.value
        expected_mbus_joining = Gen15Regs.ENUM_MBUS_JOINING.MBUS_JOINING_DISABLED.name

        # Check for current display pipe mapping if single display is present in scenario
        if display_list is not None and len(display_list) == 1:
            effective_cd_clock_hz = clock_helper.GEN14PLUS_EFFECTIVE_CD_CLOCK_MHZ * 1000000 if platform == "LNL" else \
                clock_helper.PTL_EFFECTIVE_CD_CLOCK_MHZ * 1000000
            is_pipe_joiner_required, no_of_pipe_required = _clock_helper.is_pipe_joiner_required(gfx_index,
                                                                                                 display_list[0],
                                                                                                 effective_cd_clock_hz)
            logging.info(f"PipeJoiner required for {display_list[0]}: {is_pipe_joiner_required}({no_of_pipe_required})")
            if is_pipe_joiner_required is False:
                _display_base = display_base.DisplayBase(display_list[0], gfx_index=gfx_index)
                if _display_base.pipe_suffix.upper() in ['A', 'B']:
                    expected_hashing_mode = Gen15Regs.ENUM_HASHING_MODE.HASHING_MODE_1X4_HASHING.value
                    expected_mbus_joining = Gen15Regs.ENUM_MBUS_JOINING.MBUS_JOINING_ENABLED.name

        # Based on ceil(mdclk/cdclk) ratio, program Min Tracker State Service, Translation Throttle Min fields
        mdclk_cdclk_ratio_numerator = math.ceil(mdclk_freq / cdclk_freq)

        if mdclk_cdclk_ratio_numerator == 2:
            expected_translated_throttle_min = MBusType.SEPARATE_MDCLK2_CDCLK1.value
            expected_min_tracker_state_service = MBusType.SEPARATE_MDCLK4_CDCLK1.value \
                if programmed_mbus_joining == Gen15Regs.ENUM_MBUS_JOINING.MBUS_JOINING_ENABLED.name \
                else MBusType.SEPARATE_MDCLK2_CDCLK1.value
        elif mdclk_cdclk_ratio_numerator == 3:
            expected_translated_throttle_min = MBusType.SEPARATE_MDCLK3_CDCLK1.value
            expected_min_tracker_state_service = MBusType.JOINED_MDCLK3_CDCLK1.value \
                if programmed_mbus_joining == Gen15Regs.ENUM_MBUS_JOINING.MBUS_JOINING_ENABLED.name \
                else MBusType.SEPARATE_MDCLK3_CDCLK1.value
        elif mdclk_cdclk_ratio_numerator == 4:
            expected_translated_throttle_min = MBusType.SEPARATE_MDCLK4_CDCLK1.value
            expected_min_tracker_state_service = MBusType.JOINED_MDCLK4_CDCLK1.value \
                if programmed_mbus_joining == Gen15Regs.ENUM_MBUS_JOINING.MBUS_JOINING_ENABLED.name \
                else MBusType.SEPARATE_MDCLK4_CDCLK1.value
        else:
            logging.error(f"Invalid MDCLK:CDCLK ratio programmed. Ratio numerator={mdclk_cdclk_ratio_numerator}")
            gdhm.report_bug(
                title="[Interfaces][Display_Engine] Invalid MDCLK:CDCLK ratio programmed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )

        # Verify MBUS CTL register for MDCLK:CDCLK ratio
        verify &= _clock_helper.verify_cd_clock_programming_ex(feature="MBUS_CTL",
                                                               parameter=["Translation Throttle Min", "Hashing Mode",
                                                                          "MBUS Joining"],
                                                               expected=[expected_translated_throttle_min,
                                                                         expected_hashing_mode, expected_mbus_joining],
                                                               actual=[programmed_tt_min, programmed_hashing_mode,
                                                                       programmed_mbus_joining])

        # Verify DBUF CTL register based MDCLK:CDCLK ratio and Pipe enabled.
        # All DBUF control registers expected to have the same value to be programmed.
        verify &= _clock_helper.verify_cd_clock_programming_ex(feature="DBUF_CTL",
                                                               parameter=["Min Tracker State Service S0",
                                                                          "Min Tracker State Service S1",
                                                                          "Min Tracker State Service S2",
                                                                          "Min Tracker State Service S3"],
                                                               expected=[expected_min_tracker_state_service] * 4,
                                                               actual=[programmed_min_tracker_state_service0,
                                                                       programmed_min_tracker_state_service1,
                                                                       programmed_min_tracker_state_service2,
                                                                       programmed_min_tracker_state_service3])
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
        hf_vsdb_parser = hf_vsdb_block.HdmiForumVendorSpecificDataBlock()
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
                            # for Yuv420, pixel clock is 0.5 of pixel clock we get from edid as defined in appendix J
                            # of HDMI spec.
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
                elif 'DP' in str(port_name).upper():
                    link_rate = dpcd_helper.DPCD_getLinkRate(
                        enumerated_displays.ConnectedDisplays[count].DisplayAndAdapterInfo)
                    # Control link symbols and data link symbols are of size 32 bits in case of 128b/132b encoding.
                    link_symbol_clock = round(link_rate * 1000 / 32, 2) if link_rate >= 10 else round(
                        link_rate * 100, 2)

        valfreq_offset = 0
        if '_A' in str(port_name).upper():
            valfreq_offset = Gen15DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_A
        elif '_B' in str(port_name).upper():
            valfreq_offset = Gen15DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_B
        elif '_F' in str(port_name).upper():
            valfreq_offset = Gen15DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_USBC1
        elif '_G' in str(port_name).upper():
            valfreq_offset = Gen15DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_USBC2
        elif '_H' in str(port_name).upper():
            valfreq_offset = Gen15DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_USBC3
        elif '_I' in str(port_name).upper():
            valfreq_offset = Gen15DdiRegs.OFFSET_DDI_CLK_VALFREQ.DDI_CLK_VALFREQ_USBC4

        value = DisplayArgs.read_register(valfreq_offset, gfx_index)
        reg_value_valfreq = Gen15DdiRegs.REG_DDI_CLK_VALFREQ(valfreq_offset, value)
        valfreq = reg_value_valfreq.DdiValidationFrequency
        # There is a precision mismatch due to which below rounding off is done.
        # E.g. Expected value = 92.8125 and actual value = 92.813, so will only compare till 2 digits
        pixel_rate_mhz = round((valfreq / 1000), 2)

        verify &= _clock_helper.verify_port_clock_programming_ex(feature="PHY TEST MODE",
                                                                 parameter="Phy Test Mode Val Frequency in MHz",
                                                                 expected=[rounded_pixel_rate] if 'HDMI' in str(
                                                                     port_name).upper() else [link_symbol_clock],
                                                                 actual=[pixel_rate_mhz])

        return verify

    ##
    # @brief        This function gets the lane count allotted by IOM to display controller on a TC PHY.
    # @details      Note: Even if display is using 2 lanes only, if IOM allots 4 lanes for display, then we get 4 lanes.
    # @param[in]    port_name - Port name like DP_F, HDMI_B, etc.
    # @param[in]    gfx_index - Adapter index like 'gfx_0'
    # @return       lane_count - the lane count in integer value.
    @staticmethod
    def lnl_snps_c20_get_lane_count_given_by_iom(port_name: str, gfx_index: str) -> int:
        lane_count = 0
        _clock_helper = clock_helper.ClockHelper()

        # if VBT is configured to NATIVE/PLUS/TBT (not TC), always use 4 lanes.
        if 'TC' not in _clock_helper.get_port_type_for_port(port_name):
            lane_count = 4
            return lane_count

        ddi_name = str(port_name).split('_')[1]
        if ddi_name in ['F', 'G']:
            offset = Gen15DdiRegs.OFFSET_PORT_TX_DFLEXPA1.PORT_TX_DFLEXPA1_FIA1
        elif ddi_name in ['H', 'I']:
            offset = Gen15DdiRegs.OFFSET_PORT_TX_DFLEXPA1.PORT_TX_DFLEXPA1_FIA2
        else:
            logging.error(f'Wrong port passed. {port_name} not supported by LNL C20 PHY')
            gdhm.report_test_bug_di("[Interfaces][Display_Engine][LNL] Invalid port passed to fetch DDI name")
            return 0

        value = DisplayArgs.read_register(offset, gfx_index)
        port_tx_dflexpa1 = Gen15DdiRegs.REG_PORT_TX_DFLEXPA1(offset, value)

        if ddi_name in ['F', 'H']:
            pin_assignment = port_tx_dflexpa1.DisplayportPinAssignmentForTypeCConnector0
        else:
            pin_assignment = port_tx_dflexpa1.DisplayportPinAssignmentForTypeCConnector1

        # Assignments D has 2 lanes for DP alternate mode.
        if pin_assignment == Gen15DdiRegs.ENUM_DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0. \
                DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_D.value:
            lane_count = 2
        # Assignments C and E have 4 lanes for DP alternate mode.
        elif pin_assignment in [
            Gen15DdiRegs.ENUM_DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0.
                    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C.value,
            Gen15DdiRegs.ENUM_DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0.
                    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_E.value]:
            lane_count = 4
        else:
            logging.error(f'For {port_name}, unsupported pin_assignment ({pin_assignment}) programmed in '
                          f'PORT_TX_DFLEXPA1 register')
            gdhm.report_test_bug_di("[Interfaces][Display_Engine][LNL] Unsupported pin assignment programmed in "
                                    "PORT_TX_DFLEXPA1 register")

        return lane_count

    ##
    # @brief        verification logic for port slice block (PICA registers) for LNL.
    # @param[in]    port_name - port name like DP_F, HDMI_B, etc.
    # @param[in]    gfx_index - adapter index like 'gfx_0'
    # @return       ret - returns True if all verification passed, False otherwise
    @staticmethod
    def verify_port_slice(port_name: str, gfx_index: str) -> bool:
        from Tests.ModeEnumAndSet.display_mode_enumeration_base import ModeEnumAndSetBase
        ret = True
        _clock_helper = clock_helper.ClockHelper()
        lnl_clock_helper_ = lnl_clock_helper.LnlClockHelper()
        hf_vsdb_parser = hf_vsdb_block.HdmiForumVendorSpecificDataBlock()
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
        get_ddi = display_base.DisplayBase(port_name, 'LNL', gfx_index)
        pipe_ddi = get_ddi.GetPipeDDIAttachedToPort(port_name, gfx_index=gfx_index)
        pipe = (pipe_ddi[0])[-1]
        offset = eval('Gen15TranscoderRegs.OFFSET_TRANS_DDI_FUNC_CTL.TRANS_DDI_FUNC_CTL_' + pipe)
        value = DisplayArgs.read_register(offset, gfx_index)
        trans_hdmi_port_width = Gen15TranscoderRegs.REG_TRANS_DDI_FUNC_CTL(offset, value)
        transcoder_port_width_value = trans_hdmi_port_width.PortWidthSelection

        # map based on values of 'DDI Clock Select' of register PORT_CLOCK_CTL in bspec:
        # https://gfxspecs.intel.com/Predator/Home/Index/65103?dstFilter=LNL&mode=Filter
        ddi_clk_select_map = {
            0b1000: 'Maxpclk',
            0b1001: 'div18clk',
            0b1100: 'TBT 162',
            0b1101: 'TBT 270',
            0b1110: 'TBT 540',
            0b1111: 'TBT 810'
        }
        # map based on values of 'Port Width' of register PORT_BUF_CTL1 in bspec:
        # https://gfxspecs.intel.com/Predator/Home/Index/65091?dstFilter=LNL&mode=Filter
        port_width_lanes_map = {
            0b000: 1,
            0b001: 2,
            0b011: 4,
            0b100: 3
        }

        ddi_name = str(port_name).split('_')[1]
        bspec_port_name = lnl_clock_helper_.ddi_to_bspec_name_map[ddi_name.upper()]
        # determine which msgbus PHY lanes are owned by display controller
        if 'USBC' in bspec_port_name:
            no_of_lanes_given_by_iom = LnlClock.lnl_snps_c20_get_lane_count_given_by_iom(port_name, gfx_index)
            logging.info(f'For {port_name}, IOM has given {no_of_lanes_given_by_iom} lanes to display controller.')
            if no_of_lanes_given_by_iom == 4:
                msgbus_phy_lanes_owned = ['0', '1']
            elif expected_port_reversal:
                msgbus_phy_lanes_owned = ['1']
            else:
                msgbus_phy_lanes_owned = ['0']
        else:
            msgbus_phy_lanes_owned = ['0', '1']

        offset = eval('Gen15DdiRegs.OFFSET_PORT_BUF_CTL1.PORT_BUF_CTL1_' + bspec_port_name)
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl1 = Gen15DdiRegs.REG_PORT_BUF_CTL1(offset, value)

        offset = eval('Gen15DdiRegs.OFFSET_DDI_CTL_DE.DDI_CTL_DE_' + bspec_port_name)
        value = DisplayArgs.read_register(offset, gfx_index)
        ddi_ctl_de = Gen15DdiRegs.REG_DDI_CTL_DE(offset, value)

        offset = eval('Gen15DdiRegs.OFFSET_PORT_BUF_CTL2.PORT_BUF_CTL2_' + bspec_port_name)
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl2 = Gen15DdiRegs.REG_PORT_BUF_CTL2(offset, value)

        offset = eval('Gen15DdiRegs.OFFSET_PORT_BUF_CTL3.PORT_BUF_CTL3_' + bspec_port_name)
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl3 = Gen15DdiRegs.REG_PORT_BUF_CTL3(offset, value)

        offset = eval('Gen15PllRegs.OFFSET_PORT_CLOCK_CTL.PORT_CLOCK_CTL_' + bspec_port_name)
        value = DisplayArgs.read_register(offset, gfx_index)
        port_clock_ctl = Gen15PllRegs.REG_PORT_CLOCK_CTL(offset, value)

        # Dictionary to map the Decimal Value of Port Width from Register and Transcoder
        port_width_transcoder_map = {
            0b000: 1,
            0b001: 2,
            0b010: 3,
            0b011: 4
        }

        # verify PORT_BUF_CTL1 register
        if 'TBT' in _clock_helper.get_port_type_for_port(port_name):
            ret &= _clock_helper.verify_port_clock_programming_ex(feature="PORT_BUF_CTL1_" + bspec_port_name,
                                                                  parameter="IO Select",
                                                                  expected=[1], actual=[port_buf_ctl1.IoSelect])
        ret &= _clock_helper.verify_port_clock_programming_ex(feature="DDI_CTL_DE_" + bspec_port_name,
                                                              parameter="D2D Link Enable",
                                                              expected=[1], actual=[ddi_ctl_de.D2DLinkEnable])
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
        if 'TBT' in _clock_helper.get_port_type_for_port(port_name):
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
            lanes_to_program_pipe_reset = ['0', '1'] if 'USBC' in bspec_port_name else msgbus_phy_lanes_owned
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
    # @brief        Verifies PCode notified Voltage Level as part of CD clock programming
    # @param[in]    gfx_index: Graphics Adapter Index
    # @param[in]    ports: List of port names of active displays
    # @return       bool - True if verification is successful, False otherwise
    def verify_voltage_level_notified_to_pcode(self, gfx_index: str, ports: List[str]) -> bool:
        _clock_helper = clock_helper.ClockHelper()
        _display_config = display_config.DisplayConfiguration()
        _lnl_clock_helper = lnl_clock_helper.LnlClockHelper()

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
        pm_dmd_req_offset = Gen15Regs.OFFSET_INITIATE_PM_DMD_REQ.INITIATE_PM_DMD_REQ
        pm_dmd_req_register = DisplayArgs.read_register(pm_dmd_req_offset, gfx_index)
        pm_dmd_req_reg_value = Gen15Regs.REG_INITIATE_PM_DMD_REQ(pm_dmd_req_offset, pm_dmd_req_register)
        logging.debug(f"INITIATE_PM_DMD_REQ register value - 0x{pm_dmd_req_reg_value.value:X}")
        actual_voltage_level_index = pm_dmd_req_reg_value.VoltageLevelIndex
        actual_ddi_clk_freq = pm_dmd_req_reg_value.DdiclkFreq
        logging.info(f"Programmed [VoltageLevelIndex, DdiclkFreq] = [{actual_voltage_level_index}, "
                     f"{actual_ddi_clk_freq}]")

        max_ddi_freq_target, max_ddi_freq = _lnl_clock_helper.get_max_ddi_symbol_clock_frequency(gfx_index, ports)
        logging.info(f"Target {max_ddi_freq_target} with max DDI freq = {max_ddi_freq}")

        # Ref: DVFS programming expectation - https://gfxspecs.intel.com/Predator/Home/Index/65565
        if expected_cdclock <= 307.2 and max_ddi_freq <= 594:
            expected_voltage_level_index = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_0.value
            if actual_voltage_level_index != expected_voltage_level_index:
                # logging.warning("Assigning next VoltageLevel since it should not have any power functionality issue")
                # expected_voltage_level_index = actual_voltage_level_index
                gdhm.report_test_bug_pc("[Interfaces][Display_Engine][CD Clock][WARNING] Lower VoltageLevel calculated",
                                        priority=gdhm.Priority.P3, exposure=gdhm.Exposure.E3)
        elif expected_cdclock <= 480:
            expected_voltage_level_index = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_1.value
        elif expected_cdclock <= 556.8:
            expected_voltage_level_index = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_2.value
        else:
            # Max CD Clock frequency requires Voltage Level 3 to be programmed
            expected_voltage_level_index = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_3.value
        logging.info(f"Expected VoltageLevel = {expected_voltage_level_index}")
        return _clock_helper.verify_cd_clock_programming_ex(feature="INITIATE_PM_DMD_REQ",
                                                            parameter=["VoltageLevelIndex"],
                                                            expected=[expected_voltage_level_index],
                                                            actual=[actual_voltage_level_index])
