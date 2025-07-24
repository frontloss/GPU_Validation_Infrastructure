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
# @file AdlsPllRegs.py
# @brief contains AdlsPllRegs.py related register definitions

import ctypes
from enum import Enum


class OFFSET_DPLL_CFGCR0:
    DPLL0_CFGCR0 = 0x164284
    DPLL1_CFGCR0 = 0x16428C
    DPLL4_CFGCR0 = 0x164294
    TBTPLL_CFGCR0 = 0x16429C
    DPLL3_CFGCR0 = 0x1642C0


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


class ENUM_DDIA_MUX_SELECT(Enum):
    DDIA_MUX_SELECT_DPLL0 = 0x0
    DDIA_MUX_SELECT_DPLL1 = 0x1
    DDIA_MUX_SELECT_DPLL2 = 0x2
    DDIA_MUX_SELECT_DPLL3 = 0x3


class ENUM_DDIB_MUX_SELECT(Enum):
    DDIB_MUX_SELECT_DPLL0 = 0x0
    DDIB_MUX_SELECT_DPLL1 = 0x1
    DDIB_MUX_SELECT_DPLL2 = 0x2
    DDIB_MUX_SELECT_DPLL3 = 0x3


class ENUM_DDII_MUX_SELECT(Enum):
    DDII_MUX_SELECT_DPLL0 = 0x0
    DDII_MUX_SELECT_DPLL1 = 0x1
    DDII_MUX_SELECT_DPLL2 = 0x2
    DDII_MUX_SELECT_DPLL3 = 0x3


class ENUM_DDIA_CLOCK_OFF(Enum):
    DDIA_CLOCK_OFF_ON = 0x0
    DDIA_CLOCK_OFF_OFF = 0x1


class ENUM_DDIB_CLOCK_OFF(Enum):
    DDIB_CLOCK_OFF_ON = 0x0
    DDIB_CLOCK_OFF_OFF = 0x1


class ENUM_DDIC_CLOCK_OFF(Enum):
    DDIC_CLOCK_OFF_ON = 0x0
    DDIC_CLOCK_OFF_OFF = 0x1


class ENUM_DDID_CLOCK_OFF(Enum):
    DDID_CLOCK_OFF_ON = 0x0
    DDID_CLOCK_OFF_OFF = 0x1


class ENUM_DDIE_CLOCK_OFF(Enum):
    DDIE_CLOCK_OFF_ON = 0x0
    DDIE_CLOCK_OFF_OFF = 0x1


class ENUM_DPLL0_INVERSE_REF(Enum):
    DPLL0_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL0_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL1_INVERSE_REF(Enum):
    DPLL1_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL1_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL2_INVERSE_REF(Enum):
    DPLL2_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL2_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL0_ENABLE_OVERRIDE(Enum):
    DPLL0_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL0_ENABLE_OVERRIDE_FORCED = 0x1


class ENUM_DPLL1_ENABLE_OVERRIDE(Enum):
    DPLL1_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL1_ENABLE_OVERRIDE_FORCED = 0x1


class ENUM_DPLL2_ENABLE_OVERRIDE(Enum):
    DPLL2_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL2_ENABLE_OVERRIDE_FORCED = 0x1


class ENUM_DDIF_CLOCK_OFF(Enum):
    DDIF_CLOCK_OFF_ON = 0x0
    DDIF_CLOCK_OFF_OFF = 0x1


class ENUM_DDIG_CLOCK_OFF(Enum):
    DDIG_CLOCK_OFF_ON = 0x0
    DDIG_CLOCK_OFF_OFF = 0x1


class ENUM_DDIH_CLOCK_OFF(Enum):
    DDIH_CLOCK_OFF_ON = 0x0
    DDIH_CLOCK_OFF_OFF = 0x1


class ENUM_DDII_CLOCK_OFF(Enum):
    DDII_CLOCK_OFF_ON = 0x0
    DDII_CLOCK_OFF_OFF = 0x1


class ENUM_DPLL3_INVERSE_REF(Enum):
    DPLL3_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL3_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL4_INVERSE_REF(Enum):
    DPLL4_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL4_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL3_ENABLE_OVERRIDE(Enum):
    DPLL3_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL3_ENABLE_OVERRIDE_FORCED = 0x1


class ENUM_TC_GENLOCK_REF_SELECT(Enum):
    TC_GENLOCK_REF_SELECT_CLK_GL_REFCLKIN_FILT = 0x0
    TC_GENLOCK_REF_SELECT_CLK_GL_REFCLKIN_RAW = 0x1


class ENUM_IREF_INVERSE_REF(Enum):
    IREF_INVERSE_REF_NOT_INVERSE = 0x0
    IREF_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL4_ENABLE_OVERRIDE(Enum):
    DPLL4_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL4_ENABLE_OVERRIDE_FORCED = 0x1


class OFFSET_DPCLKA_CFGCR0:
    DPCLKA_CFGCR0 = 0x164280


class _DPCLKA_CFGCR0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiaMuxSelect', ctypes.c_uint32, 2),
        ('DdibMuxSelect', ctypes.c_uint32, 2),
        ('DdiiMuxSelect', ctypes.c_uint32, 2),
        ('MipiaHvmSel', ctypes.c_uint32, 2),
        ('MipicHvmSel', ctypes.c_uint32, 2),
        ('DdiaClockOff', ctypes.c_uint32, 1),
        ('DdibClockOff', ctypes.c_uint32, 1),
        ('DdicClockOff', ctypes.c_uint32, 1),
        ('DdidClockOff', ctypes.c_uint32, 1),
        ('DdieClockOff', ctypes.c_uint32, 1),
        ('Dpll0InverseRef', ctypes.c_uint32, 1),
        ('Dpll1InverseRef', ctypes.c_uint32, 1),
        ('Dpll2InverseRef', ctypes.c_uint32, 1),
        ('Dpll0EnableOverride', ctypes.c_uint32, 1),
        ('Dpll1EnableOverride', ctypes.c_uint32, 1),
        ('Dpll2EnableOverride', ctypes.c_uint32, 1),
        ('DdifClockOff', ctypes.c_uint32, 1),
        ('DdigClockOff', ctypes.c_uint32, 1),
        ('DdihClockOff', ctypes.c_uint32, 1),
        ('DdiiClockOff', ctypes.c_uint32, 1),
        ('Dpll3InverseRef', ctypes.c_uint32, 1),
        ('Dpll4InverseRef', ctypes.c_uint32, 1),
        ('Dpll3EnableOverride', ctypes.c_uint32, 1),
        ('TcGenlockRefSelect', ctypes.c_uint32, 1),
        ('HvmIndependentMipiEnable', ctypes.c_uint32, 1),
        ('IrefInverseRef', ctypes.c_uint32, 1),
        ('Dpll4EnableOverride', ctypes.c_uint32, 1),
    ]


class REG_DPCLKA_CFGCR0(ctypes.Union):
    value = 0
    offset = 0

    DdiaMuxSelect = 0  # bit 0 to 2
    DdibMuxSelect = 0  # bit 2 to 4
    DdiiMuxSelect = 0  # bit 4 to 6
    MipiaHvmSel = 0  # bit 6 to 8
    MipicHvmSel = 0  # bit 8 to 10
    DdiaClockOff = 0  # bit 10 to 11
    DdibClockOff = 0  # bit 11 to 12
    DdicClockOff = 0  # bit 12 to 13
    DdidClockOff = 0  # bit 13 to 14
    DdieClockOff = 0  # bit 14 to 15
    Dpll0InverseRef = 0  # bit 15 to 16
    Dpll1InverseRef = 0  # bit 16 to 17
    Dpll2InverseRef = 0  # bit 17 to 18
    Dpll0EnableOverride = 0  # bit 18 to 19
    Dpll1EnableOverride = 0  # bit 19 to 20
    Dpll2EnableOverride = 0  # bit 20 to 21
    DdifClockOff = 0  # bit 21 to 22
    DdigClockOff = 0  # bit 22 to 23
    DdihClockOff = 0  # bit 23 to 24
    DdiiClockOff = 0  # bit 24 to 25
    Dpll3InverseRef = 0  # bit 25 to 26
    Dpll4InverseRef = 0  # bit 26 to 27
    Dpll3EnableOverride = 0  # bit 27 to 28
    TcGenlockRefSelect = 0  # bit 28 to 29
    HvmIndependentMipiEnable = 0  # bit 29 to 30
    IrefInverseRef = 0  # bit 30 to 31
    Dpll4EnableOverride = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPCLKA_CFGCR0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPCLKA_CFGCR0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DDIJ_MUX_SELECT(Enum):
    DDIJ_MUX_SELECT_DPLL0 = 0x0
    DDIJ_MUX_SELECT_DPLL1 = 0x1
    DDIJ_MUX_SELECT_DPLL2 = 0x2
    DDIJ_MUX_SELECT_DPLL3 = 0x3


class ENUM_DDIK_MUX_SELECT(Enum):
    DDIK_MUX_SELECT_DPLL0 = 0x0
    DDIK_MUX_SELECT_DPLL1 = 0x1
    DDIK_MUX_SELECT_DPLL2 = 0x2
    DDIK_MUX_SELECT_DPLL3 = 0x3


class ENUM_DDIJ_CLOCK_OFF(Enum):
    DDIJ_CLOCK_OFF_ON = 0x0
    DDIJ_CLOCK_OFF_OFF = 0x1


class ENUM_DDIK_CLOCK_OFF(Enum):
    DDIK_CLOCK_OFF_ON = 0x0
    DDIK_CLOCK_OFF_OFF = 0x1


class OFFSET_DPCLKA_CFGCR1:
    DPCLKA_CFGCR1 = 0x1642BC


class _DPCLKA_CFGCR1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdijMuxSelect', ctypes.c_uint32, 2),
        ('DdikMuxSelect', ctypes.c_uint32, 2),
        ('DdijClockOff', ctypes.c_uint32, 1),
        ('DdikClockOff', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 10),
        ('FuseFreqMonStatus', ctypes.c_uint32, 12),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_DPCLKA_CFGCR1(ctypes.Union):
    value = 0
    offset = 0

    DdijMuxSelect = 0  # bit 0 to 2
    DdikMuxSelect = 0  # bit 2 to 4
    DdijClockOff = 0  # bit 4 to 5
    DdikClockOff = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 16
    FuseFreqMonStatus = 0  # bit 16 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPCLKA_CFGCR1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPCLKA_CFGCR1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


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
    DPLL1_ENABLE = 0x46014
    DPLL2_ENABLE = 0x46018
    TBT_PLL_ENABLE = 0x46020
    DPLL3_ENABLE = 0x46030
    MGPLL2_ENABLE = 0x46034
    MGPLL3_ENABLE = 0x46038
    MGPLL4_ENABLE = 0x4603C
    MGPLL5_ENABLE = 0x46040
    MGPLL6_ENABLE = 0x46044


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


class ENUM_DDI0_USED(Enum):
    DDI0_USED_NOT_USED = 0x0
    DDI0_USED_USED = 0x1


class ENUM_HDMI_DP0(Enum):
    HDMI_DP0_DP = 0x0
    HDMI_DP0_HDMI = 0x1


class ENUM_DDI1_USED(Enum):
    DDI1_USED_NOT_USED = 0x0
    DDI1_USED_USED = 0x1


class ENUM_HDMI_DP1(Enum):
    HDMI_DP1_DP = 0x0
    HDMI_DP1_HDMI = 0x1


class ENUM_DDI2_USED(Enum):
    DDI2_USED_NOT_USED = 0x0
    DDI2_USED_USED = 0x1


class ENUM_HDMI_DP2(Enum):
    HDMI_DP2_DP = 0x0
    HDMI_DP2_HDMI = 0x1


class ENUM_DDI3_USED(Enum):
    DDI3_USED_NOT_USED = 0x0
    DDI3_USED_USED = 0x1


class ENUM_HDMI_DP3(Enum):
    HDMI_DP3_DP = 0x0
    HDMI_DP3_HDMI = 0x1


class ENUM_DDI4_USED(Enum):
    DDI4_USED_NOT_USED = 0x0
    DDI4_USED_USED = 0x1


class ENUM_HDMI_DP4(Enum):
    HDMI_DP4_DP = 0x0
    HDMI_DP4_HDMI = 0x1


class ENUM_DPLL0_USED(Enum):
    DPLL0_USED_NOT_USED = 0x0
    DPLL0_USED_USED = 0x1


class ENUM_DPLL1_USED(Enum):
    DPLL1_USED_NOT_USED = 0x0
    DPLL1_USED_USED = 0x1


class ENUM_DPLL2_USED(Enum):
    DPLL2_USED_NOT_USED = 0x0
    DPLL2_USED_USED = 0x1


class ENUM_DPLL3_USED(Enum):
    DPLL3_USED_NOT_USED = 0x0
    DPLL3_USED_USED = 0x1


class OFFSET_HDPORT_STATE:
    HDPORT_STATE = 0x45050


class _HDPORT_STATE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hdport_En', ctypes.c_uint32, 1),
        ('Ddi0_Used', ctypes.c_uint32, 1),
        ('Hdmi_Dp0', ctypes.c_uint32, 1),
        ('Ddi1_Used', ctypes.c_uint32, 1),
        ('Hdmi_Dp1', ctypes.c_uint32, 1),
        ('Ddi2_Used', ctypes.c_uint32, 1),
        ('Hdmi_Dp2', ctypes.c_uint32, 1),
        ('Ddi3_Used', ctypes.c_uint32, 1),
        ('Hdmi_Dp3', ctypes.c_uint32, 1),
        ('Ddi4_Used', ctypes.c_uint32, 1),
        ('Hdmi_Dp4', ctypes.c_uint32, 1),
        ('Spare_11', ctypes.c_uint32, 1),
        ('Dpll0_Used', ctypes.c_uint32, 1),
        ('Dpll1_Used', ctypes.c_uint32, 1),
        ('Dpll2_Used', ctypes.c_uint32, 1),
        ('Dpll3_Used', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_HDPORT_STATE(ctypes.Union):
    value = 0
    offset = 0

    Hdport_En = 0  # bit 0 to 1
    Ddi0_Used = 0  # bit 1 to 2
    Hdmi_Dp0 = 0  # bit 2 to 3
    Ddi1_Used = 0  # bit 3 to 4
    Hdmi_Dp1 = 0  # bit 4 to 5
    Ddi2_Used = 0  # bit 5 to 6
    Hdmi_Dp2 = 0  # bit 6 to 7
    Ddi3_Used = 0  # bit 7 to 8
    Hdmi_Dp3 = 0  # bit 8 to 9
    Ddi4_Used = 0  # bit 9 to 10
    Hdmi_Dp4 = 0  # bit 10 to 11
    Spare_11 = 0  # bit 11 to 12
    Dpll0_Used = 0  # bit 12 to 13
    Dpll1_Used = 0  # bit 13 to 14
    Dpll2_Used = 0  # bit 14 to 15
    Dpll3_Used = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HDPORT_STATE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HDPORT_STATE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

