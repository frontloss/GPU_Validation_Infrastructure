##
# @file         nvl_clock_base.py
# @brief        NVL clock validation base class
# @details      Defines methods to handle CD clock verification
# @author       Komal Tripathi

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
# @brief        Base class for NVL Clock Verification
# @details      CD clock Frequencies are defined under this class
class NvlClock:
    # Registers used for verification - CD Clock Programming
    # Reference: https://gfxspecs.intel.com/Predator/Home/Index/68861

    max_voltage_level_index: int = Gen15Regs.ENUM_VOLTAGE_LEVEL_INDEX.VOLTAGE_LEVEL_INDEX_INDEX_0.value

    # This dictionary contains mapping values for each requirement for identifying CD clock frequency being programmed
    cdclk_ctl_dict: Dict[float, Dict[float, CdClockMap]] = {
        # Currently only possible ref clk is 38.4 MHz, supported on SoC. The frequency is selected by the SoC.
        DEFAULT_REFERENCE_CLOCK_FREQUENCY: {
            # VoltageLevel VF0
            151.2: CdClockMap(151.2, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xA4A4, VoltageFrequencyLevel.VF0),
            176.4: CdClockMap(176.4, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xAA54, VoltageFrequencyLevel.VF0),
            201.6: CdClockMap(201.6, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xAAAA, VoltageFrequencyLevel.VF0),
            226.8: CdClockMap(226.8, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xAD5A, VoltageFrequencyLevel.VF0),
            252: CdClockMap(252, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xB6B6, VoltageFrequencyLevel.VF0),
            277.2: CdClockMap(277.2, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xDBB6, VoltageFrequencyLevel.VF0),
            302.4: CdClockMap(302.4, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xEEEE, VoltageFrequencyLevel.VF0),
            327.6: CdClockMap(327.6, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xF7DE, VoltageFrequencyLevel.VF0),
            352.8: CdClockMap(352.8, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xFEFE, VoltageFrequencyLevel.VF0),
            378: CdClockMap(378, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            806.4, 0xFFFE, VoltageFrequencyLevel.VF0),
            403.2: CdClockMap(403.2, 21, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              806.4, 0xFFFF, VoltageFrequencyLevel.VF0),


            422.4: CdClockMap(422.4, 22, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              844.8, 0xFFFF, VoltageFrequencyLevel.VF0),
            441.6: CdClockMap(441.6, 23, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              883.2, 0xFFFF, VoltageFrequencyLevel.VF0),
            460.8: CdClockMap(460.8, 24, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              921.6, 0xFFFF, VoltageFrequencyLevel.VF0),
            480: CdClockMap(480, 25, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              960, 0xFFFF, VoltageFrequencyLevel.VF0),
            499.2: CdClockMap(499.2, 26, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              998.4, 0xFFFF, VoltageFrequencyLevel.VF0),
            518.4: CdClockMap(518.4, 27, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            1036.8, 0xFFFF, VoltageFrequencyLevel.VF0),
            537.6: CdClockMap(537.6, 28, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1075.2, 0xFFFF, VoltageFrequencyLevel.VF0),
            556.8: CdClockMap(556.8, 29, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1113.6, 0xFFFF, VoltageFrequencyLevel.VF0),
            576: CdClockMap(576, 30, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1152, 0xFFFF, VoltageFrequencyLevel.VF0),
            595.2: CdClockMap(595.2, 31, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                            1190.4, 0xFFFF, VoltageFrequencyLevel.VF0),
            614.4: CdClockMap(614.4, 32, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1228.8, 0xFFFF, VoltageFrequencyLevel.VF0),
            633.6: CdClockMap(633.6, 33, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1267.2, 0xFFFF, VoltageFrequencyLevel.VF0),
            652.8: CdClockMap(652.8, 34, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1305.6, 0xFFFF, VoltageFrequencyLevel.VF0),
            672: CdClockMap(672, 35, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1344, 0xFFFF, VoltageFrequencyLevel.VF0),
            691.2: CdClockMap(691.2, 36, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1382.4, 0xFFFF, VoltageFrequencyLevel.VF0),
            710.4: CdClockMap(710.4, 37, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1420.8, 0xFFFF, VoltageFrequencyLevel.VF0),
            729.6: CdClockMap(729.6, 38, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1459.2, 0xFFFF, VoltageFrequencyLevel.VF0),
            748.8: CdClockMap(748.8, 39, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1497.6, 0xFFFF, VoltageFrequencyLevel.VF0),
            768: CdClockMap(691.2, 40, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                              1536.0, 0xFFFF, VoltageFrequencyLevel.VF0),
            787.2: CdClockMap(787.2, 41, Gen15PllRegs.ENUM_CD2X_DIVIDER_SELECT.CD2X_DIVIDER_SELECT_DIVIDE_BY_1.value,
                      1574.4, 0xFFFF, VoltageFrequencyLevel.VF0),

        }
    }

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
            supported_cd_clocks = [cd_clock for cd_clock in cd_clock_freq_list if
                                   cd_clock * 2 > supported_pixel_rate]
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
        effective_cd_clock_hz = clock_helper.NVL_EFFECTIVE_CD_CLOCK_MHZ * 1000000
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


