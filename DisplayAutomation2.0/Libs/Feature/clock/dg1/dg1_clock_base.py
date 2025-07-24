##
# @file   dg1_clock_base.py
# @brief  Base class for doing DG1 CD clock and port clock validation
# @author Kruti Vadhavaniya


import logging

from Libs.Core import display_utility
from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.dg1 import dg1_clock_edp
from Libs.Feature.clock.dg1 import dg1_clock_hdmi
from Libs.Core.logger import gdhm
from registers.mmioregister import MMIORegister


##
# @brief DG1 clock verification class for CDCLK and port CLK
class Dg1Clock:
    # CD Clock map as per Bspec Ref: https://gfxspecs.intel.com/Predator/Home/Index/33869
    cdclock_ctl_freq_dict = dict([
        (168, 334),
        (172.8, 344),
        (180, 358),
        (192, 382),
        (307.2, 612),
        (312, 622),
        (324, 646),
        (326.4, 651),
        (552, 1102),
        (556.8, 1112),
        (648, 1294),
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
        (38.4, dict([(9, 172.8), (10, 192), (16, 307.2), (29, 556.8), (34, [326.4, 652.8])]))
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

    cdclock_ctl_freq = 0

    ##
    # @brief Generic function for verifying DG1 clock
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
            clock = dg1_clock_hdmi.Dg1ClockHdmi()
        elif str(display_port).upper().__contains__('DP'):  # for both edp and DP
            clock = dg1_clock_edp.Dg1ClockEdp()
        return verify & clock.verify_clock(display_port, gfx_index)

    ##
    # @brief Verify the generic sanity for clock for all the displays
    # @param[in] display_port - Display Port on which Clock verification need to do
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_sanity(self, display_port, gfx_index='gfx_0'):
        verify = True
        clock_helper_ = clk_helper.ClockHelper()
        reg_value = clock_helper_.clock_register_read('CDCLK_CTL_REGISTER', 'CDCLK_CTL', gfx_index)
        # Commenting out since Dynamic CD Clk is implemented
        # cdclock_ctl_freq = clock_helper \
        #    .get_value_by_range(reg_value, 0, 10, self.cdclock_ctl_freq_dict, "CDCLK_CTL: CD Frequency Decimal")
        cd2x_divider = clock_helper_.get_value_by_range(reg_value, 22, 23, '', "CDCLK_CTL: CD2X_Divider_Select")
        cd2x_divider_str = 'Div by 1' if cd2x_divider == 0 else 'Div by 2'
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
        pll_ratio_map = list(self.cdclock_map.values())[list(self.cdclock_map).index(reference_freq)]
        calculated_cdclock = list(pll_ratio_map.values())[list(pll_ratio_map).index(pll_ratio)]

        if isinstance(calculated_cdclock, list):
            # More than 1 CD_clock frequency possible with this pll ratio, CD2x divider maybe 1 or 2
            # depending on actual frequency
            # Hence , test logs the divider data but no verification will be done
            verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_CTL",
                                                                   parameter=["CD2X Div Select", "CD2X Pipe Select"],
                                                                   expected=[cd2x_divider_str, cd2x_pipe],
                                                                   actual=[cd2x_divider_str, cd2x_pipe])
        else:
            # CD 2x divider expected to be 1 for other pll ratios , so check if cd2x divider is set to 1
            verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_CTL",
                                                                   parameter=["CD2X Div Select", "CD2X Pipe Select"],
                                                                   expected=['Div by 1', cd2x_pipe],
                                                                   actual=[cd2x_divider_str, cd2x_pipe])

        # if dc3c0 possible , then HW may dynamically disable CDCLK PLL, so skip this verification
        if not clock_helper_.is_dc3c0_supported(display_port, gfx_index):
            verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_PLL_ENABLE",
                                                                   parameter=["PLL Enable", "PLL Lock"],
                                                                   expected=['ENABLED', 'LOCKED'],
                                                                   actual=[pll_enable_str, pll_lock_str])

        # -----Get DDI Clock Mapping-------------
        reg_value_DPCLKA0_CFGCR0 = clock_helper_.clock_register_read('DPCLKA0_CFGCR0_REGISTER', 'DPCLKA0_CFGCR0',
                                                                     gfx_index)
        reg_value_DPCLKA1_CFGCR0 = clock_helper_.clock_register_read('DPCLKA1_CFGCR0_REGISTER', 'DPCLKA1_CFGCR0',
                                                                     gfx_index)
        ddi_a_b_clock_map_enabled = {k: v for k, v in self.ddi_clock_map.items() if v & reg_value_DPCLKA0_CFGCR0 == 0}
        ddi__c_d_clock_map_enabled = {k: v for k, v in self.ddi_clock_map.items() if v & reg_value_DPCLKA1_CFGCR0 == 0}
        # TODO Lists out all the active DDIs and compare with the given one
        return verify

    ##
    # @brief Generic function for verifying DG1 CD clock
    # @param[in] display_list - List of Display
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_cdclock(self, display_list, gfx_index='gfx_0'):
        verify = True
        clock_helper_ = clk_helper.ClockHelper()
        reg_value = clock_helper_.clock_register_read('CDCLK_CTL_REGISTER', 'CDCLK_CTL', gfx_index)
        cdclock_ctl_freq = clock_helper_ \
            .get_value_by_range(reg_value, 0, 10, self.cdclock_ctl_freq_dict, "CDCLK_CTL: CD Frequency Decimal")

        # if dynamic cd clk is not enabled in VBT, just print current cd clk and return
        if not clock_helper_.is_dynamic_cdclock_enabled(gfx_index):
            logging.info("INFO : Dynamic CD Clock NOT Enabled.Skip Current CD CLOCK : {0} MHz".format(cdclock_ctl_freq))
            return True

        # get bios-programmed max cd clock supported by the system
        system_max_cd_clk = self.get_system_max_cd_clk(gfx_index)

        expected_cdclock = self.get_optimal_cdclock(gfx_index, display_list)
        # We can't program cd clk greater than system max cd clk
        if expected_cdclock > system_max_cd_clk:
            expected_cdclock = system_max_cd_clk

        verify &= clock_helper_.verify_cd_clock_programming_ex(feature="CDCLK_CTL & DSSM",
                                                               parameter="Dynamic CD Clock in MHz",
                                                               expected=[expected_cdclock], actual=[cdclock_ctl_freq])

        return verify

    ##
    # @brief Generic function to get system max cd clk value
    # @param[in] gfx_index - Graphics index of Graphics adapter
    # @return new_val - System Max CD clock in MHz
    def get_system_max_cd_clk(self, gfx_index='gfx_0'):

        clock_helper_ = clk_helper.ClockHelper()
        swf06 = MMIORegister.read('SWF06_REGISTER', 'SWF06', 'SKL', gfx_index=gfx_index)
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
    # @brief        function for calculating optimal cd clock
    # @param[in]    display_list: list
    #                   List of Display
    # @param[in]    gfx_index: str
    #                   Graphics index of Graphics adapter
    # @return       optimal_cdclock: float
    #                   returns the optimal cd clock in MHz
    def get_optimal_cdclock(self, gfx_index, display_list):
        optimal_cdclock = 0
        clock_helper_ = clk_helper.ClockHelper()
        # get bios-programmed max cd clock supported by the system
        system_max_cd_clk = self.get_system_max_cd_clk(gfx_index)

        # get max supported pixel rate from list of active displays
        supported_pixel_rate = clock_helper_.get_max_pixel_rate(display_list, gfx_index)
        max_dsc_slice_one_pixel_clock = clock_helper_.get_max_dsc_slice_1_pixel_clock(gfx_index, display_list)

        # For DSC Displays with Slice Count of 1, Optimal Cd Clock using 2ppc method will not be sufficient to drive the
        # Display as only one DSC Engine will be active and this DSC Engine Clock will be synchronized with the CD Clock
        # not CD Clock x 2. Hence For DSC Displays with Slice Count 1 optimal cd clock will be determined with 1ppc
        # method. For this purpose, pixel clock of dsc display will be multiplied by 2 and the resultant max pixel rate
        # will be used to determine optimal cd clock
        supported_pixel_rate = max(supported_pixel_rate, max_dsc_slice_one_pixel_clock * 2)

        # Check if the mode is pipe ganged modeset and get the number of pipes required to drive the mode.
        is_pipe_joiner_required, no_of_pipe_required = False, 1
        effective_cd_clock_hz = self.cdclock_ctl_freq_dict[system_max_cd_clk] * 1000000
        for disp in display_list:
            logging.info("disp:{}".format(disp))
            is_pipe_joiner_required, no_of_pipe_required = clk_helper.ClockHelper.is_pipe_joiner_required(
                gfx_index, disp, effective_cd_clock_hz)
            if is_pipe_joiner_required is True:
                break
        # Divide the pixel rate by no of pipes to get the correct pixel rate for each of the pipe.
        supported_pixel_rate = supported_pixel_rate / no_of_pipe_required

        is_efp_present = False

        for disp in display_list:
            if display_utility.get_vbt_panel_type(disp, gfx_index) not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI] and \
                    'DP' in disp or 'HDMI' in disp:
                is_efp_present = True
                break

        # if EFPs present in current display configuration, maxcdclock/2 feature is only supported
        if is_efp_present is True:
            if system_max_cd_clk in [648, 652.8]:
                optimal_cdclock = system_max_cd_clk / 2 if supported_pixel_rate < system_max_cd_clk \
                    else system_max_cd_clk
            else:
                optimal_cdclock = system_max_cd_clk
        else:  # if only LFPs present in current display configuration, dynamic cd clock switching is supported
            reg_value = clock_helper_.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
            reference_freq = clock_helper_ \
                .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")
            if reference_freq == 38.4:
                optimal_cdclock = 172.8 if supported_pixel_rate < 344 else \
                                  192 if supported_pixel_rate < 382 else \
                                  307.2 if supported_pixel_rate < 612 else \
                                  326.4 if supported_pixel_rate < 651 else \
                                  556.8 if supported_pixel_rate < 1112 else 652.8
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][DG1] ERROR: Unsupported Reference frequency {0}".format(
                        reference_freq),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("ERROR: Unsupported Reference frequency {0}".format(reference_freq))

        logging.info("Optimal Cd clock: {}MHz".format(optimal_cdclock))
        return optimal_cdclock


if __name__ == "__main__":
    clk = Dg1Clock()
    clk.verify_clock('hdmi_b', 'gfx_0')
