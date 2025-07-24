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
# @file Gen15PllRegs.py
# @brief contains Gen15PllRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_PART_IS_SOC(Enum):
    PART_IS_SOC_NOT_SOC = 0x0
    PART_IS_SOC_SOC = 0x1


class ENUM_PAVP_GT_GEN_SELECT(Enum):
    PAVP_GT_GEN_SELECT_GEN11_AND_ONWARDS = 0x0
    PAVP_GT_GEN_SELECT_GEN10_AND_EARLIER = 0x1


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
        ('Spare_3', ctypes.c_uint32, 1),
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

    Spare0 = 0  # bit 0 to 0
    PartIsSoc = 0  # bit 1 to 1
    PavpGtGenSelect = 0  # bit 2 to 2
    Spare_3 = 0  # bit 3 to 3
    AudioIoSelect = 0  # bit 4 to 4
    AudioIoFlopBypass = 0  # bit 5 to 5
    De8KDis = 0  # bit 6 to 6
    Spare7 = 0  # bit 7 to 7
    Spare8 = 0  # bit 8 to 8
    Spare9 = 0  # bit 9 to 9
    Spare10 = 0  # bit 10 to 10
    Spare11 = 0  # bit 11 to 11
    Spare12 = 0  # bit 12 to 12
    Spare13 = 0  # bit 13 to 13
    Spare14 = 0  # bit 14 to 14
    Spare15 = 0  # bit 15 to 15
    Spare16 = 0  # bit 16 to 16
    Spare17 = 0  # bit 17 to 17
    Spare18 = 0  # bit 18 to 18
    Spare19 = 0  # bit 19 to 19
    Spare20 = 0  # bit 20 to 20
    Spare21 = 0  # bit 21 to 21
    Spare22 = 0  # bit 22 to 22
    Spare23 = 0  # bit 23 to 23
    Spare24 = 0  # bit 24 to 24
    Spare25 = 0  # bit 25 to 25
    Spare26 = 0  # bit 26 to 26
    Spare27 = 0  # bit 27 to 27
    Spare28 = 0  # bit 28 to 28
    ReferenceFrequency = 0  # bit 29 to 31

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


class ENUM_MDCLK_SOURCE_SELECT(Enum):
    MDCLK_SOURCE_SELECT_CD2XCLK = 0x0
    MDCLK_SOURCE_SELECT_CDCLK_PLL = 0x1


class OFFSET_CDCLK_CTL:
    CDCLK_CTL = 0x46000

class _CDCLK_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 11),
        ('Reserved11', ctypes.c_uint32, 5),
        ('SsaPrechargeEnable', ctypes.c_uint32, 1),
        ('OverrideToCrystal', ctypes.c_uint32, 1),
        ('OverrideToSlowClock', ctypes.c_uint32, 1),
        ('Cd2XPipeSelect', ctypes.c_uint32, 3),
        ('Cd2XDividerSelect', ctypes.c_uint32, 2),
        ('Reserved24', ctypes.c_uint32, 1),
        ('MdclkSourceSelect', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 6),
    ]


class REG_CDCLK_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 10
    Reserved11 = 0  # bit 11 to 15
    SsaPrechargeEnable = 0  # bit 16 to 16
    OverrideToCrystal = 0  # bit 17 to 17
    OverrideToSlowClock = 0  # bit 18 to 18
    Cd2XPipeSelect = 0  # bit 19 to 21
    Cd2XDividerSelect = 0  # bit 22 to 23
    Reserved24 = 0  # bit 24 to 24
    MdclkSourceSelect = 0  # bit 25 to 25
    Reserved26 = 0  # bit 26 to 31

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


class ENUM_SQUASH_WAVEFORM(Enum):
    SQUASH_WAVEFORM_NO_SQUASHING = 0xFFFF


class ENUM_SQUASH_WINDOW_SIZE(Enum):
    SQUASH_WINDOW_SIZE_SQUASH_WINDOW_SIZE_OF_16 = 0xF


class ENUM_SQUASH_ENABLE(Enum):
    SQUASH_ENABLE_SQUASHING_ENABLED = 0x1
    SQUASH_ENABLE_SQUASHING_DISABLED = 0x0


class OFFSET_CDCLK_SQUASH_CTL:
    CDCLK_SQUASH_CTL = 0x46008

class _CDCLK_SQUASH_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SquashWaveform', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 8),
        ('SquashWindowSize', ctypes.c_uint32, 4),
        ('Reserved28', ctypes.c_uint32, 3),
        ('SquashEnable', ctypes.c_uint32, 1),
    ]


class REG_CDCLK_SQUASH_CTL(ctypes.Union):
    value = 0
    offset = 0

    SquashWaveform = 0  # bit 0 to 15
    Reserved16 = 0  # bit 16 to 23
    SquashWindowSize = 0  # bit 24 to 27
    Reserved28 = 0  # bit 28 to 30
    SquashEnable = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CDCLK_SQUASH_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CDCLK_SQUASH_CTL, self).__init__()
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
        ('Reserved8', ctypes.c_uint32, 14),
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

    PllRatio = 0  # bit 0 to 7
    Reserved8 = 0  # bit 8 to 21
    FreqChangeAck = 0  # bit 22 to 22
    FreqChangeReq = 0  # bit 23 to 23
    Reserved24 = 0  # bit 24 to 25
    SlowClockLock = 0  # bit 26 to 26
    SlowClockEnable = 0  # bit 27 to 27
    Reserved28 = 0  # bit 28 to 29
    PllLock = 0  # bit 30 to 30
    PllEnable = 0  # bit 31 to 31

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


class ENUM_SSC_ENABLE_PLL_B(Enum):
    SSC_ENABLE_PLL_B_DISABLE = 0x0
    SSC_ENABLE_PLL_B_ENABLE = 0x1


class ENUM_SSC_ENABLE_PLL_A(Enum):
    SSC_ENABLE_PLL_A_DISABLE = 0x0
    SSC_ENABLE_PLL_A_ENABLE = 0x1


class ENUM_PHY_CLOCK_LANE_SELECT(Enum):
    PHY_CLOCK_LANE_SELECT_LANE_0 = 0x0
    PHY_CLOCK_LANE_SELECT_LANE_1 = 0x1


class ENUM_FORWARD_CLOCK_UNGATE(Enum):
    FORWARD_CLOCK_UNGATE_GATE = 0x0
    FORWARD_CLOCK_UNGATE_UNGATE = 0x1


class ENUM_DDI_CLOCK_SELECT(Enum):
    DDI_CLOCK_SELECT_NONE = 0x0  # Nothing selected. DDI clock up is disabled and gated.
    DDI_CLOCK_SELECT_MAXPCLK = 0x8  # PHY maxpclk, after lane selection
    DDI_CLOCK_SELECT_DIV18CLK = 0x9  # PHY div18 clock
    DDI_CLOCK_SELECT_TBT_162 = 0xC  # Thunderbolt 162 MHz
    DDI_CLOCK_SELECT_TBT_270 = 0xD  # Thunderbolt 270 MHz
    DDI_CLOCK_SELECT_TBT_540 = 0xE  # Thunderbolt 540 MHz
    DDI_CLOCK_SELECT_TBT_810 = 0xF  # Thunderbolt 810 MHz


class ENUM_TBT_CLOCK_ACK(Enum):
    TBT_CLOCK_ACK_NOT_ACK = 0x0
    TBT_CLOCK_ACK_ACK = 0x1


class ENUM_TBT_CLOCK_REQUEST(Enum):
    TBT_CLOCK_REQUEST_DISABLE = 0x0
    TBT_CLOCK_REQUEST_ENABLE = 0x1


class ENUM_ACK_PHY_RELEASE_REFCLK(Enum):
    ACK_PHY_RELEASE_REFCLK_NOT_ACK = 0x0
    ACK_PHY_RELEASE_REFCLK_ACK = 0x1


class ENUM_REQUEST_PHY_RELEASE_REFCLK(Enum):
    REQUEST_PHY_RELEASE_REFCLK_DON_T_REQUEST = 0x0
    REQUEST_PHY_RELEASE_REFCLK_REQUEST = 0x1


class ENUM_REFCLK_SELECT(Enum):
    REFCLK_SELECT_NORMAL = 0x0
    REFCLK_SELECT_GENLOCK = 0x1


class ENUM_PCLK_REFCLK_ACK_LN1(Enum):
    PCLK_REFCLK_ACK_LN1_NOT_ACK = 0x0
    PCLK_REFCLK_ACK_LN1_ACK = 0x1


class ENUM_PCLK_REFCLK_REQUEST_LN1(Enum):
    PCLK_REFCLK_REQUEST_LN1_DISABLE = 0x0
    PCLK_REFCLK_REQUEST_LN1_ENABLE = 0x1


class ENUM_PCLK_PLL_ACK_LN1(Enum):
    PCLK_PLL_ACK_LN1_NOT_ACK = 0x0
    PCLK_PLL_ACK_LN1_ACK = 0x1


class ENUM_PCLK_PLL_REQUEST_LN1(Enum):
    PCLK_PLL_REQUEST_LN1_DISABLE = 0x0
    PCLK_PLL_REQUEST_LN1_ENABLE = 0x1


class ENUM_PCLK_REFCLK_ACK_LN0(Enum):
    PCLK_REFCLK_ACK_LN0_NOT_ACK = 0x0
    PCLK_REFCLK_ACK_LN0_ACK = 0x1


class ENUM_PCLK_REFCLK_REQUEST_LN0(Enum):
    PCLK_REFCLK_REQUEST_LN0_DISABLE = 0x0
    PCLK_REFCLK_REQUEST_LN0_ENABLE = 0x1


class ENUM_PCLK_PLL_ACK_LN0(Enum):
    PCLK_PLL_ACK_LN0_NOT_ACK = 0x0
    PCLK_PLL_ACK_LN0_ACK = 0x1


class ENUM_PCLK_PLL_REQUEST_LN0(Enum):
    PCLK_PLL_REQUEST_LN0_DISABLE = 0x0
    PCLK_PLL_REQUEST_LN0_ENABLE = 0x1


class OFFSET_PORT_CLOCK_CTL:
    PORT_CLOCK_CTL_USBC1 = 0x16F260
    PORT_CLOCK_CTL_USBC2 = 0x16F460
    PORT_CLOCK_CTL_USBC3 = 0x16F660
    PORT_CLOCK_CTL_USBC4 = 0x16F860
    PORT_CLOCK_CTL_A = 0x16FA60
    PORT_CLOCK_CTL_B = 0x16FC60

class _PORT_CLOCK_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SscEnablePllB', ctypes.c_uint32, 1),
        ('SscEnablePllA', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 6),
        ('PhyClockLaneSelect', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 1),
        ('ForwardClockUngate', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 1),
        ('DdiClockSelect', ctypes.c_uint32, 4),
        ('Reserved16', ctypes.c_uint32, 2),
        ('TbtClockAck', ctypes.c_uint32, 1),
        ('TbtClockRequest', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 1),
        ('AckPhyReleaseRefclk', ctypes.c_uint32, 1),
        ('RequestPhyReleaseRefclk', ctypes.c_uint32, 1),
        ('RefclkSelect', ctypes.c_uint32, 1),
        ('PclkRefclkAckLn1', ctypes.c_uint32, 1),
        ('PclkRefclkRequestLn1', ctypes.c_uint32, 1),
        ('PclkPllAckLn1', ctypes.c_uint32, 1),
        ('PclkPllRequestLn1', ctypes.c_uint32, 1),
        ('PclkRefclkAckLn0', ctypes.c_uint32, 1),
        ('PclkRefclkRequestLn0', ctypes.c_uint32, 1),
        ('PclkPllAckLn0', ctypes.c_uint32, 1),
        ('PclkPllRequestLn0', ctypes.c_uint32, 1),
    ]


class REG_PORT_CLOCK_CTL(ctypes.Union):
    value = 0
    offset = 0

    SscEnablePllB = 0  # bit 0 to 0
    SscEnablePllA = 0  # bit 1 to 1
    Reserved2 = 0  # bit 2 to 7
    PhyClockLaneSelect = 0  # bit 8 to 8
    Reserved9 = 0  # bit 9 to 9
    ForwardClockUngate = 0  # bit 10 to 10
    Reserved11 = 0  # bit 11 to 11
    DdiClockSelect = 0  # bit 12 to 15
    Reserved16 = 0  # bit 16 to 17
    TbtClockAck = 0  # bit 18 to 18
    TbtClockRequest = 0  # bit 19 to 19
    Reserved20 = 0  # bit 20 to 20
    AckPhyReleaseRefclk = 0  # bit 21 to 21
    RequestPhyReleaseRefclk = 0  # bit 22 to 22
    RefclkSelect = 0  # bit 23 to 23
    PclkRefclkAckLn1 = 0  # bit 24 to 24
    PclkRefclkRequestLn1 = 0  # bit 25 to 25
    PclkPllAckLn1 = 0  # bit 26 to 26
    PclkPllRequestLn1 = 0  # bit 27 to 27
    PclkRefclkAckLn0 = 0  # bit 28 to 28
    PclkRefclkRequestLn0 = 0  # bit 29 to 29
    PclkPllAckLn0 = 0  # bit 30 to 30
    PclkPllRequestLn0 = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CLOCK_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CLOCK_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CMTG_B_CLOCK_SELECT(Enum):
    CMTG_B_CLOCK_SELECT_CLOCK_DISABLED = 0x0


class ENUM_CMTG_A_CLOCK_SELECT(Enum):
    CMTG_A_CLOCK_SELECT_CLOCK_DISABLED = 0x0


class OFFSET_CMTG_CLK_SEL:
    CMTG_CLK_SEL = 0x46160

class _CMTG_CLK_SEL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 13),
        ('CmtgBClockSelect', ctypes.c_uint32, 3),
        ('Reserved16', ctypes.c_uint32, 13),
        ('CmtgAClockSelect', ctypes.c_uint32, 3),
    ]


class REG_CMTG_CLK_SEL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    CmtgBClockSelect = 0  # bit 13 to 15
    Reserved16 = 0  # bit 16 to 28
    CmtgAClockSelect = 0  # bit 29 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CMTG_CLK_SEL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CMTG_CLK_SEL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

