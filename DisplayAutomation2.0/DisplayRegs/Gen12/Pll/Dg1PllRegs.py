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
# @file Dg1PllRegs.py
# @brief contains Dg1PllRegs.py related register definitions

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
    DPLL1_ENABLE = 0x46014
    DPLL4_ENABLE = 0x46018
    TBT_PLL_ENABLE = 0x46020
    MGPLL1_ENABLE = 0x46030
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


class OFFSET_DPLL_CFGCR0:
    DPLL0_CFGCR0 = 0x164284
    DPLL1_CFGCR0 = 0x16428C
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


class ENUM_DDIA_CLOCK_SELECT(Enum):
    DDIA_CLOCK_SELECT_DPLL0 = 0x0
    DDIA_CLOCK_SELECT_DPLL1 = 0x1


class ENUM_DDIB_CLOCK_SELECT(Enum):
    DDIB_CLOCK_SELECT_DPLL0 = 0x0
    DDIB_CLOCK_SELECT_DPLL1 = 0x1


class ENUM_DDIA_CLOCK_OFF(Enum):
    DDIA_CLOCK_OFF_ON = 0x0
    DDIA_CLOCK_OFF_OFF = 0x1


class ENUM_DDIB_CLOCK_OFF(Enum):
    DDIB_CLOCK_OFF_ON = 0x0
    DDIB_CLOCK_OFF_OFF = 0x1


class ENUM_DPLL0_INVERSE_REF(Enum):
    DPLL0_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL0_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL1_INVERSE_REF(Enum):
    DPLL1_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL1_INVERSE_REF_INVERSE = 0x1


class ENUM_GENLOCK_PLL_INVERSE_REF(Enum):
    GENLOCK_PLL_INVERSE_REF_NOT_INVERSE = 0x0
    GENLOCK_PLL_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL0_ENABLE_OVERRIDE(Enum):
    DPLL0_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL0_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_DPLL1_ENABLE_OVERRIDE(Enum):
    DPLL1_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL1_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_GENLOCK_PLL_ENABLE_OVERRIDE(Enum):
    GENLOCK_PLL_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    GENLOCK_PLL_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_IREF_INVERSE_REF(Enum):
    IREF_INVERSE_REF_NOT_INVERSE = 0x0
    IREF_INVERSE_REF_INVERSE = 0x1


class OFFSET_DPCLKA0_CFGCR0:
    DPCLKA0_CFGCR0 = 0x164280


class _DPCLKA0_CFGCR0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiaClockSelect', ctypes.c_uint32, 2),
        ('DdibClockSelect', ctypes.c_uint32, 2),
        ('Reserved4', ctypes.c_uint32, 6),
        ('DdiaClockOff', ctypes.c_uint32, 1),
        ('DdibClockOff', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 3),
        ('Dpll0InverseRef', ctypes.c_uint32, 1),
        ('Dpll1InverseRef', ctypes.c_uint32, 1),
        ('GenlockPllInverseRef', ctypes.c_uint32, 1),
        ('Dpll0EnableOverride', ctypes.c_uint32, 1),
        ('Dpll1EnableOverride', ctypes.c_uint32, 1),
        ('GenlockPllEnableOverride', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 9),
        ('IrefInverseRef', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_DPCLKA0_CFGCR0(ctypes.Union):
    value = 0
    offset = 0

    DdiaClockSelect = 0  # bit 0 to 2
    DdibClockSelect = 0  # bit 2 to 4
    Reserved4 = 0  # bit 4 to 10
    DdiaClockOff = 0  # bit 10 to 11
    DdibClockOff = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 15
    Dpll0InverseRef = 0  # bit 15 to 16
    Dpll1InverseRef = 0  # bit 16 to 17
    GenlockPllInverseRef = 0  # bit 17 to 18
    Dpll0EnableOverride = 0  # bit 18 to 19
    Dpll1EnableOverride = 0  # bit 19 to 20
    GenlockPllEnableOverride = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 30
    IrefInverseRef = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPCLKA0_CFGCR0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPCLKA0_CFGCR0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DDIC_CLOCK_SELECT(Enum):
    DDIC_CLOCK_SELECT_DPLL2 = 0x0
    DDIC_CLOCK_SELECT_DPLL3 = 0x1


class ENUM_DDID_CLOCK_SELECT(Enum):
    DDID_CLOCK_SELECT_DPLL2 = 0x0
    DDID_CLOCK_SELECT_DPLL3 = 0x1


class ENUM_DDIC_CLOCK_OFF(Enum):
    DDIC_CLOCK_OFF_ON = 0x0
    DDIC_CLOCK_OFF_OFF = 0x1


class ENUM_DDID_CLOCK_OFF(Enum):
    DDID_CLOCK_OFF_ON = 0x0
    DDID_CLOCK_OFF_OFF = 0x1


class ENUM_DPLL2_INVERSE_REF(Enum):
    DPLL2_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL2_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL3_INVERSE_REF(Enum):
    DPLL3_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL3_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL2_ENABLE_OVERRIDE(Enum):
    DPLL2_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL2_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_DPLL3_ENABLE_OVERRIDE(Enum):
    DPLL3_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL3_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class OFFSET_DPCLKA1_CFGCR0:
    DPCLKA1_CFGCR0 = 0x16C280


class _DPCLKA1_CFGCR0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdicClockSelect', ctypes.c_uint32, 2),
        ('DdidClockSelect', ctypes.c_uint32, 2),
        ('Reserved4', ctypes.c_uint32, 6),
        ('DdicClockOff', ctypes.c_uint32, 1),
        ('DdidClockOff', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 3),
        ('Dpll2InverseRef', ctypes.c_uint32, 1),
        ('Dpll3InverseRef', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 1),
        ('Dpll2EnableOverride', ctypes.c_uint32, 1),
        ('Dpll3EnableOverride', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_DPCLKA1_CFGCR0(ctypes.Union):
    value = 0
    offset = 0

    DdicClockSelect = 0  # bit 0 to 2
    DdidClockSelect = 0  # bit 2 to 4
    Reserved4 = 0  # bit 4 to 10
    DdicClockOff = 0  # bit 10 to 11
    DdidClockOff = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 15
    Dpll2InverseRef = 0  # bit 15 to 16
    Dpll3InverseRef = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 18
    Dpll2EnableOverride = 0  # bit 18 to 19
    Dpll3EnableOverride = 0  # bit 19 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPCLKA1_CFGCR0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPCLKA1_CFGCR0, self).__init__()
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

