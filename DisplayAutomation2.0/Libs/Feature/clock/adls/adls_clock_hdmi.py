##
# @file   adls_clock_hdmi.py
# @brief  Python class to validate HDMI DPLL divider values are programmed correctly
# @author Kruti, Vadhavaniya

import logging

from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.adls import adls_clock_registers
from Libs.Core.logger import gdhm


clock_helper = clk_helper.ClockHelper()
adls_clock_reg = adls_clock_registers.AdlsClockRegisters()


##
# @brief Clock register class
class ClockRegister():
    DPLL_CFGCR0 = ''
    DPLL_CFGCR1 = ''
    DPLL_SSC = ''


##
# @brief HDMI Clock class
class HdmiClock():
    PDIV = 0
    KDIV = 0
    QDIV = 0
    DCO_INT = 0
    DCO_FRAC = 0
    SSC_ENABLE = 0


##
# @brief ADLS port clock verification class for HDMI display
class AdlsClockHdmi():
    # Color Format to BPP map
    colorFormatDictionary = dict([('RGB_8', 1), ('RGB_10', 1.25),
                                  ('RGB_12', 1.5), ('YUV420_8', 0.5),
                                  ('YUV420_10', 0.625), ('YUV420_12', 0.75)])

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
    # Mapping of the listed DPLLs that can be used
    ddi_pll_map = dict([
        ('DPLL0', 0),
        ('DPLL1', 1),
        ('DPLL4', 2),  # Need update from Bspec also
        ('DPLL3', 3)
    ])
    # Mapping of bit per color
    bit_per_color = dict([
        (8, 0),
        (10, 1),
        (6, 2),
        (12, 3)
    ])

    color_format = dict([
        ('RGB', 0),
        ('YUV420', 1)
    ])
    # Mapping of the listed Reference Frequencies
    dssm_ref_freq_map = dict([
        (24, 0),
        (19.2, 1),
        (38.4, 2)
    ])
    # Mapping of color format
    central_freq_dict = dict([
        (9600, 0),
        (9000, 1),
        (8400, 3)
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

    ##
    # @brief function to validate HDMI clock.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        status = False
        reg_value_DPCLKA_CFGCR0 = clock_helper.clock_register_read('DPCLKA_CFGCR0_REGISTER', 'DPCLKA_CFGCR0')
        reg_value_DPCLKA_CFGCR1 = clock_helper.clock_register_read('DPCLKA_CFGCR1_REGISTER', 'DPCLKA_CFGCR1')
        dpllValue = clock_helper.get_value_by_range(reg_value_DPCLKA_CFGCR0, 0, 1, self.ddi_pll_map, 'DPLL') if str(
            display_port).upper().__contains__('HDMI_A') else clock_helper.get_value_by_range(reg_value_DPCLKA_CFGCR0,
                                                                                              2, 3,
                                                                                              self.ddi_pll_map,
                                                                                              'DPLL') if str(
            display_port).upper().__contains__('HDMI_B') else clock_helper.get_value_by_range(reg_value_DPCLKA_CFGCR0,
                                                                                              4, 5,
                                                                                              self.ddi_pll_map,
                                                                                              'DPLL') if str(
            display_port).upper().__contains__('HDMI_C') else clock_helper.get_value_by_range(reg_value_DPCLKA_CFGCR1,
                                                                                              0, 1,
                                                                                              self.ddi_pll_map,
                                                                                              'DPLL') if str(
            display_port).upper().__contains__('HDMI_D') else clock_helper.get_value_by_range(reg_value_DPCLKA_CFGCR1,
                                                                                              2, 3,
                                                                                              self.ddi_pll_map, 'DPLL')

        status = adls_clock_reg.verify_pll_enable(display_port, dpllValue, gfx_index)

        ClockRegister.DPLL_CFGCR0 = dpllValue + '_CFGCR0'
        ClockRegister.DPLL_CFGCR1 = dpllValue + '_CFGCR1'
        ClockRegister.DPLL_SSC = dpllValue + '_SSC'

        return status and self.ValidateDPll(display_port, gfx_index)

    ##
    # @brief function to validate HDMI DPLL divider values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def ValidateDPll(self, display_port, gfx_index='gfx_0'):
        regValue = clock_helper.clock_register_read('DPLL_CFGCR0_REGISTER', ClockRegister.DPLL_CFGCR0, gfx_index)
        reg_DPLL_SSC = clock_helper.clock_register_read('DPLL_SSC_REGISTER', ClockRegister.DPLL_SSC, gfx_index)

        reg_read_hdmi = HdmiClock()
        reg_read_hdmi.DCO_INT = clock_helper.get_value_by_range(regValue, 0, 9, '', 'DCO Integer')
        reg_read_hdmi.DCO_FRAC = clock_helper.get_value_by_range(regValue, 10, 24, '', 'DCO Fraction')
        reg_read_hdmi.SSC_ENABLE = clock_helper.get_value_by_range(reg_DPLL_SSC, 9, 9, '', 'SSC Enable')

        regValue = clock_helper.clock_register_read('DPLL_CFGCR1_REGISTER', ClockRegister.DPLL_CFGCR1, gfx_index)
        reg_read_hdmi.PDIV = clock_helper.get_value_by_range(regValue, 2, 5, self.pdiv_map, 'PDiv')
        reg_read_hdmi.KDIV = clock_helper.get_value_by_range(regValue, 6, 8, self.kdiv_map, 'KDiv')
        div_value2 = clock_helper.get_value_by_range(regValue, 9, 9, '', 'QDiv')
        if div_value2 == 0:
            reg_read_hdmi.QDIV = 1
        else:
            reg_read_hdmi.QDIV = clock_helper.get_value_by_range(regValue, 10, 17, '', 'QDiv')
        central_frequency = clock_helper.get_value_by_range(regValue, 0, 1, self.central_freq_dict, 'Central_frequency')

        self.calculate_symbol_freq(display_port, gfx_index)
        calculated_pll_freq = self.calculate_best_dco_freq()
        logging.debug("INFO : Calculated PLL Frequency = {0}".format(str(calculated_pll_freq)))
        logging.debug("INFO : DPLL0_CFGCR0 - DCO_Fraction_value = {0}, DCO_Integer_value = {1}".format(
            str(reg_read_hdmi.DCO_FRAC), str(reg_read_hdmi.DCO_INT)))

        reg_value = clock_helper.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
        reference_frequency = clock_helper \
            .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")

        # If reference freq is 38.4, treat it as 19.2
        if reference_frequency == 38.4:
            logging.debug("INFO : Reference Frequency is {0}. Using 19.2 instead".format(str(reference_frequency)))
            reference_frequency = 19.2
        logging.info("INFO : Reference Frequency is {0} MHz.".format(str(reference_frequency)))
        calculated_dco = calculated_pll_freq * (self.Pdiv * self.Kdiv * self.Qdiv)
        expected_dco_int = int(calculated_pll_freq * (self.Pdiv * self.Kdiv * self.Qdiv) / reference_frequency)
        # ADLS WA to divide dco fraction part by 2, this will override bspec formula
        expected_dco_frac = int(
            (calculated_dco / reference_frequency - int(calculated_dco / reference_frequency)) * 2 ** 14)

        ret = clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_CFGCR0),
                                                            parameter=['DCO Integer', 'DCO Fraction', 'SSC Enable'],
                                                            expected=[expected_dco_int, expected_dco_frac, 0],
                                                            actual=[reg_read_hdmi.DCO_INT, reg_read_hdmi.DCO_FRAC,
                                                               reg_read_hdmi.SSC_ENABLE])
        ret &= clock_helper.verify_port_clock_programming_ex(feature='{}'.format(ClockRegister.DPLL_CFGCR1),
                                                             parameter=['PDiv', 'KDiv', 'QDiv Mode'],
                                                             expected=[self.Pdiv, self.Kdiv, self.Qdiv],
                                                             actual=[reg_read_hdmi.PDIV, reg_read_hdmi.KDIV,
                                                                reg_read_hdmi.QDIV])

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
                                                                 expected='8400', actual=str(
                    central_frequency))  # 11 : 8400 MHz . SW should not program

        driver_dco_freq = reg_read_hdmi.DCO_INT * reference_frequency
        driver_pll_frequency = driver_dco_freq / (reg_read_hdmi.PDIV * reg_read_hdmi.KDIV * reg_read_hdmi.QDIV)

        if abs(calculated_pll_freq - driver_pll_frequency) > reference_frequency / (
                reg_read_hdmi.PDIV * reg_read_hdmi.KDIV * reg_read_hdmi.QDIV * 2):
            logging.warning("WARN: {0}: Current Value = {1} MHz is Greater than 1 MHz of Expected Value {2} MHz"
                            .format('Driver PLL Frequency', str(driver_pll_frequency), str(calculated_pll_freq)))
            return ret
        else:
            logging.debug("PASS: {0}: Current Value = {1} MHz is Less than 1 MHz of Expected Value {2} MHz"
                          .format('Driver PLL Frequency', str(driver_pll_frequency), str(calculated_pll_freq)))
            return ret

    ##
    # @brief function to find the Symbol Frequency for HDMI
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return Symbol Frequency in MHz
    def calculate_symbol_freq(self, display_port, gfx_index='gfx_0'):
        pipe = adls_clock_reg.get_pipe_for_port(display_port, gfx_index)
        logging.info("INFO : {0} ENABLED on PIPE{1}".format(display_port, pipe))
        reg_value = clock_helper.clock_register_read('TRANS_DDI_FUNC_CTL_REGISTER', 'TRANS_DDI_FUNC_CTL_' + pipe, gfx_index)
        bit_per_color_value = clock_helper.get_value_by_range(reg_value, 20, 22, self.bit_per_color, 'Bits Per Color')
        reg_value = clock_helper.clock_register_read('PIPE_MISC_REGISTER', 'PIPE_MISC_' + pipe, gfx_index)
        color_format_value = (clock_helper.get_value_by_range(reg_value, 27, 27, self.color_format, 'Color Format')) \
                             + '_' + str(bit_per_color_value)
        color_format_value = color_format_value
        color_divider = list(self.colorFormatDictionary.values())[
            list(self.colorFormatDictionary).index(color_format_value)]

        pixel_rate = clock_helper.get_pixel_rate(display_port, gfx_index)
        self.symbol_freq = (pixel_rate * color_divider)
        logging.info(
            "INFO : Symbol Frequency = {0} MHz Pixel Rate = {1} MHz".format(str(self.symbol_freq), (str(pixel_rate))))
        return self.symbol_freq

    ##
    # @brief Calculate the best DCO Frequency for HDMI
    # @return DCO Frequency in MHz
    def calculate_best_dco_freq(self):
        dco_min = 7998
        dco_max = 10000
        dco_mid = (dco_max + dco_min) / 2
        logging.debug("INFO : Mid Frequency = {0}".format(dco_mid))
        dividerlist_new = list(filter(lambda x: ((x * 5 * self.symbol_freq) < dco_max)
                                                and ((x * 5 * self.symbol_freq) > dco_min)
                                      , self.dividerlist))
        best_freq_dict = dict([(key, abs((key * 5 * self.symbol_freq) - dco_mid)) for key in dividerlist_new])
        best_key = list(best_freq_dict)[list(best_freq_dict.values()).index(sorted(best_freq_dict.values())[0])]
        best_dco = best_key * 5 * self.symbol_freq
        self.get_div_values(best_key)
        return best_dco / best_key

    ##
    # @brief Find the Divider Values
    # @param[in] bestdiv - best division integer
    # @return Bool- True or False
    def get_div_values(self, bestdiv):
        if (bestdiv != 0):
            if (bestdiv % 2 == 0):  # Even
                if (bestdiv == 2):
                    self.Pdiv = 2
                    self.Qdiv = 1
                    self.Kdiv = 1
                elif (bestdiv % 4 == 0):
                    self.Pdiv = 2
                    self.Qdiv = bestdiv / 4
                    self.Kdiv = 2
                elif (bestdiv % 6 == 0):
                    self.Pdiv = 3
                    self.Qdiv = bestdiv / 6
                    self.Kdiv = 2
                elif (bestdiv % 5 == 0):
                    self.Pdiv = 5
                    self.Qdiv = bestdiv / 10
                    self.Kdiv = 2
                elif (bestdiv % 14 == 0):
                    self.Pdiv = 7
                    self.Qdiv = bestdiv / 14
                    self.Kdiv = 2
            else:  # odd
                if (bestdiv == 3 or bestdiv == 5 or bestdiv == 7):
                    self.Pdiv = bestdiv
                    self.Qdiv = 1
                    self.Kdiv = 1
                else:  # 9, 15, 21
                    self.Pdiv = bestdiv / 3
                    self.Qdiv = 1
                    self.Kdiv = 3
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]ADLS_Clock_HDMI: Best divider value not found while calculating the "
                      "best DCO Frequency",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Best Divider Value NOT Found")
            return False
        return True


if __name__ == "__main__":
    clk = AdlsClockHdmi()
    clk.ValidateDPll(0,'gfx_0')
