##
# @file    adlp_clock_hdmi_dekelphy.py
# @brief   This tests Dekel phy HDMI PLLS are programmed correctly for platform ADLP.
# @author  Sri Sumanth Geesala


import decimal
import logging
import math
import platform
import re

from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.adlp import adlp_clock_registers
from Libs.Feature.display_engine.de_base import display_base
from Libs.Core.logger import gdhm
from Libs.Core.machine_info import machine_info


##
# @brief ADLP port clock verification class for HDMI DekelPhy display
class AdlpClockHdmiDekelPhy():

    ##
    # @brief init for HDMI DekelPhy display
    def __init__(self):
        self.symbol_frequency = 0
        self.clock_helper = clk_helper.ClockHelper()

        # Mapping of bit per color
        self.bit_per_color = dict([
            (8, 0),
            (10, 1),
            (6, 2),
            (12, 3)
        ])

        # Mapping of color format
        self.color_format = dict([
            ('RGB', 0),
            ('YUV420', 1)
        ])

        # Color Format to BPP map
        self.colorFormatDictionary = dict([('RGB_8', 1), ('RGB_10', 1.25),
                                      ('RGB_12', 1.5), ('YUV420_8', 0.5),
                                      ('YUV420_10', 0.625), ('YUV420_12', 0.75)])
        # Mapping of reference freq
        self.dssm_ref_freq_map = dict([
            (24, 0),
            (19.2, 1),
            (38.4, 2)
        ])

    ##
    # @brief function to validate dekel phy Pll and phy values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        ret = True

        ret &= self.verify_hdmi_dekel_phy(display_port, gfx_index)

        if (ret is True):
            logging.info("PASS: PLL Register values programmed as per BSPEC")
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]ADLP_Clock_HDMI_Dekelphy: PLL Register values not programmed as "
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
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_hdmi_dekel_phy(self, display_port, gfx_index='gfx_0'):

        ret = True
        self.symbol_freq = self.calculate_hdmi_symbol_freq(display_port, gfx_index)

        reg_value = self.clock_helper.clock_register_read('DSSM_REGISTER', 'DSSM', gfx_index)
        self.reference_frequency = self.clock_helper \
            .get_value_by_range(reg_value, 29, 31, self.dssm_ref_freq_map, "CD Clock Frequency")

        if display_port.startswith("HDMI_"):
            self.ssc_enable = 0
        else:
            self.ssc_enable = self.clock_helper.get_ssc_from_dpcd(display_port, gfx_index)

        dco_min_freq = 8000 if self.ssc_enable else 7992
        dco_max_freq = 10000

        frequency = self.symbol_freq * 10
        logging.debug("Frequency is {0}".format(str(frequency)))
        logging.debug("dco max is {0}".format(str(dco_max_freq)))
        logging.debug("dco min is {0}".format(str(dco_min_freq)))

        div1_vals = [7, 5, 3, 2]
        div2_vals = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        success = 0
        target_dco_mhz = 0
        port_name = str(display_port).split('_')[1]
        adlp_clock_reg = adlp_clock_registers.AdlpClockRegisters()
        display_tc_port = adlp_clock_reg.trans_ddi_tc_map[port_name.upper()]
        pll_selected = adlp_clock_reg.DKL_PLL1

        # Start TypeC PHY PLL calculations:
        # Refer https://gfxspecs.intel.com/Predator/Home/Index/55316
        for div1 in div1_vals:
            for div2 in div2_vals:
                dco = div1 * div2 * frequency / 2
                if (dco >= dco_min_freq) and (dco <= dco_max_freq):
                    logging.debug('Values of Div1 = {0}, Div2 = {1}'.format(str(div1), str(div2)))

                    reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5 = self.clock_helper.read_dkl_register(
                        'DKLP_CMN_ANA_CMN_ANA_DWORD5_REGISTER', 'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port,
                        display_tc_port, gfx_index)

                    reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD6 = self.clock_helper.read_dkl_register(
                        'DKLP_CMN_ANA_CMN_ANA_DWORD6_REGISTER',
                        'DKLP_CMN_ANA_CMN_ANA_DWORD6_' + display_tc_port, display_tc_port, gfx_index)
                    ret &= self.clock_helper.verify_port_clock_programming(
                        reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD6.od_clktop2_coreclka_divratio, 5,
                        'DKLP_CMN_ANA_CMN_ANA_DWORD6_' + display_tc_port + '.od_clktop2_coreclka_divratio')

                    if div2 >= 2:
                        ret &= self.clock_helper.verify_port_clock_programming(
                            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5.od_clktop2_tlinedrv_clksel, 1,
                            'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port + '.od_clktop2_tlinedrv_clksel')
                    else:
                        ret &= self.clock_helper.verify_port_clock_programming(
                            reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5.od_clktop2_tlinedrv_clksel, 0,
                            'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port + '.od_clktop2_tlinedrv_clksel')

                    coreclk_inputsel = 1

                    ret &= self.clock_helper.verify_port_clock_programming(
                        reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5.od_clktop2_coreclk_inputsel, coreclk_inputsel,
                        'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port + '.od_clktop2_coreclk_inputsel')

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

                    ret &= self.clock_helper.verify_port_clock_programming(
                        reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5.od_clktop2_hsdiv_divratio, hsdiv_divratio,
                        'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port + '.od_clktop2_hsdiv_divratio')
                    ret &= self.clock_helper.verify_port_clock_programming(
                        reg_value_DKLP_CMN_ANA_CMN_ANA_DWORD5.od_clktop2_dsdiv_divratio, div2,
                        'DKLP_CMN_ANA_CMN_ANA_DWORD5_' + display_tc_port + '.od_clktop2_dsdiv_divratio')

                    target_dco_mhz = dco
                    success = 1
                    break

            if success == 1:
                break
        if success == 0:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]ADLP_Clock_HDMI_Dekelphy: Divider values NOT found for the Given "
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

        # Get SKU name
        disp_hw_info = machine_info.SystemInfo().get_gfx_display_hardwareinfo()
        if len(disp_hw_info) <= int(gfx_index[-1]):
            logging.error(f'{gfx_index} not available in enumerated adapters')
            return False
        sku_name = disp_hw_info[int(gfx_index[-1])].SkuName
        platform_name = disp_hw_info[int(gfx_index[-1])].DisplayAdapterName

        # Get stepping ID
        cpu_stepping = self.get_cpu_stepping()
        logging.debug(f"cpu_stepping {cpu_stepping}")

        # lf coeffs
        if platform_name.upper() == "ADLP" and sku_name.upper() != "RPLU":
            # Use new prop_coeff & int_coeff while evaluating HDMI algo for RPL - P / ADL - N
            # HSD-1309903573 # Bspec: https://gfxspecs.intel.com/PredatorHome/Index/31475
            # Later, this Bpsec change was incorporated to ADLP platform from C0 stepping.
            # Driver PR: #131620
            prop_coeff = 2
            int_coeff = 7
        else:
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

        # DKL_BIAS verification will be warned, if there is difference of 1 in m2div_frac calculation
        # (Because of python float precision bug).
        dklp_bias_register_value_match = True
        reg_value_DKLP_PLL_BIAS = self.clock_helper.read_dkl_register(
            "DKLP_PLL_BIAS_REGISTER", "DKLP_" + pll_selected + "_BIAS_" + display_tc_port,
            display_tc_port, gfx_index)

        if (reg_value_DKLP_PLL_BIAS.i_fbdiv_frac_7_0 != i_frac_div_7_0) or (
                reg_value_DKLP_PLL_BIAS.i_fbdiv_frac_21_16 != i_frac_div_21_16) or (
                reg_value_DKLP_PLL_BIAS.i_fbdiv_frac_15_8 != i_frac_div_15_8) or (
                reg_value_DKLP_PLL_BIAS.i_fracnen_h != i_fracnen_h):
            dklp_bias_register_value_match = False

        if (dklp_bias_register_value_match is False):
            m2div_frac = m2div_frac + 1  # Adding 1 to m2div_frac to fix precision delta
            i_frac_div_7_0 = (int(m2div_frac) & 0xFF)  # Calculating new bit values for DKL BIAS REGISTER
            i_frac_div_21_16 = ((int(m2div_frac) >> 16) & 0xFF)
            i_frac_div_15_8 = ((int(m2div_frac) >> 8) & 0xFF)
            i_fracnen_h = m2div_frac > 0

            logging.warning( "WARN : m2div_frac - Expected: {0}, Actual: {1}. "
                             "Rounding of m2div_frac value with expected value".format(m2div_frac, (m2div_frac - 1)))

        # Validating DKL_PLL_DIV0_REGISTER bit values
        reg_value_DKLP_PLL_DIV0 = self.clock_helper.read_dkl_register(
            "DKLP_PLL_DIV0_REGISTER", "DKLP_" + pll_selected + "_DIV0_" + display_tc_port, display_tc_port, gfx_index)
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_DIV0.i_fbdiv_intgr, i_fbdiv_intgr_7_0,
            "DKLP_" + pll_selected + "_DIV0_" + display_tc_port + '.i_fbdiv_intgr')
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_DIV0.i_prop_coeff_3_0, i_prop_coeff_3_0,
            "DKLP_" + pll_selected + "_DIV0_" + display_tc_port + '.i_prop_coeff_3_0')
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_DIV0.i_int_coeff_4_0, i_int_coeff_4_0,
            "DKLP_" + pll_selected + "_DIV0_" + display_tc_port + '.i_int_coeff_4_0')
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_DIV0.i_fbprediv_3_0, i_fbprediv_3_0,
            "DKLP_" + pll_selected + "_DIV0_" + display_tc_port + '.i_fbprediv_3_0')

        # Validating DKL_PLL_DIV1_REGISTER bit values
        reg_value_DKLP_PLL_DIV1 = self.clock_helper.read_dkl_register(
            "DKLP_PLL_DIV1_REGISTER", "DKLP_" + pll_selected + "_DIV1_" + display_tc_port, display_tc_port, gfx_index)
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_DIV1.i_tdctargetcnt_7_0, i_tdctargetcnt_7_0,
            "DKLP_" + pll_selected + "_DIV1_" + display_tc_port + '.i_tdctargetcnt_7_0')
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_DIV1.i_ireftrim_4_0, i_ireftrim_4_0,
            "DKLP_" + pll_selected + "_DIV1_" + display_tc_port + '.i_ireftrim_4_0')

        # Validating DKL_BIAS_REGISTER bit values
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_BIAS.i_fbdiv_frac_7_0, i_frac_div_7_0,
            "DKLP_" + pll_selected + "_BIAS_" + display_tc_port + '.i_fbdiv_frac_7_0')
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_BIAS.i_fbdiv_frac_21_16, i_frac_div_21_16,
            "DKLP_" + pll_selected + "_BIAS_" + display_tc_port + '.i_fbdiv_frac_21_16')
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_BIAS.i_fbdiv_frac_15_8, i_frac_div_15_8,
            "DKLP_" + pll_selected + "_BIAS_" + display_tc_port + '.i_fbdiv_frac_15_8')
        ret &= self.clock_helper.verify_port_clock_programming(
            reg_value_DKLP_PLL_BIAS.i_fracnen_h, i_fracnen_h,
            "DKLP_" + pll_selected + "_BIAS_" + display_tc_port + '.i_fracnen_h')

        # Validating DKL_TDC_COLDST_BIAS_REGISTER bit values
        reg_value_DKLP_PLL_TDC_COLDST_BIAS = self.clock_helper.read_dkl_register(
            "DKLP_PLL_TDC_COLDST_BIAS_REGISTER", "DKLP_" + pll_selected + "_TDC_COLDST_BIAS_" + display_tc_port,
            display_tc_port, gfx_index)
        ret &= self.clock_helper.verify_port_clock_programming(reg_value_DKLP_PLL_TDC_COLDST_BIAS.i_feedfwdgain_7_0,
                                                               i_feedfwrdgain_7_0,
                                                     'DKLP_PLL_TDC_COLDST_BIAS.i_feedfwdgain_7_0')

        return ret

    ##
    # @brief function to find the Symbol Frequency for HDMI
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return Symbol Frequency in MHz
    def calculate_hdmi_symbol_freq(self, display_port, gfx_index='gfx_0'):
        disp_base = display_base.DisplayBase(display_port)
        pipe, ddi = disp_base.GetPipeDDIAttachedToPort(display_port)
        pipe = pipe.split('_')[-1].upper()
        reg_value = self.clock_helper.clock_register_read('TRANS_DDI_FUNC_CTL_REGISTER', 'TRANS_DDI_FUNC_CTL_' + pipe, gfx_index)
        bit_per_color_value = self.clock_helper.get_value_by_range(reg_value, 20, 22, self.bit_per_color, 'Bits Per Color')
        reg_value = self.clock_helper.clock_register_read('PIPE_MISC_REGISTER', 'PIPE_MISC_' + pipe, gfx_index)
        color_format_value = (self.clock_helper.get_value_by_range(reg_value, 27, 27, self.color_format, 'Color Format')) \
                             + '_' + str(bit_per_color_value)
        color_format_value = color_format_value
        color_divider = list(self.colorFormatDictionary.values())[
            list(self.colorFormatDictionary).index(color_format_value)]

        pixel_rate = self.clock_helper.get_pixel_rate(display_port, gfx_index)
        logging.info("Pixel rate: {0} , Bits per color value: {1}".format(pixel_rate, bit_per_color_value))
        self.symbol_freq = (pixel_rate * color_divider)
        return self.symbol_freq

    ##
    # @brief      Get the cpu stepping
    # @return     Stepping of the CPU
    @staticmethod
    def get_cpu_stepping():
        output = platform.processor()
        std_out = re.compile(r'[\r\n]').sub(" ", output)
        # search for the numbers after the match of "Stepping "
        match_output = re.match(r".*Stepping (?P<Stepping>[0-9]+)", std_out)
        if match_output is None:
            logging.error(f"FAILED to get info for CPU Stepping. Output= {output}")
            return None
        return match_output.group("Stepping")


if __name__ == "__main__":
    clk = AdlpClockHdmiDekelPhy()
