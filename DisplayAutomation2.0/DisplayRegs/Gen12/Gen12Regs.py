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
# @file Gen12Regs.py
# @brief contains Gen12Regs.py related register definitions

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
        ('Reserved0', ctypes.c_uint32, 4),
        ('ErrorInjectionFlipBits', ctypes.c_uint32, 2),
        ('Reserved6', ctypes.c_uint32, 1),
        ('EccErrorInjectionEnable', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 2),
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

    Reserved0 = 0  # bit 0 to 4
    ErrorInjectionFlipBits = 0  # bit 4 to 6
    Reserved6 = 0  # bit 6 to 7
    EccErrorInjectionEnable = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 12
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
        ('Spare21', ctypes.c_uint32, 1),
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
    Spare21 = 0  # bit 21 to 22
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


class OFFSET_CLKGATE_DIS_0:
    CLKGATE_DIS_0 = 0x46530


class _CLKGATE_DIS_0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DoledGatingDis', ctypes.c_uint32, 1),
        ('DbwGatingDis', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 7),
        ('DrobGatingDis', ctypes.c_uint32, 1),
        ('DrobRamGatingDis', ctypes.c_uint32, 1),
        ('DarbaGatingDis', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 4),
        ('Reserved16', ctypes.c_uint32, 4),
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
    DbwGatingDis = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 9
    DrobGatingDis = 0  # bit 9 to 10
    DrobRamGatingDis = 0  # bit 10 to 11
    DarbaGatingDis = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 16
    Reserved16 = 0  # bit 16 to 20
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
        ('Reserved11', ctypes.c_uint32, 8),
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
        ('VrhGatingDis', ctypes.c_uint32, 1),
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
    Reserved11 = 0  # bit 11 to 19
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
    VrhGatingDis = 0  # bit 31 to 32

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


class OFFSET_CLKGATE_DIS_MISC:
    CLKGATE_DIS_MISC = 0x46534


class _CLKGATE_DIS_MISC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 11),
        ('DcmpGatingDis', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 7),
        ('DmasdGatingDis', ctypes.c_uint32, 1),
        ('DmascRamGatingDis', ctypes.c_uint32, 1),
        ('DmascGatingDis', ctypes.c_uint32, 1),
        ('Reserved22', ctypes.c_uint32, 6),
        ('DbufRamGatingDis', ctypes.c_uint32, 1),
        ('DbufGatingDis', ctypes.c_uint32, 1),
        ('DbrcGatingDis', ctypes.c_uint32, 1),
        ('DciphGatingDis', ctypes.c_uint32, 1),
    ]


class REG_CLKGATE_DIS_MISC(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 11
    DcmpGatingDis = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 19
    DmasdGatingDis = 0  # bit 19 to 20
    DmascRamGatingDis = 0  # bit 20 to 21
    DmascGatingDis = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 28
    DbufRamGatingDis = 0  # bit 28 to 29
    DbufGatingDis = 0  # bit 29 to 30
    DbrcGatingDis = 0  # bit 30 to 31
    DciphGatingDis = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CLKGATE_DIS_MISC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CLKGATE_DIS_MISC, self).__init__()
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
    MBUS_ABOX_CTL = 0x45038
    MBUS_ABOX1_CTL = 0x45048
    MBUS_ABOX2_CTL = 0x4504C


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

    BtCreditsPool1 = 0  # bit 0 to 5
    B2BTransactionsDelay = 0  # bit 5 to 8
    BtCreditsPool2 = 0  # bit 8 to 13
    RegulateB2BTransactions = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 16
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


class ENUM_BW_PERFORMANCE_COUNTERS_ENABLE(Enum):
    BW_PERFORMANCE_COUNTERS_DISABLED = 0x0
    BW_PERFORMANCE_COUNTERS_ENABLED = 0x1


class ENUM_TLB_REQUEST_TIMER(Enum):
    TLB_REQUEST_TIMER_8 = 0x10


class ENUM_PLANE_REQUEST_TIMER(Enum):
    PLANE_REQUEST_TIMER_16 = 0x10


class ENUM_BW_GLOBAL_COUNTER_CLEAR(Enum):
    BW_GLOBAL_COUNTER_CLEAR_CLEAR = 0x1
    BW_GLOBAL_COUNTER_CLEAR_DO_NOT_CLEAR = 0x0


class ENUM_BW_BUDDY_DISABLE(Enum):
    BW_BUDDY_ENABLED = 0x0
    BW_BUDDY_DISABLED = 0x1


class OFFSET_BW_BUDDY_CTL:
    BW_BUDDY1_CTL = 0x45140
    BW_BUDDY2_CTL = 0x45150


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
    BW_BUDDY1_PAGE_MASK = 0x45144
    BW_BUDDY2_PAGE_MASK = 0x45154


class _BW_BUDDY_PAGE_MASK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BwBuddyPageMask', ctypes.c_uint32, 28),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_BW_BUDDY_PAGE_MASK(ctypes.Union):
    value = 0
    offset = 0

    BwBuddyPageMask = 0  # bit 0 to 28
    Reserved28 = 0  # bit 28 to 32

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


class ENUM_DISABLE_E2E_HOTSPOT_AVOIDANCE(Enum):
    DISABLE_E2E_HOTSPOT_AVOIDANCE_ENABLED = 0x0  # Hotspot avoidance algorithm is applied.
    DISABLE_E2E_HOTSPOT_AVOIDANCE_DISABLED = 0x1  # No hotspot avoidance algorithm is applied.


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
        ('DisableE2EHotspotAvoidance', ctypes.c_uint32, 1),
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
        ('Spare30', ctypes.c_uint32, 1),
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
    DisableE2EHotspotAvoidance = 0  # bit 15 to 16
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
    Spare30 = 0  # bit 30 to 31
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

