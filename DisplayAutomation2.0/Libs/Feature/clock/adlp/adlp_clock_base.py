##
# @file   adlp_clock_base.py
# @brief  Base class for doing ADL-P CD clock and port clock validation
# @author Kruti Vadhavaniya

import logging
from typing import List

from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.adlp import adlp_clock_edp
from Libs.Feature.clock.adlp import adlp_clock_dp_dekelphy
from Libs.Feature.clock.adlp import adlp_clock_hdmi
from Libs.Feature.clock.adlp import adlp_clock_hdmi_dekelphy
from Libs.Feature.clock.adlp import adlp_clock_mipi
from Libs.Core.logger import gdhm

from registers.mmioregister import MMIORegister


##
# @brief ADLP clock verification class for CDCLK and port CLK
class AdlpClock:
    # CD Clock mapping dictionary as per Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/7385
    cdclock_ctl_freq_dict = dict([
        (172.8, 344),
        (176, 350),
        (179.2, 356),
        (192, 382),
        (307.2, 612),
        (312, 622),
        (480, 958),
        (552, 1102),
        (556.8, 1112),
        (648, 1294),
        (652.8, 1304)
    ])

    # DDI values mapping dictionary as in TRANS_DDI_FUNC_CTL register
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

    # DDI PLL mapping dictionary
    ddi_pll_map = dict([
        ('DPLL0', 0),
        ('DPLL1', 1),
        ('DPLL4', 2)
    ])

    # Reference Frequency to Cd Clock map as per bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/7385
    cdclock_map = dict([
        (19.2, dict([(172.8, 27), (192, 20), (307.2, 32), (480, 50), (556.8, 58), (652.8, 68)])),
        (38.4, dict([(179.2, 14), (192, 10), (307.2, 16), (480, 25), (556.8, 29), (652.8, 34)])),
        (24, dict([(176, 22), (192, 16), (312, 26), (480, 40), (552, 46), (648, 54)]))
    ])

    # Reference Frequency to Cd Clock divider map as per bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/7385
    cd2x_divider_map = dict([
        (19.2, dict([(172.8, 1.5), (192, 1), (307.2, 1), (480, 1), (556.8, 1), (652.8, 1)])),
        (38.4, dict([(179.2, 1.5), (192, 1), (307.2, 1), (480, 1), (556.8, 1), (652.8, 1)])),
        (24, dict([(176, 1.5), (192, 1), (312, 1), (480, 1), (552, 1), (648, 1)]))
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

    # CD Clock divider mapping dictionary
    cdclock_divider = dict([
        (1, 0),
        (1.5, 1),
        (2, 2),
        (4, 3)
    ])

    cdclock_ctl_freq = 0
    expected_cdclock = 168

    ##
    # @brief Generic function for verifying ADLP clock
    # @param[in] display_port - Port on which Clock verification need to do
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        clock_helper_ = clk_helper.ClockHelper()
        target_id = clock_helper_.get_target_id(display_port, gfx_index)
        logging.info("******* CD Clock and PLL Verification of Port : {} (Target ID : {}) *******".format(display_port,
                                                                                                          target_id))
        verify = self.verify_sanity(display_port, gfx_index)
        clock = 0
        if str(display_port).upper().__contains__('HDMI'):
            if any(str(display_port).upper() in _ for _ in ['HDMI_A', 'HDMI_B', 'HDMI_C', 'HDMI_D']):
                clock = adlp_clock_hdmi.AdlpClockHdmi()
            else:
                clock = adlp_clock_hdmi_dekelphy.AdlpClockHdmiDekelPhy()
        elif str(display_port).upper().__contains__('DP'):  # Common for eDP and DP
            if any(str(display_port).upper() in _ for _ in ['DP_A', 'DP_B', 'DP_C', 'DP_D']):
                clock = adlp_clock_edp.AdlpClockEdp()
            else:
                clock = adlp_clock_dp_dekelphy.AdlpClockDpDekelPhy()
        elif str(display_port).upper().__contains__('MIPI'):
            clock = adlp_clock_mipi.AdlpClockMipi()
        return verify & clock.verify_clock(display_port, gfx_index)

    ##
    # @brief Verify the generic sanity for clock for all the displays
    # @param[in] display_port - Port on which Clock verification need to do
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_sanity(self, display_port, gfx_index='gfx_0'):
        clock_helper_ = clk_helper.ClockHelper()
        verify = True
        reg_value = clock_helper_.clock_register_read('CDCLK_CTL_REGISTER', 'CDCLK_CTL', gfx_index)
        # Commenting out since Dynamic CD Clk is implemented
        # cdclock_ctl_freq = clock_helper \
        #    .get_value_by_range(reg_value, 0, 10, self.cdclock_ctl_freq_dict, "CDCLK_CTL: CD Frequency Decimal")
        cd2x_divider = clock_helper_.get_value_by_range(reg_value, 22, 23, self.cdclock_divider,
                                                        "CDCLK_CTL: CD2X_Divider_Select")
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
        pll_ratio_map = list(self.cdclock_map.values())[list(self.cdclock_map).index(reference_freq)]
        calculated_pll_ratio = list(pll_ratio_map.values())[list(pll_ratio_map).index(self.expected_cdclock)]

        calculated_cd2x_divider_map = \
            list(self.cd2x_divider_map.values())[list(self.cd2x_divider_map).index(reference_freq)]
        calculated_cd2x_divider = list(calculated_cd2x_divider_map.values())[
            list(calculated_cd2x_divider_map).index(self.expected_cdclock)]

        verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_CTL",
                                                               parameter=["CD2X Div Select", "CD2X Pipe Select"],
                                                               expected=[calculated_cd2x_divider, cd2x_pipe],
                                                               actual=[cd2x_divider, cd2x_pipe])

        # if dc3c0 possible , then HW may dynamically disable CDCLK PLL, so skip this verification
        if not clock_helper_.is_dc3c0_supported(display_port, gfx_index):
            verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_PLL_ENABLE",
                                                                   parameter=["PLL Enable", "PLL Lock", "PLL Ratio"],
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
    def get_current_cd_clock(self, gfx_index: str):
        clock_helper_ = clk_helper.ClockHelper()
        reg_value = clock_helper_.clock_register_read('CDCLK_CTL_REGISTER', 'CDCLK_CTL', gfx_index)
        cdclock_ctl_freq = clock_helper_ \
            .get_value_by_range(reg_value, 0, 10, self.cdclock_ctl_freq_dict, "CDCLK_CTL: CD Frequency Decimal")
        logging.info("INFO : Current CD CLOCK : {0} MHz".format(cdclock_ctl_freq))
        return cdclock_ctl_freq

    ##
    # @brief Generic function for verifying ADLP CD clock
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
            self.expected_cdclock = self.get_system_max_cd_clk(gfx_index)
            verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_CTL & DSSM",
                                                                   parameter="Dynamic CD Clock in MHz",
                                                                   expected=[self.expected_cdclock],
                                                                   actual=[cdclock_ctl_freq])
            return verify

        system_max_cd_clk = self.get_system_max_cd_clk(gfx_index)
        self.expected_cdclock = self.get_optimal_cdclock(gfx_index, display_list)

        # We can't program cd clk greater than system max cd clk
        if self.expected_cdclock > system_max_cd_clk:
            self.expected_cdclock = system_max_cd_clk

        verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_CTL & DSSM",
                                                               parameter="Dynamic CD Clock in MHz",
                                                               expected=[self.expected_cdclock],
                                                               actual=[cdclock_ctl_freq])

        return verify

    ##
    # @brief Generic function to get system max cd clk value
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return System max cd clk value in MHz
    def get_system_max_cd_clk(self, gfx_index='gfx_0'):

        clock_helper_ = clk_helper.ClockHelper()
        swf06 = MMIORegister.read('SWF06_REGISTER', 'SWF06', 'SKL', gfx_index=gfx_index)
        max_value = swf06.max_cd_clock_supported
        # on pre-si, swf06 register may not be modeled, and correct value won't be read. Then assume max.
        if max_value == 0:
            reg_value = clock_helper_.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
            reference_freq = clock_helper_ \
                .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")
            if reference_freq == 19.2 or reference_freq == 38.4:
                max_value = 1304  # 652.8 MHz
            elif reference_freq == 24:
                max_value = 1294  # 648 MHz

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
        optimal_cdclock: float = 0
        clock_helper_ = clk_helper.ClockHelper()
        reg_value = clock_helper_.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
        reference_freq = clock_helper_ \
            .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")
        max_dsc_slice_one_pixel_clock = clock_helper_.get_max_dsc_slice_1_pixel_clock(gfx_index, display_list)
        # For DSC Displays with Slice Count of 1, Optimal Cd Clock using 2ppc method will not be sufficient to drive the
        # Display as only one DSC Engine will be active and this DSC Engine Clock will be synchronized with the CD Clock
        # not CD Clock x 2. Hence, For DSC Displays with Slice Count 1 optimal cd clock will be determined with 1ppc
        # method. For this purpose, pixel clock of dsc display will be multiplied by 2 and the resultant max pixel rate
        # will be used to determine optimal cd clock
        supported_pixel_rate = max(max_pixel_rate, max_dsc_slice_one_pixel_clock * 2)

        supported_pixel_rate = clock_helper_.get_calculated_pixel_clock(supported_pixel_rate)
        logging.info(f"Max supported Pixel Rate={supported_pixel_rate}")

        # Note: Added WA for CD clock calculation w.r.t. precision mismatch in boundary conditions
        # Cd Clock values for 24 Mhz reference Frequency
        if reference_freq == 24:
            optimal_cdclock = 176 if supported_pixel_rate < 350 else \
                192 if supported_pixel_rate < 382 else \
                    312 if supported_pixel_rate < 622 else \
                        480 if clk_helper.ClockHelper.is_480_mhz_supported(gfx_index) and \
                               supported_pixel_rate < 958 else \
                            552 if supported_pixel_rate < 1102 else 648
        # Cd Clock values for 19.2 Reference Frequency
        elif reference_freq == 19.2:
            optimal_cdclock = 172.8 if supported_pixel_rate < 344 else \
                192 if supported_pixel_rate < 382 else \
                    307.2 if supported_pixel_rate < 612 else \
                        480 if clk_helper.ClockHelper.is_480_mhz_supported(gfx_index) and \
                               supported_pixel_rate < 958 else \
                            556.8 if supported_pixel_rate < 1112 else 652.8
        # Cd Clock values for 38.4 Reference Frequency
        elif reference_freq == 38.4:
            optimal_cdclock = 179.2 if supported_pixel_rate < 356 else \
                192 if supported_pixel_rate < 382 else \
                    307.2 if supported_pixel_rate < 612 else \
                        480 if clk_helper.ClockHelper.is_480_mhz_supported(gfx_index) and \
                               supported_pixel_rate < 958 else \
                            556.8 if supported_pixel_rate < 1112 else 652.8
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][ADLP] Failed: reference_freq:{} not supported".format(
                    reference_freq),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Fail: reference_freq:{} not supported".format(reference_freq))

        logging.info("Optimal Cd clock: {}MHz".format(optimal_cdclock))
        return optimal_cdclock

    ##
    # @brief        function for calculating optimal cd clock
    # @param[in]    display_list: List
    #                   Active displays list
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @return       optimal_cdclock: float
    #                   returns the optimal cd clock in MHz
    def get_optimal_cdclock(self, gfx_index: str, display_list: List[str]) -> float:
        clock_helper_ = clk_helper.ClockHelper()
        # get bios-programmed max cd clock supported by the system
        system_max_cd_clk = self.get_system_max_cd_clk(gfx_index)

        # Check if the mode is pipe ganged modeset and get the number of pipes required to drive the mode.
        is_pipe_joiner_required, no_of_pipe_required, pipe_joiner_ports = False, 1, {}
        effective_cd_clock_hz = self.cdclock_ctl_freq_dict[system_max_cd_clk] * 1000000
        for port_name in display_list:
            logging.info(f"Port name: {port_name}")
            is_pipe_joiner_required, no_of_pipe_required = clock_helper_.is_pipe_joiner_required(gfx_index, port_name,
                                                                                                 effective_cd_clock_hz)
            if is_pipe_joiner_required is True:
                pipe_joiner_ports[port_name] = {'gfx_index': gfx_index, 'no_of_pipe_required': no_of_pipe_required}

        supported_pixel_rate, target_id = clock_helper_.get_max_pixel_rate(display_list, gfx_index, True,
                                                                           pipe_joiner_ports)
        optimal_cdclock = self.get_optimal_cd_clock_from_pixelclock(gfx_index, supported_pixel_rate, display_list)

        return optimal_cdclock


if __name__ == "__main__":
    clk = AdlpClock()
    clk.verify_clock('hdmi_b', 'gfx_0')
