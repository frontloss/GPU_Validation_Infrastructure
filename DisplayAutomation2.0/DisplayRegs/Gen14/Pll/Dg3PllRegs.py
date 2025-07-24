# ===========================================================================
#
#    Copyright (c) Intel Corporation (2000 - 2020)
#
#    INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
#    ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
#    INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
#    ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
#    MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
#    OTHER WARRANTY.  Intel disclaims all liability, including liability for
#    infringement of any proprietary rights, relating to use of the code. No license,
#    express or implied, by estoppel or otherwise, to any intellectual property
#    rights is granted herein.
#
# --------------------------------------------------------------------------
#
# @file Dg3PllRegs.py
# @brief contains Dg3PllRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_POWER_STATE(Enum):
    POWER_STATE_DISABLED = 0x0
    POWER_STATE_ENABLED = 0x1


class ENUM_POWER_ENABLE(Enum):
    POWER_DISABLE = 0x0
    POWER_ENABLE = 0x1


class ENUM_PLL_REFCLK_SELECT(Enum):
    PLL_REFCLK_SELECT_REFCLK = 0x0
    PLL_REFCLK_SELECT_GENLOCK = 0x1


class ENUM_PLL_LOCK(Enum):
    PLL_LOCK_NOT_LOCKED_OR_NOT_ENABLED = 0x0
    PLL_LOCK_LOCKED = 0x1


class ENUM_PLL_ENABLE(Enum):
    PLL_DISABLE = 0x0
    PLL_ENABLE = 0x1


class OFFSET_DPLL_ENABLE:
    DPLL0_ENABLE = 0x46010
    PORTA_PLL_ENABLE = 0x46010
    DPLL1_ENABLE = 0x46014
    PORTB_PLL_ENABLE = 0x46014
    DPLL4_ENABLE = 0x46018
    DPLL2_ENABLE = 0x46018
    PORTC_PLL_ENABLE = 0x46018
    PORTD_PLL_ENABLE = 0x4601C
    TBT_PLL_ENABLE = 0x46020
    MGPLL1_ENABLE = 0x46030
    DPLL3_ENABLE = 0x46030
    PORTTC1_PLL_ENABLE = 0x46030
    MGPLL2_ENABLE = 0x46034
    PORTTC1_PLL0_ENABLE = 0x46034
    MGPLL3_ENABLE = 0x46038
    PORTTC1_PLL1_ENABLE = 0x46038
    MGPLL4_ENABLE = 0x4603C
    PORTTC2_PLL0_ENABLE = 0x4603C
    MGPLL5_ENABLE = 0x46040
    PORTTC2_PLL1_ENABLE = 0x46040
    MGPLL6_ENABLE = 0x46044
    PORTTC3_PLL0_ENABLE = 0x46044
    PORTTC3_PLL1_ENABLE = 0x46048
    PORTTC4_PLL0_ENABLE = 0x4604C
    PORTTC4_PLL1_ENABLE = 0x46050


class _DPLL_ENABLE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 11),
        ('Reserved11', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 14),
        ('PowerState', ctypes.c_uint32, 1),
        ('PowerEnable', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 1),
        ('PllRefclkSelect', ctypes.c_uint32, 1),
        ('PllLock', ctypes.c_uint32, 1),
        ('PllEnable', ctypes.c_uint32, 1),
    ]


class REG_DPLL_ENABLE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 11
    Reserved11 = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 26
    PowerState = 0  # bit 26 to 27
    PowerEnable = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 29
    PllRefclkSelect = 0  # bit 29 to 30
    PllLock = 0  # bit 30 to 31
    PllEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLL_ENABLE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLL_ENABLE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLL_CFGCR0:
    DPLL0_CFGCR0 = 0x164284
    DPLL1_CFGCR0 = 0x16428C
    DPLL4_CFGCR0 = 0x164294
    TBTPLL_CFGCR0 = 0x16429C
    DPLL3_CFGCR0 = 0x1642C0
    DPLL2_CFGCR0 = 0x16C284
    DPLL3_CFGCR0 = 0x16C28C


class _DPLL_CFGCR0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DcoInteger', ctypes.c_uint32, 10),
        ('DcoFraction', ctypes.c_uint32, 15),
        ('Reserved25', ctypes.c_uint32, 7),
    ]


class REG_DPLL_CFGCR0(ctypes.Union):
    value = 0
    offset = 0

    DcoInteger = 0  # bit 0 to 10
    DcoFraction = 0  # bit 10 to 25
    Reserved25 = 0  # bit 25 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLL_CFGCR0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLL_CFGCR0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFSELOVRD(Enum):
    CFSELOVRD_NORMAL_XTAL = 0x0  # Normal XTAL cannot be picked as genlock clock source if the transcoder is programmed
                                 #  as genlock remote slave.
    CFSELOVRD_UNFILTERED_GENLOCK_REF = 0x1
    CFSELOVRD_FILTERED_GENLOCK_REF = 0x3


class ENUM_PDIV(Enum):
    PDIV_2 = 0x1
    PDIV_3 = 0x2
    PDIV_5 = 0x4
    PDIV_7 = 0x8


class ENUM_KDIV(Enum):
    KDIV_1 = 0x1
    KDIV_2 = 0x2
    KDIV_3 = 0x4


class ENUM_QDIV_MODE(Enum):
    QDIV_MODE_DISABLE = 0x0  # Q divider = 1
    QDIV_MODE_ENABLE = 0x1  # Q divider = Qdiv Ratio


class OFFSET_DPLL_CFGCR1:
    DPLL0_CFGCR1 = 0x164288
    DPLL1_CFGCR1 = 0x164290
    DPLL4_CFGCR1 = 0x164298
    TBTPLL_CFGCR1 = 0x1642A0
    DPLL3_CFGCR1 = 0x1642C4
    DPLL2_CFGCR1 = 0x16C288
    DPLL3_CFGCR1 = 0x16C290


class _DPLL_CFGCR1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfselovrd', ctypes.c_uint32, 2),
        ('Pdiv', ctypes.c_uint32, 4),
        ('Kdiv', ctypes.c_uint32, 3),
        ('QdivMode', ctypes.c_uint32, 1),
        ('QdivRatio', ctypes.c_uint32, 8),
        ('Reserved18', ctypes.c_uint32, 14),
    ]


class REG_DPLL_CFGCR1(ctypes.Union):
    value = 0
    offset = 0

    Cfselovrd = 0  # bit 0 to 2
    Pdiv = 0  # bit 2 to 6
    Kdiv = 0  # bit 6 to 9
    QdivMode = 0  # bit 9 to 10
    QdivRatio = 0  # bit 10 to 18
    Reserved18 = 0  # bit 18 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLL_CFGCR1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLL_CFGCR1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SSCEN(Enum):
    SSCEN_DISABLE = 0x0
    SSCEN_ENABLE = 0x1


class ENUM_SSCINJ_EN_H(Enum):
    SSCINJ_EN_H_DISABLE = 0x0
    SSCINJ_EN_H_ENABLE = 0x1


class ENUM_SSCINJ_ADAPT_EN_H(Enum):
    SSCINJ_ADAPT_EN_H_DISABLE = 0x0
    SSCINJ_ADAPT_EN_H_ENABLE = 0x1


class OFFSET_DPLL_SSC:
    DPLL0_SSC = 0x164B10
    DPLL1_SSC = 0x164C10
    DPLL4_SSC = 0x164E10
    DPLL2_SSC = 0x16CB10
    DPLL3_SSC = 0x16CC10


class _DPLL_SSC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Init_Dcoamp', ctypes.c_uint32, 6),
        ('Bias_Gb_Sel', ctypes.c_uint32, 2),
        ('Sscfllen', ctypes.c_uint32, 1),
        ('Sscen', ctypes.c_uint32, 1),
        ('Ssc_Openloop_En', ctypes.c_uint32, 1),
        ('Sscstepnum', ctypes.c_uint32, 3),
        ('Sscfll_Update_Sel', ctypes.c_uint32, 2),
        ('Sscsteplength', ctypes.c_uint32, 8),
        ('Sscinj_En_H', ctypes.c_uint32, 1),
        ('Sscinj_Adapt_En_H', ctypes.c_uint32, 1),
        ('Sscstepnum_Offset', ctypes.c_uint32, 3),
        ('Iref_Ndivratio', ctypes.c_uint32, 3),
    ]


class REG_DPLL_SSC(ctypes.Union):
    value = 0
    offset = 0

    Init_Dcoamp = 0  # bit 0 to 6
    Bias_Gb_Sel = 0  # bit 6 to 8
    Sscfllen = 0  # bit 8 to 9
    Sscen = 0  # bit 9 to 10
    Ssc_Openloop_En = 0  # bit 10 to 11
    Sscstepnum = 0  # bit 11 to 14
    Sscfll_Update_Sel = 0  # bit 14 to 16
    Sscsteplength = 0  # bit 16 to 24
    Sscinj_En_H = 0  # bit 24 to 25
    Sscinj_Adapt_En_H = 0  # bit 25 to 26
    Sscstepnum_Offset = 0  # bit 26 to 29
    Iref_Ndivratio = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLL_SSC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLL_SSC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_MPLLB_CP:
    SNPS_PHY_MPLLB_CP_PORT_A = 0x168000
    SNPS_PHY_MPLLB_CP_PORT_B = 0x169000
    SNPS_PHY_MPLLB_CP_PORT_C = 0x16A000
    SNPS_PHY_MPLLB_CP_PORT_D = 0x16B000
    SNPS_PHY_MPLLB_CP_PORT_TC1 = 0x16C000


class _SNPS_PHY_MPLLB_CP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Cp_Prop_Gs', ctypes.c_uint32, 7),
        ('Reserved8', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Cp_Prop', ctypes.c_uint32, 7),
        ('Reserved16', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Cp_Int_Gs', ctypes.c_uint32, 7),
        ('Reserved24', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Cp_Int', ctypes.c_uint32, 7),
    ]


class REG_SNPS_PHY_MPLLB_CP(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    Dp_Mpllb_Cp_Prop_Gs = 0  # bit 1 to 8
    Reserved8 = 0  # bit 8 to 9
    Dp_Mpllb_Cp_Prop = 0  # bit 9 to 16
    Reserved16 = 0  # bit 16 to 17
    Dp_Mpllb_Cp_Int_Gs = 0  # bit 17 to 24
    Reserved24 = 0  # bit 24 to 25
    Dp_Mpllb_Cp_Int = 0  # bit 25 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_CP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_CP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DP_SHIM_DIV32_CLK_SEL(Enum):
    DP_SHIM_DIV32_CLK_SEL_DIV32 = 0x1
    DP_SHIM_DIV32_CLK_SEL_DIV20 = 0x0


class ENUM_DP_MPLLB_TX_CLK_DIV(Enum):
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_1 = 0x0
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_2 = 0x1
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_4 = 0x2
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_8 = 0x3
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_3 = 0x4
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_5 = 0x5
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_6 = 0x6
    DP_MPLLB_TX_CLK_DIV_DIVIDE_BY_0 = 0x7


class ENUM_DP2_MODE(Enum):
    DP2_MODE_DP2_0_NOT_SELECTED = 0x0
    DP2_MODE_DP2_0_SELECTED = 0x1


class OFFSET_SNPS_PHY_MPLLB_DIV:
    SNPS_PHY_MPLLB_DIV_PORT_A = 0x168004
    SNPS_PHY_MPLLB_DIV_PORT_B = 0x169004
    SNPS_PHY_MPLLB_DIV_PORT_C = 0x16A004
    SNPS_PHY_MPLLB_DIV_PORT_D = 0x16B004
    SNPS_PHY_MPLLB_DIV_PORT_TC1 = 0x16C004


class _SNPS_PHY_MPLLB_DIV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dp_Shim_Div32_Clk_Sel', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 4),
        ('Dp_Mpllb_Tx_Clk_Div', ctypes.c_uint32, 3),
        ('Dp_Mpllb_Word_Div2_En', ctypes.c_uint32, 1),
        ('Dp2_Mode', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Pmix_En', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 5),
        ('Dp_Mpllb_Div_Multiplier', ctypes.c_uint32, 8),
        ('Dp_Mpllb_Freq_Vco', ctypes.c_uint32, 2),
        ('Dp_Mpllb_V2I', ctypes.c_uint32, 2),
        ('Dp_Mpllb_Init_Cal_Disable', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Div5_Clk_En', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Div_Clk_En', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Force_En', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_MPLLB_DIV(ctypes.Union):
    value = 0
    offset = 0

    Dp_Shim_Div32_Clk_Sel = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 5
    Dp_Mpllb_Tx_Clk_Div = 0  # bit 5 to 8
    Dp_Mpllb_Word_Div2_En = 0  # bit 8 to 9
    Dp2_Mode = 0  # bit 9 to 10
    Dp_Mpllb_Pmix_En = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 16
    Dp_Mpllb_Div_Multiplier = 0  # bit 16 to 24
    Dp_Mpllb_Freq_Vco = 0  # bit 24 to 26
    Dp_Mpllb_V2I = 0  # bit 26 to 28
    Dp_Mpllb_Init_Cal_Disable = 0  # bit 28 to 29
    Dp_Mpllb_Div5_Clk_En = 0  # bit 29 to 30
    Dp_Mpllb_Div_Clk_En = 0  # bit 30 to 31
    Dp_Mpllb_Force_En = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_DIV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_DIV, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_MPLLB_DIV2:
    SNPS_PHY_MPLLB_DIV2_PORT_A = 0x16801C
    SNPS_PHY_MPLLB_DIV2_PORT_B = 0x16901C
    SNPS_PHY_MPLLB_DIV2_PORT_C = 0x16A01C
    SNPS_PHY_MPLLB_DIV2_PORT_D = 0x16B01C
    SNPS_PHY_MPLLB_DIV2_PORT_TC1 = 0x16C01C


class _SNPS_PHY_MPLLB_DIV2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dp_Mpllb_Mulitplier', ctypes.c_uint32, 12),
        ('Dp_Ref_Clk_Mpllb_Div', ctypes.c_uint32, 3),
        ('Hdmi_Mpllb_Hdmi_Div', ctypes.c_uint32, 3),
        ('Hdmi_Mpllb_Hdmi_Pixel_Clk_Div', ctypes.c_uint32, 2),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_SNPS_PHY_MPLLB_DIV2(ctypes.Union):
    value = 0
    offset = 0

    Dp_Mpllb_Mulitplier = 0  # bit 0 to 12
    Dp_Ref_Clk_Mpllb_Div = 0  # bit 12 to 15
    Hdmi_Mpllb_Hdmi_Div = 0  # bit 15 to 18
    Hdmi_Mpllb_Hdmi_Pixel_Clk_Div = 0  # bit 18 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_DIV2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_DIV2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DP_MPLLB_SSC_EN(Enum):
    DP_MPLLB_SSC_EN_DISABLE = 0x0
    DP_MPLLB_SSC_EN_ENABLE = 0x1


class OFFSET_SNPS_PHY_MPLLB_SSCEN:
    SNPS_PHY_MPLLB_SSCEN_PORT_A = 0x168014
    SNPS_PHY_MPLLB_SSCEN_PORT_B = 0x169014
    SNPS_PHY_MPLLB_SSCEN_PORT_C = 0x16A014
    SNPS_PHY_MPLLB_SSCEN_PORT_D = 0x16B014
    SNPS_PHY_MPLLB_SSCEN_PORT_TC1 = 0x16C014


class _SNPS_PHY_MPLLB_SSCEN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 10),
        ('Dp_Mpllb_Ssc_Peak', ctypes.c_uint32, 20),
        ('Dp_Mpllb_Ssc_Up_Spread', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Ssc_En', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_MPLLB_SSCEN(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 10
    Dp_Mpllb_Ssc_Peak = 0  # bit 10 to 30
    Dp_Mpllb_Ssc_Up_Spread = 0  # bit 30 to 31
    Dp_Mpllb_Ssc_En = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_SSCEN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_SSCEN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_MPLLB_FRACN1:
    SNPS_PHY_MPLLB_FRACN1_PORT_A = 0x168008
    SNPS_PHY_MPLLB_FRACN1_PORT_B = 0x169008
    SNPS_PHY_MPLLB_FRACN1_PORT_C = 0x16A008
    SNPS_PHY_MPLLB_FRACN1_PORT_D = 0x16B008
    SNPS_PHY_MPLLB_FRACN1_PORT_TC1 = 0x16C008


class _SNPS_PHY_MPLLB_FRACN1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dp_Mpllb_Fracn_Den', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 14),
        ('Dp_Mpllb_Fracn_Cfg_Update_En', ctypes.c_uint32, 1),
        ('Dp_Mpllb_Fracn_En', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_MPLLB_FRACN1(ctypes.Union):
    value = 0
    offset = 0

    Dp_Mpllb_Fracn_Den = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 30
    Dp_Mpllb_Fracn_Cfg_Update_En = 0  # bit 30 to 31
    Dp_Mpllb_Fracn_En = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_FRACN1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_FRACN1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_MPLLB_FRACN2:
    SNPS_PHY_MPLLB_FRACN2_PORT_A = 0x16800C
    SNPS_PHY_MPLLB_FRACN2_PORT_B = 0x16900C
    SNPS_PHY_MPLLB_FRACN2_PORT_C = 0x16A00C
    SNPS_PHY_MPLLB_FRACN2_PORT_D = 0x16B00C
    SNPS_PHY_MPLLB_FRACN2_PORT_TC1 = 0x16C00C


class _SNPS_PHY_MPLLB_FRACN2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Dp_Mpllb_Fracn_Quot', ctypes.c_uint32, 16),
        ('Dp_Mpllb_Fracn_Rem', ctypes.c_uint32, 16),
    ]


class REG_SNPS_PHY_MPLLB_FRACN2(ctypes.Union):
    value = 0
    offset = 0

    Dp_Mpllb_Fracn_Quot = 0  # bit 0 to 16
    Dp_Mpllb_Fracn_Rem = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_FRACN2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_FRACN2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SNPS_PHY_MPLLB_SSCSTEP:
    SNPS_PHY_MPLLB_SSCSTEP_PORT_A = 0x168018
    SNPS_PHY_MPLLB_SSCSTEP_PORT_B = 0x169018
    SNPS_PHY_MPLLB_SSCSTEP_PORT_C = 0x16A018
    SNPS_PHY_MPLLB_SSCSTEP_PORT_D = 0x16B018
    SNPS_PHY_MPLLB_SSCSTEP_PORT_TC1 = 0x16C018


class _SNPS_PHY_MPLLB_SSCSTEP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 11),
        ('Dp_Mpllb_Ssc_Stepsize', ctypes.c_uint32, 21),
    ]


class REG_SNPS_PHY_MPLLB_SSCSTEP(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 11
    Dp_Mpllb_Ssc_Stepsize = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_SSCSTEP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_SSCSTEP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_HW_SEQ_STATE(Enum):
    HW_SEQ_STATE_PHY_INIT = 0x0
    HW_SEQ_STATE_PLL_OFF = 0x1
    HW_SEQ_STATE_REQ_PLL_ON = 0x2
    HW_SEQ_STATE_PLL_ON_P3 = 0x3
    HW_SEQ_STATE_LANE_RST = 0x4
    HW_SEQ_STATE_REQ_P0 = 0x5
    HW_SEQ_STATE_LANES_OUT_OF_RST_P0 = 0x6
    HW_SEQ_STATE_REQ_P3 = 0x7
    HW_SEQ_STATE_WAIT_FOR_PLL_OFF_ACK = 0x8
    HW_SEQ_STATE_DRIVE_DPALT_DISABLE_SIGNALS = 0x9
    HW_SEQ_STATE_REQ_PSR_PSTATE = 0xA
    HW_SEQ_STATE_PSR_STATE = 0xB


class OFFSET_SNPS_PHY_MPLLB_STATUS:
    SNPS_PHY_MPLLB_STATUS_PORT_A = 0x168010
    SNPS_PHY_MPLLB_STATUS_PORT_B = 0x169010
    SNPS_PHY_MPLLB_STATUS_PORT_C = 0x16A010
    SNPS_PHY_MPLLB_STATUS_PORT_D = 0x16B010
    SNPS_PHY_MPLLB_STATUS_PORT_TC1 = 0x16C010


class _SNPS_PHY_MPLLB_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hw_Seq_State', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 19),
        ('Dp_Tx0_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx0_Req', ctypes.c_uint32, 1),
        ('Dp_Tx1_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx1_Req', ctypes.c_uint32, 1),
        ('Dp_Tx2_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx2_Req', ctypes.c_uint32, 1),
        ('Dp_Tx3_Ack', ctypes.c_uint32, 1),
        ('Dp_Tx3_Req', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_SNPS_PHY_MPLLB_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Hw_Seq_State = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 23
    Dp_Tx0_Ack = 0  # bit 23 to 24
    Dp_Tx0_Req = 0  # bit 24 to 25
    Dp_Tx1_Ack = 0  # bit 25 to 26
    Dp_Tx1_Req = 0  # bit 26 to 27
    Dp_Tx2_Ack = 0  # bit 27 to 28
    Dp_Tx2_Req = 0  # bit 28 to 29
    Dp_Tx3_Ack = 0  # bit 29 to 30
    Dp_Tx3_Req = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_MPLLB_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_MPLLB_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_FILTER_PLL_INPUT_MUX_SELECT(Enum):
    FILTER_PLL_INPUT_MUX_SELECT_NONGENLOCK = 0x0
    FILTER_PLL_INPUT_MUX_SELECT_GENLOCK = 0x1


class ENUM_FILTER_PLL_LOCK(Enum):
    FILTER_PLL_LOCK_NOT_LOCKED_OR_NOT_ENABLED = 0x0
    FILTER_PLL_LOCK_LOCKED = 0x1


class ENUM_FILTER_PLL_ENABLE(Enum):
    FILTER_PLL_DISABLE = 0x0  # Filter PLL disabled.
    FILTER_PLL_ENABLE = 0x1  # Filter PLL enabled.


class ENUM_REFCLK_MUX_SELECT(Enum):
    REFCLK_MUX_SELECT_100_MHZ = 0x1  # PHY is configured for native DP and HDMI connections.
    REFCLK_MUX_SELECT_38_4_MHZ = 0x0  # PHY is configured for type-C connections.


class ENUM_DP_REF_CLK_REQ(Enum):
    DP_REF_CLK_REQ_REF_CLOCK_CAN_BE_DISABLED = 0x0
    DP_REF_CLK_REQ_REF_CLOCK_CANNOT_BE_DISABLED = 0x1


class ENUM_DP_REF_CLK_EN(Enum):
    DP_REF_CLK_EN_REF_CLOCK_IS_NOT_ENABLED = 0x0
    DP_REF_CLK_EN_REF_CLOCK_IS_ENABLED = 0x1


class OFFSET_SNPS_PHY_REF_CONTROL:
    SNPS_PHY_REF_CONTROL_PORT_A = 0x168188
    SNPS_PHY_REF_CONTROL_PORT_B = 0x169188
    SNPS_PHY_REF_CONTROL_PORT_C = 0x16A188
    SNPS_PHY_REF_CONTROL_PORT_D = 0x16B188
    SNPS_PHY_REF_CONTROL_PORT_TC1 = 0x16C188


class _SNPS_PHY_REF_CONTROL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 13),
        ('FilterPllInputMuxSelect', ctypes.c_uint32, 1),
        ('FilterPllLock', ctypes.c_uint32, 1),
        ('FilterPllEnable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 8),
        ('RefclkMuxSelect', ctypes.c_uint32, 1),
        ('Dp_Ref_Clk_Req', ctypes.c_uint32, 1),
        ('Dp_Ref_Clk_En', ctypes.c_uint32, 1),
        ('Ref_Range', ctypes.c_uint32, 5),
    ]


class REG_SNPS_PHY_REF_CONTROL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 13
    FilterPllInputMuxSelect = 0  # bit 13 to 14
    FilterPllLock = 0  # bit 14 to 15
    FilterPllEnable = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 24
    RefclkMuxSelect = 0  # bit 24 to 25
    Dp_Ref_Clk_Req = 0  # bit 25 to 26
    Dp_Ref_Clk_En = 0  # bit 26 to 27
    Ref_Range = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SNPS_PHY_REF_CONTROL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SNPS_PHY_REF_CONTROL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

