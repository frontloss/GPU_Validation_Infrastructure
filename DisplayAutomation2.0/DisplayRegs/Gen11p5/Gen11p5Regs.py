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
# @file Gen11p5Regs.py
# @brief contains Gen11p5Regs.py related register definitions

import ctypes
from enum import Enum


class ENUM_RST_PCH_HANDSHAKE_EN(Enum):
    RST_PCH_HANDSHAKE_EN_DISABLE = 0x0
    RST_PCH_HANDSHAKE_EN_ENABLE = 0x1


class ENUM_RSTWRN_DE_RESET_DIS(Enum):
    RSTWRN_DE_RESET_DIS_ENABLE = 0x0
    RSTWRN_DE_RESET_DIS_DISABLE = 0x1


class OFFSET_NDE_RSTWRN_OPT:
    NDE_RSTWRN_OPT = 0x46408


class _NDE_RSTWRN_OPT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 4),
        ('RstPchHandshakeEn', ctypes.c_uint32, 1),
        ('RstwrnDeResetDis', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 25),
    ]


class REG_NDE_RSTWRN_OPT(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 4
    RstPchHandshakeEn = 0  # bit 4 to 5
    RstwrnDeResetDis = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 32

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


class ENUM_POWER_GATE_DIS_OVERRIDE(Enum):
    POWER_GATE_DIS_OVERRIDE_DO_NOT_OVERRIDE = 0x0
    POWER_GATE_DIS_OVERRIDE_OVERRIDE = 0x1


class ENUM_DBUF_POWER_STATE(Enum):
    DBUF_POWER_STATE_DISABLED = 0x0
    DBUF_POWER_STATE_ENABLED = 0x1


class ENUM_DBUF_POWER_REQUEST(Enum):
    DBUF_POWER_REQUEST_DISABLE = 0x0
    DBUF_POWER_REQUEST_ENABLE = 0x1


class OFFSET_DBUF_CTL:
    DBUF_CTL_S2 = 0x44FE8
    DBUF_CTL_S1 = 0x45008


class _DBUF_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('CcBlockValidStateService', ctypes.c_uint32, 4),
        ('Reserved16', ctypes.c_uint32, 3),
        ('TrackerStateService', ctypes.c_uint32, 5),
        ('PowerGateDelay', ctypes.c_uint32, 2),
        ('Reserved26', ctypes.c_uint32, 1),
        ('PowerGateDisOverride', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 2),
        ('DbufPowerState', ctypes.c_uint32, 1),
        ('DbufPowerRequest', ctypes.c_uint32, 1),
    ]


class REG_DBUF_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    CcBlockValidStateService = 0  # bit 12 to 16
    Reserved16 = 0  # bit 16 to 19
    TrackerStateService = 0  # bit 19 to 24
    PowerGateDelay = 0  # bit 24 to 26
    Reserved26 = 0  # bit 26 to 27
    PowerGateDisOverride = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 30
    DbufPowerState = 0  # bit 30 to 31
    DbufPowerRequest = 0  # bit 31 to 32

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


class ENUM_SW_RESET_LENGTH(Enum):
    SW_RESET_LENGTH_8_CLOCKS = 0x8


class ENUM_DDI_CLOCK_REG_ACCESS(Enum):
    DDI_CLOCK_REG_ACCESS_CLOCK_OFF = 0x0  # Clock on is 0 so that ports will respond to register access immediately
    DDI_CLOCK_REG_ACCESS_CLOCK_ON = 0x1  # Clock on is 1 so that ports will delay register access while synchronizing


class ENUM_PORT_REG_ACCESS_OVERRIDE(Enum):
    PORT_REG_ACCESS_OVERRIDE_DO_NOT_OVERRIDE = 0x0  # Do not override clk on to port registers
    PORT_REG_ACCESS_OVERRIDE_OVERRIDE = 0x1  # Override clock on to 0 so that ports will respond to register access imm
                                             # ediately


class ENUM_IDLE_THRESHOLD(Enum):
    IDLE_THRESHOLD_8 = 0x0  # PM response sent when Idle for 8 clocks
    IDLE_THRESHOLD_16 = 0x1  # PM response sent when Idle for 16 clocks
    IDLE_THRESHOLD_32 = 0x2  # PM response sent when Idle for 32 clocks
    IDLE_THRESHOLD_64 = 0x3  # PM response sent when Idle for 64 clocks


class ENUM_IDLE_WAKEMEM_MASK(Enum):
    IDLE_WAKEMEM_MASK_DO_NOT_MASK_WAKEMEM = 0x0  # Streamer Wakemem is considered in the Idle calculation
    IDLE_WAKEMEM_MASK_MASK_WAKEMEM = 0x1  # Streamer Wakemem is not considered in the Idle calculation


class ENUM_MEMUP_RESPONSE_WAIT(Enum):
    MEMUP_RESPONSE_WAIT_WAIT = 0x0  # Wait for idle before sending a response to a PM request with memup=1
    MEMUP_RESPONSE_WAIT_DO_NOT_WAIT = 0x1  # Do not wait for idle before sending a response to a PM request with memup=
                                           # 1


class ENUM_DISABLE_FLR_SRD(Enum):
    DISABLE_FLR_SRD_ENABLE = 0x0  # Hold FLR until SRD exit
    DISABLE_FLR_SRD_DISABLE = 0x1  # Do not hold FLR until SRD exit


class ENUM_DISPLAY_CLOCK_GATING_OVERRIDE(Enum):
    DISPLAY_CLOCK_GATING_OVERRIDE_DISPLAY_CLOCK_GATING_ENABLED = 0x0  # Chicken bit is inactive. Clock gating depends o
                                                                      # n individual bits programmed.
    DISPLAY_CLOCK_GATING_OVERRIDE_DISPLAY_CLOCK_GATING_DISABLED = 0x1  # Clock gating is disabled for entire display. O
                                                                       # verrides any programming done for individual
                                                                       # bits.


class ENUM_BLOCK_BLOCK_FILL_RESPONSE_OVERRIDE(Enum):
    BLOCK_BLOCK_FILL_RESPONSE_OVERRIDE_PM_RESP_NOT_OVERWRITTEN = 0x0  # Chicken bit is inactive. Block block fill Pm re
                                                                      # sponse is not overwritten.
    BLOCK_BLOCK_FILL_RESPONSE_OVERRIDE_PM_RESP_IS_OVERWRITTEN = 0x1  # Chicken bit is active. Block block fill PM respo
                                                                     # nse is overwritten and response will not wait
                                                                     # for fill done.


class ENUM_DG_EMPTY_DE_WAKE_OVERWRITE(Enum):
    DG_EMPTY_DE_WAKE_OVERWRITE_DE_WAKE_GENERATED_WHEN_DG_FIFO_IS_NOT_EMPTY = 0x0  # Chicken bit is inactive. DE Wake ge
                                                                                  # nerated when DG fifo is not empty.
    DG_EMPTY_DE_WAKE_OVERWRITE_DE_WAKE_IS_NOT_GENERATED_WHEN_DG_FIFO_IS_NOT_EMPTY = 0x1  # Chicken bit is active. DE Wa
                                                                                         # ke is not generated when DG
                                                                                         # fifo is not empty.


class OFFSET_CHICKEN_DCPR_1:
    CHICKEN_DCPR_1 = 0x46430


class _CHICKEN_DCPR_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SwResetLength', ctypes.c_uint32, 5),
        ('Spare5', ctypes.c_uint32, 1),
        ('Spare6', ctypes.c_uint32, 1),
        ('DdiClockRegAccess', ctypes.c_uint32, 1),
        ('PortRegAccessOverride', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('Spare10', ctypes.c_uint32, 1),
        ('IdleThreshold', ctypes.c_uint32, 2),
        ('IdleWakememMask', ctypes.c_uint32, 1),
        ('MemupResponseWait', ctypes.c_uint32, 1),
        ('DisableFlrSrd', ctypes.c_uint32, 1),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('Spare18', ctypes.c_uint32, 1),
        ('DisplayClockGatingOverride', ctypes.c_uint32, 1),
        ('BlockBlockFillResponseOverride', ctypes.c_uint32, 1),
        ('DgEmptyDe_WakeOverwrite', ctypes.c_uint32, 1),
        ('Spare22', ctypes.c_uint32, 1),
        ('Spare23', ctypes.c_uint32, 1),
        ('Spare24', ctypes.c_uint32, 1),
        ('Spare25', ctypes.c_uint32, 1),
        ('Spare26', ctypes.c_uint32, 1),
        ('Spare27', ctypes.c_uint32, 1),
        ('Spare28', ctypes.c_uint32, 1),
        ('Spare29', ctypes.c_uint32, 1),
        ('Spare30', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_CHICKEN_DCPR_1(ctypes.Union):
    value = 0
    offset = 0

    SwResetLength = 0  # bit 0 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
    DdiClockRegAccess = 0  # bit 7 to 8
    PortRegAccessOverride = 0  # bit 8 to 9
    Spare9 = 0  # bit 9 to 10
    Spare10 = 0  # bit 10 to 11
    IdleThreshold = 0  # bit 11 to 13
    IdleWakememMask = 0  # bit 13 to 14
    MemupResponseWait = 0  # bit 14 to 15
    DisableFlrSrd = 0  # bit 15 to 16
    Spare16 = 0  # bit 16 to 17
    Spare17 = 0  # bit 17 to 18
    Spare18 = 0  # bit 18 to 19
    DisplayClockGatingOverride = 0  # bit 19 to 20
    BlockBlockFillResponseOverride = 0  # bit 20 to 21
    DgEmptyDe_WakeOverwrite = 0  # bit 21 to 22
    Spare22 = 0  # bit 22 to 23
    Spare23 = 0  # bit 23 to 24
    Spare24 = 0  # bit 24 to 25
    Spare25 = 0  # bit 25 to 26
    Spare26 = 0  # bit 26 to 27
    Spare27 = 0  # bit 27 to 28
    Spare28 = 0  # bit 28 to 29
    Spare29 = 0  # bit 29 to 30
    Spare30 = 0  # bit 30 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_DCPR_1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_DCPR_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MESSAGE_REQUEST_WAKE_DISABLE(Enum):
    MESSAGE_REQUEST_WAKE_DISABLE_DO_NOT_WAKE = 0x1  # Do not wake memory for message request
    MESSAGE_REQUEST_WAKE_DISABLE_WAKE = 0x0  # Wake memory for message request


class ENUM_MESSAGE_REQUEST_BLOCK_DISABLE(Enum):
    MESSAGE_REQUEST_BLOCK_DISABLE_DO_NOT_BLOCK = 0x1  # Do not block message requests when memory is asleep
    MESSAGE_REQUEST_BLOCK_DISABLE_BLOCK = 0x0  # Block message requests when memory is asleep


class ENUM_FORCE_ARB_IDLE_AUDIO(Enum):
    FORCE_ARB_IDLE_AUDIO_FORCE = 0x1  # Force LP Arb idle for audio
    FORCE_ARB_IDLE_AUDIO_DO_NOT_FORCE = 0x0  # Do not force LP arb idle for audio


class ENUM_FORCE_ARB_IDLE_FBC(Enum):
    FORCE_ARB_IDLE_FBC_FORCE = 0x1  # Force LP Arb idle for FBC
    FORCE_ARB_IDLE_FBC_DO_NOT_FORCE = 0x0  # Do not force LP arb idle for FBC


class ENUM_FORCE_ARB_IDLE_PLANES(Enum):
    FORCE_ARB_IDLE_PLANES_FORCE = 0x1  # Force HP arb idle when planes are disabled
    FORCE_ARB_IDLE_PLANES_DO_NOT_FORCE = 0x0  # Do not force HP arb idle when planes are disabled


class ENUM_DPARB_DGSA_SEL_STALL3(Enum):
    DPARB_DGSA_SEL_STALL3_STALL = 0x1  # Stall credits when there are 3 places remaining in the arbiter FIFO
    DPARB_DGSA_SEL_STALL3_NORMAL = 0x0  # Normal stall behavior


class ENUM_KVM_OVERFLOW_BLOCK_REVERT(Enum):
    KVM_OVERFLOW_BLOCK_REVERT_DO_NOT_REVERT = 0x0  # Writeback stopped for rest of frame after overflow
    KVM_OVERFLOW_BLOCK_REVERT_REVERT = 0x1  # Writeback continues after overflow


class ENUM_KVM_CONFIG_CHANGE_NOTIFICATION_SELECT(Enum):
    KVM_CONFIG_CHANGE_NOTIFICATION_SELECT_VALUE_CHANGE = 0x0  # Config change notification only on config value changes
    KVM_CONFIG_CHANGE_NOTIFICATION_SELECT_BOTH = 0x1  # Config change notification on config writes and on config value
                                                      #  changes


class ENUM_DPARB_EVEN_PUT_FIX_DISABLE(Enum):
    DPARB_EVEN_PUT_FIX_ENABLE = 0x0  # Enable fix for arbiter even put.
    DPARB_EVEN_PUT_FIX_DISABLE = 0x1  # Disable fix for arbiter even put.


class ENUM_DPARB_HP_CLOCK_EN_OVERRIDE(Enum):
    DPARB_HP_CLOCK_EN_OVERRIDE_NORMAL = 0x0  # Disable gated clock when all planes are disabled.
    DPARB_HP_CLOCK_EN_OVERRIDE_OVERRIDE = 0x1  # Keep gated clock enabled with any pending request when all plane are d
                                               # isabled.


class ENUM_SCALER_ECC_BYPASS(Enum):
    SCALER_ECC_BYPASS_DO_NOT_BYPASS = 0x0  # ECC is used.
    SCALER_ECC_BYPASS_BYPASS = 0x1  # ECC is is not used


class ENUM_PSR2_SU_ECC_BYPASS(Enum):
    PSR2_SU_ECC_BYPASS_DO_NOT_BYPASS = 0x0  # ECC is used.
    PSR2_SU_ECC_BYPASS_BYPASS = 0x1  # ECC is is not used


class OFFSET_CHICKEN_MISC_1:
    CHICKEN_MISC_1 = 0x42080


class _CHICKEN_MISC_1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare0', ctypes.c_uint32, 1),
        ('Spare1', ctypes.c_uint32, 1),
        ('Spare2', ctypes.c_uint32, 1),
        ('Spare3', ctypes.c_uint32, 1),
        ('Spare4', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('Spare6', ctypes.c_uint32, 1),
        ('Spare7', ctypes.c_uint32, 1),
        ('Spare8', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('MessageRequestWakeDisable', ctypes.c_uint32, 1),
        ('MessageRequestBlockDisable', ctypes.c_uint32, 1),
        ('ForceArbIdleAudio', ctypes.c_uint32, 1),
        ('ForceArbIdleFbc', ctypes.c_uint32, 1),
        ('ForceArbIdlePlanes', ctypes.c_uint32, 1),
        ('Spare15', ctypes.c_uint32, 1),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('Spare18', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('DparbDgsaSelStall3', ctypes.c_uint32, 1),
        ('Spare21', ctypes.c_uint32, 1),
        ('Spare22', ctypes.c_uint32, 1),
        ('Spare23', ctypes.c_uint32, 1),
        ('KvmOverflowBlockRevert', ctypes.c_uint32, 1),
        ('KvmConfigChangeNotificationSelect', ctypes.c_uint32, 1),
        ('Spare26', ctypes.c_uint32, 1),
        ('DparbEvenPutFixDisable', ctypes.c_uint32, 1),
        ('DparbHpClockEnOverride', ctypes.c_uint32, 1),
        ('ScalerEccBypass', ctypes.c_uint32, 1),
        ('Psr2SuEccBypass', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_CHICKEN_MISC_1(ctypes.Union):
    value = 0
    offset = 0

    Spare0 = 0  # bit 0 to 1
    Spare1 = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    Spare3 = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
    Spare7 = 0  # bit 7 to 8
    Spare8 = 0  # bit 8 to 9
    Spare9 = 0  # bit 9 to 10
    MessageRequestWakeDisable = 0  # bit 10 to 11
    MessageRequestBlockDisable = 0  # bit 11 to 12
    ForceArbIdleAudio = 0  # bit 12 to 13
    ForceArbIdleFbc = 0  # bit 13 to 14
    ForceArbIdlePlanes = 0  # bit 14 to 15
    Spare15 = 0  # bit 15 to 16
    Spare16 = 0  # bit 16 to 17
    Spare17 = 0  # bit 17 to 18
    Spare18 = 0  # bit 18 to 19
    Spare19 = 0  # bit 19 to 20
    DparbDgsaSelStall3 = 0  # bit 20 to 21
    Spare21 = 0  # bit 21 to 22
    Spare22 = 0  # bit 22 to 23
    Spare23 = 0  # bit 23 to 24
    KvmOverflowBlockRevert = 0  # bit 24 to 25
    KvmConfigChangeNotificationSelect = 0  # bit 25 to 26
    Spare26 = 0  # bit 26 to 27
    DparbEvenPutFixDisable = 0  # bit 27 to 28
    DparbHpClockEnOverride = 0  # bit 28 to 29
    ScalerEccBypass = 0  # bit 29 to 30
    Psr2SuEccBypass = 0  # bit 30 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_MISC_1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_MISC_1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_KVMRCAP_REG_DOUBLE_BUFFER(Enum):
    KVMRCAP_REG_DOUBLE_BUFFER_ENABLE_DOUBLE_BUFFER = 0x0
    KVMRCAP_REG_DOUBLE_BUFFER_DISABLE_DOUBLE_BUFFER = 0x1


class OFFSET_CHICKEN_MISC_2:
    CHICKEN_MISC_2 = 0x42084


class _CHICKEN_MISC_2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare0', ctypes.c_uint32, 1),
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
        ('Spare11', ctypes.c_uint32, 1),
        ('Spare12', ctypes.c_uint32, 1),
        ('Spare13', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('Spare15', ctypes.c_uint32, 1),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('Spare18', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('KvmrcapRegDoubleBuffer', ctypes.c_uint32, 1),
        ('Spare21', ctypes.c_uint32, 1),
        ('Spare22', ctypes.c_uint32, 1),
        ('Spare23', ctypes.c_uint32, 1),
        ('Spare24', ctypes.c_uint32, 1),
        ('Spare25', ctypes.c_uint32, 1),
        ('Spare26', ctypes.c_uint32, 1),
        ('Spare27', ctypes.c_uint32, 1),
        ('Spare28', ctypes.c_uint32, 1),
        ('Spare29', ctypes.c_uint32, 1),
        ('Spare30', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_CHICKEN_MISC_2(ctypes.Union):
    value = 0
    offset = 0

    Spare0 = 0  # bit 0 to 1
    Spare1 = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    Spare3 = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
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
    KvmrcapRegDoubleBuffer = 0  # bit 20 to 21
    Spare21 = 0  # bit 21 to 22
    Spare22 = 0  # bit 22 to 23
    Spare23 = 0  # bit 23 to 24
    Spare24 = 0  # bit 24 to 25
    Spare25 = 0  # bit 25 to 26
    Spare26 = 0  # bit 26 to 27
    Spare27 = 0  # bit 27 to 28
    Spare28 = 0  # bit 28 to 29
    Spare29 = 0  # bit 29 to 30
    Spare30 = 0  # bit 30 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_MISC_2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_MISC_2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CHICKEN_MISC_3:
    CHICKEN_MISC_3 = 0x42088


class _CHICKEN_MISC_3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare0', ctypes.c_uint32, 1),
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
        ('Spare29', ctypes.c_uint32, 1),
        ('Spare30', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_CHICKEN_MISC_3(ctypes.Union):
    value = 0
    offset = 0

    Spare0 = 0  # bit 0 to 1
    Spare1 = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    Spare3 = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
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
    Spare29 = 0  # bit 29 to 30
    Spare30 = 0  # bit 30 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_MISC_3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_MISC_3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CHICKEN_MISC_4:
    CHICKEN_MISC_4 = 0x4208C


class _CHICKEN_MISC_4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare0', ctypes.c_uint32, 1),
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
        ('Spare29', ctypes.c_uint32, 1),
        ('Spare30', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_CHICKEN_MISC_4(ctypes.Union):
    value = 0
    offset = 0

    Spare0 = 0  # bit 0 to 1
    Spare1 = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    Spare3 = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
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
    Spare29 = 0  # bit 29 to 30
    Spare30 = 0  # bit 30 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_MISC_4),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_MISC_4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SKIP_REGISTER_ACK(Enum):
    SKIP_REGISTER_ACK_DO_NOT_SKIP = 0x0
    SKIP_REGISTER_ACK_SKIP = 0x1


class OFFSET_CHICKEN_MISC_5:
    CHICKEN_MISC_5 = 0x42090


class _CHICKEN_MISC_5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SkipRegisterAck', ctypes.c_uint32, 1),
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
        ('Spare29', ctypes.c_uint32, 1),
        ('Spare30', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_CHICKEN_MISC_5(ctypes.Union):
    value = 0
    offset = 0

    SkipRegisterAck = 0  # bit 0 to 1
    Spare1 = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    Spare3 = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
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
    Spare29 = 0  # bit 29 to 30
    Spare30 = 0  # bit 30 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_MISC_5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_MISC_5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PLANE_1_TLB_STRETCH_DISABLE(Enum):
    PLANE_1_TLB_STRETCH_ENABLE = 0x0
    PLANE_1_TLB_STRETCH_DISABLE = 0x1


class ENUM_PLANE_2_TLB_STRETCH_DISABLE(Enum):
    PLANE_2_TLB_STRETCH_ENABLE = 0x0
    PLANE_2_TLB_STRETCH_DISABLE = 0x1


class ENUM_PLANE_3_TLB_STRETCH_DISABLE(Enum):
    PLANE_3_TLB_STRETCH_ENABLE = 0x0
    PLANE_3_TLB_STRETCH_DISABLE = 0x1


class ENUM_PLANE_4_TLB_STRETCH_DISABLE(Enum):
    PLANE_4_TLB_STRETCH_ENABLE = 0x0
    PLANE_4_TLB_STRETCH_DISABLE = 0x1


class ENUM_PLANE_5_TLB_STRETCH_DISABLE(Enum):
    PLANE_5_TLB_STRETCH_ENABLE = 0x0
    PLANE_5_TLB_STRETCH_DISABLE = 0x1


class ENUM_PLANE_6_TLB_STRETCH_DISABLE(Enum):
    PLANE_6_TLB_STRETCH_ENABLE = 0x0
    PLANE_6_TLB_STRETCH_DISABLE = 0x1


class ENUM_PLANE_7_TLB_STRETCH_DISABLE(Enum):
    PLANE_7_TLB_STRETCH_ENABLE = 0x0
    PLANE_7_TLB_STRETCH_DISABLE = 0x1


class ENUM_DST_CROSS_COORDINATION(Enum):
    DST_CROSS_COORDINATION_DISABLE = 0x0
    DST_CROSS_COORDINATION_ENABLE = 0x1


class ENUM_SURFACE_ARMING_REQUIRED_SYNC(Enum):
    SURFACE_ARMING_REQUIRED_SYNC_NO_ARMING = 0x0
    SURFACE_ARMING_REQUIRED_SYNC_ARMING_REQUIRED = 0x1


class ENUM_DDB_FLUSH(Enum):
    DDB_FLUSH_DISABLE = 0x0
    DDB_FLUSH_ENABLE = 0x1


class ENUM_DMUX_BFI_HOLD_SCANLINE_COUNT(Enum):
    DMUX_BFI_HOLD_SCANLINE_COUNT_RUN = 0x0  # Run the vertical line count during the black frame when in BFI mode
    DMUX_BFI_HOLD_SCANLINE_COUNT_HOLD = 0x1  # Hold the vertical line count during the black frame when in BFI mode


class ENUM_DMUX_BFI_REDUCE_SCANLINE_COUNT(Enum):
    DMUX_BFI_REDUCE_SCANLINE_COUNT_DISABLE = 0x0  # Do not reduce
    DMUX_BFI_REDUCE_SCANLINE_COUNT_ENABLE = 0x1  # Skip every other line in BFI


class ENUM_PS_LINE_FETCH_DELAY_DISABLE(Enum):
    PS_LINE_FETCH_DELAY_ENABLE = 0x0  # Line fetches delayed until the line buffers are valid
    PS_LINE_FETCH_DELAY_DISABLE = 0x1  # Line fetches not delayed by line buffer valid


class ENUM_PS_VBLANK_DROP_BYPASS(Enum):
    PS_VBLANK_DROP_BYPASS_ENABLE = 0x0  # Enable the pipe scaler fix to drop pixels between vblank and framestart
    PS_VBLANK_DROP_BYPASS_DISABLE = 0x1  # Disable the pipe scalerfix to drop pixels between vblank and framestart


class OFFSET_CHICKEN_PIPESL:
    CHICKEN_PIPESL_A = 0x420B0
    CHICKEN_PIPESL_B = 0x420B4
    CHICKEN_PIPESL_C = 0x420B8
    CHICKEN_PIPESL_D = 0x420BC


class _CHICKEN_PIPESL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Plane1TlbStretchDisable', ctypes.c_uint32, 1),
        ('Plane2TlbStretchDisable', ctypes.c_uint32, 1),
        ('Plane3TlbStretchDisable', ctypes.c_uint32, 1),
        ('Plane4TlbStretchDisable', ctypes.c_uint32, 1),
        ('Plane5TlbStretchDisable', ctypes.c_uint32, 1),
        ('Plane6TlbStretchDisable', ctypes.c_uint32, 1),
        ('Plane7TlbStretchDisable', ctypes.c_uint32, 1),
        ('Spare7', ctypes.c_uint32, 1),
        ('Spare8', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('Spare10', ctypes.c_uint32, 1),
        ('Spare11', ctypes.c_uint32, 1),
        ('DstCrossCoordination', ctypes.c_uint32, 1),
        ('Spare13', ctypes.c_uint32, 1),
        ('SurfaceArmingRequiredSync', ctypes.c_uint32, 1),
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
        ('DdbFlush', ctypes.c_uint32, 1),
        ('DmuxBfiHoldScanlineCount', ctypes.c_uint32, 1),
        ('DmuxBfiReduceScanlineCount', ctypes.c_uint32, 1),
        ('PsLineFetchDelayDisable', ctypes.c_uint32, 1),
        ('PsVblankDropBypass', ctypes.c_uint32, 1),
    ]


class REG_CHICKEN_PIPESL(ctypes.Union):
    value = 0
    offset = 0

    Plane1TlbStretchDisable = 0  # bit 0 to 1
    Plane2TlbStretchDisable = 0  # bit 1 to 2
    Plane3TlbStretchDisable = 0  # bit 2 to 3
    Plane4TlbStretchDisable = 0  # bit 3 to 4
    Plane5TlbStretchDisable = 0  # bit 4 to 5
    Plane6TlbStretchDisable = 0  # bit 5 to 6
    Plane7TlbStretchDisable = 0  # bit 6 to 7
    Spare7 = 0  # bit 7 to 8
    Spare8 = 0  # bit 8 to 9
    Spare9 = 0  # bit 9 to 10
    Spare10 = 0  # bit 10 to 11
    Spare11 = 0  # bit 11 to 12
    DstCrossCoordination = 0  # bit 12 to 13
    Spare13 = 0  # bit 13 to 14
    SurfaceArmingRequiredSync = 0  # bit 14 to 15
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
    DdbFlush = 0  # bit 27 to 28
    DmuxBfiHoldScanlineCount = 0  # bit 28 to 29
    DmuxBfiReduceScanlineCount = 0  # bit 29 to 30
    PsLineFetchDelayDisable = 0  # bit 30 to 31
    PsVblankDropBypass = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_PIPESL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_PIPESL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CLKGATE_DIS_0:
    CLKGATE_DIS_0 = 0x46530


class _CLKGATE_DIS_0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DoledGatingDis', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 10),
        ('DarbaGatingDis', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 5),
        ('Reserved18', ctypes.c_uint32, 2),
        ('DhdcpcGatingDis', ctypes.c_uint32, 1),
        ('DmgGatingDis', ctypes.c_uint32, 1),
        ('DmcRamGatingDis', ctypes.c_uint32, 1),
        ('DmcGatingDis', ctypes.c_uint32, 1),
        ('DarbuGatingDis', ctypes.c_uint32, 1),
        ('DarbfGdrGatingDis', ctypes.c_uint32, 1),
        ('DarbfLpGatingDis', ctypes.c_uint32, 1),
        ('DarbfGatingDis', ctypes.c_uint32, 1),
        ('DdtGatingDis', ctypes.c_uint32, 1),
        ('DprzGatingDis', ctypes.c_uint32, 1),
        ('DgsaCdclkGatingDis', ctypes.c_uint32, 1),
        ('DgsaFclkGatingDis', ctypes.c_uint32, 1),
    ]


class REG_CLKGATE_DIS_0(ctypes.Union):
    value = 0
    offset = 0

    DoledGatingDis = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 11
    DarbaGatingDis = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 18
    Reserved18 = 0  # bit 18 to 20
    DhdcpcGatingDis = 0  # bit 20 to 21
    DmgGatingDis = 0  # bit 21 to 22
    DmcRamGatingDis = 0  # bit 22 to 23
    DmcGatingDis = 0  # bit 23 to 24
    DarbuGatingDis = 0  # bit 24 to 25
    DarbfGdrGatingDis = 0  # bit 25 to 26
    DarbfLpGatingDis = 0  # bit 26 to 27
    DarbfGatingDis = 0  # bit 27 to 28
    DdtGatingDis = 0  # bit 28 to 29
    DprzGatingDis = 0  # bit 29 to 30
    DgsaCdclkGatingDis = 0  # bit 30 to 31
    DgsaFclkGatingDis = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CLKGATE_DIS_0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CLKGATE_DIS_0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_AUX_FRAME_SYNC_EVENT_TIMING(Enum):
    AUX_FRAME_SYNC_EVENT_TIMING_AT_THE_END_OF_CAPTURE_FRAME = 0x0
    AUX_FRAME_SYNC_EVENT_TIMING_AT_THE_BEGINNING_OF_CAPTURE_FRAME = 0x1
    AUX_FRAME_SYNC_EVENT_TIMING_AT_THE_END_OF_1ST_SU_FRAME = 0x2
    AUX_FRAME_SYNC_EVENT_TIMING_INVALID = 0x3


class ENUM_HDMI_VBI_WHILE_PORT_OFF(Enum):
    HDMI_VBI_WHILE_PORT_OFF_OFF = 0x0  # Run timing generator when TRANS_CONF and port are both enabled
    HDMI_VBI_WHILE_PORT_OFF_ON = 0x1  # Run timing generator when TRANS_CONF enabled alone


class ENUM_DDA_ACCUMULATE_COUNT_UPDATE(Enum):
    DDA_ACCUMULATE_COUNT_UPDATE_DDA_PRECALCULATE_AT_FRAMESTART = 0x0
    DDA_ACCUMULATE_COUNT_UPDATE_DDA_RECALCULATE_EVERY_LINE = 0x1


class ENUM_FRAME_START_DELAY(Enum):
    FRAME_START_DELAY_FIRST = 0x0  # Frame Start on the first HBLANK after the start of VBLANK
    FRAME_START_DELAY_SECOND = 0x1  # Frame Start on the second HBLANK after the start of VBLANK
    FRAME_START_DELAY_THIRD = 0x2  # Frame Start on the third HBLANK after the start of VBLANK
    FRAME_START_DELAY_FOURTH = 0x3  # Frame Start on the fourth HBLANK after the start of VBLANK


class ENUM_DP_ACTIVE_VIDEO_DISABLE(Enum):
    DP_ACTIVE_VIDEO_DISABLE_NO_FORCE = 0x0  # Do not force
    DP_ACTIVE_VIDEO_DISABLE_FORCE = 0x1  # Force VBID to disable active video (video mute)


class OFFSET_CHICKEN_TRANS:
    CHICKEN_TRANS_A = 0x420C0
    CHICKEN_TRANS_B = 0x420C4
    CHICKEN_TRANS_C = 0x420C8
    CHICKEN_TRANS_D = 0x420D8


class _CHICKEN_TRANS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare0', ctypes.c_uint32, 1),
        ('Spare1', ctypes.c_uint32, 1),
        ('Spare2', ctypes.c_uint32, 1),
        ('Spare3', ctypes.c_uint32, 1),
        ('Spare4', ctypes.c_uint32, 1),
        ('Spare5', ctypes.c_uint32, 1),
        ('Spare6', ctypes.c_uint32, 1),
        ('Spare7', ctypes.c_uint32, 1),
        ('Spare8', ctypes.c_uint32, 1),
        ('AuxFrameSyncEventTiming', ctypes.c_uint32, 2),
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
        ('HdmiVbiWhilePortOff', ctypes.c_uint32, 1),
        ('Spare25', ctypes.c_uint32, 1),
        ('DdaAccumulateCountUpdate', ctypes.c_uint32, 1),
        ('FrameStartDelay', ctypes.c_uint32, 2),
        ('DpActiveVideoDisable', ctypes.c_uint32, 1),
        ('Spare30', ctypes.c_uint32, 1),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_CHICKEN_TRANS(ctypes.Union):
    value = 0
    offset = 0

    Spare0 = 0  # bit 0 to 1
    Spare1 = 0  # bit 1 to 2
    Spare2 = 0  # bit 2 to 3
    Spare3 = 0  # bit 3 to 4
    Spare4 = 0  # bit 4 to 5
    Spare5 = 0  # bit 5 to 6
    Spare6 = 0  # bit 6 to 7
    Spare7 = 0  # bit 7 to 8
    Spare8 = 0  # bit 8 to 9
    AuxFrameSyncEventTiming = 0  # bit 9 to 11
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
    HdmiVbiWhilePortOff = 0  # bit 24 to 25
    Spare25 = 0  # bit 25 to 26
    DdaAccumulateCountUpdate = 0  # bit 26 to 27
    FrameStartDelay = 0  # bit 27 to 29
    DpActiveVideoDisable = 0  # bit 29 to 30
    Spare30 = 0  # bit 30 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CHICKEN_TRANS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CHICKEN_TRANS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_UTIL_PIN_DIRECTION(Enum):
    UTIL_PIN_DIRECTION_OUTPUT = 0x0
    UTIL_PIN_DIRECTION_INPUT = 0x1


class ENUM_UTIL_PIN_OUTPUT_POLARITY(Enum):
    UTIL_PIN_OUTPUT_POLARITY_NOT_INVERTED = 0x0
    UTIL_PIN_OUTPUT_POLARITY_INVERTED = 0x1


class ENUM_UTIL_PIN_OUTPUT_DATA(Enum):
    UTIL_PIN_OUTPUT_DATA_0 = 0x0
    UTIL_PIN_OUTPUT_DATA_1 = 0x1


class ENUM_UTIL_PIN_MODE(Enum):
    UTIL_PIN_MODE_DATA = 0x0  # Output the Util_Pin_Output_Data value.
    UTIL_PIN_MODE_PWM = 0x1  # Output from the backlight PWM circuit.
    UTIL_PIN_MODE_VBLANK = 0x4  # Output the vertical blank.
    UTIL_PIN_MODE_VSYNC = 0x5  # Output the vertical sync.
    UTIL_PIN_MODE_RIGHT_LEFT_EYE_LEVEL = 0x8  # Output the stereo 3D right/left eye level signal. Asserted for the left
                                              #  eye and de-asserted for the right eye.


class ENUM_PIPE_SELECT(Enum):
    PIPE_SELECT_PIPE_A = 0x0
    PIPE_SELECT_PIPE_B = 0x1
    PIPE_SELECT_PIPE_C = 0x2
    PIPE_SELECT_PIPE_D = 0x3


class ENUM_UTIL_PIN_ENABLE(Enum):
    UTIL_PIN_DISABLE = 0x0
    UTIL_PIN_ENABLE = 0x1


class OFFSET_UTIL_PIN_CTL:
    UTIL_PIN_CTL = 0x48400


class _UTIL_PIN_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 16),
        ('UtilPinInputData', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 2),
        ('UtilPinDirection', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 2),
        ('UtilPinOutputPolarity', ctypes.c_uint32, 1),
        ('UtilPinOutputData', ctypes.c_uint32, 1),
        ('UtilPinMode', ctypes.c_uint32, 4),
        ('Reserved28', ctypes.c_uint32, 1),
        ('PipeSelect', ctypes.c_uint32, 2),
        ('UtilPinEnable', ctypes.c_uint32, 1),
    ]


class REG_UTIL_PIN_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 16
    UtilPinInputData = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 19
    UtilPinDirection = 0  # bit 19 to 20
    Reserved20 = 0  # bit 20 to 22
    UtilPinOutputPolarity = 0  # bit 22 to 23
    UtilPinOutputData = 0  # bit 23 to 24
    UtilPinMode = 0  # bit 24 to 28
    Reserved28 = 0  # bit 28 to 29
    PipeSelect = 0  # bit 29 to 31
    UtilPinEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _UTIL_PIN_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_UTIL_PIN_CTL, self).__init__()
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
        ('Spare', ctypes.c_uint32, 3),
        ('Reserved27', ctypes.c_uint32, 1),
        ('Hysteresis', ctypes.c_uint32, 2),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_UTIL_PIN_BUF_CTL(ctypes.Union):
    value = 0
    offset = 0

    PullupSlew = 0  # bit 0 to 4
    PullupStrength = 0  # bit 4 to 9
    Reserved9 = 0  # bit 9 to 12
    PulldownSlew = 0  # bit 12 to 16
    PulldownStrength = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 24
    Spare = 0  # bit 24 to 27
    Reserved27 = 0  # bit 27 to 28
    Hysteresis = 0  # bit 28 to 30
    Reserved30 = 0  # bit 30 to 32

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


class ENUM_DISPLAY_AUDIO_CODEC_DISABLE(Enum):
    DISPLAY_AUDIO_CODEC_ENABLE = 0x0  # Audio Codec Capability Enabled
    DISPLAY_AUDIO_CODEC_DISABLE = 0x1  # Audio Codec Capability Disabled


class ENUM_DISPLAY_HDCP_AKSV_READ_ENABLE(Enum):
    DISPLAY_HDCP_AKSV_READ_DISABLE = 0x0
    DISPLAY_HDCP_AKSV_READ_ENABLE = 0x1


class ENUM_DMC_MEM_ACCESS_DISABLE(Enum):
    DMC_MEM_ACCESS_ENABLE = 0x0
    DMC_MEM_ACCESS_DISABLE = 0x1


class ENUM_DMC_GT_ACCESS_DISABLE(Enum):
    DMC_GT_ACCESS_ENABLE = 0x0
    DMC_GT_ACCESS_DISABLE = 0x1


class ENUM_DMC_HIP_ACCESS_DISABLE(Enum):
    DMC_HIP_ACCESS_ENABLE = 0x0
    DMC_HIP_ACCESS_DISABLE = 0x1


class ENUM_DMC_PAVP_SR_DISABLE(Enum):
    DMC_PAVP_SR_ENABLE = 0x0
    DMC_PAVP_SR_DISABLE = 0x1


class ENUM_DISPLAY_RSB_ENABLE(Enum):
    DISPLAY_RSB_DISABLE = 0x0  # RSB Capability Disabled
    DISPLAY_RSB_ENABLE = 0x1  # RSB Capability Enabled


class ENUM_DISPLAY_DSC_DISABLE(Enum):
    DISPLAY_DSC_DISABLE_DSC_CAPABILITY_ENABLED = 0x0
    DISPLAY_DSC_DISABLE_DSC_CAPABILITY_DISABLED = 0x1


class ENUM_AUDIO_CODEC_ID(Enum):
    AUDIO_CODEC_ID_AUDIO_CODEC_ID_280BH = 0xB  # Default value is N/A. Fuse download will override with correct value f
                                               # or this project.


class ENUM_ISOLATED_DECODE_DISABLE(Enum):
    ISOLATED_DECODE_DISABLE_ISOLATED_DECODE_CAPABILITY_ENABLED = 0x0
    ISOLATED_DECODE_DISABLE_ISOLATED_DECODE_CAPABILITY_DISABLED = 0x1


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


class ENUM_WD_VIDEO_TRANSLATION_SELECT(Enum):
    WD_VIDEO_TRANSLATION_SELECT_INTERNAL = 0x0  # WD video VTD translation in display engine
    WD_VIDEO_TRANSLATION_SELECT_EXTERNAL = 0x1  # WD video VTD translation in system agent


class ENUM_DISPLAY_HDCP_DISABLE(Enum):
    DISPLAY_HDCP_ENABLE = 0x0  # HDCP Capability Enabled
    DISPLAY_HDCP_DISABLE = 0x1  # HDCP Capability Disabled


class ENUM_DISPLAY_EDP_DISABLE(Enum):
    DISPLAY_EDP_ENABLE = 0x0  # eDP Capability Enabled
    DISPLAY_EDP_DISABLE = 0x1  # eDP Capability Disabled


class ENUM_DISPLAY_PM_DISABLE(Enum):
    DISPLAY_PM_ENABLE = 0x0  # PM Capability Enabled
    DISPLAY_PM_DISABLE = 0x1  # PM Capability Disabled


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
        ('DmcGtAccessDisable', ctypes.c_uint32, 1),
        ('DmcHipAccessDisable', ctypes.c_uint32, 1),
        ('DmcPavpSrDisable', ctypes.c_uint32, 1),
        ('DisplayRsbEnable', ctypes.c_uint32, 1),
        ('DisplayDscDisable', ctypes.c_uint32, 1),
        ('AudioCodecId', ctypes.c_uint32, 8),
        ('IsolatedDecodeDisable', ctypes.c_uint32, 1),
        ('DfxcmGreenEnable', ctypes.c_uint32, 1),
        ('KvmrSpriteDisable', ctypes.c_uint32, 1),
        ('KvmrCaptureDisable', ctypes.c_uint32, 1),
        ('DisplayWdDisable', ctypes.c_uint32, 1),
        ('DisplayPipebDisable', ctypes.c_uint32, 1),
        ('DisplayPipedDisable', ctypes.c_uint32, 1),
        ('DmcDisable', ctypes.c_uint32, 1),
        ('WdVideoTranslationSelect', ctypes.c_uint32, 1),
        ('DisplayHdcpDisable', ctypes.c_uint32, 1),
        ('DisplayEdpDisable', ctypes.c_uint32, 1),
        ('DisplayPmDisable', ctypes.c_uint32, 1),
        ('DisplayPipecDisable', ctypes.c_uint32, 1),
        ('DisplayDebugEnable', ctypes.c_uint32, 1),
        ('DisplayPipeaDisable', ctypes.c_uint32, 1),
        ('DfxPolicy6Disable', ctypes.c_uint32, 1),
    ]


class REG_DFSM(ctypes.Union):
    value = 0
    offset = 0

    DisplayAudioCodecDisable = 0  # bit 0 to 1
    DisplayHdcpAksvReadEnable = 0  # bit 1 to 2
    DmcMemAccessDisable = 0  # bit 2 to 3
    DmcGtAccessDisable = 0  # bit 3 to 4
    DmcHipAccessDisable = 0  # bit 4 to 5
    DmcPavpSrDisable = 0  # bit 5 to 6
    DisplayRsbEnable = 0  # bit 6 to 7
    DisplayDscDisable = 0  # bit 7 to 8
    AudioCodecId = 0  # bit 8 to 16
    IsolatedDecodeDisable = 0  # bit 16 to 17
    DfxcmGreenEnable = 0  # bit 17 to 18
    KvmrSpriteDisable = 0  # bit 18 to 19
    KvmrCaptureDisable = 0  # bit 19 to 20
    DisplayWdDisable = 0  # bit 20 to 21
    DisplayPipebDisable = 0  # bit 21 to 22
    DisplayPipedDisable = 0  # bit 22 to 23
    DmcDisable = 0  # bit 23 to 24
    WdVideoTranslationSelect = 0  # bit 24 to 25
    DisplayHdcpDisable = 0  # bit 25 to 26
    DisplayEdpDisable = 0  # bit 26 to 27
    DisplayPmDisable = 0  # bit 27 to 28
    DisplayPipecDisable = 0  # bit 28 to 29
    DisplayDebugEnable = 0  # bit 29 to 30
    DisplayPipeaDisable = 0  # bit 30 to 31
    DfxPolicy6Disable = 0  # bit 31 to 32

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


class OFFSET_TIMESTAMP_CTR:
    TIMESTAMP_CTR = 0x44070


class _TIMESTAMP_CTR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TimestampCounter', ctypes.c_uint32, 32),
    ]


class REG_TIMESTAMP_CTR(ctypes.Union):
    value = 0
    offset = 0

    TimestampCounter = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TIMESTAMP_CTR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TIMESTAMP_CTR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CLKGATE_DIS_3:
    CLKGATE_DIS_3 = 0x46538


class _CLKGATE_DIS_3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 1),
        ('DacbeRamGatingDis', ctypes.c_uint32, 1),
        ('DlutCRamGatingDis', ctypes.c_uint32, 1),
        ('DlutBRamGatingDis', ctypes.c_uint32, 1),
        ('DlutARamGatingDis', ctypes.c_uint32, 1),
        ('DlutCGatingDis', ctypes.c_uint32, 1),
        ('DlutBGatingDis', ctypes.c_uint32, 1),
        ('DlutAGatingDis', ctypes.c_uint32, 1),
        ('DlutDRamGatingDis', ctypes.c_uint32, 1),
        ('DlutDGatingDis', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 2),
        ('Reserved13', ctypes.c_uint32, 5),
        ('Reserved18', ctypes.c_uint32, 1),
        ('DpauxdGatingDis', ctypes.c_uint32, 1),
        ('DptpGatingDis', ctypes.c_uint32, 1),
        ('DptRamGatingDis', ctypes.c_uint32, 1),
        ('DptGatingDis', ctypes.c_uint32, 1),
        ('DhdcpddiGatingDis', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 1),
        ('DrposGatingDis', ctypes.c_uint32, 1),
        ('DrpoGatingDis', ctypes.c_uint32, 1),
        ('HdmiGatingDis', ctypes.c_uint32, 1),
        ('DsfGatingDis', ctypes.c_uint32, 1),
        ('DpioGatingDis', ctypes.c_uint32, 1),
        ('DacbeGatingDis', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_CLKGATE_DIS_3(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 2
    DacbeRamGatingDis = 0  # bit 2 to 3
    DlutCRamGatingDis = 0  # bit 3 to 4
    DlutBRamGatingDis = 0  # bit 4 to 5
    DlutARamGatingDis = 0  # bit 5 to 6
    DlutCGatingDis = 0  # bit 6 to 7
    DlutBGatingDis = 0  # bit 7 to 8
    DlutAGatingDis = 0  # bit 8 to 9
    DlutDRamGatingDis = 0  # bit 9 to 10
    DlutDGatingDis = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 13
    Reserved13 = 0  # bit 13 to 18
    Reserved18 = 0  # bit 18 to 19
    DpauxdGatingDis = 0  # bit 19 to 20
    DptpGatingDis = 0  # bit 20 to 21
    DptRamGatingDis = 0  # bit 21 to 22
    DptGatingDis = 0  # bit 22 to 23
    DhdcpddiGatingDis = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 25
    DrposGatingDis = 0  # bit 25 to 26
    DrpoGatingDis = 0  # bit 26 to 27
    HdmiGatingDis = 0  # bit 27 to 28
    DsfGatingDis = 0  # bit 28 to 29
    DpioGatingDis = 0  # bit 29 to 30
    DacbeGatingDis = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

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

