######################################################################################
# @file         elg_clock_hdmi_snps_phy.py
# @brief        Contains HDMI specific part of ELG Synopsys PHY (C20) verification and HDMI algorithms.
# @details      Bspec references:
#               BSPEC page: https://gfxspecs.intel.com/Predator/Home/Index/74165?dstFilter=BMG&mode=Filter
# @author       Goutham N
######################################################################################

import math
import logging

from Libs.Core.logger import gdhm
from Libs.Core.system_utility import SystemUtility
from Libs.Feature.clock.elg.elg_clock_helper import ElgClockHelper
from Libs.Feature.clock import clock_helper as clk_helper
from DisplayRegs import DisplayArgs
from DisplayRegs.Gen14.Pll import Gen14PllRegs
from DisplayRegs.Gen14 import ElgSnpsPhyRegisters

HDMI_C20_STANDARD_LINK_RATES = [0.25175, 0.27, 0.7425, 1.485, 5.94, 3.0, 6.0, 8.0, 10.0, 12.0]  # In Gbps

# These PLL values are only for standard HDMI link rates with reference clock set to 38.4 MHz given in Bspec table
# (https://gfxspecs.intel.com/Predator/Home/Index/74165?dstFilter=BMG&mode=Filter). Values are in decimals.
# For any other link rate, we will use the HDMI PLL programming algorithm.

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
# @brief        This is the class containing ELG HDMI Snps Phy related verifications
class ElgClockHdmiSnpsPhy:

    ##
    # @brief        Function that will be called from tests for ELG clock verification on DP displays
    # @param[in]    display_port   port name like HDMI_B, HDMI_F, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def verify_clock(self, gfx_index: str, display_port):
        ret = True

        ret &= self.verify_hdmi_snps_phy(gfx_index, display_port)

        if ret is True:
            logging.info('PASS: PLL Register values programmed as per BSPEC')
        else:
            gdhm.report_test_bug_di('[Interfaces][Display_Engine]ELG_Clock_HDMI_Snps_Phy: PLL Register values not '
                                    'programmed as per BSPEC')
            logging.error('FAIL: PLL Register values not programmed as per BSPEC')
            ret = False

        return ret

    ##
    # @brief        Algorithm to calculate HDMI C20 phy values as per Bspec. It will fill values into c20 dictionary.
    #               Bspec ref: https://gfxspecs.intel.com/Predator/Home/Index/68862
    # @param[in]    display_port   port name like HDMI_G, HDMI_F etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if calculation succeeded. False otherwise
    def calculate_hdmi_c20_phy_values(self, gfx_index, display_port):
        clock_helper = clk_helper.ClockHelper()
        hdmi_symbol_freq_MHz = clock_helper.calculate_hdmi_symbol_freq(display_port, gfx_index)

        # if link rate is in standard link rates, fill the lookup table values. this link rate calculation works only
        # for non-FRL link rates. TODO: modify once API is available to get FRL link rate for HDMI 2.1
        link_rate_Gbps = round(hdmi_symbol_freq_MHz / 100, 8)
        if link_rate_Gbps in HDMI_C20_STANDARD_LINK_RATES:
            for attribute, value in vars(C20Phy).items():
                if attribute.startswith('__'):
                    continue
                # E.g for exec statement--> C20Phy.mpll_ssc_peak = EXPECTED_C20_MPLL_SSC_PEAK[link_rate_Gbps]
                exec('C20Phy.' + attribute + ' = EXPECTED_C20_' + attribute.upper() + '[link_rate_Gbps]')
            return True

        datarate = int((hdmi_symbol_freq_MHz * 10) * (10 ** 6))  # Convert into Hz
        refclk = int(clock_helper.get_reference_clock_from_register(gfx_index) * (10**6))

        # As per Bspec, datarate should be <= 6G for HDMI TMDS Modes
        if not clock_helper.is_hdmi_2_1(display_port, gfx_index) and not datarate <= 6 * (10**9):
            logging.error(f'Invalid datarate for HDMI TMDS. Expected <= 6 Gbps. Actual = {datarate}')
            return False

        if not (refclk == 38400000):
            logging.error(f'Invalid refclk for HDMI. refclk = {refclk}')
            return False

        ref_ana_mpll_div = int(refclk / (10 ** 8))
        C20Phy.mpll_tx_clk_div = int(math.log2(9999999999 / datarate))
        vco_freq = (datarate << int(math.log2(4999999999 * 256 / datarate))) >> 8
        multiplier = int((vco_freq << 28) / (refclk >> (ref_ana_mpll_div + 4)))
        C20Phy.mpll_multiplier = 2 * (multiplier >> 32)
        C20Phy.mpll_fracn_quot = (multiplier >> 16) & 0xffff
        C20Phy.mpll_fracn_rem = multiplier & 0xffff
        C20Phy.mpll_fracn_den = 65535
        C20Phy.mpll_fracn_en = 1

        C20Phy.mpll_div_multiplier = int(min((vco_freq * 16 + (datarate >> 1)) / datarate, 255))

        if vco_freq <= 3 * (10 ** 9):
            C20Phy.mpllb_ana_freq_vco = 3
        elif vco_freq <= 3.5 * (10 ** 9):
            C20Phy.mpllb_ana_freq_vco = 2
        elif vco_freq <= 4 * (10 ** 9):
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
    def verify_hdmi_snps_phy(self, gfx_index, display_port):

        # All ports use C20 PHY.
        # TODO: There is a known failure in MTL where SRAM reg read will fail. If the same
        #  failure is seen in BMG, skip here as well

        # Skip this verification in pre-si as MSG BUS transactions not supported in pre-si (simulation)
        execution_environment_type = SystemUtility().get_execution_environment_type()
        if execution_environment_type is None or execution_environment_type != "POST_SI_ENV":
            logging.info("Skipping PHY SRAM Registers verification on pre-si as the environment doesn't "
                         "support MSG BUS transaction")
            return True

        # TODO: Temporary WA for SRAM register read failures, commenting out C20 PHY register reads
        # HSD: https://hsdes.intel.com/appstore/article/#/16018474191
        # TODO: Revisit when there is a permanent solution for C20 PHY reg read
        return True
        # return self.__verify_hdmi_snps_c20_phy(gfx_index, display_port)

    ##
    # @brief        this function contains HDMI Snps C20 Phy specific verification
    # @param[in]    display_port   port name like HDMI_F, HDMI_G, etc
    # @param[in]    gfx_index      adapter index like 'gfx_0'
    # @return       BOOL : returns True if all verification passed, False otherwise
    def __verify_hdmi_snps_c20_phy(self, gfx_index, display_port):
        clock_helper = clk_helper.ClockHelper()
        ret = True
        elg_clock_helper = ElgClockHelper()
        is_hdmi_2p1_frl = clock_helper.is_hdmi_2_1(display_port, gfx_index)

        # Read PHY_C20_VDR_CUSTOM_SERDES_RATE[0].CONTEXT_TOGGLE.
        # This tells which context's register set driver has programmed.
        offset = ElgSnpsPhyRegisters.OFFSET_PHY_C20_VDR_CUSTOM_SERDES.offset
        value = elg_clock_helper.read_c20_phy_vdr_register(gfx_index, display_port, offset)
        vdr_custom_serdes = ElgSnpsPhyRegisters.REG_PHY_C20_VDR_CUSTOM_SERDES(offset, value)
        if vdr_custom_serdes.ContextToggle == 0:
            current_context = 'A'
        else:
            current_context = 'B'
        logging.info(f'Current selected context for {display_port} = CONTEXT_{current_context}')

        # Calculate HDMI C20 PHY values
        if not self.calculate_hdmi_c20_phy_values(gfx_index, display_port):
            logging.error('HDMI C20 PHY values calculation failed. Aborting verification.')
            return False

        # Read all C20 VDR registers
        snps = elg_clock_helper.read_all_c20_sram_mpll_registers_helper(gfx_index, display_port, current_context,
                                                                        'MPLLB')

        # Following below verifications are in this format :
        # "Algorithm Variable" will be verified as per its storage in respective registers.
        # HDMI always uses MPLLB registers.

        # ssc_en -> PORT_CLOCK_CTL. This is verified based on SSC support by display, in verify_port_slice()

        # ssc_peak -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[3:0],SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_4[15:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ssc_peak',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_ssc_peak, 19, 16)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_6.SscPeak])
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_4 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ssc_peak',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_ssc_peak, 15, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_4.SscPeak])

        # ssc_stepsize -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[8:4],SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_5[15:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ssc_stepsize',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_ssc_step_size, 20, 16)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_6.SscStepSize])
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_5 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ssc_stepsize',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_ssc_step_size, 15, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_5.SscStepSize])

        # ssc_up_spread -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[9]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ssc_up_spread',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_ssc_up_spread, 0, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_6.SscUpSpread])

        # frac_en -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[13]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'frac_en',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_fracn_en, 0, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_6.FracEn])

        # frac_rem -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_9[15:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_9 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'frac_rem',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_fracn_rem, 15, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_9.FracRem])

        # frac_quot -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_8[15:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_8 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'frac_quot',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_fracn_quot, 15, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_8.FracQuot])

        # frac_den -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_7[15:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_7 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'frac_den',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_fracn_den, 15, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_7.FracDen])

        # ref_clk_mpllb_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_6[12:10]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_6 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ref_clk_mpllb_div',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.ref_clk_mpllb_div, 2, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_6.RefClkDiv])

        # word_clk_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_1[9:8]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_1 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'word_clk_div',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpllb_word_clk_div, 1, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_1.WordClkDiv])

        # tx_clk_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_0[15:13]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_0 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'tx_clk_div',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_tx_clk_div, 2, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_0.TxClkDiv])

        # multiplier -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_0[11:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_0 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'multiplier',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_multiplier, 11, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_0.Multiplier])

        # div_multiplier -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_1[7:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_1 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'div_multiplier',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_div_multiplier, 7, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_1.DivMultiplier])

        # div_clk_en -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_0[12]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_0 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'div_clk_en',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpll_div_clk_en, 0, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_0.DivClkEn])

        # hdmi_pixel_clk_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_10[4:3]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_10 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'hdmi_pixel_clk_div',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpllb_hdmi_pixel_clk_div, 1, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_10.
                                                             HdmiPixelClkDiv])

        # hdmi_div -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_10[2:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_10 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'hdmi_div',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpllb_hdmi_div, 2, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_10.HdmiDiv])

        # freq_vco -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_2[15:14]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_2 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'freq_vco',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpllb_ana_freq_vco, 1, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_2.FreqVco])

        # ana_cp_int_gs -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_3[6:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_3 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ana_cp_int_gs',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpllb_ana_cp_int_gs, 6, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_3.CpIntGs])

        # ana_cp_int -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_2[6:0]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_2 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ana_cp_int',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpllb_ana_cp_int, 6, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_2.CpInt])

        # ana_cp_prop_gs -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_3[13:7]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_3 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ana_cp_prop_gs',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpllb_ana_cp_prop_gs, 6, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_3.CpPropGs])

        # ana_cp_prop -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_2[13:7]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_2 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ana_cp_prop',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpllb_ana_cp_prop, 6, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_2.CpProp])

        # ana_v2i -> SRAM_GENERIC_<A/B>_MPLLB_CNTX_CFG_3[15:14]
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'SRAM_GENERIC_MPLLB_CNTX_CFG_3 '
                                                                f'(of CONTEXT_{current_context})',
                                                             parameter=f'ana_v2i',
                                                             expected=[self.extract_bits_from_int32(
                                                            C20Phy.mpllb_ana_v2i, 1, 0)],
                                                             actual=[snps.sram_generic_mpllb_cntx_cfg_3.V2i])

        # Program custom width in VDR register at offset 0xD02 to match the link protocol (DP 2.0, HDMI 2.1, etc.)
        offset = ElgSnpsPhyRegisters.OFFSET_PHY_VDR_CUSTOM_WIDTH.offset
        value = elg_clock_helper.read_c20_phy_vdr_register(gfx_index, display_port, offset)
        vdr_custom_width = ElgSnpsPhyRegisters.REG_PHY_VDR_CUSTOM_WIDTH(offset, value)

        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'PHY_VDR_CUSTOM_WIDTH',
                                                             parameter=f'CUSTOM_WIDTH',
                                                             expected=[1 if is_hdmi_2p1_frl else 0],
                                                             actual=[vdr_custom_width.CustomWidth])

        # Set PHY_C20_VDR_CUSTOM_SERDES_RATE[4:1].DP_RATE_IN_CUSTOM_SERDES to '0'.
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'PHY_C20_VDR_CUSTOM_SERDES_RATE',
                                                             parameter=f'DP_RATE_IN_CUSTOM_SERDES',
                                                             expected=[0],
                                                             actual=[vdr_custom_serdes.DpRateInCustomSerdes])

        # If HDMI 2.1 FRL, set PHY_C20_VDR_CUSTOM_SERDES_RATE[7].IS_FRL to '1'.
        ret &= clock_helper.verify_port_clock_programming_ex(feature=f'PHY_C20_VDR_CUSTOM_SERDES_RATE',
                                                             parameter=f'IS_FRL',
                                                             expected=[1 if is_hdmi_2p1_frl else 0],
                                                             actual=[vdr_custom_serdes.IsFrl])

        # Program PHY_C20_VDR_HDMI_RATE[1:0].HDMI_RATE
        offset = ElgSnpsPhyRegisters.OFFSET_PHY_C20_VDR_HDMI_RATE.offset
        value = elg_clock_helper.read_c20_phy_vdr_register(gfx_index, display_port, offset)
        vdr_hdmi_rate = ElgSnpsPhyRegisters.REG_PHY_C20_VDR_HDMI_RATE(offset, value)

        if not is_hdmi_2p1_frl:
            ret &= clock_helper.verify_port_clock_programming_ex(feature=f'PHY_C20_VDR_HDMI_RATE',
                                                                 parameter=f'HdmiRate',
                                                                 expected=[0],
                                                                 actual=[vdr_hdmi_rate.HdmiRate])
        else:
            pass  # TODO: find out right value of FrlRatePerLaneMbps in HDMI 2.1 cases

        return ret
