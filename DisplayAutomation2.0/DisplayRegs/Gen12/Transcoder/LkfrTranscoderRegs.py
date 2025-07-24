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
# @file LkfrTranscoderRegs.py
# @brief contains LkfrTranscoderRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_PORT_SYNC_MODE_MASTER_SELECT(Enum):
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_A = 0x1
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_B = 0x2
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_C = 0x3
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_D = 0x4


class ENUM_CMTG_SLAVE_MODE(Enum):
    CMTG_SLAVE_MODE_NOT_CMTG_SLAVE = 0x0
    CMTG_SLAVE_MODE_CMTG_SLAVE = 0x1


class ENUM_PORT_SYNC_MODE_ENABLE(Enum):
    PORT_SYNC_MODE_DISABLE = 0x0
    PORT_SYNC_MODE_ENABLE = 0x1


class ENUM_DUAL_PIPE_SYNC_ENABLE(Enum):
    DUAL_PIPE_SYNC_DISABLED = 0x0  # Both transcoders are being driven by a single Pipe (Dual Link - Single Pipe
                                          # )
    DUAL_PIPE_SYNC_ENABLED = 0x1  # Each transcoder is being driven by a separate Pipe (Dual Link - Dual Pipe)


class ENUM_AUDIO_MUTE_OVERRIDE(Enum):
    AUDIO_MUTE_OVERRIDE_OVERRIDE_AND_RESET = 0x2  # Override audio mute bit to '0'.
    AUDIO_MUTE_OVERRIDE_OVERRIDE_AND_SET = 0x3  # Override audio mute bit to '1'.


class ENUM_DOUBLE_BUFFER_VACTIVE(Enum):
    DOUBLE_BUFFER_VACTIVE_NORMAL_VACTIVE = 0x0
    DOUBLE_BUFFER_VACTIVE_DOUBLE_BUFFER_VACTIVE = 0x1


class ENUM_GENLOCK_MODE(Enum):
    GENLOCK_MODE_MASTER = 0x2  # Master transcoder outputs frame sync for other transcoders to slave to.
    GENLOCK_MODE_LOCAL_SLAVE = 0x0  # Local slave transcoder slaves to frame sync from a master transcoder in the same 
                                    # device. The master transcoder is selected by Port Sync Mode Master Select.
    GENLOCK_MODE_REMOTE_SLAVE = 0x1  # Remote slave transcoder slaves to frame sync from a master transcoder in a diffe
                                     # rent device.


class ENUM_GENLOCK_ENABLE(Enum):
    GENLOCK_ENABLE = 0x1
    GENLOCK_DISABLE = 0x0


class OFFSET_TRANS_DDI_FUNC_CTL2:
    TRANS_DDI_FUNC_CTL2_A = 0x60404
    TRANS_DDI_FUNC_CTL2_B = 0x61404
    TRANS_DDI_FUNC_CTL2_C = 0x62404
    TRANS_DDI_FUNC_CTL2_D = 0x63404
    TRANS_DDI_FUNC_CTL2_DSI0 = 0x6B404
    TRANS_DDI_FUNC_CTL2_DSI1 = 0x6BC04


class _TRANS_DDI_FUNC_CTL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PortSyncModeMasterSelect', ctypes.c_uint32, 3),
        ('CmtgSlaveMode', ctypes.c_uint32, 1),
        ('PortSyncModeEnable', ctypes.c_uint32, 1),
        ('DualPipeSyncEnable', ctypes.c_uint32, 1),
        ('AudioMuteOverride', ctypes.c_uint32, 2),
        ('DoubleBufferVactive', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 19),
        ('Reserved28', ctypes.c_uint32, 1),
        ('GenlockMode', ctypes.c_uint32, 2),
        ('GenlockEnable', ctypes.c_uint32, 1),
    ]


class REG_TRANS_DDI_FUNC_CTL2(ctypes.Union):
    value = 0
    offset = 0

    PortSyncModeMasterSelect = 0  # bit 0 to 3
    CmtgSlaveMode = 0  # bit 3 to 4
    PortSyncModeEnable = 0  # bit 4 to 5
    DualPipeSyncEnable = 0  # bit 5 to 6
    AudioMuteOverride = 0  # bit 6 to 8
    DoubleBufferVactive = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 28
    Reserved28 = 0  # bit 28 to 29
    GenlockMode = 0  # bit 29 to 31
    GenlockEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_DDI_FUNC_CTL2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_DDI_FUNC_CTL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DB_VACTIVE(Enum):
    DB_VACTIVE_DOUBLE_BUFFER_VACTIVE = 0x1
    DB_VACTIVE_NORMAL_VACTIVE = 0x0


class ENUM_HOLD_PLL_CONFIG(Enum):
    HOLD_PLL_CONFIG_LATCH_HOLD_CONFIG = 0x1
    HOLD_PLL_CONFIG_UNLATCH_RELEASE_CONFIG = 0x0


class ENUM_TE_MODE(Enum):
    TE_MODE_START_SYNC_ON_TE_FROM_DSI0 = 0x0
    TE_MODE_START_SYNC_ON_TE_FROM_DSI1 = 0x1
    TE_MODE_START_SYNC_ON_EITHER_DSI0_OR_DSI1 = 0x2


class ENUM_CMTG_MODE(Enum):
    CMTG_MODE_EDP_MODE = 0x0
    CMTG_MODE_MIPI_COMMAND_MODE = 0x1


class ENUM_CMTG_STATE(Enum):
    CMTG_STATE_DISABLED = 0x0
    CMTG_STATE_ENABLED = 0x1


class ENUM_CMTG_ENABLE(Enum):
    CMTG_DISABLE = 0x0
    CMTG_ENABLE = 0x1


class OFFSET_TRANS_CMTG_CTL:
    TRANS_CMTG_CTL_CMTG = 0x6FA88


class _TRANS_CMTG_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DbVactive', ctypes.c_uint32, 1),
        ('HoldPllConfig', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 11),
        ('TeMode', ctypes.c_uint32, 2),
        ('CmtgMode', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 7),
        ('CmtgState', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 6),
        ('Reserved30', ctypes.c_uint32, 1),
        ('CmtgEnable', ctypes.c_uint32, 1),
    ]


class REG_TRANS_CMTG_CTL(ctypes.Union):
    value = 0
    offset = 0

    DbVactive = 0  # bit 0 to 1
    HoldPllConfig = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 13
    TeMode = 0  # bit 13 to 15
    CmtgMode = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 23
    CmtgState = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 30
    Reserved30 = 0  # bit 30 to 31
    CmtgEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_CMTG_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_CMTG_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_CMTG_CHICKEN:
    TRANS_CMTG_CHICKEN_CMTG = 0x6FA90


class _TRANS_CMTG_CHICKEN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare0', ctypes.c_uint32, 1),
        ('Spare1', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 14),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_TRANS_CMTG_CHICKEN(ctypes.Union):
    value = 0
    offset = 0

    Spare0 = 0  # bit 0 to 1
    Spare1 = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_CMTG_CHICKEN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_CMTG_CHICKEN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_IDLE_FRAMES(Enum):
    IDLE_FRAMES_DEEP_SLEEP_DISABLED = 0x0
    IDLE_FRAMES_1_IDLE_FRAME = 0x1


class ENUM_FRAMES_BEFORE_SU_ENTRY(Enum):
    FRAMES_BEFORE_SU_ENTRY_1_FRAMES_BEFORE_SU_ENTRY = 0x1


class ENUM_TP2_TIME(Enum):
    TP2_TIME_500US = 0x0
    TP2_TIME_100US = 0x1
    TP2_TIME_2_5MS = 0x2
    TP2_TIME_50US = 0x3


class ENUM_FAST_WAKE(Enum):
    FAST_WAKE_5_LINES = 0x0
    FAST_WAKE_6_LINES = 0x1
    FAST_WAKE_7_LINES = 0x2
    FAST_WAKE_8_LINES = 0x3
    FAST_WAKE_9_LINES = 0x4
    FAST_WAKE_10_LINES = 0x5
    FAST_WAKE_11_LINES = 0x6
    FAST_WAKE_12_LINES = 0x7


class ENUM_IO_BUFFER_WAKE(Enum):
    IO_BUFFER_WAKE_5_LINES = 0x0
    IO_BUFFER_WAKE_6_LINES = 0x1
    IO_BUFFER_WAKE_7_LINES = 0x2
    IO_BUFFER_WAKE_8_LINES = 0x3
    IO_BUFFER_WAKE_9_LINES = 0x4
    IO_BUFFER_WAKE_10_LINES = 0x5
    IO_BUFFER_WAKE_11_LINES = 0x6
    IO_BUFFER_WAKE_12_LINES = 0x7


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


class ENUM_MAX_SU_DISABLE_TIME(Enum):
    MAX_SU_DISABLE_TIME_DISABLED = 0x0


class ENUM_AUX_FRAME_SYNC_ENABLE(Enum):
    AUX_FRAME_SYNC_ENABLE = 0x1
    AUX_FRAME_SYNC_DISABLE = 0x0


class ENUM_BLOCK_COUNT_NUMBER(Enum):
    BLOCK_COUNT_NUMBER_2_BLOCKS_OR_8_LINES = 0x0
    BLOCK_COUNT_NUMBER_3_BLOCKS_OR_12_LINES = 0x1


class ENUM_CONTEXT_RESTORE_TO_PSR2_DEEP_SLEEP_STATE(Enum):
    CONTEXT_RESTORE_TO_PSR2_DEEP_SLEEP_STATE_DISABLE = 0x0
    CONTEXT_RESTORE_TO_PSR2_DEEP_SLEEP_STATE_ENABLE = 0x1


class ENUM_PSR2_ENABLE(Enum):
    PSR2_DISABLE = 0x0
    PSR2_ENABLE = 0x1


class OFFSET_PSR2_CTL:
    PSR2_CTL_A = 0x60900
    PSR2_CTL_B = 0x61900


class _PSR2_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IdleFrames', ctypes.c_uint32, 4),
        ('FramesBeforeSuEntry', ctypes.c_uint32, 4),
        ('Tp2Time', ctypes.c_uint32, 2),
        ('FastWake', ctypes.c_uint32, 3),
        ('IoBufferWake', ctypes.c_uint32, 3),
        ('ErrorInjectionFlipBits', ctypes.c_uint32, 2),
        ('Psr2RamPowerState', ctypes.c_uint32, 1),
        ('EccErrorInjectionEnable', ctypes.c_uint32, 1),
        ('MaxSuDisableTime', ctypes.c_uint32, 5),
        ('Reserved25', ctypes.c_uint32, 2),
        ('AuxFrameSyncEnable', ctypes.c_uint32, 1),
        ('BlockCountNumber', ctypes.c_uint32, 1),
        ('ContextRestoreToPsr2DeepSleepState', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('Psr2Enable', ctypes.c_uint32, 1),
    ]


class REG_PSR2_CTL(ctypes.Union):
    value = 0
    offset = 0

    IdleFrames = 0  # bit 0 to 4
    FramesBeforeSuEntry = 0  # bit 4 to 8
    Tp2Time = 0  # bit 8 to 10
    FastWake = 0  # bit 10 to 13
    IoBufferWake = 0  # bit 13 to 16
    ErrorInjectionFlipBits = 0  # bit 16 to 18
    Psr2RamPowerState = 0  # bit 18 to 19
    EccErrorInjectionEnable = 0  # bit 19 to 20
    MaxSuDisableTime = 0  # bit 20 to 25
    Reserved25 = 0  # bit 25 to 27
    AuxFrameSyncEnable = 0  # bit 27 to 28
    BlockCountNumber = 0  # bit 28 to 29
    ContextRestoreToPsr2DeepSleepState = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 31
    Psr2Enable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR2_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR2_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE(Enum):
    ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE_NOT_ALLOWED = 0x0
    ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE_ALLOWED = 0x1


class ENUM_SF_PARTIAL_FRAME_ENABLE(Enum):
    SF_PARTIAL_FRAME_DISABLE = 0x0
    SF_PARTIAL_FRAME_ENABLE = 0x1


class ENUM_PSR2_MANUAL_TRACKING_ENABLE(Enum):
    PSR2_MANUAL_TRACKING_DISABLE = 0x0
    PSR2_MANUAL_TRACKING_ENABLE = 0x1


class OFFSET_PSR2_MAN_TRK_CTL:
    PSR2_MAN_TRK_CTL_A = 0x60910
    PSR2_MAN_TRK_CTL_B = 0x61910


class _PSR2_MAN_TRK_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AllowDoubleBufferUpdateDisable', ctypes.c_uint32, 1),
        ('SfPartialFrameEnable', ctypes.c_uint32, 1),
        ('SfContinuousFullFrame', ctypes.c_uint32, 1),
        ('SfSingleFullFrame', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 7),
        ('SuRegionEndAddress', ctypes.c_uint32, 10),
        ('SuRegionStartAddress', ctypes.c_uint32, 10),
        ('Psr2ManualTrackingEnable', ctypes.c_uint32, 1),
    ]


class REG_PSR2_MAN_TRK_CTL(ctypes.Union):
    value = 0
    offset = 0

    AllowDoubleBufferUpdateDisable = 0  # bit 0 to 1
    SfPartialFrameEnable = 0  # bit 1 to 2
    SfContinuousFullFrame = 0  # bit 2 to 3
    SfSingleFullFrame = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 11
    SuRegionEndAddress = 0  # bit 11 to 21
    SuRegionStartAddress = 0  # bit 21 to 31
    Psr2ManualTrackingEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR2_MAN_TRK_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR2_MAN_TRK_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_FRAMESYNC_RECEIVE_ERROR(Enum):
    FRAMESYNC_RECEIVE_ERROR_NO_ERROR = 0x0
    FRAMESYNC_RECEIVE_ERROR_ERROR = 0x1


class ENUM_FRAMESYNC_TIME_OUT_ERROR(Enum):
    FRAMESYNC_TIME_OUT_ERROR_NO_ERROR = 0x0
    FRAMESYNC_TIME_OUT_ERROR_ERROR = 0x1


class ENUM_FRAMESYNC_DONE(Enum):
    FRAMESYNC_DONE_NOT_DONE = 0x0
    FRAMESYNC_DONE_DONE = 0x1


class ENUM_FASTWAKE_INVALID_REQUEST(Enum):
    FASTWAKE_INVALID_REQUEST_NO_ERROR = 0x0
    FASTWAKE_INVALID_REQUEST_ERROR = 0x1


class ENUM_FASTWAKE_RECEIVE_ERROR(Enum):
    FASTWAKE_RECEIVE_ERROR_NO_ERROR = 0x0
    FASTWAKE_RECEIVE_ERROR_ERROR = 0x1


class ENUM_FASTWAKE_TIME_OUT_ERROR(Enum):
    FASTWAKE_TIME_OUT_ERROR_NO_ERROR = 0x0
    FASTWAKE_TIME_OUT_ERROR_ERROR = 0x1


class ENUM_FASTWAKE_DONE(Enum):
    FASTWAKE_DONE_NOT_DONE = 0x0
    FASTWAKE_DONE_DONE = 0x1


class OFFSET_PSR2_DEBUG:
    PSR2_DEBUG_A = 0x60948
    PSR2_DEBUG_B = 0x61948


class _PSR2_DEBUG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 7),
        ('FramesyncReceiveError', ctypes.c_uint32, 1),
        ('FramesyncTimeOutError', ctypes.c_uint32, 1),
        ('FramesyncDone', ctypes.c_uint32, 1),
        ('FastwakeInvalidRequest', ctypes.c_uint32, 1),
        ('FastwakeReceiveError', ctypes.c_uint32, 1),
        ('FastwakeTimeOutError', ctypes.c_uint32, 1),
        ('FastwakeDone', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 18),
    ]


class REG_PSR2_DEBUG(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 7
    FramesyncReceiveError = 0  # bit 7 to 8
    FramesyncTimeOutError = 0  # bit 8 to 9
    FramesyncDone = 0  # bit 9 to 10
    FastwakeInvalidRequest = 0  # bit 10 to 11
    FastwakeReceiveError = 0  # bit 11 to 12
    FastwakeTimeOutError = 0  # bit 12 to 13
    FastwakeDone = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR2_DEBUG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR2_DEBUG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PSR2_SU_ENTRY_COMPLETION(Enum):
    PSR2_SU_ENTRY_COMPLETION_NOT_COMPLETE = 0x0
    PSR2_SU_ENTRY_COMPLETION_COMPLETE = 0x1


class ENUM_PSR2_DEEP_SLEEP_ENTRY_COMPLETION(Enum):
    PSR2_DEEP_SLEEP_ENTRY_COMPLETION_NOT_COMPLETE = 0x0
    PSR2_DEEP_SLEEP_ENTRY_COMPLETION_COMPLETE = 0x1


class ENUM_SENDING_TP2(Enum):
    SENDING_TP2_NOT_SENDING = 0x0  # Not sending TP2
    SENDING_TP2_SENDING = 0x1  # Sending TP2


class ENUM_IDLE_NOT_ALLOWED(Enum):
    IDLE_NOT_ALLOWED_NOT_SET = 0x0  # Idle not allowed is not set.
    IDLE_NOT_ALLOWED_SET = 0x1  # Idle not allowed is set.


class ENUM_PSR2_NOT_ALLOWED(Enum):
    PSR2_NOT_ALLOWED_NOT_SET = 0x0  # PSR2 not allowed is not set.
    PSR2_NOT_ALLOWED_SET = 0x1  # PSR2 not allowed is set.


class ENUM_LINK_STATUS(Enum):
    LINK_STATUS_FULL_OFF = 0x0  # Link is fully off
    LINK_STATUS_FULL_ON = 0x1  # Link is fully on


class ENUM_PSR2_STATE(Enum):
    PSR2_STATE_IDLE = 0x0  # Reset state
    PSR2_STATE_CAPTURE = 0x1  # Send capture frame
    PSR2_STATE_CPTURE_FS = 0x2  # Fast sleep after capture frame is sent
    PSR2_STATE_SLEEP = 0x3  # Selective Update
    PSR2_STATE_BUFON_FW = 0x4  # Turn Buffer on and Send Fast wake
    PSR2_STATE_ML_UP = 0x5  # Turn Main link up and send SR
    PSR2_STATE_SU_STANDBY = 0x6  # Selective update or Standby state
    PSR2_STATE_FAST_SLEEP = 0x7  # Send Fast sleep
    PSR2_STATE_DEEP_SLEEP = 0x8  # Enter Deep sleep
    PSR2_STATE_BUF_ON = 0x9  # Turn ON IO Buffer
    PSR2_STATE_TG_ON = 0xA  # Turn ON Timing Generator
    PSR2_STATE_BUFON_FW_2 = 0xB  # Turn Buffer on and Send Fast wake for 3 Block case


class OFFSET_PSR2_STATUS:
    PSR2_STATUS_A = 0x60940
    PSR2_STATUS_B = 0x61940


class _PSR2_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IdleFrameCounter', ctypes.c_uint32, 4),
        ('Psr2SuEntryCompletion', ctypes.c_uint32, 1),
        ('Psr2DeepSleepEntryCompletion', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('SendingTp2', ctypes.c_uint32, 1),
        ('Psr2IdleFrameIndication', ctypes.c_uint32, 1),
        ('IdleNotAllowed', ctypes.c_uint32, 1),
        ('Psr2NotAllowed', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 4),
        ('Psr2DeepSleepEntryCount', ctypes.c_uint32, 4),
        ('MaxSleepTimeCounter', ctypes.c_uint32, 5),
        ('Reserved25', ctypes.c_uint32, 1),
        ('LinkStatus', ctypes.c_uint32, 2),
        ('Psr2State', ctypes.c_uint32, 4),
    ]


class REG_PSR2_STATUS(ctypes.Union):
    value = 0
    offset = 0

    IdleFrameCounter = 0  # bit 0 to 4
    Psr2SuEntryCompletion = 0  # bit 4 to 5
    Psr2DeepSleepEntryCompletion = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    SendingTp2 = 0  # bit 8 to 9
    Psr2IdleFrameIndication = 0  # bit 9 to 10
    IdleNotAllowed = 0  # bit 10 to 11
    Psr2NotAllowed = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 16
    Psr2DeepSleepEntryCount = 0  # bit 16 to 20
    MaxSleepTimeCounter = 0  # bit 20 to 25
    Reserved25 = 0  # bit 25 to 26
    LinkStatus = 0  # bit 26 to 28
    Psr2State = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR2_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR2_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PSR2_SU_STATUS:
    PSR2_SU_STATUS_A = 0x60914
    PSR2_SU_STATUS_B = 0x61914


class _PSR2_SU_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('NumberOfSuBlocksInFrameN', ctypes.c_uint32, 10),
        ('NumberOfSuBlocksInFrameN1', ctypes.c_uint32, 10),
        ('NumberOfSuBlocksInFrameN2', ctypes.c_uint32, 10),
        ('Reserved30', ctypes.c_uint32, 2),
        ('NumberOfSuBlocksInFrameN3', ctypes.c_uint32, 10),
        ('NumberOfSuBlocksInFrameN4', ctypes.c_uint32, 10),
        ('NumberOfSuBlocksInFrameN5', ctypes.c_uint32, 10),
        ('Reserved30', ctypes.c_uint32, 2),
        ('NumberOfSuBlocksInFrameN6', ctypes.c_uint32, 10),
        ('NumberOfSuBlocksInFrameN7', ctypes.c_uint32, 10),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_PSR2_SU_STATUS(ctypes.Union):
    value = 0
    offset = 0

    NumberOfSuBlocksInFrameN = 0  # bit 0 to 10
    NumberOfSuBlocksInFrameN1 = 0  # bit 10 to 20
    NumberOfSuBlocksInFrameN2 = 0  # bit 20 to 30
    Reserved30 = 0  # bit 30 to 32
    NumberOfSuBlocksInFrameN3 = 0  # bit 0 to 10
    NumberOfSuBlocksInFrameN4 = 0  # bit 10 to 20
    NumberOfSuBlocksInFrameN5 = 0  # bit 20 to 30
    Reserved30 = 0  # bit 30 to 32
    NumberOfSuBlocksInFrameN6 = 0  # bit 0 to 10
    NumberOfSuBlocksInFrameN7 = 0  # bit 10 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR2_SU_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR2_SU_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

