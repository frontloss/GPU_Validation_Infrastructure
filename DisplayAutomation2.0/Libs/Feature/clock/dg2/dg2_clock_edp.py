##
# @file    dg2_clock_edp.py
# @brief   This tests EDP PLLS are programmed correctly for platform DG2. Can be used in EDP tests.
# @author  Kruti Vadhavaniya

import logging

from Libs.Feature.clock import clock_helper as clk_helper
from Libs.Feature.clock.dg2 import dg2_clock_registers
from Libs.Feature.display_port import dpcd_helper
from Libs.Core.logger import gdhm


clock_helper = clk_helper.ClockHelper()
dg2_clock_reg = dg2_clock_registers.Dg2ClockRegisters()

edp = 0


##
# @brief edp clock cp class
class EdpClockCp():
    ref_range = 0
    cp_init = 0
    cp_prop = 0
    cp_gs = 0
    cp_prop_gs = 0


##
# @brief edp clock DIV class
class EdpClockDiv():
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
# @brief edp clock fractional class
class EdpClockFracn():
    fracn_en = 0
    fracn_den = 0
    cfg_update_en = 0
    fracn_quot = 0
    fracn_rem = 0


##
# @brief edp clock SSC class
class EdpClockSsc():
    ssc_en = 0
    ssc_ip_spread = 0
    ssc_peak = 0
    ssc_ste_size = 0


##
# DP PLL value dictionary with reference clock 100MHz
DPModePLLValueRefClk100Mhz = {
    0: {"LinkRateMbps": 1620, "ref_range": 3, "clk_div": 2, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 226,
        "FracnEn": 1, "FracnQuot": 39321, "FracnRem": 3, "FracnDen": 5, "SscUpSpread": 0, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 2, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 2, "CpInit": 4, "CpProp": 20, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    1: {"LinkRateMbps": 1620, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 226,
        "FracnEn": 1, "FracnQuot": 39321, "FracnRem": 3, "FracnDen": 5, "SscUpSpread": 0, "SscPeak": 38221,
        "SscStepSize": 49314, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 2, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 2, "CpInit": 4, "CpProp": 20, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    2: {"LinkRateMbps": 2700, "ref_range": 3, "clk_div": 2, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 184,
        "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 1, "PmixEn": 0, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 4, "CpProp": 20, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    3: {"LinkRateMbps": 2700, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 184,
        "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 31850,
        "SscStepSize": 41095, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 1, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 4, "CpProp": 20, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    4: {"LinkRateMbps": 5400, "ref_range": 3, "clk_div": 2, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 184,
        "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 0, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 4, "CpProp": 20, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    5: {"LinkRateMbps": 5400, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 184,
        "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 31850,
        "SscStepSize": 41095, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 4, "CpProp": 20, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    6: {"LinkRateMbps": 8100, "ref_range": 3, "clk_div": 2, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 292,
        "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 0, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 0, "CpInit": 4, "CpProp": 19, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    7: {"LinkRateMbps": 8100, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 292,
        "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 47776,
        "SscStepSize": 61642, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 0, "CpInit": 4, "CpProp": 19, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    # edp Mode PLL value
    8: {"LinkRateMbps": 2160, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 312,
        "FracnEn": 1, "FracnQuot": 52428, "FracnRem": 4, "FracnDen": 5, "SscUpSpread": 0, "SscPeak": 50961,
        "SscStepSize": 65752, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 2, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 0, "CpInit": 4, "CpProp": 19, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 1,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    9: {"LinkRateMbps": 2430, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 356,
        "FracnEn": 1, "FracnQuot": 26214, "FracnRem": 2, "FracnDen": 5, "SscUpSpread": 0, "SscPeak": 57331,
        "SscStepSize": 73971, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 2, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 0, "CpInit": 4, "CpProp": 20, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 1,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    10: {"LinkRateMbps": 3230, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 226,
         "FracnEn": 1, "FracnQuot": 39321, "FracnRem": 3, "FracnDen": 5, "SscUpSpread": 0, "SscPeak": 38221,
         "SscStepSize": 49314, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 1, "PmixEn": 1, "WordDiv2En": 0,
         "V2i": 2, "FreqVco": 2, "CpInit": 4, "CpProp": 20, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 1,
         "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    11: {"LinkRateMbps": 4320, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 312,
         "FracnEn": 1, "FracnQuot": 52428, "FracnRem": 4, "FracnDen": 5, "SscUpSpread": 0, "SscPeak": 50961,
         "SscStepSize": 65752, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 1, "PmixEn": 1, "WordDiv2En": 0,
         "V2i": 2, "FreqVco": 0, "CpInit": 4, "CpProp": 19, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 1,
         "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    # UHBR
    12: {"LinkRateMbps": 10000, "ref_range": 3, "clk_div": 2, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 368,
         "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
         "SscStepSize": 0, "DivClkEn": 1, "DivMult": 8, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 0, "WordDiv2En": 1,
         "V2i": 2, "FreqVco": 0, "CpInit": 4, "CpProp": 21, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
         "DPShimDiv32ClkSel": 1, "DP2Mode": 1, "CfgUpdateEn": 1},
    13: {"LinkRateMbps": 10000, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 368,
         "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 58982,
         "SscStepSize": 76101, "DivClkEn": 1, "DivMult": 8, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 1,
         "V2i": 2, "FreqVco": 0, "CpInit": 4, "CpProp": 21, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
         "DPShimDiv32ClkSel": 1, "DP2Mode": 1, "CfgUpdateEn": 1},
    14: {"LinkRateMbps": 13500, "ref_range": 3, "clk_div": 2, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 508,
         "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
         "SscStepSize": 0, "DivClkEn": 1, "DivMult": 8, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 0, "WordDiv2En": 1,
         "V2i": 3, "FreqVco": 0, "CpInit": 5, "CpProp": 45, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
         "DPShimDiv32ClkSel": 1, "DP2Mode": 1, "CfgUpdateEn": 1},
    15: {"LinkRateMbps": 13500, "ref_range": 3, "clk_div": 2, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 508,
         "FracnEn": 0, "FracnQuot": 0, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 79626,
         "SscStepSize": 102737, "DivClkEn": 1, "DivMult": 8, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 1,
         "V2i": 3, "FreqVco": 0, "CpInit": 5, "CpProp": 45, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
         "DPShimDiv32ClkSel": 1, "DP2Mode": 1, "CfgUpdateEn": 1},
}


##
# DP PLL value dictionary with reference clock 38p4MHz
DPModePLLValueRefClk38p4Mhz = {
    0: {"LinkRateMbps": 1620, "ref_range": 1, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 304,
        "FracnEn": 1, "FracnQuot": 49152, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 2, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 2, "CpInit": 5, "CpProp": 25, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    1: {"LinkRateMbps": 1620, "ref_range": 1, "clk_div": 1, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 304,
        "FracnEn": 1, "FracnQuot": 49152, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 49766,
        "SscStepSize": 83608, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 2, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 2, "CpInit": 5, "CpProp": 25, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    2: {"LinkRateMbps": 2700, "ref_range": 1, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 248,
        "FracnEn": 1, "FracnQuot": 40960, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 1, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 5, "CpProp": 25, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    3: {"LinkRateMbps": 2700, "ref_range": 1, "clk_div": 1, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 248,
        "FracnEn": 1, "FracnQuot": 40960, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 41472,
        "SscStepSize": 69673, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 1, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 5, "CpProp": 25, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    4: {"LinkRateMbps": 5400, "ref_range": 1, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 248,
        "FracnEn": 1, "FracnQuot": 40960, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 0 , "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 5, "CpProp": 25, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    5: {"LinkRateMbps": 5400, "ref_range": 1, "clk_div": 1, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 248,
        "FracnEn": 1, "FracnQuot": 40960, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 41472,
        "SscStepSize": 69673, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 3, "CpInit": 5, "CpProp": 25, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    6: {"LinkRateMbps": 8100, "ref_range": 1, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 388,
        "FracnEn": 1, "FracnQuot": 61440, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
        "SscStepSize": 0, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 0, "CpInit": 6, "CpProp": 26, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    7: {"LinkRateMbps": 8100, "ref_range": 1, "clk_div": 1, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 388,
        "FracnEn": 1, "FracnQuot": 61440, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 62208,
        "SscStepSize": 104509, "DivClkEn": 0, "DivMult": 0, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 0,
        "V2i": 2, "FreqVco": 0, "CpInit": 6, "CpProp": 26, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
        "DPShimDiv32ClkSel": 0, "DP2Mode": 0, "CfgUpdateEn": 1},
    # edp Mode PLL value
    8: {0},
    9: {0},
    10: {0},
    11: {0},
    # UHBR
    12: {"LinkRateMbps": 10000, "ref_range": 1, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 488,
         "FracnEn": 1, "FracnQuot": 27306, "FracnRem": 2, "FracnDen": 3, "SscUpSpread": 0, "SscPeak": 0,
         "SscStepSize": 0, "DivClkEn": 1, "DivMult": 8, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 1,
         "V2i": 2, "FreqVco": 0, "CpInit": 5, "CpProp": 26, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
         "DPShimDiv32ClkSel": 1, "DP2Mode": 1, "CfgUpdateEn": 1},
    13: {"LinkRateMbps": 10000, "ref_range": 1, "clk_div": 1, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 488,
         "FracnEn": 1, "FracnQuot": 27306, "FracnRem": 2, "FracnDen": 3, "SscUpSpread": 0, "SscPeak": 76800,
         "SscStepSize": 129024, "DivClkEn": 1, "DivMult": 8, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 1,
         "V2i": 2, "FreqVco": 0, "CpInit": 5, "CpProp": 26, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
         "DPShimDiv32ClkSel": 1, "DP2Mode": 1, "CfgUpdateEn": 1},
    14: {"LinkRateMbps": 13500, "ref_range": 1, "clk_div": 1, "SscEn": 0, "Div5ClkEn": 1, "Multiplier": 670,
         "FracnEn": 1, "FracnQuot": 36864, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 0,
         "SscStepSize": 0, "DivClkEn": 1, "DivMult": 8, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 1,
         "V2i": 3, "FreqVco": 0, "CpInit": 6, "CpProp": 56, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
         "DPShimDiv32ClkSel": 1, "DP2Mode": 1, "CfgUpdateEn": 1},
    15: {"LinkRateMbps": 13500, "ref_range": 1, "clk_div": 1, "SscEn": 1, "Div5ClkEn": 1, "Multiplier": 670,
         "FracnEn": 1, "FracnQuot": 36864, "FracnRem": 0, "FracnDen": 1, "SscUpSpread": 0, "SscPeak": 103680,
         "SscStepSize": 174182, "DivClkEn": 1, "DivMult": 8, "HdmiDiv": 0, "TxClkDiv": 0, "PmixEn": 1, "WordDiv2En": 1,
         "V2i": 3, "FreqVco": 0, "CpInit": 6, "CpProp": 56, "CpGs": 65, "CpPropGs": 127, "PixelClkDiv": 0, "skipssc": 0,
         "DPShimDiv32ClkSel": 1, "DP2Mode": 1, "CfgUpdateEn": 1},
}


##
# @brief DG2 edp clock verification class
class Dg2ClockEdp():
    # Mapping of the listed port ref_clk
    port_ref_clk_map = dict([
        (38.4, 0),
        (100, 1)
    ])

    # Mapping of the listed Reference Frequencies
    dssm_ref_freq_map = dict([
        (24, 0),
        (19.2, 1),
        (38.4, 2),
        (25, 3)
    ])

    ##
    # @brief function to validate EDP Pll divider values are programmed correctly.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which clock verification
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_clock(self, display_port, gfx_index='gfx_0'):
        port_ref_clk = 100
        port_name = ''
        logging.debug("Check for which DPLL is being used")
        reg_value = clock_helper.clock_register_read('DPCLKA_CFGCR0_REGISTER', 'DPCLKA_CFGCR0', gfx_index)
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
            # Read Ref control for port_ref_clock
            reg_val_ref_ctrl = clock_helper.clock_register_read('SNPS_PHY_REF_CONTROL_REGISTER',
                                                                'SNPS_PHY_REF_CONTROL_PORT_TC1', gfx_index)
            port_ref_clk = clock_helper.get_value_by_range(reg_val_ref_ctrl, 24, 24, self.port_ref_clk_map, 'ref_clk')
            logging.info("port_ref_clk from SNPS_PHY_REF_CRL_reg{}".format(port_ref_clk))
        else:
            logging.info("ERROR:Provided port is not valid for DG2")

        if dg2_clock_reg.verify_pll_enable(display_port, port_name, gfx_index) is False:
            return False

        dg2_clock_registers.ClockRegister.MPLLB_CP = 'SNPS_PHY_MPLLB_CP_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_DIV = 'SNPS_PHY_MPLLB_DIV_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_DIV2 = 'SNPS_PHY_MPLLB_DIV2_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_FRACN1 = 'SNPS_PHY_MPLLB_FRACN1_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_FRACN2 = 'SNPS_PHY_MPLLB_FRACN2_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_SSCEN = 'SNPS_PHY_MPLLB_SSCEN_' + port_name
        dg2_clock_registers.ClockRegister.MPLLB_SSCSTEP = 'SNPS_PHY_MPLLB_SSCSTEP_' + port_name
        dg2_clock_registers.ClockRegister.REF_CONTROL = 'SNPS_PHY_REF_CONTROL_' + port_name

        logging.info("{}".format(dg2_clock_registers.ClockRegister.MPLLB_CP))
        adapter_info = clock_helper.get_adapter_info(display_port, gfx_index)
        link_bw = dpcd_helper.DPCD_getLinkRate(adapter_info)
        logging.info("link_bw from DPCD{}".format(link_bw))

        ret, pll_values = self.get_edp_pll_ref_values(link_bw, port_ref_clk, display_port, gfx_index)

        if ret is True:
            if self.verify_edp_pll(pll_values, display_port, gfx_index) is True:
                logging.debug("PASS : PLL Register values Programmed as per BSPEC")
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine]DG2_Clock_EDP: PLL Register values {0} not programmed as "
                          "per BSPEC".format(pll_values),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error("FAIL : PLL Register values NOT Programmed as per BSPEC")
                ret = False
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine]DG2_Clock_EDP:Failed getting reference pll values"
                      " for: link rate {0} ref clk {1}".format(str(link_bw), str(port_ref_clk)),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("Failed getting Reference PLL values for Link Rate: "
                          + str(link_bw) + "ref clk :" + str(port_ref_clk))
            ret = False

        return ret

    ##
    # @brief function to validate EDP Pll divider values are programmed correctly.
    # @param[in] pll_values - pll_values dictionary
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which register read
    # @return BOOL test pass/fail : Pass = 0 , Fail = non-zero fail count
    def verify_edp_pll(self, pll_values, display_port, gfx_index='gfx_0'):
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

        if pll_values["skipssc"] != 1:
            ssc_en &= clock_helper.get_ssc_from_dpcd(display_port, gfx_index)

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

        reg_read_cp = EdpClockCp()
        reg_read_cp.ref_range = clock_helper.get_value_by_range(reg_ref_control, 27, 31, '', 'Ref Range')
        reg_read_cp.cp_init = clock_helper.get_value_by_range(reg_mpllb_cp, 25, 31, '', 'CP Init')
        reg_read_cp.cp_gs = clock_helper.get_value_by_range(reg_mpllb_cp, 17, 23, '', 'CP Gs')
        reg_read_cp.cp_prop = clock_helper.get_value_by_range(reg_mpllb_cp, 9, 15, '', 'CP Prop')
        reg_read_cp.cp_prop_gs = clock_helper.get_value_by_range(reg_mpllb_cp, 1, 7, '', 'CP prop Gs')

        reg_read_div = EdpClockDiv()
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

        reg_read_fracn = EdpClockFracn()
        reg_read_fracn.fracn_en = clock_helper.get_value_by_range(reg_mpllb_fracn1, 31, 31, '', 'Fracn En')
        reg_read_fracn.cfg_update_en = clock_helper.get_value_by_range(reg_mpllb_fracn1, 30, 30, '', 'cfg update en')
        reg_read_fracn.fracn_den = clock_helper.get_value_by_range(reg_mpllb_fracn1, 0, 15, '', 'Fracn Den')
        reg_read_fracn.fracn_rem = clock_helper.get_value_by_range(reg_mpllb_fracn2, 16, 31, '', 'Fracn Rem')
        reg_read_fracn.fracn_quot = clock_helper.get_value_by_range(reg_mpllb_fracn2, 0, 15, '', 'Fracn Quot')

        reg_read_ssc = EdpClockSsc()
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
            actual= [reg_read_fracn.fracn_en, reg_read_fracn.cfg_update_en, reg_read_fracn.fracn_den])

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
    # @brief function to get reference pll divider values based on bspec.
    # @param[in] link_bw - Link Rate.
    # @param[in] ref_clk : Reference Clock for platform.
    # @param[in] display_port - Display port
    # @param[in] gfx_index - Graphics index on which register read
    # @return ret - BOOL ( True /False ), pll_values (pll_values dictionary )
    def get_edp_pll_ref_values(self, link_bw, ref_clk, display_port, gfx_index='gfx_0'):
        pll_values = []
        ret = True
        index = 0

        logging.debug("Get Reference EDP PLL Values for ref_clk = " + str(ref_clk)
                      + " & link_rate = " + str(link_bw))

        if ref_clk == 38.4 or ref_clk == 100:
            if link_bw == 1.62:   # rbr
                index = 0
            elif link_bw == 2.7:  # hbr1
                index = 2
            elif link_bw == 5.4:  # hbr2
                index = 4
            elif link_bw == 8.1:  # hbr3
                index = 6
            elif link_bw == 2.16:  # R216
                index = 8
            elif link_bw == 2.43:  # R243
                index = 9
            elif link_bw == 3.24:  # R324
                index = 10
            elif link_bw == 4.32:  # R432
                index = 11
            elif link_bw == 10:  # Uhbr10
                index = 12
            elif link_bw == 13.5:  # Uhbr13p5
                index = 14
            else:
                ret = False
        else:
            ret = False
        if clock_helper.get_ssc_from_dpcd(display_port, gfx_index):
            index = index if index in [8, 9, 10, 11] else index + 1
        pll_values = DPModePLLValueRefClk100Mhz[index] if ref_clk == 100 else DPModePLLValueRefClk38p4Mhz[index]
        return ret, pll_values


if __name__ == "__main__":
    clk = Dg2ClockEdp()
    clk.verify_clock('DP_A', 'gfx_0')
