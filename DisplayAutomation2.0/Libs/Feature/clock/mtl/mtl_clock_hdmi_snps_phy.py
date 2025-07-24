######################################################################################
# @file         mtl_clock_hdmi_snps_phy.py
# @brief        Contains HDMI specific part of MTL Synopsys PHY (both C10 and C20) verification and HDMI algorithms.
# @details      Bspec references:
#               C10 registers and programming sequence: https://gfxspecs.intel.com/Predator/Home/Index/67636
#               C20 registers and programming sequence: https://gfxspecs.intel.com/Predator/Home/Index/67610
#               HDMI algorithms (C10 and C20): https://gfxspecs.intel.com/Predator/Home/Index/64568
# @author       Sri Sumanth Geesala
######################################################################################

import math
import logging

from Libs.Core.logger import gdhm
from Libs.Feature.clock.mtl.mtl_clock_helper import MtlClockHelper
from Libs.Feature.clock import clock_helper as clk_helper
from DisplayRegs import DisplayArgs
from DisplayRegs.Gen14.Pll import Gen14PllRegs
from DisplayRegs.Gen14 import MtlSnpsPhyRegisters

HDMI_C10_STANDARD_LINK_RATES = [0.25175, 0.27, 0.7425, 1.485, 5.94]         # In Gbps
HDMI_C20_STANDARD_LINK_RATES = [0.25175, 0.27, 0.7425, 1.485, 5.94, 3.0, 6.0, 8.0, 10.0, 12.0]      # In Gbps

# These PLL values are only for standard HDMI link rates with reference clock set to 38.4 MHz given in Bspec table
# (https://gfxspecs.intel.com/Predator/Home/Index/64568?dstFilter=MTL&mode=Filter). Values are in decimals.
# For any other link rate, we will use the HDMI PLL programming algorithm.
# C10 PHY
EXPECTED_C10_MPLL_SSC_EN = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 0, 0, 0, 0]))
EXPECTED_C10_MPLL_DIV5_EN = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [1, 1, 1, 1, 1]))
EXPECTED_C10_MPLL_MULTIPLIER = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [178, 192, 122, 122, 122]))
EXPECTED_C10_MPLL_FRACN_EN = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 1, 1, 1, 1]))
EXPECTED_C10_MPLL_FRACN_QUOT = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 32768, 22528, 22528, 22528]))
EXPECTED_C10_MPLL_FRACN_REM = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 0, 0, 0, 0]))
EXPECTED_C10_MPLL_FRACN_DEN = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [1, 1, 1, 1, 1]))
EXPECTED_C10_MPLL_SSC_UP_SPREAD = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [1, 1, 1, 1, 1]))
EXPECTED_C10_MPLL_SSC_PEAK = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 0, 0, 0, 0]))
EXPECTED_C10_MPLL_SSC_STEPSIZE = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 0, 0, 0, 0]))
EXPECTED_C10_MPLL_DIV_CLK_EN = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 0, 0, 0, 0]))
EXPECTED_C10_MPLL_DIV_MULTIPLIER = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 0, 0, 0, 0]))
EXPECTED_C10_MPLL_HDMI_DIV = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [1, 1, 1, 1, 1]))
EXPECTED_C10_MPLL_TX_CLK_DIV = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [5, 5, 3, 2, 0]))
EXPECTED_C10_MPLL_PMIX_EN = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 1, 1, 1, 1]))
EXPECTED_C10_MPLL_WORD_DIV2_EN = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 0, 0, 0, 0]))
EXPECTED_C10_MPLL_ANA_V2I = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [2, 2, 2, 2, 2]))
EXPECTED_C10_MPLL_CP_INT = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [6, 6, 6, 6, 6]))
EXPECTED_C10_MPLL_CP_PROP = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [18, 19, 20, 20, 20]))
EXPECTED_C10_MPLL_ANA_CP_INT_GS = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [30, 30, 30, 30, 30]))
EXPECTED_C10_MPLL_ANA_CP_PROP_GS = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [28, 28, 28, 28, 28]))
EXPECTED_C10_MPLL_HDMI_PIXEL_CLK_DIV = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [0, 0, 0, 0, 0]))
EXPECTED_C10_REF_RANGE = dict(zip(HDMI_C10_STANDARD_LINK_RATES, [1, 1, 1, 1, 1]))

# C20 PHY
EXPECTED_C20_REF_CLK_MPLLB_DIV = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
EXPECTED_C20_MPLL_MULTIPLIER = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [210, 224, 154, 154, 154, 156, 156, 208, 260,
                                                                       312]))
EXPECTED_C20_MPLL_FRACN_EN = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
EXPECTED_C20_MPLL_FRACN_QUOT = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [0, 32768, 22528, 22528, 22528, 8192, 8192, 10922,
                                                                       13653, 16384]))
EXPECTED_C20_MPLL_FRACN_REM = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [0, 0, 0, 0, 0, 0, 0, 2, 1, 0]))
EXPECTED_C20_MPLL_FRACN_DEN = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [1, 1, 1, 1, 1, 1, 1, 3, 3, 1]))
EXPECTED_C20_MPLL_SSC_UP_SPREAD = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
EXPECTED_C20_MPLL_SSC_PEAK = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
EXPECTED_C20_MPLL_SSC_STEP_SIZE = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
EXPECTED_C20_MPLL_DIV_CLK_EN = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]))
EXPECTED_C20_MPLL_DIV_MULTIPLIER = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [128, 128, 64, 32, 8, 16, 8, 8, 8, 8]))
EXPECTED_C20_MPLLB_HDMI_DIV = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [1, 1, 1, 1, 1, 4, 4, 4, 4, 4]))
EXPECTED_C20_MPLL_TX_CLK_DIV = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [5, 5, 3, 2, 0, 1, 0, 0, 0, 0]))
EXPECTED_C20_MPLLB_ANA_V2I = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [2, 2, 2, 2, 2, 2, 2, 2, 2, 3]))
EXPECTED_C20_MPLLB_ANA_FREQ_VCO = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [0, 0, 3, 3, 3, 3, 3, 1, 0, 1]))
EXPECTED_C20_MPLLB_ANA_CP_INT = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]))
EXPECTED_C20_MPLLB_ANA_CP_PROP = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [18, 18, 20, 20, 20, 20, 20, 20, 20, 41]))
EXPECTED_C20_MPLLB_ANA_CP_INT_GS = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [64, 64, 64, 64, 64, 64, 64, 64, 64, 64]))
EXPECTED_C20_MPLLB_ANA_CP_PROP_GS = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [124, 124, 124, 124, 124, 124, 124, 124, 124,
                                                                            124]))
EXPECTED_C20_MPLLB_HDMI_PIXEL_CLK_DIV = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
EXPECTED_C20_MPLLB_WORD_CLK_DIV = dict(zip(HDMI_C20_STANDARD_LINK_RATES, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))

##
# @brief        This class containing C10 PHY parameters that will be filled during C10 PHY HDMI calculation
class C10Phy:
    mpll_hdmi_pixel_clk_div = 0
    mpll_ssc_en = 0
    mpll_ssc_peak = 0
    mpll_ssc_stepsize = 0
    mpll_ssc_up_spread = 0
    mpll_word_div2_en = 0
    mpll_div5_en = 0
    mpll_div_multiplier = 0
    mpll_div_clk_en = 0
    mpll_hdmi_div = 0
    mpll_ana_cp_int_gs = 0
    mpll_ana_cp_prop_gs = 0
    mpll_ana_v2i = 0
    mpll_tx_clk_div = 0
    mpll_fracn_quot = 0
    mpll_fracn_rem = 0
    mpll_fracn_den = 0
    mpll_fracn_en = 0
    mpll_pmix_en = 0
    mpll_multiplier = 0
    mpll_cp_int = 0
    mpll_cp_prop = 0
    ref_range = 0


##
# @brief        This class containing C20 PHY parameters that will be filled during C20 PHY HDMI calculation
class C20Phy:
    mpll_tx_clk_div = 0
    mpll_multiplier = 0
    mpll_fracn_quot = 0
    mpll_fracn_rem = 0
    mpll_fracn_den = 0
    mpll_fracn_en = 0
    mpll_ssc_up_spread = 0
    mpll_ssc_peak = 0
    mpll_ssc_step_size = 0
    mpll_div_clk_en = 0
    mpll_div_multiplier = 0
    mpllb_ana_freq_vco = 0
    mpllb_ana_cp_int = 0
    mpllb_ana_cp_prop = 0
    mpllb_hdmi_div = 0
    mpllb_ana_cp_int_gs = 0
    mpllb_ana_cp_prop_gs = 0
    ref_clk_mpllb_div = 0
    mpllb_word_clk_div = 0
    mpllb_hdmi_pixel_clk_div = 0
    mpllb_ana_v2i = 0


##
# @brief        This is the class containing MTL HDMI Snps Phy related verifications
class MtlClockHdmiSnpsPhy:
    clock_helper = clk_helper.ClockHelper()

    # Mapping of reference freq in DSSM register field
    dssm_ref_freq_map = {
        0:  24,
        1:  19.2,
        2:  38.4
    }

    ##
    # @brief        Function that will be called from tests for MTL clock verification on DP displays
    # @param[in]    display_port   port name like HDMI_B, HDMI_F, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        ret = True

        ret &= self.verify_hdmi_snps_phy(display_port, gfx_index)

        if ret is True:
            logging.info('PASS: PLL Register values programmed as per BSPEC')
        else:
            gdhm.report_bug(
                title='[Interfaces][Display_Engine]MTL_Clock_HDMI_Snps_Phy: PLL Register values not programmed as '
                      'per BSPEC',
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error('FAIL: PLL Register values not programmed as per BSPEC')
            ret = False

        return ret

    ##
    # @brief        Algorithm to calculate HDMI C10 phy values as per Bspec. It will fill values into c10 dictionary.
    #               Bspec ref: https://gfxspecs.intel.com/Predator/Home/Index/64568
    # @param[in]    display_port   port name like HDMI_B etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if calculation succeeded. False otherwise
    def calculate_hdmi_c10_phy_values(self, display_port, gfx_index):
        hdmi_symbol_freq_MHz = self.clock_helper.calculate_hdmi_symbol_freq(display_port, gfx_index)

        # if link rate is in standard link rates, fill the lookup table values
        link_rate_Gbps = round(hdmi_symbol_freq_MHz / 100, 8)
        if link_rate_Gbps in HDMI_C10_STANDARD_LINK_RATES:
            for attribute, value in C10Phy.__dict__.items():
                if attribute.startswith('__'):
                    continue
                # E.g for exec statement--> C10Phy.mpll_ssc_en = EXPECTED_C10_MPLL_SSC_EN[link_rate_Gbps]
                exec('C10Phy.' + attribute + ' = EXPECTED_C10_' + attribute.upper() + '[link_rate_Gbps]')
            return True

        CLOCK_100MHZ = 100000000
        CLOCK_10GHZ = 10000000000
        CLOCK_8GHZ = 8000000000
        CLOCK_4999MHZ = 4999999900
        CLOCK_16GHZ = 16000000000
        CLOCK_9999MHZ = 2 * CLOCK_4999MHZ

        # x axis frequencies.One curve in each array per v2i point.
        curve_freq_hz = [
            [2500000000, 3000000000, 3000000000, 3500000000, 3500000000, 4000000000, 4000000000, 5000000000],
            [4000000000, 4600000000, 4601000000, 5400000000, 5401000000, 6600000000, 6601000000, 8001000000]
        ]

        # y axis heights
        curve_0 = [
            [0.0411745, 0.0486055, 0.0429737, 0.0494331, 0.0424086, 0.0476819, 0.0402974, 0.0491314],
            [0.0820568, 0.0944207, 0.0823234, 0.0963706, 0.0812733, 0.0986301, 0.0817287, 0.0991057]
        ]
        curve_1 = [
            [733000000000.0, 660000000000.0, 831000000000.0, 753000000000.0, 997000000000.0, 923000000000.0,
             1250000000000.0, 1100000000000.0],
            [537000000000.0, 477000000000.0, 622000000000.0, 544000000000.0, 751000000000.0, 634000000000.0,
             906000000000.0, 763000000000.0]
        ]
        curve_2 = [
            [0.00241579, 0.00313646, 0.00258199, 0.00322267, 0.00252933, 0.00304202, 0.00233697, 0.00319146],
            [0.00480839, 0.00599425, 0.00483273, 0.00619373, 0.0047377, 0.00642875, 0.0047792, 0.00647934]
        ]

        # Helper function to calculate linear interpolation value. x= independent variable,
        # x1, y1= values of the function at one point, x2, y2= values of the function at another point
        def interp(x, x1, x2, y1, y2):
            dydx = (y2 - y1) / ((x2 - x1) * 1.0)
            return y1 + (dydx * int(x - x1))

        # calculation begins here
        offset = Gen14PllRegs.OFFSET_DSSM.DSSM
        value = DisplayArgs.read_register(offset, gfx_index)
        reg_dssm = Gen14PllRegs.REG_DSSM(offset, value)
        refclk = int(self.dssm_ref_freq_map[reg_dssm.ReferenceFrequency] * (10 ** 6))
        datarate = round((hdmi_symbol_freq_MHz * 10) * (10 ** 6))  # convert into Hz

        C10Phy.mpll_hdmi_pixel_clk_div = 0
        prescaler_divider = max(math.floor(math.log2(refclk / (50 * (10 ** 6)) )), 0)
        C10Phy.mpll_ssc_en = 0
        C10Phy.mpll_ssc_peak = 0
        C10Phy.mpll_ssc_stepsize = 0
        C10Phy.mpll_ssc_up_spread = 1
        C10Phy.mpll_word_div2_en = 0
        C10Phy.mpll_div5_en = 1
        C10Phy.mpll_div_multiplier = 0
        C10Phy.mpll_div_clk_en = 0
        C10Phy.mpll_hdmi_div = 1
        f_ana_div_clk = 0
        C10Phy.ref_range = 1
        C10Phy.mpll_ana_cp_int_gs = 30
        C10Phy.mpll_ana_cp_prop_gs = 28

        refclk_postscalar = refclk >> prescaler_divider

        # Calculate the VCO divider to get to datarate
        if datarate <= CLOCK_9999MHZ:
            mpll_ana_v2i = 2    # Select appropriate v2i point
            tx_clk_div = int(math.log2(CLOCK_9999MHZ / datarate))
        else:
            mpll_ana_v2i = 3 # Select appropriate v2i point
            tx_clk_div = int(math.log2(CLOCK_16GHZ / datarate))

        C10Phy.mpll_ana_v2i = mpll_ana_v2i
        C10Phy.mpll_tx_clk_div = tx_clk_div
        vco_clk = (datarate << tx_clk_div) >> 1

        # Highly accurate division, calculate fraction to 32 bits of precision
        vco_div_refclk_integer = int(vco_clk / refclk_postscalar)
        vco_div_refclk_fracn = int(((vco_clk % refclk_postscalar) << 32) / refclk_postscalar)
        C10Phy.mpll_fracn_quot = vco_div_refclk_fracn >> 16
        fracn_rem = vco_div_refclk_fracn & 0xffff
        fracn_rem = fracn_rem - (fracn_rem >> 15)
        C10Phy.mpll_fracn_rem = fracn_rem
        C10Phy.mpll_fracn_den = 0xffff
        C10Phy.mpll_fracn_en = 1 if (C10Phy.mpll_fracn_quot != 0 or fracn_rem != 0) else 0
        C10Phy.mpll_pmix_en = C10Phy.mpll_fracn_en
        C10Phy.mpll_multiplier = (vco_div_refclk_integer - 16) * 2

        # Curve selection for ana_cp_ * calculations.One curve hardcoded per v2i range
        c = mpll_ana_v2i - 2

        # Find the right segment of the table
        a = 0
        for j in range(8)[::2] :
            if vco_clk <= curve_freq_hz[c][j+1] :
                a = j
                ana_freq_vco = 3 - (a >> 1)
                break

        vco_div_refclk_float = vco_clk / refclk_postscalar
        o_397ced90 = interp(vco_clk, curve_freq_hz[c][a], curve_freq_hz[c][a + 1], curve_0[c][a], curve_0[c][a + 1])
        o_20c634d6 = interp(vco_clk, curve_freq_hz[c][a], curve_freq_hz[c][a + 1], curve_2[c][a], curve_2[c][a + 1])
        o_20c634d4 = interp(vco_clk, curve_freq_hz[c][a], curve_freq_hz[c][a + 1], curve_1[c][a], curve_1[c][a + 1])
        o_72019306 = o_20c634d6 * (4 - mpll_ana_v2i) / 16000
        o_6593e82b = o_20c634d6 * (4 - mpll_ana_v2i) / 160
        o_5cefc329 = 1120.08301 * vco_div_refclk_float / (o_397ced90 * o_20c634d4)
        ana_cp_int = max(1.0, min(round(o_5cefc329 / o_72019306), 127.0))
        C10Phy.mpll_cp_int = ana_cp_int
        o_49960328 = o_72019306 * ana_cp_int
        o_544adb37 = math.sqrt((o_20c634d4 * o_49960328 * o_397ced90 / (5.5e-11 * vco_div_refclk_float)))
        o_4ef74e66 = 1.460281 * vco_div_refclk_float * o_544adb37 / o_20c634d4
        C10Phy.mpll_cp_prop = max(1.0, min(round(o_4ef74e66 / o_6593e82b), 127.0))

        return True

    ##
    # @brief        Algorithm to calculate HDMI C20 phy values as per Bspec. It will fill values into c20 dictionary.
    #               Bspec ref: https://gfxspecs.intel.com/Predator/Home/Index/64568
    # @param[in]    display_port   port name like HDMI_G, HDMI_F etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if calculation succeeded. False otherwise
    def calculate_hdmi_c20_phy_values(self, display_port, gfx_index):
        hdmi_symbol_freq_MHz = self.clock_helper.calculate_hdmi_symbol_freq(display_port, gfx_index)

        # if link rate is in standard link rates, fill the lookup table values. this link rate calculation works only
        # for non-FRL link rates. TODO: modify once API is available to get FRL link rate for HDMI 2.1
        link_rate_Gbps = round(hdmi_symbol_freq_MHz / 100, 8)
        if link_rate_Gbps in HDMI_C20_STANDARD_LINK_RATES:
            for attribute, value in C20Phy.__dict__.items():
                if attribute.startswith('__'):
                    continue
                # E.g for exec statement--> C20Phy.mpll_ssc_peak = EXPECTED_C20_MPLL_SSC_PEAK[link_rate_Gbps]
                exec('C20Phy.' + attribute + ' = EXPECTED_C20_' + attribute.upper() + '[link_rate_Gbps]')
            return True

        datarate = int((hdmi_symbol_freq_MHz * 10) * (10 ** 6))         # Convert into Hz

        offset = Gen14PllRegs.OFFSET_DSSM.DSSM
        value = DisplayArgs.read_register(offset, gfx_index)
        reg_dssm = Gen14PllRegs.REG_DSSM(offset, value)
        refclk = int(self.dssm_ref_freq_map[reg_dssm.ReferenceFrequency] * (10**6))

        # As per Bspec, datarate should be <= 6G for HDMI TMDS Modes
        if not self.clock_helper.is_hdmi_2_1(display_port, gfx_index) and not datarate <= 6 * (10**9):
            logging.error(f'Invalid datarate for HDMI TMDS. Expected <= 6 Gbps. Actual = {datarate}')
            return False

        if not (refclk == 38400000):
            logging.error(f'Invalid refclk for HDMI. refclk = {refclk}')
            return False

        ref_ana_mpll_div = int(refclk / (10**8))
        C20Phy.mpll_tx_clk_div = int(math.log2(9999999999 / datarate))
        vco_freq = (datarate << int(math.log2(4999999999 * 256 / datarate))) >> 8
        multiplier = int((vco_freq << 28) / (refclk >> (ref_ana_mpll_div + 4)))
        C20Phy.mpll_multiplier = 2 * (multiplier >> 32)
        C20Phy.mpll_fracn_quot = (multiplier >> 16) & 0xffff
        C20Phy.mpll_fracn_rem = multiplier & 0xffff
        C20Phy.mpll_fracn_den = 65535
        C20Phy.mpll_fracn_en = 1

        C20Phy.mpll_div_multiplier = int(min((vco_freq * 16 + (datarate >> 1)) / datarate, 255))

        if vco_freq <= 3 * (10**9):
            C20Phy.mpllb_ana_freq_vco = 3
        elif vco_freq <= 3.5 * (10**9):
            C20Phy.mpllb_ana_freq_vco = 2
        elif vco_freq <= 4 * (10**9):
            C20Phy.mpllb_ana_freq_vco = 1
        else:
            C20Phy.mpllb_ana_freq_vco = 0

        C20Phy.mpll_div_clk_en = 0
        C20Phy.mpllb_hdmi_div = 1
        C20Phy.mpllb_ana_v2i = 2
        C20Phy.mpllb_ana_cp_int = 6
        C20Phy.mpllb_ana_cp_prop = 20
        C20Phy.mpllb_ana_cp_int_gs = 28
        C20Phy.mpllb_ana_cp_prop_gs = 30
        C20Phy.mpll_ssc_up_spread = 1
        C20Phy.mpll_ssc_peak = 0
        C20Phy.mpll_ssc_step_size = 0
        C20Phy.mpllb_word_clk_div = 1
        C20Phy.mpllb_hdmi_pixel_clk_div = 0
        C20Phy.ref_clk_mpllb_div = 0

        return True

    ##
    # @brief        helper function for extracting bits from one index to other index in an 32-bit integer
    #               e.g: extract_bits_from_int32 (240, 6, 3) will extract bits from [6:3] (both included)
    # @param[in]    value   any integer value (within 32 bit)
    # @param[in]    high_index     index from where to start extracting bits
    # @param[in]    low_index      index till where to do extracting bits
    # @return       returns the integer value that forms with extracted bits
    def extract_bits_from_int32(self, value, high_index, low_index):
        if high_index >= 32 or low_index >= 32 or high_index < low_index:
            logging.error(f'Cannot extract bits for given high_index ({high_index}) and low_index ({low_index}) '
                          f'in value ({bin(value)})')
            return None

        mask = 0
        for pos in range(low_index, high_index + 1):
            mask |= 1 << pos
        return (value & mask) >> low_index

    ##
    # @brief        wrapper function for HDMI Snps Phy verification
    # @param[in]    display_port   port name like HDMI_B, HDMI_F, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def verify_hdmi_snps_phy(self, display_port, gfx_index):
        port_name = str(display_port).split('_')[1]
        mtl_clock_helper = MtlClockHelper()
        display_port_name = mtl_clock_helper.ddi_to_bspec_name_map[port_name.upper()]

        # Ports A and B use C10 PHY.
        if 'USBC' not in display_port_name:
            return self.__verify_hdmi_snps_c10_phy(display_port, gfx_index)
        # All USBC ports use C20 PHY.
        else:
            # TODO: Temporary WA for SRAM register read failures, commenting out C20 PHY register reads
            # HSD: https://hsdes.intel.com/appstore/article/#/16018474191
            # TODO: Revisit when there is a permanent solution for C20 PHY reg read
            return True
            # return self.__verify_hdmi_snps_c20_phy(display_port, gfx_index)

    ##
    # @brief        this function contains HDMI Snps C20 Phy specific verification
    # @param[in]    display_port   port name like HDMI_F, HDMI_G, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def __verify_hdmi_snps_c20_phy(self, display_port, gfx_index):

        ret = True
        mtl_clock_helper = MtlClockHelper()
        is_hdmi_2p1_frl = self.clock_helper.is_hdmi_2_1(display_port, gfx_index)

        # Read PHY_C20_VDR_CUSTOM_SERDES_RATE[0].CONTEXT_TOGGLE.
        # This tells which context's register set driver has programmed.
        offset = MtlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_CUSTOM_SERDES.offset
        value = mtl_clock_helper.read_c10_phy_vdr_register(display_port, offset, gfx_index)
        vdr_custom_serdes = MtlSnpsPhyRegisters.REG_PHY_C10_VDR_CUSTOM_SERDES(offset, value)
        if vdr_custom_serdes.ContextToggle == 0:
            current_context = 'A'
        else:
            current_context = 'B'
        logging.info(f'Current selected context for {display_port} = CONTEXT_{current_context}')

        # Calculate HDMI C20 PHY values
        if not self.calculate_hdmi_c20_phy_values(display_port, gfx_index):
            logging.error('HDMI C20 PHY values calculation failed. Aborting verification.')
            return False

        # Read all C20 VDR registers
        snps = mtl_clock_helper.read_all_c20_sram_mpll_registers_helper(display_port, current_context, 'MPLLB',
                                                                        gfx_index)

        # Following below verifications are in this format :
        # "Algorithm Variable" will be verified as per its storage in respective registers.
        # HDMI always uses MPLLB registers.

        # ssc_en -> PORT_CLOCK_CTL. This is verified based on SSC support by display, in verify_port_slice()

        # ssc_peak -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[3:0],SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_4[15:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ssc_peak',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_ssc_peak, 19, 16)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_6.SscPeak])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_4 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ssc_peak',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_ssc_peak, 15, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_4.SscPeak])

        # ssc_stepsize -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[8:4],SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_5[15:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ssc_stepsize',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_ssc_step_size, 20, 16)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_6.SscStepSize])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_5 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ssc_stepsize',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_ssc_step_size, 15, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_5.SscStepSize])

        # ssc_up_spread -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[9]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ssc_up_spread',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_ssc_up_spread, 0, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_6.SscUpSpread])

        # frac_en -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[13]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'frac_en',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_fracn_en, 0, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_6.FracEn])

        # frac_rem -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_9[15:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_9 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'frac_rem',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_fracn_rem, 15, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_9.FracRem])

        # frac_quot -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_8[15:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_8 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'frac_quot',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_fracn_quot, 15, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_8.FracQuot])

        # frac_den -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_7[15:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_7 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'frac_den',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_fracn_den, 15, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_7.FracDen])

        # ref_clk_mpllb_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[12:10]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ref_clk_mpllb_div',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.ref_clk_mpllb_div, 2, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_6.RefClkDiv])

        # word_clk_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_1[9:8]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_1 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'word_clk_div',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpllb_word_clk_div, 1, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_1.WordClkDiv])

        # tx_clk_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_0[15:13]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_0 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'tx_clk_div',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_tx_clk_div, 2, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_0.TxClkDiv])

        # multiplier -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_0[11:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_0 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'multiplier',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_multiplier, 11, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_0.Multiplier])

        # div_multiplier -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_1[7:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_1 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'div_multiplier',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_div_multiplier, 7, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_1.DivMultiplier])

        # div_clk_en -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_0[12]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_0 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'div_clk_en',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpll_div_clk_en, 0, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_0.DivClkEn])

        # hdmi_pixel_clk_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_10[4:3]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_10 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'hdmi_pixel_clk_div',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpllb_hdmi_pixel_clk_div, 1, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_10.
                                                                  HdmiPixelClkDiv])

        # hdmi_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_10[2:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_10 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'hdmi_div',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpllb_hdmi_div, 2, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_10.HdmiDiv])

        # freq_vco -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_2[15:14]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_2 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'freq_vco',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpllb_ana_freq_vco, 1, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_2.FreqVco])

        # ana_cp_int_gs -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_3[6:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_3 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ana_cp_int_gs',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpllb_ana_cp_int_gs, 6, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_3.CpIntGs])

        # ana_cp_int -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_2[6:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_2 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ana_cp_int',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpllb_ana_cp_int, 6, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_2.CpInt])

        # ana_cp_prop_gs -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_3[13:7]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_3 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ana_cp_prop_gs',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpllb_ana_cp_prop_gs, 6, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_3.CpPropGs])

        # ana_cp_prop -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_2[13:7]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_2 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ana_cp_prop',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpllb_ana_cp_prop, 6, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_2.CpProp])

        # ana_v2i -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_3[15:14]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_3 '
                                                                     f'(of CONTEXT_{current_context})',
                                                                  parameter=f'ana_v2i',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C20Phy.mpllb_ana_v2i, 1, 0)],
                                                                  actual=[snps.sram_generic_mpllb_cntx_cfg_3.V2i])

        # Program custom width in VDR register at offset 0xD02 to match the link protocol (DP 2.0, HDMI 2.1, etc.)
        offset = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_CUSTOM_WIDTH.offset
        value = mtl_clock_helper.read_c10_phy_vdr_register(display_port, offset, gfx_index)
        vdr_custom_width = MtlSnpsPhyRegisters.REG_PHY_VDR_CUSTOM_WIDTH(offset, value)

        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'PHY_VDR_CUSTOM_WIDTH',
                                                                  parameter=f'CUSTOM_WIDTH',
                                                                  expected=[1 if is_hdmi_2p1_frl else 0],
                                                                  actual=[vdr_custom_width.CustomWidth])

        # Set PHY_C20_VDR_CUSTOM_SERDES_RATE[4:1].DP_RATE_IN_CUSTOM_SERDES to '0'.
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'PHY_C20_VDR_CUSTOM_SERDES_RATE',
                                                                  parameter=f'DP_RATE_IN_CUSTOM_SERDES',
                                                                  expected=[0],
                                                                  actual=[vdr_custom_serdes.DpRateInCustomSerdes])

        # If HDMI 2.1 FRL, set PHY_C20_VDR_CUSTOM_SERDES_RATE[7].IS_FRL to '1'.
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'PHY_C20_VDR_CUSTOM_SERDES_RATE',
                                                                  parameter=f'IS_FRL',
                                                                  expected=[1 if is_hdmi_2p1_frl else 0],
                                                                  actual=[vdr_custom_serdes.IsFrl])

        # Program PHY_C20_VDR_HDMI_RATE[1:0].HDMI_RATE
        offset = MtlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_HDMI_RATE.offset
        value = mtl_clock_helper.read_c10_phy_vdr_register(display_port, offset, gfx_index)
        vdr_hdmi_rate = MtlSnpsPhyRegisters.REG_PHY_C10_VDR_HDMI_RATE(offset, value)

        if not is_hdmi_2p1_frl:
            ret &= self.clock_helper.verify_port_clock_programming_ex(feature=f'PHY_C20_VDR_HDMI_RATE',
                                                                      parameter=f'HdmiRate',
                                                                      expected=[0],
                                                                      actual=[vdr_hdmi_rate.HdmiRate])
        else:
            pass        # TODO: find out right value of FrlRatePerLaneMbps in HDMI 2.1 cases

        return ret

    ##
    # @brief        this function contains HDMI Snps C10 Phy specific verification
    # @param[in]    display_port   port name like HDMI_B, HDMI_A, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def __verify_hdmi_snps_c10_phy(self, display_port, gfx_index):

        ret = True
        mtl_clock_helper = MtlClockHelper()

        # Calculate HDMI C10 PHY values
        if not self.calculate_hdmi_c10_phy_values(display_port, gfx_index):
            logging.error('HDMI C10 PHY values calculation failed. Aborting verification.')
            return False

        # Read all C10 VDR registers
        snps = mtl_clock_helper.read_all_c10_vdr_registers_helper(display_port, gfx_index)

        # Following below verifications are in this format :
        # "Algorithm Variable" will be verified as per its storage in respective registers.
        # HDMI always uses MPLLB registers.

        # mpll_ssc_en -> PORT_CLOCK_CTL. This is verified based on SSC support by display, in verify_port_slice()

        # mpll_tx_clk_div -> PHY_C10_VDR_PLL15[2:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL15',
                                                                  parameter='mpll_tx_clk_div',
                                                                  expected=[C10Phy.mpll_tx_clk_div],
                                                                  actual=[snps.phy_c10_vdr_pll15.TxClkDiv])

        # mpll_ssc_up_spread -> PHY_C10_VDR_PLL8[5]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL8',
                                                                  parameter='mpll_ssc_up_spread',
                                                                  expected=[C10Phy.mpll_ssc_up_spread],
                                                                  actual=[snps.phy_c10_vdr_pll8.SscUpSpread])

        # mpll_ssc_peak -> PHY_C10_VDR_PLL5[7:0], PHY_C10_VDR_PLL4[7:0], PHY_C10_VDR_PLL3[7:4]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL3',
                                                                  parameter='mpll_ssc_peak',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ssc_peak, 3, 0)],
                                                                  actual=[snps.phy_c10_vdr_pll3.SscPeak])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL4',
                                                                  parameter='mpll_ssc_peak',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ssc_peak, 11, 4)],
                                                                  actual=[snps.phy_c10_vdr_pll4.SscPeak])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL5',
                                                                  parameter='mpll_ssc_peak',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ssc_peak, 19, 12)],
                                                                  actual=[snps.phy_c10_vdr_pll5.SscPeak])

        # mpll_ssc_step_size -> PHY_C10_VDR_PLL8[4:0],PHY_C10_VDR_PLL7[7:0],PHY_C10_VDR_PLL6[7:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL6',
                                                                  parameter='mpll_ssc_step_size',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ssc_stepsize, 7, 0)],
                                                                  actual=[snps.phy_c10_vdr_pll6.SscStepsize])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL7',
                                                                  parameter='mpll_ssc_step_size',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ssc_stepsize, 15, 8)],
                                                                  actual=[snps.phy_c10_vdr_pll7.SscStepsize])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL8',
                                                                  parameter='mpll_ssc_step_size',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ssc_stepsize, 20, 16)],
                                                                  actual=[snps.phy_c10_vdr_pll8.SscStepsize])

        # mpll_div_clk_en -> PHY_C10_VDR_PLL0[1]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL0',
                                                                  parameter='mpll_div_clk_en',
                                                                  expected=[C10Phy.mpll_div_clk_en],
                                                                  actual=[snps.phy_c10_vdr_pll0.DivClkEn])

        # mpll_div5_clk_en -> PHY_C10_VDR_PLL0[2]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL0',
                                                                  parameter='mpll_div5_clk_en',
                                                                  expected=[C10Phy.mpll_div5_en],
                                                                  actual=[snps.phy_c10_vdr_pll0.Div5ClkEn])

        # mpll_word_div2_en -> PHY_C10_VDR_PLL0[3]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL0',
                                                                  parameter='mpll_word_div2_en',
                                                                  expected=[C10Phy.mpll_word_div2_en],
                                                                  actual=[snps.phy_c10_vdr_pll0.WordDiv2En])

        # mpll_fracn_en -> PHY_C10_VDR_PLL0[4]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL0',
                                                                  parameter='mpll_fracn_en',
                                                                  expected=[C10Phy.mpll_fracn_en],
                                                                  actual=[snps.phy_c10_vdr_pll0.FracnEn])

        # mpll_frac_den -> PHY_C10_VDR_PLL10[7:0],PHY_C10_VDR_PLL9[7:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL9',
                                                                  parameter='mpll_frac_den',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_fracn_den, 7, 0)],
                                                                  actual=[snps.phy_c10_vdr_pll9.FracnDen])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL10',
                                                                  parameter='mpll_frac_den',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_fracn_den, 15, 8)],
                                                                  actual=[snps.phy_c10_vdr_pll10.FracnDen])

        # mpll_frac_quot -> PHY_C10_VDR_PLL12[7:0],PHY_C10_VDR_PLL11[7:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL11',
                                                                  parameter='mpll_frac_quot',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_fracn_quot, 7, 0)],
                                                                  actual=[snps.phy_c10_vdr_pll11.FracnQuot])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL12',
                                                                  parameter='mpll_frac_quot',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_fracn_quot, 15, 8)],
                                                                  actual=[snps.phy_c10_vdr_pll12.FracnQuot])

        # mpll_frac_rem -> PHY_C10_VDR_PLL14[7:0],PHY_C10_VDR_PLL13[7:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL13',
                                                                  parameter='mpll_frac_rem',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_fracn_rem, 7, 0)],
                                                                  actual=[snps.phy_c10_vdr_pll13.FracnRem])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL14',
                                                                  parameter='mpll_frac_rem',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_fracn_rem, 15, 8)],
                                                                  actual=[snps.phy_c10_vdr_pll14.FracnRem])

        # mpll_pmix_en -> PHY_C10_VDR_PLL0[5]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL0',
                                                                  parameter='mpll_pmix_en',
                                                                  expected=[C10Phy.mpll_pmix_en],
                                                                  actual=[snps.phy_c10_vdr_pll0.PmixEn])

        # mpll_div_multiplier -> PHY_C10_VDR_PLL1[7:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL1',
                                                                  parameter='mpll_div_multiplier',
                                                                  expected=[C10Phy.mpll_div_multiplier],
                                                                  actual=[snps.phy_c10_vdr_pll1.DivMultiplier])

        # mpll_div_multiplier -> PHY_C10_VDR_PLL1[7:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL1',
                                                                  parameter='mpll_div_multiplier',
                                                                  expected=[C10Phy.mpll_div_multiplier],
                                                                  actual=[snps.phy_c10_vdr_pll1.DivMultiplier])

        # mpll_multiplier -> PHY_C10_VDR_PLL3[3:0],PHY_C10_VDR_PLL2[7:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL2',
                                                                  parameter='mpll_multiplier',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_multiplier, 7, 0)],
                                                                  actual=[snps.phy_c10_vdr_pll2.Multiplier])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL3',
                                                                  parameter='mpll_multiplier',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_multiplier, 11, 8)],
                                                                  actual=[snps.phy_c10_vdr_pll3.Multiplier])

        # mpll_tx_clk_div -> PHY_C10_VDR_PLL15[2:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL15',
                                                                  parameter='mpll_tx_clk_div',
                                                                  expected=[C10Phy.mpll_tx_clk_div],
                                                                  actual=[snps.phy_c10_vdr_pll15.TxClkDiv])

        # mpll_hdmi_div -> PHY_C10_VDR_PLL15[5:3]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL15',
                                                                  parameter='mpll_hdmi_div',
                                                                  expected=[C10Phy.mpll_hdmi_div],
                                                                  actual=[snps.phy_c10_vdr_pll15.HdmiDiv])

        # mpll_hdmi_pixel_clk_div -> PHY_C10_VDR_PLL15[7:6]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL15',
                                                                  parameter='mpll_hdmi_pixel_clk_div',
                                                                  expected=[C10Phy.mpll_hdmi_pixel_clk_div],
                                                                  actual=[snps.phy_c10_vdr_pll15.HdmiPixelClkDiv])

        # mpll_cp_int -> PHY_C10_VDR_PLL16[6:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL16',
                                                                  parameter='mpll_cp_int',
                                                                  expected=[C10Phy.mpll_cp_int],
                                                                  actual=[snps.phy_c10_vdr_pll16.CpInt])

        # mpll_cp_int_gs -> PHY_C10_VDR_PLL17[5:0],PHY_C10_VDR_PLL16[7]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL16',
                                                                  parameter='mpll_cp_int_gs',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ana_cp_int_gs, 0, 0)],
                                                                  actual=[snps.phy_c10_vdr_pll16.CpIntGs])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL17',
                                                                  parameter='mpll_cp_int_gs',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ana_cp_int_gs, 6, 1)],
                                                                  actual=[snps.phy_c10_vdr_pll17.CpIntGs])

        # mpll_cp_prop -> PHY_C10_VDR_PLL18[4:0], PHY_C10_VDR_PLL17[7:6]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL17',
                                                                  parameter='mpll_cp_prop',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_cp_prop, 1, 0)],
                                                                  actual=[snps.phy_c10_vdr_pll17.CpProp])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL18',
                                                                  parameter='mpll_cp_prop',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_cp_prop, 6, 2)],
                                                                  actual=[snps.phy_c10_vdr_pll18.CpProp])

        # mpll_cp_prop_gs -> PHY_C10_VDR_PLL19[3:0],PHY_C10_VDR_PLL18[7:5]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL18',
                                                                  parameter='mpll_cp_prop_gs',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ana_cp_prop_gs, 2, 0)],
                                                                  actual=[snps.phy_c10_vdr_pll18.CpPropGs])
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL19',
                                                                  parameter='mpll_cp_prop_gs',
                                                                  expected=[self.extract_bits_from_int32(
                                                                 C10Phy.mpll_ana_cp_prop_gs, 6, 3)],
                                                                  actual=[snps.phy_c10_vdr_pll19.CpPropGs])

        # mpll_ana_v2i -> PHY_C10_VDR_PLL19[5:4]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_PLL19',
                                                                  parameter='mpllb_ana_v2i',
                                                                  expected=[C10Phy.mpll_ana_v2i],
                                                                  actual=[snps.phy_c10_vdr_pll19.V2i])

        offset = MtlSnpsPhyRegisters.OFFSET_PHY_C10_VDR_CONTROL1.offset
        phy_c10_vdr_control1_value = mtl_clock_helper.read_c10_phy_vdr_register(display_port, offset, gfx_index)
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_CONTROL1',
                                                                  parameter='reg_value',
                                                                  expected=[0x6],
                                                                  actual=[phy_c10_vdr_control1_value])

        # Program custom width in VDR register at offset 0xD02 to match the link protocol (8b/10b mode (value 0) always
        # for C10 displays)
        offset = MtlSnpsPhyRegisters.OFFSET_PHY_VDR_CUSTOM_WIDTH.offset
        value = mtl_clock_helper.read_c10_phy_vdr_register(display_port, offset, gfx_index)
        vdr_custom_width = MtlSnpsPhyRegisters.REG_PHY_VDR_CUSTOM_WIDTH(offset, value)

        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_VDR_CUSTOM_WIDTH',
                                                                  parameter='CUSTOM_WIDTH',
                                                                  expected=[0],
                                                                  actual=[vdr_custom_width.CustomWidth])

        # ref_range -> PHY_C10_VDR_CMN0[4:0]
        ret &= self.clock_helper.verify_port_clock_programming_ex(feature='PHY_C10_VDR_CMN0',
                                                                  parameter='ref_range',
                                                                  expected=[C10Phy.ref_range],
                                                                  actual=[snps.phy_c10_vdr_cmn0.RefRange])

        return ret
