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
# @file Gen15Regs.py
# @brief contains Gen15Regs.py related register definitions

import ctypes
from enum import Enum


class ENUM_RST_PCH_HANDSHAKE_EN(Enum):
    RST_PCH_HANDSHAKE_EN_DISABLE = 0x0
    RST_PCH_HANDSHAKE_EN_ENABLE = 0x1


class ENUM_RST_PICA_HANDSHAKE_EN(Enum):
    RST_PICA_HANDSHAKE_EN_DISABLE = 0x0
    RST_PICA_HANDSHAKE_EN_ENABLE = 0x1


class OFFSET_NDE_RSTWRN_OPT:
    NDE_RSTWRN_OPT = 0x46408

class _NDE_RSTWRN_OPT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 4),
        ('RstPchHandshakeEn', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 1),
        ('RstPicaHandshakeEn', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 25),
    ]


class REG_NDE_RSTWRN_OPT(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 3
    RstPchHandshakeEn = 0  # bit 4 to 4
    Reserved5 = 0  # bit 5 to 5
    RstPicaHandshakeEn = 0  # bit 6 to 6
    Reserved7 = 0  # bit 7 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _NDE_RSTWRN_OPT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_NDE_RSTWRN_OPT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ERROR_INJECTION_FLIP_BITS(Enum):
    ERROR_INJECTION_FLIP_BITS_NO_ERRORS = 0x0  # No bits will be flipped
    ERROR_INJECTION_FLIP_BITS_FLIP_BIT_0 = 0x1  # Flip bit 0 of the static Data + ECC value. Should result in a Single 
                                                # bit error
    ERROR_INJECTION_FLIP_BITS_FLIP_BIT_1 = 0x2  # Flip bit 1of the static Data + ECC value. Should result in a Single b
                                                # it error
    ERROR_INJECTION_FLIP_BITS_FLIP_BITS_0_AND_1 = 0x3  # Flip bits 0 and 1 of the staticData + ECC value. Should result
                                                       #  in a Double bit error


class ENUM_ECC_ERROR_INJECTION_ENABLE(Enum):
    ECC_ERROR_INJECTION_DISABLED = 0x0
    ECC_ERROR_INJECTION_ENABLED = 0x1


class ENUM_B2B_WRITE_DISABLE(Enum):
    B2B_WRITE_ENABLE = 0x0  # B2B Writes are allowed.
    B2B_WRITE_DISABLE = 0x1  # B2B Writes are not allowed.


class ENUM_B2B_READ_DISABLE(Enum):
    B2B_READ_ENABLE = 0x0  # B2B Reads are allowed.
    B2B_READ_DISABLE = 0x1  # B2B Reads are not allowed.


class ENUM_DISPLAY_REORDER_BUFFER_DISABLE(Enum):
    DISPLAY_REORDER_BUFFER_ENABLE = 0x0
    DISPLAY_REORDER_BUFFER_DISABLE = 0x1


class ENUM_DBUF_POWER_STATE(Enum):
    DBUF_POWER_STATE_DISABLED = 0x0
    DBUF_POWER_STATE_ENABLED = 0x1


class ENUM_DBUF_POWER_REQUEST(Enum):
    DBUF_POWER_REQUEST_DISABLE = 0x0
    DBUF_POWER_REQUEST_ENABLE = 0x1


class OFFSET_DBUF_CTL:
    DBUF_CTL_S2 = 0x44300
    DBUF_CTL_S3 = 0x44304
    DBUF_CTL_S1 = 0x44FE8
    DBUF_CTL_S0 = 0x45008

class _DBUF_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 4),
        ('ErrorInjectionFlipBits', ctypes.c_uint32, 2),
        ('Reserved6', ctypes.c_uint32, 1),
        ('EccErrorInjectionEnable', ctypes.c_uint32, 1),
        ('B2BWriteDisable', ctypes.c_uint32, 1),
        ('B2BReadDisable', ctypes.c_uint32, 1),
        ('Reserved10', ctypes.c_uint32, 6),
        ('MinTrackerStateService', ctypes.c_uint32, 3),
        ('MaxTrackerStateService', ctypes.c_uint32, 5),
        ('PowerGateDelay', ctypes.c_uint32, 2),
        ('DisplayReorderBufferDisable', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 3),
        ('DbufPowerState', ctypes.c_uint32, 1),
        ('DbufPowerRequest', ctypes.c_uint32, 1),
    ]


class REG_DBUF_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 3
    ErrorInjectionFlipBits = 0  # bit 4 to 5
    Reserved6 = 0  # bit 6 to 6
    EccErrorInjectionEnable = 0  # bit 7 to 7
    B2BWriteDisable = 0  # bit 8 to 8
    B2BReadDisable = 0  # bit 9 to 9
    Reserved10 = 0  # bit 10 to 15
    MinTrackerStateService = 0  # bit 16 to 18
    MaxTrackerStateService = 0  # bit 19 to 23
    PowerGateDelay = 0  # bit 24 to 25
    DisplayReorderBufferDisable = 0  # bit 26 to 26
    Reserved27 = 0  # bit 27 to 29
    DbufPowerState = 0  # bit 30 to 30
    DbufPowerRequest = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBUF_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBUF_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DBUF_STATUS:
    DBUF_STATUS_S2 = 0x44310
    DBUF_STATUS_S3 = 0x44314
    DBUF_STATUS_S1 = 0x44FEC
    DBUF_STATUS_S0 = 0x4500C

class _DBUF_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TrackersAvailable', ctypes.c_uint32, 16),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('Spare18', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 1),
        ('TrackerOverAllocated', ctypes.c_uint32, 1),
        ('Spare22', ctypes.c_uint32, 1),
        ('DrobTrackNumFifoOverrun', ctypes.c_uint32, 1),
        ('DrobRsvd3', ctypes.c_uint32, 1),
        ('DrobRsvd4', ctypes.c_uint32, 1),
        ('DrobRsvd5', ctypes.c_uint32, 1),
        ('DrobRsvd6', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 1),
        ('Spare29', ctypes.c_uint32, 1),
        ('DataoutFifoOverrun', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_DBUF_STATUS(ctypes.Union):
    value = 0
    offset = 0

    TrackersAvailable = 0  # bit 0 to 15
    Spare16 = 0  # bit 16 to 16
    Spare17 = 0  # bit 17 to 17
    Spare18 = 0  # bit 18 to 18
    Spare19 = 0  # bit 19 to 19
    Reserved20 = 0  # bit 20 to 20
    TrackerOverAllocated = 0  # bit 21 to 21
    Spare22 = 0  # bit 22 to 22
    DrobTrackNumFifoOverrun = 0  # bit 23 to 23
    DrobRsvd3 = 0  # bit 24 to 24
    DrobRsvd4 = 0  # bit 25 to 25
    DrobRsvd5 = 0  # bit 26 to 26
    DrobRsvd6 = 0  # bit 27 to 27
    Reserved28 = 0  # bit 28 to 28
    Spare29 = 0  # bit 29 to 29
    DataoutFifoOverrun = 0  # bit 30 to 30
    Spare31 = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBUF_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBUF_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DDR_TYPE(Enum):
    DDR_TYPE_LPDDR3 = 0x5
    DDR_TYPE_DDR3 = 0x4
    DDR_TYPE_LPDDR4 = 0x3
    DDR_TYPE_LPDDR5 = 0x2
    DDR_TYPE_DDR5 = 0x1
    DDR_TYPE_DDR4 = 0x0


class OFFSET_MEM_SS_INFO_GLOBAL:
    MEM_SS_INFO_GLOBAL = 0x45700

class _MEM_SS_INFO_GLOBAL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdrType', ctypes.c_uint32, 4),
        ('NumberOfPopulatedChannels', ctypes.c_uint32, 4),
        ('NumberOfEnabledQgvPoints', ctypes.c_uint32, 4),
        ('Reserved12', ctypes.c_uint32, 20),
    ]


class REG_MEM_SS_INFO_GLOBAL(ctypes.Union):
    value = 0
    offset = 0

    DdrType = 0  # bit 0 to 3
    NumberOfPopulatedChannels = 0  # bit 4 to 7
    NumberOfEnabledQgvPoints = 0  # bit 8 to 11
    Reserved12 = 0  # bit 12 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MEM_SS_INFO_GLOBAL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MEM_SS_INFO_GLOBAL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MEM_SS_INFO_QGV_POINT:
    MEM_SS_INFO_QGV_POINT_0 = 0x45710
    MEM_SS_INFO_QGV_POINT_1 = 0x45718
    MEM_SS_INFO_QGV_POINT_2 = 0x45720
    MEM_SS_INFO_QGV_POINT_3 = 0x45728
    MEM_SS_INFO_QGV_POINT_4 = 0x45730
    MEM_SS_INFO_QGV_POINT_5 = 0x45738
    MEM_SS_INFO_QGV_POINT_6 = 0x45740
    MEM_SS_INFO_QGV_POINT_7 = 0x45748

class _MEM_SS_INFO_QGV_POINT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DclkInMultiplesOf16_6666Mhz', ctypes.c_uint32, 16),
        ('TrpInDclks', ctypes.c_uint32, 8),
        ('TrcdInDclks', ctypes.c_uint32, 8),
        ('TrdpreInDclks', ctypes.c_uint32, 8),
        ('TrasInDclks', ctypes.c_uint32, 9),
        ('Reserved49', ctypes.c_uint32, 15),
    ]


class REG_MEM_SS_INFO_QGV_POINT(ctypes.Union):
    value = []
    offset = 0

    DclkInMultiplesOf16_6666Mhz = 0  # bit 0 to 15
    TrpInDclks = 0  # bit 16 to 23
    TrcdInDclks = 0  # bit 24 to 31
    TrdpreInDclks = 0  # bit 32 to 39
    TrasInDclks = 0  # bit 40 to 48
    Reserved49 = 0  # bit 49 to 63

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MEM_SS_INFO_QGV_POINT),
        ('value', ctypes.c_uint32 * 2)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MEM_SS_INFO_QGV_POINT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            for i, v in enumerate(value):
                self.value[i] = v


class ENUM_ACTIVE_PHYS(Enum):
    ACTIVE_PHYS_0_PHYS = 0x0
    ACTIVE_PHYS_1_PHYS = 0x1
    ACTIVE_PHYS_2_PHYS = 0x2
    ACTIVE_PHYS_3_PHYS = 0x3
    ACTIVE_PHYS_4_PHYS = 0x4
    ACTIVE_PHYS_5_PHYS = 0x5
    ACTIVE_PHYS_6_PHYS = 0x6
    ACTIVE_PHYS_7_OR_MORE_PHYS = 0x7


class ENUM_ACTIVE_DBUFS(Enum):
    ACTIVE_DBUFS_0_DBUFS = 0x0
    ACTIVE_DBUFS_1_DBUFS = 0x1
    ACTIVE_DBUFS_2_DBUFS = 0x2
    ACTIVE_DBUFS_3_OR_MORE_DBUFS = 0x3


class ENUM_ACTIVE_PIPES(Enum):
    ACTIVE_PIPES_0_PIPES = 0x0
    ACTIVE_PIPES_1_PIPES = 0x1
    ACTIVE_PIPES_2_PIPES = 0x2
    ACTIVE_PIPES_3_OR_MORE_PIPES = 0x3


class ENUM_VOLTAGE_LEVEL_INDEX(Enum):
    VOLTAGE_LEVEL_INDEX_INDEX_0 = 0x0
    VOLTAGE_LEVEL_INDEX_INDEX_1 = 0x1
    VOLTAGE_LEVEL_INDEX_INDEX_2 = 0x2
    VOLTAGE_LEVEL_INDEX_INDEX_3 = 0x3
    VOLTAGE_LEVEL_INDEX_INDEX_4 = 0x4
    VOLTAGE_LEVEL_INDEX_INDEX_5 = 0x5
    VOLTAGE_LEVEL_INDEX_INDEX_6 = 0x6
    VOLTAGE_LEVEL_INDEX_INDEX_7 = 0x7


class ENUM_ACTIVE_PLLS(Enum):
    ACTIVE_PLLS_0_PLLS = 0x0
    ACTIVE_PLLS_1_PLLS = 0x1
    ACTIVE_PLLS_2_PLLS = 0x2
    ACTIVE_PLLS_3_PLLS = 0x3
    ACTIVE_PLLS_4_PLLS = 0x4
    ACTIVE_PLLS_5_PLLS = 0x5
    ACTIVE_PLLS_6_PLLS = 0x6
    ACTIVE_PLLS_7_OR_MORE_PLLS = 0x7


class ENUM_ACTIVE_SCALARS(Enum):
    ACTIVE_SCALARS_0_SCALARS = 0x0
    ACTIVE_SCALARS_1_SCALARS = 0x1
    ACTIVE_SCALARS_2_SCALARS = 0x2
    ACTIVE_SCALARS_3_SCALARS = 0x3
    ACTIVE_SCALARS_4_SCALARS = 0x4
    ACTIVE_SCALARS_5_SCALARS = 0x5
    ACTIVE_SCALARS_6_SCALARS = 0x6
    ACTIVE_SCALARS_7_OR_MORE_SCALARS = 0x7


class ENUM_ENABLE(Enum):
    ENABLE_ENABLE = 0x0
    ENABLE_DISABLE = 0x1


class OFFSET_INITIATE_PM_DMD_REQ:
    INITIATE_PM_DMD_REQ = 0x45230

class _INITIATE_PM_DMD_REQ(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ActivePhys', ctypes.c_uint32, 3),
        ('Spare3Dword0', ctypes.c_uint32, 1),
        ('ActiveDbufs', ctypes.c_uint32, 2),
        ('ActivePipes', ctypes.c_uint32, 2),
        ('QclkGvIndex', ctypes.c_uint32, 4),
        ('VoltageLevelIndex', ctypes.c_uint32, 3),
        ('Spare15', ctypes.c_uint32, 1),
        ('BandwidthForQclkGv', ctypes.c_uint32, 16),
        ('ActivePlls', ctypes.c_uint32, 3),
        ('Spare3Dword1', ctypes.c_uint32, 1),
        ('ActiveScalars', ctypes.c_uint32, 3),
        ('Spare7', ctypes.c_uint32, 1),
        ('DdiclkFreq', ctypes.c_uint32, 11),
        ('Spare19', ctypes.c_uint32, 1),
        ('CdclkFreq', ctypes.c_uint32, 11),
        ('Enable', ctypes.c_uint32, 1),
    ]


class REG_INITIATE_PM_DMD_REQ(ctypes.Union):
    value = 0
    offset = 0

    ActivePhys = 0  # bit 0 to 2
    Spare3Dword0 = 0  # bit 3 to 3
    ActiveDbufs = 0  # bit 4 to 5
    ActivePipes = 0  # bit 6 to 7
    QclkGvIndex = 0  # bit 8 to 11
    VoltageLevelIndex = 0  # bit 12 to 14
    Spare15 = 0  # bit 15 to 15
    BandwidthForQclkGv = 0  # bit 16 to 31
    ActivePlls = 0  # bit 32 to 34
    Spare3Dword1 = 0  # bit 35 to 35
    ActiveScalars = 0  # bit 36 to 38
    Spare7 = 0  # bit 39 to 39
    DdiclkFreq = 0  # bit 40 to 50
    Spare19 = 0  # bit 51 to 51
    CdclkFreq = 0  # bit 52 to 62
    Enable = 0  # bit 63 to 63

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _INITIATE_PM_DMD_REQ),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_INITIATE_PM_DMD_REQ, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LATENCY_LP0_LP1:
    LATENCY_LP0_LP1 = 0x45780

class _LATENCY_LP0_LP1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LatencyLevel0', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('LatencyLevel1', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_LATENCY_LP0_LP1(ctypes.Union):
    value = 0
    offset = 0

    LatencyLevel0 = 0  # bit 0 to 12
    Reserved13 = 0  # bit 13 to 15
    LatencyLevel1 = 0  # bit 16 to 28
    Reserved29 = 0  # bit 29 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LATENCY_LP0_LP1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LATENCY_LP0_LP1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LATENCY_LP2_LP3:
    LATENCY_LP2_LP3 = 0x45784

class _LATENCY_LP2_LP3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LatencyLevel2', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('LatencyLevel3', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_LATENCY_LP2_LP3(ctypes.Union):
    value = 0
    offset = 0

    LatencyLevel2 = 0  # bit 0 to 12
    Reserved13 = 0  # bit 13 to 15
    LatencyLevel3 = 0  # bit 16 to 28
    Reserved29 = 0  # bit 29 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LATENCY_LP2_LP3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LATENCY_LP2_LP3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LATENCY_LP4_LP5:
    LATENCY_LP4_LP5 = 0x45788

class _LATENCY_LP4_LP5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LatencyLevel4', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('LatencyLevel5', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_LATENCY_LP4_LP5(ctypes.Union):
    value = 0
    offset = 0

    LatencyLevel4 = 0  # bit 0 to 12
    Reserved13 = 0  # bit 13 to 15
    LatencyLevel5 = 0  # bit 16 to 28
    Reserved29 = 0  # bit 29 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LATENCY_LP4_LP5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LATENCY_LP4_LP5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LATENCY_SAGV:
    LATENCY_SAGV = 0x4578C

class _LATENCY_SAGV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LatencyLevelQclkSagv', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_LATENCY_SAGV(ctypes.Union):
    value = 0
    offset = 0

    LatencyLevelQclkSagv = 0  # bit 0 to 12
    Reserved13 = 0  # bit 13 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LATENCY_SAGV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LATENCY_SAGV, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_UTIL_PIN_BUF_CTL:
    UTIL_PIN_BUF_CTL = 0x48404

class _UTIL_PIN_BUF_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PullupSlew', ctypes.c_uint32, 4),
        ('PullupStrength', ctypes.c_uint32, 5),
        ('Reserved9', ctypes.c_uint32, 3),
        ('PulldownSlew', ctypes.c_uint32, 4),
        ('PulldownStrength', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 3),
        ('Reserved24', ctypes.c_uint32, 3),
        ('Reserved27', ctypes.c_uint32, 1),
        ('Hysteresis', ctypes.c_uint32, 2),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_UTIL_PIN_BUF_CTL(ctypes.Union):
    value = 0
    offset = 0

    PullupSlew = 0  # bit 0 to 3
    PullupStrength = 0  # bit 4 to 8
    Reserved9 = 0  # bit 9 to 11
    PulldownSlew = 0  # bit 12 to 15
    PulldownStrength = 0  # bit 16 to 20
    Reserved21 = 0  # bit 21 to 23
    Reserved24 = 0  # bit 24 to 26
    Reserved27 = 0  # bit 27 to 27
    Hysteresis = 0  # bit 28 to 29
    Reserved30 = 0  # bit 30 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _UTIL_PIN_BUF_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_UTIL_PIN_BUF_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_UTIL2_PIN_BUF_CTL:
    UTIL2_PIN_BUF_CTL = 0x4840C

class _UTIL2_PIN_BUF_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PullupSlew', ctypes.c_uint32, 4),
        ('PullupStrength', ctypes.c_uint32, 5),
        ('Reserved9', ctypes.c_uint32, 3),
        ('PulldownSlew', ctypes.c_uint32, 4),
        ('PulldownStrength', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 3),
        ('Spare', ctypes.c_uint32, 3),
        ('Reserved27', ctypes.c_uint32, 1),
        ('Hysteresis', ctypes.c_uint32, 2),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_UTIL2_PIN_BUF_CTL(ctypes.Union):
    value = 0
    offset = 0

    PullupSlew = 0  # bit 0 to 3
    PullupStrength = 0  # bit 4 to 8
    Reserved9 = 0  # bit 9 to 11
    PulldownSlew = 0  # bit 12 to 15
    PulldownStrength = 0  # bit 16 to 20
    Reserved21 = 0  # bit 21 to 23
    Spare = 0  # bit 24 to 26
    Reserved27 = 0  # bit 27 to 27
    Hysteresis = 0  # bit 28 to 29
    Reserved30 = 0  # bit 30 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _UTIL2_PIN_BUF_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_UTIL2_PIN_BUF_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISPLAY_AUDIO_CODEC_DISABLE(Enum):
    DISPLAY_AUDIO_CODEC_ENABLE = 0x0  # Audio Codec Capability Enabled
    DISPLAY_AUDIO_CODEC_DISABLE = 0x1  # Audio Codec Capability Disabled


class ENUM_DISPLAY_HDCP_AKSV_READ_ENABLE(Enum):
    DISPLAY_HDCP_AKSV_READ_DISABLE = 0x0
    DISPLAY_HDCP_AKSV_READ_ENABLE = 0x1


class ENUM_DMC_MEM_ACCESS_DISABLE(Enum):
    DMC_MEM_ACCESS_ENABLE = 0x0
    DMC_MEM_ACCESS_DISABLE = 0x1


class ENUM_DMC_PICA_ACCESS_DISABLE(Enum):
    DMC_PICA_ACCESS_ENABLE = 0x0
    DMC_PICA_ACCESS_DISABLE = 0x1


class ENUM_DMC_PAVP_SR_DISABLE(Enum):
    DMC_PAVP_SR_ENABLE = 0x0
    DMC_PAVP_SR_DISABLE = 0x1


class ENUM_DISPLAY_RSB_DISABLE(Enum):
    DISPLAY_RSB_DISABLE = 0x1  # RSB Capability Disabled
    DISPLAY_RSB_ENABLE = 0x0  # RSB Capability Enabled


class ENUM_AUDIO_CODEC_ID(Enum):
    AUDIO_CODEC_ID_AUDIO_CODEC_ID_280BH = 0xB  # Default value is N/A. Fuse download will override with correct value f
                                               # or this project.


class ENUM_DFXCM_GREEN_ENABLE(Enum):
    DFXCM_GREEN_ENABLE = 0x1
    DFXCM_GREEN_DISABLE = 0x0


class ENUM_KVMR_SPRITE_DISABLE(Enum):
    KVMR_SPRITE_ENABLE = 0x0
    KVMR_SPRITE_DISABLE = 0x1


class ENUM_KVMR_CAPTURE_DISABLE(Enum):
    KVMR_CAPTURE_ENABLE = 0x0
    KVMR_CAPTURE_DISABLE = 0x1


class ENUM_DISPLAY_WD_DISABLE(Enum):
    DISPLAY_WD_ENABLE = 0x0  # WD Capability Enabled
    DISPLAY_WD_DISABLE = 0x1  # WD Capability Disabled


class ENUM_DISPLAY_PIPEB_DISABLE(Enum):
    DISPLAY_PIPEB_DISABLE_PIPE_B_CAPABILITY_ENABLED = 0x0
    DISPLAY_PIPEB_DISABLE_PIPE_B_CAPABILITY_DISABLED = 0x1


class ENUM_DISPLAY_PIPED_DISABLE(Enum):
    DISPLAY_PIPED_ENABLE = 0x0
    DISPLAY_PIPED_DISABLE = 0x1


class ENUM_DMC_DISABLE(Enum):
    DMC_ENABLE = 0x0
    DMC_DISABLE = 0x1


class ENUM_DISPLAY_HDCP_DISABLE(Enum):
    DISPLAY_HDCP_ENABLE = 0x0  # HDCP Capability Enabled
    DISPLAY_HDCP_DISABLE = 0x1  # HDCP Capability Disabled


class ENUM_DISPLAY_EDP_DISABLE(Enum):
    DISPLAY_EDP_ENABLE = 0x0  # eDP Capability Enabled
    DISPLAY_EDP_DISABLE = 0x1  # eDP Capability Disabled


class ENUM_DISPLAY_PIPEC_DISABLE(Enum):
    DISPLAY_PIPEC_ENABLE = 0x0  # Pipe C Capability Enabled
    DISPLAY_PIPEC_DISABLE = 0x1  # Pipe C Capability Disabled


class ENUM_DISPLAY_DEBUG_ENABLE(Enum):
    DISPLAY_DEBUG_DISABLE = 0x0  # Display Debug Disabled
    DISPLAY_DEBUG_ENABLE = 0x1  # Display Debug Enabled


class ENUM_DISPLAY_PIPEA_DISABLE(Enum):
    DISPLAY_PIPEA_ENABLE = 0x0  # Pipe A Capability Enabled
    DISPLAY_PIPEA_DISABLE = 0x1  # Pipe A Capability Disabled


class ENUM_DFX_POLICY6_DISABLE(Enum):
    DFX_POLICY6_ENABLE = 0x1
    DFX_POLICY6_DISABLE = 0x0


class OFFSET_DFSM:
    DFSM = 0x51000

class _DFSM(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayAudioCodecDisable', ctypes.c_uint32, 1),
        ('DisplayHdcpAksvReadEnable', ctypes.c_uint32, 1),
        ('DmcMemAccessDisable', ctypes.c_uint32, 1),
        ('Spare3', ctypes.c_uint32, 1),
        ('DmcPicaAccessDisable', ctypes.c_uint32, 1),
        ('DmcPavpSrDisable', ctypes.c_uint32, 1),
        ('DisplayRsbDisable', ctypes.c_uint32, 1),
        ('Spare7', ctypes.c_uint32, 1),
        ('AudioCodecId', ctypes.c_uint32, 8),
        ('Spare16', ctypes.c_uint32, 1),
        ('DfxcmGreenEnable', ctypes.c_uint32, 1),
        ('KvmrSpriteDisable', ctypes.c_uint32, 1),
        ('KvmrCaptureDisable', ctypes.c_uint32, 1),
        ('DisplayWdDisable', ctypes.c_uint32, 1),
        ('DisplayPipebDisable', ctypes.c_uint32, 1),
        ('DisplayPipedDisable', ctypes.c_uint32, 1),
        ('DmcDisable', ctypes.c_uint32, 1),
        ('Spare24', ctypes.c_uint32, 1),
        ('DisplayHdcpDisable', ctypes.c_uint32, 1),
        ('DisplayEdpDisable', ctypes.c_uint32, 1),
        ('Spare27', ctypes.c_uint32, 1),
        ('DisplayPipecDisable', ctypes.c_uint32, 1),
        ('DisplayDebugEnable', ctypes.c_uint32, 1),
        ('DisplayPipeaDisable', ctypes.c_uint32, 1),
        ('DfxPolicy6Disable', ctypes.c_uint32, 1),
    ]


class REG_DFSM(ctypes.Union):
    value = 0
    offset = 0

    DisplayAudioCodecDisable = 0  # bit 0 to 0
    DisplayHdcpAksvReadEnable = 0  # bit 1 to 1
    DmcMemAccessDisable = 0  # bit 2 to 2
    Spare3 = 0  # bit 3 to 3
    DmcPicaAccessDisable = 0  # bit 4 to 4
    DmcPavpSrDisable = 0  # bit 5 to 5
    DisplayRsbDisable = 0  # bit 6 to 6
    Spare7 = 0  # bit 7 to 7
    AudioCodecId = 0  # bit 8 to 15
    Spare16 = 0  # bit 16 to 16
    DfxcmGreenEnable = 0  # bit 17 to 17
    KvmrSpriteDisable = 0  # bit 18 to 18
    KvmrCaptureDisable = 0  # bit 19 to 19
    DisplayWdDisable = 0  # bit 20 to 20
    DisplayPipebDisable = 0  # bit 21 to 21
    DisplayPipedDisable = 0  # bit 22 to 22
    DmcDisable = 0  # bit 23 to 23
    Spare24 = 0  # bit 24 to 24
    DisplayHdcpDisable = 0  # bit 25 to 25
    DisplayEdpDisable = 0  # bit 26 to 26
    Spare27 = 0  # bit 27 to 27
    DisplayPipecDisable = 0  # bit 28 to 28
    DisplayDebugEnable = 0  # bit 29 to 29
    DisplayPipeaDisable = 0  # bit 30 to 30
    DfxPolicy6Disable = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DFSM),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DFSM, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MASK_LP_IDLE_IN_FILL_DONE(Enum):
    MASK_LP_IDLE_IN_FILL_DONE_MASK_IS_DISABLED = 0x0  # Both hp idle and lp idle will be considered in Fill done
    MASK_LP_IDLE_IN_FILL_DONE_MASK_IS_ENABLED = 0x1  # Only hp idle will be considered in Fill done.


class ENUM_COUNTER_COMPARE(Enum):
    COUNTER_COMPARE_COUNTER_11US = 0xB  # Value to compare 1Mhz counter which counts from Memup internal signal going l
                                        # ow to all inflight transactions completion.


class ENUM_OPEN_MIPI_DPHY_LATCHES(Enum):
    OPEN_MIPI_DPHY_LATCHES_DO_NOT_OVERRIDE_THE_DPHY_LATCHES = 0x0
    OPEN_MIPI_DPHY_LATCHES_OVERRIDE_THE_DPHY_LATCHES = 0x1


class OFFSET_CHICKEN_DCPR_2:
    CHICKEN_DCPR_2 = 0x46434

class _CHICKEN_DCPR_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MaskLpIdleInFillDone', ctypes.c_uint32, 1),
        ('CounterCompare', ctypes.c_uint32, 5),
        ('StickyForPhase1Counter', ctypes.c_uint32, 1),
        ('DisablePhase1Counter', ctypes.c_uint32, 1),
        ('StickyForPhase2Counter', ctypes.c_uint32, 1),
        ('DisablePhase2Counter', ctypes.c_uint32, 1),
        ('MasksNo_Lp_PendingInMemup', ctypes.c_uint32, 1),
        ('MaskNo_Lp_PendingInFill', ctypes.c_uint32, 1),
        ('IpcDemoteOverride', ctypes.c_uint32, 1),
        ('OpenMipiDphyLatches', ctypes.c_uint32, 1),
        ('DisablePmDmdRequests', ctypes.c_uint32, 1),
        ('BlockPmDmd', ctypes.c_uint32, 1),
        ('Dc5InProgress', ctypes.c_uint32, 1),
        ('DisableFusaErrorsPreventingDc6Entry', ctypes.c_uint32, 1),
        ('ForceAuxpowerreq', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('Spare20', ctypes.c_uint32, 1),
        ('Vbi_Enable_Dc6V', ctypes.c_uint32, 1),
        ('MaskDc5_Dc6_OkFromDsbsls', ctypes.c_uint32, 1),
        ('MaskDewakeFromDsbsls', ctypes.c_uint32, 1),
        ('DelayIsolationCounter', ctypes.c_uint32, 8),
    ]


class REG_CHICKEN_DCPR_2(ctypes.Union):
    value = 0
    offset = 0

    MaskLpIdleInFillDone = 0  # bit 0 to 0
    CounterCompare = 0  # bit 1 to 5
    StickyForPhase1Counter = 0  # bit 6 to 6
    DisablePhase1Counter = 0  # bit 7 to 7
    StickyForPhase2Counter = 0  # bit 8 to 8
    DisablePhase2Counter = 0  # bit 9 to 9
    MasksNo_Lp_PendingInMemup = 0  # bit 10 to 10
    MaskNo_Lp_PendingInFill = 0  # bit 11 to 11
    IpcDemoteOverride = 0  # bit 12 to 12
    OpenMipiDphyLatches = 0  # bit 13 to 13
    DisablePmDmdRequests = 0  # bit 14 to 14
    BlockPmDmd = 0  # bit 15 to 15
    Dc5InProgress = 0  # bit 16 to 16
    DisableFusaErrorsPreventingDc6Entry = 0  # bit 17 to 17
    ForceAuxpowerreq = 0  # bit 18 to 18
    Spare19 = 0  # bit 19 to 19
    Spare20 = 0  # bit 20 to 20
    Vbi_Enable_Dc6V = 0  # bit 21 to 21
    MaskDc5_Dc6_OkFromDsbsls = 0  # bit 22 to 22
    MaskDewakeFromDsbsls = 0  # bit 23 to 23
    DelayIsolationCounter = 0  # bit 24 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_DCPR_2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_DCPR_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ENABLE_IDLE_DETECTION_FOR_UC3_CLOCK(Enum):
    ENABLE_IDLE_DETECTION_FOR_UC3_CLOCK_DISABLE = 0x0
    ENABLE_IDLE_DETECTION_FOR_UC3_CLOCK_ENABLE = 0x1


class ENUM_ENABLE_IDLE_DETECTION_FOR_UC2_CLOCK(Enum):
    ENABLE_IDLE_DETECTION_FOR_UC2_CLOCK_DISABLE = 0x0
    ENABLE_IDLE_DETECTION_FOR_UC2_CLOCK_ENABLE = 0x1


class ENUM_ENABLE_IDLE_DETECTION_FOR_UC1_CLOCK(Enum):
    ENABLE_IDLE_DETECTION_FOR_UC1_CLOCK_DISABLE = 0x0
    ENABLE_IDLE_DETECTION_FOR_UC1_CLOCK_ENABLE = 0x1


class ENUM_ENABLE_IDLE_DETECTION_FOR_DDIB_CLOCK(Enum):
    ENABLE_IDLE_DETECTION_FOR_DDIB_CLOCK_DISABLE = 0x0
    ENABLE_IDLE_DETECTION_FOR_DDIB_CLOCK_ENABLE = 0x1


class ENUM_ENABLE_IDLE_DETECTION_FOR_DDIA_CLOCK(Enum):
    ENABLE_IDLE_DETECTION_FOR_DDIA_CLOCK_DISABLE = 0x0
    ENABLE_IDLE_DETECTION_FOR_DDIA_CLOCK_ENABLE = 0x1


class ENUM_CD_ON_UC4_CLOCK_ENABLE(Enum):
    CD_ON_UC4_CLOCK_DISABLE = 0x0
    CD_ON_UC4_CLOCK_ENABLE = 0x1


class ENUM_CD_ON_UC3_CLOCK_ENABLE(Enum):
    CD_ON_UC3_CLOCK_DISABLE = 0x0
    CD_ON_UC3_CLOCK_ENABLE = 0x1


class ENUM_CD_ON_UC2_CLOCK_ENABLE(Enum):
    CD_ON_UC2_CLOCK_DISABLE = 0x0
    CD_ON_UC2_CLOCK_ENABLE = 0x1


class ENUM_CD_ON_UC1_CLOCK_ENABLE(Enum):
    CD_ON_UC1_CLOCK_DISABLE = 0x0
    CD_ON_UC1_CLOCK_ENABLE = 0x1


class ENUM_ENABLE_IDLE_DETECTION_FOR_UC4_CLOCK(Enum):
    ENABLE_IDLE_DETECTION_FOR_UC4_CLOCK_DISABLE = 0x0
    ENABLE_IDLE_DETECTION_FOR_UC4_CLOCK_ENABLE = 0x1


class ENUM_CD_ON_DDIB_CLOCK_ENABLE(Enum):
    CD_ON_DDIB_CLOCK_DISABLE = 0x0
    CD_ON_DDIB_CLOCK_ENABLE = 0x1


class ENUM_CD_ON_DDIA_CLOCK_ENABLE(Enum):
    CD_ON_DDIA_CLOCK_DISABLE = 0x0
    CD_ON_DDIA_CLOCK_ENABLE = 0x1


class OFFSET_CHICKEN_DCPR_3:
    CHICKEN_DCPR_3 = 0x46438

class _CHICKEN_DCPR_3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EnableIdleDetectionForUc3Clock', ctypes.c_uint32, 1),
        ('EnableIdleDetectionForUc2Clock', ctypes.c_uint32, 1),
        ('SkipWaitOnCdpllUnlock', ctypes.c_uint32, 1),
        ('EnableIdleDetectionForUc1Clock', ctypes.c_uint32, 1),
        ('EnableIdleDetectionForDdibClock', ctypes.c_uint32, 1),
        ('EnableIdleDetectionForDdiaClock', ctypes.c_uint32, 1),
        ('CdOnPortclk', ctypes.c_uint32, 1),
        ('SkipPfetAck', ctypes.c_uint32, 1),
        ('Spare8', ctypes.c_uint32, 1),
        ('SkipWaitOnD2DLinkDisableAck', ctypes.c_uint32, 1),
        ('SkipEbbAck', ctypes.c_uint32, 1),
        ('ForceVdcoreOn', ctypes.c_uint32, 1),
        ('ForceVdcoreOff', ctypes.c_uint32, 1),
        ('ForceVdtgOn', ctypes.c_uint32, 1),
        ('ForceVdtgOff', ctypes.c_uint32, 1),
        ('ForceVdretOn', ctypes.c_uint32, 1),
        ('ForceVdretOff', ctypes.c_uint32, 1),
        ('SetDewake', ctypes.c_uint32, 1),
        ('ResetDewake', ctypes.c_uint32, 1),
        ('DmdRspTimeoutDisable', ctypes.c_uint32, 1),
        ('SagvTimeoutDisable', ctypes.c_uint32, 1),
        ('BlockPmReqNackDisable', ctypes.c_uint32, 1),
        ('Dc5ExitBlockReq', ctypes.c_uint32, 1),
        ('CdOnUc4ClockEnable', ctypes.c_uint32, 1),
        ('CdOnUc3ClockEnable', ctypes.c_uint32, 1),
        ('CdOnUc2ClockEnable', ctypes.c_uint32, 1),
        ('CdOnUc1ClockEnable', ctypes.c_uint32, 1),
        ('EnableIdleDetectionForUc4Clock', ctypes.c_uint32, 1),
        ('Spare28', ctypes.c_uint32, 1),
        ('Spare29', ctypes.c_uint32, 1),
        ('CdOnDdibClockEnable', ctypes.c_uint32, 1),
        ('CdOnDdiaClockEnable', ctypes.c_uint32, 1),
    ]


class REG_CHICKEN_DCPR_3(ctypes.Union):
    value = 0
    offset = 0

    EnableIdleDetectionForUc3Clock = 0  # bit 0 to 0
    EnableIdleDetectionForUc2Clock = 0  # bit 1 to 1
    SkipWaitOnCdpllUnlock = 0  # bit 2 to 2
    EnableIdleDetectionForUc1Clock = 0  # bit 3 to 3
    EnableIdleDetectionForDdibClock = 0  # bit 4 to 4
    EnableIdleDetectionForDdiaClock = 0  # bit 5 to 5
    CdOnPortclk = 0  # bit 6 to 6
    SkipPfetAck = 0  # bit 7 to 7
    Spare8 = 0  # bit 8 to 8
    SkipWaitOnD2DLinkDisableAck = 0  # bit 9 to 9
    SkipEbbAck = 0  # bit 10 to 10
    ForceVdcoreOn = 0  # bit 11 to 11
    ForceVdcoreOff = 0  # bit 12 to 12
    ForceVdtgOn = 0  # bit 13 to 13
    ForceVdtgOff = 0  # bit 14 to 14
    ForceVdretOn = 0  # bit 15 to 15
    ForceVdretOff = 0  # bit 16 to 16
    SetDewake = 0  # bit 17 to 17
    ResetDewake = 0  # bit 18 to 18
    DmdRspTimeoutDisable = 0  # bit 19 to 19
    SagvTimeoutDisable = 0  # bit 20 to 20
    BlockPmReqNackDisable = 0  # bit 21 to 21
    Dc5ExitBlockReq = 0  # bit 22 to 22
    CdOnUc4ClockEnable = 0  # bit 23 to 23
    CdOnUc3ClockEnable = 0  # bit 24 to 24
    CdOnUc2ClockEnable = 0  # bit 25 to 25
    CdOnUc1ClockEnable = 0  # bit 26 to 26
    EnableIdleDetectionForUc4Clock = 0  # bit 27 to 27
    Spare28 = 0  # bit 28 to 28
    Spare29 = 0  # bit 29 to 29
    CdOnDdibClockEnable = 0  # bit 30 to 30
    CdOnDdiaClockEnable = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_DCPR_3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_DCPR_3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_REGULATE_B2B_TRANSACTIONS(Enum):
    REGULATE_B2B_TRANSACTIONS_DISABLE = 0x0
    REGULATE_B2B_TRANSACTIONS_ENABLE = 0x1


class ENUM_STATUS(Enum):
    STATUS_DISABLED = 0x0
    STATUS_ENABLED = 0x1


class OFFSET_MBUS_ABOX_CTL:
    MBUS_ABOX_CTL0 = 0x45038
    MBUS_ABOX_CTL1 = 0x45048

class _MBUS_ABOX_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BtCreditsPool1', ctypes.c_uint32, 5),
        ('B2BTransactionsDelay', ctypes.c_uint32, 3),
        ('BtCreditsPool2', ctypes.c_uint32, 5),
        ('RegulateB2BTransactions', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 2),
        ('BCredits', ctypes.c_uint32, 4),
        ('BwCredits', ctypes.c_uint32, 2),
        ('B2BTransactionsMax', ctypes.c_uint32, 5),
        ('RingStopAddress', ctypes.c_uint32, 4),
        ('Status', ctypes.c_uint32, 1),
    ]


class REG_MBUS_ABOX_CTL(ctypes.Union):
    value = 0
    offset = 0

    BtCreditsPool1 = 0  # bit 0 to 4
    B2BTransactionsDelay = 0  # bit 5 to 7
    BtCreditsPool2 = 0  # bit 8 to 12
    RegulateB2BTransactions = 0  # bit 13 to 13
    Reserved14 = 0  # bit 14 to 15
    BCredits = 0  # bit 16 to 19
    BwCredits = 0  # bit 20 to 21
    B2BTransactionsMax = 0  # bit 22 to 26
    RingStopAddress = 0  # bit 27 to 30
    Status = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MBUS_ABOX_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MBUS_ABOX_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MBUS_BBOX_CTL:
    MBUS_BBOX_CTL_S2 = 0x44390
    MBUS_BBOX_CTL_S3 = 0x44394
    MBUS_BBOX_CTL_S0 = 0x45040
    MBUS_BBOX_CTL_S1 = 0x45044

class _MBUS_BBOX_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 16),
        ('RegulateB2BTransactions', ctypes.c_uint32, 1),
        ('B2BTransactionsDelay', ctypes.c_uint32, 3),
        ('B2BTransactionsMax', ctypes.c_uint32, 5),
        ('Reserved25', ctypes.c_uint32, 2),
        ('RingStopAddress', ctypes.c_uint32, 4),
        ('Status', ctypes.c_uint32, 1),
    ]


class REG_MBUS_BBOX_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 15
    RegulateB2BTransactions = 0  # bit 16 to 16
    B2BTransactionsDelay = 0  # bit 17 to 19
    B2BTransactionsMax = 0  # bit 20 to 24
    Reserved25 = 0  # bit 25 to 26
    RingStopAddress = 0  # bit 27 to 30
    Status = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MBUS_BBOX_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MBUS_BBOX_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ALLOW_B2B_APUT(Enum):
    ALLOW_B2B_APUT_ALLOW_B2B_APUTS = 0x0
    ALLOW_B2B_APUT_BLOCK_B2B_APUTS = 0x1


class ENUM_MBUS_JOINING_PIPE_SELECT(Enum):
    MBUS_JOINING_PIPE_SELECT_PIPE_A = 0x0
    MBUS_JOINING_PIPE_SELECT_PIPE_B = 0x1
    MBUS_JOINING_PIPE_SELECT_PIPE_C = 0x2
    MBUS_JOINING_PIPE_SELECT_PIPE_D = 0x3
    MBUS_JOINING_PIPE_SELECT_NONE = 0x7  # Double buffer enable is tied to 1 so that writes to the MBus joining and Has
                                         # hing Mode bit fields will take effect immediately.


class ENUM_HASHING_MODE(Enum):
    HASHING_MODE_2X2_HASHING = 0x0
    HASHING_MODE_1X4_HASHING = 0x1


class ENUM_MBUS_JOINING(Enum):
    MBUS_JOINING_DISABLED = 0x0
    MBUS_JOINING_ENABLED = 0x1


class OFFSET_MBUS_CTL:
    MBUS_CTL = 0x4438C

class _MBUS_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Mbus2CringPacketDrop', ctypes.c_uint32, 1),
        ('Mbus1CringPacketDrop', ctypes.c_uint32, 1),
        ('Mbus2DringPacketDrop', ctypes.c_uint32, 1),
        ('Mbus1DringPacketDrop', ctypes.c_uint32, 1),
        ('Mbus2CringPacketErrorStatus', ctypes.c_uint32, 1),
        ('Mbus1CringPacketErrorStatus', ctypes.c_uint32, 1),
        ('Mbus2DringPacketErrorStatus', ctypes.c_uint32, 1),
        ('Mbus1DringPacketErrorStatus', ctypes.c_uint32, 1),
        ('TranslationThrottleMax', ctypes.c_uint32, 4),
        ('AllowB2BAput', ctypes.c_uint32, 1),
        ('TranslationThrottleMin', ctypes.c_uint32, 3),
        ('TranslationTypeThrottleSelect', ctypes.c_uint32, 1),
        ('TranslationTypeThrottleValue', ctypes.c_uint32, 3),
        ('Reserved20', ctypes.c_uint32, 6),
        ('MbusJoiningPipeSelect', ctypes.c_uint32, 3),
        ('Reserved29', ctypes.c_uint32, 1),
        ('HashingMode', ctypes.c_uint32, 1),
        ('MbusJoining', ctypes.c_uint32, 1),
    ]


class REG_MBUS_CTL(ctypes.Union):
    value = 0
    offset = 0

    Mbus2CringPacketDrop = 0  # bit 0 to 0
    Mbus1CringPacketDrop = 0  # bit 1 to 1
    Mbus2DringPacketDrop = 0  # bit 2 to 2
    Mbus1DringPacketDrop = 0  # bit 3 to 3
    Mbus2CringPacketErrorStatus = 0  # bit 4 to 4
    Mbus1CringPacketErrorStatus = 0  # bit 5 to 5
    Mbus2DringPacketErrorStatus = 0  # bit 6 to 6
    Mbus1DringPacketErrorStatus = 0  # bit 7 to 7
    TranslationThrottleMax = 0  # bit 8 to 11
    AllowB2BAput = 0  # bit 12 to 12
    TranslationThrottleMin = 0  # bit 13 to 15
    TranslationTypeThrottleSelect = 0  # bit 16 to 16
    TranslationTypeThrottleValue = 0  # bit 17 to 19
    Reserved20 = 0  # bit 20 to 25
    MbusJoiningPipeSelect = 0  # bit 26 to 28
    Reserved29 = 0  # bit 29 to 29
    HashingMode = 0  # bit 30 to 30
    MbusJoining = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MBUS_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MBUS_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_BW_PERFORMANCE_COUNTERS_ENABLE(Enum):
    BW_PERFORMANCE_COUNTERS_DISABLED = 0x0
    BW_PERFORMANCE_COUNTERS_ENABLED = 0x1


class ENUM_TLB_REQUEST_TIMER(Enum):
    TLB_REQUEST_TIMER_8 = 0x8


class ENUM_PLANE_REQUEST_TIMER(Enum):
    PLANE_REQUEST_TIMER_16 = 0x10


class ENUM_BW_GLOBAL_COUNTER_CLEAR(Enum):
    BW_GLOBAL_COUNTER_CLEAR_CLEAR = 0x1
    BW_GLOBAL_COUNTER_CLEAR_DO_NOT_CLEAR = 0x0


class ENUM_BW_BUDDY_DISABLE(Enum):
    BW_BUDDY_ENABLED = 0x0
    BW_BUDDY_DISABLED = 0x1


class OFFSET_BW_BUDDY_CTL:
    BW_BUDDY_CTL0 = 0x45130
    BW_BUDDY_CTL1 = 0x45140

class _BW_BUDDY_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 15),
        ('BwPerformanceCountersEnable', ctypes.c_uint32, 1),
        ('TlbRequestTimer', ctypes.c_uint32, 6),
        ('Reserved22', ctypes.c_uint32, 1),
        ('PlaneRequestTimer', ctypes.c_uint32, 6),
        ('Reserved29', ctypes.c_uint32, 1),
        ('BwGlobalCounterClear', ctypes.c_uint32, 1),
        ('BwBuddyDisable', ctypes.c_uint32, 1),
    ]


class REG_BW_BUDDY_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 14
    BwPerformanceCountersEnable = 0  # bit 15 to 15
    TlbRequestTimer = 0  # bit 16 to 21
    Reserved22 = 0  # bit 22 to 22
    PlaneRequestTimer = 0  # bit 23 to 28
    Reserved29 = 0  # bit 29 to 29
    BwGlobalCounterClear = 0  # bit 30 to 30
    BwBuddyDisable = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _BW_BUDDY_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_BW_BUDDY_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_BW_BUDDY_PAGE_MASK(Enum):
    BW_BUDDY_PAGE_MASK_ALL_ADDRESS_BITS_ARE_NOT_MASKED = 0x0


class OFFSET_BW_BUDDY_PAGE_MASK:
    BW_BUDDY_PAGE_MASK0 = 0x45134
    BW_BUDDY_PAGE_MASK1 = 0x45144

class _BW_BUDDY_PAGE_MASK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BwBuddyPageMask', ctypes.c_uint32, 32),
    ]


class REG_BW_BUDDY_PAGE_MASK(ctypes.Union):
    value = 0
    offset = 0

    BwBuddyPageMask = 0  # bit 0 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _BW_BUDDY_PAGE_MASK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_BW_BUDDY_PAGE_MASK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DISPLAY_ERR_FATAL_MASK:
    DISPLAY_ERR_FATAL_MASK = 0x4421C

class _DISPLAY_ERR_FATAL_MASK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ErrorMask', ctypes.c_uint32, 32),
    ]


class REG_DISPLAY_ERR_FATAL_MASK(ctypes.Union):
    value = 0
    offset = 0

    ErrorMask = 0  # bit 0 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DISPLAY_ERR_FATAL_MASK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DISPLAY_ERR_FATAL_MASK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DCPR_STATUS_1:
    DCPR_STATUS_1 = 0x46440

class _DCPR_STATUS_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 26),
        ('PmDmdInflightStatus', ctypes.c_uint32, 1),
        ('StickyPipeDIpcDemoteStatus', ctypes.c_uint32, 1),
        ('StickyPipeCIpcDemoteStatus', ctypes.c_uint32, 1),
        ('StickyPipeBIpcDemoteStatus', ctypes.c_uint32, 1),
        ('StickyPipeAIpcDemoteStatus', ctypes.c_uint32, 1),
        ('IpcDemoteLiveStatus', ctypes.c_uint32, 1),
    ]


class REG_DCPR_STATUS_1(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 25
    PmDmdInflightStatus = 0  # bit 26 to 26
    StickyPipeDIpcDemoteStatus = 0  # bit 27 to 27
    StickyPipeCIpcDemoteStatus = 0  # bit 28 to 28
    StickyPipeBIpcDemoteStatus = 0  # bit 29 to 29
    StickyPipeAIpcDemoteStatus = 0  # bit 30 to 30
    IpcDemoteLiveStatus = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DCPR_STATUS_1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DCPR_STATUS_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CLKGATE_DIS_3:
    CLKGATE_DIS_3 = 0x46538

class _CLKGATE_DIS_3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('DbregGatingDis', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 23),
        ('DrposGatingDis', ctypes.c_uint32, 1),
        ('DrpoGatingDis', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 2),
        ('DpioGatingDis', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_CLKGATE_DIS_3(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 0
    DbregGatingDis = 0  # bit 1 to 1
    Reserved2 = 0  # bit 2 to 24
    DrposGatingDis = 0  # bit 25 to 25
    DrpoGatingDis = 0  # bit 26 to 26
    Reserved27 = 0  # bit 27 to 28
    DpioGatingDis = 0  # bit 29 to 29
    Reserved30 = 0  # bit 30 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CLKGATE_DIS_3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CLKGATE_DIS_3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CLKGATE_DIS_4:
    CLKGATE_DIS_4 = 0x4653C

class _CLKGATE_DIS_4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 3),
        ('UltraJoinerGatingDis', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 13),
        ('DmapGatingDis', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 2),
        ('Reserved20', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 4),
        ('DprGatingDis', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 3),
        ('DpfdGatingDis', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_CLKGATE_DIS_4(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 2
    UltraJoinerGatingDis = 0  # bit 3 to 3
    Reserved4 = 0  # bit 4 to 16
    DmapGatingDis = 0  # bit 17 to 17
    Reserved18 = 0  # bit 18 to 19
    Reserved20 = 0  # bit 20 to 20
    Reserved21 = 0  # bit 21 to 24
    DprGatingDis = 0  # bit 25 to 25
    Reserved26 = 0  # bit 26 to 28
    DpfdGatingDis = 0  # bit 29 to 29
    Reserved30 = 0  # bit 30 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CLKGATE_DIS_4),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CLKGATE_DIS_4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CLKGATE_DIS_5:
    CLKGATE_DIS_5 = 0x46540

class _CLKGATE_DIS_5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 14),
        ('DksGatingDis', ctypes.c_uint32, 1),
        ('DkGatingDis', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 1),
        ('DpceGatingDis', ctypes.c_uint32, 1),
        ('DkvmrGatingDis', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 2),
        ('DacfpGatingDis', ctypes.c_uint32, 1),
        ('DacrgGatingDis', ctypes.c_uint32, 1),
        ('VrdGatingDis', ctypes.c_uint32, 1),
        ('DacfeGatingDis', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 2),
        ('DkdbGatingDis', ctypes.c_uint32, 1),
        ('DwdciphGatingDis', ctypes.c_uint32, 1),
        ('DwdsGatingDis', ctypes.c_uint32, 1),
        ('DwdcGatingDis', ctypes.c_uint32, 1),
        ('DrwdGatingDis', ctypes.c_uint32, 1),
    ]


class REG_CLKGATE_DIS_5(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 13
    DksGatingDis = 0  # bit 14 to 14
    DkGatingDis = 0  # bit 15 to 15
    Reserved16 = 0  # bit 16 to 16
    DpceGatingDis = 0  # bit 17 to 17
    DkvmrGatingDis = 0  # bit 18 to 18
    Reserved19 = 0  # bit 19 to 20
    DacfpGatingDis = 0  # bit 21 to 21
    DacrgGatingDis = 0  # bit 22 to 22
    VrdGatingDis = 0  # bit 23 to 23
    DacfeGatingDis = 0  # bit 24 to 24
    Reserved25 = 0  # bit 25 to 26
    DkdbGatingDis = 0  # bit 27 to 27
    DwdciphGatingDis = 0  # bit 28 to 28
    DwdsGatingDis = 0  # bit 29 to 29
    DwdcGatingDis = 0  # bit 30 to 30
    DrwdGatingDis = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CLKGATE_DIS_5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CLKGATE_DIS_5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

