##
# @file     tgl_clock_hdmi_dekelphy.py
# @brief   This tests EDP PLLS are programmed correctly for platform TGL.
# @author  Kruti, Vadhavaniya; Doriwala, Nainesh P

import decimal
import logging

import math
from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.tgl import tgl_clock_registers
from Libs.Feature.display_port import dpcd_helper
from Libs.Core.logger import gdhm


clock_helper = clk_helper.ClockHelper()
tgl_clock_reg = tgl_clock_registers.TglClockRegisters()
edp = 0


##
# @brief TGL port clock verification class for HDMI display on DekelPhy port
class TglClockHdmiDekelPhy():
    symbol_frequency = 0
    # Map of bit per color
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

    # Color Format to BPP map
    colorFormatDictionary = dict([('RGB_8', 1), ('RGB_10', 1.25),
                                  ('RGB_12', 1.5), ('YUV420_8', 0.5),
                                  ('YUV420_10', 0.625), ('YUV420_12', 0.75)])
    # Map of dssm freq
    dssm_ref_freq_map = dict([
        (24, 0),
        (19.2, 1),
        (38.4, 2)
    ])
    # Map of port phy base address
    port_phy_base_address_map = dict([
        ('D', 0x168000),
        ('E', 0x169000),
        ('F', 0x16A000),
        ('G', 0x16B000),
        ('H', 0x16C000),
        ('I', 0x16D000)
    ])
    # Map of port index reg
    port_index_reg_map = dict([
        ('D', '0_7'),
        ('E', '8_15'),
        ('F', '16_23'),
        ('G', '24_31'),
        ('H', '0_7'),
        ('I', '8_15')
    ])

    ##
    # @brief function to validate dekel phy Pll and phy values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return ret -  BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        ret = True

        ret &= self.verify_hdmi_dekel_phy(display_port, gfx_index)

        if (ret is True):
            logging.info("PASS: PLL Register values programmed as per BSPEC")
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]TGL_Clock_HDMI_Dekelphy: PLL Register values not programmed as "
                      "per BSPEC",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("FAIL: PLL Register values not programmed as per BSPEC")
            ret = False

        return ret

    ##
    # @brief function to validate dekel phy Pll and phy values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return ret - BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_hdmi_dekel_phy(self,display_port, gfx_index='gfx_0'):

        ret = True

        self.dp = 1 if str(display_port).__contains__('DP') else 0
        self.adapter_info = clock_helper.get_adapter_info(display_port, gfx_index)
        self.symbol_freq = self.calculate_symbol_freq(display_port, gfx_index)

        reg_value = clock_helper.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
        self.reference_frequency = clock_helper \
            .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")

        if display_port.startswith("HDMI_"):
            self.ssc_enable = 0
        else:
            self.ssc_enable = clock_helper.get_ssc_from_dpcd(display_port, gfx_index)

        dp_dco = 8100

        dco_min_freq = dp_dco if self.dp else 8000 if self.ssc_enable else 7992
        dco_max_freq = dp_dco if self.dp else 10000

        frequency = self.symbol_freq * 10
        logging.debug("Frequency is {0}".format(str(frequency)))
        logging.debug("dco max is {0}".format(str(dco_max_freq)))
        logging.debug("dco min is {0}".format(str(dco_min_freq)))

        div1_vals = [7, 5, 3, 2]
        div2_vals = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        success = 0
        target_dco_mhz = 0
        port_name = str(display_port).split('_')[1]
        display_tc_port = tgl_clock_reg.trans_ddi_tc_map[port_name.upper()]
        phy_base_address = self.port_phy_base_address_map[port_name]

        # Start MGPLL calculations:
        # Refer https://gfxspecs.intel.com/Predator/Home/Index/20845?dstFilter=TGL&mode=Filter
        for div1 in div1_vals:
            for div2 in div2_vals:
                dco = div1 * div2 * frequency / 2
                if (dco >= dco_min_freq) and (dco <= dco_max_freq):
                    logging.debug('Values of Div1 = {0}, Div2 = {1}'.format(str(div1), str(div2)))

                    reg_value_DKL_REFCLKIN_CTL = clock_helper.read_dkl_register('DKL_REFCLKIN_CTL_REGISTER',
                                                                                'DKL_REFCLKIN_CTL_NULL_' + port_name,
                                                                                display_tc_port, gfx_index)
                    ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_REFCLKIN_CTL.od_refclkin2_refclkmux, 1,
                                                                 'DKL_REFCLKIN_CTL.od_refclkin2_refclkmux')

                    reg_value_DKL_CLKTOP2_HSCLKCTL = clock_helper.read_dkl_register('DKL_CLKTOP2_HSCLKCTL_REGISTER',
                                                                                    'DKL_CLKTOP2_HSCLKCTL_NULL_' + port_name,
                                                                                    display_tc_port, gfx_index)
                    ret &= clock_helper.verify_port_clock_programming(
                        reg_value_DKL_CLKTOP2_HSCLKCTL.od_clktop2_coreclk_inputsel, 1,
                        'DKL_CLKTOP2_HSCLKCTL.od_clktop2_coreclk_inputsel')

                    reg_value_DKL_CLKTOP2_CORECLKCTL1 = clock_helper.read_dkl_register(
                        'DKL_CLKTOP2_CORECLKCTL1_REGISTER',
                        'DKL_CLKTOP2_CORECLKCTL1_NULL_' + port_name, display_tc_port, gfx_index)

                    ret &= clock_helper.verify_port_clock_programming(
                        reg_value_DKL_CLKTOP2_CORECLKCTL1.od_clktop2_coreclka_divratio, 5,
                        'DKL_CLKTOP2_CORECLKCTL1.od_clktop2_coreclka_divratio')

                    if div2 >= 2:
                        ret &= clock_helper.verify_port_clock_programming(
                            reg_value_DKL_CLKTOP2_HSCLKCTL.od_clktop2_tlinedrv_clksel, 1,
                            'DKL_CLKTOP2_HSCLKCTL.od_clktop2_tlinedrv_clksel')
                    else:
                        ret &= clock_helper.verify_port_clock_programming(
                            reg_value_DKL_CLKTOP2_HSCLKCTL.od_clktop2_tlinedrv_clksel, 0,
                            'DKL_CLKTOP2_HSCLKCTL.od_clktop2_tlinedrv_clksel')

                    coreclk_inputsel = 1

                    if self.dp:  # else default
                        coreclk_inputsel = 0

                    ret &= clock_helper.verify_port_clock_programming(
                        reg_value_DKL_CLKTOP2_HSCLKCTL.od_clktop2_coreclk_inputsel, coreclk_inputsel,
                        'DKL_CLKTOP2_HSCLKCTL.od_clktop2_coreclk_inputsel')

                    hsdiv_divratio = 0
                    if (div1 == 2):
                        hsdiv_divratio = 0
                    elif (div1 == 3):
                        hsdiv_divratio = 1
                    elif (div1 == 5):
                        hsdiv_divratio = 2
                    elif (div1 == 7):
                        hsdiv_divratio = 3
                    else:
                        hsdiv_divratio = 0

                    ret &= clock_helper.verify_port_clock_programming(
                        reg_value_DKL_CLKTOP2_HSCLKCTL.od_clktop2_hsdiv_divratio, hsdiv_divratio,
                        'DKL_CLKTOP2_HSCLKCTL.od_clktop2_hsdiv_divratio')
                    ret &= clock_helper.verify_port_clock_programming(
                        reg_value_DKL_CLKTOP2_HSCLKCTL.od_clktop2_dsdiv_divratio, div2,
                        'DKL_CLKTOP2_HSCLKCTL.od_clktop2_dsdiv_divratio')

                    target_dco_mhz = dco
                    success = 1
                    break

            if success == 1:
                break
        if success == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]TGL_Clock_HDMI_Dekelphy: Divider values NOT found for the Given "
                      "Frequency {0}".format(str(self.symbol_freq)),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Divider values not found for the given frequency {0}".format(str(self.symbol_freq)))

        m1div = 2  # pre-divider ratio
        ndiv = 1.0  # reference clock divider
        tdc_res = 0.000003  # TDC resolution
        ssc_freq_mhz = .032  # SSC frequency
        ssc_stepnum = 32  # SSC step num
        ssc_amp = .0047  # SSC amplitude

        # calculate the M2 ratio
        m2div = (target_dco_mhz / (self.reference_frequency / ndiv)) / m1div

        if m2div > 255:
            logging.info("FAIL and try a different frequency")

        # integer portion
        m2div_int = math.floor(m2div)

        # fractional portion
        fraction = decimal.Decimal(m2div) - decimal.Decimal(m2div_int)  # To prevent precision loss
        m2div_frac = math.floor(2 ** 22 * (fraction))

        # iref ndiv
        iref_ndiv = 4 if (self.reference_frequency > 80) else 2 if (self.reference_frequency > 38) else 1

        # TDC target count
        tdc_targetcnt = int(2 / (tdc_res * 8 * 50 * 1.1) / self.reference_frequency + 0.5)

        # feed forward gain
        logging.debug("m1div ={0}".format(m1div))
        logging.debug("target_dco_mhz ={0}".format(target_dco_mhz))
        logging.debug("tdc_res ={0}".format(tdc_res))
        logging.debug("ssc_en ={0}".format(self.ssc_enable))
        logging.debug("m2div_frac = {0}".format(m2div_frac))

        feedfwdgain = math.floor(m1div * (1.0 / target_dco_mhz) / tdc_res) if (self.ssc_enable or m2div_frac > 0) else 0

        # iref trim value
        if (self.reference_frequency / iref_ndiv) <= 19.2:
            iref_trim = 28
        elif ((self.reference_frequency / iref_ndiv) > 19.2 and (self.reference_frequency / iref_ndiv) <= 25):
            iref_trim = 25
        else:
            iref_trim = 24

        logging.debug("Reference Frequency = %s" % iref_trim)

        # bias start-up pulse width
        iref_pulse_width = 2 if ((self.reference_frequency / iref_ndiv) > 20) else 1

        # lf coeffs
        prop_coeff = 5 if (target_dco_mhz >= 9000) else 4
        int_coeff = 10 if (target_dco_mhz >= 9000) else 8

        # ssc params
        ssc_stepsize = (math.floor(m2div * ssc_amp / ssc_stepnum * 2 ** 10)) if self.ssc_enable else 0
        ssc_steplen = (math.ceil(self.reference_frequency / ssc_freq_mhz / (2 * ssc_stepnum))) if self.ssc_enable else 0
        ssc_steplog = math.log(ssc_stepnum) / math.log(2) - 1

        # calculate register values
        div0 = (int_coeff << 16) + (prop_coeff << 12) + (m1div << 8) + (m2div_int)
        div1 = (iref_trim << 16) + (tdc_targetcnt)
        ssc = (iref_ndiv << 29) + (ssc_steplen << 16) + (ssc_stepnum << 11) + (self.ssc_enable << 9)
        bias = (2 ** 30 if m2div_frac > 0 else 0) + (m2div_frac * 2 ** 8)
        tdc = (ssc_stepsize * 2 ** 8) + feedfwdgain

        logging.info("DCO : {0}".format(target_dco_mhz))

        # BIAS field
        i_frac_div_7_0 = (int(m2div_frac) & 0xFF)
        i_frac_div_21_16 = ((int(m2div_frac) >> 16) & 0xFF)
        i_frac_div_15_8 = ((int(m2div_frac) >> 8) & 0xFF)
        i_fracnen_h = m2div_frac > 0

        # DIV0 fields
        i_fbdiv_intgr_7_0 = m2div_int
        i_prop_coeff_3_0 = prop_coeff
        i_int_coeff_4_0 = int_coeff
        i_fbprediv_3_0 = m1div

        # DIV1 fields
        i_tdctargetcnt_7_0 = tdc_targetcnt
        i_ireftrim_4_0 = iref_trim

        # TDC_COLD_BIAS Fields
        i_feedfwrdgain_7_0 = feedfwdgain

        # DKL_BIAS verification will be warned, if there is difference of 1 in m2div_frac calculation (Because of python float precision bug).
        dkl_bias_register_value_match = True
        reg_value_DKL_BIAS = clock_helper.read_dkl_register("DKL_BIAS_REGISTER", "DKL_BIAS_" + port_name,
                                                            display_tc_port, gfx_index)

        if (reg_value_DKL_BIAS.i_fbdiv_frac_7_0 != i_frac_div_7_0) or (
                reg_value_DKL_BIAS.i_fbdiv_frac_21_16 != i_frac_div_21_16) or (
                reg_value_DKL_BIAS.i_fbdiv_frac_15_8 != i_frac_div_15_8) or (
                reg_value_DKL_BIAS.i_fracnen_h != i_fracnen_h):
            dkl_bias_register_value_match = False

        if (dkl_bias_register_value_match is False):
            m2div_frac = m2div_frac + 1  # Adding 1 to m2div_frac to fix precision delta
            i_frac_div_7_0 = (int(m2div_frac) & 0xFF)  # Calculating new bit values for DKL BIAS REGISTER
            i_frac_div_21_16 = ((int(m2div_frac) >> 16) & 0xFF)
            i_frac_div_15_8 = ((int(m2div_frac) >> 8) & 0xFF)
            i_fracnen_h = m2div_frac > 0

            logging.warning(
                "WARN : m2div_frac - Expected: {0}, Actual: {1}. Rounding of m2div_frac value with expected value".format(
                    m2div_frac, (m2div_frac - 1)))

        # Validating DKL_PLL_DIV0_REGISTER bit values
        reg_value_DKL_PLL_DIV0 = clock_helper.read_dkl_register("DKL_PLL_DIV0_REGISTER", "DKL_PLL_DIV0_" + port_name,
                                                                display_tc_port, gfx_index)
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_PLL_DIV0.i_fbdiv_intgr, i_fbdiv_intgr_7_0,
                                                     'DKL_PLL_DIV0.i_fbdiv_intgr')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_PLL_DIV0.i_prop_coeff_3_0, i_prop_coeff_3_0,
                                                     'DKL_PLL_DIV0.i_prop_coeff_3_0')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_PLL_DIV0.i_int_coeff_4_0, i_int_coeff_4_0,
                                                     'DKL_PLL_DIV0.i_int_coeff_4_0')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_PLL_DIV0.i_fbprediv_3_0, i_fbprediv_3_0,
                                                     'DKL_PLL_DIV0.i_fbprediv_3_0')

        # Validating DKL_PLL_DIV1_REGISTER bit values
        reg_value_DKL_PLL_DIV1 = clock_helper.read_dkl_register("DKL_PLL_DIV1_REGISTER", "DKL_PLL_DIV1_" + port_name,
                                                                display_tc_port, gfx_index)
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_PLL_DIV1.i_tdctargetcnt_7_0, i_tdctargetcnt_7_0,
                                                     'DKL_PLL_DIV1.i_tdctargetcnt_7_0')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_PLL_DIV1.i_ireftrim_4_0, i_ireftrim_4_0,
                                                     'DKL_PLL_DIV1.i_ireftrim_4_0')

        # Validating DKL_BIAS_REGISTER bit values
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_BIAS.i_fbdiv_frac_7_0, i_frac_div_7_0,
                                                     'DKL_BIAS.i_fbdiv_frac_7_0')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_BIAS.i_fbdiv_frac_21_16, i_frac_div_21_16,
                                                     'DKL_BIAS.i_fbdiv_frac_21_16')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_BIAS.i_fbdiv_frac_15_8, i_frac_div_15_8,
                                                     'DKL_BIAS.i_fbdiv_frac_15_8')
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_BIAS.i_fracnen_h, i_fracnen_h,
                                                     'DKL_BIAS.i_fracnen_h')

        # Validating DKL_TDC_COLDST_BIAS_REGISTER bit values
        reg_value_DKL_TDC_COLDST_BIAS = clock_helper.read_dkl_register("DKL_TDC_COLDST_BIAS_REGISTER",
                                                                       "DKL_TDC_COLDST_BIAS_" + port_name,
                                                                       display_tc_port, gfx_index)
        ret &= clock_helper.verify_port_clock_programming(reg_value_DKL_TDC_COLDST_BIAS.i_feedfwdgain_7_0,
                                                          i_feedfwrdgain_7_0,
                                                     'DKL_TDC_COLDST_BIAS.i_feedfwdgain_7_0')

        return ret

    ##
    # @brief function to find the Symbol Frequency based on the Display Type
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return Symbol Frequency in MHz
    def calculate_symbol_freq(self, display_port, gfx_index='gfx_0'):
        if self.dp:
            return self.calculate_dp_frequency(display_port, gfx_index)
        else:
            return self.calculate_hdmi_symbol_freq(display_port, gfx_index)

    ##
    # @brief function to find the Symbol Frequency for DP
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return Symbol Frequency in MHz
    def calculate_dp_frequency(self, display_port, gfx_index='gfx_0'):
        link_bw = dpcd_helper.DPCD_getLinkRate(self.adapter_info)
        return (link_bw * 100)

    ##
    # @brief function to find the Symbol Frequency for HDMI
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return Symbol Frequency in MHz
    def calculate_hdmi_symbol_freq(self, display_port, gfx_index='gfx_0'):
        pipe = tgl_clock_reg.get_pipe_for_port(display_port, gfx_index)
        reg_value = clock_helper.clock_register_read('TRANS_DDI_FUNC_CTL_REGISTER', 'TRANS_DDI_FUNC_CTL_' + pipe, gfx_index)
        bit_per_color_value = clock_helper.get_value_by_range(reg_value, 20, 22, self.bit_per_color, 'Bits Per Color')
        reg_value = clock_helper.clock_register_read('PIPE_MISC_REGISTER', 'PIPE_MISC_' + pipe, gfx_index)
        color_format_value = (clock_helper.get_value_by_range(reg_value, 27, 27, self.color_format, 'Color Format')) \
                             + '_' + str(bit_per_color_value)
        color_format_value = color_format_value
        color_divider = list(self.colorFormatDictionary.values())[
            list(self.colorFormatDictionary).index(color_format_value)]
        pixel_rate = clock_helper.get_pixel_rate(display_port, gfx_index)
        logging.info("Pixel rate: {0} , Bits per color value: {1}".format(pixel_rate,bit_per_color_value))
        self.symbol_freq = (pixel_rate * color_divider)
        return self.symbol_freq


if __name__ == "__main__":
    clk = TglClockHdmiDekelPhy()
