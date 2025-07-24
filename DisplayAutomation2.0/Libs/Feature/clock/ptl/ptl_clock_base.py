##
# @file         ptl_clock_base.py
# @brief        PTL clock validation base class
# @details      Defines methods to handle CD clock verification
# @author       Kiran Kumar Lakshmanan

import logging
import math
from typing import Dict, List

from DisplayRegs import DisplayArgs
# @todo: Using Gen15 registers until auto-generated files are available
from DisplayRegs.Gen15 import Gen15Regs
from DisplayRegs.Gen15.Pll import Gen15PllRegs
from Libs.Core import enum
from Libs.Core.display_config import display_config
from Libs.Core.logger import gdhm
from Libs.Feature.clock import clock_helper
from Libs.Feature.clock.clock_helper import CdClockMap, DEFAULT_REFERENCE_CLOCK_FREQUENCY, VoltageFrequencyLevel, \
    MBusType, WCL_MAX_CD_CLOCK_MHZ
from Libs.Feature.clock.ptl import ptl_clock_helper
from Libs.Feature.display_engine.de_base import display_base


##
# @brief        Base class for LNL Clock Verification
# @details      CD clock and port clock verification methods are defined under this class
class PtlClock:
    # Registers used for verification - CD Clock Programming
    # Reference: https://gfxspecs.intel.com/Predator/Home/Index/68861

    is_wcl_platform: bool = False
    max_voltage_level_index: int = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_3.value

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
            326.4: CdClockMap(326.4, 17, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              652.8, 0xFFFF, VoltageFrequencyLevel.VF1),
            345.6: CdClockMap(345.6, 18, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              691.2, 0xFFFF, VoltageFrequencyLevel.VF1),
            364.8: CdClockMap(364.8, 19, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              729.6, 0xFFFF, VoltageFrequencyLevel.VF1),
            384: CdClockMap(384, 20, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            768, 0xFFFF, VoltageFrequencyLevel.VF1),
            403.2: CdClockMap(403.2, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xFFFF, VoltageFrequencyLevel.VF1),
            422.4: CdClockMap(422.4, 22, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              844.8, 0xFFFF, VoltageFrequencyLevel.VF1),
            441.6: CdClockMap(441.6, 23, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              883.2, 0xFFFF, VoltageFrequencyLevel.VF1),
            460.8: CdClockMap(460.8, 24, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              921.6, 0xFFFF, VoltageFrequencyLevel.VF1),
            480: CdClockMap(480, 25, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            960, 0xFFFF, VoltageFrequencyLevel.VF1),

            # VoltageLevel VF2
            499.2: CdClockMap(499.2, 26, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              998.4, 0xFFFF, VoltageFrequencyLevel.VF2),
            518.4: CdClockMap(518.4, 27, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1036.8, 0xFFFF, VoltageFrequencyLevel.VF2),
            537.6: CdClockMap(537.6, 28, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1075.2, 0xFFFF, VoltageFrequencyLevel.VF2),
            556.8: CdClockMap(556.8, 29, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1113.6, 0xFFFF, VoltageFrequencyLevel.VF2),


            # VoltageLevel VF3
            576: CdClockMap(576, 30, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            1152, 0xFFFF, VoltageFrequencyLevel.VF3),
            595.2: CdClockMap(595.2, 31, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1190.4, 0xFFFF, VoltageFrequencyLevel.VF3),
            614.4: CdClockMap(614.4, 32, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1228.8, 0xFFFF, VoltageFrequencyLevel.VF3),
            633.6: CdClockMap(633.6, 33, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1267.2, 0xFFFF, VoltageFrequencyLevel.VF3),
            652.8: CdClockMap(652.8, 34, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1305.6, 0xFFFF, VoltageFrequencyLevel.VF3),
            672: CdClockMap(672, 35, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                             1344, 0xFFFF, VoltageFrequencyLevel.VF3),
            691.2: CdClockMap(691.2, 36, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1382.4, 0xFFFF, VoltageFrequencyLevel.VF3),
        }
    }

    ##
    # @brief        Class Constructor
    # @param[in]    sku_name - Defines current platform SKU name. Pass WCL explicitly for WildCatLake platform
    #               verifications. Default value is PTL (also applicable for NVL)
    def __init__(self, sku_name="PTL"):
        self.is_wcl_platform = sku_name == "WCL"
        if self.is_wcl_platform is True:
            self.cdclk_ctl_dict = {k: v for k, v in self.cdclk_ctl_dict.items()
                                   if not any(cd_freq > WCL_MAX_CD_CLOCK_MHZ for cd_freq in v)}
            self.max_voltage_level_index = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_1.value

        logging.info(f"Updated CD Clock Dict = {self.cdclk_ctl_dict}")

    ##
    # @brief        Verification method to check for CD clock programming in PTL
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

        # If the Panel is DSC Supported but the mode is non-DSC then the CD Clock verification will be skipped
        if _clock_helper.is_non_dsc_mode_present(gfx_index, display_list):
            return True


        optimal_cd_clock = self.get_optimal_cdclock(gfx_index, display_list)

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
        verify &= PtlClock.__verify_mbus_programming(gfx_index, display_list, programmed_cdclock_freq,
                                                     programmed_pll_output)

        return verify

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
            effective_cd_clock_hz = clock_helper.PTL_EFFECTIVE_CD_CLOCK_MHZ * 1000000
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
    # @brief        Function to get Max CD Clock
    # @param[in]    gfx_index - Adapter to verify
    # @return       max_cd_clock - Max System CD Clock
    def get_system_max_cd_clk(self, gfx_index: str) -> float:
        _clock_helper = clock_helper.ClockHelper()

        reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)
        logging.debug(f"Reference clock identified as : {reference_clock} MHz")

        max_cd_clock = max(self.cdclk_ctl_dict[reference_clock].keys())

        return max_cd_clock

    ##
    # @brief        Function for calculating optimal cd clock with given pixel_rate
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @param[in]    max_pixel_rate: float
    #                   Maximum pixel rate
    # @param[in]    display_list: list
    #                   Display list
    # @param[in]    supported_pixel_rate_target_id: tuple
    # @param[in]    pipe_joiner_ports : dict
    # @return       optimal_cdclock: float
    #                   returns the optimal cd clock in MHz
    def get_optimal_cd_clock_from_pixelclock(self, gfx_index: str, max_pixel_rate: float,
                                             display_list: List[str], max_supported_pixel_rate_target_id, pipe_joiner_ports=None) -> float:
        _clock_helper = clock_helper.ClockHelper()
        optimal_cd_clock: float = 0
        max_slice_1_pixel_rate_target_id = _clock_helper.get_max_dsc_slice_1_pixel_clock(gfx_index, display_list, require_target_id = True)

        # For DSC Displays with Slice Count of 1, Optimal Cd Clock using 2ppc method will not be sufficient to drive the
        # Display as only one DSC Engine will be active and this DSC Engine Clock will be synchronized with the CD Clock
        # not CD Clock x 2. Hence, For DSC Displays with Slice Count 1 optimal cd clock will be determined with 1ppc
        # method. For this purpose, pixel clock of dsc display will be multiplied by 2 and the resultant max pixel rate
        # will be used to determine optimal cd clock

        # sinlge_pipe_pixel_rate = max(max_pixel_rate
        # , max_dsc_slice_one_pixel_clock * 2)

        # If panel is DSC Slice 1 max_slice_1_pixel_rate_target_id will be selected to get Elevated pixel clock
        #Else it will select max_pixel_rate among the displays
        if max_supported_pixel_rate_target_id[0] == max(max_supported_pixel_rate_target_id[0], max_slice_1_pixel_rate_target_id[0] * 2):
            max_pixel_rate_target_id = max_supported_pixel_rate_target_id
        else:
            max_slice1_pixel_rate  = max_slice_1_pixel_rate_target_id[0] * 2
            max_pixel_rate_target_id = (max_slice1_pixel_rate, max_slice_1_pixel_rate_target_id[1])


        logging.info(f"Max Pixel Rate and Target_ID : {max_pixel_rate_target_id}")
        supported_pixel_rate = _clock_helper.get_elevated_pixel_clock(gfx_index, max_pixel_rate_target_id, display_list, pipe_joiner_ports)
        logging.info(f"supported_pixel_rate : {supported_pixel_rate}")

        reference_clock = _clock_helper.get_reference_clock_from_register(gfx_index)
        if reference_clock in self.cdclk_ctl_dict.keys():
            # Assuming CD clock programming is done with 2ppc
            cd_clock_freq_list = sorted(list(self.cdclk_ctl_dict[reference_clock].keys()))
            supported_cd_clocks = [cd_clock for cd_clock in cd_clock_freq_list if cd_clock * 2 > supported_pixel_rate]
            logging.info(f"Supported CD clocks for pixel_rate:{supported_pixel_rate} = {supported_cd_clocks}")
            # Get first element from sorted list if list is non-empty or take max CD clock
            optimal_cd_clock = supported_cd_clocks[0] if bool(supported_cd_clocks) else max(cd_clock_freq_list)
        else:
            logging.error(f"Invalid reference clock frequency programmed = {reference_clock}. "
                          f"Failed to get optimal CD clock programmed")

        logging.info(f"Optimal Cd clock: {optimal_cd_clock} MHz")
        return optimal_cd_clock

    ##
    # @brief        Function for calculating optimal cd clock
    # @param[in]    gfx_index - Graphics adapter index
    # @param[in]    display_list - List of Display
    # @return       optimal_cd_clock - Returns the optimal cd clock in MHz
    def get_optimal_cdclock(self, gfx_index: str, display_list: List[str]) -> float:
        _clock_helper = clock_helper.ClockHelper()

        # Check if the mode is pipe ganged modeset and get the number of pipes required to drive the mode.
        is_pipe_joiner_required, no_of_pipe_required, pipe_joiner_ports = False, 1, {}
        effective_cd_clock_hz = clock_helper.PTL_EFFECTIVE_CD_CLOCK_MHZ * 1000000
        for port_name in display_list:
            logging.info(f"Port name: {port_name}")

            is_vdsc_supported, is_vdsc_enabled = _clock_helper.get_dsc_status_for_current_mode(gfx_index, port_name)
            if is_vdsc_enabled is False:
                effective_cd_clock_hz = clock_helper.PTL_NON_DSC_EFFECTIVE_CD_CLOCK_MHZ * 1000000
            is_pipe_joiner_required, no_of_pipe_required = _clock_helper.is_pipe_joiner_required(gfx_index, port_name,
                                                                                                 effective_cd_clock_hz)
            if is_pipe_joiner_required is True:
                pipe_joiner_ports[port_name] = {'gfx_index': gfx_index, 'no_of_pipe_required': no_of_pipe_required}

        supported_pixel_rate_target_id = _clock_helper.get_max_pixel_rate(display_list, gfx_index, require_target_id = True,
                                                                pipe_joiner_ports=pipe_joiner_ports)
        optimal_cdclock = self.get_optimal_cd_clock_from_pixelclock(gfx_index, supported_pixel_rate_target_id[0], display_list, supported_pixel_rate_target_id, pipe_joiner_ports=pipe_joiner_ports)

        return optimal_cdclock

    ##
    # @brief        Generic function to fetch current CD clock
    # @param[in]    gfx_index: str - Graphics index of Graphics adapter
    # @return       current cd clock
    def get_current_cd_clock(self, gfx_index: str) -> float:
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
    # @brief        Verifies PCode notified Voltage Level as part of CD clock programming
    # @param[in]    gfx_index: Graphics Adapter Index
    # @param[in]    ports: List of port names of active displays
    # @return       bool - True if verification is successful, False otherwise
    def verify_voltage_level_notified_to_pcode(self, gfx_index: str, ports: List[str]) -> bool:
        _clock_helper = clock_helper.ClockHelper()
        _display_config = display_config.DisplayConfiguration()
        _ptl_clock_helper = ptl_clock_helper.PtlClockHelper()

        # If the Panel is DSC Supported but the mode is non-DSC then the DVFS verification will be skipped
        if _clock_helper.is_non_dsc_mode_present(gfx_index, ports):
            return True

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

        max_ddi_freq_target, max_ddi_freq = _ptl_clock_helper.get_max_ddi_symbol_clock_frequency(gfx_index, ports)
        logging.info(f"Target {max_ddi_freq_target} with max DDI freq = {max_ddi_freq}")

        # Ref: DVFS programming expectation [PTL/NVL] - https://gfxspecs.intel.com/Predator/Home/Index/65565
        # Ref: DVFS programming expectation [WCL] - https://gfxspecs.intel.com/Predator/Home/Index/68863
        if expected_cdclock <= 307.2 and max_ddi_freq <= 594:
            expected_voltage_level_index = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_0.value
            if actual_voltage_level_index != expected_voltage_level_index:
                gdhm.report_test_bug_pc("[Interfaces][Display_Engine][CD Clock][WARNING] Higher VoltageLevel "
                                        "programmed during DVFS programming",
                                        priority=gdhm.Priority.P3, exposure=gdhm.Exposure.E3)
        elif expected_cdclock <= 480 and self.is_wcl_platform is False:
            expected_voltage_level_index = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_1.value
        elif expected_cdclock <= 556.8 and self.is_wcl_platform is False:
            expected_voltage_level_index = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_2.value
        else:
            # Expect Voltage Level Index to be programmed to this value when Max CD Clock frequency is programmed for
            # PTL/NVL = Voltage Level 3, WCL = Voltage Level 1
            expected_voltage_level_index = self.max_voltage_level_index

        logging.info(f"Expected VoltageLevel = {expected_voltage_level_index}")

        return _clock_helper.verify_cd_clock_programming_ex(feature="INITIATE_PM_DMD_REQ",
                                                            parameter=["VoltageLevelIndex"],
                                                            expected=[expected_voltage_level_index],
                                                            actual=[actual_voltage_level_index])
