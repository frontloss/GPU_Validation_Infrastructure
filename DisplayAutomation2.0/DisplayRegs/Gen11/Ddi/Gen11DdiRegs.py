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
# @file Gen11DdiRegs.py
# @brief contains Gen11DdiRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_INIT_DISPLAY_DETECTED(Enum):
    INIT_DISPLAY_DETECTED_NOT_DETECTED = 0x0  # Digital display not detected during initialization
    INIT_DISPLAY_DETECTED_DETECTED = 0x1  # Digital display detected during initialization


class ENUM_DP_PORT_WIDTH_SELECTION(Enum):
    DP_PORT_WIDTH_SELECTION_X1 = 0x0  # x1 Mode
    DP_PORT_WIDTH_SELECTION_X2 = 0x1  # x2 Mode
    DP_PORT_WIDTH_SELECTION_X4 = 0x3  # x4 Mode


class ENUM_DDI_IDLE_STATUS(Enum):
    DDI_IDLE_STATUS_BUFFER_NOT_IDLE = 0x0
    DDI_IDLE_STATUS_BUFFER_IDLE = 0x1


class ENUM_PORT_REVERSAL(Enum):
    PORT_REVERSAL_NOT_REVERSED = 0x0
    PORT_REVERSAL_REVERSED = 0x1


class ENUM_PHY_PARAM_ADJUST(Enum):
    PHY_PARAM_ADJUST_ENABLE = 0x1
    PHY_PARAM_ADJUST_DISABLE = 0x0


class ENUM_OVERRIDE_TRAINING_ENABLE(Enum):
    OVERRIDE_TRAINING_ENABLE_OVERRIDE = 0x1
    OVERRIDE_TRAINING_DISABLE_OVERRIDE = 0x0


class ENUM_DDI_BUFFER_ENABLE(Enum):
    DDI_BUFFER_DISABLE = 0x0
    DDI_BUFFER_ENABLE = 0x1


class OFFSET_DDI_BUF_CTL:
    DDI_BUF_CTL_A = 0x64000
    DDI_BUF_CTL_B = 0x64100
    DDI_BUF_CTL_C = 0x64200
    DDI_BUF_CTL_D = 0x64300
    DDI_BUF_CTL_E = 0x64400
    DDI_BUF_CTL_F = 0x64500


class _DDI_BUF_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('InitDisplayDetected', ctypes.c_uint32, 1),
        ('DpPortWidthSelection', ctypes.c_uint32, 3),
        ('Reserved4', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 2),
        ('DdiIdleStatus', ctypes.c_uint32, 1),
        ('UsbTypeCDpLaneStaggeringDelay', ctypes.c_uint32, 8),
        ('PortReversal', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 7),
        ('Reserved24', ctypes.c_uint32, 4),
        ('PhyParamAdjust', ctypes.c_uint32, 1),
        ('OverrideTrainingEnable', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('DdiBufferEnable', ctypes.c_uint32, 1),
    ]


class REG_DDI_BUF_CTL(ctypes.Union):
    value = 0
    offset = 0

    InitDisplayDetected = 0  # bit 0 to 1
    DpPortWidthSelection = 0  # bit 1 to 4
    Reserved4 = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 7
    DdiIdleStatus = 0  # bit 7 to 8
    UsbTypeCDpLaneStaggeringDelay = 0  # bit 8 to 16
    PortReversal = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 24
    Reserved24 = 0  # bit 24 to 28
    PhyParamAdjust = 0  # bit 28 to 29
    OverrideTrainingEnable = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 31
    DdiBufferEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DDI_BUF_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DDI_BUF_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ALTERNATE_SR_ENABLE(Enum):
    ALTERNATE_SR_DISABLE = 0x0
    ALTERNATE_SR_ENABLE = 0x1


class ENUM_SCRAMBLING_DISABLE(Enum):
    SCRAMBLING_ENABLE = 0x0  # Enable scrambling
    SCRAMBLING_DISABLE = 0x1  # Disable scrambling


class ENUM_DP_LINK_TRAINING_ENABLE(Enum):
    DP_LINK_TRAINING_ENABLE_PATTERN_1 = 0x0  # Training Pattern 1 enabled
    DP_LINK_TRAINING_ENABLE_PATTERN_2 = 0x1  # Training Pattern 2 enabled
    DP_LINK_TRAINING_ENABLE_IDLE = 0x2  # Idle Pattern enabled
    DP_LINK_TRAINING_ENABLE_NORMAL = 0x3  # Link not in training: Send normal pixels
    DP_LINK_TRAINING_ENABLE_PATTERN_3 = 0x4  # Training Pattern 3 enabled
    DP_LINK_TRAINING_ENABLE_PATTERN_4 = 0x5  # Training Pattern 4 enabled


class ENUM_ENHANCED_FRAMING_ENABLE(Enum):
    ENHANCED_FRAMING_DISABLED = 0x0
    ENHANCED_FRAMING_ENABLED = 0x1


class ENUM_TRAINING_PATTERN_4_SELECT(Enum):
    TRAINING_PATTERN_4_SELECT_TRAINING_PATTERN_4A = 0x0  # CP2520 Pattern 3 :SR-BS-BS-SR-248 00hs (after data symbol sc
                                                         # rambling and ANSI8B/10B coding)
    TRAINING_PATTERN_4_SELECT_TRAINING_PATTERN_4B = 0x1  # CP2520 Pattern 2 :SR-BF-BF-SR-248 00hs (after data symbol sc
                                                         # rambling and ANSI8B/10B coding)
    TRAINING_PATTERN_4_SELECT_TRAINING_PATTERN_4C = 0x2  # CP2520 Pattern 1 :SR-CP-CP-SR-248 of 00hs (after data symbol
                                                         #  scrambling and ANSI8B/10B coding)


class ENUM_FORCE_ACT(Enum):
    FORCE_ACT_DO_NOT_FORCE = 0x0  # Do not force ACT to be sent
    FORCE_ACT_FORCE = 0x1  # Force ACT to be sent one time


class ENUM_TRANSPORT_MODE_SELECT(Enum):
    TRANSPORT_MODE_SELECT_SST_MODE = 0x0  # DisplayPort SST mode
    TRANSPORT_MODE_SELECT_MST_MODE = 0x1  # DisplayPort MST mode


class ENUM_FEC_ENABLE(Enum):
    FEC_DISABLE = 0x0
    FEC_ENABLE = 0x1


class ENUM_TRANSPORT_ENABLE(Enum):
    TRANSPORT_DISABLE = 0x0
    TRANSPORT_ENABLE = 0x1


class OFFSET_DP_TP_CTL:
    DP_TP_CTL_A = 0x64040
    DP_TP_CTL_B = 0x64140
    DP_TP_CTL_C = 0x64240
    DP_TP_CTL_D = 0x64340
    DP_TP_CTL_E = 0x64440
    DP_TP_CTL_F = 0x64540


class _DP_TP_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 6),
        ('AlternateSrEnable', ctypes.c_uint32, 1),
        ('ScramblingDisable', ctypes.c_uint32, 1),
        ('DpLinkTrainingEnable', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 4),
        ('Reserved15', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 2),
        ('EnhancedFramingEnable', ctypes.c_uint32, 1),
        ('TrainingPattern4Select', ctypes.c_uint32, 2),
        ('Reserved21', ctypes.c_uint32, 4),
        ('ForceAct', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 1),
        ('TransportModeSelect', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 2),
        ('FecEnable', ctypes.c_uint32, 1),
        ('TransportEnable', ctypes.c_uint32, 1),
    ]


class REG_DP_TP_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 6
    AlternateSrEnable = 0  # bit 6 to 7
    ScramblingDisable = 0  # bit 7 to 8
    DpLinkTrainingEnable = 0  # bit 8 to 11
    Reserved11 = 0  # bit 11 to 15
    Reserved15 = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 18
    EnhancedFramingEnable = 0  # bit 18 to 19
    TrainingPattern4Select = 0  # bit 19 to 21
    Reserved21 = 0  # bit 21 to 25
    ForceAct = 0  # bit 25 to 26
    Reserved26 = 0  # bit 26 to 27
    TransportModeSelect = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 30
    FecEnable = 0  # bit 30 to 31
    TransportEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DP_TP_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DP_TP_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PAYLOAD_MAPPING_VC0(Enum):
    PAYLOAD_MAPPING_VC0_A = 0x0  # Transcoder A mapped to this VC
    PAYLOAD_MAPPING_VC0_B = 0x1  # Transcoder B mapped to this VC
    PAYLOAD_MAPPING_VC0_C = 0x2  # Transcoder C mapped to this VC


class ENUM_PAYLOAD_MAPPING_VC1(Enum):
    PAYLOAD_MAPPING_VC1_A = 0x0  # Transcoder A mapped to this VC
    PAYLOAD_MAPPING_VC1_B = 0x1  # Transcoder B mapped to this VC
    PAYLOAD_MAPPING_VC1_C = 0x2  # Transcoder C mapped to this VC


class ENUM_PAYLOAD_MAPPING_VC2(Enum):
    PAYLOAD_MAPPING_VC2_A = 0x0  # Transcoder A mapped to this VC
    PAYLOAD_MAPPING_VC2_B = 0x1  # Transcoder B mapped to this VC
    PAYLOAD_MAPPING_VC2_C = 0x2  # Transcoder C mapped to this VC


class ENUM_STREAMS_ENABLED(Enum):
    STREAMS_ENABLED_ZERO = 0x0  # Zero streams enabled
    STREAMS_ENABLED_ONE = 0x1  # One stream enabled
    STREAMS_ENABLED_TWO = 0x2  # Two streams enabled
    STREAMS_ENABLED_THREE = 0x3  # Three streams enabled


class ENUM_MODE_STATUS(Enum):
    MODE_STATUS_SST = 0x0  # Single-stream mode
    MODE_STATUS_MST = 0x1  # Multi-stream mode


class ENUM_ACT_SENT_STATUS(Enum):
    ACT_SENT_STATUS_ACT_NOT_SENT = 0x0
    ACT_SENT_STATUS_ACT_SENT = 0x1


class ENUM_MIN_IDLES_SENT(Enum):
    MIN_IDLES_SENT_MIN_IDLES_NOT_SENT = 0x0
    MIN_IDLES_SENT_MIN_IDLES_SENT = 0x1


class ENUM_ACTIVE_LINK_FRAME_STATUS(Enum):
    ACTIVE_LINK_FRAME_STATUS_ACTIVE_LINK_FRAME_NOT_SENT = 0x0
    ACTIVE_LINK_FRAME_STATUS_ACTIVE_LINK_FRAME_SENT = 0x1


class ENUM_IDLE_LINK_FRAME_STATUS(Enum):
    IDLE_LINK_FRAME_STATUS_IDLE_LINK_FRAME_NOT_SENT = 0x0
    IDLE_LINK_FRAME_STATUS_IDLE_LINK_FRAME_SENT = 0x1


class OFFSET_DP_TP_STATUS:
    DP_TP_STATUS_B = 0x64144
    DP_TP_STATUS_C = 0x64244
    DP_TP_STATUS_D = 0x64344
    DP_TP_STATUS_E = 0x64444
    DP_TP_STATUS_F = 0x64544


class _DP_TP_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PayloadMappingVc0', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 2),
        ('PayloadMappingVc1', ctypes.c_uint32, 2),
        ('Reserved6', ctypes.c_uint32, 2),
        ('PayloadMappingVc2', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 2),
        ('Reserved12', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 3),
        ('StreamsEnabled', ctypes.c_uint32, 2),
        ('Reserved18', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 4),
        ('ModeStatus', ctypes.c_uint32, 1),
        ('ActSentStatus', ctypes.c_uint32, 1),
        ('MinIdlesSent', ctypes.c_uint32, 1),
        ('ActiveLinkFrameStatus', ctypes.c_uint32, 1),
        ('IdleLinkFrameStatus', ctypes.c_uint32, 1),
        ('FecEnableLiveStatus', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_DP_TP_STATUS(ctypes.Union):
    value = 0
    offset = 0

    PayloadMappingVc0 = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 4
    PayloadMappingVc1 = 0  # bit 4 to 6
    Reserved6 = 0  # bit 6 to 8
    PayloadMappingVc2 = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 12
    Reserved12 = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 16
    StreamsEnabled = 0  # bit 16 to 18
    Reserved18 = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 23
    ModeStatus = 0  # bit 23 to 24
    ActSentStatus = 0  # bit 24 to 25
    MinIdlesSent = 0  # bit 25 to 26
    ActiveLinkFrameStatus = 0  # bit 26 to 27
    IdleLinkFrameStatus = 0  # bit 27 to 28
    FecEnableLiveStatus = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DP_TP_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DP_TP_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_LINK_QUAL_PATTERN_SET(Enum):
    LINK_QUAL_PATTERN_SET_D10_2_UNSCRAMBLED = 0x0  # Unscrambled D10.2 test pattern
    LINK_QUAL_PATTERN_SET_SCRAMBLED_0S = 0x1  # Scrambled 0s symbol error rate measurement pattern
    LINK_QUAL_PATTERN_SET_PRBS7 = 0x2  # PRBS7 pattern
    LINK_QUAL_PATTERN_SET_CUSTOM = 0x3  # Custom 80 bit pattern
    LINK_QUAL_PATTERN_SET_HBR2 = 0x4  # HBR2 compliance eye pattern. The length of the pattern must be programmed in HB
                                      # R2 Scrambler Reset.
    LINK_QUAL_PATTERN_SET_SCRAMBLED_1S = 0x5  # Scrambled 1s pattern


class ENUM_TEST_PATTERN_ENABLE(Enum):
    TEST_PATTERN_DISABLE = 0x0
    TEST_PATTERN_ENABLE = 0x1


class OFFSET_DP_COMP_CTL:
    DP_COMP_CTL_A = 0x640F0
    DP_COMP_CTL_B = 0x641F0
    DP_COMP_CTL_C = 0x642F0
    DP_COMP_CTL_D = 0x643F0
    DP_COMP_CTL_E = 0x644F0
    DP_COMP_CTL_F = 0x645F0


class _DP_COMP_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hbr2ScramblerReset', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 12),
        ('LinkQualPatternSet', ctypes.c_uint32, 3),
        ('TestPatternEnable', ctypes.c_uint32, 1),
    ]


class REG_DP_COMP_CTL(ctypes.Union):
    value = 0
    offset = 0

    Hbr2ScramblerReset = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 28
    LinkQualPatternSet = 0  # bit 28 to 31
    TestPatternEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DP_COMP_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DP_COMP_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DP_COMP_PAT:
    DP_COMP_PAT_A_ = 0x640F4
    DP_COMP_PAT_B_ = 0x641F4
    DP_COMP_PAT_C_ = 0x642F4
    DP_COMP_PAT_D_ = 0x643F4
    DP_COMP_PAT_E_ = 0x644F4
    DP_COMP_PAT_F_ = 0x645F4


class _DP_COMP_PAT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CompliancePattern310', ctypes.c_uint32, 32),
        ('CompliancePattern6332', ctypes.c_uint32, 32),
        ('CompliancePattern7964', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DP_COMP_PAT(ctypes.Union):
    value = 0
    offset = 0

    CompliancePattern310 = 0  # bit 0 to 32
    CompliancePattern6332 = 0  # bit 0 to 32
    CompliancePattern7964 = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DP_COMP_PAT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DP_COMP_PAT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PHY_MISC:
    PHY_MISC_A = 0x64C00
    PHY_MISC_B = 0x64C04


class _PHY_MISC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 20),
        ('Spare20', ctypes.c_uint32, 1),
        ('Spare21', ctypes.c_uint32, 1),
        ('Spare22', ctypes.c_uint32, 1),
        ('DeToIoCompPwrDown', ctypes.c_uint32, 1),
        ('IoToDeMisc', ctypes.c_uint32, 4),
        ('DeToIoMisc', ctypes.c_uint32, 4),
    ]


class REG_PHY_MISC(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 20
    Spare20 = 0  # bit 20 to 21
    Spare21 = 0  # bit 21 to 22
    Spare22 = 0  # bit 22 to 23
    DeToIoCompPwrDown = 0  # bit 23 to 24
    IoToDeMisc = 0  # bit 24 to 28
    DeToIoMisc = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PHY_MISC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PHY_MISC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PERIODIC_COMP_COUNTER(Enum):
    PERIODIC_COMP_COUNTER_1_25MS = 0x5F  # Period of ~ 1.25ms w.r.t sus clock frequency of 19.2MHz.
    PERIODIC_COMP_COUNTER_10US = 0x1  # Period of ~10us w.r.t sus clock frequency of 19.2MHz.


class OFFSET_PORT_COMP_DW0:
    PORT_COMP_DW0_B = 0x6C100
    PORT_COMP_DW0_A = 0x162100


class _PORT_COMP_DW0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 8),
        ('PeriodicCompCounter', ctypes.c_uint32, 12),
        ('Reserved20', ctypes.c_uint32, 3),
        ('ProcmonClockSel', ctypes.c_uint32, 1),
        ('CompSpare', ctypes.c_uint32, 2),
        ('TxDrvswCtl', ctypes.c_uint32, 1),
        ('TxDrvswOn', ctypes.c_uint32, 2),
        ('TxSlewCtl', ctypes.c_uint32, 2),
        ('CompInit', ctypes.c_uint32, 1),
    ]


class REG_PORT_COMP_DW0(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 8
    PeriodicCompCounter = 0  # bit 8 to 20
    Reserved20 = 0  # bit 20 to 23
    ProcmonClockSel = 0  # bit 23 to 24
    CompSpare = 0  # bit 24 to 26
    TxDrvswCtl = 0  # bit 26 to 27
    TxDrvswOn = 0  # bit 27 to 29
    TxSlewCtl = 0  # bit 29 to 31
    CompInit = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_COMP_DW1:
    PORT_COMP_DW1_B = 0x6C104
    PORT_COMP_DW1_A = 0x162104


class _PORT_COMP_DW1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Nlvt_Ref_Lowval98', ctypes.c_uint32, 2),
        ('Nlvt_Ref_Highval98', ctypes.c_uint32, 2),
        ('Plvt_Ref_Lowval98', ctypes.c_uint32, 2),
        ('Plvt_Ref_Highval98', ctypes.c_uint32, 2),
        ('Nhvt_Ref_Lowval98', ctypes.c_uint32, 2),
        ('Nhvt_Ref_Highval98', ctypes.c_uint32, 2),
        ('Phvt_Ref_Lowval98', ctypes.c_uint32, 2),
        ('Phvt_Ref_Highval98', ctypes.c_uint32, 2),
        ('N_Ref_Lowval98', ctypes.c_uint32, 2),
        ('N_Ref_Highval98', ctypes.c_uint32, 2),
        ('P_Ref_Lowval98', ctypes.c_uint32, 2),
        ('P_Ref_Highval98', ctypes.c_uint32, 2),
        ('Rcomp_En', ctypes.c_uint32, 1),
        ('Fcomp_Polaritysel', ctypes.c_uint32, 1),
        ('Fcomp_Inputsel_Ovrd', ctypes.c_uint32, 2),
        ('Fcomp_Bias_Sel', ctypes.c_uint32, 1),
        ('Fcomp_Capratio', ctypes.c_uint32, 1),
        ('Fcomp_Ovrd_En', ctypes.c_uint32, 1),
        ('Ldo_Bypass', ctypes.c_uint32, 1),
    ]


class REG_PORT_COMP_DW1(ctypes.Union):
    value = 0
    offset = 0

    Nlvt_Ref_Lowval98 = 0  # bit 0 to 2
    Nlvt_Ref_Highval98 = 0  # bit 2 to 4
    Plvt_Ref_Lowval98 = 0  # bit 4 to 6
    Plvt_Ref_Highval98 = 0  # bit 6 to 8
    Nhvt_Ref_Lowval98 = 0  # bit 8 to 10
    Nhvt_Ref_Highval98 = 0  # bit 10 to 12
    Phvt_Ref_Lowval98 = 0  # bit 12 to 14
    Phvt_Ref_Highval98 = 0  # bit 14 to 16
    N_Ref_Lowval98 = 0  # bit 16 to 18
    N_Ref_Highval98 = 0  # bit 18 to 20
    P_Ref_Lowval98 = 0  # bit 20 to 22
    P_Ref_Highval98 = 0  # bit 22 to 24
    Rcomp_En = 0  # bit 24 to 25
    Fcomp_Polaritysel = 0  # bit 25 to 26
    Fcomp_Inputsel_Ovrd = 0  # bit 26 to 28
    Fcomp_Bias_Sel = 0  # bit 28 to 29
    Fcomp_Capratio = 0  # bit 29 to 30
    Fcomp_Ovrd_En = 0  # bit 30 to 31
    Ldo_Bypass = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_VOLTAGE_INFO(Enum):
    VOLTAGE_INFO_0_85V = 0x0
    VOLTAGE_INFO_0_95V = 0x1
    VOLTAGE_INFO_1_05 = 0x2


class ENUM_PROCESS_INFO(Enum):
    PROCESS_INFO_DOT0 = 0x0
    PROCESS_INFO_DOT1 = 0x1
    PROCESS_INFO_DOT4 = 0x2


class OFFSET_PORT_COMP_DW3:
    PORT_COMP_DW3_B = 0x6C10C
    PORT_COMP_DW3_A = 0x16210C


class _PORT_COMP_DW3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MipiLpdnCode', ctypes.c_uint32, 6),
        ('LpdnCodeMinout', ctypes.c_uint32, 1),
        ('LpdnCodeMaxout', ctypes.c_uint32, 1),
        ('IcompCode', ctypes.c_uint32, 7),
        ('Reserved15', ctypes.c_uint32, 4),
        ('IcompCodeMinout', ctypes.c_uint32, 1),
        ('IcompCodeMaxout', ctypes.c_uint32, 1),
        ('ProcmonDone', ctypes.c_uint32, 1),
        ('FirstCompDone', ctypes.c_uint32, 1),
        ('PllDdiPwrAck', ctypes.c_uint32, 1),
        ('VoltageInfo', ctypes.c_uint32, 2),
        ('ProcessInfo', ctypes.c_uint32, 3),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PORT_COMP_DW3(ctypes.Union):
    value = 0
    offset = 0

    MipiLpdnCode = 0  # bit 0 to 6
    LpdnCodeMinout = 0  # bit 6 to 7
    LpdnCodeMaxout = 0  # bit 7 to 8
    IcompCode = 0  # bit 8 to 15
    Reserved15 = 0  # bit 15 to 19
    IcompCodeMinout = 0  # bit 19 to 20
    IcompCodeMaxout = 0  # bit 20 to 21
    ProcmonDone = 0  # bit 21 to 22
    FirstCompDone = 0  # bit 22 to 23
    PllDdiPwrAck = 0  # bit 23 to 24
    VoltageInfo = 0  # bit 24 to 26
    ProcessInfo = 0  # bit 26 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PRDIC_ICOMP_DIS(Enum):
    PRDIC_ICOMP_DIS_ENABLE = 0x0
    PRDIC_ICOMP_DIS_DISABLE = 0x1


class ENUM_IREFGEN(Enum):
    IREFGEN_ENABLE = 0x1
    IREFGEN_DISABLE = 0x0


class OFFSET_PORT_COMP_DW8:
    PORT_COMP_DW8_B = 0x6C120
    PORT_COMP_DW8_A = 0x162120


class _PORT_COMP_DW8(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 14),
        ('Prdic_Icomp_Dis', ctypes.c_uint32, 1),
        ('Spare2315', ctypes.c_uint32, 9),
        ('Irefgen', ctypes.c_uint32, 1),
        ('Spare3125', ctypes.c_uint32, 7),
    ]


class REG_PORT_COMP_DW8(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 14
    Prdic_Icomp_Dis = 0  # bit 14 to 15
    Spare2315 = 0  # bit 15 to 24
    Irefgen = 0  # bit 24 to 25
    Spare3125 = 0  # bit 25 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW8),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW8, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_COMP_DW9:
    PORT_COMP_DW9_B = 0x6C124
    PORT_COMP_DW9_A = 0x162124


class _PORT_COMP_DW9(ctypes.LittleEndianStructure):
    _fields_ = [
        ('P_Ref_Highval70', ctypes.c_uint32, 8),
        ('P_Ref_Lowval70', ctypes.c_uint32, 8),
        ('N_Ref_Highval70', ctypes.c_uint32, 8),
        ('N_Ref_Lowval70', ctypes.c_uint32, 8),
    ]


class REG_PORT_COMP_DW9(ctypes.Union):
    value = 0
    offset = 0

    P_Ref_Highval70 = 0  # bit 0 to 8
    P_Ref_Lowval70 = 0  # bit 8 to 16
    N_Ref_Highval70 = 0  # bit 16 to 24
    N_Ref_Lowval70 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW9),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW9, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_COMP_DW10:
    PORT_COMP_DW10_B = 0x6C128
    PORT_COMP_DW10_A = 0x162128


class _PORT_COMP_DW10(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Plvt_Ref_Highval70', ctypes.c_uint32, 8),
        ('Plvt_Ref_Lowval70', ctypes.c_uint32, 8),
        ('Nlvt_Ref_Highval70', ctypes.c_uint32, 8),
        ('Nlvt_Ref_Lowval70', ctypes.c_uint32, 8),
    ]


class REG_PORT_COMP_DW10(ctypes.Union):
    value = 0
    offset = 0

    Plvt_Ref_Highval70 = 0  # bit 0 to 8
    Plvt_Ref_Lowval70 = 0  # bit 8 to 16
    Nlvt_Ref_Highval70 = 0  # bit 16 to 24
    Nlvt_Ref_Lowval70 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_COMP_DW10),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_COMP_DW10, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CL_POWER_DOWN_ENABLE(Enum):
    CL_POWER_DOWN_DISABLE = 0x0
    CL_POWER_DOWN_ENABLE = 0x1


class OFFSET_PORT_CL_DW5:
    PORT_CL_DW5_B = 0x6C014
    PORT_CL_DW5_A = 0x162014


class _PORT_CL_DW5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SusClockConfig', ctypes.c_uint32, 2),
        ('PhyPowerAckOverride', ctypes.c_uint32, 1),
        ('CriClockSelect', ctypes.c_uint32, 1),
        ('ClPowerDownEnable', ctypes.c_uint32, 1),
        ('PgStaggeringControlDisable', ctypes.c_uint32, 1),
        ('EnablePortStaggering', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 1),
        ('DlBroadcastEnable', ctypes.c_uint32, 1),
        ('IosfClkdivSel', ctypes.c_uint32, 3),
        ('Reserved12', ctypes.c_uint32, 1),
        ('IosfPdCount', ctypes.c_uint32, 2),
        ('Reserved15', ctypes.c_uint32, 1),
        ('CriClockCountMax', ctypes.c_uint32, 4),
        ('FuseRepull', ctypes.c_uint32, 1),
        ('FusevalidOverride', ctypes.c_uint32, 1),
        ('FusevalidReset', ctypes.c_uint32, 1),
        ('Reserved23', ctypes.c_uint32, 1),
        ('Force', ctypes.c_uint32, 8),
    ]


class REG_PORT_CL_DW5(ctypes.Union):
    value = 0
    offset = 0

    SusClockConfig = 0  # bit 0 to 2
    PhyPowerAckOverride = 0  # bit 2 to 3
    CriClockSelect = 0  # bit 3 to 4
    ClPowerDownEnable = 0  # bit 4 to 5
    PgStaggeringControlDisable = 0  # bit 5 to 6
    EnablePortStaggering = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 8
    DlBroadcastEnable = 0  # bit 8 to 9
    IosfClkdivSel = 0  # bit 9 to 12
    Reserved12 = 0  # bit 12 to 13
    IosfPdCount = 0  # bit 13 to 15
    Reserved15 = 0  # bit 15 to 16
    CriClockCountMax = 0  # bit 16 to 20
    FuseRepull = 0  # bit 20 to 21
    FusevalidOverride = 0  # bit 21 to 22
    FusevalidReset = 0  # bit 22 to 23
    Reserved23 = 0  # bit 23 to 24
    Force = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CL_DW5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CL_DW5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_STATIC_POWER_DOWN_DDI(Enum):
    STATIC_POWER_DOWN_DDI_POWER_UP_ALL_LANES = 0x0  # Enable x4
    STATIC_POWER_DOWN_DDI_POWER_DOWN_LANES_3_2 = 0xC  # Enable x2
    STATIC_POWER_DOWN_DDI_POWER_DOWN_LANES_3_2_1 = 0xE  # Enable x1
    STATIC_POWER_DOWN_DDI_POWER_DOWN_LANES_1_0 = 0x3  # Enable x2 Reversed
    STATIC_POWER_DOWN_DDI_POWER_DOWN_LANES_2_1_0 = 0x7  # Enable x1 Reversed
    STATIC_POWER_DOWN_DDI_POWER_DOWN_LANES_3 = 0x8  # Enable DSI x3
    STATIC_POWER_DOWN_DDI_POWER_DOWN_LANES_3_1 = 0xA  # Enable DSI x2
    STATIC_POWER_DOWN_DDI_POWER_DOWN_LANES_3_1_0 = 0xB  # Enable DSI x1


class ENUM_PG_SEQ_DELAY_OVERRIDE_ENABLE(Enum):
    PG_SEQ_DELAY_OVERRIDE_DISABLE = 0x0
    PG_SEQ_DELAY_OVERRIDE_ENABLE = 0x1


class OFFSET_PORT_CL_DW10:
    PORT_CL_DW10_B = 0x6C028
    PORT_CL_DW10_A = 0x162028


class _PORT_CL_DW10(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 4),
        ('StaticPowerDownDdi', ctypes.c_uint32, 4),
        ('Reserved8', ctypes.c_uint32, 8),
        ('Ospare_Cri_Ret_5_0', ctypes.c_uint32, 6),
        ('Ohvpg_Ctrl_Mipic', ctypes.c_uint32, 1),
        ('Ohvpg_Ctrl_Mipia', ctypes.c_uint32, 1),
        ('PgSeqDelayOverrideEnable', ctypes.c_uint32, 1),
        ('PgSeqDelayOverride', ctypes.c_uint32, 2),
        ('Reserved27', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_PORT_CL_DW10(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 4
    StaticPowerDownDdi = 0  # bit 4 to 8
    Reserved8 = 0  # bit 8 to 16
    Ospare_Cri_Ret_5_0 = 0  # bit 16 to 22
    Ohvpg_Ctrl_Mipic = 0  # bit 22 to 23
    Ohvpg_Ctrl_Mipia = 0  # bit 23 to 24
    PgSeqDelayOverrideEnable = 0  # bit 24 to 25
    PgSeqDelayOverride = 0  # bit 25 to 27
    Reserved27 = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CL_DW10),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CL_DW10, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_LANE_ENABLE_AUX(Enum):
    LANE_ENABLE_AUX_DISABLE = 0x0
    LANE_ENABLE_AUX_ENABLE = 0x1


class ENUM_PWR_REQ_OVERRIDE_ENABLE_AUX(Enum):
    PWR_REQ_OVERRIDE_ENABLE_AUX_DISABLE = 0x0
    PWR_REQ_OVERRIDE_ENABLE_AUX_ENABLE = 0x1


class ENUM_MIPI_LANE_ENABLE(Enum):
    MIPI_LANE_DISABLE = 0x0
    MIPI_LANE_ENABLE = 0x1


class OFFSET_PORT_CL_DW12:
    PORT_CL_DW12_B = 0x6C030
    PORT_CL_DW12_A = 0x162030


class _PORT_CL_DW12(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LaneEnableAux', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 3),
        ('PowerAckAux', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 1),
        ('PhyStatusAux', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 3),
        ('PwrReqOverrideEnableAux', ctypes.c_uint32, 1),
        ('PwrReqOverrideAux', ctypes.c_uint32, 1),
        ('Reserved12', ctypes.c_uint32, 14),
        ('MipiModeOverride', ctypes.c_uint32, 1),
        ('MipiModeOverrideEnable', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 1),
        ('MipiLaneEnable', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PORT_CL_DW12(ctypes.Union):
    value = 0
    offset = 0

    LaneEnableAux = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 4
    PowerAckAux = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 6
    PhyStatusAux = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 10
    PwrReqOverrideEnableAux = 0  # bit 10 to 11
    PwrReqOverrideAux = 0  # bit 11 to 12
    Reserved12 = 0  # bit 12 to 26
    MipiModeOverride = 0  # bit 26 to 27
    MipiModeOverrideEnable = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 29
    MipiLaneEnable = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CL_DW12),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CL_DW12, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_CL_DW15:
    PORT_CL_DW15_B = 0x6C03C
    PORT_CL_DW15_A = 0x16203C


class _PORT_CL_DW15(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 17),
        ('PowerAckAux', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 3),
        ('PowerReqAux', ctypes.c_uint32, 1),
        ('Reserved22', ctypes.c_uint32, 5),
        ('PowerAckMipi', ctypes.c_uint32, 1),
        ('HvpgEnableStatus', ctypes.c_uint32, 1),
        ('HvpgPowerAck', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PORT_CL_DW15(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 17
    PowerAckAux = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 21
    PowerReqAux = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 27
    PowerAckMipi = 0  # bit 27 to 28
    HvpgEnableStatus = 0  # bit 28 to 29
    HvpgPowerAck = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_CL_DW15),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_CL_DW15, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DW2:
    PORT_TX_DW2_AUX_B = 0x6C388
    PORT_TX_DW2_GRP_B = 0x6C688
    PORT_TX_DW2_LN0_B = 0x6C888
    PORT_TX_DW2_LN1_B = 0x6C988
    PORT_TX_DW2_LN2_B = 0x6CA88
    PORT_TX_DW2_LN3_B = 0x6CB88
    PORT_TX_DW2_AUX_A = 0x162388
    PORT_TX_DW2_GRP_A = 0x162688
    PORT_TX_DW2_LN0_A = 0x162888
    PORT_TX_DW2_LN1_A = 0x162988
    PORT_TX_DW2_LN2_A = 0x162A88
    PORT_TX_DW2_LN3_A = 0x162B88


class _PORT_TX_DW2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RcompScalar', ctypes.c_uint32, 8),
        ('Frclatencyoptim', ctypes.c_uint32, 3),
        ('Swing_SelLower', ctypes.c_uint32, 3),
        ('Cmnmode_Sel', ctypes.c_uint32, 1),
        ('Swing_SelUpper', ctypes.c_uint32, 1),
        ('Spare3116', ctypes.c_uint32, 16),
    ]


class REG_PORT_TX_DW2(ctypes.Union):
    value = 0
    offset = 0

    RcompScalar = 0  # bit 0 to 8
    Frclatencyoptim = 0  # bit 8 to 11
    Swing_SelLower = 0  # bit 11 to 14
    Cmnmode_Sel = 0  # bit 14 to 15
    Swing_SelUpper = 0  # bit 15 to 16
    Spare3116 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DW4:
    PORT_TX_DW4_AUX_B = 0x6C390
    PORT_TX_DW4_GRP_B = 0x6C690
    PORT_TX_DW4_LN0_B = 0x6C890
    PORT_TX_DW4_LN1_B = 0x6C990
    PORT_TX_DW4_LN2_B = 0x6CA90
    PORT_TX_DW4_LN3_B = 0x6CB90
    PORT_TX_DW4_AUX_A = 0x162390
    PORT_TX_DW4_GRP_A = 0x162690
    PORT_TX_DW4_LN0_A = 0x162890
    PORT_TX_DW4_LN1_A = 0x162990
    PORT_TX_DW4_LN2_A = 0x162A90
    PORT_TX_DW4_LN3_A = 0x162B90


class _PORT_TX_DW4(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CursorCoeff', ctypes.c_uint32, 6),
        ('PostCursor2', ctypes.c_uint32, 6),
        ('PostCursor1', ctypes.c_uint32, 6),
        ('RtermLimit', ctypes.c_uint32, 5),
        ('BsCompOvrd', ctypes.c_uint32, 1),
        ('Spare', ctypes.c_uint32, 7),
        ('LoadgenSelect', ctypes.c_uint32, 1),
    ]


class REG_PORT_TX_DW4(ctypes.Union):
    value = 0
    offset = 0

    CursorCoeff = 0  # bit 0 to 6
    PostCursor2 = 0  # bit 6 to 12
    PostCursor1 = 0  # bit 12 to 18
    RtermLimit = 0  # bit 18 to 23
    BsCompOvrd = 0  # bit 23 to 24
    Spare = 0  # bit 24 to 31
    LoadgenSelect = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW4),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW4, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_COEFF_POLARITY(Enum):
    COEFF_POLARITY_ENABLE = 0x0
    COEFF_POLARITY_DISABLE = 0x1


class ENUM_CURSOR_PROGRAM(Enum):
    CURSOR_PROGRAM_ENABLE = 0x0
    CURSOR_PROGRAM_DISABLE = 0x1


class ENUM_DISABLE_3TAP(Enum):
    DISABLE_3TAP_ENABLE = 0x0
    DISABLE_3TAP_DISABLE = 0x1


class ENUM_DISABLE_2TAP(Enum):
    DISABLE_2TAP_ENABLE = 0x0
    DISABLE_2TAP_DISABLE = 0x1


class ENUM_TX_TRAINING_ENABLE(Enum):
    TX_TRAINING_ENABLE = 0x1
    TX_TRAINING_DISABLE = 0x0


class OFFSET_PORT_TX_DW5:
    PORT_TX_DW5_AUX_B = 0x6C394
    PORT_TX_DW5_GRP_B = 0x6C694
    PORT_TX_DW5_LN0_B = 0x6C894
    PORT_TX_DW5_LN1_B = 0x6C994
    PORT_TX_DW5_LN2_B = 0x6CA94
    PORT_TX_DW5_LN3_B = 0x6CB94
    PORT_TX_DW5_AUX_A = 0x162394
    PORT_TX_DW5_GRP_A = 0x162694
    PORT_TX_DW5_LN0_A = 0x162894
    PORT_TX_DW5_LN1_A = 0x162994
    PORT_TX_DW5_LN2_A = 0x162A94
    PORT_TX_DW5_LN3_A = 0x162B94


class _PORT_TX_DW5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare20', ctypes.c_uint32, 3),
        ('RtermSelect', ctypes.c_uint32, 3),
        ('Spare106', ctypes.c_uint32, 5),
        ('CrScalingCoef', ctypes.c_uint32, 5),
        ('DecodeTimerSel', ctypes.c_uint32, 2),
        ('ScalingModeSel', ctypes.c_uint32, 3),
        ('Reserved21', ctypes.c_uint32, 3),
        ('Spare24', ctypes.c_uint32, 1),
        ('CoeffPolarity', ctypes.c_uint32, 1),
        ('CursorProgram', ctypes.c_uint32, 1),
        ('Spare2827', ctypes.c_uint32, 2),
        ('Disable3Tap', ctypes.c_uint32, 1),
        ('Disable2Tap', ctypes.c_uint32, 1),
        ('TxTrainingEnable', ctypes.c_uint32, 1),
    ]


class REG_PORT_TX_DW5(ctypes.Union):
    value = 0
    offset = 0

    Spare20 = 0  # bit 0 to 3
    RtermSelect = 0  # bit 3 to 6
    Spare106 = 0  # bit 6 to 11
    CrScalingCoef = 0  # bit 11 to 16
    DecodeTimerSel = 0  # bit 16 to 18
    ScalingModeSel = 0  # bit 18 to 21
    Reserved21 = 0  # bit 21 to 24
    Spare24 = 0  # bit 24 to 25
    CoeffPolarity = 0  # bit 25 to 26
    CursorProgram = 0  # bit 26 to 27
    Spare2827 = 0  # bit 27 to 29
    Disable3Tap = 0  # bit 29 to 30
    Disable2Tap = 0  # bit 30 to 31
    TxTrainingEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW5),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW5, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_TX_DW7:
    PORT_TX_DW7_AUX_B = 0x6C39C
    PORT_TX_DW7_GRP_B = 0x6C69C
    PORT_TX_DW7_LN0_B = 0x6C89C
    PORT_TX_DW7_LN1_B = 0x6C99C
    PORT_TX_DW7_LN2_B = 0x6CA9C
    PORT_TX_DW7_LN3_B = 0x6CB9C
    PORT_TX_DW7_AUX_A = 0x16239C
    PORT_TX_DW7_GRP_A = 0x16269C
    PORT_TX_DW7_LN0_A = 0x16289C
    PORT_TX_DW7_LN1_A = 0x16299C
    PORT_TX_DW7_LN2_A = 0x162A9C
    PORT_TX_DW7_LN3_A = 0x162B9C


class _PORT_TX_DW7(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spare230', ctypes.c_uint32, 24),
        ('NScalar', ctypes.c_uint32, 7),
        ('Spare31', ctypes.c_uint32, 1),
    ]


class REG_PORT_TX_DW7(ctypes.Union):
    value = 0
    offset = 0

    Spare230 = 0  # bit 0 to 24
    NScalar = 0  # bit 24 to 31
    Spare31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DW7),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DW7, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SOFTRESET_ENABLE(Enum):
    SOFTRESET_ENABLE = 0x1
    SOFTRESET_DISABLE = 0x0


class ENUM_CMNKEEPER_ENABLE(Enum):
    CMNKEEPER_ENABLE = 0x1
    CMNKEEPER_DISABLE = 0x0


class ENUM_PG_PWRDOWNEN(Enum):
    PG_PWRDOWNEN_ENABLE = 0x1
    PG_PWRDOWNEN_DISABLE = 0x0


class ENUM_CMNKEEPER_ENABLE_IN_PG(Enum):
    CMNKEEPER_ENABLE_IN_PG_ENABLE = 0x1
    CMNKEEPER_ENABLE_IN_PG_DISABLE = 0x0


class OFFSET_PORT_PCS_DW1:
    PORT_PCS_DW1_AUX_B = 0x6C304
    PORT_PCS_DW1_GRP_B = 0x6C604
    PORT_PCS_DW1_LN0_B = 0x6C804
    PORT_PCS_DW1_AUX_A = 0x162304
    PORT_PCS_DW1_GRP_A = 0x162604
    PORT_PCS_DW1_LN0_A = 0x162804


class _PORT_PCS_DW1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Soft_Reset_N', ctypes.c_uint32, 1),
        ('Softreset_Enable', ctypes.c_uint32, 1),
        ('Latencyoptim', ctypes.c_uint32, 2),
        ('Txdeemp', ctypes.c_uint32, 1),
        ('Txfifo_Rst_Master_Ovrd', ctypes.c_uint32, 1),
        ('Txfifo_Rst_Master_Ovrden', ctypes.c_uint32, 1),
        ('Tbc_As_Symbclk', ctypes.c_uint32, 1),
        ('Clkreq', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 2),
        ('Txhigh', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 2),
        ('Dcc', ctypes.c_uint32, 6),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Cmnkeep_Biasctr', ctypes.c_uint32, 2),
        ('Cmnkeeper_Enable', ctypes.c_uint32, 1),
        ('Pg_Pwrdownen', ctypes.c_uint32, 1),
        ('Cmnkeeper_Enable_In_Pg', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PORT_PCS_DW1(ctypes.Union):
    value = 0
    offset = 0

    Soft_Reset_N = 0  # bit 0 to 1
    Softreset_Enable = 0  # bit 1 to 2
    Latencyoptim = 0  # bit 2 to 4
    Txdeemp = 0  # bit 4 to 5
    Txfifo_Rst_Master_Ovrd = 0  # bit 5 to 6
    Txfifo_Rst_Master_Ovrden = 0  # bit 6 to 7
    Tbc_As_Symbclk = 0  # bit 7 to 8
    Clkreq = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 12
    Txhigh = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 16
    Dcc = 0  # bit 16 to 22
    Reserved22 = 0  # bit 22 to 24
    Cmnkeep_Biasctr = 0  # bit 24 to 26
    Cmnkeeper_Enable = 0  # bit 26 to 27
    Pg_Pwrdownen = 0  # bit 27 to 28
    Cmnkeeper_Enable_In_Pg = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_PCS_DW1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_PCS_DW1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PORT_PCS_DW9:
    PORT_PCS_DW9_AUX_B = 0x6C324
    PORT_PCS_DW9_GRP_B = 0x6C624
    PORT_PCS_DW9_LN0_B = 0x6C824
    PORT_PCS_DW9_AUX_A = 0x162324
    PORT_PCS_DW9_GRP_A = 0x162624
    PORT_PCS_DW9_LN0_A = 0x162824


class _PORT_PCS_DW9(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Stagger', ctypes.c_uint32, 5),
        ('StaggerOverride', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('StaggerMult', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 5),
        ('StrongCmCountOvrd', ctypes.c_uint32, 12),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_PORT_PCS_DW9(ctypes.Union):
    value = 0
    offset = 0

    Stagger = 0  # bit 0 to 5
    StaggerOverride = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    StaggerMult = 0  # bit 8 to 11
    Reserved11 = 0  # bit 11 to 16
    StrongCmCountOvrd = 0  # bit 16 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_PCS_DW9),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_PCS_DW9, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISPLAY_PORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0(Enum):
    DISPLAY_PORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0_NOT_COMPLETED = 0x0
    DISPLAY_PORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0_COMPLETED = 0x1


class OFFSET_PORT_TX_DFLEXDPPMS:
    PORT_TX_DFLEXDPPMS = 0x163890


class _PORT_TX_DFLEXDPPMS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayPortPhyModeStatusForTypeCConnector0', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector1', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector2', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector3', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector4', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector5', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector6', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector7', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector8', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector9', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector10', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector11', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector12', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector13', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector14', ctypes.c_uint32, 1),
        ('DisplayPortPhyModeStatusForTypeCConnector15', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_PORT_TX_DFLEXDPPMS(ctypes.Union):
    value = 0
    offset = 0

    DisplayPortPhyModeStatusForTypeCConnector0 = 0  # bit 0 to 1
    DisplayPortPhyModeStatusForTypeCConnector1 = 0  # bit 1 to 2
    DisplayPortPhyModeStatusForTypeCConnector2 = 0  # bit 2 to 3
    DisplayPortPhyModeStatusForTypeCConnector3 = 0  # bit 3 to 4
    DisplayPortPhyModeStatusForTypeCConnector4 = 0  # bit 4 to 5
    DisplayPortPhyModeStatusForTypeCConnector5 = 0  # bit 5 to 6
    DisplayPortPhyModeStatusForTypeCConnector6 = 0  # bit 6 to 7
    DisplayPortPhyModeStatusForTypeCConnector7 = 0  # bit 7 to 8
    DisplayPortPhyModeStatusForTypeCConnector8 = 0  # bit 8 to 9
    DisplayPortPhyModeStatusForTypeCConnector9 = 0  # bit 9 to 10
    DisplayPortPhyModeStatusForTypeCConnector10 = 0  # bit 10 to 11
    DisplayPortPhyModeStatusForTypeCConnector11 = 0  # bit 11 to 12
    DisplayPortPhyModeStatusForTypeCConnector12 = 0  # bit 12 to 13
    DisplayPortPhyModeStatusForTypeCConnector13 = 0  # bit 13 to 14
    DisplayPortPhyModeStatusForTypeCConnector14 = 0  # bit 14 to 15
    DisplayPortPhyModeStatusForTypeCConnector15 = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXDPPMS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXDPPMS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_0_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_1_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_2_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_3_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_4_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_5_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_6_ML30 = 0xF


class ENUM_DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7(Enum):
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7_ML0 = 0x1
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7_ML10 = 0x3
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7_ML32 = 0xC  # This setting should not be used with Type-C ALT co
                                                                   # nnections.
    DISPLAYPORT_MAIN_LINK_ENABLE_FOR_TYPEC_CONNECTOR_7_ML30 = 0xF


class OFFSET_PORT_TX_DFLEXDPMLE1:
    PORT_TX_DFLEXDPMLE1 = 0x1638C0


class _PORT_TX_DFLEXDPMLE1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayportMainLinkEnableForTypeCConnector0', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector1', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector2', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector3', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector4', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector5', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector6', ctypes.c_uint32, 4),
        ('DisplayportMainLinkEnableForTypeCConnector7', ctypes.c_uint32, 4),
    ]


class REG_PORT_TX_DFLEXDPMLE1(ctypes.Union):
    value = 0
    offset = 0

    DisplayportMainLinkEnableForTypeCConnector0 = 0  # bit 0 to 4
    DisplayportMainLinkEnableForTypeCConnector1 = 0  # bit 4 to 8
    DisplayportMainLinkEnableForTypeCConnector2 = 0  # bit 8 to 12
    DisplayportMainLinkEnableForTypeCConnector3 = 0  # bit 12 to 16
    DisplayportMainLinkEnableForTypeCConnector4 = 0  # bit 16 to 20
    DisplayportMainLinkEnableForTypeCConnector5 = 0  # bit 20 to 24
    DisplayportMainLinkEnableForTypeCConnector6 = 0  # bit 24 to 28
    DisplayportMainLinkEnableForTypeCConnector7 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXDPMLE1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXDPMLE1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DISPLAYPORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0(Enum):
    DISPLAYPORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0_DP_CONTROLLER_IS_NOT_IN_SAFE_STATE = 0x1
    DISPLAYPORT_PHY_MODE_STATUS_FOR_TYPEC_CONNECTOR_0_DP_CONTROLLER_IS_IN_SAFE_STATE = 0x0


class OFFSET_PORT_TX_DFLEXDPCSSS:
    PORT_TX_DFLEXDPCSSS = 0x163894


class _PORT_TX_DFLEXDPCSSS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayportPhyModeStatusForTypeCConnector0', ctypes.c_uint32, 1),
        ('DisplayportPhyModeStatusForTypeCConnector1', ctypes.c_uint32, 1),
        ('DisplayportPhyModeStatusForTypeCConnector2', ctypes.c_uint32, 1),
        ('DisplayportPhyModeStatusForTypeCConnector3', ctypes.c_uint32, 1),
        ('DisplayportPhyModeStatusForTypeCConnector4', ctypes.c_uint32, 1),
        ('DisplayportPhyModeStatusForTypeCConnector5', ctypes.c_uint32, 1),
        ('DisplayportPhyModeStatusForTypeCConnector6', ctypes.c_uint32, 1),
        ('DisplayportPhyModeStatusForTypeCConnector7', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 24),
    ]


class REG_PORT_TX_DFLEXDPCSSS(ctypes.Union):
    value = 0
    offset = 0

    DisplayportPhyModeStatusForTypeCConnector0 = 0  # bit 0 to 1
    DisplayportPhyModeStatusForTypeCConnector1 = 0  # bit 1 to 2
    DisplayportPhyModeStatusForTypeCConnector2 = 0  # bit 2 to 3
    DisplayportPhyModeStatusForTypeCConnector3 = 0  # bit 3 to 4
    DisplayportPhyModeStatusForTypeCConnector4 = 0  # bit 4 to 5
    DisplayportPhyModeStatusForTypeCConnector5 = 0  # bit 5 to 6
    DisplayportPhyModeStatusForTypeCConnector6 = 0  # bit 6 to 7
    DisplayportPhyModeStatusForTypeCConnector7 = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PORT_TX_DFLEXDPCSSS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PORT_TX_DFLEXDPCSSS, self).__init__()
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
    PORT_TX_DFLEXPA1 = 0x163880


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


class ENUM_DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0(Enum):
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX0 = 0x1
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX1 = 0x2
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX10 = 0x3
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX2 = 0x4
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX2_TX0 = 0x5
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX3 = 0x8
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX32 = 0xC
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_0_PHY_TX30 = 0xF


class ENUM_TC0_LIVE_STATE(Enum):
    TC0_LIVE_STATE_NO_HPD = 0x0  # No HPD connect for TypeC (DP alternate) or TBT
    TC0_LIVE_STATE_TYPEC_HPD = 0x1  # HPD connect for TypeC (DP alternate)
    TC0_LIVE_STATE_TBT_HPD = 0x2  # HPD connect for TBT
    TC0_LIVE_STATE_INVALID = 0x3  # Invalid


class ENUM_DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1(Enum):
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX0 = 0x1
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX1 = 0x2
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX10 = 0x3
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX2 = 0x4
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX2_TX0 = 0x5
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX3 = 0x8
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX32 = 0xC
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_1_PHY_TX30 = 0xF


class ENUM_TC1_LIVE_STATE(Enum):
    TC1_LIVE_STATE_NO_HPD = 0x0  # No HPD connect for TypeC (DP alternate) or TBT
    TC1_LIVE_STATE_TYPEC_HPD = 0x1  # HPD connect for TypeC (DP alternate)
    TC1_LIVE_STATE_TBT_HPD = 0x2  # HPD connect for TBT
    TC1_LIVE_STATE_INVALID = 0x3  # Invalid


class ENUM_DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2(Enum):
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX0 = 0x1
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX1 = 0x2
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX10 = 0x3
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX2 = 0x4
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX2_TX0 = 0x5
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX3 = 0x8
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX32 = 0xC
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_2_PHY_TX30 = 0xF


class ENUM_TC2_LIVE_STATE(Enum):
    TC2_LIVE_STATE_NO_HPD = 0x0  # No HPD connect for TypeC (DP alternate) or TBT
    TC2_LIVE_STATE_TYPEC_HPD = 0x1  # HPD connect for TypeC (DP alternate)
    TC2_LIVE_STATE_TBT_HPD = 0x2  # HPD connect for TBT
    TC2_LIVE_STATE_INVALID = 0x3  # Invalid


class ENUM_DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3(Enum):
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX0 = 0x1
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX1 = 0x2
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX10 = 0x3
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX2 = 0x4
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX2_TX0 = 0x5
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX3 = 0x8
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX32 = 0xC
    DISPLAY_PORT_X4_TX_LANE_ASSIGNMENT_FOR_TYPEC_CONNECTOR_3_PHY_TX30 = 0xF


class ENUM_TC3_LIVE_STATE(Enum):
    TC3_LIVE_STATE_NO_HPD = 0x0  # No HPD connect for TypeC (DP alternate) or TBT
    TC3_LIVE_STATE_TYPEC_HPD = 0x1  # HPD connect for TypeC (DP alternate)
    TC3_LIVE_STATE_TBT_HPD = 0x2  # HPD connect for TBT
    TC3_LIVE_STATE_INVALID = 0x3  # Invalid


class OFFSET_PORT_TX_DFLEXDPSP:
    PORT_TX_DFLEXDPSP1 = 0x1638A0
    PORT_TX_DFLEXDPSP2 = 0x1638A4
    PORT_TX_DFLEXDPSP3 = 0x1638A8
    PORT_TX_DFLEXDPSP4 = 0x1638AC


class _PORT_TX_DFLEXDPSP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector0', ctypes.c_uint32, 4),
        ('DpScratchPadTc0Lsb_Dpsptc0Lsb', ctypes.c_uint32, 1),
        ('Tc0LiveState', ctypes.c_uint32, 2),
        ('Reserved7', ctypes.c_uint32, 1),
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector1', ctypes.c_uint32, 4),
        ('Reserved12', ctypes.c_uint32, 1),
        ('Tc1LiveState', ctypes.c_uint32, 2),
        ('Reserved15', ctypes.c_uint32, 1),
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector2', ctypes.c_uint32, 4),
        ('Reserved20', ctypes.c_uint32, 1),
        ('Tc2LiveState', ctypes.c_uint32, 2),
        ('Reserved23', ctypes.c_uint32, 1),
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector3', ctypes.c_uint32, 4),
        ('Reserved28', ctypes.c_uint32, 1),
        ('Tc3LiveState', ctypes.c_uint32, 2),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_PORT_TX_DFLEXDPSP(ctypes.Union):
    value = 0
    offset = 0

    DisplayPortX4TxLaneAssignmentForTypeCConnector0 = 0  # bit 0 to 4
    DpScratchPadTc0Lsb_Dpsptc0Lsb = 0  # bit 4 to 5
    Tc0LiveState = 0  # bit 5 to 7
    Reserved7 = 0  # bit 7 to 8
    DisplayPortX4TxLaneAssignmentForTypeCConnector1 = 0  # bit 8 to 12
    Reserved12 = 0  # bit 12 to 13
    Tc1LiveState = 0  # bit 13 to 15
    Reserved15 = 0  # bit 15 to 16
    DisplayPortX4TxLaneAssignmentForTypeCConnector2 = 0  # bit 16 to 20
    Reserved20 = 0  # bit 20 to 21
    Tc2LiveState = 0  # bit 21 to 23
    Reserved23 = 0  # bit 23 to 24
    DisplayPortX4TxLaneAssignmentForTypeCConnector3 = 0  # bit 24 to 28
    Reserved28 = 0  # bit 28 to 29
    Tc3LiveState = 0  # bit 29 to 31
    Reserved31 = 0  # bit 31 to 32

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


class ENUM_CRI_USE_FS32(Enum):
    CRI_USE_FS32_FS32 = 0x1  # TX EQ advertised full-scale value. Advertised full-scale value is set to 32.
    CRI_USE_FS32_FS63 = 0x0  # TX EQ advertised full-scale value. Advertised full-scale value is set to63.


class ENUM_CRI_POSTCUR_COEFF_SIGN(Enum):
    CRI_POSTCUR_COEFF_SIGN_NEGATIVE = 0x1  # TX EQ coefficient post-cursor sign. C+1 is a negative value. 2's complemen
                                           # t version of the preset or iTxdeemph[17:12] will be used.
    CRI_POSTCUR_COEFF_SIGN_AS_IS = 0x0  # TX EQ coefficient post-cursor value. Value will be used "as is".


class ENUM_CRI_PRECUR_COEFF_SIGN(Enum):
    CRI_PRECUR_COEFF_SIGN_NEGATIVE = 0x1  # TX EQ coefficient pre-cursor sign. C-1 is a negative value. 2's complement 
                                          # version of the preset or iTxdeemph[5:0] will be used.
    CRI_PRECUR_COEFF_SIGN_AS_IS = 0x0  # TX EQ coefficient pre-cursor sign. Value will be used "as is".


class ENUM_CRI_REVERSEDEEMPH_EN(Enum):
    CRI_REVERSEDEEMPH_EN_NORMAL = 0x0
    CRI_REVERSEDEEMPH_EN_SWAP = 0x1


class OFFSET_MG_TX_LINK_PARAMS:
    MG_TX_LINK_PARAMS_TX2LN0_PORT1 = 0x1680AC
    MG_TX_LINK_PARAMS_TX1LN0_PORT1 = 0x16812C
    MG_TX_LINK_PARAMS_TX2LN1_PORT1 = 0x1684AC
    MG_TX_LINK_PARAMS_TX1LN1_PORT1 = 0x16852C
    MG_TX_LINK_PARAMS_TX2LN0_PORT2 = 0x1690AC
    MG_TX_LINK_PARAMS_TX1LN0_PORT2 = 0x16912C
    MG_TX_LINK_PARAMS_TX2LN1_PORT2 = 0x1694AC
    MG_TX_LINK_PARAMS_TX1LN1_PORT2 = 0x16952C
    MG_TX_LINK_PARAMS_TX2LN0_PORT3 = 0x16A0AC
    MG_TX_LINK_PARAMS_TX1LN0_PORT3 = 0x16A12C
    MG_TX_LINK_PARAMS_TX2LN1_PORT3 = 0x16A4AC
    MG_TX_LINK_PARAMS_TX1LN1_PORT3 = 0x16A52C
    MG_TX_LINK_PARAMS_TX2LN0_PORT4 = 0x16B0AC
    MG_TX_LINK_PARAMS_TX1LN0_PORT4 = 0x16B12C
    MG_TX_LINK_PARAMS_TX2LN1_PORT4 = 0x16B4AC
    MG_TX_LINK_PARAMS_TX1LN1_PORT4 = 0x16B52C


class _MG_TX_LINK_PARAMS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 5),
        ('Cri_Use_Fs32', ctypes.c_uint32, 1),
        ('Cri_Postcur_Coeff_Sign', ctypes.c_uint32, 1),
        ('Cri_Precur_Coeff_Sign', ctypes.c_uint32, 1),
        ('Curpreset', ctypes.c_uint32, 6),
        ('Reserved14', ctypes.c_uint32, 2),
        ('AutoSwingMargin', ctypes.c_uint32, 6),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Cri_Autoswingsqlch', ctypes.c_uint32, 1),
        ('Cri_Autoswingup', ctypes.c_uint32, 1),
        ('Cri_Autoswingen', ctypes.c_uint32, 1),
        ('Autoswingdone', ctypes.c_uint32, 1),
        ('Cri_Prepostpresetcurswap', ctypes.c_uint32, 1),
        ('Cri_Prepostcurswap', ctypes.c_uint32, 1),
        ('Cri_Reversedeemph_En', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_MG_TX_LINK_PARAMS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 5
    Cri_Use_Fs32 = 0  # bit 5 to 6
    Cri_Postcur_Coeff_Sign = 0  # bit 6 to 7
    Cri_Precur_Coeff_Sign = 0  # bit 7 to 8
    Curpreset = 0  # bit 8 to 14
    Reserved14 = 0  # bit 14 to 16
    AutoSwingMargin = 0  # bit 16 to 22
    Reserved22 = 0  # bit 22 to 24
    Cri_Autoswingsqlch = 0  # bit 24 to 25
    Cri_Autoswingup = 0  # bit 25 to 26
    Cri_Autoswingen = 0  # bit 26 to 27
    Autoswingdone = 0  # bit 27 to 28
    Cri_Prepostpresetcurswap = 0  # bit 28 to 29
    Cri_Prepostcurswap = 0  # bit 29 to 30
    Cri_Reversedeemph_En = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_TX_LINK_PARAMS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_TX_LINK_PARAMS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MG_TX_SWINGCTRL:
    MG_TX_SWINGCTRL_TX2LN0_PORT1 = 0x1680C8
    MG_TX_SWINGCTRL_TX1LN0_PORT1 = 0x168148
    MG_TX_SWINGCTRL_TX2LN1_PORT1 = 0x1684C8
    MG_TX_SWINGCTRL_TX1LN1_PORT1 = 0x168548
    MG_TX_SWINGCTRL_TX2LN0_PORT2 = 0x1690C8
    MG_TX_SWINGCTRL_TX1LN0_PORT2 = 0x169148
    MG_TX_SWINGCTRL_TX2LN1_PORT2 = 0x1694C8
    MG_TX_SWINGCTRL_TX1LN1_PORT2 = 0x169548
    MG_TX_SWINGCTRL_TX2LN0_PORT3 = 0x16A0C8
    MG_TX_SWINGCTRL_TX1LN0_PORT3 = 0x16A148
    MG_TX_SWINGCTRL_TX2LN1_PORT3 = 0x16A4C8
    MG_TX_SWINGCTRL_TX1LN1_PORT3 = 0x16A548
    MG_TX_SWINGCTRL_TX2LN0_PORT4 = 0x16B0C8
    MG_TX_SWINGCTRL_TX1LN0_PORT4 = 0x16B148
    MG_TX_SWINGCTRL_TX2LN1_PORT4 = 0x16B4C8
    MG_TX_SWINGCTRL_TX1LN1_PORT4 = 0x16B548


class _MG_TX_SWINGCTRL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cri_Txdeemph_Override17_12', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 2),
        ('Rcomp_Pullup_H', ctypes.c_uint32, 8),
        ('Rcomp_Pulldown_H', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_MG_TX_SWINGCTRL(ctypes.Union):
    value = 0
    offset = 0

    Cri_Txdeemph_Override17_12 = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 8
    Rcomp_Pullup_H = 0  # bit 8 to 16
    Rcomp_Pulldown_H = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_TX_SWINGCTRL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_TX_SWINGCTRL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MG_TX_DRVCTRL:
    MG_TX_DRVCTRL_TX2LN0_TXPORT1 = 0x1680C4
    MG_TX_DRVCTRL_TX1LN0_TXPORT1 = 0x168144
    MG_TX_DRVCTRL_TX2LN1_TXPORT1 = 0x1684C4
    MG_TX_DRVCTRL_TX1LN1_TXPORT1 = 0x168544
    MG_TX_DRVCTRL_TX2LN0_TXPORT2 = 0x1690C4
    MG_TX_DRVCTRL_TX1LN0_TXPORT2 = 0x169144
    MG_TX_DRVCTRL_TX2LN1_TXPORT2 = 0x1694C4
    MG_TX_DRVCTRL_TX1LN1_TXPORT2 = 0x169544
    MG_TX_DRVCTRL_TX2LN0_TXPORT3 = 0x16A0C4
    MG_TX_DRVCTRL_TX1LN0_TXPORT3 = 0x16A144
    MG_TX_DRVCTRL_TX2LN1_TXPORT3 = 0x16A4C4
    MG_TX_DRVCTRL_TX1LN1_TXPORT3 = 0x16A544
    MG_TX_DRVCTRL_TX2LN0_TXPORT4 = 0x16B0C4
    MG_TX_DRVCTRL_TX1LN0_TXPORT4 = 0x16B144
    MG_TX_DRVCTRL_TX2LN1_TXPORT4 = 0x16B4C4
    MG_TX_DRVCTRL_TX1LN1_TXPORT4 = 0x16B544


class _MG_TX_DRVCTRL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Bin_Bypassdata', ctypes.c_uint32, 1),
        ('Onehot_Bypass_Mode_H', ctypes.c_uint32, 1),
        ('Postc_Bypassen_H', ctypes.c_uint32, 3),
        ('Prec_Bypassen_H', ctypes.c_uint32, 3),
        ('O_Frcstrongcmen', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 2),
        ('O_Use_Rcomp_In_Bypass_H', ctypes.c_uint32, 1),
        ('Cri_Loadgen_Sel', ctypes.c_uint32, 2),
        ('Continuous_Rcomp_Mode_H', ctypes.c_uint32, 1),
        ('Reserved15', ctypes.c_uint32, 1),
        ('Cri_Txdeemph_Override_5_0', ctypes.c_uint32, 6),
        ('Cri_Txdeemph_Override_En', ctypes.c_uint32, 1),
        ('Reserved23', ctypes.c_uint32, 1),
        ('Cri_Txdeemph_Override_11_6', ctypes.c_uint32, 6),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_MG_TX_DRVCTRL(ctypes.Union):
    value = 0
    offset = 0

    Bin_Bypassdata = 0  # bit 0 to 1
    Onehot_Bypass_Mode_H = 0  # bit 1 to 2
    Postc_Bypassen_H = 0  # bit 2 to 5
    Prec_Bypassen_H = 0  # bit 5 to 8
    O_Frcstrongcmen = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 11
    O_Use_Rcomp_In_Bypass_H = 0  # bit 11 to 12
    Cri_Loadgen_Sel = 0  # bit 12 to 14
    Continuous_Rcomp_Mode_H = 0  # bit 14 to 15
    Reserved15 = 0  # bit 15 to 16
    Cri_Txdeemph_Override_5_0 = 0  # bit 16 to 22
    Cri_Txdeemph_Override_En = 0  # bit 22 to 23
    Reserved23 = 0  # bit 23 to 24
    Cri_Txdeemph_Override_11_6 = 0  # bit 24 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_TX_DRVCTRL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_TX_DRVCTRL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MG_TX_PISO_READLOAD:
    MG_TX_PISO_READLOAD_TX2LN0_PORT1 = 0x1680CC
    MG_TX_PISO_READLOAD_TX1LN0_PORT1 = 0x16814C
    MG_TX_PISO_READLOAD_TX2LN1_PORT1 = 0x1684CC
    MG_TX_PISO_READLOAD_TX1LN1_PORT1 = 0x16854C
    MG_TX_PISO_READLOAD_TX2LN0_PORT2 = 0x1690CC
    MG_TX_PISO_READLOAD_TX1LN0_PORT2 = 0x16914C
    MG_TX_PISO_READLOAD_TX2LN1_PORT2 = 0x1694CC
    MG_TX_PISO_READLOAD_TX1LN1_PORT2 = 0x16954C
    MG_TX_PISO_READLOAD_TX2LN0_PORT3 = 0x16A0CC
    MG_TX_PISO_READLOAD_TX1LN0_PORT3 = 0x16A14C
    MG_TX_PISO_READLOAD_TX2LN1_PORT3 = 0x16A4CC
    MG_TX_PISO_READLOAD_TX1LN1_PORT3 = 0x16A54C
    MG_TX_PISO_READLOAD_TX2LN0_PORT4 = 0x16B0CC
    MG_TX_PISO_READLOAD_TX1LN0_PORT4 = 0x16B14C
    MG_TX_PISO_READLOAD_TX2LN1_PORT4 = 0x16B4CC
    MG_TX_PISO_READLOAD_TX1LN1_PORT4 = 0x16B54C


class _MG_TX_PISO_READLOAD(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cri_Calccont', ctypes.c_uint32, 1),
        ('Cri_Calcinit', ctypes.c_uint32, 1),
        ('Cri_Frcpresetcalc', ctypes.c_uint32, 1),
        ('Cri_Rounding_Disable', ctypes.c_uint32, 1),
        ('Cri_Use_Preset_Coef', ctypes.c_uint32, 1),
        ('Cri_Mediumcmrcompdis', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('Reserved8', ctypes.c_uint32, 4),
        ('Cri_Pisorate8Bit_Ovrd_En', ctypes.c_uint32, 1),
        ('Cri_Pisorate8Bit_Ovrd', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 2),
        ('Cri_Dnelb_En', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 4),
        ('Cri_Neloopbacken', ctypes.c_uint32, 1),
        ('Cri_Beacondivratio', ctypes.c_uint32, 1),
        ('Cri_Bssb_Gpio_Out_Cri_Cfg', ctypes.c_uint32, 1),
        ('Cri_Bypdftmode', ctypes.c_uint32, 5),
        ('Cri_Bypbycomp', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_MG_TX_PISO_READLOAD(ctypes.Union):
    value = 0
    offset = 0

    Cri_Calccont = 0  # bit 0 to 1
    Cri_Calcinit = 0  # bit 1 to 2
    Cri_Frcpresetcalc = 0  # bit 2 to 3
    Cri_Rounding_Disable = 0  # bit 3 to 4
    Cri_Use_Preset_Coef = 0  # bit 4 to 5
    Cri_Mediumcmrcompdis = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    Reserved8 = 0  # bit 8 to 12
    Cri_Pisorate8Bit_Ovrd_En = 0  # bit 12 to 13
    Cri_Pisorate8Bit_Ovrd = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 16
    Cri_Dnelb_En = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 21
    Cri_Neloopbacken = 0  # bit 21 to 22
    Cri_Beacondivratio = 0  # bit 22 to 23
    Cri_Bssb_Gpio_Out_Cri_Cfg = 0  # bit 23 to 24
    Cri_Bypdftmode = 0  # bit 24 to 29
    Cri_Bypbycomp = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_TX_PISO_READLOAD),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_TX_PISO_READLOAD, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_LANECLKREQ_FORCE(Enum):
    CFG_LANECLKREQ_FORCE_FORCE_SUS_CLK_REQUEST = 0x1
    CFG_LANECLKREQ_FORCE_DO_NOT_FORCE_SUS_CLK_REQUEST = 0x0


class OFFSET_MG_DP_MODE:
    MG_DP_MODE_LN0_ACU_PORT1 = 0x1683A0
    MG_DP_MODE_LN1_ACU_PORT1 = 0x1687A0
    MG_DP_MODE_LN0_ACU_PORT2 = 0x1693A0
    MG_DP_MODE_LN1_ACU_PORT2 = 0x1697A0
    MG_DP_MODE_LN0_ACU_PORT3 = 0x16A3A0
    MG_DP_MODE_LN1_ACU_PORT3 = 0x16A7A0
    MG_DP_MODE_LN0_ACU_PORT4 = 0x16B3A0
    MG_DP_MODE_LN1_ACU_PORT4 = 0x16B7A0


class _MG_DP_MODE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Cfg_Suspwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Gaonpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Digpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Clnpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Trpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Tr2Pwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Dp_X1_Mode', ctypes.c_uint32, 1),
        ('Cfg_Dp_X2_Mode', ctypes.c_uint32, 1),
        ('Cfg_Rawpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Digpwr_Req_Override', ctypes.c_uint32, 1),
        ('Cfg_Rawpwr_Req_Override', ctypes.c_uint32, 1),
        ('Cfg_Susclk_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Laneclkreq_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Laneclkreq_Force', ctypes.c_uint32, 1),
        ('Cfg_Cri_Digpwr_Req', ctypes.c_uint32, 1),
        ('Reserved15', ctypes.c_uint32, 1),
        ('Cfg_Ldo_Powerup_Timer_8', ctypes.c_uint32, 1),
        ('Cfg_Vr_Pulldwn2Gnd_Tr', ctypes.c_uint32, 1),
        ('Cfg_Vr_Pulldwn2Gnd_Tr2', ctypes.c_uint32, 1),
        ('Crireg_Cold_Boot_Done', ctypes.c_uint32, 1),
        ('Cfg_Dig_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Cl_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Tr_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Tr2_Pwrgate_Timer_Bypass', ctypes.c_uint32, 1),
        ('Cfg_Ldo_Powerup_Timer_7_0', ctypes.c_uint32, 8),
    ]


class REG_MG_DP_MODE(ctypes.Union):
    value = 0
    offset = 0

    Cfg_Suspwr_Gating_Ctrl = 0  # bit 0 to 1
    Cfg_Gaonpwr_Gating_Ctrl = 0  # bit 1 to 2
    Cfg_Digpwr_Gating_Ctrl = 0  # bit 2 to 3
    Cfg_Clnpwr_Gating_Ctrl = 0  # bit 3 to 4
    Cfg_Trpwr_Gating_Ctrl = 0  # bit 4 to 5
    Cfg_Tr2Pwr_Gating_Ctrl = 0  # bit 5 to 6
    Cfg_Dp_X1_Mode = 0  # bit 6 to 7
    Cfg_Dp_X2_Mode = 0  # bit 7 to 8
    Cfg_Rawpwr_Gating_Ctrl = 0  # bit 8 to 9
    Cfg_Digpwr_Req_Override = 0  # bit 9 to 10
    Cfg_Rawpwr_Req_Override = 0  # bit 10 to 11
    Cfg_Susclk_Gating_Ctrl = 0  # bit 11 to 12
    Cfg_Laneclkreq_Gating_Ctrl = 0  # bit 12 to 13
    Cfg_Laneclkreq_Force = 0  # bit 13 to 14
    Cfg_Cri_Digpwr_Req = 0  # bit 14 to 15
    Reserved15 = 0  # bit 15 to 16
    Cfg_Ldo_Powerup_Timer_8 = 0  # bit 16 to 17
    Cfg_Vr_Pulldwn2Gnd_Tr = 0  # bit 17 to 18
    Cfg_Vr_Pulldwn2Gnd_Tr2 = 0  # bit 18 to 19
    Crireg_Cold_Boot_Done = 0  # bit 19 to 20
    Cfg_Dig_Pwrgate_Timer_Bypass = 0  # bit 20 to 21
    Cfg_Cl_Pwrgate_Timer_Bypass = 0  # bit 21 to 22
    Cfg_Tr_Pwrgate_Timer_Bypass = 0  # bit 22 to 23
    Cfg_Tr2_Pwrgate_Timer_Bypass = 0  # bit 23 to 24
    Cfg_Ldo_Powerup_Timer_7_0 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_DP_MODE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_DP_MODE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CRI_AMI_CK_DIV_SEL_LE_500MHZ(Enum):
    CRI_AMI_CK_DIV_SEL_LE_500MHZ_DIV1 = 0x0
    CRI_AMI_CK_DIV_SEL_LE_500MHZ_DIV2 = 0x1
    CRI_AMI_CK_DIV_SEL_LE_500MHZ_DIV4 = 0x2
    CRI_AMI_CK_DIV_SEL_LE_500MHZ_DIV8 = 0x3


class ENUM_CRI_AMI_CK_DIV_SEL_GT_500MHZ(Enum):
    CRI_AMI_CK_DIV_SEL_GT_500MHZ_DIV1 = 0x0
    CRI_AMI_CK_DIV_SEL_GT_500MHZ_DIV2 = 0x1
    CRI_AMI_CK_DIV_SEL_GT_500MHZ_DIV4 = 0x2
    CRI_AMI_CK_DIV_SEL_GT_500MHZ_DIV8 = 0x3


class ENUM_CRI_AMI_CK_DIV_SEL_LE_1000MHZ(Enum):
    CRI_AMI_CK_DIV_SEL_LE_1000MHZ_DIV1 = 0x0
    CRI_AMI_CK_DIV_SEL_LE_1000MHZ_DIV2 = 0x1
    CRI_AMI_CK_DIV_SEL_LE_1000MHZ_DIV4 = 0x2
    CRI_AMI_CK_DIV_SEL_LE_1000MHZ_DIV8 = 0x3


class ENUM_CFG_AMI_CK_DIV_OVERRIDE_EN(Enum):
    CFG_AMI_CK_DIV_OVERRIDE_EN_DISABLE = 0x0
    CFG_AMI_CK_DIV_OVERRIDE_EN_ENABLE = 0x1


class ENUM_CRI_PERIODICDCC_TIMERSEL(Enum):
    CRI_PERIODICDCC_TIMERSEL_0_1MS = 0x0
    CRI_PERIODICDCC_TIMERSEL_1MS = 0x1
    CRI_PERIODICDCC_TIMERSEL_5MS = 0x2
    CRI_PERIODICDCC_TIMERSEL_10MS = 0x3


class OFFSET_MG_TX_DCC:
    MG_TX_DCC_TX2_LN0_PORT1 = 0x168090
    MG_TX_DCC_TX1_LN0_PORT1 = 0x168110
    MG_TX_DCC_TX2_LN1_PORT1 = 0x168490
    MG_TX_DCC_TX1_LN1_PORT1 = 0x168510
    MG_TX_DCC_TX2_LN0_PORT2 = 0x169090
    MG_TX_DCC_TX1_LN0_PORT2 = 0x169110
    MG_TX_DCC_TX2_LN1_PORT2 = 0x169490
    MG_TX_DCC_TX1_LN1_PORT2 = 0x169510
    MG_TX_DCC_TX2_LN0_PORT3 = 0x16A090
    MG_TX_DCC_TX1_LN0_PORT3 = 0x16A110
    MG_TX_DCC_TX2_LN1_PORT3 = 0x16A490
    MG_TX_DCC_TX1_LN1_PORT3 = 0x16A510
    MG_TX_DCC_TX2_LN0_PORT4 = 0x16B090
    MG_TX_DCC_TX1_LN0_PORT4 = 0x16B110
    MG_TX_DCC_TX2_LN1_PORT4 = 0x16B490
    MG_TX_DCC_TX1_LN1_PORT4 = 0x16B510


class _MG_TX_DCC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('O_Dcc_Coarse_P_L', ctypes.c_uint32, 4),
        ('O_Dcc_Coarse_N_H', ctypes.c_uint32, 4),
        ('O_Dcc_Fine_Code', ctypes.c_uint32, 3),
        ('O_Dcc_Periodic_Code', ctypes.c_uint32, 3),
        ('Cri_Frcdcccmpout_En', ctypes.c_uint32, 1),
        ('Cri_Frcdcccmpout_Value', ctypes.c_uint32, 1),
        ('Cri_Codeupdate_Sel', ctypes.c_uint32, 2),
        ('Cri_Ami_Ck_Div_Sel_Le_500Mhz', ctypes.c_uint32, 2),
        ('Cri_Ami_Ck_Div_Sel_Gt_500Mhz', ctypes.c_uint32, 2),
        ('Cri_Ami_Ck_Div_Sel_Le_1000Mhz', ctypes.c_uint32, 2),
        ('Cfg_Ami_Ck_Div_Override_En', ctypes.c_uint32, 1),
        ('Cfg_Ami_Ck_Div_Override_Value', ctypes.c_uint32, 2),
        ('Cri_Periodicdcc_Timersel', ctypes.c_uint32, 2),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_MG_TX_DCC(ctypes.Union):
    value = 0
    offset = 0

    O_Dcc_Coarse_P_L = 0  # bit 0 to 4
    O_Dcc_Coarse_N_H = 0  # bit 4 to 8
    O_Dcc_Fine_Code = 0  # bit 8 to 11
    O_Dcc_Periodic_Code = 0  # bit 11 to 14
    Cri_Frcdcccmpout_En = 0  # bit 14 to 15
    Cri_Frcdcccmpout_Value = 0  # bit 15 to 16
    Cri_Codeupdate_Sel = 0  # bit 16 to 18
    Cri_Ami_Ck_Div_Sel_Le_500Mhz = 0  # bit 18 to 20
    Cri_Ami_Ck_Div_Sel_Gt_500Mhz = 0  # bit 20 to 22
    Cri_Ami_Ck_Div_Sel_Le_1000Mhz = 0  # bit 22 to 24
    Cfg_Ami_Ck_Div_Override_En = 0  # bit 24 to 25
    Cfg_Ami_Ck_Div_Override_Value = 0  # bit 25 to 27
    Cri_Periodicdcc_Timersel = 0  # bit 27 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_TX_DCC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_TX_DCC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_MG_MISC_SUS0:
    MG_MISC_SUS0_PORT1 = 0x168814
    MG_MISC_SUS0_PORT2 = 0x169814
    MG_MISC_SUS0_PORT3 = 0x16A814
    MG_MISC_SUS0_PORT4 = 0x16B814


class _MG_MISC_SUS0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Os_Cfg_Susclk_Delay', ctypes.c_uint32, 5),
        ('Os_Cfg_Dgpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Os_Cfg_Cl1Pwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Os_Cfg_Trpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Calclkgate_Dis', ctypes.c_uint32, 1),
        ('Os_Cfg_Cl2Pwr_Pll1En_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Os_Cfg_Gaonpwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Os_Cfg_Cl2Pwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Os_Cfg_Tr2Pwr_Gating_Ctrl', ctypes.c_uint32, 1),
        ('Cfg_Calclk_Srcsel', ctypes.c_uint32, 1),
        ('Os_Susclk_Dynclkgate_Mode', ctypes.c_uint32, 2),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_MG_MISC_SUS0(ctypes.Union):
    value = 0
    offset = 0

    Os_Cfg_Susclk_Delay = 0  # bit 0 to 5
    Os_Cfg_Dgpwr_Gating_Ctrl = 0  # bit 5 to 6
    Os_Cfg_Cl1Pwr_Gating_Ctrl = 0  # bit 6 to 7
    Os_Cfg_Trpwr_Gating_Ctrl = 0  # bit 7 to 8
    Cfg_Calclkgate_Dis = 0  # bit 8 to 9
    Os_Cfg_Cl2Pwr_Pll1En_Gating_Ctrl = 0  # bit 9 to 10
    Os_Cfg_Gaonpwr_Gating_Ctrl = 0  # bit 10 to 11
    Os_Cfg_Cl2Pwr_Gating_Ctrl = 0  # bit 11 to 12
    Os_Cfg_Tr2Pwr_Gating_Ctrl = 0  # bit 12 to 13
    Cfg_Calclk_Srcsel = 0  # bit 13 to 14
    Os_Susclk_Dynclkgate_Mode = 0  # bit 14 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_MISC_SUS0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_MISC_SUS0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CFG_LOW_RATE_LKREN(Enum):
    CFG_LOW_RATE_LKREN_DISABLE = 0x0
    CFG_LOW_RATE_LKREN_ENABLE = 0x1


class OFFSET_MG_CLKHUB:
    MG_CLKHUB_LN0_PORT1 = 0x16839C
    MG_CLKHUB_LN1_PORT1 = 0x16879C
    MG_CLKHUB_LN0_PORT2 = 0x16939C
    MG_CLKHUB_LN1_PORT2 = 0x16979C
    MG_CLKHUB_LN0_PORT3 = 0x16A39C
    MG_CLKHUB_LN1_PORT3 = 0x16A79C
    MG_CLKHUB_LN0_PORT4 = 0x16B39C
    MG_CLKHUB_LN1_PORT4 = 0x16B79C


class _MG_CLKHUB(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Vhfclk_Overrides', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 3),
        ('Cfg_Low_Rate_Lkren', ctypes.c_uint32, 1),
        ('Od_Clkhub2_Iqgen_En', ctypes.c_uint32, 1),
        ('Od_Clkhub1_Iqgen_En', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 10),
        ('Od_Clkhub2_Rxvhf_Selclk1A_H', ctypes.c_uint32, 1),
        ('Od_Clkhub1_Rxvhf_Selclk1A_H', ctypes.c_uint32, 1),
        ('Hsclk_Overrides', ctypes.c_uint32, 6),
    ]


class REG_MG_CLKHUB(ctypes.Union):
    value = 0
    offset = 0

    Vhfclk_Overrides = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 11
    Cfg_Low_Rate_Lkren = 0  # bit 11 to 12
    Od_Clkhub2_Iqgen_En = 0  # bit 12 to 13
    Od_Clkhub1_Iqgen_En = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 24
    Od_Clkhub2_Rxvhf_Selclk1A_H = 0  # bit 24 to 25
    Od_Clkhub1_Rxvhf_Selclk1A_H = 0  # bit 25 to 26
    Hsclk_Overrides = 0  # bit 26 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MG_CLKHUB),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MG_CLKHUB, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

