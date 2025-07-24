##
# @file   adlp_clock_mipi.py
# @brief  Python class to validate MIPI DPLL divider values are programmed correctly
# @author Kruti, Vadhavaniya

import logging

import math
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.adlp import adlp_clock_registers
from Libs.Core.logger import gdhm

clock_helper = clk_helper.ClockHelper()
adlp_clock_reg = adlp_clock_registers.AdlpClockRegisters()


##
# @brief Clock register class
class ClockRegister():
    DPLL_CFGCR0 = ''
    DPLL_CFGCR1 = ''
    DPLL_SSC = ''


##
# @brief HDMI Clock class
class MipiClock():
    PDIV = 0
    KDIV = 0
    QDIV = 0
    DCO_INT = 0
    DCO_FRAC = 0
    SSC_ENABLE = 0


##
# @brief ADLP Port clock verification class for MIPI display
class AdlpClockMipi():
    # Map of CD Clock frequency
    cdclock_ctl_freq_dict = dict([
        (168, 334),
        (307.2, 612),
        (312, 622),
        (552, 1102),
        (556.8, 1112),
        (648, 1294),
        (652.8, 1304)
    ])

    # Map of possible PDIV values
    pdiv_map = dict([
        (2, 1),
        (3, 2),
        (5, 4),
        (7, 8)
    ])
    # Map of possible PDIV values
    kdiv_map = dict([
        (1, 1),
        (2, 2),
        (3, 4)
    ])
    # Map of DDI to clock mapping
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
    # Map of DPLL
    ddi_pll_map = dict([
        ('DPLL0', 0),
        ('DPLL1', 1),
        ('DPLL4', 2)
    ])
    # Map of Bit per color
    bit_per_color = dict([
        (8, 0),
        (10, 1),
        (6, 2),
        (12, 3)
    ])
    # Map of color format
    color_format = dict([
        ('RGB', 0),
        ('YUV420', 1)
    ])
    # Mapping of the listed Reference Frequencies
    dssm_ref_freq_map = dict([
        (24, 0),
        (19.2, 1),
        (38.4, 2),
        (25, 3)
    ])
    # Mapping of central freq
    central_freq_dict = dict([
        (9600, 0),
        (9000, 1),
        (8400, 3)
    ])
    # Mapping of pixel format
    pixel_format_map = dict([
        (16, 0),
        (18, 1),
        (24, 3),
        (30, 4),
        (36, 5)
    ])

    cdclock_ctl_freq = 0
    symbol_freq = 0
    # Array of all possible divider values
    dividerlist = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 30, 32, 36, 40,
                   42, 44, 48, 50, 52, 54, 56, 60, 64, 66, 68, 70, 72, 76, 78,
                   80, 84, 88, 90, 92, 96, 98, 100, 102, 3, 5, 7, 9, 15, 21]

    Pdiv = 0
    Kdiv = 0
    Qdiv = 0
    bpp = 0
    lane_count = 0
    esc_clock_divider = 0

    ##
    # @brief function to validate MIPI clock.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        reg_value = clock_helper.clock_register_read('DPCLKA_CFGCR0_REGISTER', 'DPCLKA_CFGCR0', gfx_index)
        dpllValue = clock_helper.get_value_by_range(reg_value, 2, 3, self.ddi_pll_map, 'DPLL') if str(
            display_port).upper() in ['MIPI_B', 'MIPI_C'] else clock_helper.get_value_by_range(reg_value, 0, 1,
                                                                                               self.ddi_pll_map, 'DPLL')

        adlp_clock_reg.verify_pll_enable(display_port, dpllValue, gfx_index)

        ClockRegister.DPLL_CFGCR0 = dpllValue + '_CFGCR0'
        ClockRegister.DPLL_CFGCR1 = dpllValue + '_CFGCR1'
        ClockRegister.DPLL_SSC = dpllValue + '_SSC'

        return self.ValidateDPll(display_port, gfx_index)

    ##
    # @brief function to validate MIPI DPLL divider values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def ValidateDPll(self, display_port, gfx_index='gfx_0'):
        self.set_lane_values(display_port, gfx_index)
        regValue = clock_helper.clock_register_read('DPLL_CFGCR0_REGISTER', ClockRegister.DPLL_CFGCR0, gfx_index)
        reg_DPLL_SSC = clock_helper.clock_register_read('DPLL_SSC_REGISTER', ClockRegister.DPLL_SSC, gfx_index)
        reg_read_mipi = MipiClock()
        reg_read_mipi.DCO_INT = clock_helper.get_value_by_range(regValue, 0, 9, '', 'DCO Integer')
        reg_read_mipi.DCO_FRAC = clock_helper.get_value_by_range(regValue, 10, 24, '', 'DCO Fraction')
        reg_read_mipi.SSC_ENABLE = clock_helper.get_value_by_range(reg_DPLL_SSC, 9, 9, '', 'SSC Enable')

        regValue = clock_helper.clock_register_read('DPLL_CFGCR1_REGISTER', ClockRegister.DPLL_CFGCR1, gfx_index)
        reg_read_mipi.PDIV = clock_helper.get_value_by_range(regValue, 2, 5, self.pdiv_map, 'PDiv')
        reg_read_mipi.KDIV = clock_helper.get_value_by_range(regValue, 6, 8, self.kdiv_map, 'KDiv')
        div_value2 = clock_helper.get_value_by_range(regValue, 9, 9, '', 'QDiv')
        if div_value2 == 0:
            reg_read_mipi.QDIV = 1
        else:
            reg_read_mipi.QDIV = clock_helper.get_value_by_range(regValue, 10, 17, '', 'QDiv')
        central_frequency = clock_helper.get_value_by_range(regValue, 0, 1, self.central_freq_dict, 'Central_frequency')

        self.calculate_symbol_freq(display_port, gfx_index)

        ##
        # check platform
        self.machine_info = SystemInfo()
        gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
        # WA : currently test are execute on single platform. so loop break after 1 st iteration.
        # once Enable MultiAdapter remove the break statement.
        for i in range(len(gfx_display_hwinfo)):
            if str(gfx_display_hwinfo[i].gfxIndex).lower() == gfx_index:
                self.platform = ("%s" % gfx_display_hwinfo[i].DisplayAdapterName).lower()
                break

        adapter_info = clock_helper.get_adapter_info(display_port, gfx_index)
        mode = DisplayConfiguration().get_current_mode(adapter_info)
        link_frequency = (mode.pixelClock_Hz * self.bpp) / self.lane_count

        n_div_total = math.ceil(link_frequency / (19 * 8 * 1000000))  # Assuming escape clock of 19MHz as per Bspec)
        n_div_actual = max(3, n_div_total + (n_div_total + 1) % 2)

        self.esc_clock_divider_for_dphy = n_div_actual * 8
        self.esc_clock_divider_for_combophy = (n_div_actual - 1) / 2

        if display_port == 'MIPI_A':
            regValue = clock_helper.clock_register_read('DSI_ESC_CLK_DIV_REGISTER', 'DSI_ESC_CLK_DIV_DSI0', gfx_index)
        if display_port == 'MIPI_C':
            regValue = clock_helper.clock_register_read('DSI_ESC_CLK_DIV_REGISTER', 'DSI_ESC_CLK_DIV_DSI1', gfx_index)
        dsi_esc_div = clock_helper.get_value_by_range(regValue, 0, 8, '', 'escape_clock_divider_m')

        if display_port == 'MIPI_A':
            regValue = clock_helper.clock_register_read('DPHY_ESC_CLK_DIV_REGISTER', 'DPHY_ESC_CLK_DIV_0', gfx_index)
        if display_port == 'MIPI_C':
            regValue = clock_helper.clock_register_read('DPHY_ESC_CLK_DIV_REGISTER', 'DPHY_ESC_CLK_DIV_1', gfx_index)
        dphy_esc_div = clock_helper.get_value_by_range(regValue, 0, 8, '', 'escape_clock_divider_m')

        regValue = clock_helper.clock_register_read('MIPIO_DW8_REGISTER', 'MIPIO_DW8_' + display_port, gfx_index)
        physical_esc_clock_div = clock_helper.get_value_by_range(regValue, 16, 23, '', 'escape_clock_divider_m')

        calculated_pll_freq = self.calculate_best_dco_freq()
        logging.debug("INFO : Calculated PLL Frequency = {0}".format(str(calculated_pll_freq)))
        logging.debug("INFO : DPLL0_CFGCR0 - DCO_Fraction_value = {0} & DCO_Integer_value = {1}".format(
            str(reg_read_mipi.DCO_FRAC), str(reg_read_mipi.DCO_INT)))

        reg_value = clock_helper.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
        reference_frequency = clock_helper \
            .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")

        # If reference freq is 38.4, treat it as 19.2
        if reference_frequency == 38.4:
            logging.debug("INFO : Reference Frequency is {0}. Using 19.2 Instead".format(str(reference_frequency)))
            reference_frequency = 19.2
        logging.info("INFO : Reference Frequency is {0}MHz.".format(str(reference_frequency)))
        calculated_dco = calculated_pll_freq * (self.Pdiv * self.Kdiv * self.Qdiv)
        expected_dco_int = int(calculated_pll_freq * (self.Pdiv * self.Kdiv * self.Qdiv) / reference_frequency)
        expected_dco_frac = int(
            (calculated_dco / reference_frequency - int(calculated_dco / reference_frequency)) * 2 ** 15)

        if reference_frequency == 19.2:
            expected_dco_frac = int(expected_dco_frac / 2)

        ret = clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_CFGCR0),
                                                            parameter=['DCO Integer', 'DCO Fraction'],
                                                            expected=[expected_dco_int, expected_dco_frac],
                                                            actual=[reg_read_mipi.DCO_INT, reg_read_mipi.DCO_FRAC])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_SSC),
                                                             parameter=['SSC Enable'],
                                                             expected=[0], actual=[reg_read_mipi.SSC_ENABLE])

        ret &= clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_CFGCR1),
                                                             parameter=['PDiv', 'KDiv', 'QDiv Mode'],
                                                             expected=[self.Pdiv, self.Kdiv, self.Qdiv],
                                                             actual=[reg_read_mipi.PDIV, reg_read_mipi.KDIV,
                                                                reg_read_mipi.QDIV])

        ret &= clock_helper.verify_port_clock_programming_ex(feature="DSI_ESC_CLK_DIV_DSI0 & DSI1",
                                                             parameter="Escape Clock Divider M",
                                                             expected=[int(self.esc_clock_divider_for_dphy)],
                                                             actual=[dsi_esc_div])

        ret &= clock_helper.verify_port_clock_programming_ex(feature="DPHY_ESC_CLK_DIV_0",
                                                             parameter="Escape Clock Divider M",
                                                             expected=[int(self.esc_clock_divider_for_dphy)],
                                                             actual=[dphy_esc_div])

        ret &= clock_helper.verify_port_clock_programming_ex(feature="MIPIO_DW8", parameter="Escape Clock Divider M",
                                                             expected=[int(self.esc_clock_divider_for_combophy)],
                                                             actual=[physical_esc_clock_div])

        if (central_frequency != 8400):
            logging.warning("{res:^5}: {feature:<60}: Expected: {exp:<20}  Actual: [{act}]".format(res="WARN",
                                                                                                   feature="DPCLKA_CFGCR0 & {} - Central Frequency in MHz".format(
                                                                                                       ClockRegister.DPLL_CFGCR1),
                                                                                                   exp="[{0}]".format(
                                                                                                       '8400'), act=str(
                    central_frequency)))
        else:
            ret &= clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_CFGCR1),
                                                                 parameter="Central Frequency in MHz",
                                                                 expected=['8400'], actual=[str(central_frequency)])

        driver_dco_freq = reg_read_mipi.DCO_INT * reference_frequency
        driver_pll_frequency = driver_dco_freq / (reg_read_mipi.PDIV * reg_read_mipi.KDIV * reg_read_mipi.QDIV)

        if abs(calculated_pll_freq - driver_pll_frequency) > reference_frequency / (
                reg_read_mipi.PDIV * reg_read_mipi.KDIV * reg_read_mipi.QDIV * 2):
            logging.warning("WARN: {0}: Current Value = {1} MHz Greater than 1 MHz of Expected Value {2} MHz".format(
                'Driver PLL Frequency', str(driver_pll_frequency), str(calculated_pll_freq)))
            return ret
        else:
            logging.debug("PASS: {0}: Current Value = {1} MHz Less than 1 MHz of Expected Value {2} MHz".format(
                'Driver PLL Frequency', str(driver_pll_frequency), str(calculated_pll_freq)))
            return ret

    ##
    # @brief function to find the Symbol Frequency for MIPI
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return Symbol Frequency in MHz
    def calculate_symbol_freq(self, display_port, gfx_index='gfx_0'):
        self.symbol_freq = clock_helper.get_pixel_rate(display_port, gfx_index)
        logging.info("INFO : MIPI 8X = Pixel Rate = {0}MHz".format(str(self.symbol_freq)))

    ##
    # @brief Calculate the best DCO Frequency for MIPI
    # @return DCO Frequency in MHz
    def calculate_best_dco_freq(self):
        dco_min = 7998
        dco_max = 10000
        afe_multiplier = self.bpp / self.lane_count
        dco_mid = (dco_max + dco_min) / 2
        logging.debug("INFO : Mid Frequency = {0}".format(dco_mid))
        dividerlist_new = list(filter(lambda x: ((x * afe_multiplier * self.symbol_freq) < dco_max)
                                                and ((x * afe_multiplier * self.symbol_freq) > dco_min)
                                      , self.dividerlist))
        best_freq_dict = dict(
            [(key, abs((key * afe_multiplier * self.symbol_freq) - dco_mid)) for key in dividerlist_new])
        best_key = list(best_freq_dict)[list(best_freq_dict.values()).index(sorted(best_freq_dict.values())[0])]
        best_dco = best_key * afe_multiplier * self.symbol_freq
        self.get_div_values(best_key)
        return best_dco / best_key

    ##
    # @brief Find the Divider Values
    # @param[in] bestdiv - best division value
    # @return Boot True or False
    def get_div_values(self, bestdiv):
        if bestdiv != 0:
            if bestdiv % 2 == 0:  # Even
                if bestdiv == 2:
                    self.Pdiv = 2
                    self.Qdiv = 1
                    self.Kdiv = 1
                elif bestdiv % 4 == 0:
                    self.Pdiv = 2
                    self.Qdiv = bestdiv / 4
                    self.Kdiv = 2
                elif bestdiv % 6 == 0:
                    self.Pdiv = 3
                    self.Qdiv = bestdiv / 6
                    self.Kdiv = 2
                elif bestdiv % 5 == 0:
                    self.Pdiv = 5
                    self.Qdiv = bestdiv / 10
                    self.Kdiv = 2
                elif bestdiv % 14 == 0:
                    self.Pdiv = 7
                    self.Qdiv = bestdiv / 14
                    self.Kdiv = 2
            else:  # odd
                if bestdiv == 3 or bestdiv == 5 or bestdiv == 7:
                    self.Pdiv = bestdiv
                    self.Qdiv = 1
                    self.Kdiv = 1
                else:  # 9, 15, 21
                    self.Pdiv = bestdiv / 3
                    self.Qdiv = 1
                    self.Kdiv = 3
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]ADLP_Clock_MIPI: Best divider value not found while calculating the "
                      "best DCO Frequency",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Best Divider Value NOT Found")
            return False
        return True

    ##
    # @brief function to set lane values
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return None
    def set_lane_values(self, display_port, gfx_index='gfx_0'):
        dsi_value = ''
        reg_value = 0
        if display_port == 'MIPI_A':
            dsi_value = 'DSI0'
            reg_value = clock_helper.clock_register_read('TRANS_DSI_FUNC_CONF_REGISTER',
                                                         'TRANS_DSI_FUNC_CONF_DSI0', gfx_index)
        else:
            dsi_value = 'DSI1'
            reg_value = clock_helper.clock_register_read('TRANS_DSI_FUNC_CONF_REGISTER',
                                                         'TRANS_DSI_FUNC_CONF_DSI1', gfx_index)
        self.bpp = clock_helper \
            .get_value_by_range(reg_value, 16, 18, self.pixel_format_map, "Pixel Format")
        reg_value = clock_helper.clock_register_read('TRANS_DDI_FUNC_CTL_REGISTER', 'TRANS_DDI_FUNC_CTL_'+dsi_value, gfx_index)
        self.lane_count = clock_helper \
                              .get_value_by_range(reg_value, 1, 3, '', "Port Width Selection") + 1


if __name__ == "__main__":
    clk = AdlpClockMipi()
    clk.ValidateDPll(0, 'gfx_0')
