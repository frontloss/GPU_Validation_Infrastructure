##
# @file   dg2_clock_hdmi.py
# @brief  Python class to validate HDMI DPLL divider values are programmed correctly
# @author Kruti, Vadhavaniya; Doriwala, Nainesh P

import logging
import math
import ctypes

from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.dg2 import dg2_clock_registers
from Libs.Core.logger import gdhm


clock_helper = clk_helper.ClockHelper()
dg2_clock_reg = dg2_clock_registers.Dg2ClockRegisters()


##
# @brief Clock register class CP
class HdmiClockCp():
    ref_range = 0
    cp_init = 0
    cp_prop = 0
    cp_gs = 0
    cp_prop_gs = 0


##
# @brief Clock register class DIV
class HdmiClockDiv():
    div_5_clk_en = 0
    div_clk_en = 0
    div_mult = 0
    tx_clk_div = 0
    pmix_en = 0
    word_div_2_en = 0
    v2i = 0
    freq_vco = 0
    clk_div = 0
    multiplier = 0
    hdmi_div = 0
    pixel_clk_div = 0
    dp2_mode = 0
    div32_clk_sel = 0


##
# @brief Clock register class Fracn
class HdmiClockFracn():
    fracn_en = 0
    fracn_den = 0
    cfg_update_en = 0
    fracn_quot = 0
    fracn_rem = 0


##
# @brief Clock register class SSC
class HdmiClockSsc():
    ssc_en = 0
    ssc_ip_spread = 0
    ssc_peak = 0
    ssc_ste_size = 0


##
# HDMI PLL value dictionary with reference clock 100MH
HdmiModePLLValueRefClk100Mhz = {
    0: {"LinkRateMbps": 25.175, "ref_range": 3, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 128,
        "FracnEn": 1, "FracnQuot": 36663, "FracnRem": 71, "FracnDen": 143, "SscUpSpread": 1, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 1, "TxClkDiv": 5, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 0, "CpInit": 5, "CpProp": 15, "CpGs": 64, "CpPropGs": 124, "PixelClkDiv": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    1: {"LinkRateMbps": 27.0, "ref_range": 3, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 140,
        "FracnEn": 1, "FracnQuot": 26214, "FracnRem": 2, "FracnDen": 5, "SscUpSpread": 1, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 1, "TxClkDiv": 5, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 0, "CpInit": 5, "CpProp": 15, "CpGs": 64, "CpPropGs": 124, "PixelClkDiv": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    2: {"LinkRateMbps": 74.25, "ref_range": 3, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 86,
        "FracnEn": 1, "FracnQuot": 26214, "FracnRem": 2, "FracnDen": 5, "SscUpSpread": 1, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 1, "TxClkDiv": 3, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 4, "CpProp": 15, "CpGs": 64, "CpPropGs": 124, "PixelClkDiv": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    3: {"LinkRateMbps": 148.5, "ref_range": 3, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 86,
        "FracnEn": 1, "FracnQuot": 26214, "FracnRem": 2, "FracnDen": 5, "SscUpSpread": 1, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 1, "TxClkDiv": 2, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 4, "CpProp": 15, "CpGs": 64, "CpPropGs": 124, "PixelClkDiv": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    4: {"LinkRateMbps": 594, "ref_range": 3, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 86,
        "FracnEn": 1, "FracnQuot": 26214, "FracnRem": 2, "FracnDen": 5, "SscUpSpread": 1, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 1, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 4, "CpProp": 15, "CpGs": 64, "CpPropGs": 124, "PixelClkDiv": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
}


##
# @brief DG2 port clock verification class for HDMI display
class Dg2ClockHdmi():
    CurveFreqHz = [
        [2500000000, 3000000000, 3000000000, 3500000000, 3500000000, 4000000000, 4000000000, 5000000000],
        [4000000000, 4600000000, 4601000000, 5400000000, 5401000000, 6600000000, 6601000000, 8001000000]]

    # y axis heights const
    Curve0 = [
        [0.034149871, 0.039803269, 0.036034544, 0.040601014, 0.03564694, 0.040016109, 0.035127987, 0.041889522],
        [0.070000000, 0.078770454, 0.070451838, 0.080427119, 0.07099140, 0.084230173, 0.072945921, 0.087064218]]
    Curve1 = [
        [851770000000.0, 793852271600.0, 956726035800.0, 888572071600.0,
         1093797909000.0, 1035281939000.0, 1319412424000.0, 1172790000000.0],
        [602550000000.0, 555690000000.0, 720360000000.0, 695090000000.0,
         817850000000.0, 731030000000.0, 965910000000.0, 690770000000.0]]

    Curve2 = [
        [0.00218693, 0.002835287134, 0.002395395343, 0.002932270687,
         0.002351887545, 0.002861031697, 0.002294149152, 0.00309173],
        [0.00456000, 0.005570000000, 0.004610000000, 0.005770000000,
         0.004670000000, 0.006240000000, 0.004890000000, 0.00660000]]

    # Color Format to BPP map
    colorFormatDictionary = dict([('RGB_8', 1), ('RGB_10', 1.25),
                                  ('RGB_12', 1.5), ('YUV420_8', 0.5),
                                  ('YUV420_10', 0.625), ('YUV420_12', 0.75)])

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

    # Mapping of the listed port ref_clk
    port_ref_clk_map = dict([
        (38.4, 0),
        (100, 1)
    ])

    port_ref_clk = 100
    symbol_freq = 0

    ##
    # @brief function to validate HDMI clock.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        port_name = ''
        if str(display_port).upper().__contains__('_A'):
            port_name = 'PORT_A'
        elif str(display_port).upper().__contains__('_B'):
            port_name = 'PORT_B'
        elif str(display_port).upper().__contains__('_C'):
            port_name = 'PORT_C'
        elif str(display_port).upper().__contains__('_D'):
            port_name = 'PORT_D'
        elif str(display_port).upper().__contains__('_F'):
            port_name = 'PORT_TC1'
        else:
            logging.info("ERROR:Provided port is not valid for DG2")

        if dg2_clock_reg.verify_pll_enable(display_port, port_name, gfx_index) is False:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]DG2_Clock_HDMI:PLL not enable for {}".format(display_port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("FAIL : PLL not enable for {}".format(display_port))
            return False

        dg2_clock_registers.ClockRegister.MPLLB_CP = 'SNPS_PHY_MPLLB_CP_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_DIV = 'SNPS_PHY_MPLLB_DIV_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_DIV2 = 'SNPS_PHY_MPLLB_DIV2_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_FRACN1 = 'SNPS_PHY_MPLLB_FRACN1_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_FRACN2 = 'SNPS_PHY_MPLLB_FRACN2_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_SSCEN = 'SNPS_PHY_MPLLB_SSCEN_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_SSCSTEP = 'SNPS_PHY_MPLLB_SSCSTEP_' + port_name
        dg2_clock_registers.ClockRegister.REF_CONTROL = 'SNPS_PHY_REF_CONTROL_' + port_name

        pll_values = self.get_hdmi_pll_ref_values(display_port, gfx_index)

        if self.ValidateDPll(pll_values, gfx_index) is True:
            logging.debug("PASS : PLL Register values Programmed as per BSPEC")
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]DG2_Clock_HDMI: PLL Register values {0} not programmed as "
                      "per BSPEC".format(pll_values),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("FAIL : PLL Register values NOT Programmed as per BSPEC")
            return False

        return True

    ##
    # @brief function to validate HDMI DPLL divider values are programmed correctly.
    # @param[in] pll_values - PLL values dictionary
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def ValidateDPll(self, pll_values, gfx_index='gfx_0'):
        ret = True
        ref_range = pll_values["ref_range"]
        cp_init = pll_values["CpInit"]
        cp_prop = pll_values["CpProp"]
        cp_gs = pll_values["CpGs"]
        cp_prop_gs = pll_values["CpPropGs"]

        div_5_clk_en = pll_values["Div5ClkEn"]
        div_clk_en = pll_values["DivClkEn"]
        div_mult = pll_values["DivMult"]
        tx_clk_div = pll_values["TxClkDiv"]
        pmix_en = pll_values["PmixEn"]
        word_div_2_en = pll_values["WordDiv2En"]
        v2i = pll_values["V2i"]
        freq_vco = pll_values["FreqVco"]
        dp2_mode = pll_values["DP2Mode"]
        div32_clk_sel = pll_values["DPShimDiv32ClkSel"]

        clk_div = pll_values["clk_div"]
        multiplier = pll_values["Multiplier"]
        hdmi_div = pll_values["HdmiDiv"]
        pixel_clk_div = pll_values["PixelClkDiv"]

        ssc_en = pll_values["SscEn"]
        ssc_up_spread = pll_values["SscUpSpread"]
        ssc_peak = pll_values["SscPeak"]
        ssc_step_size = pll_values["SscStepSize"]

        fracn_en = pll_values["FracnEn"]
        fracn_den = pll_values["FracnDen"]
        fracn_quot = pll_values["FracnQuot"]
        fracn_rem = pll_values["FracnRem"]
        cfg_update_en = pll_values["CfgUpdateEn"]

        # read all PHY register
        reg_mpllb_cp = clock_helper.clock_register_read('SNPS_PHY_MPLLB_CP_REGISTER',
                                                        dg2_clock_registers.ClockRegister.MPLLB_CP, gfx_index)
        reg_mpllb_div = clock_helper.clock_register_read('SNPS_PHY_MPLLB_DIV_REGISTER',
                                                         dg2_clock_registers.ClockRegister.MPLLB_DIV, gfx_index)
        reg_mpllb_div2 = clock_helper.clock_register_read('SNPS_PHY_MPLLB_DIV2_REGISTER',
                                                          dg2_clock_registers.ClockRegister.MPLLB_DIV2, gfx_index)
        reg_mpllb_fracn1 = clock_helper.clock_register_read('SNPS_PHY_MPLLB_FRACN1_REGISTER',
                                                            dg2_clock_registers.ClockRegister.MPLLB_FRACN1, gfx_index)
        reg_mpllb_fracn2 = clock_helper.clock_register_read('SNPS_PHY_MPLLB_FRACN2_REGISTER',
                                                            dg2_clock_registers.ClockRegister.MPLLB_FRACN2, gfx_index)
        reg_mpllb_sscen = clock_helper.clock_register_read('SNPS_PHY_MPLLB_SSCEN_REGISTER',
                                                           dg2_clock_registers.ClockRegister.MPLLB_SSCEN, gfx_index)
        reg_mpllb_sscstep = clock_helper.clock_register_read('SNPS_PHY_MPLLB_SSCSTEP_REGISTER',
                                                             dg2_clock_registers.ClockRegister.MPLLB_SSCSTEP, gfx_index)
        reg_ref_control = clock_helper.clock_register_read('SNPS_PHY_REF_CONTROL_REGISTER',
                                                           dg2_clock_registers.ClockRegister.REF_CONTROL, gfx_index)

        reg_read_cp = HdmiClockCp()
        reg_read_cp.ref_range = clock_helper.get_value_by_range(reg_ref_control, 27, 31, '', 'Ref Range')
        reg_read_cp.cp_init = clock_helper.get_value_by_range(reg_mpllb_cp, 25, 31, '', 'CP Init')
        reg_read_cp.cp_gs = clock_helper.get_value_by_range(reg_mpllb_cp, 17, 23, '', 'CP Gs')
        reg_read_cp.cp_prop = clock_helper.get_value_by_range(reg_mpllb_cp, 9, 15, '', 'CP Prop')
        reg_read_cp.cp_prop_gs = clock_helper.get_value_by_range(reg_mpllb_cp, 1, 7, '', 'CP prop Gs')

        reg_read_div = HdmiClockDiv()
        reg_read_div.div_clk_en = clock_helper.get_value_by_range(reg_mpllb_div, 30, 30, '', 'Div Clk En')
        reg_read_div.div_5_clk_en = clock_helper.get_value_by_range(reg_mpllb_div, 29, 29, '', 'Div 5 Clk En')
        reg_read_div.v2i = clock_helper.get_value_by_range(reg_mpllb_div, 26, 27, '', 'V2i')
        reg_read_div.freq_vco = clock_helper.get_value_by_range(reg_mpllb_div, 24, 25, '', 'Freq Vco')
        reg_read_div.div_mult = clock_helper.get_value_by_range(reg_mpllb_div, 16, 23, '', 'Div Mul')
        reg_read_div.pmix_en = clock_helper.get_value_by_range(reg_mpllb_div, 10, 10, '', 'Pmix En')
        reg_read_div.dp2_mode = clock_helper.get_value_by_range(reg_mpllb_div, 9, 9, '', 'DP2 Mode')
        reg_read_div.word_div_2_en = clock_helper.get_value_by_range(reg_mpllb_div, 8, 8, '', 'Word Div 2 En')
        reg_read_div.tx_clk_div = clock_helper.get_value_by_range(reg_mpllb_div, 5, 7, '', 'Tx Clk Div')
        reg_read_div.div32_clk_sel = clock_helper.get_value_by_range(reg_mpllb_div, 0, 0, '', 'Div32 Clk Sel')

        reg_read_div.clk_div = clock_helper.get_value_by_range(reg_mpllb_div2, 12, 14, '', 'DP Ref Clk Div')
        reg_read_div.multiplier = clock_helper.get_value_by_range(reg_mpllb_div2, 0, 11, '', 'DP Multiplier')
        reg_read_div.hdmi_div = clock_helper.get_value_by_range(reg_mpllb_div2, 15, 17, '', 'HDMI Div')
        reg_read_div.pixel_clk_div = clock_helper.get_value_by_range(reg_mpllb_div2, 18, 19, '', 'Pixel Clk Div')

        reg_read_fracn = HdmiClockFracn()
        reg_read_fracn.fracn_en = clock_helper.get_value_by_range(reg_mpllb_fracn1, 31, 31, '', 'Fracn En')
        reg_read_fracn.cfg_update_en = clock_helper.get_value_by_range(reg_mpllb_fracn1, 30, 30, '', 'cfg update en')
        reg_read_fracn.fracn_den = clock_helper.get_value_by_range(reg_mpllb_fracn1, 0, 15, '', 'Fracn Den')
        reg_read_fracn.fracn_rem = clock_helper.get_value_by_range(reg_mpllb_fracn2, 16, 31, '', 'Fracn Rem')
        reg_read_fracn.fracn_quot = clock_helper.get_value_by_range(reg_mpllb_fracn2, 0, 15, '', 'Fracn Quot')

        reg_read_ssc = HdmiClockSsc()
        reg_read_ssc.ssc_en = clock_helper.get_value_by_range(reg_mpllb_sscen, 31, 31, '', 'SSC Enable')
        reg_read_ssc.ssc_up_spread = clock_helper.get_value_by_range(reg_mpllb_sscen, 30, 30, '', 'SSC Up Spread')
        reg_read_ssc.ssc_peak = clock_helper.get_value_by_range(reg_mpllb_sscen, 10, 29, '', 'SSC Peak')
        reg_read_ssc.ssc_ste_size = clock_helper.get_value_by_range(reg_mpllb_sscstep, 11, 31, '', 'SSC Step Size')

        ret &= clock_helper.verify_port_clock_programming_ex(
            feature='{}'.format(dg2_clock_registers.ClockRegister.REF_CONTROL),
            parameter=['Ref Range'],
            expected=[ref_range],
            actual=[reg_read_cp.ref_range])

        ret &= clock_helper.verify_port_clock_programming_ex(
            feature='{}'.format(dg2_clock_registers.ClockRegister.MPLLB_CP),
            parameter=['CP Init', 'CP Gs', 'CP Prop', 'CP prop Gs'],
            expected=[cp_init, cp_gs, cp_prop, cp_prop_gs],
            actual=[reg_read_cp.cp_init, reg_read_cp.cp_gs, reg_read_cp.cp_prop, reg_read_cp.cp_prop_gs])

        ret &= clock_helper.verify_port_clock_programming_ex(
            feature='{}'.format(dg2_clock_registers.ClockRegister.MPLLB_DIV),
            parameter=['Div Clk En', 'Div 5 Clk En', 'V2i', 'Freq Vco',
                       'Div Mul', 'Pmix En', 'DP2 Mode', 'Word Div 2 En', 'Tx Clk Div', 'Div32 Clk Sel'],
            expected=[div_clk_en, div_5_clk_en, v2i, freq_vco, div_mult, pmix_en,
                      dp2_mode, word_div_2_en, tx_clk_div, div32_clk_sel],
            actual=[reg_read_div.div_clk_en, reg_read_div.div_5_clk_en, reg_read_div.v2i, reg_read_div.freq_vco,
                    reg_read_div.div_mult, reg_read_div.pmix_en, reg_read_div.dp2_mode, reg_read_div.word_div_2_en,
                    reg_read_div.tx_clk_div, reg_read_div.div32_clk_sel])

        ret &= clock_helper.verify_port_clock_programming_ex(
            feature='{}'.format(dg2_clock_registers.ClockRegister.MPLLB_DIV2),
            parameter=['DP Ref Clk Div', 'DP Multiplier', 'HDMI Div', 'Pixel Clk Div'],
            expected=[clk_div, multiplier, hdmi_div, pixel_clk_div],
            actual=[reg_read_div.clk_div, reg_read_div.multiplier, reg_read_div.hdmi_div, reg_read_div.pixel_clk_div])

        ret &= clock_helper.verify_port_clock_programming_ex(
            feature='{}'.format(dg2_clock_registers.ClockRegister.MPLLB_FRACN1),
            parameter=['Fracn En', 'Cfg update en', 'Fracn Den'],
            expected=[fracn_en, cfg_update_en, fracn_den],
            actual=[reg_read_fracn.fracn_en, reg_read_fracn.cfg_update_en, reg_read_fracn.fracn_den])

        ret &= clock_helper.verify_port_clock_programming_ex(
            feature='{}'.format(dg2_clock_registers.ClockRegister.MPLLB_FRACN2),
            parameter=['Fracn Rem', 'Fracn Quot'],
            expected=[fracn_rem, fracn_quot],
            actual=[reg_read_fracn.fracn_rem, reg_read_fracn.fracn_quot])

        ret &= clock_helper.verify_port_clock_programming_ex(
            feature='{}'.format(dg2_clock_registers.ClockRegister.MPLLB_SSCEN),
            parameter=['SSC Enable', 'SSC Up Spread', 'SSC Peak'],
            expected=[ssc_en, ssc_up_spread, ssc_peak],
            actual=[reg_read_ssc.ssc_en, reg_read_ssc.ssc_up_spread, reg_read_ssc.ssc_peak])

        ret &= clock_helper.verify_port_clock_programming_ex(
            feature='{}'.format(dg2_clock_registers.ClockRegister.MPLLB_SSCSTEP),
            parameter=['SSC Step Size'],
            expected=[ssc_step_size],
            actual=[reg_read_ssc.ssc_ste_size])

        return ret

    ##
    # @brief function to get pll ref value based on symbol freq of display
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return pll_values - PLL_value dictionary
    def get_hdmi_pll_ref_values(self, display_port, gfx_index='gfx_0'):
        pll_values = []
        index = 0
        # get symbol clock freq
        self.calculate_symbol_freq(display_port, gfx_index)
        if self.symbol_freq == 25.175:
            index = 0
        elif self.symbol_freq == 27.0:
            index = 1
        elif self.symbol_freq == 74.25:
            index = 2
        elif self.symbol_freq == 148.5:
            index = 3
        elif self.symbol_freq == 594:
            index = 4
        else:
            pll_values = self.calculate_pll_value()
            return pll_values
        pll_values = HdmiModePLLValueRefClk100Mhz[index]
        return pll_values

    ##
    # @details Helper function to calculate pll values
    # @param[in]  x - input value in integer
    # @param[in]  x1 - input value in integer
    # @param[in]  x2 - input value in integer
    # @param[in]  y1 - input value in integer
    # @param[in]  y2 - input value in integer
    # @return int - calculated value
    def interp(self, x, x1, x2, y1, y2):
        dydx = (y2 - y1) / (x2 - x1)
        return y1 + dydx * (x - x1)

    ##
    # @details Helper function to count leading zeros in binary from given number
    # @param[in]  x - input value in integer
    # @return res - Number of leading zeros in binary
    def count_leading_zeros(self, x):

        # Keep shifting x by one until
        # leftmost bit does not become 1.
        total_bits = 64
        res = 0
        while (x & (1 << (total_bits - 1))) == 0:
            x = (x << 1)
            res += 1
        return res

    ##
    # @details Function to get log2 value of given value
    # @param[in] x- value in integer
    # @return int - log2 value of input value x
    def log2(self, x):
        return 63 - self.count_leading_zeros(int(x))

    ##
    # @details function to calculate pll value
    # @return pll_values - pll value of display
    def calculate_pll_value(self):
        pll_values = []
        refclk = 100000000
        clock_4999MHz = 4999999900
        clock_16GHz = 16000000000
        clock_9999MHz = 2 * clock_4999MHz
        clk_div = 1

        refclk_postscalar = refclk >> clk_div
        datarate = int(self.symbol_freq*1000*1000) * 10  # Convert to Hz
        if datarate <= clock_9999MHz:
            v2i = 2
            tx_clk_div = self.log2(clock_9999MHz / datarate)
        else:
            v2i = 3
            tx_clk_div = self.log2(clock_16GHz / datarate)
        vco_clk = (datarate << tx_clk_div) >> 1
        vco_div_refclk_integer = int(vco_clk / refclk_postscalar)
        vco_div_refclk_fracn = int(((vco_clk % refclk_postscalar) << 32) / refclk_postscalar)
        fracn_quot = vco_div_refclk_fracn >> 16
        fracn_rem = vco_div_refclk_fracn & 0xffff
        fracn_rem = fracn_rem - (fracn_rem >> 15)
        fracn_den = 0xffff
        fracn_en = 1 if (fracn_quot != 0 or fracn_rem != 0) else 0

        pmix_en = fracn_en
        multiplier = (vco_div_refclk_integer - 16) * 2

        curve_index = v2i - 2
        segmentindex = 0
        freq_vco = 0
        for index in range(0, 8, 2):

            if vco_clk <= self.CurveFreqHz[curve_index][index + 1]:
                segmentindex = index
                freq_vco = 3 - (segmentindex >> 1)
                break
        vco_div_refclk_float = vco_clk / refclk_postscalar
        o_397ced90 = self.interp(vco_clk, self.CurveFreqHz[curve_index][segmentindex],
                                 self.CurveFreqHz[curve_index][segmentindex + 1],
                                 self.Curve0[curve_index][segmentindex],
                                 self.Curve0[curve_index][segmentindex + 1])
        o_20c634d6 = self.interp(vco_clk, self.CurveFreqHz[curve_index][segmentindex],
                                 self.CurveFreqHz[curve_index][segmentindex + 1],
                                 self.Curve2[curve_index][segmentindex],
                                 self.Curve2[curve_index][segmentindex + 1])
        o_20c634d4 = self.interp(vco_clk, self.CurveFreqHz[curve_index][segmentindex],
                                 self.CurveFreqHz[curve_index][segmentindex + 1],
                                 self.Curve1[curve_index][segmentindex],
                                 self.Curve1[curve_index][segmentindex + 1])
        o_72019306 = o_20c634d6 * (4 - v2i) / 16000
        o_6593e82b = o_20c634d6 * (4 - v2i) / 160
        o_5cefc329 = 1120.08301 * vco_div_refclk_float / (o_397ced90 * o_20c634d4)
        cp_init = max(1.0, min(round(o_5cefc329 / o_72019306), 127))
        o_49960328 = o_72019306 * cp_init
        o_544adb37 = math.sqrt(o_20c634d4 * o_49960328 * o_397ced90 / (5.5e-11 * vco_div_refclk_float))
        o_4ef74e66 = 1.460281 * vco_div_refclk_float * o_544adb37 / o_20c634d4
        cp_prop = max(1.0, min(round(o_4ef74e66 / o_6593e82b), 127))
        pll_values = {"LinkRateMbps": self.symbol_freq, "ref_range": 3, "clk_div": clk_div, "SscEn": 0, "Div5ClkEn": 1,
                      "Multiplier": multiplier, "FracnEn": fracn_en, "FracnQuot": fracn_quot, "FracnRem": fracn_rem,
                      "FracnDen": fracn_den, "SscUpSpread": 1, "SscPeak": 0, "SscStepSize": 0, "DivClkEn": 0,
                      "DivMult": 0, "HdmiDiv": 1, "TxClkDiv": tx_clk_div, "PmixEn": pmix_en, "WordDiv2En": 0,
                      "V2i": v2i, "FreqVco": freq_vco, "CpInit": cp_init, "CpProp": cp_prop, "CpGs": 64,
                      "CpPropGs": 124, "PixelClkDiv": 0, "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1}

        return pll_values

    ##
    # @brief function to find the Symbol Frequency for HDMI
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return Symbol Frequency in MHz
    def calculate_symbol_freq(self, display_port, gfx_index='gfx_0'):
        pipe = dg2_clock_reg.get_pipe_for_port(display_port, gfx_index)
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


if __name__ == "__main__":
    clk = Dg2ClockHdmi()
    clk.ValidateDPll(HdmiModePLLValueRefClk100Mhz[0], 'gfx_0')

