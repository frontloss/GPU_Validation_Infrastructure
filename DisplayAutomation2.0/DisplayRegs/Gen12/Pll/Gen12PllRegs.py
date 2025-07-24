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
# @file Gen12PllRegs.py
# @brief contains Gen12PllRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_DISPLAYPORT_A_PRESENT(Enum):
    DISPLAYPORT_A_PRESENT_NOT_PRESENT = 0x0  # Port not present
    DISPLAYPORT_A_PRESENT_PRESENT = 0x1  # Port present


class ENUM_PART_IS_SOC(Enum):
    PART_IS_SOC_NOT_SOC = 0x0
    PART_IS_SOC_SOC = 0x1


class ENUM_PAVP_GT_GEN_SELECT(Enum):
    PAVP_GT_GEN_SELECT_GEN11_AND_ONWARDS = 0x0
    PAVP_GT_GEN_SELECT_GEN10_AND_EARLIER = 0x1


class ENUM_WD_VIDEO_FAULT_CONTINUE(Enum):
    WD_VIDEO_FAULT_CONTINUE_STOP_WRITES = 0x0
    WD_VIDEO_FAULT_CONTINUE_CONTINUE_WRITES = 0x1


class ENUM_AUDIO_IO_SELECT(Enum):
    AUDIO_IO_SELECT_SOUTH = 0x0
    AUDIO_IO_SELECT_NORTH = 0x1


class ENUM_AUDIO_IO_FLOP_BYPASS(Enum):
    AUDIO_IO_FLOP_BYPASS_DON_T_BYPASS = 0x0
    AUDIO_IO_FLOP_BYPASS_BYPASS = 0x1


class ENUM_DE_8K_DIS(Enum):
    DE_8K_DIS_ENABLE = 0x0  # 8k Capability Enabled
    DE_8K_DIS_DISABLE = 0x1  # 8k Capability Disabled


class ENUM_REFERENCE_FREQUENCY(Enum):
    REFERENCE_FREQUENCY_24_MHZ = 0x0
    REFERENCE_FREQUENCY_19_2_MHZ = 0x1
    REFERENCE_FREQUENCY_38_4_MHZ = 0x2
    REFERENCE_FREQUENCY_25_MHZ_TEST = 0x3


class OFFSET_DSSM:
    DSSM = 0x51004


class _DSSM(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayportAPresent', ctypes.c_uint32, 1),
        ('PartIsSoc', ctypes.c_uint32, 1),
        ('PavpGtGenSelect', ctypes.c_uint32, 1),
        ('WdVideoFaultContinue', ctypes.c_uint32, 1),
        ('AudioIoSelect', ctypes.c_uint32, 1),
        ('AudioIoFlopBypass', ctypes.c_uint32, 1),
        ('De8KDis', ctypes.c_uint32, 1),
        ('Spare7', ctypes.c_uint32, 1),
        ('Spare8', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('Spare10', ctypes.c_uint32, 1),
        ('Spare11', ctypes.c_uint32, 1),
        ('Spare12', ctypes.c_uint32, 1),
        ('Spare13', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('Spare15', ctypes.c_uint32, 1),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('Spare18', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('Spare20', ctypes.c_uint32, 1),
        ('Spare21', ctypes.c_uint32, 1),
        ('Spare22', ctypes.c_uint32, 1),
        ('Spare23', ctypes.c_uint32, 1),
        ('Spare24', ctypes.c_uint32, 1),
        ('Spare25', ctypes.c_uint32, 1),
        ('Spare26', ctypes.c_uint32, 1),
        ('Spare27', ctypes.c_uint32, 1),
        ('Spare28', ctypes.c_uint32, 1),
        ('ReferenceFrequency', ctypes.c_uint32, 3),
    ]


class REG_DSSM(ctypes.Union):
    value = 0
    offset = 0

    DisplayportAPresent = 0  # bit 0 to 1
    PartIsSoc = 0  # bit 1 to 2
    PavpGtGenSelect = 0  # bit 2 to 3
    WdVideoFaultContinue = 0  # bit 3 to 4
    AudioIoSelect = 0  # bit 4 to 5
    AudioIoFlopBypass = 0  # bit 5 to 6
    De8KDis = 0  # bit 6 to 7
    Spare7 = 0  # bit 7 to 8
    Spare8 = 0  # bit 8 to 9
    Spare9 = 0  # bit 9 to 10
    Spare10 = 0  # bit 10 to 11
    Spare11 = 0  # bit 11 to 12
    Spare12 = 0  # bit 12 to 13
    Spare13 = 0  # bit 13 to 14
    Spare14 = 0  # bit 14 to 15
    Spare15 = 0  # bit 15 to 16
    Spare16 = 0  # bit 16 to 17
    Spare17 = 0  # bit 17 to 18
    Spare18 = 0  # bit 18 to 19
    Spare19 = 0  # bit 19 to 20
    Spare20 = 0  # bit 20 to 21
    Spare21 = 0  # bit 21 to 22
    Spare22 = 0  # bit 22 to 23
    Spare23 = 0  # bit 23 to 24
    Spare24 = 0  # bit 24 to 25
    Spare25 = 0  # bit 25 to 26
    Spare26 = 0  # bit 26 to 27
    Spare27 = 0  # bit 27 to 28
    Spare28 = 0  # bit 28 to 29
    ReferenceFrequency = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSSM),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSSM, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CD_FREQUENCY_DECIMAL(Enum):
    CD_FREQUENCY_DECIMAL_168_MHZ_CD = 0x14E  # This value is default, but not valid.
    CD_FREQUENCY_DECIMAL_172_8_MHZ_CD = 0x158
    CD_FREQUENCY_DECIMAL_179_2_MHZ_CD = 0x164
    CD_FREQUENCY_DECIMAL_180_MHZ_CD = 0x166
    CD_FREQUENCY_DECIMAL_192_MHZ_CD = 0x17E
    CD_FREQUENCY_DECIMAL_307_2_MHZ_CD = 0x264
    CD_FREQUENCY_DECIMAL_312_MHZ_CD = 0x26E
    CD_FREQUENCY_DECIMAL_324_MHZ_CD = 0x286
    CD_FREQUENCY_DECIMAL_326_4MHZ_CD = 0x28B
    CD_FREQUENCY_DECIMAL_480MHZ_CD = 0x3BE
    CD_FREQUENCY_DECIMAL_552_MHZ_CD = 0x44E
    CD_FREQUENCY_DECIMAL_556_8_MHZ_CD = 0x458
    CD_FREQUENCY_DECIMAL_648_MHZ_CD = 0x50E
    CD_FREQUENCY_DECIMAL_652_8_MHZ_CD = 0x518


class ENUM_PAR0_CD_DIVMUX_OVERRIDE(Enum):
    PAR0_CD_DIVMUX_OVERRIDE_NORMAL = 0x0  # Par0 CD source selected by hardware
    PAR0_CD_DIVMUX_OVERRIDE_OVERRIDE_TO_DIVMUX = 0x1  # Debug override Par0 CD source to Divmux output


class ENUM_SSA_PRECHARGE_ENABLE(Enum):
    SSA_PRECHARGE_DISABLE = 0x0


class ENUM_OVERRIDE_TO_CRYSTAL(Enum):
    OVERRIDE_TO_CRYSTAL_NORMAL = 0x0
    OVERRIDE_TO_CRYSTAL_OVERRIDE = 0x1


class ENUM_OVERRIDE_TO_SLOW_CLOCK(Enum):
    OVERRIDE_TO_SLOW_CLOCK_NORMAL = 0x0
    OVERRIDE_TO_SLOW_CLOCK_OVERRIDE = 0x1


class ENUM_CD2X_PIPE_SELECT(Enum):
    CD2X_PIPE_SELECT_PIPE_A = 0x0
    CD2X_PIPE_SELECT_PIPE_B = 0x2
    CD2X_PIPE_SELECT_PIPE_C = 0x4
    CD2X_PIPE_SELECT_PIPE_D = 0x6
    CD2X_PIPE_SELECT_NONE = 0x7  # Double buffer enable is tied to 1 so that writes to the CD2X Divider Select will tak
                                 # e effect immediately.


class ENUM_CD2X_DIVIDER_SELECT(Enum):
    CD2X_DIVIDER_SELECT_DIVIDE_BY_1 = 0x0
    CD2X_DIVIDER_SELECT_DIVIDE_BY_2 = 0x2


class OFFSET_CDCLK_CTL:
    CDCLK_CTL = 0x46000


class _CDCLK_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CdFrequencyDecimal', ctypes.c_uint32, 11),
        ('Reserved11', ctypes.c_uint32, 4),
        ('Par0CdDivmuxOverride', ctypes.c_uint32, 1),
        ('SsaPrechargeEnable', ctypes.c_uint32, 1),
        ('OverrideToCrystal', ctypes.c_uint32, 1),
        ('OverrideToSlowClock', ctypes.c_uint32, 1),
        ('Cd2XPipeSelect', ctypes.c_uint32, 3),
        ('Cd2XDividerSelect', ctypes.c_uint32, 2),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_CDCLK_CTL(ctypes.Union):
    value = 0
    offset = 0

    CdFrequencyDecimal = 0  # bit 0 to 11
    Reserved11 = 0  # bit 11 to 15
    Par0CdDivmuxOverride = 0  # bit 15 to 16
    SsaPrechargeEnable = 0  # bit 16 to 17
    OverrideToCrystal = 0  # bit 17 to 18
    OverrideToSlowClock = 0  # bit 18 to 19
    Cd2XPipeSelect = 0  # bit 19 to 22
    Cd2XDividerSelect = 0  # bit 22 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CDCLK_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CDCLK_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PLL_RATIO(Enum):
    PLL_RATIO_28_DEFAULT = 0x1C  # Default value. Refer to the Clocks page for valid ratios to program.


class ENUM_SLOW_CLOCK_LOCK(Enum):
    SLOW_CLOCK_LOCK_NOT_LOCKED_OR_NOT_ENABLED = 0x0
    SLOW_CLOCK_LOCK_LOCKED = 0x1


class ENUM_SLOW_CLOCK_ENABLE(Enum):
    SLOW_CLOCK_DISABLE = 0x0
    SLOW_CLOCK_ENABLE = 0x1


class ENUM_PLL_LOCK(Enum):
    PLL_LOCK_NOT_LOCKED_OR_NOT_ENABLED = 0x0
    PLL_LOCK_LOCKED = 0x1


class ENUM_PLL_ENABLE(Enum):
    PLL_DISABLE = 0x0
    PLL_ENABLE = 0x1


class OFFSET_CDCLK_PLL_ENABLE:
    CDCLK_PLL_ENABLE = 0x46070


class _CDCLK_PLL_ENABLE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PllRatio', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 10),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Reserved24', ctypes.c_uint32, 2),
        ('SlowClockLock', ctypes.c_uint32, 1),
        ('SlowClockEnable', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 2),
        ('PllLock', ctypes.c_uint32, 1),
        ('PllEnable', ctypes.c_uint32, 1),
    ]


class REG_CDCLK_PLL_ENABLE(ctypes.Union):
    value = 0
    offset = 0

    PllRatio = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 11
    Reserved11 = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 22
    Reserved22 = 0  # bit 22 to 24
    Reserved24 = 0  # bit 24 to 26
    SlowClockLock = 0  # bit 26 to 27
    SlowClockEnable = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 30
    PllLock = 0  # bit 30 to 31
    PllEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CDCLK_PLL_ENABLE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CDCLK_PLL_ENABLE, self).__init__()
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
    DPLL4_CFGCR0 = 0x164294
    TBTPLL_CFGCR0 = 0x16429C


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
    DDIA_CLOCK_SELECT_DPLL4 = 0x2


class ENUM_DDIB_CLOCK_SELECT(Enum):
    DDIB_CLOCK_SELECT_DPLL0 = 0x0
    DDIB_CLOCK_SELECT_DPLL1 = 0x1
    DDIB_CLOCK_SELECT_DPLL4 = 0x2


class ENUM_DDIC_CLOCK_SELECT(Enum):
    DDIC_CLOCK_SELECT_DPLL0 = 0x0
    DDIC_CLOCK_SELECT_DPLL1 = 0x1
    DDIC_CLOCK_SELECT_DPLL4 = 0x2


class ENUM_DDIA_CLOCK_OFF(Enum):
    DDIA_CLOCK_OFF_ON = 0x0
    DDIA_CLOCK_OFF_OFF = 0x1


class ENUM_DDIB_CLOCK_OFF(Enum):
    DDIB_CLOCK_OFF_ON = 0x0
    DDIB_CLOCK_OFF_OFF = 0x1


class ENUM_TC1_CLOCK_OFF(Enum):
    TC1_CLOCK_OFF_ON = 0x0
    TC1_CLOCK_OFF_OFF = 0x1


class ENUM_TC2_CLOCK_OFF(Enum):
    TC2_CLOCK_OFF_ON = 0x0
    TC2_CLOCK_OFF_OFF = 0x1


class ENUM_TC3_CLOCK_OFF(Enum):
    TC3_CLOCK_OFF_ON = 0x0
    TC3_CLOCK_OFF_OFF = 0x1


class ENUM_DPLL0_INVERSE_REF(Enum):
    DPLL0_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL0_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL1_INVERSE_REF(Enum):
    DPLL1_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL1_INVERSE_REF_INVERSE = 0x1


class ENUM_TBTPLL_INVERSE_REF(Enum):
    TBTPLL_INVERSE_REF_NOT_INVERSE = 0x0
    TBTPLL_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL0_ENABLE_OVERRIDE(Enum):
    DPLL0_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL0_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_DPLL1_ENABLE_OVERRIDE(Enum):
    DPLL1_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL1_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_DPLL4_ENABLE_OVERRIDE(Enum):
    DPLL4_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    DPLL4_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class ENUM_TC4_CLOCK_OFF(Enum):
    TC4_CLOCK_OFF_ON = 0x0
    TC4_CLOCK_OFF_OFF = 0x1


class ENUM_TC5_CLOCK_OFF(Enum):
    TC5_CLOCK_OFF_ON = 0x0
    TC5_CLOCK_OFF_OFF = 0x1


class ENUM_TC6_CLOCK_OFF(Enum):
    TC6_CLOCK_OFF_ON = 0x0
    TC6_CLOCK_OFF_OFF = 0x1


class ENUM_DDIC_CLOCK_OFF(Enum):
    DDIC_CLOCK_OFF_ON = 0x0
    DDIC_CLOCK_OFF_OFF = 0x1


class ENUM_DPLL3_INVERSE_REF(Enum):
    DPLL3_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL3_INVERSE_REF_INVERSE = 0x1


class ENUM_DPLL4_INVERSE_REF(Enum):
    DPLL4_INVERSE_REF_NOT_INVERSE = 0x0
    DPLL4_INVERSE_REF_INVERSE = 0x1


class ENUM_IREF_INVERSE_REF(Enum):
    IREF_INVERSE_REF_NOT_INVERSE = 0x0
    IREF_INVERSE_REF_INVERSE = 0x1


class ENUM_TBTPLL_ENABLE_OVERRIDE(Enum):
    TBTPLL_ENABLE_OVERRIDE_NOT_FORCED = 0x0
    TBTPLL_ENABLE_OVERRIDE_FORCE_ENABLE = 0x1


class OFFSET_DPCLKA_CFGCR0:
    DPCLKA_CFGCR0 = 0x164280


class _DPCLKA_CFGCR0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiaClockSelect', ctypes.c_uint32, 2),
        ('DdibClockSelect', ctypes.c_uint32, 2),
        ('DdicClockSelect', ctypes.c_uint32, 2),
        ('MipiaHvmSel', ctypes.c_uint32, 2),
        ('MipicHvmSel', ctypes.c_uint32, 2),
        ('DdiaClockOff', ctypes.c_uint32, 1),
        ('DdibClockOff', ctypes.c_uint32, 1),
        ('Tc1ClockOff', ctypes.c_uint32, 1),
        ('Tc2ClockOff', ctypes.c_uint32, 1),
        ('Tc3ClockOff', ctypes.c_uint32, 1),
        ('Dpll0InverseRef', ctypes.c_uint32, 1),
        ('Dpll1InverseRef', ctypes.c_uint32, 1),
        ('TbtpllInverseRef', ctypes.c_uint32, 1),
        ('Dpll0EnableOverride', ctypes.c_uint32, 1),
        ('Dpll1EnableOverride', ctypes.c_uint32, 1),
        ('Dpll4EnableOverride', ctypes.c_uint32, 1),
        ('Tc4ClockOff', ctypes.c_uint32, 1),
        ('Tc5ClockOff', ctypes.c_uint32, 1),
        ('Tc6ClockOff', ctypes.c_uint32, 1),
        ('DdicClockOff', ctypes.c_uint32, 1),
        ('Dpll3InverseRef', ctypes.c_uint32, 1),
        ('Dpll4InverseRef', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 2),
        ('HvmIndependentMipiEnable', ctypes.c_uint32, 1),
        ('IrefInverseRef', ctypes.c_uint32, 1),
        ('TbtpllEnableOverride', ctypes.c_uint32, 1),
    ]


class REG_DPCLKA_CFGCR0(ctypes.Union):
    value = 0
    offset = 0

    DdiaClockSelect = 0  # bit 0 to 2
    DdibClockSelect = 0  # bit 2 to 4
    DdicClockSelect = 0  # bit 4 to 6
    MipiaHvmSel = 0  # bit 6 to 8
    MipicHvmSel = 0  # bit 8 to 10
    DdiaClockOff = 0  # bit 10 to 11
    DdibClockOff = 0  # bit 11 to 12
    Tc1ClockOff = 0  # bit 12 to 13
    Tc2ClockOff = 0  # bit 13 to 14
    Tc3ClockOff = 0  # bit 14 to 15
    Dpll0InverseRef = 0  # bit 15 to 16
    Dpll1InverseRef = 0  # bit 16 to 17
    TbtpllInverseRef = 0  # bit 17 to 18
    Dpll0EnableOverride = 0  # bit 18 to 19
    Dpll1EnableOverride = 0  # bit 19 to 20
    Dpll4EnableOverride = 0  # bit 20 to 21
    Tc4ClockOff = 0  # bit 21 to 22
    Tc5ClockOff = 0  # bit 22 to 23
    Tc6ClockOff = 0  # bit 23 to 24
    DdicClockOff = 0  # bit 24 to 25
    Dpll3InverseRef = 0  # bit 25 to 26
    Dpll4InverseRef = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 29
    HvmIndependentMipiEnable = 0  # bit 29 to 30
    IrefInverseRef = 0  # bit 30 to 31
    TbtpllEnableOverride = 0  # bit 31 to 32

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


class ENUM_CLOCK_SELECT(Enum):
    CLOCK_SELECT_NONE = 0x0  # Nothing selected. Clock is disabled for this DDI.
    CLOCK_SELECT_MG = 0x8  # Type-C PHY PLL output
    CLOCK_SELECT_TBT_162 = 0xC  # Thunderbolt 162 MHz
    CLOCK_SELECT_TBT_270 = 0xD  # Thunderbolt 270 MHz
    CLOCK_SELECT_TBT_540 = 0xE  # Thunderbolt 540 MHz
    CLOCK_SELECT_TBT_810 = 0xF  # Thunderbolt 810 MHz


class OFFSET_DDI_CLK_SEL:
    DDI_CLK_SEL_USBC1 = 0x4610C
    DDI_CLK_SEL_USBC2 = 0x46110
    DDI_CLK_SEL_USBC3 = 0x46114
    DDI_CLK_SEL_USBC4 = 0x46118
    DDI_CLK_SEL_USBC5 = 0x4611C
    DDI_CLK_SEL_USBC6 = 0x46120


class _DDI_CLK_SEL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 28),
        ('ClockSelect', ctypes.c_uint32, 4),
    ]


class REG_DDI_CLK_SEL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 28
    ClockSelect = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_CLK_SEL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_CLK_SEL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_PLL_DIV0:
    DKL_PLL1_DIV0 = 0x200


class _DKL_PLL_DIV0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Fbdiv_Intgr', ctypes.c_uint32, 8),
        ('I_Fbprediv_3_0', ctypes.c_uint32, 4),
        ('I_Prop_Coeff_3_0', ctypes.c_uint32, 4),
        ('I_Int_Coeff_4_0', ctypes.c_uint32, 5),
        ('I_Gainctrl_2_0', ctypes.c_uint32, 3),
        ('I_Divretimeren', ctypes.c_uint32, 1),
        ('I_Afc_Startup_2_0', ctypes.c_uint32, 3),
        ('I_Earlylock_Criteria_1_0', ctypes.c_uint32, 2),
        ('I_Truelock_Criteria_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKL_PLL_DIV0(ctypes.Union):
    value = 0
    offset = 0

    I_Fbdiv_Intgr = 0  # bit 0 to 8
    I_Fbprediv_3_0 = 0  # bit 8 to 12
    I_Prop_Coeff_3_0 = 0  # bit 12 to 16
    I_Int_Coeff_4_0 = 0  # bit 16 to 21
    I_Gainctrl_2_0 = 0  # bit 21 to 24
    I_Divretimeren = 0  # bit 24 to 25
    I_Afc_Startup_2_0 = 0  # bit 25 to 28
    I_Earlylock_Criteria_1_0 = 0  # bit 28 to 30
    I_Truelock_Criteria_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_PLL_DIV0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_PLL_DIV0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_I_BIAS_FILTER_EN(Enum):
    I_BIAS_FILTER_EN_DISABLE = 0x0
    I_BIAS_FILTER_EN_ENABLE = 0x1


class OFFSET_DKL_PLL_DIV1:
    DKL_PLL1_DIV1 = 0x204


class _DKL_PLL_DIV1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Tdctargetcnt_7_0', ctypes.c_uint32, 8),
        ('I_Lockthresh_3_0', ctypes.c_uint32, 4),
        ('I_Dcodither_Config', ctypes.c_uint32, 1),
        ('I_Biascal_En_H', ctypes.c_uint32, 1),
        ('I_Bias_Filter_En', ctypes.c_uint32, 1),
        ('I_Biasfilter_En_Delay', ctypes.c_uint32, 1),
        ('I_Ireftrim_4_0', ctypes.c_uint32, 5),
        ('I_Bias_R_Programmability', ctypes.c_uint32, 2),
        ('I_Fastlock_Internal_Reset', ctypes.c_uint32, 1),
        ('I_Ctrim_4_0', ctypes.c_uint32, 5),
        ('I_Bias_Calib_Stepsize_1_0', ctypes.c_uint32, 2),
        ('I_Bw_Ampmeas_Window', ctypes.c_uint32, 1),
    ]


class REG_DKL_PLL_DIV1(ctypes.Union):
    value = 0
    offset = 0

    I_Tdctargetcnt_7_0 = 0  # bit 0 to 8
    I_Lockthresh_3_0 = 0  # bit 8 to 12
    I_Dcodither_Config = 0  # bit 12 to 13
    I_Biascal_En_H = 0  # bit 13 to 14
    I_Bias_Filter_En = 0  # bit 14 to 15
    I_Biasfilter_En_Delay = 0  # bit 15 to 16
    I_Ireftrim_4_0 = 0  # bit 16 to 21
    I_Bias_R_Programmability = 0  # bit 21 to 23
    I_Fastlock_Internal_Reset = 0  # bit 23 to 24
    I_Ctrim_4_0 = 0  # bit 24 to 29
    I_Bias_Calib_Stepsize_1_0 = 0  # bit 29 to 31
    I_Bw_Ampmeas_Window = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_PLL_DIV1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_PLL_DIV1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_REFCLKIN_CTL:
    DKL_REFCLKIN_CTL = 0x12C


class _DKL_REFCLKIN_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Od_Refclkin1_Refclkmux', ctypes.c_uint32, 3),
        ('Od_Refclkin1_Refclkinjmux', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 4),
        ('Od_Refclkin2_Refclkmux', ctypes.c_uint32, 3),
        ('Od_Refclkin2_Refclkinjmux', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 20),
    ]


class REG_DKL_REFCLKIN_CTL(ctypes.Union):
    value = 0
    offset = 0

    Od_Refclkin1_Refclkmux = 0  # bit 0 to 3
    Od_Refclkin1_Refclkinjmux = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 8
    Od_Refclkin2_Refclkmux = 0  # bit 8 to 11
    Od_Refclkin2_Refclkinjmux = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_REFCLKIN_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_REFCLKIN_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_OD_CLKTOP2_HSDIV_EN_H(Enum):
    OD_CLKTOP2_HSDIV_EN_H_DISABLE = 0x0
    OD_CLKTOP2_HSDIV_EN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP2_DSDIV_EN_H(Enum):
    OD_CLKTOP2_DSDIV_EN_H_DISABLE = 0x0
    OD_CLKTOP2_DSDIV_EN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD(Enum):
    OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD(Enum):
    OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD(Enum):
    OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD(Enum):
    OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD_ENABLE = 0x1


class ENUM_OD_CLKTOP2_TLINEDRV_OVERRIDEEN(Enum):
    OD_CLKTOP2_TLINEDRV_OVERRIDEEN_DISABLE = 0x0
    OD_CLKTOP2_TLINEDRV_OVERRIDEEN_ENABLE = 0x1


class ENUM_OD_CLKTOP2_DSDIV_DIVRATIO(Enum):
    OD_CLKTOP2_DSDIV_DIVRATIO_NO_DIVISION = 0x0
    OD_CLKTOP2_DSDIV_DIVRATIO_NO_DIV = 0x1
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_2 = 0x2
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_3 = 0x3
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_4 = 0x4
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_5 = 0x5
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_6 = 0x6
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_7 = 0x7
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_8 = 0x8
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_9 = 0x9
    OD_CLKTOP2_DSDIV_DIVRATIO_DIVIDE_BY_10 = 0xA


class ENUM_OD_CLKTOP2_HSDIV_DIVRATIO(Enum):
    OD_CLKTOP2_HSDIV_DIVRATIO_DIVIDE_BY_2 = 0x0
    OD_CLKTOP2_HSDIV_DIVRATIO_DIVIDE_BY_3 = 0x1
    OD_CLKTOP2_HSDIV_DIVRATIO_DIVIDE_BY_5 = 0x2
    OD_CLKTOP2_HSDIV_DIVRATIO_DIVIDE_BY_7 = 0x3


class ENUM_OD_CLKTOP2_TLINEDRV_CLKSEL(Enum):
    OD_CLKTOP2_TLINEDRV_CLKSEL_HSCLKDIV_OUTPUT = 0x0
    OD_CLKTOP2_TLINEDRV_CLKSEL_ICLK_BYPASS_INPUT_FROM_OTHER_CLKTOP = 0x1
    OD_CLKTOP2_TLINEDRV_CLKSEL_DSDIV_OUTPUT_CLOCK = 0x2
    OD_CLKTOP2_TLINEDRV_CLKSEL_NONDIVIDED_PLL_CLOCK = 0x3


class ENUM_OD_CLKTOP2_CORECLK_INPUTSEL(Enum):
    OD_CLKTOP2_CORECLK_INPUTSEL_HSDIV_OUTPUT = 0x0
    OD_CLKTOP2_CORECLK_INPUTSEL_DSDIV_OUTPUT = 0x1


class ENUM_OD_CLKTOP2_OUTCLK_BYPASSEN_H(Enum):
    OD_CLKTOP2_OUTCLK_BYPASSEN_H_DISABLE = 0x0
    OD_CLKTOP2_OUTCLK_BYPASSEN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP2_CLK2OBS_EN_H(Enum):
    OD_CLKTOP2_CLK2OBS_EN_H_DISABLE = 0x0
    OD_CLKTOP2_CLK2OBS_EN_H_ENABLE = 0x1


class ENUM_OD_CLKTOP2_CLKOBS_INPUTSEL(Enum):
    OD_CLKTOP2_CLKOBS_INPUTSEL_HSDIV_OUTPUT_CLOCK = 0x0
    OD_CLKTOP2_CLKOBS_INPUTSEL_ICLK_BYPASS_INPUT_FROM_OTHER_CLKTOP = 0x1
    OD_CLKTOP2_CLKOBS_INPUTSEL_DSDIV_OUTPUT_CLOCK = 0x2
    OD_CLKTOP2_CLKOBS_INPUTSEL_NONDIVIDED_PLL_CLOCK = 0x3


class OFFSET_DKL_CLKTOP2_HSCLKCTL:
    DKL_CLKTOP2_HSCLKCTL = 0x0D4


class _DKL_CLKTOP2_HSCLKCTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Od_Clktop2_Hsdiv_En_H', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 1),
        ('Od_Clktop2_Dsdiv_En_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Enright_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Enleft_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Enright_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Enleft_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Od_Clktop2_Tlinedrv_Overrideen', ctypes.c_uint32, 1),
        ('Od_Clktop2_Dsdiv_Divratio', ctypes.c_uint32, 4),
        ('Od_Clktop2_Hsdiv_Divratio', ctypes.c_uint32, 2),
        ('Od_Clktop2_Tlinedrv_Clksel', ctypes.c_uint32, 2),
        ('Od_Clktop2_Coreclk_Inputsel', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 1),
        ('Od_Clktop2_Outclk_Bypassen_H', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 1),
        ('Od_Clktop2_Clktop_Vhfclk_Testen_H', ctypes.c_uint32, 2),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Od_Clktop2_Clk2Obs_En_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Clkobs_Inputsel', ctypes.c_uint32, 2),
        ('Reserved27', ctypes.c_uint32, 5),
    ]


class REG_DKL_CLKTOP2_HSCLKCTL(ctypes.Union):
    value = 0
    offset = 0

    Od_Clktop2_Hsdiv_En_H = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 2
    Od_Clktop2_Dsdiv_En_H = 0  # bit 2 to 3
    Od_Clktop2_Tlinedrv_Enright_H_Ovrd = 0  # bit 3 to 4
    Od_Clktop2_Tlinedrv_Enleft_H_Ovrd = 0  # bit 4 to 5
    Od_Clktop2_Tlinedrv_Enright_Ded_H_Ovrd = 0  # bit 5 to 6
    Od_Clktop2_Tlinedrv_Enleft_Ded_H_Ovrd = 0  # bit 6 to 7
    Od_Clktop2_Tlinedrv_Overrideen = 0  # bit 7 to 8
    Od_Clktop2_Dsdiv_Divratio = 0  # bit 8 to 12
    Od_Clktop2_Hsdiv_Divratio = 0  # bit 12 to 14
    Od_Clktop2_Tlinedrv_Clksel = 0  # bit 14 to 16
    Od_Clktop2_Coreclk_Inputsel = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 18
    Od_Clktop2_Outclk_Bypassen_H = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 20
    Od_Clktop2_Clktop_Vhfclk_Testen_H = 0  # bit 20 to 22
    Reserved22 = 0  # bit 22 to 24
    Od_Clktop2_Clk2Obs_En_H = 0  # bit 24 to 25
    Od_Clktop2_Clkobs_Inputsel = 0  # bit 25 to 27
    Reserved27 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_CLKTOP2_HSCLKCTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_CLKTOP2_HSCLKCTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_CLKTOP2_CORECLKCTL1:
    DKL_CLKTOP2_CORECLKCTL1 = 0x0D8


class _DKL_CLKTOP2_CORECLKCTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclka_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclka_Bypass', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkb_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkb_Bypass', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('Od_Clktop2_Coreclka_Divratio', ctypes.c_uint32, 8),
        ('Od_Clktop2_Coreclkb_Divratio', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkc_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkc_Bypass', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkd_Divretimeren_H', ctypes.c_uint32, 1),
        ('Od_Clktop2_Coreclkd_Bypass', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_DKL_CLKTOP2_CORECLKCTL1(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    Od_Clktop2_Coreclka_Divretimeren_H = 0  # bit 1 to 2
    Od_Clktop2_Coreclka_Bypass = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 4
    Od_Clktop2_Coreclkb_Divretimeren_H = 0  # bit 4 to 5
    Od_Clktop2_Coreclkb_Bypass = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    Od_Clktop2_Coreclka_Divratio = 0  # bit 8 to 16
    Od_Clktop2_Coreclkb_Divratio = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 25
    Od_Clktop2_Coreclkc_Divretimeren_H = 0  # bit 25 to 26
    Od_Clktop2_Coreclkc_Bypass = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 28
    Od_Clktop2_Coreclkd_Divretimeren_H = 0  # bit 28 to 29
    Od_Clktop2_Coreclkd_Bypass = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_CLKTOP2_CORECLKCTL1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_CLKTOP2_CORECLKCTL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_I_SSCINJ_EN_H(Enum):
    I_SSCINJ_EN_H_DISABLE = 0x0
    I_SSCINJ_EN_H_ENABLE = 0x1


class ENUM_I_SSCINJ_ADAPT_EN_H(Enum):
    I_SSCINJ_ADAPT_EN_H_DISABLE = 0x0
    I_SSCINJ_ADAPT_EN_H_ENABLE = 0x1


class OFFSET_DKL_SSC:
    DKL_SSC = 0x210


class _DKL_SSC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Init_Dcoamp_5_0', ctypes.c_uint32, 6),
        ('I_Bias_Gb_Sel_1_0', ctypes.c_uint32, 2),
        ('I_Sscfllen_H', ctypes.c_uint32, 1),
        ('I_Sscen_H', ctypes.c_uint32, 1),
        ('I_Ssc_Openloop_En_H', ctypes.c_uint32, 1),
        ('I_Sscstepnum_2_0', ctypes.c_uint32, 3),
        ('I_Sscfll_Update_Sel_1_0', ctypes.c_uint32, 2),
        ('I_Sscsteplength_7_0', ctypes.c_uint32, 8),
        ('I_Sscinj_En_H', ctypes.c_uint32, 1),
        ('I_Sscinj_Adapt_En_H', ctypes.c_uint32, 1),
        ('Ssc_Stepnum_Offset_2_0', ctypes.c_uint32, 3),
        ('I_Iref_Ndivratio_2_0', ctypes.c_uint32, 3),
    ]


class REG_DKL_SSC(ctypes.Union):
    value = 0
    offset = 0

    I_Init_Dcoamp_5_0 = 0  # bit 0 to 6
    I_Bias_Gb_Sel_1_0 = 0  # bit 6 to 8
    I_Sscfllen_H = 0  # bit 8 to 9
    I_Sscen_H = 0  # bit 9 to 10
    I_Ssc_Openloop_En_H = 0  # bit 10 to 11
    I_Sscstepnum_2_0 = 0  # bit 11 to 14
    I_Sscfll_Update_Sel_1_0 = 0  # bit 14 to 16
    I_Sscsteplength_7_0 = 0  # bit 16 to 24
    I_Sscinj_En_H = 0  # bit 24 to 25
    I_Sscinj_Adapt_En_H = 0  # bit 25 to 26
    Ssc_Stepnum_Offset_2_0 = 0  # bit 26 to 29
    I_Iref_Ndivratio_2_0 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_SSC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_SSC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_BIAS:
    DKL_BIAS = 0x214


class _DKL_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Sscinj_Stepsize_7_0', ctypes.c_uint32, 8),
        ('I_Fbdiv_Frac_7_0', ctypes.c_uint32, 8),
        ('I_Fbdiv_Frac_15_8', ctypes.c_uint32, 8),
        ('I_Fbdiv_Frac_21_16', ctypes.c_uint32, 6),
        ('I_Fracnen_H', ctypes.c_uint32, 1),
        ('I_Tdc_Fine_Res', ctypes.c_uint32, 1),
    ]


class REG_DKL_BIAS(ctypes.Union):
    value = 0
    offset = 0

    I_Sscinj_Stepsize_7_0 = 0  # bit 0 to 8
    I_Fbdiv_Frac_7_0 = 0  # bit 8 to 16
    I_Fbdiv_Frac_15_8 = 0  # bit 16 to 24
    I_Fbdiv_Frac_21_16 = 0  # bit 24 to 30
    I_Fracnen_H = 0  # bit 30 to 31
    I_Tdc_Fine_Res = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_TDC_COLDST_BIAS:
    DKL_TDC_COLDST_BIAS = 0x218


class _DKL_TDC_COLDST_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Feedfwdgain_7_0', ctypes.c_uint32, 8),
        ('I_Sscstepsize_7_0', ctypes.c_uint32, 8),
        ('I_Dcocoarse_7_0', ctypes.c_uint32, 8),
        ('I_Tribufctrlext_4_0', ctypes.c_uint32, 5),
        ('I_Cloadctrlext_4_2', ctypes.c_uint32, 3),
    ]


class REG_DKL_TDC_COLDST_BIAS(ctypes.Union):
    value = 0
    offset = 0

    I_Feedfwdgain_7_0 = 0  # bit 0 to 8
    I_Sscstepsize_7_0 = 0  # bit 8 to 16
    I_Dcocoarse_7_0 = 0  # bit 16 to 24
    I_Tribufctrlext_4_0 = 0  # bit 24 to 29
    I_Cloadctrlext_4_2 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_TDC_COLDST_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_TDC_COLDST_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPHY_ESC_CLK_DIV:
    DPHY_ESC_CLK_DIV_1 = 0x6C190
    DPHY_ESC_CLK_DIV_0 = 0x162190


class _DPHY_ESC_CLK_DIV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EscapeClockDividerM', ctypes.c_uint32, 9),
        ('Reserved9', ctypes.c_uint32, 7),
        ('ByteClocksPerEscapeClock', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DPHY_ESC_CLK_DIV(ctypes.Union):
    value = 0
    offset = 0

    EscapeClockDividerM = 0  # bit 0 to 9
    Reserved9 = 0  # bit 9 to 16
    ByteClocksPerEscapeClock = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPHY_ESC_CLK_DIV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPHY_ESC_CLK_DIV, self).__init__()
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


class OFFSET_DKL_PLL_LF:
    DKL_PLL_LF = 0x208


class _DKL_PLL_LF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Tdc_Offset_1_0', ctypes.c_uint32, 2),
        ('I_Bbthresh1_2_0', ctypes.c_uint32, 3),
        ('I_Bbthresh2_2_0', ctypes.c_uint32, 3),
        ('I_Dcoampovrrden_H', ctypes.c_uint32, 1),
        ('I_Dcoamp_3_0', ctypes.c_uint32, 4),
        ('I_Bw_Lowerbound_2_0', ctypes.c_uint32, 3),
        ('I_Bw_Upperbound_2_0', ctypes.c_uint32, 3),
        ('I_Bw_Mode_1_0', ctypes.c_uint32, 2),
        ('I_Ft_Mode_Sel_2_0', ctypes.c_uint32, 3),
        ('I_Bwphase_4_0', ctypes.c_uint32, 5),
        ('I_Plllock_Sel_1_0', ctypes.c_uint32, 2),
        ('I_Afc_Divratio', ctypes.c_uint32, 1),
    ]


class REG_DKL_PLL_LF(ctypes.Union):
    value = 0
    offset = 0

    I_Tdc_Offset_1_0 = 0  # bit 0 to 2
    I_Bbthresh1_2_0 = 0  # bit 2 to 5
    I_Bbthresh2_2_0 = 0  # bit 5 to 8
    I_Dcoampovrrden_H = 0  # bit 8 to 9
    I_Dcoamp_3_0 = 0  # bit 9 to 13
    I_Bw_Lowerbound_2_0 = 0  # bit 13 to 16
    I_Bw_Upperbound_2_0 = 0  # bit 16 to 19
    I_Bw_Mode_1_0 = 0  # bit 19 to 21
    I_Ft_Mode_Sel_2_0 = 0  # bit 21 to 24
    I_Bwphase_4_0 = 0  # bit 24 to 29
    I_Plllock_Sel_1_0 = 0  # bit 29 to 31
    I_Afc_Divratio = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_PLL_LF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_PLL_LF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_I_FASTLOCK_EN_H(Enum):
    I_FASTLOCK_EN_H_DISABLE = 0x0
    I_FASTLOCK_EN_H_ENABLE = 0x1


class OFFSET_DKL_PLL_FRAC_LOCK:
    DKL_PLL1_FRAC_LOCK = 0x20C


class _DKL_PLL_FRAC_LOCK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Init_Cselafc_7_0', ctypes.c_uint32, 8),
        ('I_Max_Cselafc_7_0', ctypes.c_uint32, 8),
        ('I_Fllafc_Lockcnt_2_0', ctypes.c_uint32, 3),
        ('I_Fllafc_Gain_3_0', ctypes.c_uint32, 4),
        ('I_Fastlock_En_H', ctypes.c_uint32, 1),
        ('I_Bb_Gain1_2_0', ctypes.c_uint32, 3),
        ('I_Bb_Gain2_2_0', ctypes.c_uint32, 3),
        ('I_Cml2Cmosbonus_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKL_PLL_FRAC_LOCK(ctypes.Union):
    value = 0
    offset = 0

    I_Init_Cselafc_7_0 = 0  # bit 0 to 8
    I_Max_Cselafc_7_0 = 0  # bit 8 to 16
    I_Fllafc_Lockcnt_2_0 = 0  # bit 16 to 19
    I_Fllafc_Gain_3_0 = 0  # bit 19 to 23
    I_Fastlock_En_H = 0  # bit 23 to 24
    I_Bb_Gain1_2_0 = 0  # bit 24 to 27
    I_Bb_Gain2_2_0 = 0  # bit 27 to 30
    I_Cml2Cmosbonus_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_PLL_FRAC_LOCK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_PLL_FRAC_LOCK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_CMN_ANA_DWORD28:
    DKL_CMN_ANA_DWORD28 = 0x130


class _DKL_CMN_ANA_DWORD28(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Clktop1_Plldivby2_2Dmon_En_H', ctypes.c_uint32, 1),
        ('Clktop1_Divby2Clk_Bypass_En', ctypes.c_uint32, 1),
        ('Clktop1_Vga_Clk_Sel', ctypes.c_uint32, 1),
        ('Clktop1_Vga_Clk2Dl_En', ctypes.c_uint32, 1),
        ('Clktop2_Plldivby2_2Dmon_En_H', ctypes.c_uint32, 1),
        ('Clktop2_Divby2Clk_Bypass_En', ctypes.c_uint32, 1),
        ('Clktop2_Vga_Clk_Sel', ctypes.c_uint32, 1),
        ('Clktop2_Vga_Clk2Dl_En', ctypes.c_uint32, 1),
        ('Refclkin1_Refclk_Dlane_Sel', ctypes.c_uint32, 2),
        ('Refclkin1_Refclk_Sel', ctypes.c_uint32, 1),
        ('Refclkin1_Refclk_Dlane_En', ctypes.c_uint32, 1),
        ('Refclkin2_Refclk_Dlane_Sel', ctypes.c_uint32, 2),
        ('Refclkin2_Refclk_Sel', ctypes.c_uint32, 1),
        ('Refclkin2_Refclk_Dlane_En', ctypes.c_uint32, 1),
        ('Clktop1_Id_Vga_Chpmp_Ck_Divratio', ctypes.c_uint32, 4),
        ('Clktop1_Id_Vga_Chpmp_Div_En_H', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 4),
        ('Clktop2_Id_Vga_Chpmp_Ck_Divratio', ctypes.c_uint32, 3),
        ('Clktop2_Id_Vga_Chpmp_Div_En_H', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_DKL_CMN_ANA_DWORD28(ctypes.Union):
    value = 0
    offset = 0

    Clktop1_Plldivby2_2Dmon_En_H = 0  # bit 0 to 1
    Clktop1_Divby2Clk_Bypass_En = 0  # bit 1 to 2
    Clktop1_Vga_Clk_Sel = 0  # bit 2 to 3
    Clktop1_Vga_Clk2Dl_En = 0  # bit 3 to 4
    Clktop2_Plldivby2_2Dmon_En_H = 0  # bit 4 to 5
    Clktop2_Divby2Clk_Bypass_En = 0  # bit 5 to 6
    Clktop2_Vga_Clk_Sel = 0  # bit 6 to 7
    Clktop2_Vga_Clk2Dl_En = 0  # bit 7 to 8
    Refclkin1_Refclk_Dlane_Sel = 0  # bit 8 to 10
    Refclkin1_Refclk_Sel = 0  # bit 10 to 11
    Refclkin1_Refclk_Dlane_En = 0  # bit 11 to 12
    Refclkin2_Refclk_Dlane_Sel = 0  # bit 12 to 14
    Refclkin2_Refclk_Sel = 0  # bit 14 to 15
    Refclkin2_Refclk_Dlane_En = 0  # bit 15 to 16
    Clktop1_Id_Vga_Chpmp_Ck_Divratio = 0  # bit 16 to 20
    Clktop1_Id_Vga_Chpmp_Div_En_H = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 25
    Clktop2_Id_Vga_Chpmp_Ck_Divratio = 0  # bit 25 to 28
    Clktop2_Id_Vga_Chpmp_Div_En_H = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_CMN_ANA_DWORD28),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_CMN_ANA_DWORD28, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_CMN_DIG_PLL_MISC:
    DKL_CMN_DIG_PLL_MISC = 0x03C


class _DKL_CMN_DIG_PLL_MISC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Od_Cri_Pll2_Pcie_Enable', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 15),
        ('Od_Cri_Cascaded_Pll1_Enable', ctypes.c_uint32, 1),
        ('Od_Cri_Cascaded_Pll2_Enable', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 14),
    ]


class REG_DKL_CMN_DIG_PLL_MISC(ctypes.Union):
    value = 0
    offset = 0

    Od_Cri_Pll2_Pcie_Enable = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 16
    Od_Cri_Cascaded_Pll1_Enable = 0  # bit 16 to 17
    Od_Cri_Cascaded_Pll2_Enable = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_CMN_DIG_PLL_MISC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_CMN_DIG_PLL_MISC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_XXX_TDC_CRO:
    DKL_XXX_TDC_CRO = 0x228


class _DKL_XXX_TDC_CRO(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Tdcdc_En_H', ctypes.c_uint32, 1),
        ('I_Swcap_Irefgen_Clkmode_1_0', ctypes.c_uint32, 2),
        ('I_Bbinlock_H', ctypes.c_uint32, 1),
        ('I_Coldstart', ctypes.c_uint32, 1),
        ('I_Irefbias_Startup_Pulse_Width_1_0', ctypes.c_uint32, 2),
        ('I_Irefbias_Startup_Pulse_Bypass', ctypes.c_uint32, 1),
        ('I_Irefint_En', ctypes.c_uint32, 1),
        ('I_Vgsbufen', ctypes.c_uint32, 1),
        ('I_Digdftswep', ctypes.c_uint32, 1),
        ('I_Irefdigdften', ctypes.c_uint32, 1),
        ('I_Iref_Refclk_Inv_En', ctypes.c_uint32, 1),
        ('I_Plllc_Regen_H', ctypes.c_uint32, 1),
        ('I_Plllc_En_Mode_Ctrl_1_0', ctypes.c_uint32, 2),
        ('I_Plllc_Ro_Regen_H', ctypes.c_uint32, 1),
        ('I_Plllc_Ro_Regdisable', ctypes.c_uint32, 1),
        ('I_Plllc_Ro_Mode_Ctrl', ctypes.c_uint32, 1),
        ('I_Plllc_Reg_Resetb_Ana_Mode_Ctrl', ctypes.c_uint32, 1),
        ('I_Plllc_Reg_Active_Standby', ctypes.c_uint32, 1),
        ('I_Plllc_Reg_Active_Standby_Mode_Ctrl', ctypes.c_uint32, 1),
        ('I_Plllc_Reg_Refclk_Ack', ctypes.c_uint32, 1),
        ('I_Plllc_Reg_Refclk_Ack_Mode_Ctrl', ctypes.c_uint32, 1),
        ('I_Plllc_Iref_Clock_Ovrd', ctypes.c_uint32, 1),
        ('I_Plllc_Iref_Clock_Sel_1_0', ctypes.c_uint32, 2),
        ('I_Dfx_Tdc_Disable', ctypes.c_uint32, 1),
        ('I_Dfx_Mdith_Disable', ctypes.c_uint32, 1),
        ('I_Dfx_Mdfx_Enable', ctypes.c_uint32, 1),
        ('I_Dfx_Postdiv_Disable', ctypes.c_uint32, 1),
        ('I_Plllc_Reg_Fullcalresetb', ctypes.c_uint32, 1),
    ]


class REG_DKL_XXX_TDC_CRO(ctypes.Union):
    value = 0
    offset = 0

    I_Tdcdc_En_H = 0  # bit 0 to 1
    I_Swcap_Irefgen_Clkmode_1_0 = 0  # bit 1 to 3
    I_Bbinlock_H = 0  # bit 3 to 4
    I_Coldstart = 0  # bit 4 to 5
    I_Irefbias_Startup_Pulse_Width_1_0 = 0  # bit 5 to 7
    I_Irefbias_Startup_Pulse_Bypass = 0  # bit 7 to 8
    I_Irefint_En = 0  # bit 8 to 9
    I_Vgsbufen = 0  # bit 9 to 10
    I_Digdftswep = 0  # bit 10 to 11
    I_Irefdigdften = 0  # bit 11 to 12
    I_Iref_Refclk_Inv_En = 0  # bit 12 to 13
    I_Plllc_Regen_H = 0  # bit 13 to 14
    I_Plllc_En_Mode_Ctrl_1_0 = 0  # bit 14 to 16
    I_Plllc_Ro_Regen_H = 0  # bit 16 to 17
    I_Plllc_Ro_Regdisable = 0  # bit 17 to 18
    I_Plllc_Ro_Mode_Ctrl = 0  # bit 18 to 19
    I_Plllc_Reg_Resetb_Ana_Mode_Ctrl = 0  # bit 19 to 20
    I_Plllc_Reg_Active_Standby = 0  # bit 20 to 21
    I_Plllc_Reg_Active_Standby_Mode_Ctrl = 0  # bit 21 to 22
    I_Plllc_Reg_Refclk_Ack = 0  # bit 22 to 23
    I_Plllc_Reg_Refclk_Ack_Mode_Ctrl = 0  # bit 23 to 24
    I_Plllc_Iref_Clock_Ovrd = 0  # bit 24 to 25
    I_Plllc_Iref_Clock_Sel_1_0 = 0  # bit 25 to 27
    I_Dfx_Tdc_Disable = 0  # bit 27 to 28
    I_Dfx_Mdith_Disable = 0  # bit 28 to 29
    I_Dfx_Mdfx_Enable = 0  # bit 29 to 30
    I_Dfx_Postdiv_Disable = 0  # bit 30 to 31
    I_Plllc_Reg_Fullcalresetb = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_XXX_TDC_CRO),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_XXX_TDC_CRO, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKL_PLL1_CNTR_XXXX_SETTINGS:
    DKL_PLL1_CNTR_BIST_SETTINGS = 0x244


class _DKL_PLL1_CNTR_XXXX_SETTINGS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('I_Irefgen_Settling_Time_Cntr_7_0', ctypes.c_uint32, 8),
        ('I_Irefgen_Settling_Time_Ro_Standby_1_0', ctypes.c_uint32, 2),
        ('Reserved196', ctypes.c_uint32, 5),
        ('Reserved197', ctypes.c_uint32, 1),
        ('Ai_Plllc_Reg_Fbclkext_Sel', ctypes.c_uint32, 1),
        ('I_Plllc_Reg_Longloopclk_Sel', ctypes.c_uint32, 1),
        ('I_Dither_Div_1_0', ctypes.c_uint32, 2),
        ('I_M1_Longloop_Sel', ctypes.c_uint32, 1),
        ('I_Dfx_Div_Cklo_1_0', ctypes.c_uint32, 2),
        ('Reserved203', ctypes.c_uint32, 1),
        ('Reserved204', ctypes.c_uint32, 4),
        ('Reserved205', ctypes.c_uint32, 4),
    ]


class REG_DKL_PLL1_CNTR_XXXX_SETTINGS(ctypes.Union):
    value = 0
    offset = 0

    I_Irefgen_Settling_Time_Cntr_7_0 = 0  # bit 0 to 8
    I_Irefgen_Settling_Time_Ro_Standby_1_0 = 0  # bit 8 to 10
    Reserved196 = 0  # bit 10 to 15
    Reserved197 = 0  # bit 15 to 16
    Ai_Plllc_Reg_Fbclkext_Sel = 0  # bit 16 to 17
    I_Plllc_Reg_Longloopclk_Sel = 0  # bit 17 to 18
    I_Dither_Div_1_0 = 0  # bit 18 to 20
    I_M1_Longloop_Sel = 0  # bit 20 to 21
    I_Dfx_Div_Cklo_1_0 = 0  # bit 21 to 23
    Reserved203 = 0  # bit 23 to 24
    Reserved204 = 0  # bit 24 to 28
    Reserved205 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKL_PLL1_CNTR_XXXX_SETTINGS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKL_PLL1_CNTR_XXXX_SETTINGS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

