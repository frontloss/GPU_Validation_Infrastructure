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
# @file Gen15DdiRegs.py
# @brief contains Gen15DdiRegs.py related register definitions

import ctypes
from enum import Enum


class OFFSET_TCSS_DDI_STATUS:
    TCSS_DDI_STATUS_1 = 0x161500
    TCSS_DDI_STATUS_2 = 0x161504
    TCSS_DDI_STATUS_3 = 0x161508
    TCSS_DDI_STATUS_4 = 0x16150C

class _TCSS_DDI_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hpd_Live_Status_Alt', ctypes.c_uint32, 1),
        ('Hpd_Live_Status_Tbt', ctypes.c_uint32, 1),
        ('Ready', ctypes.c_uint32, 1),
        ('Sss', ctypes.c_uint32, 1),
        ('Src_Port_Num', ctypes.c_uint32, 4),
        ('Hpd_In_Progress', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 23),
    ]


class REG_TCSS_DDI_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Hpd_Live_Status_Alt = 0  # bit 0 to 0
    Hpd_Live_Status_Tbt = 0  # bit 1 to 1
    Ready = 0  # bit 2 to 2
    Sss = 0  # bit 3 to 3
    Src_Port_Num = 0  # bit 4 to 7
    Hpd_In_Progress = 0  # bit 8 to 8
    Reserved9 = 0  # bit 9 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TCSS_DDI_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TCSS_DDI_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PORT_WIDTH(Enum):
    PORT_WIDTH_X1 = 0x0
    PORT_WIDTH_X2 = 0x1
    PORT_WIDTH_X4 = 0x3
    PORT_WIDTH_X3 = 0x4


class ENUM_BYPASS_IDLE_STATUS(Enum):
    BYPASS_IDLE_STATUS_DO_NOT_BYPASS = 0x0
    BYPASS_IDLE_STATUS_BYPASS = 0x1


class ENUM_IDLE_STATUS(Enum):
    IDLE_STATUS_NOT_IDLE = 0x0
    IDLE_STATUS_IDLE = 0x1


class ENUM_PORT_REVERSAL(Enum):
    PORT_REVERSAL_NOT_REVERSED = 0x0
    PORT_REVERSAL_REVERSED = 0x1


class ENUM_DATA_WIDTH(Enum):
    DATA_WIDTH_10BIT = 0x0  # This value is used for eDP 1.x, DP 1.x, DP 2.0 with 8b/10b.
    DATA_WIDTH_20BIT = 0x1  # This value is used for HDMI 2.1 Fixed Rate Links.
    DATA_WIDTH_40BIT = 0x2  # This value is used for DP 2.0 with 128b/132b.


class ENUM_D2D_LINK_STATE(Enum):
    D2D_LINK_STATE_DISABLED = 0x0
    D2D_LINK_STATE_ENABLED = 0x1


class ENUM_D2D_LINK_ENABLE(Enum):
    D2D_LINK_DISABLE = 0x0
    D2D_LINK_ENABLE = 0x1


class ENUM_ENABLE(Enum):
    ENABLE_DISABLE = 0x0
    ENABLE_ENABLE = 0x1


class OFFSET_DDI_CTL_DE:
    DDI_CTL_DE_A = 0x64000
    DDI_CTL_DE_B = 0x64100
    DDI_CTL_DE_USBC1 = 0x64300
    DDI_CTL_DE_USBC2 = 0x64400
    DDI_CTL_DE_USBC3 = 0x64500
    DDI_CTL_DE_USBC4 = 0x64600

class _DDI_CTL_DE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('PortWidth', ctypes.c_uint32, 3),
        ('Reserved4', ctypes.c_uint32, 2),
        ('BypassIdleStatus', ctypes.c_uint32, 1),
        ('IdleStatus', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 8),
        ('PortReversal', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 1),
        ('DataWidth', ctypes.c_uint32, 2),
        ('Reserved20', ctypes.c_uint32, 8),
        ('D2DLinkState', ctypes.c_uint32, 1),
        ('D2DLinkEnable', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('Enable', ctypes.c_uint32, 1),
    ]


class REG_DDI_CTL_DE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 0
    PortWidth = 0  # bit 1 to 3
    Reserved4 = 0  # bit 4 to 5
    BypassIdleStatus = 0  # bit 6 to 6
    IdleStatus = 0  # bit 7 to 7
    Reserved8 = 0  # bit 8 to 15
    PortReversal = 0  # bit 16 to 16
    Reserved17 = 0  # bit 17 to 17
    DataWidth = 0  # bit 18 to 19
    Reserved20 = 0  # bit 20 to 27
    D2DLinkState = 0  # bit 28 to 28
    D2DLinkEnable = 0  # bit 29 to 29
    Reserved30 = 0  # bit 30 to 30
    Enable = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_CTL_DE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_CTL_DE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CONFIG_BUS_GRANT_ERROR(Enum):
    CONFIG_BUS_GRANT_ERROR_NO_ERROR = 0x0
    CONFIG_BUS_GRANT_ERROR_ERROR = 0x1


class ENUM_CONFIG_BUS_DATA(Enum):
    CONFIG_BUS_DATA_FORCE_PHY_POWER_DOWN = 0x0
    CONFIG_BUS_DATA_RELEASE_PHY_POWER_DOWN = 0x1
    CONFIG_BUS_DATA_FORCE_PHY_PLL_OFF = 0x2
    CONFIG_BUS_DATA_RELEASE_PHY_PLL_OFF = 0x3
    CONFIG_BUS_DATA_INITIATE_CUSTOM_AUX = 0x4
    CONFIG_BUS_DATA_STATUS_OF_CUSTOM_AUX = 0x5


class ENUM_CONFIG_BUS_ABORT(Enum):
    CONFIG_BUS_ABORT_DO_NOT_ABORT = 0x0
    CONFIG_BUS_ABORT_ABORT = 0x1


class ENUM_CONFIG_BUS_GRANT(Enum):
    CONFIG_BUS_GRANT_NOT_GRANTED = 0x0
    CONFIG_BUS_GRANT_GRANTED = 0x1


class ENUM_CONFIG_BUS_REQUEST(Enum):
    CONFIG_BUS_REQUEST_DISABLED = 0x0
    CONFIG_BUS_REQUEST_ENABLED = 0x1


class OFFSET_PMCONFIGBUS:
    PMCONFIGBUS_A = 0x452B4
    PMCONFIGBUS_B = 0x452B8

class _PMCONFIGBUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 3),
        ('ConfigBusGrantError', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 12),
        ('ConfigBusDataDelay', ctypes.c_uint32, 8),
        ('ConfigBusData', ctypes.c_uint32, 4),
        ('Reserved28', ctypes.c_uint32, 1),
        ('ConfigBusAbort', ctypes.c_uint32, 1),
        ('ConfigBusGrant', ctypes.c_uint32, 1),
        ('ConfigBusRequest', ctypes.c_uint32, 1),
    ]


class REG_PMCONFIGBUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 2
    ConfigBusGrantError = 0  # bit 3 to 3
    Reserved4 = 0  # bit 4 to 15
    ConfigBusDataDelay = 0  # bit 16 to 23
    ConfigBusData = 0  # bit 24 to 27
    Reserved28 = 0  # bit 28 to 28
    ConfigBusAbort = 0  # bit 29 to 29
    ConfigBusGrant = 0  # bit 30 to 30
    ConfigBusRequest = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PMCONFIGBUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PMCONFIGBUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SYNC_PULSE_COUNT(Enum):
    SYNC_PULSE_COUNT_32_PULSES = 0x1F


class ENUM_FAST_WAKE_SYNC_PULSE_COUNT(Enum):
    FAST_WAKE_SYNC_PULSE_COUNT_18_PULSES = 0x11


class ENUM_IO_SELECT(Enum):
    IO_SELECT_TBT = 0x1  # Use Thunderbolt IO
    IO_SELECT_NON_TBT = 0x0  # Use non-thunderbolt (legacy) IO.This is used for typeC ports in DP-alternate or native/f
                             # ixed/legacy mode or for non-typeC ports.


class ENUM_AUX_FRAME_SYNC_DATA_SELECT(Enum):
    AUX_FRAME_SYNC_DATA_SELECT_AUX = 0x1  # Use AUX Data registers for frame sync
    AUX_FRAME_SYNC_DATA_SELECT_HARDCODED = 0x0  # Use hardcoded data value for frame sync.


class ENUM_AUX_PSR_DATA_SELECT(Enum):
    AUX_PSR_DATA_SELECT_AUX = 0x1  # Use AUX Data registers for PSR
    AUX_PSR_DATA_SELECT_HARDCODED = 0x0  # Use hardcoded data value for PSR.


class ENUM_AUX_AKSV_SELECT(Enum):
    AUX_AKSV_SELECT_AUX = 0x0  # Use AUX Data registers for regular data transmission
    AUX_AKSV_SELECT_HDCP = 0x1  # Use HDCP internal Aksv for part of the data transmission.


class ENUM_PHY_POWER_STATE(Enum):
    PHY_POWER_STATE_DISABLE = 0x0
    PHY_POWER_STATE_ENABLE = 0x1


class ENUM_PHY_POWER_REQUEST(Enum):
    PHY_POWER_REQUEST_DISABLE = 0x0
    PHY_POWER_REQUEST_ENABLE = 0x1


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


class OFFSET_PORT_AUX_CTL:
    PORT_AUX_CTL_USBC1 = 0x16F210
    PORT_AUX_CTL_USBC2 = 0x16F410
    PORT_AUX_CTL_USBC3 = 0x16F610
    PORT_AUX_CTL_USBC4 = 0x16F810
    PORT_AUX_CTL_A = 0x16FA10
    PORT_AUX_CTL_B = 0x16FC10

class _PORT_AUX_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SyncPulseCount', ctypes.c_uint32, 5),
        ('FastWakeSyncPulseCount', ctypes.c_uint32, 5),
        ('Reserved10', ctypes.c_uint32, 1),
        ('IoSelect', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 1),
        ('AuxFrameSyncDataSelect', ctypes.c_uint32, 1),
        ('AuxPsrDataSelect', ctypes.c_uint32, 1),
        ('AuxAksvSelect', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 2),
        ('PhyPowerState', ctypes.c_uint32, 1),
        ('PhyPowerRequest', ctypes.c_uint32, 1),
        ('MessageSize', ctypes.c_uint32, 5),
        ('ReceiveError', ctypes.c_uint32, 1),
        ('TimeOutTimerValue', ctypes.c_uint32, 2),
        ('TimeOutError', ctypes.c_uint32, 1),
        ('InterruptOnDone', ctypes.c_uint32, 1),
        ('Done', ctypes.c_uint32, 1),
        ('SendBusy', ctypes.c_uint32, 1),
    ]


class REG_PORT_AUX_CTL(ctypes.Union):
    value = 0
    offset = 0

    SyncPulseCount = 0  # bit 0 to 4
    FastWakeSyncPulseCount = 0  # bit 5 to 9
    Reserved10 = 0  # bit 10 to 10
    IoSelect = 0  # bit 11 to 11
    Reserved12 = 0  # bit 12 to 12
    AuxFrameSyncDataSelect = 0  # bit 13 to 13
    AuxPsrDataSelect = 0  # bit 14 to 14
    AuxAksvSelect = 0  # bit 15 to 15
    Reserved16 = 0  # bit 16 to 17
    PhyPowerState = 0  # bit 18 to 18
    PhyPowerRequest = 0  # bit 19 to 19
    MessageSize = 0  # bit 20 to 24
    ReceiveError = 0  # bit 25 to 25
    TimeOutTimerValue = 0  # bit 26 to 27
    TimeOutError = 0  # bit 28 to 28
    InterruptOnDone = 0  # bit 29 to 29
    Done = 0  # bit 30 to 30
    SendBusy = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_AUX_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_AUX_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_AUX_DATA:
    PORT_AUX_DATA_0_USBC1 = 0x16F214
    PORT_AUX_DATA_1_USBC1 = 0x16F218
    PORT_AUX_DATA_2_USBC1 = 0x16F21C
    PORT_AUX_DATA_3_USBC1 = 0x16F220
    PORT_AUX_DATA_4_USBC1 = 0x16F224
    PORT_AUX_DATA_0_USBC2 = 0x16F414
    PORT_AUX_DATA_1_USBC2 = 0x16F418
    PORT_AUX_DATA_2_USBC2 = 0x16F41C
    PORT_AUX_DATA_3_USBC2 = 0x16F420
    PORT_AUX_DATA_4_USBC2 = 0x16F424
    PORT_AUX_DATA_0_USBC3 = 0x16F614
    PORT_AUX_DATA_1_USBC3 = 0x16F618
    PORT_AUX_DATA_2_USBC3 = 0x16F61C
    PORT_AUX_DATA_3_USBC3 = 0x16F620
    PORT_AUX_DATA_4_USBC3 = 0x16F624
    PORT_AUX_DATA_0_USBC4 = 0x16F814
    PORT_AUX_DATA_1_USBC4 = 0x16F818
    PORT_AUX_DATA_2_USBC4 = 0x16F81C
    PORT_AUX_DATA_3_USBC4 = 0x16F820
    PORT_AUX_DATA_4_USBC4 = 0x16F824
    PORT_AUX_DATA_0_A = 0x16FA14
    PORT_AUX_DATA_1_A = 0x16FA18
    PORT_AUX_DATA_2_A = 0x16FA1C
    PORT_AUX_DATA_3_A = 0x16FA20
    PORT_AUX_DATA_4_A = 0x16FA24
    PORT_AUX_DATA_0_B = 0x16FC14
    PORT_AUX_DATA_1_B = 0x16FC18
    PORT_AUX_DATA_2_B = 0x16FC1C
    PORT_AUX_DATA_3_B = 0x16FC20
    PORT_AUX_DATA_4_B = 0x16FC24

class _PORT_AUX_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AuxChData', ctypes.c_uint32, 32),
    ]


class REG_PORT_AUX_DATA(ctypes.Union):
    value = 0
    offset = 0

    AuxChData = 0  # bit 0 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_AUX_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_AUX_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PICA_AUXCLK_CTL:
    PICA_AUXCLK_CTL_0 = 0x16FE40

class _PICA_AUXCLK_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SbFrequencyDecimal', ctypes.c_uint32, 11),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PICA_AUXCLK_CTL(ctypes.Union):
    value = 0
    offset = 0

    SbFrequencyDecimal = 0  # bit 0 to 10
    Reserved11 = 0  # bit 11 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PICA_AUXCLK_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PICA_AUXCLK_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ALPM_AUX_LESS_ENABLE(Enum):
    ALPM_AUX_LESS_DISABLED_AUXWAKE = 0x0
    ALPM_AUX_LESS_ENABLED_AUXLESS = 0x1


class OFFSET_PORT_ALPM_CTL:
    PORT_ALPM_CTL_A = 0x16FA2C
    PORT_ALPM_CTL_B = 0x16FC2C

class _PORT_ALPM_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SilencePeriod', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 8),
        ('MaxPhySwingHold', ctypes.c_uint32, 4),
        ('MaxPhySwingSetup', ctypes.c_uint32, 4),
        ('Reserved24', ctypes.c_uint32, 7),
        ('AlpmAuxLessEnable', ctypes.c_uint32, 1),
    ]


class REG_PORT_ALPM_CTL(ctypes.Union):
    value = 0
    offset = 0

    SilencePeriod = 0  # bit 0 to 7
    Reserved8 = 0  # bit 8 to 15
    MaxPhySwingHold = 0  # bit 16 to 19
    MaxPhySwingSetup = 0  # bit 20 to 23
    Reserved24 = 0  # bit 24 to 30
    AlpmAuxLessEnable = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_ALPM_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_ALPM_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_LFPS_CYCLE_COUNT(Enum):
    LFPS_CYCLE_COUNT_7_CYCLES = 0x0
    LFPS_CYCLE_COUNT_8_CYCLES = 0x1
    LFPS_CYCLE_COUNT_9_CYCLES = 0x2
    LFPS_CYCLE_COUNT_10_CYCLES = 0x3


class ENUM_LFPS_START_POLARITY(Enum):
    LFPS_START_POLARITY_NEGATIVE_POLARITY = 0x0  # LFPS pattern starts with a 0
    LFPS_START_POLARITY_POSITIVE_POLARITY = 0x1  # LFPS pattern starts with a 1


class OFFSET_PORT_ALPM_LFPS_CTL:
    PORT_ALPM_LFPS_CTL_A = 0x16FA30
    PORT_ALPM_LFPS_CTL_B = 0x16FC30

class _PORT_ALPM_LFPS_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LastLfpsHalfCycleDuration', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 3),
        ('FirstLfpsHalfCycleDuration', ctypes.c_uint32, 5),
        ('Reserved13', ctypes.c_uint32, 3),
        ('LfpsHalfCycleDuration', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 3),
        ('LfpsCycleCount', ctypes.c_uint32, 2),
        ('Reserved26', ctypes.c_uint32, 5),
        ('LfpsStartPolarity', ctypes.c_uint32, 1),
    ]


class REG_PORT_ALPM_LFPS_CTL(ctypes.Union):
    value = 0
    offset = 0

    LastLfpsHalfCycleDuration = 0  # bit 0 to 4
    Reserved5 = 0  # bit 5 to 7
    FirstLfpsHalfCycleDuration = 0  # bit 8 to 12
    Reserved13 = 0  # bit 13 to 15
    LfpsHalfCycleDuration = 0  # bit 16 to 20
    Reserved21 = 0  # bit 21 to 23
    LfpsCycleCount = 0  # bit 24 to 25
    Reserved26 = 0  # bit 26 to 30
    LfpsStartPolarity = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_ALPM_LFPS_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_ALPM_LFPS_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_AUX_ARBITER_STATE_MACHINE_STATUS(Enum):
    AUX_ARBITER_STATE_MACHINE_STATUS_ARBIDLE = 0x0
    AUX_ARBITER_STATE_MACHINE_STATUS_ARBFRAMESYNC = 0x1
    AUX_ARBITER_STATE_MACHINE_STATUS_ARBFASTWAKE = 0x2
    AUX_ARBITER_STATE_MACHINE_STATUS_ARBGTC = 0x3
    AUX_ARBITER_STATE_MACHINE_STATUS_ARBSOFTWARE = 0x4
    AUX_ARBITER_STATE_MACHINE_STATUS_ARBPSR = 0x5


class ENUM_SENDING_AUX(Enum):
    SENDING_AUX_NOT_SENDING = 0x0  # Not sending AUX handshake
    SENDING_AUX_SENDING = 0x1  # Sending AUX handshake


class ENUM_SYNC_ONLY_CLOCK_RECOVERY(Enum):
    SYNC_ONLY_CLOCK_RECOVERY_SYNC_AND_DATA = 0x0  # Recover clock during sync pattern and data phase
    SYNC_ONLY_CLOCK_RECOVERY_SYNC_ONLY = 0x1  # Only recover clock during sync pattern


class ENUM_INVERT_MANCHESTER(Enum):
    INVERT_MANCHESTER_NORMAL = 0x0  # Manchester code rising edge mid-clk signifies zero
    INVERT_MANCHESTER_INVERT = 0x1  # Manchester code rising edge mid-clk signifies one


class ENUM_GLOBAL_RX_INVERT(Enum):
    GLOBAL_RX_INVERT_NONINVERTED = 0x0  # No part of the transaction is inverted.
    GLOBAL_RX_INVERT_INVERTED = 0x1  # Complete transaction is inverted.


class ENUM_GLOBAL_TX_INVERT(Enum):
    GLOBAL_TX_INVERT_NONINVERTED = 0x0  # No part of the transaction is inverted.
    GLOBAL_TX_INVERT_INVERTED = 0x1  # Complete transaction is inverted.


class ENUM_MULTI_RX_EDGES_ERROR_ENABLE(Enum):
    MULTI_RX_EDGES_ERROR_ENABLE_OKAY = 0x0  # Multiple edges in window is okay
    MULTI_RX_EDGES_ERROR_ENABLE_ERROR = 0x1  # Multiple edges in window is an error


class ENUM_DEGLITCH_AMOUNT(Enum):
    DEGLITCH_AMOUNT_25_CLOCKS = 0x0  # 25 clocks - 50ns at 500MHz cdclk
    DEGLITCH_AMOUNT_125NS = 0x1  # 1/4 2X bit clock divider value - 125ns
    DEGLITCH_AMOUNT_62_5NS = 0x2  # 1/8 2X bit clock divider value - 62.5ns
    DEGLITCH_AMOUNT_31_125NS = 0x3  # 1/16 2X bit clock divider value - 31.125ns


class ENUM_FASTWAKE_DONE(Enum):
    FASTWAKE_DONE_NOT_DONE = 0x0
    FASTWAKE_DONE_DONE = 0x1


class ENUM_TIGHTEN_FREQUENCY_WINDOW(Enum):
    TIGHTEN_FREQUENCY_WINDOW_DISABLE = 0x0
    TIGHTEN_FREQUENCY_WINDOW_ENABLE = 0x1


class ENUM_CONSTANT_0S_TEST_PATTERN(Enum):
    CONSTANT_0S_TEST_PATTERN_DISABLE = 0x0
    CONSTANT_0S_TEST_PATTERN_ENABLE = 0x1


class ENUM_AUX_ERROR(Enum):
    AUX_ERROR_NO_ERROR = 0x0  # AUX had no error
    AUX_ERROR_ERROR = 0x1  # AUX error (receive error or timeout) occured


class ENUM_MULTIPLE_EDGES_OUTSIDE_STATUS(Enum):
    MULTIPLE_EDGES_OUTSIDE_STATUS_SINGLE_EDGE_OUTSIDE_FREQUENCY_WINDOW = 0x0
    MULTIPLE_EDGES_OUTSIDE_STATUS_MULTIPLE_EDGES_OUTSIDE_FREQUENCY_WINDOW = 0x1


class ENUM_MULTIPLE_EDGES_INSIDE_STATUS(Enum):
    MULTIPLE_EDGES_INSIDE_STATUS_SINGLE_EDGE_INSIDE_FREQUENCY_WINDOW = 0x0
    MULTIPLE_EDGES_INSIDE_STATUS_MULTIPLE_EDGES_INSIDE_FREQUENCY_WINDOW = 0x1


class ENUM_DATA_NOT_BYTE_ALIGNED_STATUS(Enum):
    DATA_NOT_BYTE_ALIGNED_STATUS_DATA_RECEIVED_WAS_BYTE_ALIGNED = 0x0
    DATA_NOT_BYTE_ALIGNED_STATUS_DATA_RECEIVED_WAS_NOT_BYTE_ALIGNED = 0x1


class ENUM_TOO_MUCH_DATA_STATUS(Enum):
    TOO_MUCH_DATA_STATUS_AUX_CONTROLLER_RECEIVED_LESS_THAN_OR_EQUAL_TO_20_BYTES = 0x0
    TOO_MUCH_DATA_STATUS_AUX_CONTROLLER_RECEIVED_MORE_THAN_20_BYTES = 0x1


class ENUM_BAD_STOP_STATUS(Enum):
    BAD_STOP_STATUS_VALID_STOP = 0x0
    BAD_STOP_STATUS_BAD_STOP_AT_THE_END_OF_THE_DATA_PHASE = 0x1


class ENUM_CONTROL_STATE_MACHINE_STATUS(Enum):
    CONTROL_STATE_MACHINE_STATUS_CTLIDLE = 0x0
    CONTROL_STATE_MACHINE_STATUS_CTLTURNAROUND = 0x1
    CONTROL_STATE_MACHINE_STATUS_CTLPRECH = 0x2
    CONTROL_STATE_MACHINE_STATUS_CTLXMITSYNC = 0x3
    CONTROL_STATE_MACHINE_STATUS_CTLXMITDATA = 0x4
    CONTROL_STATE_MACHINE_STATUS_CTLXMITSTOP = 0x5
    CONTROL_STATE_MACHINE_STATUS_CTLRCVWAIT = 0x6
    CONTROL_STATE_MACHINE_STATUS_CTLRCVSYNC = 0x7
    CONTROL_STATE_MACHINE_STATUS_CTLRCVDATA = 0x8
    CONTROL_STATE_MACHINE_STATUS_CTLDONE = 0x9
    CONTROL_STATE_MACHINE_STATUS_CTLSPARE1 = 0xA
    CONTROL_STATE_MACHINE_STATUS_CTLSPARE2 = 0xB


class ENUM_OUTPUT_SERIAL_DATA_STATUS(Enum):
    OUTPUT_SERIAL_DATA_STATUS_LOW = 0x0
    OUTPUT_SERIAL_DATA_STATUS_HIGH = 0x1


class ENUM_INPUT_SERIAL_DATA_STATUS(Enum):
    INPUT_SERIAL_DATA_STATUS_LOW = 0x0
    INPUT_SERIAL_DATA_STATUS_HIGH = 0x1


class ENUM_LOOPBACK_TYPE(Enum):
    LOOPBACK_TYPE_DIGITAL = 0x0
    LOOPBACK_TYPE_ANALOG = 0x1


class ENUM_LOOPBACK_ENABLE(Enum):
    LOOPBACK_DISABLE = 0x0
    LOOPBACK_ENABLE = 0x1


class ENUM_FASTWAKE_INVALID_REQUEST(Enum):
    FASTWAKE_INVALID_REQUEST_NO_ERROR = 0x0
    FASTWAKE_INVALID_REQUEST_ERROR = 0x1


class ENUM_FASTWAKE_RECEIVE_ERROR(Enum):
    FASTWAKE_RECEIVE_ERROR_NO_ERROR = 0x0
    FASTWAKE_RECEIVE_ERROR_ERROR = 0x1


class ENUM_FASTWAKE_TIME_OUT_ERROR(Enum):
    FASTWAKE_TIME_OUT_ERROR_NO_ERROR = 0x0
    FASTWAKE_TIME_OUT_ERROR_ERROR = 0x1


class OFFSET_PORT_AUX_TST:
    PORT_AUX_TST_USBC1 = 0x16F228
    PORT_AUX_TST_USBC2 = 0x16F428
    PORT_AUX_TST_USBC3 = 0x16F628
    PORT_AUX_TST_USBC4 = 0x16F828
    PORT_AUX_TST_A = 0x16FA28
    PORT_AUX_TST_B = 0x16FC28

class _PORT_AUX_TST(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AuxArbiterStateMachineStatus', ctypes.c_uint32, 3),
        ('SendingAux', ctypes.c_uint32, 1),
        ('SyncOnlyClockRecovery', ctypes.c_uint32, 1),
        ('InvertManchester', ctypes.c_uint32, 1),
        ('GlobalRxInvert', ctypes.c_uint32, 1),
        ('GlobalTxInvert', ctypes.c_uint32, 1),
        ('MultiRxEdgesErrorEnable', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 1),
        ('DeglitchAmount', ctypes.c_uint32, 2),
        ('FastwakeDone', ctypes.c_uint32, 1),
        ('TightenFrequencyWindow', ctypes.c_uint32, 1),
        ('Constant0STestPattern', ctypes.c_uint32, 1),
        ('AuxError', ctypes.c_uint32, 1),
        ('MultipleEdgesOutsideStatus', ctypes.c_uint32, 1),
        ('MultipleEdgesInsideStatus', ctypes.c_uint32, 1),
        ('DataNotByteAlignedStatus', ctypes.c_uint32, 1),
        ('TooMuchDataStatus', ctypes.c_uint32, 1),
        ('BadStopStatus', ctypes.c_uint32, 1),
        ('ControlStateMachineStatus', ctypes.c_uint32, 4),
        ('OutputSerialDataStatus', ctypes.c_uint32, 1),
        ('InputSerialDataStatus', ctypes.c_uint32, 1),
        ('LoopbackType', ctypes.c_uint32, 1),
        ('LoopbackEnable', ctypes.c_uint32, 1),
        ('FastwakeInvalidRequest', ctypes.c_uint32, 1),
        ('FastwakeReceiveError', ctypes.c_uint32, 1),
        ('FastwakeTimeOutError', ctypes.c_uint32, 1),
    ]


class REG_PORT_AUX_TST(ctypes.Union):
    value = 0
    offset = 0

    AuxArbiterStateMachineStatus = 0  # bit 0 to 2
    SendingAux = 0  # bit 3 to 3
    SyncOnlyClockRecovery = 0  # bit 4 to 4
    InvertManchester = 0  # bit 5 to 5
    GlobalRxInvert = 0  # bit 6 to 6
    GlobalTxInvert = 0  # bit 7 to 7
    MultiRxEdgesErrorEnable = 0  # bit 8 to 8
    Reserved9 = 0  # bit 9 to 9
    DeglitchAmount = 0  # bit 10 to 11
    FastwakeDone = 0  # bit 12 to 12
    TightenFrequencyWindow = 0  # bit 13 to 13
    Constant0STestPattern = 0  # bit 14 to 14
    AuxError = 0  # bit 15 to 15
    MultipleEdgesOutsideStatus = 0  # bit 16 to 16
    MultipleEdgesInsideStatus = 0  # bit 17 to 17
    DataNotByteAlignedStatus = 0  # bit 18 to 18
    TooMuchDataStatus = 0  # bit 19 to 19
    BadStopStatus = 0  # bit 20 to 20
    ControlStateMachineStatus = 0  # bit 21 to 24
    OutputSerialDataStatus = 0  # bit 25 to 25
    InputSerialDataStatus = 0  # bit 26 to 26
    LoopbackType = 0  # bit 27 to 27
    LoopbackEnable = 0  # bit 28 to 28
    FastwakeInvalidRequest = 0  # bit 29 to 29
    FastwakeReceiveError = 0  # bit 30 to 30
    FastwakeTimeOutError = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_AUX_TST),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_AUX_TST, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PICA_DEVICE_ID:
    PICA_DEVICE_ID_0 = 0x16FE00

class _PICA_DEVICE_ID(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare', ctypes.c_uint32, 8),
        ('Revision', ctypes.c_uint32, 8),
        ('MinorArch', ctypes.c_uint32, 8),
        ('MajorArch', ctypes.c_uint32, 8),
    ]


class REG_PICA_DEVICE_ID(ctypes.Union):
    value = 0
    offset = 0

    Spare = 0  # bit 0 to 7
    Revision = 0  # bit 8 to 15
    MinorArch = 0  # bit 16 to 23
    MajorArch = 0  # bit 24 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PICA_DEVICE_ID),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PICA_DEVICE_ID, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_UTIL1_PIN_DIRECTION(Enum):
    UTIL1_PIN_DIRECTION_OUTPUT = 0x0
    UTIL1_PIN_DIRECTION_INPUT = 0x1


class ENUM_UTIL1_PIN_ENABLE(Enum):
    UTIL1_PIN_DISABLE = 0x0
    UTIL1_PIN_ENABLE = 0x1


class ENUM_UTIL2_PIN_DIRECTION(Enum):
    UTIL2_PIN_DIRECTION_OUTPUT = 0x0
    UTIL2_PIN_DIRECTION_INPUT = 0x1


class ENUM_UTIL2_PIN_ENABLE(Enum):
    UTIL2_PIN_DISABLE = 0x0
    UTIL2_PIN_ENABLE = 0x1


class ENUM_PLL_LOCK(Enum):
    PLL_LOCK_NOT_LOCKED_OR_NOT_ENABLED = 0x0
    PLL_LOCK_LOCKED = 0x1


class ENUM_PLL_ENABLE(Enum):
    PLL_DISABLE = 0x0
    PLL_ENABLE = 0x1


class OFFSET_PICA_GENLOCK_CONTROL:
    PICA_GENLOCK_CONTROL_0 = 0x16FE14

class _PICA_GENLOCK_CONTROL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('Util1PinDirection', ctypes.c_uint32, 1),
        ('Util1PinEnable', ctypes.c_uint32, 1),
        ('Util2PinDirection', ctypes.c_uint32, 1),
        ('Util2PinEnable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 14),
        ('PllLock', ctypes.c_uint32, 1),
        ('PllEnable', ctypes.c_uint32, 1),
    ]


class REG_PICA_GENLOCK_CONTROL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 11
    Util1PinDirection = 0  # bit 12 to 12
    Util1PinEnable = 0  # bit 13 to 13
    Util2PinDirection = 0  # bit 14 to 14
    Util2PinEnable = 0  # bit 15 to 15
    Reserved16 = 0  # bit 16 to 29
    PllLock = 0  # bit 30 to 30
    PllEnable = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PICA_GENLOCK_CONTROL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PICA_GENLOCK_CONTROL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SKIP_PORT_SLICES_RESET_PREP(Enum):
    SKIP_PORT_SLICES_RESET_PREP_DO_NOT_SKIP = 0x0
    SKIP_PORT_SLICES_RESET_PREP_SKIP = 0x1


class ENUM_TYPEC_PIPEIF_LATCH_ENABLE_OVRD(Enum):
    TYPEC_PIPEIF_LATCH_ENABLE_OVRD_NO_OVERRIDE = 0x0
    TYPEC_PIPEIF_LATCH_ENABLE_OVRD_OVERRIDE = 0x1


class ENUM_DFDPICA_CLOCKGATING_DISABLE(Enum):
    DFDPICA_CLOCKGATING_DISABLE_DO_NOT_DISABLE = 0x0
    DFDPICA_CLOCKGATING_DISABLE = 0x1


class ENUM_DRPOPICA_CLOCKGATING_DISABLE(Enum):
    DRPOPICA_CLOCKGATING_DISABLE_DO_NOT_DISABLE = 0x0
    DRPOPICA_CLOCKGATING_DISABLE = 0x1


class ENUM_DPMGPICA_CLOCKGATING_DISABLE(Enum):
    DPMGPICA_CLOCKGATING_DISABLE_DO_NOT_DISABLE = 0x0
    DPMGPICA_CLOCKGATING_DISABLE = 0x1


class ENUM_AUX_CLOCKGATING_DISABLE(Enum):
    AUX_CLOCKGATING_DISABLE_DO_NOT_DISABLE = 0x0
    AUX_CLOCKGATING_DISABLE = 0x1


class ENUM_RESET_PREP_RESET_LENGTH(Enum):
    RESET_PREP_RESET_LENGTH_8_CLOCKS = 0x8


class ENUM_BYPASS_POWER_WELL_1_TURNOFF(Enum):
    BYPASS_POWER_WELL_1_TURNOFF_TURN_OFF = 0x0
    BYPASS_POWER_WELL_1_TURNOFF_DO_NOT_TURN_OFF = 0x1


class ENUM_SB_CLOCK_OVERRIDE(Enum):
    SB_CLOCK_OVERRIDE_DO_NOT_OVERRIDE = 0x0  # SB clock shuts down when PICA is in idle state.
    SB_CLOCK_OVERRIDE_OVERRIDE = 0x1  # SB clock continues to run when PICA is in idle state.


class ENUM_CHASSIS_CLOCK_REQUEST_DURATION(Enum):
    CHASSIS_CLOCK_REQUEST_DURATION_13_CLOCKS = 0x9


class OFFSET_PICA_CHKN:
    PICA_CHKN_0 = 0x16FE10

class _PICA_CHKN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SkipPortSlicesResetPrep', ctypes.c_uint32, 1),
        ('Spare1', ctypes.c_uint32, 1),
        ('Spare2', ctypes.c_uint32, 1),
        ('Spare3', ctypes.c_uint32, 1),
        ('Spare4', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('Spare6', ctypes.c_uint32, 1),
        ('Spare7', ctypes.c_uint32, 1),
        ('Spare8', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('Spare10', ctypes.c_uint32, 1),
        ('Typec_Pipeif_Latch_Enable_Ovrd', ctypes.c_uint32, 1),
        ('DfdpicaClockgatingDisable', ctypes.c_uint32, 1),
        ('DrpopicaClockgatingDisable', ctypes.c_uint32, 1),
        ('DpmgpicaClockgatingDisable', ctypes.c_uint32, 1),
        ('AuxClockgatingDisable', ctypes.c_uint32, 1),
        ('ResetPrepResetLength', ctypes.c_uint32, 5),
        ('BypassPowerWell1Turnoff', ctypes.c_uint32, 1),
        ('SkipPfetAck', ctypes.c_uint32, 1),
        ('SbClockOverride', ctypes.c_uint32, 1),
        ('ChassisClockRequestDuration', ctypes.c_uint32, 4),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_PICA_CHKN(ctypes.Union):
    value = 0
    offset = 0

    SkipPortSlicesResetPrep = 0  # bit 0 to 0
    Spare1 = 0  # bit 1 to 1
    Spare2 = 0  # bit 2 to 2
    Spare3 = 0  # bit 3 to 3
    Spare4 = 0  # bit 4 to 4
    Spare5 = 0  # bit 5 to 5
    Spare6 = 0  # bit 6 to 6
    Spare7 = 0  # bit 7 to 7
    Spare8 = 0  # bit 8 to 8
    Spare9 = 0  # bit 9 to 9
    Spare10 = 0  # bit 10 to 10
    Typec_Pipeif_Latch_Enable_Ovrd = 0  # bit 11 to 11
    DfdpicaClockgatingDisable = 0  # bit 12 to 12
    DrpopicaClockgatingDisable = 0  # bit 13 to 13
    DpmgpicaClockgatingDisable = 0  # bit 14 to 14
    AuxClockgatingDisable = 0  # bit 15 to 15
    ResetPrepResetLength = 0  # bit 16 to 20
    BypassPowerWell1Turnoff = 0  # bit 21 to 21
    SkipPfetAck = 0  # bit 22 to 22
    SbClockOverride = 0  # bit 23 to 23
    ChassisClockRequestDuration = 0  # bit 24 to 27
    Reserved28 = 0  # bit 28 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PICA_CHKN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PICA_CHKN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ISOLREQ_ASSERT_DELAY(Enum):
    ISOLREQ_ASSERT_DELAY_5 = 0x5  # 5 sideband clock cycles at 400.00 MHz.


class ENUM_ISOLREQ_DEASSERT_DELAY(Enum):
    ISOLREQ_DEASSERT_DELAY_2 = 0x2  # 2 sideband clock cycles at 400.00 MHz.


class ENUM_CLKACK_ASSERT_DELAY(Enum):
    CLKACK_ASSERT_DELAY_5 = 0x5  # 5 sideband clock cycles at 400.00 MHz.


class ENUM_CLKACK_DEASSERT_DELAY(Enum):
    CLKACK_DEASSERT_DELAY_2 = 0x2  # 2 sideband clock cycles at 400.00 MHz.


class ENUM_RSTACK_ASSERT_DELAY(Enum):
    RSTACK_ASSERT_DELAY_5 = 0x5  # 5 sideband clock cycles at 400.00 MHz.


class ENUM_RSTACK_DEASSERT_DELAY(Enum):
    RSTACK_DEASSERT_DELAY_2 = 0x2  # 2 sideband clock cycles at 400.00 MHz.


class OFFSET_PICA_DCP_DCPR_INTF_DELAY:
    PICA_DCP_DCPR_INTF_DELAY_0 = 0x16FE0C

class _PICA_DCP_DCPR_INTF_DELAY(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Isolreq_Assert_Delay', ctypes.c_uint32, 5),
        ('Isolreq_Deassert_Delay', ctypes.c_uint32, 5),
        ('Clkack_Assert_Delay', ctypes.c_uint32, 5),
        ('Clkack_Deassert_Delay', ctypes.c_uint32, 5),
        ('Rstack_Assert_Delay', ctypes.c_uint32, 5),
        ('Rstack_Deassert_Delay', ctypes.c_uint32, 5),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PICA_DCP_DCPR_INTF_DELAY(ctypes.Union):
    value = 0
    offset = 0

    Isolreq_Assert_Delay = 0  # bit 0 to 4
    Isolreq_Deassert_Delay = 0  # bit 5 to 9
    Clkack_Assert_Delay = 0  # bit 10 to 14
    Clkack_Deassert_Delay = 0  # bit 15 to 19
    Rstack_Assert_Delay = 0  # bit 20 to 24
    Rstack_Deassert_Delay = 0  # bit 25 to 29
    Reserved30 = 0  # bit 30 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PICA_DCP_DCPR_INTF_DELAY),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PICA_DCP_DCPR_INTF_DELAY, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_POWERUP_PFET_DELAY(Enum):
    POWERUP_PFET_DELAY_200 = 0xC8  # 200 sideband clock cycles at 400.00 MHz for 500ns delay specified.


class ENUM_FORCEON_PFET_DELAY(Enum):
    FORCEON_PFET_DELAY_200 = 0xC8  # 200 sideband clock cycles at 400.00 MHz for 500ns delay specified.


class ENUM_PWR_GOOD_CNTR(Enum):
    PWR_GOOD_CNTR_200 = 0xC8  # 200 sideband clock cycles at 400.00 MHz for 500ns delay specified.


class OFFSET_PICA_PFET_EN_DELAY:
    PICA_PFET_EN_DELAY_0 = 0x16FE08

class _PICA_PFET_EN_DELAY(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PowerupPfetDelay', ctypes.c_uint32, 10),
        ('ForceonPfetDelay', ctypes.c_uint32, 10),
        ('Pwr_Good_Cntr', ctypes.c_uint32, 10),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PICA_PFET_EN_DELAY(ctypes.Union):
    value = 0
    offset = 0

    PowerupPfetDelay = 0  # bit 0 to 9
    ForceonPfetDelay = 0  # bit 10 to 19
    Pwr_Good_Cntr = 0  # bit 20 to 29
    Reserved30 = 0  # bit 30 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PICA_PFET_EN_DELAY),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PICA_PFET_EN_DELAY, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_HDMI_FRL_SHIFTER_ENABLE(Enum):
    HDMI_FRL_SHIFTER_DISABLE = 0x0
    HDMI_FRL_SHIFTER_ENABLE = 0x1


class ENUM_TCSS_POWER_STATE(Enum):
    TCSS_POWER_STATE_DISABLED = 0x0
    TCSS_POWER_STATE_ENABLED = 0x1


class ENUM_TCSS_POWER_REQUEST(Enum):
    TCSS_POWER_REQUEST_DISABLE = 0x0
    TCSS_POWER_REQUEST_ENABLE = 0x1


class ENUM_TYPEC_PHY_OWNERSHIP(Enum):
    TYPEC_PHY_OWNERSHIP_RELEASE_OWNERSHIP = 0x0
    TYPEC_PHY_OWNERSHIP_TAKE_OWNERSHIP = 0x1


class ENUM_PHY_MODE(Enum):
    PHY_MODE_CUSTOM_SERDES = 0x9


class ENUM_PHY_LINK_RATE(Enum):
    PHY_LINK_RATE_RATE_PROGRAMMED_THROUGH_MESSAGE_BUS = 0xF


class ENUM_SOC_PHY_READY(Enum):
    SOC_PHY_READY_NOT_READY = 0x0
    SOC_PHY_READY_READY = 0x1


class OFFSET_PORT_BUF_CTL1:
    PORT_BUF_CTL1_USBC1 = 0x16F200
    PORT_BUF_CTL1_USBC2 = 0x16F400
    PORT_BUF_CTL1_USBC3 = 0x16F600
    PORT_BUF_CTL1_USBC4 = 0x16F800
    PORT_BUF_CTL1_A = 0x16FA00
    PORT_BUF_CTL1_B = 0x16FC00

class _PORT_BUF_CTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HdmiFrlShifterEnable', ctypes.c_uint32, 1),
        ('PortWidth', ctypes.c_uint32, 3),
        ('TcssPowerState', ctypes.c_uint32, 1),
        ('TcssPowerRequest', ctypes.c_uint32, 1),
        ('TypecPhyOwnership', ctypes.c_uint32, 1),
        ('IdleStatus', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 3),
        ('IoSelect', ctypes.c_uint32, 1),
        ('PhyMode', ctypes.c_uint32, 4),
        ('PortReversal', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 1),
        ('DataWidth', ctypes.c_uint32, 2),
        ('PhyLinkRate', ctypes.c_uint32, 4),
        ('SocPhyReady', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 3),
        ('Reserved28', ctypes.c_uint32, 2),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PORT_BUF_CTL1(ctypes.Union):
    value = 0
    offset = 0

    HdmiFrlShifterEnable = 0  # bit 0 to 0
    PortWidth = 0  # bit 1 to 3
    TcssPowerState = 0  # bit 4 to 4
    TcssPowerRequest = 0  # bit 5 to 5
    TypecPhyOwnership = 0  # bit 6 to 6
    IdleStatus = 0  # bit 7 to 7
    Reserved8 = 0  # bit 8 to 10
    IoSelect = 0  # bit 11 to 11
    PhyMode = 0  # bit 12 to 15
    PortReversal = 0  # bit 16 to 16
    Reserved17 = 0  # bit 17 to 17
    DataWidth = 0  # bit 18 to 19
    PhyLinkRate = 0  # bit 20 to 23
    SocPhyReady = 0  # bit 24 to 24
    Reserved25 = 0  # bit 25 to 27
    Reserved28 = 0  # bit 28 to 29
    Reserved30 = 0  # bit 30 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_BUF_CTL1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_BUF_CTL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_POWER_STATE_IN_READY(Enum):
    POWER_STATE_IN_READY_P2 = 0x2


class ENUM_LANE1_POWERDOWN_NEW_STATE(Enum):
    LANE1_POWERDOWN_NEW_STATE_P2 = 0x2


class ENUM_LANE0_POWERDOWN_NEW_STATE(Enum):
    LANE0_POWERDOWN_NEW_STATE_P2 = 0x2


class ENUM_LANE1_POWERDOWN_UPDATE(Enum):
    LANE1_POWERDOWN_UPDATE_NO_UPDATE = 0x0
    LANE1_POWERDOWN_UPDATE_UPDATED = 0x1


class ENUM_LANE0_POWERDOWN_UPDATE(Enum):
    LANE0_POWERDOWN_UPDATE_NO_UPDATE = 0x0
    LANE0_POWERDOWN_UPDATE_UPDATED = 0x1


class ENUM_LANE1_PHY_PULSE_STATUS(Enum):
    LANE1_PHY_PULSE_STATUS_NO_PULSE = 0x0
    LANE1_PHY_PULSE_STATUS_PULSED = 0x1


class ENUM_LANE0_PHY_PULSE_STATUS(Enum):
    LANE0_PHY_PULSE_STATUS_NO_PULSE = 0x0
    LANE0_PHY_PULSE_STATUS_PULSED = 0x1


class ENUM_LANE1_PHY_CURRENT_STATUS(Enum):
    LANE1_PHY_CURRENT_STATUS_0 = 0x0
    LANE1_PHY_CURRENT_STATUS_1 = 0x1


class ENUM_LANE0_PHY_CURRENT_STATUS(Enum):
    LANE0_PHY_CURRENT_STATUS_0 = 0x0
    LANE0_PHY_CURRENT_STATUS_1 = 0x1


class ENUM_LANE1_PIPE_RESET(Enum):
    LANE1_PIPE_RESET_RESET = 0x1
    LANE1_PIPE_RESET_OUT_OF_RESET = 0x0


class ENUM_LANE0_PIPE_RESET(Enum):
    LANE0_PIPE_RESET_RESET = 0x1
    LANE0_PIPE_RESET_OUT_OF_RESET = 0x0


class OFFSET_PORT_BUF_CTL2:
    PORT_BUF_CTL2_USBC1 = 0x16F204
    PORT_BUF_CTL2_USBC2 = 0x16F404
    PORT_BUF_CTL2_USBC3 = 0x16F604
    PORT_BUF_CTL2_USBC4 = 0x16F804
    PORT_BUF_CTL2_A = 0x16FA04
    PORT_BUF_CTL2_B = 0x16FC04

class _PORT_BUF_CTL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 4),
        ('PowerStateInReady', ctypes.c_uint32, 4),
        ('Lane1PowerdownCurrentState', ctypes.c_uint32, 4),
        ('Lane0PowerdownCurrentState', ctypes.c_uint32, 4),
        ('Lane1PowerdownNewState', ctypes.c_uint32, 4),
        ('Lane0PowerdownNewState', ctypes.c_uint32, 4),
        ('Lane1PowerdownUpdate', ctypes.c_uint32, 1),
        ('Lane0PowerdownUpdate', ctypes.c_uint32, 1),
        ('Lane1PhyPulseStatus', ctypes.c_uint32, 1),
        ('Lane0PhyPulseStatus', ctypes.c_uint32, 1),
        ('Lane1PhyCurrentStatus', ctypes.c_uint32, 1),
        ('Lane0PhyCurrentStatus', ctypes.c_uint32, 1),
        ('Lane1PipeReset', ctypes.c_uint32, 1),
        ('Lane0PipeReset', ctypes.c_uint32, 1),
    ]


class REG_PORT_BUF_CTL2(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 3
    PowerStateInReady = 0  # bit 4 to 7
    Lane1PowerdownCurrentState = 0  # bit 8 to 11
    Lane0PowerdownCurrentState = 0  # bit 12 to 15
    Lane1PowerdownNewState = 0  # bit 16 to 19
    Lane0PowerdownNewState = 0  # bit 20 to 23
    Lane1PowerdownUpdate = 0  # bit 24 to 24
    Lane0PowerdownUpdate = 0  # bit 25 to 25
    Lane1PhyPulseStatus = 0  # bit 26 to 26
    Lane0PhyPulseStatus = 0  # bit 27 to 27
    Lane1PhyCurrentStatus = 0  # bit 28 to 28
    Lane0PhyCurrentStatus = 0  # bit 29 to 29
    Lane1PipeReset = 0  # bit 30 to 30
    Lane0PipeReset = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_BUF_CTL2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_BUF_CTL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_POWER_STATE_IN_ACTIVE(Enum):
    POWER_STATE_IN_ACTIVE_P0 = 0x0


class ENUM_PLL_LANE_STAGGERING_DELAY(Enum):
    PLL_LANE_STAGGERING_DELAY_0 = 0x0  # No delay
    PLL_LANE_STAGGERING_DELAY_128 = 0x80  # 158ns for HBR3. 790ns for RBR.


class ENUM_DC5_DEFAULT_MAXPCLKREQ(Enum):
    DC5_DEFAULT_MAXPCLKREQ_PLL_OFF = 0x0


class ENUM_DC5_DEFAULT_POWERSTATE(Enum):
    DC5_DEFAULT_POWERSTATE_P2_PG = 0x9


class ENUM_REFCLK_LANE_STAGGERING_DELAY(Enum):
    REFCLK_LANE_STAGGERING_DELAY_0 = 0x0  # No delay
    REFCLK_LANE_STAGGERING_DELAY_MAX = 0x8  # 208ns for 38.4 reference.


class OFFSET_PORT_BUF_CTL3:
    PORT_BUF_CTL3_USBC1 = 0x16F208
    PORT_BUF_CTL3_USBC2 = 0x16F408
    PORT_BUF_CTL3_USBC3 = 0x16F608
    PORT_BUF_CTL3_USBC4 = 0x16F808
    PORT_BUF_CTL3_A = 0x16FA08
    PORT_BUF_CTL3_B = 0x16FC08

class _PORT_BUF_CTL3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PowerStateInActive', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 4),
        ('PllLaneStaggeringDelay', ctypes.c_uint32, 8),
        ('Reserved16', ctypes.c_uint32, 2),
        ('Dc5DefaultMaxpclkreq', ctypes.c_uint32, 2),
        ('Dc5DefaultPowerstate', ctypes.c_uint32, 4),
        ('RefclkLaneStaggeringDelay', ctypes.c_uint32, 8),
    ]


class REG_PORT_BUF_CTL3(ctypes.Union):
    value = 0
    offset = 0

    PowerStateInActive = 0  # bit 0 to 3
    Reserved4 = 0  # bit 4 to 7
    PllLaneStaggeringDelay = 0  # bit 8 to 15
    Reserved16 = 0  # bit 16 to 17
    Dc5DefaultMaxpclkreq = 0  # bit 18 to 19
    Dc5DefaultPowerstate = 0  # bit 20 to 23
    RefclkLaneStaggeringDelay = 0  # bit 24 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_BUF_CTL3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_BUF_CTL3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_BUF_CTL4:
    PORT_BUF_CTL4_USBC1 = 0x16F20C
    PORT_BUF_CTL4_USBC2 = 0x16F40C
    PORT_BUF_CTL4_USBC3 = 0x16F60C
    PORT_BUF_CTL4_USBC4 = 0x16F80C
    PORT_BUF_CTL4_A = 0x16FA0C
    PORT_BUF_CTL4_B = 0x16FC0C

class _PORT_BUF_CTL4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LanePowerdownFsmTimeoutInRefclkCycles', ctypes.c_uint32, 14),
        ('Lane1PowerdownFsmTimedOut', ctypes.c_uint32, 1),
        ('Lane1PowerdownReset', ctypes.c_uint32, 1),
        ('LanePowerdownFsmTimeoutInPclkCycles', ctypes.c_uint32, 14),
        ('Lane0PowerdownFsmTimedOut', ctypes.c_uint32, 1),
        ('Lane0PowerdownReset', ctypes.c_uint32, 1),
    ]


class REG_PORT_BUF_CTL4(ctypes.Union):
    value = 0
    offset = 0

    LanePowerdownFsmTimeoutInRefclkCycles = 0  # bit 0 to 13
    Lane1PowerdownFsmTimedOut = 0  # bit 14 to 14
    Lane1PowerdownReset = 0  # bit 15 to 15
    LanePowerdownFsmTimeoutInPclkCycles = 0  # bit 16 to 29
    Lane0PowerdownFsmTimedOut = 0  # bit 30 to 30
    Lane0PowerdownReset = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_BUF_CTL4),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_BUF_CTL4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_LFPS_PHASE_FSM_PRESENT_STATE(Enum):
    LFPS_PHASE_FSM_PRESENT_STATE_ST_PH0 = 0x0
    LFPS_PHASE_FSM_PRESENT_STATE_ST_PH1 = 0x1


class ENUM_SEQUENCE_TRACKING_FSM_PRESENT_STATE(Enum):
    SEQUENCE_TRACKING_FSM_PRESENT_STATE_ST_LINK_ON = 0x0
    SEQUENCE_TRACKING_FSM_PRESENT_STATE_ST_LINK_OFF = 0x1
    SEQUENCE_TRACKING_FSM_PRESENT_STATE_ST_PHY_SWING_SETUP = 0x2
    SEQUENCE_TRACKING_FSM_PRESENT_STATE_ST_LFPS_TX = 0x3
    SEQUENCE_TRACKING_FSM_PRESENT_STATE_ST_PHY_SWING_HOLD = 0x4
    SEQUENCE_TRACKING_FSM_PRESENT_STATE_ST_SILENCE = 0x5


class OFFSET_PORT_SLICE_EDP_DBG:
    PORT_SLICE_EDP_DBG_A = 0x16FA90
    PORT_SLICE_EDP_DBG_B = 0x16FC90

class _PORT_SLICE_EDP_DBG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LfpsPhaseFsmPresentState', ctypes.c_uint32, 1),
        ('SequenceTrackingFsmPresentState', ctypes.c_uint32, 3),
        ('Reserved4', ctypes.c_uint32, 28),
    ]


class REG_PORT_SLICE_EDP_DBG(ctypes.Union):
    value = 0
    offset = 0

    LfpsPhaseFsmPresentState = 0  # bit 0 to 0
    SequenceTrackingFsmPresentState = 0  # bit 1 to 3
    Reserved4 = 0  # bit 4 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_SLICE_EDP_DBG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_SLICE_EDP_DBG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CONFIG_BUS_STATE(Enum):
    CONFIG_BUS_STATE_IDLE = 0x0
    CONFIG_BUS_STATE_ACTION = 0x1
    CONFIG_BUS_STATE_GRANT = 0x2
    CONFIG_BUS_STATE_RESETPREP = 0x3


class ENUM_ABORT_DETECTED(Enum):
    ABORT_DETECTED_NO_ABORTED_TRANSACTION = 0x0
    ABORT_DETECTED_TRANSACTION_ABORTED = 0x1


class ENUM_TRANSACTION_FINISHED(Enum):
    TRANSACTION_FINISHED_NO_FINISHED_TRANSACTION = 0x0
    TRANSACTION_FINISHED_TRANSACTION_FINISHED = 0x1


class ENUM_ABORT_TRANSACTION(Enum):
    ABORT_TRANSACTION_DO_NOT_ABORT = 0x0
    ABORT_TRANSACTION_ABORT = 0x1


class OFFSET_PORT_CFGBUS_STATUS:
    PORT_CFGBUS_STATUS_A = 0x16FAC8
    PORT_CFGBUS_STATUS_B = 0x16FCC8

class _PORT_CFGBUS_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 17),
        ('ConfigBusState', ctypes.c_uint32, 3),
        ('Reserved20', ctypes.c_uint32, 2),
        ('AbortDetected', ctypes.c_uint32, 1),
        ('TransactionFinished', ctypes.c_uint32, 1),
        ('ConfigBusData', ctypes.c_uint32, 4),
        ('Reserved28', ctypes.c_uint32, 1),
        ('ConfigBusGrant', ctypes.c_uint32, 1),
        ('ConfigBusRequest', ctypes.c_uint32, 1),
        ('AbortTransaction', ctypes.c_uint32, 1),
    ]


class REG_PORT_CFGBUS_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 16
    ConfigBusState = 0  # bit 17 to 19
    Reserved20 = 0  # bit 20 to 21
    AbortDetected = 0  # bit 22 to 22
    TransactionFinished = 0  # bit 23 to 23
    ConfigBusData = 0  # bit 24 to 27
    Reserved28 = 0  # bit 28 to 28
    ConfigBusGrant = 0  # bit 29 to 29
    ConfigBusRequest = 0  # bit 30 to 30
    AbortTransaction = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CFGBUS_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CFGBUS_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DDI_CLK_VALFREQ:
    DDI_CLK_VALFREQ_A = 0x64030
    DDI_CLK_VALFREQ_B = 0x64130
    DDI_CLK_VALFREQ_USBC1 = 0x64330
    DDI_CLK_VALFREQ_USBC2 = 0x64430
    DDI_CLK_VALFREQ_USBC3 = 0x64530
    DDI_CLK_VALFREQ_USBC4 = 0x64630

class _DDI_CLK_VALFREQ(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DdiValidationFrequency', ctypes.c_uint32, 32),
    ]


class REG_DDI_CLK_VALFREQ(ctypes.Union):
    value = 0
    offset = 0

    DdiValidationFrequency = 0  # bit 0 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_CLK_VALFREQ),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_CLK_VALFREQ, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0(Enum):
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_NO_PIN_ASSIGNMENT_FOR_NON_TYPEC_STATIC_FIXED_LEGACY_CONNECTIONS = 0x0
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C = 0x3
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_D = 0x4
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_E = 0x5


class OFFSET_PORT_TX_DFLEXPA1:
    PORT_TX_DFLEXPA1_FIA1 = 0x163880
    PORT_TX_DFLEXPA1_FIA2 = 0x16E880

class _PORT_TX_DFLEXPA1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayportPinAssignmentForTypeCConnector0', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector1', ctypes.c_uint32, 4),
        ('Reserved8', ctypes.c_uint32, 24),
    ]


class REG_PORT_TX_DFLEXPA1(ctypes.Union):
    value = 0
    offset = 0

    DisplayportPinAssignmentForTypeCConnector0 = 0  # bit 0 to 3
    DisplayportPinAssignmentForTypeCConnector1 = 0  # bit 4 to 7
    Reserved8 = 0  # bit 8 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXPA1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXPA1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HIP_INDEX_REG0:
    HIP_INDEX_REG0 = 0x1010A0

class _HIP_INDEX_REG0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hip_168_Index', ctypes.c_uint32, 8),
        ('Hip_169_Index', ctypes.c_uint32, 8),
        ('Hip_16A_Index', ctypes.c_uint32, 8),
        ('Hip_16B_Index', ctypes.c_uint32, 8),
    ]


class REG_HIP_INDEX_REG0(ctypes.Union):
    value = 0
    offset = 0

    Hip_168_Index = 0  # bit 0 to 7
    Hip_169_Index = 0  # bit 8 to 15
    Hip_16A_Index = 0  # bit 16 to 23
    Hip_16B_Index = 0  # bit 24 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HIP_INDEX_REG0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HIP_INDEX_REG0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_HIP_INDEX_REG1:
    HIP_INDEX_REG1 = 0x1010A4

class _HIP_INDEX_REG1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hip_16C_Index', ctypes.c_uint32, 8),
        ('Hip_16D_Index', ctypes.c_uint32, 8),
        ('Hip_16E_Index', ctypes.c_uint32, 8),
        ('Hip_16F_Index', ctypes.c_uint32, 8),
    ]


class REG_HIP_INDEX_REG1(ctypes.Union):
    value = 0
    offset = 0

    Hip_16C_Index = 0  # bit 0 to 7
    Hip_16D_Index = 0  # bit 8 to 15
    Hip_16E_Index = 0  # bit 16 to 23
    Hip_16F_Index = 0  # bit 24 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _HIP_INDEX_REG1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_HIP_INDEX_REG1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_COMMAND_TYPE(Enum):
    COMMAND_TYPE_WRITE_UNCOMMITTED = 0x1  # Current write is saved off into a write buffer and its associated data valu
                                          # es are updated into the relevant PIPE register at a future time when a
                                          # write committed is received.
    COMMAND_TYPE_WRITE_COMMITTED = 0x2  # Current write as well as any previously uncommitted writes saved into the wri
                                        # te buffer should be cmmitted. Wait for write ack before sending a new write,
                                        # committed or uncommitted.
    COMMAND_TYPE_READ = 0x3  # Used to read contents of a PIPE register. Only one read can be outstanding at a time in 
                             # each direction.


class ENUM_TRANSACTION_PENDING(Enum):
    TRANSACTION_PENDING_NO_PENDING_TRANSACTION = 0x0  # For a write commit command type, HW clears this bit to '0' afte
                                                      # r receiving transaction completed notification from PHY. For a
                                                      # write uncommit command type, HW clears this bit to '0' without
                                                      # waiting for transaction completed notification from PHY.
    TRANSACTION_PENDING_PENDING_TRANSACTION = 0x1  # This bit when set indicates a pending message bus transaction. Onl
                                                   # y SW can set this bit indicating a new transaction.


class OFFSET_PORT_M2P_MSGBUS_CTL:
    PORT_M2P_MSGBUS_CTL_LN0_USBC1 = 0x16F240
    PORT_M2P_MSGBUS_CTL_LN1_USBC1 = 0x16F244
    PORT_M2P_MSGBUS_CTL_LN0_USBC2 = 0x16F440
    PORT_M2P_MSGBUS_CTL_LN1_USBC2 = 0x16F444
    PORT_M2P_MSGBUS_CTL_LN0_USBC3 = 0x16F640
    PORT_M2P_MSGBUS_CTL_LN1_USBC3 = 0x16F644
    PORT_M2P_MSGBUS_CTL_LN0_USBC4 = 0x16F840
    PORT_M2P_MSGBUS_CTL_LN1_USBC4 = 0x16F844
    PORT_M2P_MSGBUS_CTL_LN0_A = 0x16FA40
    PORT_M2P_MSGBUS_CTL_LN1_A = 0x16FA44
    PORT_M2P_MSGBUS_CTL_LN0_B = 0x16FC40
    PORT_M2P_MSGBUS_CTL_LN1_B = 0x16FC44

class _PORT_M2P_MSGBUS_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Address', ctypes.c_uint32, 12),
        ('Reserved12', ctypes.c_uint32, 3),
        ('ResetMessageBus', ctypes.c_uint32, 1),
        ('Data', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 3),
        ('CommandType', ctypes.c_uint32, 4),
        ('TransactionPending', ctypes.c_uint32, 1),
    ]


class REG_PORT_M2P_MSGBUS_CTL(ctypes.Union):
    value = 0
    offset = 0

    Address = 0  # bit 0 to 11
    Reserved12 = 0  # bit 12 to 14
    ResetMessageBus = 0  # bit 15 to 15
    Data = 0  # bit 16 to 23
    Reserved24 = 0  # bit 24 to 26
    CommandType = 0  # bit 27 to 30
    TransactionPending = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_M2P_MSGBUS_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_M2P_MSGBUS_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ERROR_SET(Enum):
    ERROR_SET_ERROR_NOT_SET = 0x0
    ERROR_SET_ERROR_SET = 0x1


class ENUM_RESPONSE_READY(Enum):
    RESPONSE_READY_NO_RESPONSE_PENDING = 0x0
    RESPONSE_READY_RESPONSE_PENDING = 0x1


class OFFSET_PORT_P2M_MSGBUS_STATUS:
    PORT_P2M_MSGBUS_STATUS_LN0_USBC1 = 0x16F248
    PORT_P2M_MSGBUS_STATUS_LN1_USBC1 = 0x16F24C
    PORT_P2M_MSGBUS_STATUS_LN0_USBC2 = 0x16F448
    PORT_P2M_MSGBUS_STATUS_LN1_USBC2 = 0x16F44C
    PORT_P2M_MSGBUS_STATUS_LN0_USBC3 = 0x16F648
    PORT_P2M_MSGBUS_STATUS_LN1_USBC3 = 0x16F64C
    PORT_P2M_MSGBUS_STATUS_LN0_USBC4 = 0x16F848
    PORT_P2M_MSGBUS_STATUS_LN1_USBC4 = 0x16F84C
    PORT_P2M_MSGBUS_STATUS_LN0_A = 0x16FA48
    PORT_P2M_MSGBUS_STATUS_LN1_A = 0x16FA4C
    PORT_P2M_MSGBUS_STATUS_LN0_B = 0x16FC48
    PORT_P2M_MSGBUS_STATUS_LN1_B = 0x16FC4C

class _PORT_P2M_MSGBUS_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 15),
        ('ErrorSet', ctypes.c_uint32, 1),
        ('Data', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 3),
        ('CommandType', ctypes.c_uint32, 4),
        ('ResponseReady', ctypes.c_uint32, 1),
    ]


class REG_PORT_P2M_MSGBUS_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 14
    ErrorSet = 0  # bit 15 to 15
    Data = 0  # bit 16 to 23
    Reserved24 = 0  # bit 24 to 26
    CommandType = 0  # bit 27 to 30
    ResponseReady = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_P2M_MSGBUS_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_P2M_MSGBUS_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_MSGBUS_STATUS:
    PORT_MSGBUS_STATUS_LN0_USBC1 = 0x16F250
    PORT_MSGBUS_STATUS_LN1_USBC1 = 0x16F254
    PORT_MSGBUS_STATUS_LN0_USBC2 = 0x16F450
    PORT_MSGBUS_STATUS_LN1_USBC2 = 0x16F454
    PORT_MSGBUS_STATUS_LN0_USBC3 = 0x16F650
    PORT_MSGBUS_STATUS_LN1_USBC3 = 0x16F654
    PORT_MSGBUS_STATUS_LN0_USBC4 = 0x16F850
    PORT_MSGBUS_STATUS_LN1_USBC4 = 0x16F854
    PORT_MSGBUS_STATUS_LN0_A = 0x16FA50
    PORT_MSGBUS_STATUS_LN1_A = 0x16FA54
    PORT_MSGBUS_STATUS_LN0_B = 0x16FC50
    PORT_MSGBUS_STATUS_LN1_B = 0x16FC54

class _PORT_MSGBUS_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MessageBusFsmStatus', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 28),
    ]


class REG_PORT_MSGBUS_STATUS(ctypes.Union):
    value = 0
    offset = 0

    MessageBusFsmStatus = 0  # bit 0 to 3
    Reserved4 = 0  # bit 4 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_MSGBUS_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_MSGBUS_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_MSGBUS_TIMER:
    PORT_MSGBUS_TIMER_LN0_USBC1 = 0x16F258
    PORT_MSGBUS_TIMER_LN1_USBC1 = 0x16F25C
    PORT_MSGBUS_TIMER_LN0_USBC2 = 0x16F458
    PORT_MSGBUS_TIMER_LN1_USBC2 = 0x16F45C
    PORT_MSGBUS_TIMER_LN0_USBC3 = 0x16F658
    PORT_MSGBUS_TIMER_LN1_USBC3 = 0x16F65C
    PORT_MSGBUS_TIMER_LN0_USBC4 = 0x16F858
    PORT_MSGBUS_TIMER_LN1_USBC4 = 0x16F85C
    PORT_MSGBUS_TIMER_LN0_A = 0x16FA58
    PORT_MSGBUS_TIMER_LN1_A = 0x16FA5C
    PORT_MSGBUS_TIMER_LN0_B = 0x16FC58
    PORT_MSGBUS_TIMER_LN1_B = 0x16FC5C

class _PORT_MSGBUS_TIMER(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MessageBusTimer', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 7),
        ('MessageBusTimedOut', ctypes.c_uint32, 1),
    ]


class REG_PORT_MSGBUS_TIMER(ctypes.Union):
    value = 0
    offset = 0

    MessageBusTimer = 0  # bit 0 to 23
    Reserved24 = 0  # bit 24 to 30
    MessageBusTimedOut = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_MSGBUS_TIMER),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_MSGBUS_TIMER, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ACCUM_ENABLE(Enum):
    ACCUM_DISABLE = 0x0
    ACCUM_ENABLE = 0x1


class ENUM_CRC_CHANNEL_MASK(Enum):
    CRC_CHANNEL_MASK_ALL_CHANNELS_UNMASKED = 0x0
    CRC_CHANNEL_MASK_MASK_CHANNEL_0 = 0x0
    CRC_CHANNEL_MASK_UNMASK_CHANNEL_0 = 0x0
    CRC_CHANNEL_MASK_MASK_CHANNEL_1 = 0x0
    CRC_CHANNEL_MASK_UNMASK_CHANNEL_1 = 0x0
    CRC_CHANNEL_MASK_MASK_CHANNEL_2 = 0x0
    CRC_CHANNEL_MASK_UNMASK_CHANNEL_2 = 0x0
    CRC_CHANNEL_MASK_MASK_CHANNEL_3 = 0x0
    CRC_CHANNEL_MASK_UNMASK_CHANNEL_3 = 0x0


class ENUM_CRC_INPUT_INSUFFICIENT(Enum):
    CRC_INPUT_INSUFFICIENT_SUFFICIENT = 0x0
    CRC_INPUT_INSUFFICIENT_INSUFFICIENT = 0x1


class ENUM_CRC_DONE(Enum):
    CRC_DONE_NOT_DONE = 0x0
    CRC_DONE_DONE = 0x1


class ENUM_CRC_CHANGE(Enum):
    CRC_CHANGE_NO_CHANGE = 0x0
    CRC_CHANGE_CHANGE = 0x1


class ENUM_ENABLE_CRC(Enum):
    ENABLE_CRC_DISABLE = 0x0
    ENABLE_CRC_ENABLE = 0x1


class OFFSET_DDI_CRC_CTL:
    DDI_CRC_CTL_A = 0x64050
    DDI_CRC_CTL_B = 0x64150
    DDI_CRC_CTL_USBC1 = 0x64350
    DDI_CRC_CTL_USBC2 = 0x64450
    DDI_CRC_CTL_USBC3 = 0x64550
    DDI_CRC_CTL_USBC4 = 0x64650

class _DDI_CRC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AccumStartFrame', ctypes.c_uint32, 4),
        ('AccumEndFrame', ctypes.c_uint32, 4),
        ('AccumEnable', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 7),
        ('CrcChannelMask', ctypes.c_uint32, 4),
        ('Reserved20', ctypes.c_uint32, 3),
        ('CrcInputInsufficient', ctypes.c_uint32, 1),
        ('CrcDone', ctypes.c_uint32, 1),
        ('CrcChange', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 5),
        ('EnableCrc', ctypes.c_uint32, 1),
    ]


class REG_DDI_CRC_CTL(ctypes.Union):
    value = 0
    offset = 0

    AccumStartFrame = 0  # bit 0 to 3
    AccumEndFrame = 0  # bit 4 to 7
    AccumEnable = 0  # bit 8 to 8
    Reserved9 = 0  # bit 9 to 15
    CrcChannelMask = 0  # bit 16 to 19
    Reserved20 = 0  # bit 20 to 22
    CrcInputInsufficient = 0  # bit 23 to 23
    CrcDone = 0  # bit 24 to 24
    CrcChange = 0  # bit 25 to 25
    Reserved26 = 0  # bit 26 to 30
    EnableCrc = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_CRC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_CRC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

