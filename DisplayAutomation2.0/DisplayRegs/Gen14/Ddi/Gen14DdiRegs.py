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
# @file Gen14DdiRegs.py
# @brief contains Gen14DdiRegs.py related register definitions

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

    Hpd_Live_Status_Alt = 0  # bit 0 to 1
    Hpd_Live_Status_Tbt = 0  # bit 1 to 2
    Ready = 0  # bit 2 to 3
    Sss = 0  # bit 3 to 4
    Src_Port_Num = 0  # bit 4 to 8
    Hpd_In_Progress = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 32

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
        ('Reserved20', ctypes.c_uint32, 11),
        ('Enable', ctypes.c_uint32, 1),
    ]


class REG_DDI_CTL_DE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    PortWidth = 0  # bit 1 to 4
    Reserved4 = 0  # bit 4 to 6
    BypassIdleStatus = 0  # bit 6 to 7
    IdleStatus = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 16
    PortReversal = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 18
    DataWidth = 0  # bit 18 to 20
    Reserved20 = 0  # bit 20 to 31
    Enable = 0  # bit 31 to 32

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


class ENUM_SYNC_PULSE_COUNT(Enum):
    SYNC_PULSE_COUNT_32_PULSES = 0x1F


class ENUM_FAST_WAKE_SYNC_PULSE_COUNT(Enum):
    FAST_WAKE_SYNC_PULSE_COUNT_18_PULSES = 0x11


class ENUM_IO_SELECT(Enum):
    IO_SELECT_TBT = 0x1  # Use Thunderbolt IO
    IO_SELECT_NON_TBT = 0x0  # Use non-thunderbolt (legacy) IO.This is used for typeC ports in DP-alternate or native/
    # fixed/legacy mode or for non-typeC ports.


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
    PORT_AUX_CTL_A = 0x64010
    PORT_AUX_CTL_B = 0x64110
    PORT_AUX_CTL_USBC1 = 0x16F210
    PORT_AUX_CTL_USBC2 = 0x16F410
    PORT_AUX_CTL_USBC3 = 0x16F610
    PORT_AUX_CTL_USBC4 = 0x16F810


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

    SyncPulseCount = 0  # bit 0 to 5
    FastWakeSyncPulseCount = 0  # bit 5 to 10
    Reserved10 = 0  # bit 10 to 11
    IoSelect = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 13
    AuxFrameSyncDataSelect = 0  # bit 13 to 14
    AuxPsrDataSelect = 0  # bit 14 to 15
    AuxAksvSelect = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 18
    PhyPowerState = 0  # bit 18 to 19
    PhyPowerRequest = 0  # bit 19 to 20
    MessageSize = 0  # bit 20 to 25
    ReceiveError = 0  # bit 25 to 26
    TimeOutTimerValue = 0  # bit 26 to 28
    TimeOutError = 0  # bit 28 to 29
    InterruptOnDone = 0  # bit 29 to 30
    Done = 0  # bit 30 to 31
    SendBusy = 0  # bit 31 to 32

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
    PORT_AUX_DATA_0_A = 0x64014
    PORT_AUX_DATA_1_A = 0x64018
    PORT_AUX_DATA_2_A = 0x6401C
    PORT_AUX_DATA_3_A = 0x64020
    PORT_AUX_DATA_4_A = 0x64024
    PORT_AUX_DATA_0_B = 0x64114
    PORT_AUX_DATA_1_B = 0x64118
    PORT_AUX_DATA_2_B = 0x6411C
    PORT_AUX_DATA_3_B = 0x64120
    PORT_AUX_DATA_4_B = 0x64124
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


class _PORT_AUX_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AuxChData', ctypes.c_uint32, 32),
    ]


class REG_PORT_AUX_DATA(ctypes.Union):
    value = 0
    offset = 0

    AuxChData = 0  # bit 0 to 32

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

    SbFrequencyDecimal = 0  # bit 0 to 11
    Reserved11 = 0  # bit 11 to 32

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


class ENUM_D2D_LINK_STATE(Enum):
    D2D_LINK_STATE_DISABLED = 0x0
    D2D_LINK_STATE_ENABLED = 0x1


class ENUM_D2D_LINK_ENABLE(Enum):
    D2D_LINK_DISABLE = 0x0
    D2D_LINK_ENABLE = 0x1


class OFFSET_PORT_BUF_CTL1:
    PORT_BUF_CTL1_A = 0x64004
    PORT_BUF_CTL1_B = 0x64104
    PORT_BUF_CTL1_USBC1 = 0x16F200
    PORT_BUF_CTL1_USBC2 = 0x16F400
    PORT_BUF_CTL1_USBC3 = 0x16F600
    PORT_BUF_CTL1_USBC4 = 0x16F800


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
        ('D2DLinkState', ctypes.c_uint32, 1),
        ('D2DLinkEnable', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PORT_BUF_CTL1(ctypes.Union):
    value = 0
    offset = 0

    HdmiFrlShifterEnable = 0  # bit 0 to 1
    PortWidth = 0  # bit 1 to 4
    TcssPowerState = 0  # bit 4 to 5
    TcssPowerRequest = 0  # bit 5 to 6
    TypecPhyOwnership = 0  # bit 6 to 7
    IdleStatus = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 11
    IoSelect = 0  # bit 11 to 12
    PhyMode = 0  # bit 12 to 16
    PortReversal = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 18
    DataWidth = 0  # bit 18 to 20
    PhyLinkRate = 0  # bit 20 to 24
    SocPhyReady = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 28
    D2DLinkState = 0  # bit 28 to 29
    D2DLinkEnable = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

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
    PORT_BUF_CTL2_A = 0x64008
    PORT_BUF_CTL2_B = 0x64108
    PORT_BUF_CTL2_USBC1 = 0x16F204
    PORT_BUF_CTL2_USBC2 = 0x16F404
    PORT_BUF_CTL2_USBC3 = 0x16F604
    PORT_BUF_CTL2_USBC4 = 0x16F804


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

    Reserved0 = 0  # bit 0 to 4
    PowerStateInReady = 0  # bit 4 to 8
    Lane1PowerdownCurrentState = 0  # bit 8 to 12
    Lane0PowerdownCurrentState = 0  # bit 12 to 16
    Lane1PowerdownNewState = 0  # bit 16 to 20
    Lane0PowerdownNewState = 0  # bit 20 to 24
    Lane1PowerdownUpdate = 0  # bit 24 to 25
    Lane0PowerdownUpdate = 0  # bit 25 to 26
    Lane1PhyPulseStatus = 0  # bit 26 to 27
    Lane0PhyPulseStatus = 0  # bit 27 to 28
    Lane1PhyCurrentStatus = 0  # bit 28 to 29
    Lane0PhyCurrentStatus = 0  # bit 29 to 30
    Lane1PipeReset = 0  # bit 30 to 31
    Lane0PipeReset = 0  # bit 31 to 32

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


class ENUM_REFCLK_LANE_STAGGERING_DELAY(Enum):
    REFCLK_LANE_STAGGERING_DELAY_0 = 0x0  # No delay
    REFCLK_LANE_STAGGERING_DELAY_MAX = 0x8  # 208ns for 38.4 reference.


class OFFSET_PORT_BUF_CTL3:
    PORT_BUF_CTL3_A = 0x6400C
    PORT_BUF_CTL3_B = 0x6410C
    PORT_BUF_CTL3_USBC1 = 0x16F208
    PORT_BUF_CTL3_USBC2 = 0x16F408
    PORT_BUF_CTL3_USBC3 = 0x16F608
    PORT_BUF_CTL3_USBC4 = 0x16F808


class _PORT_BUF_CTL3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PowerStateInActive', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 4),
        ('PllLaneStaggeringDelay', ctypes.c_uint32, 8),
        ('Reserved16', ctypes.c_uint32, 8),
        ('RefclkLaneStaggeringDelay', ctypes.c_uint32, 8),
    ]


class REG_PORT_BUF_CTL3(ctypes.Union):
    value = 0
    offset = 0

    PowerStateInActive = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 8
    PllLaneStaggeringDelay = 0  # bit 8 to 16
    Reserved16 = 0  # bit 16 to 24
    RefclkLaneStaggeringDelay = 0  # bit 24 to 32

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

    DdiValidationFrequency = 0  # bit 0 to 32

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
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_NO_PIN_ASSIGNMENT_FOR_NON_TYPEC_DP = 0x0
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_A = 0x1
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_B = 0x2
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_C = 0x3
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_D = 0x4
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_E = 0x5
    DISPLAYPORT_PIN_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PIN_ASSIGNMENT_F = 0x6


class OFFSET_PORT_TX_DFLEXPA1:
    PORT_TX_DFLEXPA1_FIA1 = 0x163880
    PORT_TX_DFLEXPA1_FIA2 = 0x16E880


class _PORT_TX_DFLEXPA1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayportPinAssignmentForTypeCConnector0', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector1', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector2', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector3', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector4', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector5', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector6', ctypes.c_uint32, 4),
        ('DisplayportPinAssignmentForTypeCConnector7', ctypes.c_uint32, 4),
    ]


class REG_PORT_TX_DFLEXPA1(ctypes.Union):
    value = 0
    offset = 0

    DisplayportPinAssignmentForTypeCConnector0 = 0  # bit 0 to 4
    DisplayportPinAssignmentForTypeCConnector1 = 0  # bit 4 to 8
    DisplayportPinAssignmentForTypeCConnector2 = 0  # bit 8 to 12
    DisplayportPinAssignmentForTypeCConnector3 = 0  # bit 12 to 16
    DisplayportPinAssignmentForTypeCConnector4 = 0  # bit 16 to 20
    DisplayportPinAssignmentForTypeCConnector5 = 0  # bit 20 to 24
    DisplayportPinAssignmentForTypeCConnector6 = 0  # bit 24 to 28
    DisplayportPinAssignmentForTypeCConnector7 = 0  # bit 28 to 32

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


class ENUM_IOE_STEPPING(Enum):
    IOE_STEPPING_A_STEP = 0x0
    IOE_STEPPING_B_STEP = 0x1


class OFFSET_PORT_TX_DFLEXDPSP:
    PORT_TX_DFLEXDPSP_FIA1 = 0x1638A0
    PORT_TX_DFLEXDPSP_FIA2 = 0x16E8A0


class _PORT_TX_DFLEXDPSP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('IoeStepping', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_PORT_TX_DFLEXDPSP(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 11
    IoeStepping = 0  # bit 12
    Reserved13 = 0  # bit 13 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXDPSP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXDPSP, self).__init__()
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

    Hip_168_Index = 0  # bit 0 to 8
    Hip_169_Index = 0  # bit 8 to 16
    Hip_16A_Index = 0  # bit 16 to 24
    Hip_16B_Index = 0  # bit 24 to 32

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

    Hip_16C_Index = 0  # bit 0 to 8
    Hip_16D_Index = 0  # bit 8 to 16
    Hip_16E_Index = 0  # bit 16 to 24
    Hip_16F_Index = 0  # bit 24 to 32

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
