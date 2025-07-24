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
# @file Gen13PllRegs.py
# @brief contains Gen13PllRegs.py related register definitions

import ctypes
from enum import Enum


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
    AUDIO_IO_FLOP_BYPASS_BYPASS = 0x0
    AUDIO_IO_FLOP_BYPASS_DON_T_BYPASS = 0x1


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
        ('Spare0', ctypes.c_uint32, 1),
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

    Spare0 = 0  # bit 0 to 1
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
    CD_FREQUENCY_DECIMAL_176_MHZ_CD = 0x15E
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
    CD2X_DIVIDER_SELECT_DIVIDE_BY_1_5 = 0x1
    CD2X_DIVIDER_SELECT_DIVIDE_BY_2 = 0x2
    CD2X_DIVIDER_SELECT_DIVIDE_BY_4 = 0x3


class OFFSET_CDCLK_CTL:
    CDCLK_CTL = 0x46000


class _CDCLK_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CdFrequencyDecimal', ctypes.c_uint32, 11),
        ('Reserved11', ctypes.c_uint32, 4),
        ('Reserved15', ctypes.c_uint32, 1),
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
    Reserved15 = 0  # bit 15 to 16
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


class ENUM_FREQ_CHANGE_ACK(Enum):
    FREQ_CHANGE_ACK_NO_PENDING_REQUEST_OR_REQUEST_NOT_FINISHED = 0x0
    FREQ_CHANGE_ACK_REQUEST_FINISHED = 0x1


class ENUM_FREQ_CHANGE_REQ(Enum):
    FREQ_CHANGE_REQ_NO_REQUEST_PENDING = 0x0
    FREQ_CHANGE_REQ_REQUEST_PENDING = 0x1


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
        ('FreqChangeAck', ctypes.c_uint32, 1),
        ('FreqChangeReq', ctypes.c_uint32, 1),
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
    FreqChangeAck = 0  # bit 22 to 23
    FreqChangeReq = 0  # bit 23 to 24
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
    TBT_PLL_ENABLE = 0x46020
    PORTTC1_PLL0_ENABLE = 0x46034
    PORTTC1_PLL1_ENABLE = 0x46038
    PORTTC2_PLL0_ENABLE = 0x4603C
    PORTTC2_PLL1_ENABLE = 0x46040
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


class ENUM_MASTER_TIMING_GENERATOR_CLOCK_SELECT(Enum):
    MASTER_TIMING_GENERATOR_CLOCK_SELECT_DIV5 = 0x0
    MASTER_TIMING_GENERATOR_CLOCK_SELECT_DIV8 = 0x1


class OFFSET_DPCLKA_CFGCR1:
    DPCLKA_CFGCR1 = 0x1642BC


class _DPCLKA_CFGCR1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare_5To0', ctypes.c_uint32, 6),
        ('MasterTimingGeneratorClockSelect', ctypes.c_uint32, 1),
        ('Spare_31To7', ctypes.c_uint32, 25),
    ]


class REG_DPCLKA_CFGCR1(ctypes.Union):
    value = 0
    offset = 0

    Spare_5To0 = 0  # bit 0 to 6
    MasterTimingGeneratorClockSelect = 0  # bit 6 to 7
    Spare_31To7 = 0  # bit 7 to 32

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


class ENUM_CFG_I_FBDIV_INTGR_7_0(Enum):
    CFG_I_FBDIV_INTGR_7_0_CFG_I_FBDIV_INTGR_7_0_DEFAULTRESET = 0x82


class ENUM_CFG_I_FBPREDIV_3_0(Enum):
    CFG_I_FBPREDIV_3_0_CFG_I_FBPREDIV_3_0_DEFAULTRESET = 0x2


class ENUM_CFG_I_PROP_COEFF_3_0(Enum):
    CFG_I_PROP_COEFF_3_0_CFG_I_PROP_COEFF_3_0_DEFAULTRESET = 0x3


class ENUM_CFG_I_INT_COEFF_4_0(Enum):
    CFG_I_INT_COEFF_4_0_CFG_I_INT_COEFF_4_0_DEFAULTRESET = 0x7


class ENUM_CFG_I_GAINCTRL_2_0(Enum):
    CFG_I_GAINCTRL_2_0_CFG_I_GAINCTRL_2_0_DEFAULTRESET = 0x1


class ENUM_CFG_I_DIVRETIMEREN(Enum):
    CFG_I_DIVRETIMEREN_CFG_I_DIVRETIMEREN_DEFAULTRESET = 0x0


class ENUM_CFG_I_AFC_STARTUP_2_0(Enum):
    CFG_I_AFC_STARTUP_2_0_CFG_I_AFC_STARTUP_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_EARLYLOCK_CRITERIA_1_0(Enum):
    CFG_I_EARLYLOCK_CRITERIA_1_0_CFG_I_EARLYLOCK_CRITERIA_1_0_DEFAULTRESET = 0x3


class ENUM_CFG_I_TRUELOCK_CRITERIA_1_0(Enum):
    CFG_I_TRUELOCK_CRITERIA_1_0_CFG_I_TRUELOCK_CRITERIA_1_0_DEFAULTRESET = 0x1


class OFFSET_DKLP_PLL0_DIV0:
    DKLP_PLL0_DIV0 = 0x180


class _DKLP_PLL0_DIV0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Fbdiv_Intgr_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbprediv_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Prop_Coeff_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Int_Coeff_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Gainctrl_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Divretimeren', ctypes.c_uint32, 1),
        ('Cfg_I_Afc_Startup_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Earlylock_Criteria_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Truelock_Criteria_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKLP_PLL0_DIV0(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Fbdiv_Intgr_7_0 = 0  # bit 0 to 8
    Cfg_I_Fbprediv_3_0 = 0  # bit 8 to 12
    Cfg_I_Prop_Coeff_3_0 = 0  # bit 12 to 16
    Cfg_I_Int_Coeff_4_0 = 0  # bit 16 to 21
    Cfg_I_Gainctrl_2_0 = 0  # bit 21 to 24
    Cfg_I_Divretimeren = 0  # bit 24 to 25
    Cfg_I_Afc_Startup_2_0 = 0  # bit 25 to 28
    Cfg_I_Earlylock_Criteria_1_0 = 0  # bit 28 to 30
    Cfg_I_Truelock_Criteria_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_DIV0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_DIV0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_TDCTARGETCNT_7_0(Enum):
    CFG_I_TDCTARGETCNT_7_0_CFG_I_TDCTARGETCNT_7_0_DEFAULTRESET = 0x11


class ENUM_CFG_I_LOCKTHRESH_3_0(Enum):
    CFG_I_LOCKTHRESH_3_0_CFG_I_LOCKTHRESH_3_0_DEFAULTRESET = 0x5


class ENUM_CFG_I_DCODITHER_CONFIG(Enum):
    CFG_I_DCODITHER_CONFIG_CFG_I_DCODITHER_CONFIG_DEFAULTRESET = 0x0


class ENUM_CFG_I_BIASCAL_EN_H(Enum):
    CFG_I_BIASCAL_EN_H_CFG_I_BIASCAL_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_BIAS_FILTER_EN(Enum):
    CFG_I_BIAS_FILTER_EN_CFG_I_BIAS_FILTER_EN_DEFAULTRESET = 0x1


class ENUM_CFG_I_BIASFILTER_EN_DELAY(Enum):
    CFG_I_BIASFILTER_EN_DELAY_CFG_I_BIASFILTER_EN_DELAY_DEFAULTRESET = 0x1


class ENUM_CFG_I_IREFTRIM_4_0(Enum):
    CFG_I_IREFTRIM_4_0_CFG_I_IREFTRIM_4_0_DEFAULTRESET = 0x1C


class ENUM_CFG_I_BIAS_R_PROGRAMABILITY_1_0(Enum):
    CFG_I_BIAS_R_PROGRAMABILITY_1_0_CFG_I_BIAS_R_PROGRAMABILITY_1_0_DEFAULTRESET = 0x2


class ENUM_CFG_I_FASTLOCK_INTERNAL_RESET(Enum):
    CFG_I_FASTLOCK_INTERNAL_RESET_CFG_I_FASTLOCK_INTERNAL_RESET_DEFAULTRESET = 0x1


class ENUM_CFG_I_CTRIM_4_0(Enum):
    CFG_I_CTRIM_4_0_CFG_I_CTRIM_4_0_DEFAULTRESET = 0xC


class ENUM_CFG_I_BIAS_CALIB_STEPSIZE_1_0(Enum):
    CFG_I_BIAS_CALIB_STEPSIZE_1_0_CFG_I_BIAS_CALIB_STEPSIZE_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BW_AMPMEAS_WINDOW(Enum):
    CFG_I_BW_AMPMEAS_WINDOW_CFG_I_BW_AMPMEAS_WINDOW_DEFAULTRESET = 0x0


class OFFSET_DKLP_PLL0_DIV1:
    DKLP_PLL0_DIV1 = 0x184


class _DKLP_PLL0_DIV1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Tdctargetcnt_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Lockthresh_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Dcodither_Config', ctypes.c_uint32, 1),
        ('Cfg_I_Biascal_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Bias_Filter_En', ctypes.c_uint32, 1),
        ('Cfg_I_Biasfilter_En_Delay', ctypes.c_uint32, 1),
        ('Cfg_I_Ireftrim_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Bias_R_Programability_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Fastlock_Internal_Reset', ctypes.c_uint32, 1),
        ('Cfg_I_Ctrim_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Bias_Calib_Stepsize_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Bw_Ampmeas_Window', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL0_DIV1(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Tdctargetcnt_7_0 = 0  # bit 0 to 8
    Cfg_I_Lockthresh_3_0 = 0  # bit 8 to 12
    Cfg_I_Dcodither_Config = 0  # bit 12 to 13
    Cfg_I_Biascal_En_H = 0  # bit 13 to 14
    Cfg_I_Bias_Filter_En = 0  # bit 14 to 15
    Cfg_I_Biasfilter_En_Delay = 0  # bit 15 to 16
    Cfg_I_Ireftrim_4_0 = 0  # bit 16 to 21
    Cfg_I_Bias_R_Programability_1_0 = 0  # bit 21 to 23
    Cfg_I_Fastlock_Internal_Reset = 0  # bit 23 to 24
    Cfg_I_Ctrim_4_0 = 0  # bit 24 to 29
    Cfg_I_Bias_Calib_Stepsize_1_0 = 0  # bit 29 to 31
    Cfg_I_Bw_Ampmeas_Window = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_DIV1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_DIV1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_TDC_OFFSET_LOCK_1_0(Enum):
    CFG_I_TDC_OFFSET_LOCK_1_0_CFG_I_TDC_OFFSET_LOCK_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BBTHRESH1_2_0(Enum):
    CFG_I_BBTHRESH1_2_0_CFG_I_BBTHRESH1_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BBTHRESH2_2_0(Enum):
    CFG_I_BBTHRESH2_2_0_CFG_I_BBTHRESH2_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_DCOAMPOVRDEN_H(Enum):
    CFG_I_DCOAMPOVRDEN_H_CFG_I_DCOAMPOVRDEN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_DCOAMP_3_0(Enum):
    CFG_I_DCOAMP_3_0_CFG_I_DCOAMP_3_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BW_LOWERBOUND_2_0(Enum):
    CFG_I_BW_LOWERBOUND_2_0_CFG_I_BW_LOWERBOUND_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BW_UPPERBOUND_2_0(Enum):
    CFG_I_BW_UPPERBOUND_2_0_CFG_I_BW_UPPERBOUND_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BW_MODE_1_0(Enum):
    CFG_I_BW_MODE_1_0_CFG_I_BW_MODE_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_FT_MODE_SEL_2_0(Enum):
    CFG_I_FT_MODE_SEL_2_0_CFG_I_FT_MODE_SEL_2_0_DEFAULTRESET = 0x2


class ENUM_CFG_I_BWPHASE_4_0(Enum):
    CFG_I_BWPHASE_4_0_CFG_I_BWPHASE_4_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_PLLLOCK_SEL_1_0(Enum):
    CFG_I_PLLLOCK_SEL_1_0_CFG_I_PLLLOCK_SEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_AFC_DIVRATIO(Enum):
    CFG_I_AFC_DIVRATIO_CFG_I_AFC_DIVRATIO_DEFAULTRESET = 0x0


class OFFSET_DKLP_PLL0_LF:
    DKLP_PLL0_LF = 0x188


class _DKLP_PLL0_LF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Tdc_Offset_Lock_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Bbthresh1_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bbthresh2_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Dcoampovrden_H', ctypes.c_uint32, 1),
        ('Cfg_I_Dcoamp_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Bw_Lowerbound_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bw_Upperbound_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bw_Mode_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Ft_Mode_Sel_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bwphase_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Plllock_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Afc_Divratio', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL0_LF(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Tdc_Offset_Lock_1_0 = 0  # bit 0 to 2
    Cfg_I_Bbthresh1_2_0 = 0  # bit 2 to 5
    Cfg_I_Bbthresh2_2_0 = 0  # bit 5 to 8
    Cfg_I_Dcoampovrden_H = 0  # bit 8 to 9
    Cfg_I_Dcoamp_3_0 = 0  # bit 9 to 13
    Cfg_I_Bw_Lowerbound_2_0 = 0  # bit 13 to 16
    Cfg_I_Bw_Upperbound_2_0 = 0  # bit 16 to 19
    Cfg_I_Bw_Mode_1_0 = 0  # bit 19 to 21
    Cfg_I_Ft_Mode_Sel_2_0 = 0  # bit 21 to 24
    Cfg_I_Bwphase_4_0 = 0  # bit 24 to 29
    Cfg_I_Plllock_Sel_1_0 = 0  # bit 29 to 31
    Cfg_I_Afc_Divratio = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_LF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_LF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_INIT_CSELAFC_7_0(Enum):
    CFG_I_INIT_CSELAFC_7_0_CFG_I_INIT_CSELAFC_7_0_DEFAULTRESET = 0x6A


class ENUM_CFG_I_MAX_CSELAFC_7_0(Enum):
    CFG_I_MAX_CSELAFC_7_0_CFG_I_MAX_CSELAFC_7_0_DEFAULTRESET = 0x3F


class ENUM_CFG_I_FLLAFC_LOCKCNT_2_0(Enum):
    CFG_I_FLLAFC_LOCKCNT_2_0_CFG_I_FLLAFC_LOCKCNT_2_0_DEFAULTRESET = 0x4


class ENUM_CFG_I_FLLAFC_GAIN_3_0(Enum):
    CFG_I_FLLAFC_GAIN_3_0_CFG_I_FLLAFC_GAIN_3_0_DEFAULTRESET = 0x8


class ENUM_CFG_I_FASTLOCK_EN_H(Enum):
    CFG_I_FASTLOCK_EN_H_CFG_I_FASTLOCK_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_BB_GAIN1_2_0(Enum):
    CFG_I_BB_GAIN1_2_0_CFG_I_BB_GAIN1_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_BB_GAIN2_2_0(Enum):
    CFG_I_BB_GAIN2_2_0_CFG_I_BB_GAIN2_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_CML2CMOSBONUS_1_0(Enum):
    CFG_I_CML2CMOSBONUS_1_0_CFG_I_CML2CMOSBONUS_1_0_DEFAULTRESET = 0x0


class OFFSET_DKLP_PLL0_FRAC_LOCK:
    DKLP_PLL0_FRAC_LOCK = 0x18C


class _DKLP_PLL0_FRAC_LOCK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Init_Cselafc_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Max_Cselafc_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fllafc_Lockcnt_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Fllafc_Gain_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Fastlock_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Bb_Gain1_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bb_Gain2_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Cml2Cmosbonus_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKLP_PLL0_FRAC_LOCK(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Init_Cselafc_7_0 = 0  # bit 0 to 8
    Cfg_I_Max_Cselafc_7_0 = 0  # bit 8 to 16
    Cfg_I_Fllafc_Lockcnt_2_0 = 0  # bit 16 to 19
    Cfg_I_Fllafc_Gain_3_0 = 0  # bit 19 to 23
    Cfg_I_Fastlock_En_H = 0  # bit 23 to 24
    Cfg_I_Bb_Gain1_2_0 = 0  # bit 24 to 27
    Cfg_I_Bb_Gain2_2_0 = 0  # bit 27 to 30
    Cfg_I_Cml2Cmosbonus_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_FRAC_LOCK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_FRAC_LOCK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_INIT_DCOAMP_5_0(Enum):
    CFG_I_INIT_DCOAMP_5_0_CFG_I_INIT_DCOAMP_5_0_DEFAULTRESET = 0x3F


class ENUM_CFG_I_BIAS_GB_SEL_1_0(Enum):
    CFG_I_BIAS_GB_SEL_1_0_CFG_I_BIAS_GB_SEL_1_0_DEFAULTRESET = 0x3


class ENUM_CFG_I_SSCFLLEN_H(Enum):
    CFG_I_SSCFLLEN_H_CFG_I_SSCFLLEN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCEN_H(Enum):
    CFG_I_SSCEN_H_CFG_I_SSCEN_H_DEFAULTRESET = 0x1


class ENUM_CFG_I_SSC_OPENLOOP_EN_H(Enum):
    CFG_I_SSC_OPENLOOP_EN_H_CFG_I_SSC_OPENLOOP_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCSTEPNUM_2_0(Enum):
    CFG_I_SSCSTEPNUM_2_0_CFG_I_SSCSTEPNUM_2_0_DEFAULTRESET = 0x4


class ENUM_CFG_I_SSCFLL_UPDATE_SEL_1_0(Enum):
    CFG_I_SSCFLL_UPDATE_SEL_1_0_CFG_I_SSCFLL_UPDATE_SEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCSTEPLENGTH_7_0(Enum):
    CFG_I_SSCSTEPLENGTH_7_0_CFG_I_SSCSTEPLENGTH_7_0_DEFAULTRESET = 0x13


class ENUM_CFG_I_SSCINJ_EN_H(Enum):
    CFG_I_SSCINJ_EN_H_CFG_I_SSCINJ_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCINJ_ADAPT_EN_H(Enum):
    CFG_I_SSCINJ_ADAPT_EN_H_CFG_I_SSCINJ_ADAPT_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_I_SSCSTEPNUM_OFFSET_2_0(Enum):
    CFG_I_SSCSTEPNUM_OFFSET_2_0_CFG_I_SSCSTEPNUM_OFFSET_2_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_IREF_NDIVRATIO_2_0(Enum):
    CFG_I_IREF_NDIVRATIO_2_0_CFG_I_IREF_NDIVRATIO_2_0_DEFAULTRESET = 0x2


class OFFSET_DKLP_PLL0_SSC:
    DKLP_PLL0_SSC = 0x190


class _DKLP_PLL0_SSC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Init_Dcoamp_5_0', ctypes.c_uint32, 6),
        ('Cfg_I_Bias_Gb_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Sscfllen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Ssc_Openloop_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscstepnum_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Sscfll_Update_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Sscsteplength_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Sscinj_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscinj_Adapt_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscstepnum_Offset_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Iref_Ndivratio_2_0', ctypes.c_uint32, 3),
    ]


class REG_DKLP_PLL0_SSC(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Init_Dcoamp_5_0 = 0  # bit 0 to 6
    Cfg_I_Bias_Gb_Sel_1_0 = 0  # bit 6 to 8
    Cfg_I_Sscfllen_H = 0  # bit 8 to 9
    Cfg_I_Sscen_H = 0  # bit 9 to 10
    Cfg_I_Ssc_Openloop_En_H = 0  # bit 10 to 11
    Cfg_I_Sscstepnum_2_0 = 0  # bit 11 to 14
    Cfg_I_Sscfll_Update_Sel_1_0 = 0  # bit 14 to 16
    Cfg_I_Sscsteplength_7_0 = 0  # bit 16 to 24
    Cfg_I_Sscinj_En_H = 0  # bit 24 to 25
    Cfg_I_Sscinj_Adapt_En_H = 0  # bit 25 to 26
    Cfg_I_Sscstepnum_Offset_2_0 = 0  # bit 26 to 29
    Cfg_I_Iref_Ndivratio_2_0 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_SSC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_SSC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_SSCINJ_STEPSIZE_7_0(Enum):
    CFG_I_SSCINJ_STEPSIZE_7_0_CFG_I_SSCINJ_STEPSIZE_7_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_FBDIV_FRAC_7_0(Enum):
    CFG_I_FBDIV_FRAC_7_0_CFG_I_FBDIV_FRAC_7_0_DEFAULTRESET = 0x55


class ENUM_CFG_I_FBDIV_FRAC_15_8(Enum):
    CFG_I_FBDIV_FRAC_15_8_CFG_I_FBDIV_FRAC_15_8_DEFAULTRESET = 0x55


class ENUM_CFG_I_FBDIV_FRAC_21_16(Enum):
    CFG_I_FBDIV_FRAC_21_16_CFG_I_FBDIV_FRAC_21_16_DEFAULTRESET = 0xD


class ENUM_CFG_I_FRACNEN_H(Enum):
    CFG_I_FRACNEN_H_CFG_I_FRACNEN_H_DEFAULTRESET = 0x1


class ENUM_CFG_I_TDC_FINE_RES(Enum):
    CFG_I_TDC_FINE_RES_CFG_I_TDC_FINE_RES_DEFAULTRESET = 0x1


class OFFSET_DKLP_PLL0_BIAS:
    DKLP_PLL0_BIAS = 0x194


class _DKLP_PLL0_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Sscinj_Stepsize_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_15_8', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_21_16', ctypes.c_uint32, 6),
        ('Cfg_I_Fracnen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Tdc_Fine_Res', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL0_BIAS(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Sscinj_Stepsize_7_0 = 0  # bit 0 to 8
    Cfg_I_Fbdiv_Frac_7_0 = 0  # bit 8 to 16
    Cfg_I_Fbdiv_Frac_15_8 = 0  # bit 16 to 24
    Cfg_I_Fbdiv_Frac_21_16 = 0  # bit 24 to 30
    Cfg_I_Fracnen_H = 0  # bit 30 to 31
    Cfg_I_Tdc_Fine_Res = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_I_FEEDFWRDGAIN_7_0(Enum):
    CFG_I_FEEDFWRDGAIN_7_0_CFG_I_FEEDFWRDGAIN_7_0_DEFAULTRESET = 0x1C


class ENUM_CFG_I_SSCSTEPSIZE_7_0(Enum):
    CFG_I_SSCSTEPSIZE_7_0_CFG_I_SSCSTEPSIZE_7_0_DEFAULTRESET = 0x13


class ENUM_CFG_I_DCOCOARSE_7_0(Enum):
    CFG_I_DCOCOARSE_7_0_CFG_I_DCOCOARSE_7_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_TRIBUFCTRLEXT_4_0(Enum):
    CFG_I_TRIBUFCTRLEXT_4_0_CFG_I_TRIBUFCTRLEXT_4_0_DEFAULTRESET = 0x0


class ENUM_CFG_I_CLOADCTRLLEXT_4_2(Enum):
    CFG_I_CLOADCTRLLEXT_4_2_CFG_I_CLOADCTRLLEXT_4_2_DEFAULTRESET = 0x0


class OFFSET_DKLP_PLL0_TDC_COLDST_BIAS:
    DKLP_PLL0_TDC_COLDST_BIAS = 0x198


class _DKLP_PLL0_TDC_COLDST_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Feedfwrdgain_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Sscstepsize_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Dcocoarse_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Tribufctrlext_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Cloadctrllext_4_2', ctypes.c_uint32, 3),
    ]


class REG_DKLP_PLL0_TDC_COLDST_BIAS(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Feedfwrdgain_7_0 = 0  # bit 0 to 8
    Cfg_I_Sscstepsize_7_0 = 0  # bit 8 to 16
    Cfg_I_Dcocoarse_7_0 = 0  # bit 16 to 24
    Cfg_I_Tribufctrlext_4_0 = 0  # bit 24 to 29
    Cfg_I_Cloadctrllext_4_2 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL0_TDC_COLDST_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL0_TDC_COLDST_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_DIV0:
    DKLP_PLL1_DIV0 = 0x200


class _DKLP_PLL1_DIV0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Fbdiv_Intgr_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbprediv_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Prop_Coeff_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Int_Coeff_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Gainctrl_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Divretimeren', ctypes.c_uint32, 1),
        ('Cfg_I_Afc_Startup_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Earlylock_Criteria_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Truelock_Criteria_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKLP_PLL1_DIV0(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Fbdiv_Intgr_7_0 = 0  # bit 0 to 8
    Cfg_I_Fbprediv_3_0 = 0  # bit 8 to 12
    Cfg_I_Prop_Coeff_3_0 = 0  # bit 12 to 16
    Cfg_I_Int_Coeff_4_0 = 0  # bit 16 to 21
    Cfg_I_Gainctrl_2_0 = 0  # bit 21 to 24
    Cfg_I_Divretimeren = 0  # bit 24 to 25
    Cfg_I_Afc_Startup_2_0 = 0  # bit 25 to 28
    Cfg_I_Earlylock_Criteria_1_0 = 0  # bit 28 to 30
    Cfg_I_Truelock_Criteria_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_DIV0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_DIV0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_DIV1:
    DKLP_PLL1_DIV1 = 0x204


class _DKLP_PLL1_DIV1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Tdctargetcnt_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Lockthresh_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Dcodither_Config', ctypes.c_uint32, 1),
        ('Cfg_I_Biascal_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Bias_Filter_En', ctypes.c_uint32, 1),
        ('Cfg_I_Biasfilter_En_Delay', ctypes.c_uint32, 1),
        ('Cfg_I_Ireftrim_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Bias_R_Programability_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Fastlock_Internal_Reset', ctypes.c_uint32, 1),
        ('Cfg_I_Ctrim_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Bias_Calib_Stepsize_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Bw_Ampmeas_Window', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL1_DIV1(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Tdctargetcnt_7_0 = 0  # bit 0 to 8
    Cfg_I_Lockthresh_3_0 = 0  # bit 8 to 12
    Cfg_I_Dcodither_Config = 0  # bit 12 to 13
    Cfg_I_Biascal_En_H = 0  # bit 13 to 14
    Cfg_I_Bias_Filter_En = 0  # bit 14 to 15
    Cfg_I_Biasfilter_En_Delay = 0  # bit 15 to 16
    Cfg_I_Ireftrim_4_0 = 0  # bit 16 to 21
    Cfg_I_Bias_R_Programability_1_0 = 0  # bit 21 to 23
    Cfg_I_Fastlock_Internal_Reset = 0  # bit 23 to 24
    Cfg_I_Ctrim_4_0 = 0  # bit 24 to 29
    Cfg_I_Bias_Calib_Stepsize_1_0 = 0  # bit 29 to 31
    Cfg_I_Bw_Ampmeas_Window = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_DIV1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_DIV1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_LF:
    DKLP_PLL1_LF = 0x208


class _DKLP_PLL1_LF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Tdc_Offset_Lock_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Bbthresh1_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bbthresh2_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Dcoampovrden_H', ctypes.c_uint32, 1),
        ('Cfg_I_Dcoamp_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Bw_Lowerbound_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bw_Upperbound_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bw_Mode_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Ft_Mode_Sel_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bwphase_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Plllock_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Afc_Divratio', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL1_LF(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Tdc_Offset_Lock_1_0 = 0  # bit 0 to 2
    Cfg_I_Bbthresh1_2_0 = 0  # bit 2 to 5
    Cfg_I_Bbthresh2_2_0 = 0  # bit 5 to 8
    Cfg_I_Dcoampovrden_H = 0  # bit 8 to 9
    Cfg_I_Dcoamp_3_0 = 0  # bit 9 to 13
    Cfg_I_Bw_Lowerbound_2_0 = 0  # bit 13 to 16
    Cfg_I_Bw_Upperbound_2_0 = 0  # bit 16 to 19
    Cfg_I_Bw_Mode_1_0 = 0  # bit 19 to 21
    Cfg_I_Ft_Mode_Sel_2_0 = 0  # bit 21 to 24
    Cfg_I_Bwphase_4_0 = 0  # bit 24 to 29
    Cfg_I_Plllock_Sel_1_0 = 0  # bit 29 to 31
    Cfg_I_Afc_Divratio = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_LF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_LF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_FRAC_LOCK:
    DKLP_PLL1_FRAC_LOCK = 0x20C


class _DKLP_PLL1_FRAC_LOCK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Init_Cselafc_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Max_Cselafc_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fllafc_Lockcnt_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Fllafc_Gain_3_0', ctypes.c_uint32, 4),
        ('Cfg_I_Fastlock_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Bb_Gain1_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Bb_Gain2_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Cml2Cmosbonus_1_0', ctypes.c_uint32, 2),
    ]


class REG_DKLP_PLL1_FRAC_LOCK(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Init_Cselafc_7_0 = 0  # bit 0 to 8
    Cfg_I_Max_Cselafc_7_0 = 0  # bit 8 to 16
    Cfg_I_Fllafc_Lockcnt_2_0 = 0  # bit 16 to 19
    Cfg_I_Fllafc_Gain_3_0 = 0  # bit 19 to 23
    Cfg_I_Fastlock_En_H = 0  # bit 23 to 24
    Cfg_I_Bb_Gain1_2_0 = 0  # bit 24 to 27
    Cfg_I_Bb_Gain2_2_0 = 0  # bit 27 to 30
    Cfg_I_Cml2Cmosbonus_1_0 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_FRAC_LOCK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_FRAC_LOCK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_SSC:
    DKLP_PLL1_SSC = 0x210


class _DKLP_PLL1_SSC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Init_Dcoamp_5_0', ctypes.c_uint32, 6),
        ('Cfg_I_Bias_Gb_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Sscfllen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Ssc_Openloop_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscstepnum_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Sscfll_Update_Sel_1_0', ctypes.c_uint32, 2),
        ('Cfg_I_Sscsteplength_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Sscinj_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscinj_Adapt_En_H', ctypes.c_uint32, 1),
        ('Cfg_I_Sscstepnum_Offset_2_0', ctypes.c_uint32, 3),
        ('Cfg_I_Iref_Ndivratio_2_0', ctypes.c_uint32, 3),
    ]


class REG_DKLP_PLL1_SSC(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Init_Dcoamp_5_0 = 0  # bit 0 to 6
    Cfg_I_Bias_Gb_Sel_1_0 = 0  # bit 6 to 8
    Cfg_I_Sscfllen_H = 0  # bit 8 to 9
    Cfg_I_Sscen_H = 0  # bit 9 to 10
    Cfg_I_Ssc_Openloop_En_H = 0  # bit 10 to 11
    Cfg_I_Sscstepnum_2_0 = 0  # bit 11 to 14
    Cfg_I_Sscfll_Update_Sel_1_0 = 0  # bit 14 to 16
    Cfg_I_Sscsteplength_7_0 = 0  # bit 16 to 24
    Cfg_I_Sscinj_En_H = 0  # bit 24 to 25
    Cfg_I_Sscinj_Adapt_En_H = 0  # bit 25 to 26
    Cfg_I_Sscstepnum_Offset_2_0 = 0  # bit 26 to 29
    Cfg_I_Iref_Ndivratio_2_0 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_SSC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_SSC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_BIAS:
    DKLP_PLL1_BIAS = 0x214


class _DKLP_PLL1_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Sscinj_Stepsize_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_15_8', ctypes.c_uint32, 8),
        ('Cfg_I_Fbdiv_Frac_21_16', ctypes.c_uint32, 6),
        ('Cfg_I_Fracnen_H', ctypes.c_uint32, 1),
        ('Cfg_I_Tdc_Fine_Res', ctypes.c_uint32, 1),
    ]


class REG_DKLP_PLL1_BIAS(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Sscinj_Stepsize_7_0 = 0  # bit 0 to 8
    Cfg_I_Fbdiv_Frac_7_0 = 0  # bit 8 to 16
    Cfg_I_Fbdiv_Frac_15_8 = 0  # bit 16 to 24
    Cfg_I_Fbdiv_Frac_21_16 = 0  # bit 24 to 30
    Cfg_I_Fracnen_H = 0  # bit 30 to 31
    Cfg_I_Tdc_Fine_Res = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DKLP_PLL1_TDC_COLDST_BIAS:
    DKLP_PLL1_TDC_COLDST_BIAS = 0x218


class _DKLP_PLL1_TDC_COLDST_BIAS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_I_Feedfwrdgain_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Sscstepsize_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Dcocoarse_7_0', ctypes.c_uint32, 8),
        ('Cfg_I_Tribufctrlext_4_0', ctypes.c_uint32, 5),
        ('Cfg_I_Cloadctrllext_4_2', ctypes.c_uint32, 3),
    ]


class REG_DKLP_PLL1_TDC_COLDST_BIAS(ctypes.Union):
    value = 0
    offset = 0

    Cfg_I_Feedfwrdgain_7_0 = 0  # bit 0 to 8
    Cfg_I_Sscstepsize_7_0 = 0  # bit 8 to 16
    Cfg_I_Dcocoarse_7_0 = 0  # bit 16 to 24
    Cfg_I_Tribufctrlext_4_0 = 0  # bit 24 to 29
    Cfg_I_Cloadctrllext_4_2 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_PLL1_TDC_COLDST_BIAS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_PLL1_TDC_COLDST_BIAS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_OD_CLKTOP1_HSDIV_EN_H(Enum):
    CFG_OD_CLKTOP1_HSDIV_EN_H_CFG_OD_CLKTOP1_HSDIV_EN_H_DEFAULTRESET = 0x1


class ENUM_CFG_RESERVED500(Enum):
    CFG_RESERVED500_CFG_RESERVED500_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_DSDIV_EN_H(Enum):
    CFG_OD_CLKTOP1_DSDIV_EN_H_CFG_OD_CLKTOP1_DSDIV_EN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_H_OVRD(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_H_OVRD_CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_H_OVRD_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_H_OVRD(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_H_OVRD_CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_H_OVRD_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_DED_H_OVRD(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_DED_H_OVRD_CFG_OD_CLKTOP1_TLINEDRV_ENRIGHT_DED_H_OVRD_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_DED_H_OVRD(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_DED_H_OVRD_CFG_OD_CLKTOP1_TLINEDRV_ENLEFT_DED_H_OVRD_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_OVERRIDEEN(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_OVERRIDEEN_CFG_OD_CLKTOP1_TLINEDRV_OVERRIDEEN_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_DSDIV_DIVRATIO_3_0(Enum):
    CFG_OD_CLKTOP1_DSDIV_DIVRATIO_3_0_CFG_OD_CLKTOP1_DSDIV_DIVRATIO_3_0_DEFAULTRESET = 0xA


class ENUM_CFG_OD_CLKTOP1_HSDIV_DIVRATIO_1_0(Enum):
    CFG_OD_CLKTOP1_HSDIV_DIVRATIO_1_0_CFG_OD_CLKTOP1_HSDIV_DIVRATIO_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_TLINEDRV_CLKSEL_1_0(Enum):
    CFG_OD_CLKTOP1_TLINEDRV_CLKSEL_1_0_CFG_OD_CLKTOP1_TLINEDRV_CLKSEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLK_INPUTSEL(Enum):
    CFG_OD_CLKTOP1_CORECLK_INPUTSEL_CFG_OD_CLKTOP1_CORECLK_INPUTSEL_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED503(Enum):
    CFG_RESERVED503_CFG_RESERVED503_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_OUTCLK_BYPASSEN_H(Enum):
    CFG_OD_CLKTOP1_OUTCLK_BYPASSEN_H_CFG_OD_CLKTOP1_OUTCLK_BYPASSEN_H_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED502(Enum):
    CFG_RESERVED502_CFG_RESERVED502_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CLKTOP1_VHFCLK_TESTEN_H_1_0(Enum):
    CFG_OD_CLKTOP1_CLKTOP1_VHFCLK_TESTEN_H_1_0_CFG_OD_CLKTOP1_CLKTOP1_VHFCLK_TESTEN_H_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED501(Enum):
    CFG_RESERVED501_CFG_RESERVED501_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CLK2OBS_EN_H(Enum):
    CFG_OD_CLKTOP1_CLK2OBS_EN_H_CFG_OD_CLKTOP1_CLK2OBS_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CLKOBS_MUXSEL_1_0(Enum):
    CFG_OD_CLKTOP1_CLKOBS_MUXSEL_1_0_CFG_OD_CLKTOP1_CLKOBS_MUXSEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED504(Enum):
    CFG_RESERVED504_CFG_RESERVED504_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD0:
    DKLP_CMN_ANA_CMN_ANA_DWORD0 = 0x0C0


class _DKLP_CMN_ANA_CMN_ANA_DWORD0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Od_Clktop1_Hsdiv_En_H', ctypes.c_uint32, 1),
        ('Cfg_Reserved500', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Dsdiv_En_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Enright_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Enleft_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Enright_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Enleft_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Tlinedrv_Overrideen', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Dsdiv_Divratio_3_0', ctypes.c_uint32, 4),
        ('Cfg_Od_Clktop1_Hsdiv_Divratio_1_0', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop1_Tlinedrv_Clksel_1_0', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop1_Coreclk_Inputsel', ctypes.c_uint32, 1),
        ('Cfg_Reserved503', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Outclk_Bypassen_H', ctypes.c_uint32, 1),
        ('Cfg_Reserved502', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Clktop1_Vhfclk_Testen_H_1_0', ctypes.c_uint32, 2),
        ('Cfg_Reserved501', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop1_Clk2Obs_En_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Clkobs_Muxsel_1_0', ctypes.c_uint32, 2),
        ('Cfg_Reserved504', ctypes.c_uint32, 5),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD0(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Od_Clktop1_Hsdiv_En_H = 0  # bit 0 to 1
    Cfg_Reserved500 = 0  # bit 1 to 2
    Cfg_Od_Clktop1_Dsdiv_En_H = 0  # bit 2 to 3
    Cfg_Od_Clktop1_Tlinedrv_Enright_H_Ovrd = 0  # bit 3 to 4
    Cfg_Od_Clktop1_Tlinedrv_Enleft_H_Ovrd = 0  # bit 4 to 5
    Cfg_Od_Clktop1_Tlinedrv_Enright_Ded_H_Ovrd = 0  # bit 5 to 6
    Cfg_Od_Clktop1_Tlinedrv_Enleft_Ded_H_Ovrd = 0  # bit 6 to 7
    Cfg_Od_Clktop1_Tlinedrv_Overrideen = 0  # bit 7 to 8
    Cfg_Od_Clktop1_Dsdiv_Divratio_3_0 = 0  # bit 8 to 12
    Cfg_Od_Clktop1_Hsdiv_Divratio_1_0 = 0  # bit 12 to 14
    Cfg_Od_Clktop1_Tlinedrv_Clksel_1_0 = 0  # bit 14 to 16
    Cfg_Od_Clktop1_Coreclk_Inputsel = 0  # bit 16 to 17
    Cfg_Reserved503 = 0  # bit 17 to 18
    Cfg_Od_Clktop1_Outclk_Bypassen_H = 0  # bit 18 to 19
    Cfg_Reserved502 = 0  # bit 19 to 20
    Cfg_Od_Clktop1_Clktop1_Vhfclk_Testen_H_1_0 = 0  # bit 20 to 22
    Cfg_Reserved501 = 0  # bit 22 to 24
    Cfg_Od_Clktop1_Clk2Obs_En_H = 0  # bit 24 to 25
    Cfg_Od_Clktop1_Clkobs_Muxsel_1_0 = 0  # bit 25 to 27
    Cfg_Reserved504 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_RESERVED507(Enum):
    CFG_RESERVED507_CFG_RESERVED507_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKA_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKA_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKA_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_CORECLKA_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKA_BYPASS_CFG_OD_CLKTOP1_CORECLKA_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED506(Enum):
    CFG_RESERVED506_CFG_RESERVED506_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKB_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKB_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKB_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_CORECLKB_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKB_BYPASS_CFG_OD_CLKTOP1_CORECLKB_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_ON_PLL12CORECLKA_SELECT(Enum):
    CFG_ON_PLL12CORECLKA_SELECT_CFG_ON_PLL12CORECLKA_SELECT_DEFAULTRESET = 0x0


class ENUM_CFG_ON_PLL12CORECLKD_SELECT(Enum):
    CFG_ON_PLL12CORECLKD_SELECT_CFG_ON_PLL12CORECLKD_SELECT_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKA_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKA_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKA_DIVRATIO_7_0_DEFAULTRESET = 0x14


class ENUM_CFG_OD_CLKTOP1_CORECLKB_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKB_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKB_DIVRATIO_7_0_DEFAULTRESET = 0x8


class ENUM_CFG_RESERVED510(Enum):
    CFG_RESERVED510_CFG_RESERVED510_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKC_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKC_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKC_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_CORECLKC_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKC_BYPASS_CFG_OD_CLKTOP1_CORECLKC_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED509(Enum):
    CFG_RESERVED509_CFG_RESERVED509_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKD_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKD_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKD_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP1_CORECLKD_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKD_BYPASS_CFG_OD_CLKTOP1_CORECLKD_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED508(Enum):
    CFG_RESERVED508_CFG_RESERVED508_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD1:
    DKLP_CMN_ANA_CMN_ANA_DWORD1 = 0x0C4


class _DKLP_CMN_ANA_CMN_ANA_DWORD1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Reserved507', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclka_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclka_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved506', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkb_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkb_Bypass', ctypes.c_uint32, 1),
        ('Cfg_On_Pll12Coreclka_Select', ctypes.c_uint32, 1),
        ('Cfg_On_Pll12Coreclkd_Select', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclka_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Od_Clktop1_Coreclkb_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Reserved510', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkc_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkc_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved509', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkd_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkd_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved508', ctypes.c_uint32, 2),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD1(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Reserved507 = 0  # bit 0 to 1
    Cfg_Od_Clktop1_Coreclka_Divretimeren_H = 0  # bit 1 to 2
    Cfg_Od_Clktop1_Coreclka_Bypass = 0  # bit 2 to 3
    Cfg_Reserved506 = 0  # bit 3 to 4
    Cfg_Od_Clktop1_Coreclkb_Divretimeren_H = 0  # bit 4 to 5
    Cfg_Od_Clktop1_Coreclkb_Bypass = 0  # bit 5 to 6
    Cfg_On_Pll12Coreclka_Select = 0  # bit 6 to 7
    Cfg_On_Pll12Coreclkd_Select = 0  # bit 7 to 8
    Cfg_Od_Clktop1_Coreclka_Divratio_7_0 = 0  # bit 8 to 16
    Cfg_Od_Clktop1_Coreclkb_Divratio_7_0 = 0  # bit 16 to 24
    Cfg_Reserved510 = 0  # bit 24 to 25
    Cfg_Od_Clktop1_Coreclkc_Divretimeren_H = 0  # bit 25 to 26
    Cfg_Od_Clktop1_Coreclkc_Bypass = 0  # bit 26 to 27
    Cfg_Reserved509 = 0  # bit 27 to 28
    Cfg_Od_Clktop1_Coreclkd_Divretimeren_H = 0  # bit 28 to 29
    Cfg_Od_Clktop1_Coreclkd_Bypass = 0  # bit 29 to 30
    Cfg_Reserved508 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_OD_CLKTOP1_CORECLKC_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKC_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKC_DIVRATIO_7_0_DEFAULTRESET = 0xA


class ENUM_CFG_OD_CLKTOP1_CORECLKD_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKD_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKD_DIVRATIO_7_0_DEFAULTRESET = 0x4


class ENUM_CFG_RESERVED513(Enum):
    CFG_RESERVED513_CFG_RESERVED513_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKE_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKE_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKE_DIVRETIMEREN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKE_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKE_BYPASS_CFG_OD_CLKTOP1_CORECLKE_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED512(Enum):
    CFG_RESERVED512_CFG_RESERVED512_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKF_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP1_CORECLKF_DIVRETIMEREN_H_CFG_OD_CLKTOP1_CORECLKF_DIVRETIMEREN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKF_BYPASS(Enum):
    CFG_OD_CLKTOP1_CORECLKF_BYPASS_CFG_OD_CLKTOP1_CORECLKF_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED511(Enum):
    CFG_RESERVED511_CFG_RESERVED511_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP1_CORECLKE_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP1_CORECLKE_DIVRATIO_7_0_CFG_OD_CLKTOP1_CORECLKE_DIVRATIO_7_0_DEFAULTRESET = 0x19


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD2:
    DKLP_CMN_ANA_CMN_ANA_DWORD2 = 0x0C8


class _DKLP_CMN_ANA_CMN_ANA_DWORD2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Od_Clktop1_Coreclkc_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Od_Clktop1_Coreclkd_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Reserved513', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclke_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclke_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved512', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkf_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop1_Coreclkf_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved511', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop1_Coreclke_Divratio_7_0', ctypes.c_uint32, 8),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD2(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Od_Clktop1_Coreclkc_Divratio_7_0 = 0  # bit 0 to 8
    Cfg_Od_Clktop1_Coreclkd_Divratio_7_0 = 0  # bit 8 to 16
    Cfg_Reserved513 = 0  # bit 16 to 17
    Cfg_Od_Clktop1_Coreclke_Divretimeren_H = 0  # bit 17 to 18
    Cfg_Od_Clktop1_Coreclke_Bypass = 0  # bit 18 to 19
    Cfg_Reserved512 = 0  # bit 19 to 20
    Cfg_Od_Clktop1_Coreclkf_Divretimeren_H = 0  # bit 20 to 21
    Cfg_Od_Clktop1_Coreclkf_Bypass = 0  # bit 21 to 22
    Cfg_Reserved511 = 0  # bit 22 to 24
    Cfg_Od_Clktop1_Coreclke_Divratio_7_0 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_OD_CLKTOP2_HSDIV_EN_H(Enum):
    CFG_OD_CLKTOP2_HSDIV_EN_H_CFG_OD_CLKTOP2_HSDIV_EN_H_DEFAULTRESET = 0x1


class ENUM_CFG_RESERVED520(Enum):
    CFG_RESERVED520_CFG_RESERVED520_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_DSDIV_EN_H(Enum):
    CFG_OD_CLKTOP2_DSDIV_EN_H_CFG_OD_CLKTOP2_DSDIV_EN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD_CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_H_OVRD_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD_CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_H_OVRD_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD_CFG_OD_CLKTOP2_TLINEDRV_ENRIGHT_DED_H_OVRD_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD_CFG_OD_CLKTOP2_TLINEDRV_ENLEFT_DED_H_OVRD_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_OVERRIDEEN(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_OVERRIDEEN_CFG_OD_CLKTOP2_TLINEDRV_OVERRIDEEN_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_DSDIV_DIVRATIO_3_0(Enum):
    CFG_OD_CLKTOP2_DSDIV_DIVRATIO_3_0_CFG_OD_CLKTOP2_DSDIV_DIVRATIO_3_0_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_HSDIV_DIVRATIO_1_0(Enum):
    CFG_OD_CLKTOP2_HSDIV_DIVRATIO_1_0_CFG_OD_CLKTOP2_HSDIV_DIVRATIO_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_TLINEDRV_CLKSEL_1_0(Enum):
    CFG_OD_CLKTOP2_TLINEDRV_CLKSEL_1_0_CFG_OD_CLKTOP2_TLINEDRV_CLKSEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLK_INPUTSEL(Enum):
    CFG_OD_CLKTOP2_CORECLK_INPUTSEL_CFG_OD_CLKTOP2_CORECLK_INPUTSEL_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED523(Enum):
    CFG_RESERVED523_CFG_RESERVED523_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_OUTCLK_BYPASSEN_H(Enum):
    CFG_OD_CLKTOP2_OUTCLK_BYPASSEN_H_CFG_OD_CLKTOP2_OUTCLK_BYPASSEN_H_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED522(Enum):
    CFG_RESERVED522_CFG_RESERVED522_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_VHFCLK_TESTEN_H_1_0(Enum):
    CFG_OD_CLKTOP2_VHFCLK_TESTEN_H_1_0_CFG_OD_CLKTOP2_VHFCLK_TESTEN_H_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED521(Enum):
    CFG_RESERVED521_CFG_RESERVED521_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CLK2OBS_EN_H(Enum):
    CFG_OD_CLKTOP2_CLK2OBS_EN_H_CFG_OD_CLKTOP2_CLK2OBS_EN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CLKOBS_INPUTSEL_1_0(Enum):
    CFG_OD_CLKTOP2_CLKOBS_INPUTSEL_1_0_CFG_OD_CLKTOP2_CLKOBS_INPUTSEL_1_0_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED524(Enum):
    CFG_RESERVED524_CFG_RESERVED524_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD5:
    DKLP_CMN_ANA_CMN_ANA_DWORD5 = 0x0D4


class _DKLP_CMN_ANA_CMN_ANA_DWORD5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Od_Clktop2_Hsdiv_En_H', ctypes.c_uint32, 1),
        ('Cfg_Reserved520', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Dsdiv_En_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Enright_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Enleft_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Enright_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Enleft_Ded_H_Ovrd', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Tlinedrv_Overrideen', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Dsdiv_Divratio_3_0', ctypes.c_uint32, 4),
        ('Cfg_Od_Clktop2_Hsdiv_Divratio_1_0', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop2_Tlinedrv_Clksel_1_0', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop2_Coreclk_Inputsel', ctypes.c_uint32, 1),
        ('Cfg_Reserved523', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Outclk_Bypassen_H', ctypes.c_uint32, 1),
        ('Cfg_Reserved522', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Vhfclk_Testen_H_1_0', ctypes.c_uint32, 2),
        ('Cfg_Reserved521', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop2_Clk2Obs_En_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Clkobs_Inputsel_1_0', ctypes.c_uint32, 2),
        ('Cfg_Reserved524', ctypes.c_uint32, 5),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD5(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Od_Clktop2_Hsdiv_En_H = 0  # bit 0 to 1
    Cfg_Reserved520 = 0  # bit 1 to 2
    Cfg_Od_Clktop2_Dsdiv_En_H = 0  # bit 2 to 3
    Cfg_Od_Clktop2_Tlinedrv_Enright_H_Ovrd = 0  # bit 3 to 4
    Cfg_Od_Clktop2_Tlinedrv_Enleft_H_Ovrd = 0  # bit 4 to 5
    Cfg_Od_Clktop2_Tlinedrv_Enright_Ded_H_Ovrd = 0  # bit 5 to 6
    Cfg_Od_Clktop2_Tlinedrv_Enleft_Ded_H_Ovrd = 0  # bit 6 to 7
    Cfg_Od_Clktop2_Tlinedrv_Overrideen = 0  # bit 7 to 8
    Cfg_Od_Clktop2_Dsdiv_Divratio_3_0 = 0  # bit 8 to 12
    Cfg_Od_Clktop2_Hsdiv_Divratio_1_0 = 0  # bit 12 to 14
    Cfg_Od_Clktop2_Tlinedrv_Clksel_1_0 = 0  # bit 14 to 16
    Cfg_Od_Clktop2_Coreclk_Inputsel = 0  # bit 16 to 17
    Cfg_Reserved523 = 0  # bit 17 to 18
    Cfg_Od_Clktop2_Outclk_Bypassen_H = 0  # bit 18 to 19
    Cfg_Reserved522 = 0  # bit 19 to 20
    Cfg_Od_Clktop2_Vhfclk_Testen_H_1_0 = 0  # bit 20 to 22
    Cfg_Reserved521 = 0  # bit 22 to 24
    Cfg_Od_Clktop2_Clk2Obs_En_H = 0  # bit 24 to 25
    Cfg_Od_Clktop2_Clkobs_Inputsel_1_0 = 0  # bit 25 to 27
    Cfg_Reserved524 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_RESERVED527(Enum):
    CFG_RESERVED527_CFG_RESERVED527_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKA_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP2_CORECLKA_DIVRETIMEREN_H_BYPASS_THE_RETIMER_PATH = 0x0  # This is POR.
    CFG_OD_CLKTOP2_CORECLKA_DIVRETIMEREN_H_ENABLE_THE_RETIMER_PATH = 0x1


class ENUM_CFG_RESERVED526(Enum):
    CFG_RESERVED526_CFG_RESERVED526_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKB_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP2_CORECLKB_DIVRETIMEREN_H_BYPASS_THE_RETIMER_PATH = 0x0


class ENUM_CFG_RESERVED525(Enum):
    CFG_RESERVED525_CFG_RESERVED525_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKA_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP2_CORECLKA_DIVRATIO_7_0_CFG_OD_CLKTOP2_CORECLKA_DIVRATIO_7_0_DEFAULTRESET = 0x5


class ENUM_CFG_OD_CLKTOP2_CORECLKB_DIVRATIO_7_0(Enum):
    CFG_OD_CLKTOP2_CORECLKB_DIVRATIO_7_0_CFG_OD_CLKTOP2_CORECLKB_DIVRATIO_7_0_DEFAULTRESET = 0x8


class ENUM_CFG_RESERVED530(Enum):
    CFG_RESERVED530_CFG_RESERVED530_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKC_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP2_CORECLKC_DIVRETIMEREN_H_CFG_OD_CLKTOP2_CORECLKC_DIVRETIMEREN_H_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKC_BYPASS(Enum):
    CFG_OD_CLKTOP2_CORECLKC_BYPASS_CFG_OD_CLKTOP2_CORECLKC_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED529(Enum):
    CFG_RESERVED529_CFG_RESERVED529_DEFAULTRESET = 0x0


class ENUM_CFG_OD_CLKTOP2_CORECLKD_DIVRETIMEREN_H(Enum):
    CFG_OD_CLKTOP2_CORECLKD_DIVRETIMEREN_H_CFG_OD_CLKTOP2_CORECLKD_DIVRETIMEREN_H_DEFAULTRESET = 0x1


class ENUM_CFG_OD_CLKTOP2_CORECLKD_BYPASS(Enum):
    CFG_OD_CLKTOP2_CORECLKD_BYPASS_CFG_OD_CLKTOP2_CORECLKD_BYPASS_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED528(Enum):
    CFG_RESERVED528_CFG_RESERVED528_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD6:
    DKLP_CMN_ANA_CMN_ANA_DWORD6 = 0x0D8


class _DKLP_CMN_ANA_CMN_ANA_DWORD6(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Reserved527', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclka_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclka_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved526', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkb_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkb_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved525', ctypes.c_uint32, 2),
        ('Cfg_Od_Clktop2_Coreclka_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Od_Clktop2_Coreclkb_Divratio_7_0', ctypes.c_uint32, 8),
        ('Cfg_Reserved530', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkc_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkc_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved529', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkd_Divretimeren_H', ctypes.c_uint32, 1),
        ('Cfg_Od_Clktop2_Coreclkd_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Reserved528', ctypes.c_uint32, 2),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD6(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Reserved527 = 0  # bit 0 to 1
    Cfg_Od_Clktop2_Coreclka_Divretimeren_H = 0  # bit 1 to 2
    Cfg_Od_Clktop2_Coreclka_Bypass = 0  # bit 2 to 3
    Cfg_Reserved526 = 0  # bit 3 to 4
    Cfg_Od_Clktop2_Coreclkb_Divretimeren_H = 0  # bit 4 to 5
    Cfg_Od_Clktop2_Coreclkb_Bypass = 0  # bit 5 to 6
    Cfg_Reserved525 = 0  # bit 6 to 8
    Cfg_Od_Clktop2_Coreclka_Divratio_7_0 = 0  # bit 8 to 16
    Cfg_Od_Clktop2_Coreclkb_Divratio_7_0 = 0  # bit 16 to 24
    Cfg_Reserved530 = 0  # bit 24 to 25
    Cfg_Od_Clktop2_Coreclkc_Divretimeren_H = 0  # bit 25 to 26
    Cfg_Od_Clktop2_Coreclkc_Bypass = 0  # bit 26 to 27
    Cfg_Reserved529 = 0  # bit 27 to 28
    Cfg_Od_Clktop2_Coreclkd_Divretimeren_H = 0  # bit 28 to 29
    Cfg_Od_Clktop2_Coreclkd_Bypass = 0  # bit 29 to 30
    Cfg_Reserved528 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD6),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD6, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_OD_REFCLKIN1_REFCLKMUX_2_0(Enum):
    CFG_OD_REFCLKIN1_REFCLKMUX_2_0_CFG_OD_REFCLKIN1_REFCLKMUX_2_0_DEFAULTRESET = 0x1


class ENUM_CFG_OD_REFCLKIN1_REFCLKINJMUX(Enum):
    CFG_OD_REFCLKIN1_REFCLKINJMUX_CFG_OD_REFCLKIN1_REFCLKINJMUX_DEFAULTRESET = 0x0


class ENUM_CFG_OD_PLL10G_REFCLKIN_GENLOCK_REFCLKSEL(Enum):
    CFG_OD_PLL10G_REFCLKIN_GENLOCK_REFCLKSEL_CFG_OD_PLL10G_REFCLKIN_GENLOCK_REFCLKSEL_DEFAULTRESET = 0x0


class ENUM_CFG_OD_PLL10P3G_REFCLKIN_GENLOCK_REFCLKSEL(Enum):
    CFG_OD_PLL10P3G_REFCLKIN_GENLOCK_REFCLKSEL_CFG_OD_PLL10P3G_REFCLKIN_GENLOCK_REFCLKSEL_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED586(Enum):
    CFG_RESERVED586_CFG_RESERVED586_DEFAULTRESET = 0x0


class ENUM_CFG_OD_REFCLKIN2_REFCLKMUX_2_0(Enum):
    CFG_OD_REFCLKIN2_REFCLKMUX_2_0_CFG_OD_REFCLKIN2_REFCLKMUX_2_0_DEFAULTRESET = 0x3


class ENUM_CFG_OD_REFCLKIN2_REFCLKINJMUX(Enum):
    CFG_OD_REFCLKIN2_REFCLKINJMUX_CFG_OD_REFCLKIN2_REFCLKINJMUX_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED587(Enum):
    CFG_RESERVED587_CFG_RESERVED587_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED588(Enum):
    CFG_RESERVED588_CFG_RESERVED588_DEFAULTRESET = 0x0


class ENUM_CFG_RESERVED589(Enum):
    CFG_RESERVED589_CFG_RESERVED589_DEFAULTRESET = 0x0


class OFFSET_DKLP_CMN_ANA_CMN_ANA_DWORD27:
    DKLP_CMN_ANA_CMN_ANA_DWORD27 = 0x12C


class _DKLP_CMN_ANA_CMN_ANA_DWORD27(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Od_Refclkin1_Refclkmux_2_0', ctypes.c_uint32, 3),
        ('Cfg_Od_Refclkin1_Refclkinjmux', ctypes.c_uint32, 1),
        ('Cfg_Od_Pll10G_Refclkin_Genlock_Refclksel', ctypes.c_uint32, 1),
        ('Cfg_Od_Pll10P3G_Refclkin_Genlock_Refclksel', ctypes.c_uint32, 1),
        ('Cfg_Reserved586', ctypes.c_uint32, 2),
        ('Cfg_Od_Refclkin2_Refclkmux_2_0', ctypes.c_uint32, 3),
        ('Cfg_Od_Refclkin2_Refclkinjmux', ctypes.c_uint32, 1),
        ('Cfg_Reserved587', ctypes.c_uint32, 4),
        ('Cfg_Reserved588', ctypes.c_uint32, 8),
        ('Cfg_Reserved589', ctypes.c_uint32, 8),
    ]


class REG_DKLP_CMN_ANA_CMN_ANA_DWORD27(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Od_Refclkin1_Refclkmux_2_0 = 0  # bit 0 to 3
    Cfg_Od_Refclkin1_Refclkinjmux = 0  # bit 3 to 4
    Cfg_Od_Pll10G_Refclkin_Genlock_Refclksel = 0  # bit 4 to 5
    Cfg_Od_Pll10P3G_Refclkin_Genlock_Refclksel = 0  # bit 5 to 6
    Cfg_Reserved586 = 0  # bit 6 to 8
    Cfg_Od_Refclkin2_Refclkmux_2_0 = 0  # bit 8 to 11
    Cfg_Od_Refclkin2_Refclkinjmux = 0  # bit 11 to 12
    Cfg_Reserved587 = 0  # bit 12 to 16
    Cfg_Reserved588 = 0  # bit 16 to 24
    Cfg_Reserved589 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DKLP_CMN_ANA_CMN_ANA_DWORD27),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DKLP_CMN_ANA_CMN_ANA_DWORD27, self).__init__()
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


class OFFSET_DSI_ESC_CLK_DIV:
    DSI_ESC_CLK_DIV_0 = 0x6B090
    DSI_ESC_CLK_DIV_1 = 0x6B890


class _DSI_ESC_CLK_DIV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EscapeClockDividerM', ctypes.c_uint32, 9),
        ('Reserved9', ctypes.c_uint32, 7),
        ('ByteClocksPerEscapeClock', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DSI_ESC_CLK_DIV(ctypes.Union):
    value = 0
    offset = 0

    EscapeClockDividerM = 0  # bit 0 to 9
    Reserved9 = 0  # bit 9 to 16
    ByteClocksPerEscapeClock = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_ESC_CLK_DIV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_ESC_CLK_DIV, self).__init__()
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


class OFFSET_MIPIO_DW8:
    MIPIO_DW8_MIPIO_B = 0x6C1A0
    MIPIO_DW8_MIPIO_A = 0x1621A0


class _MIPIO_DW8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 16),
        ('EscapeClockDividerM', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_MIPIO_DW8(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 16
    EscapeClockDividerM = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MIPIO_DW8),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MIPIO_DW8, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

