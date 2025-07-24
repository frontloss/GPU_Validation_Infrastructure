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
# @file Gen11p5AuxRegs.py
# @brief contains Gen11p5AuxRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_SYNC_PULSE_COUNT(Enum):
    SYNC_PULSE_COUNT_32_PULSES = 0x1F


class ENUM_FAST_WAKE_SYNC_PULSE_COUNT(Enum):
    FAST_WAKE_SYNC_PULSE_COUNT_18_PULSES = 0x11


class ENUM_IO_SELECT(Enum):
    IO_SELECT_TBT = 0x1  # Use Thunderbolt IO
    IO_SELECT_LEGACY = 0x0  # Use legacy IO. Either typeC or regular DDI, depending on project and SKU


class ENUM_AUX_GTC_DATA_SELECT(Enum):
    AUX_GTC_DATA_SELECT_AUX = 0x1  # Use AUX Data registers for GTC
    AUX_GTC_DATA_SELECT_HARDCODED = 0x0  # Use hardcoded data value for GTC.


class ENUM_AUX_FRAME_SYNC_DATA_SELECT(Enum):
    AUX_FRAME_SYNC_DATA_SELECT_AUX = 0x1  # Use AUX Data registers for frame sync
    AUX_FRAME_SYNC_DATA_SELECT_HARDCODED = 0x0  # Use hardcoded data value for frame sync.


class ENUM_AUX_PSR_DATA_SELECT(Enum):
    AUX_PSR_DATA_SELECT_AUX = 0x1  # Use AUX Data registers for PSR
    AUX_PSR_DATA_SELECT_HARDCODED = 0x0  # Use hardcoded data value for PSR.


class ENUM_AUX_AKSV_SELECT(Enum):
    AUX_AKSV_SELECT_AUX = 0x0  # Use AUX Data registers for regular data transmission
    AUX_AKSV_SELECT_HDCP = 0x1  # Use HDCP internal Aksv for part of the data transmission.


class ENUM_RECEIVE_ERROR(Enum):
    RECEIVE_ERROR_NOT_ERROR = 0x0
    RECEIVE_ERROR_ERROR = 0x1


class ENUM_TIME_OUT_TIMER_VALUE(Enum):
    TIME_OUT_TIMER_VALUE_400US = 0x0
    TIME_OUT_TIMER_VALUE_600US = 0x1
    TIME_OUT_TIMER_VALUE_800US = 0x2
    TIME_OUT_TIMER_VALUE_4000US = 0x3


class ENUM_TIME_OUT_ERROR(Enum):
    TIME_OUT_ERROR_NOT_ERROR = 0x0
    TIME_OUT_ERROR_ERROR = 0x1


class ENUM_INTERRUPT_ON_DONE(Enum):
    INTERRUPT_ON_DONE_DISABLE = 0x0
    INTERRUPT_ON_DONE_ENABLE = 0x1


class ENUM_DONE(Enum):
    DONE_NOT_DONE = 0x0
    DONE_DONE = 0x1


class OFFSET_DDI_AUX_CTL:
    DDI_AUX_CTL_A = 0x64010
    DDI_AUX_CTL_B = 0x64110
    DDI_AUX_CTL_C = 0x64210
    DDI_AUX_CTL_USBC1 = 0x64310
    DDI_AUX_CTL_USBC2 = 0x64410
    DDI_AUX_CTL_USBC3 = 0x64510
    DDI_AUX_CTL_USBC4 = 0x64610
    DDI_AUX_CTL_USBC5 = 0x64710
    DDI_AUX_CTL_USBC6 = 0x64810


class _DDI_AUX_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SyncPulseCount', ctypes.c_uint32, 5),
        ('FastWakeSyncPulseCount', ctypes.c_uint32, 5),
        ('Reserved10', ctypes.c_uint32, 1),
        ('IoSelect', ctypes.c_uint32, 1),
        ('AuxGtcDataSelect', ctypes.c_uint32, 1),
        ('AuxFrameSyncDataSelect', ctypes.c_uint32, 1),
        ('AuxPsrDataSelect', ctypes.c_uint32, 1),
        ('AuxAksvSelect', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 4),
        ('MessageSize', ctypes.c_uint32, 5),
        ('ReceiveError', ctypes.c_uint32, 1),
        ('TimeOutTimerValue', ctypes.c_uint32, 2),
        ('TimeOutError', ctypes.c_uint32, 1),
        ('InterruptOnDone', ctypes.c_uint32, 1),
        ('Done', ctypes.c_uint32, 1),
        ('SendBusy', ctypes.c_uint32, 1),
    ]


class REG_DDI_AUX_CTL(ctypes.Union):
    value = 0
    offset = 0

    SyncPulseCount = 0  # bit 0 to 5
    FastWakeSyncPulseCount = 0  # bit 5 to 10
    Reserved10 = 0  # bit 10 to 11
    IoSelect = 0  # bit 11 to 12
    AuxGtcDataSelect = 0  # bit 12 to 13
    AuxFrameSyncDataSelect = 0  # bit 13 to 14
    AuxPsrDataSelect = 0  # bit 14 to 15
    AuxAksvSelect = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 20
    MessageSize = 0  # bit 20 to 25
    ReceiveError = 0  # bit 25 to 26
    TimeOutTimerValue = 0  # bit 26 to 28
    TimeOutError = 0  # bit 28 to 29
    InterruptOnDone = 0  # bit 29 to 30
    Done = 0  # bit 30 to 31
    SendBusy = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_AUX_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_AUX_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DDI_AUX_DATA:
    DDI_AUX_DATA_0_A = 0x64014
    DDI_AUX_DATA_1_A = 0x64018
    DDI_AUX_DATA_2_A = 0x6401C
    DDI_AUX_DATA_3_A = 0x64020
    DDI_AUX_DATA_4_A = 0x64024
    DDI_AUX_DATA_0_B = 0x64114
    DDI_AUX_DATA_1_B = 0x64118
    DDI_AUX_DATA_2_B = 0x6411C
    DDI_AUX_DATA_3_B = 0x64120
    DDI_AUX_DATA_4_B = 0x64124
    DDI_AUX_DATA_0_C = 0x64214
    DDI_AUX_DATA_1_C = 0x64218
    DDI_AUX_DATA_2_C = 0x6421C
    DDI_AUX_DATA_3_C = 0x64220
    DDI_AUX_DATA_4_C = 0x64224
    DDI_AUX_DATA_0_USBC1 = 0x64314
    DDI_AUX_DATA_1_USBC1 = 0x64318
    DDI_AUX_DATA_2_USBC1 = 0x6431C
    DDI_AUX_DATA_3_USBC1 = 0x64320
    DDI_AUX_DATA_4_USBC1 = 0x64324
    DDI_AUX_DATA_0_USBC2 = 0x64414
    DDI_AUX_DATA_1_USBC2 = 0x64418
    DDI_AUX_DATA_2_USBC2 = 0x6441C
    DDI_AUX_DATA_3_USBC2 = 0x64420
    DDI_AUX_DATA_4_USBC2 = 0x64424
    DDI_AUX_DATA_0_USBC3 = 0x64514
    DDI_AUX_DATA_1_USBC3 = 0x64518
    DDI_AUX_DATA_2_USBC3 = 0x6451C
    DDI_AUX_DATA_3_USBC3 = 0x64520
    DDI_AUX_DATA_4_USBC3 = 0x64524
    DDI_AUX_DATA_0_USBC4 = 0x64614
    DDI_AUX_DATA_1_USBC4 = 0x64618
    DDI_AUX_DATA_2_USBC4 = 0x6461C
    DDI_AUX_DATA_3_USBC4 = 0x64620
    DDI_AUX_DATA_4_USBC4 = 0x64624
    DDI_AUX_DATA_0_USBC5 = 0x64714
    DDI_AUX_DATA_1_USBC5 = 0x64718
    DDI_AUX_DATA_2_USBC5 = 0x6471C
    DDI_AUX_DATA_3_USBC5 = 0x64720
    DDI_AUX_DATA_4_USBC5 = 0x64724
    DDI_AUX_DATA_0_USBC6 = 0x64814
    DDI_AUX_DATA_1_USBC6 = 0x64818
    DDI_AUX_DATA_2_USBC6 = 0x6481C
    DDI_AUX_DATA_3_USBC6 = 0x64820
    DDI_AUX_DATA_4_USBC6 = 0x64824


class _DDI_AUX_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AuxChData', ctypes.c_uint32, 32),
    ]


class REG_DDI_AUX_DATA(ctypes.Union):
    value = 0
    offset = 0

    AuxChData = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_AUX_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_AUX_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

