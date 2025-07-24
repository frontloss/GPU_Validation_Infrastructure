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
# @file Gen13Regs.py
# @brief contains Gen13Regs.py related register definitions

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
        ('Reserved10', ctypes.c_uint32, 2),
        ('CcBlockValidStateService', ctypes.c_uint32, 4),
        ('MinTrackerStateService', ctypes.c_uint32, 3),
        ('MaxTrackerStateService', ctypes.c_uint32, 5),
        ('PowerGateDelay', ctypes.c_uint32, 2),
        ('DisplayReorderBufferDisable', ctypes.c_uint32, 1),
        ('PowerGateDisOverride', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 2),
        ('DbufPowerState', ctypes.c_uint32, 1),
        ('DbufPowerRequest', ctypes.c_uint32, 1),
    ]


class REG_DBUF_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 4
    ErrorInjectionFlipBits = 0  # bit 4 to 6
    Reserved6 = 0  # bit 6 to 7
    EccErrorInjectionEnable = 0  # bit 7 to 8
    B2BWriteDisable = 0  # bit 8 to 9
    B2BReadDisable = 0  # bit 9 to 10
    Reserved10 = 0  # bit 10 to 12
    CcBlockValidStateService = 0  # bit 12 to 16
    MinTrackerStateService = 0  # bit 16 to 19
    MaxTrackerStateService = 0  # bit 19 to 24
    PowerGateDelay = 0  # bit 24 to 26
    DisplayReorderBufferDisable = 0  # bit 26 to 27
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


class ENUM_UTIL_PIN_DIRECTION(Enum):
    UTIL_PIN_DIRECTION_OUTPUT = 0x0
    UTIL_PIN_DIRECTION_INPUT = 0x1


class ENUM_UTIL_PIN_ENABLE(Enum):
    UTIL_PIN_DISABLE = 0x0
    UTIL_PIN_ENABLE = 0x1


class OFFSET_UTIL2_PIN_CTL:
    UTIL2_PIN_CTL = 0x48408


class _UTIL2_PIN_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 30),
        ('UtilPinDirection', ctypes.c_uint32, 1),
        ('UtilPinEnable', ctypes.c_uint32, 1),
    ]


class REG_UTIL2_PIN_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 30
    UtilPinDirection = 0  # bit 30 to 31
    UtilPinEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _UTIL2_PIN_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_UTIL2_PIN_CTL, self).__init__()
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


class ENUM_WD_VIDEO_TRANSLATION_SELECT(Enum):
    WD_VIDEO_TRANSLATION_SELECT_INTERNAL = 0x0  # WD video VTD translation in display engine
    WD_VIDEO_TRANSLATION_SELECT_EXTERNAL = 0x1  # WD video VTD translation in system agent


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
        ('DmcGtAccessDisable', ctypes.c_uint32, 1),
        ('DmcHipAccessDisable', ctypes.c_uint32, 1),
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
        ('WdVideoTranslationSelect', ctypes.c_uint32, 1),
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

    DisplayAudioCodecDisable = 0  # bit 0 to 1
    DisplayHdcpAksvReadEnable = 0  # bit 1 to 2
    DmcMemAccessDisable = 0  # bit 2 to 3
    DmcGtAccessDisable = 0  # bit 3 to 4
    DmcHipAccessDisable = 0  # bit 4 to 5
    DmcPavpSrDisable = 0  # bit 5 to 6
    DisplayRsbDisable = 0  # bit 6 to 7
    Spare7 = 0  # bit 7 to 8
    AudioCodecId = 0  # bit 8 to 16
    Spare16 = 0  # bit 16 to 17
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
    Spare27 = 0  # bit 27 to 28
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
        ('EnableIsochRequests', ctypes.c_uint32, 1),
        ('IsocRequestOverride', ctypes.c_uint32, 1),
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

    MaskLpIdleInFillDone = 0  # bit 0 to 1
    CounterCompare = 0  # bit 1 to 6
    StickyForPhase1Counter = 0  # bit 6 to 7
    DisablePhase1Counter = 0  # bit 7 to 8
    StickyForPhase2Counter = 0  # bit 8 to 9
    DisablePhase2Counter = 0  # bit 9 to 10
    MasksNo_Lp_PendingInMemup = 0  # bit 10 to 11
    MaskNo_Lp_PendingInFill = 0  # bit 11 to 12
    IpcDemoteOverride = 0  # bit 12 to 13
    OpenMipiDphyLatches = 0  # bit 13 to 14
    EnableIsochRequests = 0  # bit 14 to 15
    IsocRequestOverride = 0  # bit 15 to 16
    Dc5InProgress = 0  # bit 16 to 17
    DisableFusaErrorsPreventingDc6Entry = 0  # bit 17 to 18
    ForceAuxpowerreq = 0  # bit 18 to 19
    Spare19 = 0  # bit 19 to 20
    Spare20 = 0  # bit 20 to 21
    Vbi_Enable_Dc6V = 0  # bit 21 to 22
    MaskDc5_Dc6_OkFromDsbsls = 0  # bit 22 to 23
    MaskDewakeFromDsbsls = 0  # bit 23 to 24
    DelayIsolationCounter = 0  # bit 24 to 32

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
        ('MinBputDelay', ctypes.c_uint32, 2),
        ('BCredits', ctypes.c_uint32, 4),
        ('BwCredits', ctypes.c_uint32, 2),
        ('B2BTransactionsMax', ctypes.c_uint32, 5),
        ('RingStopAddress', ctypes.c_uint32, 4),
        ('Status', ctypes.c_uint32, 1),
    ]


class REG_MBUS_ABOX_CTL(ctypes.Union):
    value = 0
    offset = 0

    BtCreditsPool1 = 0  # bit 0 to 5
    B2BTransactionsDelay = 0  # bit 5 to 8
    BtCreditsPool2 = 0  # bit 8 to 13
    RegulateB2BTransactions = 0  # bit 13 to 14
    MinBputDelay = 0  # bit 14 to 16
    BCredits = 0  # bit 16 to 20
    BwCredits = 0  # bit 20 to 22
    B2BTransactionsMax = 0  # bit 22 to 27
    RingStopAddress = 0  # bit 27 to 31
    Status = 0  # bit 31 to 32

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

    Reserved0 = 0  # bit 0 to 16
    RegulateB2BTransactions = 0  # bit 16 to 17
    B2BTransactionsDelay = 0  # bit 17 to 20
    B2BTransactionsMax = 0  # bit 20 to 25
    Reserved25 = 0  # bit 25 to 27
    RingStopAddress = 0  # bit 27 to 31
    Status = 0  # bit 31 to 32

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
    ALLOW_B2B_APUT_BLOCK_B2B_APUTS = 0x0
    ALLOW_B2B_APUT_ALLOW_B2B_APUTS = 0x1


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
        ('BputThrottleMax', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 1),
        ('AllowB2BAput', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 7),
        ('Reserved20', ctypes.c_uint32, 6),
        ('MbusJoiningPipeSelect', ctypes.c_uint32, 3),
        ('Reserved29', ctypes.c_uint32, 1),
        ('HashingMode', ctypes.c_uint32, 1),
        ('MbusJoining', ctypes.c_uint32, 1),
    ]


class REG_MBUS_CTL(ctypes.Union):
    value = 0
    offset = 0

    Mbus2CringPacketDrop = 0  # bit 0 to 1
    Mbus1CringPacketDrop = 0  # bit 1 to 2
    Mbus2DringPacketDrop = 0  # bit 2 to 3
    Mbus1DringPacketDrop = 0  # bit 3 to 4
    Mbus2CringPacketErrorStatus = 0  # bit 4 to 5
    Mbus1CringPacketErrorStatus = 0  # bit 5 to 6
    Mbus2DringPacketErrorStatus = 0  # bit 6 to 7
    Mbus1DringPacketErrorStatus = 0  # bit 7 to 8
    BputThrottleMax = 0  # bit 8 to 11
    Reserved11 = 0  # bit 11 to 12
    AllowB2BAput = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 20
    Reserved20 = 0  # bit 20 to 26
    MbusJoiningPipeSelect = 0  # bit 26 to 29
    Reserved29 = 0  # bit 29 to 30
    HashingMode = 0  # bit 30 to 31
    MbusJoining = 0  # bit 31 to 32

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

    Reserved0 = 0  # bit 0 to 15
    BwPerformanceCountersEnable = 0  # bit 15 to 16
    TlbRequestTimer = 0  # bit 16 to 22
    Reserved22 = 0  # bit 22 to 23
    PlaneRequestTimer = 0  # bit 23 to 29
    Reserved29 = 0  # bit 29 to 30
    BwGlobalCounterClear = 0  # bit 30 to 31
    BwBuddyDisable = 0  # bit 31 to 32

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

    BwBuddyPageMask = 0  # bit 0 to 32

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

    ErrorMask = 0  # bit 0 to 32

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


class OFFSET_CLKGATE_DIS_5:
    CLKGATE_DIS_5 = 0x46540


class _CLKGATE_DIS_5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 3),
        ('DcusGatingDis', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 1),
        ('DplcSlGatingDis', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 1),
        ('Dacwd1GatingDis', ctypes.c_uint32, 1),
        ('Dacwr1GatingDis', ctypes.c_uint32, 1),
        ('Dacwr0GatingDis', ctypes.c_uint32, 1),
        ('Reserved10', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 2),
        ('DksGatingDis', ctypes.c_uint32, 1),
        ('DkGatingDis', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 1),
        ('DpceGatingDis', ctypes.c_uint32, 1),
        ('DkvmrGatingDis', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 1),
        ('Dacwd0GatingDis', ctypes.c_uint32, 1),
        ('DacfpGatingDis', ctypes.c_uint32, 1),
        ('DacrgGatingDis', ctypes.c_uint32, 1),
        ('VrdGatingDis', ctypes.c_uint32, 1),
        ('DacfeGatingDis', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 1),
        ('DkdbGatingDis', ctypes.c_uint32, 1),
        ('DwdciphGatingDis', ctypes.c_uint32, 1),
        ('DwdsGatingDis', ctypes.c_uint32, 1),
        ('DwdcGatingDis', ctypes.c_uint32, 1),
        ('DrwdGatingDis', ctypes.c_uint32, 1),
    ]


class REG_CLKGATE_DIS_5(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 3
    DcusGatingDis = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 5
    DplcSlGatingDis = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 7
    Dacwd1GatingDis = 0  # bit 7 to 8
    Dacwr1GatingDis = 0  # bit 8 to 9
    Dacwr0GatingDis = 0  # bit 9 to 10
    Reserved10 = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 14
    DksGatingDis = 0  # bit 14 to 15
    DkGatingDis = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 17
    DpceGatingDis = 0  # bit 17 to 18
    DkvmrGatingDis = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 20
    Dacwd0GatingDis = 0  # bit 20 to 21
    DacfpGatingDis = 0  # bit 21 to 22
    DacrgGatingDis = 0  # bit 22 to 23
    VrdGatingDis = 0  # bit 23 to 24
    DacfeGatingDis = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 26
    Reserved26 = 0  # bit 26 to 27
    DkdbGatingDis = 0  # bit 27 to 28
    DwdciphGatingDis = 0  # bit 28 to 29
    DwdsGatingDis = 0  # bit 29 to 30
    DwdcGatingDis = 0  # bit 30 to 31
    DrwdGatingDis = 0  # bit 31 to 32

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

