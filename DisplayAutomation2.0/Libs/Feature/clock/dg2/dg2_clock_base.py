##
# @file   dg2_clock_base.py
# @brief  Base class for doing DG2 CD clock and port clock validation
# @author Kruti Vadhavaniya

import logging

from Libs.Core import display_utility
from Libs.Core import system_utility as sys_util
from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.dg2 import dg2_clock_edp
from Libs.Feature.clock.dg2 import dg2_clock_hdmi
from Libs.Core.logger import gdhm

from registers.mmioregister import MMIORegister


##
# @brief DG2 clock verification class for CDCLK and port CLK
class Dg2Clock:
    # CD Clock map as per Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/33869
    cdclock_ctl_freq_dict = dict([
        (163.2, 324),
        (172.8, 344),
        (192, 382),
        (204, 406),
        (244.8, 488),
        (285.6, 569),
        (307.2, 612),
        (326.4, 651),
        (367.2, 732),
        (408, 814),
        (448.8, 896),
        (489.6, 977),
        (530.4, 1059),
        (552, 1102),
        (556.8, 1112),
        (571.2, 1140),
        (612, 1222),
        (652.8, 1304)
    ])

    # DDI values map as in TRANS_DDI_FUNC_CTL register
    ddi_clock_map = dict([
        ('A', 1024),
        ('B', 2048),
        ('C', 4096),
        ('D', 8192)
    ])

    # Reference Frequency to Cd Clock map as per bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/54034
    cdclock_map = dict([
        (38.4, dict([(172.8, 9), (192, 10), (307.2, 16), (326.4, 34), (556.8, 29), (652.8, 34)]))
    ])

    cd2x_divider_map = dict([
        (38.4, dict([(172.8, 1), (192, 1), (307.2, 1), (326.4, 2), (556.8, 1), (652.8, 1)]))
    ])
    # Ref frequency mapping dictionary
    dssm_ref_freq_map = dict([
        (24, 0),
        (19.2, 1),
        (38.4, 2),
        (25, 3)
    ])
    # Pipe Allocation dictionary
    cdclock_pipe_dict = dict([
        ('Pipe_A', 0),
        ('Pipe_B', 2),
        ('Pipe_C', 4),
        ('Pipe_D', 6),
        ('None', 7)
    ])
    # CD clk divider
    cdclock_divider = dict([
        (1, 0),
        (1.5, 1),
        (2, 2),
        (4, 3)
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

    cdclock_ctl_freq = 0
    expected_cdclock = 168
    system_max_cd_clk = 0

    ##
    # @brief Generic function for verifying DG2 clock
    # @param[in] display_port - Port on which Clock verification need to do
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        clock_helper_ = clk_helper.ClockHelper()
        is_pre_si_environment = sys_util.SystemUtility().get_execution_environment_type() in ["SIMENV_FULSIM",
                                                                                              "SIMENV_PIPE2D"]
        target_id = clock_helper_.get_target_id(display_port, gfx_index)
        logging.info("******* CD Clock and PLL Verification of Port : {} (Target ID : {}) *******".format(display_port,
                                                                                                          target_id))

        verify = True

        verify &= self.verify_sanity(display_port, gfx_index)
        if str(display_port).upper().__contains__('HDMI'):
            clock = dg2_clock_hdmi.Dg2ClockHdmi()
            # WA: VSDI-19619 remove this and enable below comment code, once HDMI issue resolved in GTA fulsim.
            if not is_pre_si_environment:
                verify &= clock.verify_clock(display_port, gfx_index)
        elif str(display_port).upper().__contains__('DP'):  # for both edp and DP
            clock = dg2_clock_edp.Dg2ClockEdp()
            verify &= clock.verify_clock(display_port, gfx_index)
        return verify  # & clock.verify_clock(display_port)

    ##
    # @brief Verify the generic sanity for clock for all the displays
    # @param[in] display_port - Port on which Clock verification need to do
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_sanity(self, display_port, gfx_index='gfx_0'):
        clock_helper_ = clk_helper.ClockHelper()
        verify = True
        reg_value = clock_helper_.clock_register_read('CDCLK_CTL_REGISTER', 'CDCLK_CTL', gfx_index)
        cd2x_divider = clock_helper_ \
            .get_value_by_range(reg_value, 22, 23, self.cdclock_divider, "CDCLK_CTL: CD2X_Divider_Select")
        cd2x_pipe = clock_helper_ \
            .get_value_by_range(reg_value, 19, 21, self.cdclock_pipe_dict, "CDCLK_CTL: CD2X_Pipe_Select")

        reg_value = clock_helper_.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
        reference_freq = clock_helper_ \
            .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")
        reg_value = clock_helper_.clock_register_read('CDCLK_PLL_ENABLE_REGISTER', 'CDCLK_PLL_ENABLE', gfx_index)

        pll_enable_str = 'ENABLED' if clock_helper_.get_value_by_range(reg_value, 31, 31, '',
                                                                       "CDCLK_PLL_ENABLE: PLL Enable") == 1 \
            else 'DISABLED'
        pll_lock_str = 'LOCKED' if clock_helper_.get_value_by_range(reg_value, 30, 30, '',
                                                                    "CDCLK_PLL_ENABLE: PLL Lock") == 1 else 'UNLOCKED'
        pll_ratio = clock_helper_.get_value_by_range(reg_value, 0, 7, '', "PLL Ratio")
        logging.debug("expected cd clk:{0}".format(self.expected_cdclock))

        # check for squashing clock_helper_ condition and get expected CD CLK value
        squash_reg_value = clock_helper_. \
            clock_register_read('CDCLK_SQUASH_CTL_REGISTER', 'CDCLK_SQUASH_CTL', gfx_index)
        squash_enable = clock_helper_ \
            .get_value_by_range(squash_reg_value, 31, 31, '', "squashing enable")

        if squash_enable and self.system_max_cd_clk == 652.8:
            calculated_pll_ratio = 34
            calculated_cd2x_divider = 1
            squash_window_size = clock_helper_ \
                .get_value_by_range(squash_reg_value, 24, 27, '', "squashing enable")
            squash_waveform = clock_helper_ \
                .get_value_by_range(squash_reg_value, 0, 15, '', "squashing enable")

            calculated_squash_waveform = list(self.squash_wave_dict.values())[list(
                self.squash_wave_dict).index(self.expected_cdclock)]

            verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_SQUASH_CTL",
                                                                   parameter=["Squash Window Size", "Squash Waveform"],
                                                                   expected=[15, calculated_squash_waveform],
                                                                   actual=[squash_window_size, squash_waveform])

        else:
            pll_ratio_map = list(self.cdclock_map.values())[list(self.cdclock_map).index(reference_freq)]
            calculated_pll_ratio = list(pll_ratio_map.values())[list(pll_ratio_map).index(self.expected_cdclock)]

            calculated_cd2x_divider_map = \
                list(self.cd2x_divider_map.values())[list(self.cd2x_divider_map).index(reference_freq)]
            calculated_cd2x_divider = list(calculated_cd2x_divider_map.values())[
                list(calculated_cd2x_divider_map).index(self.expected_cdclock)]

        # Divider can be 1 , 1.5  or 2 depending on frequency , so it will not be verified , log it instead
        verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_CTL",
                                                               parameter=["CD2X Div Select", "CD2X Pipe Select"],
                                                               expected=[calculated_cd2x_divider, cd2x_pipe],
                                                               actual=[cd2x_divider, cd2x_pipe])

        # if dc3c0 possible , then HW may dynamically disable CDCLK PLL, so skip this verification
        if not clock_helper_.is_dc3c0_supported(display_port, gfx_index):
            verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_PLL_ENABLE",
                                                                   parameter=["PLL Enable", "PLL Lock", "PLL ratio"],
                                                                   expected=['ENABLED', 'LOCKED', calculated_pll_ratio],
                                                                   actual=[pll_enable_str, pll_lock_str, pll_ratio])

        # -----Get DDI Clock Mapping-------------
        reg_value_DPCLKA_CFGCR0 = clock_helper_.clock_register_read('DPCLKA_CFGCR0_REGISTER', 'DPCLKA_CFGCR0',
                                                                    gfx_index)
        ddi_a_b_clock_map_enabled = {k: v for k, v in self.ddi_clock_map.items() if v & reg_value_DPCLKA_CFGCR0 == 0}
        # TODO Lists out all the active DDIs and compare with the given one
        return verify

    ##
    # @brief        Generic function for getting current cd clock
    # @param[in]    gfx_index: str - Graphics index of Graphics adapter
    # @return       current cd clock
    def get_current_cd_clock(self, gfx_index: str) -> int:
        clock_helper_ = clk_helper.ClockHelper()
        reg_value = clock_helper_.clock_register_read('CDCLK_CTL_REGISTER', 'CDCLK_CTL', gfx_index)
        cdclock_ctl_freq = clock_helper_ \
            .get_value_by_range(reg_value, 0, 10, self.cdclock_ctl_freq_dict, "CDCLK_CTL: CD Frequency Decimal")
        logging.info("INFO : Current CD CLOCK : {0} MHz".format(cdclock_ctl_freq))
        return cdclock_ctl_freq

    ##
    # @brief Generic function for verifying DG2 CD clock
    # @param[in] display_list - List of Display
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_cdclock(self, display_list, gfx_index='gfx_0'):
        clock_helper_ = clk_helper.ClockHelper()
        verify = True
        reg_value = clock_helper_.clock_register_read('CDCLK_CTL_REGISTER', 'CDCLK_CTL', gfx_index)
        cdclock_ctl_freq = clock_helper_ \
            .get_value_by_range(reg_value, 0, 10, self.cdclock_ctl_freq_dict, "CDCLK_CTL: CD Frequency Decimal")

        # if dynamic cd clk is not enabled, just print current cd clk and return
        if not clock_helper_.is_dynamic_cdclock_enabled(gfx_index):
            logging.info("INFO : Dynamic CD Clock NOT Enabled. Current CD CLOCK : {0} MHz".format(cdclock_ctl_freq))
            self.expected_cdclock = cdclock_ctl_freq
            return True

        self.expected_cdclock = self.get_optimal_cdclock(gfx_index, display_list)

        # We can't program cd clk greater than system max cd clk
        if self.expected_cdclock > self.system_max_cd_clk:
            self.expected_cdclock = self.system_max_cd_clk

        verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_CTL & DSSM",
                                                               parameter="Dynamic CD Clock in MHz",
                                                               expected=[self.expected_cdclock],
                                                               actual=[cdclock_ctl_freq])

        return verify

    ##
    # @brief Generic function to get system max cd clk value
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return new_val - System max CD clk value
    def get_system_max_cd_clk(self, gfx_index='gfx_0'):
        clock_helper_ = clk_helper.ClockHelper()
        swf06 = MMIORegister.read('SWF06_REGISTER', 'SWF06', 'SKL', gfx_index='gfx_0')
        max_value = swf06.max_cd_clock_supported
        # on pre-si, swf06 register may not be modeled, and correct value won't be read. Then assume max.
        if max_value == 0:
            reg_value = clock_helper_.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
            reference_freq = clock_helper_ \
                .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")
            if reference_freq == 38.4:
                max_value = 1304  # 652.8 MHz

        if max_value in self.cdclock_ctl_freq_dict.values():
            new_val = list(self.cdclock_ctl_freq_dict)[list(self.cdclock_ctl_freq_dict.values()).index(max_value)]
            return new_val
        else:
            return 0

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
    def get_optimal_cd_clock_from_pixelclock(self, gfx_index: str, max_pixel_rate: float, display_list: list) -> float:
        optimal_cdclock = 0
        clock_helper_ = clk_helper.ClockHelper()
        self.system_max_cd_clk = self.get_system_max_cd_clk(gfx_index)
        max_dsc_slice_one_pixel_clock = clock_helper_.get_max_dsc_slice_1_pixel_clock(gfx_index, display_list)

        # For DSC Displays with Slice Count of 1, Optimal Cd Clock using 2ppc method will not be sufficient to drive the
        # Display as only one DSC Engine will be active and this DSC Engine Clock will be synchronized with the CD Clock
        # not CD Clock x 2. Hence For DSC Displays with Slice Count 1 optimal cd clock will be determined with 1ppc
        # method. For this purpose, pixel clock of dsc display will be multiplied by 2 and the resultant max pixel rate
        # will be used to determine optimal cd clock
        supported_pixel_rate = max(max_pixel_rate, max_dsc_slice_one_pixel_clock * 2)

        is_efp_present = False
        for disp in display_list:
            if display_utility.get_vbt_panel_type(disp, gfx_index) not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI] and \
                    'DP' in disp or 'HDMI' in disp:
                is_efp_present = True
                break
        supported_pixel_rate = clock_helper_.get_calculated_pixel_clock(supported_pixel_rate)

        reg_value = clock_helper_.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
        reference_freq = clock_helper_ \
            .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")
        # Cd Clock values for 38.4 Mhz reference Frequency
        if reference_freq == 38.4:
            # check for squashing enabling condition and get expected CD CLK value
            squash_reg_value = clock_helper_. \
                clock_register_read('CDCLK_SQUASH_CTL_REGISTER', 'CDCLK_SQUASH_CTL', gfx_index)
            squash_enable = clock_helper_ \
                .get_value_by_range(squash_reg_value, 31, 31, '', "squashing enable")
            if self.system_max_cd_clk == 652.8 and squash_enable:
                optimal_cdclock = 163.2 if supported_pixel_rate < 324 else \
                    204 if supported_pixel_rate < 406 else \
                        244.8 if supported_pixel_rate < 488 else \
                            285.6 if supported_pixel_rate < 569 else \
                                326.4 if supported_pixel_rate < 651 else \
                                    367.2 if supported_pixel_rate < 732 else \
                                        408 if supported_pixel_rate < 814 else \
                                            448.8 if supported_pixel_rate < 896 else \
                                                489.6 if supported_pixel_rate < 977 else \
                                                    530.4 if supported_pixel_rate < 1059 else \
                                                        571.2 if supported_pixel_rate < 1140 else \
                                                            612 if supported_pixel_rate < 1222 else 652.8
            elif not squash_enable and is_efp_present:
                optimal_cdclock = self.system_max_cd_clk
            else:
                optimal_cdclock = 172.8 if supported_pixel_rate < 344 else \
                    192 if supported_pixel_rate < 382 else \
                        307.2 if supported_pixel_rate < 612 else \
                            326.4 if supported_pixel_rate < 651 else \
                                556.8 if supported_pixel_rate < 1112 else 652.8
        # Cd Clock values for 19.2 amd 38.4 Mhz Reference Frequency
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][DG2] ERROR: Unsupported Reference frequency {0}".format(
                    reference_freq),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR: Unsupported Reference frequency {0}".format(reference_freq))

        logging.info("Optimal Cd clock: {}MHz".format(optimal_cdclock))
        return optimal_cdclock

    ##
    # @brief        function for calculating optimal cd clock
    # @param[in]    display_list: list
    #                   List of Display
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @return       optimal_cdclock: float
    #                   returns the optimal cd clock in MHz
    def get_optimal_cdclock(self, gfx_index, display_list):
        clock_helper_ = clk_helper.ClockHelper()
        # get bios-programmed max cd clock supported by the system
        self.system_max_cd_clk = self.get_system_max_cd_clk(gfx_index)

        supported_pixel_rate, target_id = clock_helper_.get_max_pixel_rate(display_list, gfx_index, True)

        # Check if the mode is pipe ganged modeset and get the number of pipes required to drive the mode.
        is_pipe_joiner_required, no_of_pipe_required = False, 1
        effective_cd_clock_hz = self.cdclock_ctl_freq_dict[self.system_max_cd_clk] * 1000000
        for disp in display_list:
            logging.info("disp:{}".format(disp))
            is_pipe_joiner_required, no_of_pipe_required = clk_helper.ClockHelper.is_pipe_joiner_required(
                gfx_index, disp, effective_cd_clock_hz)
            if is_pipe_joiner_required is True:
                break

        # Divide the pixel rate by no of pipes to get the correct pixel rate for each of the pipe.
        supported_pixel_rate = supported_pixel_rate / no_of_pipe_required
        logging.debug(f"Pixel Rate Per Pipe={supported_pixel_rate}")

        optimal_cdclock = self.get_optimal_cd_clock_from_pixelclock(gfx_index, supported_pixel_rate, display_list)

        return optimal_cdclock


if __name__ == "__main__":
    clk = Dg2Clock()
    clk.verify_clock('hdmi_b', 'gfx_0')
