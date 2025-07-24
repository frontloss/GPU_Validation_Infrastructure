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
# @file Gen12TranscoderRegs.py
# @brief contains Gen12TranscoderRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_HDMI_SCRAMBLING_ENABLED(Enum):
    HDMI_SCRAMBLING_ENABLED_DISABLE = 0x0
    HDMI_SCRAMBLING_ENABLED_ENABLE = 0x1


class ENUM_PORT_WIDTH_SELECTION(Enum):
    PORT_WIDTH_SELECTION_X1 = 0x0  # x1 Mode
    PORT_WIDTH_SELECTION_X2 = 0x1  # x2 Mode
    PORT_WIDTH_SELECTION_X3 = 0x2  # x3 Mode (DSI only)
    PORT_WIDTH_SELECTION_X4 = 0x3  # x4 Mode


class ENUM_HIGH_TMDS_CHAR_RATE(Enum):
    HIGH_TMDS_CHAR_RATE_DISABLE = 0x0  # TMDS Character Rate is less than or equal to 340 Mega-characters/second/channe
                                       # l
    HIGH_TMDS_CHAR_RATE_ENABLE = 0x1  # TMDS Character Rate is greater than 340 Mega-characters/second/channel


class ENUM_MULTISTREAM_HDCP_SELECT(Enum):
    MULTISTREAM_HDCP_SELECT_NO_HDCP = 0x0
    MULTISTREAM_HDCP_SELECT_SELECT_HDCP = 0x1


class ENUM_HDMI_SCRAMBLER_RESET_FREQUENCY(Enum):
    HDMI_SCRAMBLER_RESET_FREQUENCY_EVERY_LINE = 0x0  # SSCP sent on hsync of every line
    HDMI_SCRAMBLER_RESET_FREQUENCY_EVERY_OTHER_LINE = 0x1  # SSCP sent on hsync of every other line


class ENUM_HDMI_SCRAMBLER_CTS_ENABLE(Enum):
    HDMI_SCRAMBLER_CTS_DISABLE = 0x0
    HDMI_SCRAMBLER_CTS_ENABLE_TRUE = 0x1


class ENUM_DP_VC_PAYLOAD_ALLOCATE(Enum):
    DP_VC_PAYLOAD_ALLOCATE_DISABLE = 0x0
    DP_VC_PAYLOAD_ALLOCATE_ENABLE = 0x1


class ENUM_HDMI_DVI_HDCP_SIGNALING(Enum):
    HDMI_DVI_HDCP_SIGNALING_DISABLE = 0x0
    HDMI_DVI_HDCP_SIGNALING_ENABLE = 0x1


class ENUM_MST_TRANSPORT_SELECT(Enum):
    MST_TRANSPORT_SELECT_DPTP_A = 0x0
    MST_TRANSPORT_SELECT_DPTP_B = 0x1
    MST_TRANSPORT_SELECT_DPTP_C = 0x2
    MST_TRANSPORT_SELECT_DPTP_D = 0x3


class ENUM_DSI_INPUT_SELECT(Enum):
    DSI_INPUT_SELECT_PIPE_A = 0x0
    DSI_INPUT_SELECT_PIPE_B = 0x5
    DSI_INPUT_SELECT_PIPE_C = 0x6
    DSI_INPUT_SELECT_PIPE_D = 0x7


class ENUM_SYNC_POLARITY(Enum):
    SYNC_POLARITY_LOW = 0x0  # VS and HS are active low (inverted)
    SYNC_POLARITY_VS_LOW_HS_HIGH = 0x1  # VS is active low (inverted), HS is active high
    SYNC_POLARITY_VS_HIGH_HS_LOW = 0x2  # VS is active high, HS is active low (inverted)
    SYNC_POLARITY_HIGH = 0x3  # VS and HS are active high


class ENUM_BITS_PER_COLOR(Enum):
    BITS_PER_COLOR_8_BPC = 0x0
    BITS_PER_COLOR_10_BPC = 0x1
    BITS_PER_COLOR_6_BPC = 0x2
    BITS_PER_COLOR_12_BPC = 0x3


class ENUM_TRANS_DDI_MODE_SELECT(Enum):
    TRANS_DDI_MODE_SELECT_HDMI = 0x0  # Function in HDMI mode
    TRANS_DDI_MODE_SELECT_DVI = 0x1  # Function in DVI mode
    TRANS_DDI_MODE_SELECT_DP_SST = 0x2  # Function in DisplayPort SST mode
    TRANS_DDI_MODE_SELECT_DP_MST = 0x3  # Function in DisplayPort MST mode


class ENUM_DDI_SELECT(Enum):
    DDI_SELECT_NONE = 0x0
    DDI_SELECT_DDI_A = 0x1
    DDI_SELECT_DDI_B = 0x2
    DDI_SELECT_DDI_C = 0x3
    DDI_SELECT_DDI_USBC1 = 0x4
    DDI_SELECT_DDI_USBC2 = 0x5
    DDI_SELECT_DDI_USBC3 = 0x6
    DDI_SELECT_DDI_USBC4 = 0x7
    DDI_SELECT_DDI_USBC5 = 0x8
    DDI_SELECT_DDI_USBC6 = 0x9


class ENUM_TRANS_DDI_FUNCTION_ENABLE(Enum):
    TRANS_DDI_FUNCTION_DISABLE = 0x0
    TRANS_DDI_FUNCTION_ENABLE = 0x1


class OFFSET_TRANS_DDI_FUNC_CTL:
    TRANS_DDI_FUNC_CTL_A = 0x60400
    TRANS_DDI_FUNC_CTL_B = 0x61400
    TRANS_DDI_FUNC_CTL_C = 0x62400
    TRANS_DDI_FUNC_CTL_D = 0x63400
    TRANS_DDI_FUNC_CTL_DSI0 = 0x6B400
    TRANS_DDI_FUNC_CTL_DSI1 = 0x6BC00


class _TRANS_DDI_FUNC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HdmiScramblingEnabled', ctypes.c_uint32, 1),
        ('PortWidthSelection', ctypes.c_uint32, 3),
        ('HighTmdsCharRate', ctypes.c_uint32, 1),
        ('MultistreamHdcpSelect', ctypes.c_uint32, 1),
        ('HdmiScramblerResetFrequency', ctypes.c_uint32, 1),
        ('HdmiScramblerCtsEnable', ctypes.c_uint32, 1),
        ('DpVcPayloadAllocate', ctypes.c_uint32, 1),
        ('HdmiDviHdcpSignaling', ctypes.c_uint32, 1),
        ('MstTransportSelect', ctypes.c_uint32, 2),
        ('DsiInputSelect', ctypes.c_uint32, 3),
        ('Reserved15', ctypes.c_uint32, 1),
        ('SyncPolarity', ctypes.c_uint32, 2),
        ('Reserved18', ctypes.c_uint32, 2),
        ('BitsPerColor', ctypes.c_uint32, 3),
        ('Reserved23', ctypes.c_uint32, 1),
        ('TransDdiModeSelect', ctypes.c_uint32, 3),
        ('DdiSelect', ctypes.c_uint32, 4),
        ('TransDdiFunctionEnable', ctypes.c_uint32, 1),
    ]


class REG_TRANS_DDI_FUNC_CTL(ctypes.Union):
    value = 0
    offset = 0

    HdmiScramblingEnabled = 0  # bit 0 to 1
    PortWidthSelection = 0  # bit 1 to 4
    HighTmdsCharRate = 0  # bit 4 to 5
    MultistreamHdcpSelect = 0  # bit 5 to 6
    HdmiScramblerResetFrequency = 0  # bit 6 to 7
    HdmiScramblerCtsEnable = 0  # bit 7 to 8
    DpVcPayloadAllocate = 0  # bit 8 to 9
    HdmiDviHdcpSignaling = 0  # bit 9 to 10
    MstTransportSelect = 0  # bit 10 to 12
    DsiInputSelect = 0  # bit 12 to 15
    Reserved15 = 0  # bit 15 to 16
    SyncPolarity = 0  # bit 16 to 18
    Reserved18 = 0  # bit 18 to 20
    BitsPerColor = 0  # bit 20 to 23
    Reserved23 = 0  # bit 23 to 24
    TransDdiModeSelect = 0  # bit 24 to 27
    DdiSelect = 0  # bit 27 to 31
    TransDdiFunctionEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_DDI_FUNC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_DDI_FUNC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PORT_SYNC_MODE_MASTER_SELECT(Enum):
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_A = 0x1
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_B = 0x2
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_C = 0x3
    PORT_SYNC_MODE_MASTER_SELECT_TRANSCODER_D = 0x4


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
        ('Reserved3', ctypes.c_uint32, 1),
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
    Reserved3 = 0  # bit 3 to 4
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


class ENUM_DP_AUDIO_SYMBOL_WATERMARK(Enum):
    DP_AUDIO_SYMBOL_WATERMARK_36_ENTRIES = 0x24


class ENUM_STOP_FRAME_ENABLE(Enum):
    STOP_FRAME_DISABLED = 0x0
    STOP_FRAME_ENABLED = 0x1


class ENUM_INTERLACED_MODE(Enum):
    INTERLACED_MODE_PFPD = 0x0  # Progressive Fetch with Progressive Display
    INTERLACED_MODE_PFID = 0x1  # Progressive Fetch with Interlaced Display
    INTERLACED_MODE_IFID = 0x3  # Interlaced Fetch with Interlaced Display


class ENUM_TRANSCODER_STATE(Enum):
    TRANSCODER_STATE_DISABLED = 0x0
    TRANSCODER_STATE_ENABLED = 0x1


class ENUM_TRANSCODER_ENABLE(Enum):
    TRANSCODER_DISABLE = 0x0
    TRANSCODER_ENABLE = 0x1


class OFFSET_TRANS_CONF:
    TRANS_CONF_A = 0x70008
    TRANS_CONF_B = 0x71008
    TRANS_CONF_C = 0x72008
    TRANS_CONF_D = 0x73008
    TRANS_CONF_DSI0 = 0x7B008
    TRANS_CONF_DSI1 = 0x7B808
    TRANS_CONF_WD1 = 0x7D008
    TRANS_CONF_WD0 = 0x7E008


class _TRANS_CONF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DpAudioSymbolWatermark', ctypes.c_uint32, 7),
        ('StopFrameEnable', ctypes.c_uint32, 1),
        ('StopFrameCount', ctypes.c_uint32, 4),
        ('Reserved12', ctypes.c_uint32, 9),
        ('InterlacedMode', ctypes.c_uint32, 2),
        ('Reserved23', ctypes.c_uint32, 7),
        ('TranscoderState', ctypes.c_uint32, 1),
        ('TranscoderEnable', ctypes.c_uint32, 1),
    ]


class REG_TRANS_CONF(ctypes.Union):
    value = 0
    offset = 0

    DpAudioSymbolWatermark = 0  # bit 0 to 7
    StopFrameEnable = 0  # bit 7 to 8
    StopFrameCount = 0  # bit 8 to 12
    Reserved12 = 0  # bit 12 to 21
    InterlacedMode = 0  # bit 21 to 23
    Reserved23 = 0  # bit 23 to 30
    TranscoderState = 0  # bit 30 to 31
    TranscoderEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_CONF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_CONF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TRANS_CLOCK_SELECT(Enum):
    TRANS_CLOCK_SELECT_NONE_CLOCK_DISABLED = 0x0
    TRANS_CLOCK_SELECT_DDI_A = 0x1
    TRANS_CLOCK_SELECT_DDI_B = 0x2
    TRANS_CLOCK_SELECT_DDI_C = 0x3
    TRANS_CLOCK_SELECT_DDI_USBC1 = 0x4
    TRANS_CLOCK_SELECT_DDI_USBC2 = 0x5
    TRANS_CLOCK_SELECT_DDI_USBC3 = 0x6
    TRANS_CLOCK_SELECT_DDI_USBC4 = 0x7
    TRANS_CLOCK_SELECT_DDI_USBC5 = 0x8
    TRANS_CLOCK_SELECT_DDI_USBC6 = 0x9


class OFFSET_TRANS_CLK_SEL:
    TRANS_CLK_SEL_A = 0x46140
    TRANS_CLK_SEL_B = 0x46144
    TRANS_CLK_SEL_C = 0x46148
    TRANS_CLK_SEL_D = 0x4614C


class _TRANS_CLK_SEL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 28),
        ('TransClockSelect', ctypes.c_uint32, 4),
    ]


class REG_TRANS_CLK_SEL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 28
    TransClockSelect = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_CLK_SEL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_CLK_SEL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_MSA_MISC:
    TRANS_MSA_MISC_A = 0x60410
    TRANS_MSA_MISC_B = 0x61410
    TRANS_MSA_MISC_C = 0x62410
    TRANS_MSA_MISC_D = 0x63410


class _TRANS_MSA_MISC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MsaMisc0', ctypes.c_uint32, 8),
        ('MsaMisc1', ctypes.c_uint32, 8),
        ('MsaUnused', ctypes.c_uint32, 16),
    ]


class REG_TRANS_MSA_MISC(ctypes.Union):
    value = 0
    offset = 0

    MsaMisc0 = 0  # bit 0 to 8
    MsaMisc1 = 0  # bit 8 to 16
    MsaUnused = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_MSA_MISC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_MSA_MISC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DATAM:
    TRANS_DATAM1_A = 0x60030
    TRANS_DATAM1_B = 0x61030
    TRANS_DATAM1_C = 0x62030
    TRANS_DATAM1_D = 0x63030


class _DATAM(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DataMValue', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 1),
        ('TuOrVcpayloadSize', ctypes.c_uint32, 6),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_DATAM(ctypes.Union):
    value = 0
    offset = 0

    DataMValue = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 25
    TuOrVcpayloadSize = 0  # bit 25 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DATAM),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DATAM, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DATAN:
    TRANS_DATAN1_A = 0x60034
    TRANS_DATAN1_B = 0x61034
    TRANS_DATAN1_C = 0x62034
    TRANS_DATAN1_D = 0x63034


class _DATAN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DataNValue', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_DATAN(ctypes.Union):
    value = 0
    offset = 0

    DataNValue = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DATAN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DATAN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LINKM:
    TRANS_LINKM1_A = 0x60040
    TRANS_LINKM1_B = 0x61040
    TRANS_LINKM1_C = 0x62040
    TRANS_LINKM1_D = 0x63040


class _LINKM(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LinkMValue', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_LINKM(ctypes.Union):
    value = 0
    offset = 0

    LinkMValue = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LINKM),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LINKM, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LINKN:
    TRANS_LINKN1_A = 0x60044
    TRANS_LINKN1_B = 0x61044
    TRANS_LINKN1_C = 0x62044
    TRANS_LINKN1_D = 0x63044


class _LINKN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LinkNValue', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_LINKN(ctypes.Union):
    value = 0
    offset = 0

    LinkNValue = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LINKN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LINKN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_HTOTAL:
    TRANS_HTOTAL_A = 0x60000
    TRANS_HTOTAL_B = 0x61000
    TRANS_HTOTAL_C = 0x62000
    TRANS_HTOTAL_D = 0x63000
    TRANS_HTOTAL_DSI0 = 0x6B000
    TRANS_HTOTAL_DSI1 = 0x6B800
    TRANS_HTOTAL_WD0 = 0x6E000
    TRANS_HTOTAL_WD1 = 0x6E800


class _TRANS_HTOTAL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HorizontalActive', ctypes.c_uint32, 14),
        ('Reserved14', ctypes.c_uint32, 2),
        ('HorizontalTotal', ctypes.c_uint32, 14),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_TRANS_HTOTAL(ctypes.Union):
    value = 0
    offset = 0

    HorizontalActive = 0  # bit 0 to 14
    Reserved14 = 0  # bit 14 to 16
    HorizontalTotal = 0  # bit 16 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_HTOTAL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_HTOTAL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_HBLANK:
    TRANS_HBLANK_A = 0x60004
    TRANS_HBLANK_B = 0x61004
    TRANS_HBLANK_C = 0x62004
    TRANS_HBLANK_D = 0x63004


class _TRANS_HBLANK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HorizontalBlankStart', ctypes.c_uint32, 14),
        ('Reserved14', ctypes.c_uint32, 2),
        ('HorizontalBlankEnd', ctypes.c_uint32, 14),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_TRANS_HBLANK(ctypes.Union):
    value = 0
    offset = 0

    HorizontalBlankStart = 0  # bit 0 to 14
    Reserved14 = 0  # bit 14 to 16
    HorizontalBlankEnd = 0  # bit 16 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_HBLANK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_HBLANK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_HSYNC:
    TRANS_HSYNC_A = 0x60008
    TRANS_HSYNC_B = 0x61008
    TRANS_HSYNC_C = 0x62008
    TRANS_HSYNC_D = 0x63008
    TRANS_HSYNC_DSI0 = 0x6B008
    TRANS_HSYNC_DSI1 = 0x6B808


class _TRANS_HSYNC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HorizontalSyncStart', ctypes.c_uint32, 14),
        ('Reserved14', ctypes.c_uint32, 2),
        ('HorizontalSyncEnd', ctypes.c_uint32, 14),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_TRANS_HSYNC(ctypes.Union):
    value = 0
    offset = 0

    HorizontalSyncStart = 0  # bit 0 to 14
    Reserved14 = 0  # bit 14 to 16
    HorizontalSyncEnd = 0  # bit 16 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_HSYNC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_HSYNC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_VTOTAL:
    TRANS_VTOTAL_A = 0x6000C
    TRANS_VTOTAL_B = 0x6100C
    TRANS_VTOTAL_C = 0x6200C
    TRANS_VTOTAL_D = 0x6300C
    TRANS_VTOTAL_DSI0 = 0x6B00C
    TRANS_VTOTAL_DSI1 = 0x6B80C
    TRANS_VTOTAL_WD0 = 0x6E00C
    TRANS_VTOTAL_WD1 = 0x6E80C


class _TRANS_VTOTAL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VerticalActive', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('VerticalTotal', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_TRANS_VTOTAL(ctypes.Union):
    value = 0
    offset = 0

    VerticalActive = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    VerticalTotal = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VTOTAL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VTOTAL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_VBLANK:
    TRANS_VBLANK_A = 0x60010
    TRANS_VBLANK_B = 0x61010
    TRANS_VBLANK_C = 0x62010
    TRANS_VBLANK_D = 0x63010
    TRANS_VBLANK_DSI0 = 0x6B010
    TRANS_VBLANK_DSI1 = 0x6B810


class _TRANS_VBLANK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VerticalBlankStart', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('VerticalBlankEnd', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_TRANS_VBLANK(ctypes.Union):
    value = 0
    offset = 0

    VerticalBlankStart = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    VerticalBlankEnd = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VBLANK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VBLANK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_VSYNC:
    TRANS_VSYNC_A = 0x60014
    TRANS_VSYNC_B = 0x61014
    TRANS_VSYNC_C = 0x62014
    TRANS_VSYNC_D = 0x63014
    TRANS_VSYNC_DSI0 = 0x6B014
    TRANS_VSYNC_DSI1 = 0x6B814


class _TRANS_VSYNC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VerticalSyncStart', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('VerticalSyncEnd', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_TRANS_VSYNC(ctypes.Union):
    value = 0
    offset = 0

    VerticalSyncStart = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    VerticalSyncEnd = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VSYNC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VSYNC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_VSYNCSHIFT:
    TRANS_VSYNCSHIFT_A = 0x60028
    TRANS_VSYNCSHIFT_B = 0x61028
    TRANS_VSYNCSHIFT_C = 0x62028
    TRANS_VSYNCSHIFT_D = 0x63028
    TRANS_VSYNCSHIFT_DSI0 = 0x6B028
    TRANS_VSYNCSHIFT_DSI1 = 0x6B828


class _TRANS_VSYNCSHIFT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SecondFieldVsyncShift', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_TRANS_VSYNCSHIFT(ctypes.Union):
    value = 0
    offset = 0

    SecondFieldVsyncShift = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VSYNCSHIFT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VSYNCSHIFT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MULTIPLIER(Enum):
    MULTIPLIER_X1 = 0x0  # Multiply by 1
    MULTIPLIER_X2 = 0x1  # Multiply by 2
    MULTIPLIER_X4 = 0x3  # Multiply by 4


class OFFSET_TRANS_MULT:
    TRANS_MULT_A = 0x6002C
    TRANS_MULT_B = 0x6102C
    TRANS_MULT_C = 0x6202C
    TRANS_MULT_D = 0x6302C


class _TRANS_MULT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Multiplier', ctypes.c_uint32, 3),
        ('Reserved3', ctypes.c_uint32, 29),
    ]


class REG_TRANS_MULT(ctypes.Union):
    value = 0
    offset = 0

    Multiplier = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_MULT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_MULT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_SPACE:
    TRANS_SPACE_A = 0x60024
    TRANS_SPACE_B = 0x61024
    TRANS_SPACE_C = 0x62024
    TRANS_SPACE_D = 0x63024
    TRANS_SPACE_DSI0 = 0x6B024
    TRANS_SPACE_DSI1 = 0x6B824


class _TRANS_SPACE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VerticalActiveSpace', ctypes.c_uint32, 12),
        ('Reserved12', ctypes.c_uint32, 20),
    ]


class REG_TRANS_SPACE(ctypes.Union):
    value = 0
    offset = 0

    VerticalActiveSpace = 0  # bit 0 to 12
    Reserved12 = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_SPACE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_SPACE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_VDIP_ENABLE_SPD(Enum):
    VDIP_ENABLE_SPD_DISABLE_SPD_DIP = 0x0
    VDIP_ENABLE_SPD_ENABLE_SPD_DIP = 0x1


class ENUM_VDIP_ENABLE_GMP(Enum):
    VDIP_ENABLE_GMP_DISABLE_GMP_DIP = 0x0
    VDIP_ENABLE_GMP_ENABLE_GMP_DIP = 0x1


class ENUM_VDIP_ENABLE_VS(Enum):
    VDIP_ENABLE_VS_DISABLE_VS_DIP = 0x0
    VDIP_ENABLE_VS_ENABLE_VS_DIP = 0x1


class ENUM_VDIP_ENABLE_AVI(Enum):
    VDIP_ENABLE_AVI_DISABLE_AVI_DIP = 0x0
    VDIP_ENABLE_AVI_ENABLE_AVI_DIP = 0x1


class ENUM_VDIP_ENABLE_GCP(Enum):
    VDIP_ENABLE_GCP_DISABLE_GCP_DIP = 0x0
    VDIP_ENABLE_GCP_ENABLE_GCP_DIP = 0x1


class ENUM_VDIP_ENABLE_VSC(Enum):
    VDIP_ENABLE_VSC_DISABLE_VSC_DIP = 0x0
    VDIP_ENABLE_VSC_ENABLE_VSC_DIP = 0x1


class ENUM_VDIP_ENABLE_PPS(Enum):
    VDIP_ENABLE_PPS_DISABLE = 0x0
    VDIP_ENABLE_PPS_ENABLE = 0x1


class ENUM_VSC_SELECT(Enum):
    VSC_SELECT_HEADER_AND_DATA = 0x0  # Hardware controls header and data.
    VSC_SELECT_HEADER_ONLY = 0x1  # Hardware controls header, software controls data.
    VSC_SELECT_DATA_ONLY = 0x2  # Software controls header, hardware controls data.
    VSC_SELECT_NONE = 0x3  # Software controls header and data.


class ENUM_PSR_PSR2_VSC_BIT_7(Enum):
    PSR_PSR2_VSC_BIT_7_DO_NOT_SET = 0x0
    PSR_PSR2_VSC_BIT_7_SET = 0x1


class ENUM_DRM_DIP_ENABLE(Enum):
    DRM_DIP_ENABLE_DRM_DIP_ENABLE = 0x1
    DRM_DIP_ENABLE_DRM_DIP_DISABLE = 0x0


class OFFSET_VIDEO_DIP_CTL:
    VIDEO_DIP_CTL_A = 0x60200
    VIDEO_DIP_CTL_B = 0x61200
    VIDEO_DIP_CTL_C = 0x62200
    VIDEO_DIP_CTL_D = 0x63200


class _VIDEO_DIP_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VdipEnableSpd', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 3),
        ('VdipEnableGmp', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 3),
        ('VdipEnableVs', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 3),
        ('VdipEnableAvi', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 3),
        ('VdipEnableGcp', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 3),
        ('VdipEnableVsc', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 1),
        ('Reserved22', ctypes.c_uint32, 2),
        ('VdipEnablePps', ctypes.c_uint32, 1),
        ('VscSelect', ctypes.c_uint32, 2),
        ('PsrPsr2VscBit7', ctypes.c_uint32, 1),
        ('DrmDipEnable', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_VIDEO_DIP_CTL(ctypes.Union):
    value = 0
    offset = 0

    VdipEnableSpd = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 4
    VdipEnableGmp = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 8
    VdipEnableVs = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 12
    VdipEnableAvi = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 16
    VdipEnableGcp = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 20
    VdipEnableVsc = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 24
    VdipEnablePps = 0  # bit 24 to 25
    VscSelect = 0  # bit 25 to 27
    PsrPsr2VscBit7 = 0  # bit 27 to 28
    DrmDipEnable = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VIDEO_DIP_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VIDEO_DIP_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GCP_AV_MUTE(Enum):
    GCP_AV_MUTE_CLEAR = 0x0  # AV mute bit in GCP is cleared.
    GCP_AV_MUTE_SET = 0x1  # AV mute bit in GCP is set.


class ENUM_GCP_DEFAULT_PHASE_ENABLE(Enum):
    GCP_DEFAULT_PHASE_ENABLE_CLEAR = 0x0  # Default phase bit in GCP is cleared.
    GCP_DEFAULT_PHASE_ENABLE_SET = 0x1  # Default phase bit in GCP is set.


class ENUM_GCP_COLOR_INDICATION(Enum):
    GCP_COLOR_INDICATION_DON_T_INDICATE = 0x0  # Don't indicate color depth. CD and PP bits in GCP set to zero.
    GCP_COLOR_INDICATION_INDICATE = 0x1  # Indicate color depth using CD bits in GCP. The color depth value comes from 
                                         # the TRANS_DDI_FUNC_CTL register.


class OFFSET_VIDEO_DIP_GCP:
    VIDEO_DIP_GCP_A = 0x60210
    VIDEO_DIP_GCP_B = 0x61210
    VIDEO_DIP_GCP_C = 0x62210
    VIDEO_DIP_GCP_D = 0x63210


class _VIDEO_DIP_GCP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GcpAvMute', ctypes.c_uint32, 1),
        ('GcpDefaultPhaseEnable', ctypes.c_uint32, 1),
        ('GcpColorIndication', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 29),
    ]


class REG_VIDEO_DIP_GCP(ctypes.Union):
    value = 0
    offset = 0

    GcpAvMute = 0  # bit 0 to 1
    GcpDefaultPhaseEnable = 0  # bit 1 to 2
    GcpColorIndication = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VIDEO_DIP_GCP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VIDEO_DIP_GCP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_VIDEO_DIP_DATA:
    VIDEO_DIP_AVI_DATA_0_A = 0x60220
    VIDEO_DIP_AVI_DATA_1_A = 0x60224
    VIDEO_DIP_AVI_DATA_2_A = 0x60228
    VIDEO_DIP_AVI_DATA_3_A = 0x6022C
    VIDEO_DIP_AVI_DATA_4_A = 0x60230
    VIDEO_DIP_AVI_DATA_5_A = 0x60234
    VIDEO_DIP_AVI_DATA_6_A = 0x60238
    VIDEO_DIP_AVI_DATA_7_A = 0x6023C
    VIDEO_DIP_VS_DATA_0_A = 0x60260
    VIDEO_DIP_VS_DATA_1_A = 0x60264
    VIDEO_DIP_VS_DATA_2_A = 0x60268
    VIDEO_DIP_VS_DATA_3_A = 0x6026C
    VIDEO_DIP_VS_DATA_4_A = 0x60270
    VIDEO_DIP_VS_DATA_5_A = 0x60274
    VIDEO_DIP_VS_DATA_6_A = 0x60278
    VIDEO_DIP_VS_DATA_7_A = 0x6027C
    VIDEO_DIP_SPD_DATA_0_A = 0x602A0
    VIDEO_DIP_SPD_DATA_1_A = 0x602A4
    VIDEO_DIP_SPD_DATA_2_A = 0x602A8
    VIDEO_DIP_SPD_DATA_3_A = 0x602AC
    VIDEO_DIP_SPD_DATA_4_A = 0x602B0
    VIDEO_DIP_SPD_DATA_5_A = 0x602B4
    VIDEO_DIP_SPD_DATA_6_A = 0x602B8
    VIDEO_DIP_SPD_DATA_7_A = 0x602BC
    VIDEO_DIP_GMP_DATA_0_A = 0x602E0
    VIDEO_DIP_GMP_DATA_1_A = 0x602E4
    VIDEO_DIP_GMP_DATA_2_A = 0x602E8
    VIDEO_DIP_GMP_DATA_3_A = 0x602EC
    VIDEO_DIP_GMP_DATA_4_A = 0x602F0
    VIDEO_DIP_GMP_DATA_5_A = 0x602F4
    VIDEO_DIP_GMP_DATA_6_A = 0x602F8
    VIDEO_DIP_GMP_DATA_7_A = 0x602FC
    VIDEO_DIP_GMP_DATA_8_A = 0x60300
    VIDEO_DIP_VSC_DATA_0_A = 0x60320
    VIDEO_DIP_VSC_DATA_1_A = 0x60324
    VIDEO_DIP_VSC_DATA_2_A = 0x60328
    VIDEO_DIP_VSC_DATA_3_A = 0x6032C
    VIDEO_DIP_VSC_DATA_4_A = 0x60330
    VIDEO_DIP_VSC_DATA_5_A = 0x60334
    VIDEO_DIP_VSC_DATA_6_A = 0x60338
    VIDEO_DIP_VSC_DATA_7_A = 0x6033C
    VIDEO_DIP_VSC_DATA_8_A = 0x60340
    VIDEO_DIP_AVI_DATA_0_B = 0x61220
    VIDEO_DIP_AVI_DATA_1_B = 0x61224
    VIDEO_DIP_AVI_DATA_2_B = 0x61228
    VIDEO_DIP_AVI_DATA_3_B = 0x6122C
    VIDEO_DIP_AVI_DATA_4_B = 0x61230
    VIDEO_DIP_AVI_DATA_5_B = 0x61234
    VIDEO_DIP_AVI_DATA_6_B = 0x61238
    VIDEO_DIP_AVI_DATA_7_B = 0x6123C
    VIDEO_DIP_VS_DATA_0_B = 0x61260
    VIDEO_DIP_VS_DATA_1_B = 0x61264
    VIDEO_DIP_VS_DATA_2_B = 0x61268
    VIDEO_DIP_VS_DATA_3_B = 0x6126C
    VIDEO_DIP_VS_DATA_4_B = 0x61270
    VIDEO_DIP_VS_DATA_5_B = 0x61274
    VIDEO_DIP_VS_DATA_6_B = 0x61278
    VIDEO_DIP_VS_DATA_7_B = 0x6127C
    VIDEO_DIP_SPD_DATA_0_B = 0x612A0
    VIDEO_DIP_SPD_DATA_1_B = 0x612A4
    VIDEO_DIP_SPD_DATA_2_B = 0x612A8
    VIDEO_DIP_SPD_DATA_3_B = 0x612AC
    VIDEO_DIP_SPD_DATA_4_B = 0x612B0
    VIDEO_DIP_SPD_DATA_5_B = 0x612B4
    VIDEO_DIP_SPD_DATA_6_B = 0x612B8
    VIDEO_DIP_SPD_DATA_7_B = 0x612BC
    VIDEO_DIP_GMP_DATA_0_B = 0x612E0
    VIDEO_DIP_GMP_DATA_1_B = 0x612E4
    VIDEO_DIP_GMP_DATA_2_B = 0x612E8
    VIDEO_DIP_GMP_DATA_3_B = 0x612EC
    VIDEO_DIP_GMP_DATA_4_B = 0x612F0
    VIDEO_DIP_GMP_DATA_5_B = 0x612F4
    VIDEO_DIP_GMP_DATA_6_B = 0x612F8
    VIDEO_DIP_GMP_DATA_7_B = 0x612FC
    VIDEO_DIP_GMP_DATA_8_B = 0x61300
    VIDEO_DIP_VSC_DATA_0_B = 0x61320
    VIDEO_DIP_VSC_DATA_1_B = 0x61324
    VIDEO_DIP_VSC_DATA_2_B = 0x61328
    VIDEO_DIP_VSC_DATA_3_B = 0x6132C
    VIDEO_DIP_VSC_DATA_4_B = 0x61330
    VIDEO_DIP_VSC_DATA_5_B = 0x61334
    VIDEO_DIP_VSC_DATA_6_B = 0x61338
    VIDEO_DIP_VSC_DATA_7_B = 0x6133C
    VIDEO_DIP_VSC_DATA_8_B = 0x61340
    VIDEO_DIP_AVI_DATA_0_C = 0x62220
    VIDEO_DIP_AVI_DATA_1_C = 0x62224
    VIDEO_DIP_AVI_DATA_2_C = 0x62228
    VIDEO_DIP_AVI_DATA_3_C = 0x6222C
    VIDEO_DIP_AVI_DATA_4_C = 0x62230
    VIDEO_DIP_AVI_DATA_5_C = 0x62234
    VIDEO_DIP_AVI_DATA_6_C = 0x62238
    VIDEO_DIP_AVI_DATA_7_C = 0x6223C
    VIDEO_DIP_VS_DATA_0_C = 0x62260
    VIDEO_DIP_VS_DATA_1_C = 0x62264
    VIDEO_DIP_VS_DATA_2_C = 0x62268
    VIDEO_DIP_VS_DATA_3_C = 0x6226C
    VIDEO_DIP_VS_DATA_4_C = 0x62270
    VIDEO_DIP_VS_DATA_5_C = 0x62274
    VIDEO_DIP_VS_DATA_6_C = 0x62278
    VIDEO_DIP_VS_DATA_7_C = 0x6227C
    VIDEO_DIP_SPD_DATA_0_C = 0x622A0
    VIDEO_DIP_SPD_DATA_1_C = 0x622A4
    VIDEO_DIP_SPD_DATA_2_C = 0x622A8
    VIDEO_DIP_SPD_DATA_3_C = 0x622AC
    VIDEO_DIP_SPD_DATA_4_C = 0x622B0
    VIDEO_DIP_SPD_DATA_5_C = 0x622B4
    VIDEO_DIP_SPD_DATA_6_C = 0x622B8
    VIDEO_DIP_SPD_DATA_7_C = 0x622BC
    VIDEO_DIP_GMP_DATA_0_C = 0x622E0
    VIDEO_DIP_GMP_DATA_1_C = 0x622E4
    VIDEO_DIP_GMP_DATA_2_C = 0x622E8
    VIDEO_DIP_GMP_DATA_3_C = 0x622EC
    VIDEO_DIP_GMP_DATA_4_C = 0x622F0
    VIDEO_DIP_GMP_DATA_5_C = 0x622F4
    VIDEO_DIP_GMP_DATA_6_C = 0x622F8
    VIDEO_DIP_GMP_DATA_7_C = 0x622FC
    VIDEO_DIP_GMP_DATA_8_C = 0x62300
    VIDEO_DIP_VSC_DATA_0_C = 0x62320
    VIDEO_DIP_VSC_DATA_1_C = 0x62324
    VIDEO_DIP_VSC_DATA_2_C = 0x62328
    VIDEO_DIP_VSC_DATA_3_C = 0x6232C
    VIDEO_DIP_VSC_DATA_4_C = 0x62330
    VIDEO_DIP_VSC_DATA_5_C = 0x62334
    VIDEO_DIP_VSC_DATA_6_C = 0x62338
    VIDEO_DIP_VSC_DATA_7_C = 0x6233C
    VIDEO_DIP_VSC_DATA_8_C = 0x62340
    VIDEO_DIP_AVI_DATA_0_D = 0x63220
    VIDEO_DIP_AVI_DATA_1_D = 0x63224
    VIDEO_DIP_AVI_DATA_2_D = 0x63228
    VIDEO_DIP_AVI_DATA_3_D = 0x6322C
    VIDEO_DIP_AVI_DATA_4_D = 0x63230
    VIDEO_DIP_AVI_DATA_5_D = 0x63234
    VIDEO_DIP_AVI_DATA_6_D = 0x63238
    VIDEO_DIP_AVI_DATA_7_D = 0x6323C
    VIDEO_DIP_VS_DATA_0_D = 0x63260
    VIDEO_DIP_VS_DATA_1_D = 0x63264
    VIDEO_DIP_VS_DATA_2_D = 0x63268
    VIDEO_DIP_VS_DATA_3_D = 0x6326C
    VIDEO_DIP_VS_DATA_4_D = 0x63270
    VIDEO_DIP_VS_DATA_5_D = 0x63274
    VIDEO_DIP_VS_DATA_6_D = 0x63278
    VIDEO_DIP_VS_DATA_7_D = 0x6327C
    VIDEO_DIP_SPD_DATA_0_D = 0x632A0
    VIDEO_DIP_SPD_DATA_1_D = 0x632A4
    VIDEO_DIP_SPD_DATA_2_D = 0x632A8
    VIDEO_DIP_SPD_DATA_3_D = 0x632AC
    VIDEO_DIP_SPD_DATA_4_D = 0x632B0
    VIDEO_DIP_SPD_DATA_5_D = 0x632B4
    VIDEO_DIP_SPD_DATA_6_D = 0x632B8
    VIDEO_DIP_SPD_DATA_7_D = 0x632BC
    VIDEO_DIP_GMP_DATA_0_D = 0x632E0
    VIDEO_DIP_GMP_DATA_1_D = 0x632E4
    VIDEO_DIP_GMP_DATA_2_D = 0x632E8
    VIDEO_DIP_GMP_DATA_3_D = 0x632EC
    VIDEO_DIP_GMP_DATA_4_D = 0x632F0
    VIDEO_DIP_GMP_DATA_5_D = 0x632F4
    VIDEO_DIP_GMP_DATA_6_D = 0x632F8
    VIDEO_DIP_GMP_DATA_7_D = 0x632FC
    VIDEO_DIP_GMP_DATA_8_D = 0x63300
    VIDEO_DIP_VSC_DATA_0_D = 0x63320
    VIDEO_DIP_VSC_DATA_1_D = 0x63324
    VIDEO_DIP_VSC_DATA_2_D = 0x63328
    VIDEO_DIP_VSC_DATA_3_D = 0x6332C
    VIDEO_DIP_VSC_DATA_4_D = 0x63330
    VIDEO_DIP_VSC_DATA_5_D = 0x63334
    VIDEO_DIP_VSC_DATA_6_D = 0x63338
    VIDEO_DIP_VSC_DATA_7_D = 0x6333C
    VIDEO_DIP_VSC_DATA_8_D = 0x63340


class _VIDEO_DIP_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VideoDipData', ctypes.c_uint32, 32),
    ]


class REG_VIDEO_DIP_DATA(ctypes.Union):
    value = 0
    offset = 0

    VideoDipData = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VIDEO_DIP_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VIDEO_DIP_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_VIDEO_DIP_DRM_DATA:
    VIDEO_DIP_DRM_DATA_0_A = 0x60440
    VIDEO_DIP_DRM_DATA_1_A = 0x60444
    VIDEO_DIP_DRM_DATA_2_A = 0x60448
    VIDEO_DIP_DRM_DATA_3_A = 0x6044C
    VIDEO_DIP_DRM_DATA_4_A = 0x60450
    VIDEO_DIP_DRM_DATA_5_A = 0x60454
    VIDEO_DIP_DRM_DATA_6_A = 0x60458
    VIDEO_DIP_DRM_DATA_7_A = 0x6045C
    VIDEO_DIP_DRM_DATA_0_B = 0x61440
    VIDEO_DIP_DRM_DATA_1_B = 0x61444
    VIDEO_DIP_DRM_DATA_2_B = 0x61448
    VIDEO_DIP_DRM_DATA_3_B = 0x6144C
    VIDEO_DIP_DRM_DATA_4_B = 0x61450
    VIDEO_DIP_DRM_DATA_5_B = 0x61454
    VIDEO_DIP_DRM_DATA_6_B = 0x61458
    VIDEO_DIP_DRM_DATA_7_B = 0x6145C
    VIDEO_DIP_DRM_DATA_0_C = 0x62440
    VIDEO_DIP_DRM_DATA_1_C = 0x62444
    VIDEO_DIP_DRM_DATA_2_C = 0x62448
    VIDEO_DIP_DRM_DATA_3_C = 0x6244C
    VIDEO_DIP_DRM_DATA_4_C = 0x62450
    VIDEO_DIP_DRM_DATA_5_C = 0x62454
    VIDEO_DIP_DRM_DATA_6_C = 0x62458
    VIDEO_DIP_DRM_DATA_7_C = 0x6245C
    VIDEO_DIP_DRM_DATA_0_D = 0x63440
    VIDEO_DIP_DRM_DATA_1_D = 0x63444
    VIDEO_DIP_DRM_DATA_2_D = 0x63448
    VIDEO_DIP_DRM_DATA_3_D = 0x6344C
    VIDEO_DIP_DRM_DATA_4_D = 0x63450
    VIDEO_DIP_DRM_DATA_5_D = 0x63454
    VIDEO_DIP_DRM_DATA_6_D = 0x63458
    VIDEO_DIP_DRM_DATA_7_D = 0x6345C


class _VIDEO_DIP_DRM_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DrmDipData', ctypes.c_uint32, 32),
    ]


class REG_VIDEO_DIP_DRM_DATA(ctypes.Union):
    value = 0
    offset = 0

    DrmDipData = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VIDEO_DIP_DRM_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VIDEO_DIP_DRM_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_VIDEO_DIP_PPS_DATA:
    VIDEO_DIP_PPS_DATA_0_A = 0x60350
    VIDEO_DIP_PPS_DATA_1_A = 0x60354
    VIDEO_DIP_PPS_DATA_2_A = 0x60358
    VIDEO_DIP_PPS_DATA_3_A = 0x6035C
    VIDEO_DIP_PPS_DATA_4_A = 0x60360
    VIDEO_DIP_PPS_DATA_5_A = 0x60364
    VIDEO_DIP_PPS_DATA_6_A = 0x60368
    VIDEO_DIP_PPS_DATA_7_A = 0x6036C
    VIDEO_DIP_PPS_DATA_8_A = 0x60370
    VIDEO_DIP_PPS_DATA_9_A = 0x60374
    VIDEO_DIP_PPS_DATA_10_A = 0x60378
    VIDEO_DIP_PPS_DATA_11_A = 0x6037C
    VIDEO_DIP_PPS_DATA_12_A = 0x60380
    VIDEO_DIP_PPS_DATA_13_A = 0x60384
    VIDEO_DIP_PPS_DATA_14_A = 0x60388
    VIDEO_DIP_PPS_DATA_15_A = 0x6038C
    VIDEO_DIP_PPS_DATA_16_A = 0x60390
    VIDEO_DIP_PPS_DATA_17_A = 0x60394
    VIDEO_DIP_PPS_DATA_18_A = 0x60398
    VIDEO_DIP_PPS_DATA_19_A = 0x6039C
    VIDEO_DIP_PPS_DATA_20_A = 0x603A0
    VIDEO_DIP_PPS_DATA_21_A = 0x603A4
    VIDEO_DIP_PPS_DATA_22_A = 0x603A8
    VIDEO_DIP_PPS_DATA_23_A = 0x603AC
    VIDEO_DIP_PPS_DATA_24_A = 0x603B0
    VIDEO_DIP_PPS_DATA_25_A = 0x603B4
    VIDEO_DIP_PPS_DATA_26_A = 0x603B8
    VIDEO_DIP_PPS_DATA_27_A = 0x603BC
    VIDEO_DIP_PPS_DATA_28_A = 0x603C0
    VIDEO_DIP_PPS_DATA_29_A = 0x603C4
    VIDEO_DIP_PPS_DATA_30_A = 0x603C8
    VIDEO_DIP_PPS_DATA_31_A = 0x603CC
    VIDEO_DIP_PPS_DATA_32_A = 0x603D0
    VIDEO_DIP_PPS_DATA_0_B = 0x61350
    VIDEO_DIP_PPS_DATA_1_B = 0x61354
    VIDEO_DIP_PPS_DATA_2_B = 0x61358
    VIDEO_DIP_PPS_DATA_3_B = 0x6135C
    VIDEO_DIP_PPS_DATA_4_B = 0x61360
    VIDEO_DIP_PPS_DATA_5_B = 0x61364
    VIDEO_DIP_PPS_DATA_6_B = 0x61368
    VIDEO_DIP_PPS_DATA_7_B = 0x6136C
    VIDEO_DIP_PPS_DATA_8_B = 0x61370
    VIDEO_DIP_PPS_DATA_9_B = 0x61374
    VIDEO_DIP_PPS_DATA_10_B = 0x61378
    VIDEO_DIP_PPS_DATA_11_B = 0x6137C
    VIDEO_DIP_PPS_DATA_12_B = 0x61380
    VIDEO_DIP_PPS_DATA_13_B = 0x61384
    VIDEO_DIP_PPS_DATA_14_B = 0x61388
    VIDEO_DIP_PPS_DATA_15_B = 0x6138C
    VIDEO_DIP_PPS_DATA_16_B = 0x61390
    VIDEO_DIP_PPS_DATA_17_B = 0x61394
    VIDEO_DIP_PPS_DATA_18_B = 0x61398
    VIDEO_DIP_PPS_DATA_19_B = 0x6139C
    VIDEO_DIP_PPS_DATA_20_B = 0x613A0
    VIDEO_DIP_PPS_DATA_21_B = 0x613A4
    VIDEO_DIP_PPS_DATA_22_B = 0x613A8
    VIDEO_DIP_PPS_DATA_23_B = 0x613AC
    VIDEO_DIP_PPS_DATA_24_B = 0x613B0
    VIDEO_DIP_PPS_DATA_25_B = 0x613B4
    VIDEO_DIP_PPS_DATA_26_B = 0x613B8
    VIDEO_DIP_PPS_DATA_27_B = 0x613BC
    VIDEO_DIP_PPS_DATA_28_B = 0x613C0
    VIDEO_DIP_PPS_DATA_29_B = 0x613C4
    VIDEO_DIP_PPS_DATA_30_B = 0x613C8
    VIDEO_DIP_PPS_DATA_31_B = 0x613CC
    VIDEO_DIP_PPS_DATA_32_B = 0x613D0
    VIDEO_DIP_PPS_DATA_0_C = 0x62350
    VIDEO_DIP_PPS_DATA_1_C = 0x62354
    VIDEO_DIP_PPS_DATA_2_C = 0x62358
    VIDEO_DIP_PPS_DATA_3_C = 0x6235C
    VIDEO_DIP_PPS_DATA_4_C = 0x62360
    VIDEO_DIP_PPS_DATA_5_C = 0x62364
    VIDEO_DIP_PPS_DATA_6_C = 0x62368
    VIDEO_DIP_PPS_DATA_7_C = 0x6236C
    VIDEO_DIP_PPS_DATA_8_C = 0x62370
    VIDEO_DIP_PPS_DATA_9_C = 0x62374
    VIDEO_DIP_PPS_DATA_10_C = 0x62378
    VIDEO_DIP_PPS_DATA_11_C = 0x6237C
    VIDEO_DIP_PPS_DATA_12_C = 0x62380
    VIDEO_DIP_PPS_DATA_13_C = 0x62384
    VIDEO_DIP_PPS_DATA_14_C = 0x62388
    VIDEO_DIP_PPS_DATA_15_C = 0x6238C
    VIDEO_DIP_PPS_DATA_16_C = 0x62390
    VIDEO_DIP_PPS_DATA_17_C = 0x62394
    VIDEO_DIP_PPS_DATA_18_C = 0x62398
    VIDEO_DIP_PPS_DATA_19_C = 0x6239C
    VIDEO_DIP_PPS_DATA_20_C = 0x623A0
    VIDEO_DIP_PPS_DATA_21_C = 0x623A4
    VIDEO_DIP_PPS_DATA_22_C = 0x623A8
    VIDEO_DIP_PPS_DATA_23_C = 0x623AC
    VIDEO_DIP_PPS_DATA_24_C = 0x623B0
    VIDEO_DIP_PPS_DATA_25_C = 0x623B4
    VIDEO_DIP_PPS_DATA_26_C = 0x623B8
    VIDEO_DIP_PPS_DATA_27_C = 0x623BC
    VIDEO_DIP_PPS_DATA_28_C = 0x623C0
    VIDEO_DIP_PPS_DATA_29_C = 0x623C4
    VIDEO_DIP_PPS_DATA_30_C = 0x623C8
    VIDEO_DIP_PPS_DATA_31_C = 0x623CC
    VIDEO_DIP_PPS_DATA_32_C = 0x623D0
    VIDEO_DIP_PPS_DATA_0_D = 0x63350
    VIDEO_DIP_PPS_DATA_1_D = 0x63354
    VIDEO_DIP_PPS_DATA_2_D = 0x63358
    VIDEO_DIP_PPS_DATA_3_D = 0x6335C
    VIDEO_DIP_PPS_DATA_4_D = 0x63360
    VIDEO_DIP_PPS_DATA_5_D = 0x63364
    VIDEO_DIP_PPS_DATA_6_D = 0x63368
    VIDEO_DIP_PPS_DATA_7_D = 0x6336C
    VIDEO_DIP_PPS_DATA_8_D = 0x63370
    VIDEO_DIP_PPS_DATA_9_D = 0x63374
    VIDEO_DIP_PPS_DATA_10_D = 0x63378
    VIDEO_DIP_PPS_DATA_11_D = 0x6337C
    VIDEO_DIP_PPS_DATA_12_D = 0x63380
    VIDEO_DIP_PPS_DATA_13_D = 0x63384
    VIDEO_DIP_PPS_DATA_14_D = 0x63388
    VIDEO_DIP_PPS_DATA_15_D = 0x6338C
    VIDEO_DIP_PPS_DATA_16_D = 0x63390
    VIDEO_DIP_PPS_DATA_17_D = 0x63394
    VIDEO_DIP_PPS_DATA_18_D = 0x63398
    VIDEO_DIP_PPS_DATA_19_D = 0x6339C
    VIDEO_DIP_PPS_DATA_20_D = 0x633A0
    VIDEO_DIP_PPS_DATA_21_D = 0x633A4
    VIDEO_DIP_PPS_DATA_22_D = 0x633A8
    VIDEO_DIP_PPS_DATA_23_D = 0x633AC
    VIDEO_DIP_PPS_DATA_24_D = 0x633B0
    VIDEO_DIP_PPS_DATA_25_D = 0x633B4
    VIDEO_DIP_PPS_DATA_26_D = 0x633B8
    VIDEO_DIP_PPS_DATA_27_D = 0x633BC
    VIDEO_DIP_PPS_DATA_28_D = 0x633C0
    VIDEO_DIP_PPS_DATA_29_D = 0x633C4
    VIDEO_DIP_PPS_DATA_30_D = 0x633C8
    VIDEO_DIP_PPS_DATA_31_D = 0x633CC
    VIDEO_DIP_PPS_DATA_32_D = 0x633D0


class _VIDEO_DIP_PPS_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VideoDipPpsData', ctypes.c_uint32, 32),
    ]


class REG_VIDEO_DIP_PPS_DATA(ctypes.Union):
    value = 0
    offset = 0

    VideoDipPpsData = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VIDEO_DIP_PPS_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VIDEO_DIP_PPS_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_VIDEO_DIP_DRM_ECC:
    VIDEO_DIP_DRM_ECC_0_A = 0x60460
    VIDEO_DIP_DRM_ECC_1_A = 0x60464
    VIDEO_DIP_DRM_ECC_0_B = 0x61460
    VIDEO_DIP_DRM_ECC_1_B = 0x61464
    VIDEO_DIP_DRM_ECC_0_C = 0x62460
    VIDEO_DIP_DRM_ECC_1_C = 0x62464
    VIDEO_DIP_DRM_ECC_0_D = 0x63460
    VIDEO_DIP_DRM_ECC_1_D = 0x63464


class _VIDEO_DIP_DRM_ECC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DrmEccData', ctypes.c_uint32, 32),
    ]


class REG_VIDEO_DIP_DRM_ECC(ctypes.Union):
    value = 0
    offset = 0

    DrmEccData = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VIDEO_DIP_DRM_ECC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VIDEO_DIP_DRM_ECC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_VRR_VMIN:
    TRANS_VRR_VMIN_A = 0x60434
    TRANS_VRR_VMIN_B = 0x61434
    TRANS_VRR_VMIN_C = 0x62434
    TRANS_VRR_VMIN_D = 0x63434


class _TRANS_VRR_VMIN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VrrVmin', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_TRANS_VRR_VMIN(ctypes.Union):
    value = 0
    offset = 0

    VrrVmin = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VRR_VMIN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VRR_VMIN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_VRR_VMAX:
    TRANS_VRR_VMAX_A = 0x60424
    TRANS_VRR_VMAX_B = 0x61424
    TRANS_VRR_VMAX_C = 0x62424
    TRANS_VRR_VMAX_D = 0x63424


class _TRANS_VRR_VMAX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VrrVmax', ctypes.c_uint32, 20),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_TRANS_VRR_VMAX(ctypes.Union):
    value = 0
    offset = 0

    VrrVmax = 0  # bit 0 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VRR_VMAX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VRR_VMAX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PIPELINE_FULL_OVERRIDE(Enum):
    PIPELINE_FULL_OVERRIDE_HW_GENERATED_PIPELINE_FULL_LINE_COUNT = 0x0
    PIPELINE_FULL_OVERRIDE_PROGRAMMED_PIPELINE_FULL_LINE_COUNT = 0x1


class ENUM_FLIP_LINE_ENABLE(Enum):
    FLIP_LINE_DISABLE = 0x0
    FLIP_LINE_ENABLE = 0x1


class ENUM_IGNORE_MAX_SHIFT(Enum):
    IGNORE_MAX_SHIFT_IGNORE = 0x1
    IGNORE_MAX_SHIFT_DO_NOT_IGNORE = 0x0


class ENUM_VRR_ENABLE(Enum):
    VRR_DISABLE = 0x0
    VRR_ENABLE = 0x1


class OFFSET_TRANS_VRR_CTL:
    TRANS_VRR_CTL_A = 0x60420
    TRANS_VRR_CTL_B = 0x61420
    TRANS_VRR_CTL_C = 0x62420
    TRANS_VRR_CTL_D = 0x63420


class _TRANS_VRR_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PipelineFullOverride', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 2),
        ('FramestartToPipelineFullLinecount', ctypes.c_uint32, 8),
        ('Reserved11', ctypes.c_uint32, 5),
        ('Reserved16', ctypes.c_uint32, 13),
        ('FlipLineEnable', ctypes.c_uint32, 1),
        ('IgnoreMaxShift', ctypes.c_uint32, 1),
        ('VrrEnable', ctypes.c_uint32, 1),
    ]


class REG_TRANS_VRR_CTL(ctypes.Union):
    value = 0
    offset = 0

    PipelineFullOverride = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 3
    FramestartToPipelineFullLinecount = 0  # bit 3 to 11
    Reserved11 = 0  # bit 11 to 16
    Reserved16 = 0  # bit 16 to 29
    FlipLineEnable = 0  # bit 29 to 30
    IgnoreMaxShift = 0  # bit 30 to 31
    VrrEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VRR_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VRR_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CURRENT_REGION_IN_VBLANK(Enum):
    CURRENT_REGION_IN_VBLANK_IDLE = 0x0  # Timing generator disabled.
    CURRENT_REGION_IN_VBLANK_WAIT_TILL_FDB = 0x1  # Wait till the flip decision boundary
    CURRENT_REGION_IN_VBLANK_WAIT_TILL_FRAMESTART = 0x2  # After the decision boundary, wait for framestart
    CURRENT_REGION_IN_VBLANK_WAIT_TILL_FLIP = 0x3  # Transition to this state when past the decision boundary, but no m
                                                   # aster flip
    CURRENT_REGION_IN_VBLANK_PIPELINE_FILL = 0x4  # State after framestart, waiting for a fixed num of lines
    CURRENT_REGION_IN_VBLANK_ACTIVE = 0x5
    CURRENT_REGION_IN_VBLANK_LEGACY_VBLANK = 0x6  # No VRR


class ENUM_VMAX_REACHED(Enum):
    VMAX_REACHED_NOT_REACHED = 0x0
    VMAX_REACHED_REACHED = 0x1


class OFFSET_TRANS_VRR_STATUS:
    TRANS_VRR_STATUS_A = 0x6042C
    TRANS_VRR_STATUS_B = 0x6142C
    TRANS_VRR_STATUS_C = 0x6242C
    TRANS_VRR_STATUS_D = 0x6342C


class _TRANS_VRR_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 20),
        ('CurrentRegionInVblank', ctypes.c_uint32, 3),
        ('Reserved23', ctypes.c_uint32, 3),
        ('FlipsServiced', ctypes.c_uint32, 1),
        ('VrrEnableLive', ctypes.c_uint32, 1),
        ('NoFlipFrame', ctypes.c_uint32, 1),
        ('FlipBeforeDecisionBoundary', ctypes.c_uint32, 1),
        ('NoFlipTillDecisionBoundary', ctypes.c_uint32, 1),
        ('VmaxReached', ctypes.c_uint32, 1),
    ]


class REG_TRANS_VRR_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 20
    CurrentRegionInVblank = 0  # bit 20 to 23
    Reserved23 = 0  # bit 23 to 26
    FlipsServiced = 0  # bit 26 to 27
    VrrEnableLive = 0  # bit 27 to 28
    NoFlipFrame = 0  # bit 28 to 29
    FlipBeforeDecisionBoundary = 0  # bit 29 to 30
    NoFlipTillDecisionBoundary = 0  # bit 30 to 31
    VmaxReached = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VRR_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VRR_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_VRR_VTOTAL_PREV:
    TRANS_VRR_VTOTAL_PREV_A = 0x60480
    TRANS_VRR_VTOTAL_PREV_B = 0x61480
    TRANS_VRR_VTOTAL_PREV_C = 0x62480
    TRANS_VRR_VTOTAL_PREV_D = 0x63480


class _TRANS_VRR_VTOTAL_PREV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VtotalPrevious', ctypes.c_uint32, 20),
        ('Reserved20', ctypes.c_uint32, 9),
        ('FlipAfterDoubleBuffer', ctypes.c_uint32, 1),
        ('FlipAfterBoundary', ctypes.c_uint32, 1),
        ('FlipBeforeBoundary', ctypes.c_uint32, 1),
    ]


class REG_TRANS_VRR_VTOTAL_PREV(ctypes.Union):
    value = 0
    offset = 0

    VtotalPrevious = 0  # bit 0 to 20
    Reserved20 = 0  # bit 20 to 29
    FlipAfterDoubleBuffer = 0  # bit 29 to 30
    FlipAfterBoundary = 0  # bit 30 to 31
    FlipBeforeBoundary = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VRR_VTOTAL_PREV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VRR_VTOTAL_PREV, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_VRR_FLIPLINE:
    TRANS_VRR_FLIPLINE_A = 0x60438
    TRANS_VRR_FLIPLINE_B = 0x61438
    TRANS_VRR_FLIPLINE_C = 0x62438
    TRANS_VRR_FLIPLINE_D = 0x63438


class _TRANS_VRR_FLIPLINE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VrrFlipline', ctypes.c_uint32, 20),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_TRANS_VRR_FLIPLINE(ctypes.Union):
    value = 0
    offset = 0

    VrrFlipline = 0  # bit 0 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VRR_FLIPLINE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VRR_FLIPLINE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_TRANS_VRR_STATUS2:
    TRANS_VRR_STATUS2_A = 0x6043C
    TRANS_VRR_STATUS2_B = 0x6143C
    TRANS_VRR_STATUS2_C = 0x6243C
    TRANS_VRR_STATUS2_D = 0x6343C


class _TRANS_VRR_STATUS2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VerticalLineCounterStatus', ctypes.c_uint32, 20),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_TRANS_VRR_STATUS2(ctypes.Union):
    value = 0
    offset = 0

    VerticalLineCounterStatus = 0  # bit 0 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_VRR_STATUS2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_VRR_STATUS2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PUSH_ENABLE(Enum):
    PUSH_DISABLE = 0x0
    PUSH_ENABLE = 0x1


class OFFSET_TRANS_PUSH:
    TRANS_PUSH_A = 0x60A70
    TRANS_PUSH_B = 0x61A70
    TRANS_PUSH_C = 0x62A70
    TRANS_PUSH_D = 0x63A70


class _TRANS_PUSH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 30),
        ('SendPush', ctypes.c_uint32, 1),
        ('PushEnable', ctypes.c_uint32, 1),
    ]


class REG_TRANS_PUSH(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 30
    SendPush = 0  # bit 30 to 31
    PushEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_PUSH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_PUSH, self).__init__()
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
    DP_LINK_TRAINING_ENABLE_PATTERN_1 = 0x0  # Training Pattern 1 enabled.
    DP_LINK_TRAINING_ENABLE_PATTERN_2 = 0x1  # Training Pattern 2 enabled.
    DP_LINK_TRAINING_ENABLE_IDLE = 0x2  # Idle Pattern enabled.
    DP_LINK_TRAINING_ENABLE_NORMAL = 0x3  # Link not in training: Send normal pixels
    DP_LINK_TRAINING_ENABLE_PATTERN_3 = 0x4  # Training Pattern 3 enabled.
    DP_LINK_TRAINING_ENABLE_PATTERN_4 = 0x5  # Training Pattern 4 enabled.


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
    DP_TP_CTL_A = 0x60540
    DP_TP_CTL_B = 0x61540
    DP_TP_CTL_C = 0x62540
    DP_TP_CTL_D = 0x63540


class _DP_TP_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 6),
        ('AlternateSrEnable', ctypes.c_uint32, 1),
        ('ScramblingDisable', ctypes.c_uint32, 1),
        ('DpLinkTrainingEnable', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 7),
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
    Reserved11 = 0  # bit 11 to 18
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
    PAYLOAD_MAPPING_VC0_D = 0x3  # Transcoder D mapped to this VC


class ENUM_PAYLOAD_MAPPING_VC1(Enum):
    PAYLOAD_MAPPING_VC1_A = 0x0  # Transcoder A mapped to this VC
    PAYLOAD_MAPPING_VC1_B = 0x1  # Transcoder B mapped to this VC
    PAYLOAD_MAPPING_VC1_C = 0x2  # Transcoder C mapped to this VC
    PAYLOAD_MAPPING_VC1_D = 0x3  # Transcoder D mapped to this VC


class ENUM_PAYLOAD_MAPPING_VC2(Enum):
    PAYLOAD_MAPPING_VC2_A = 0x0  # Transcoder A mapped to this VC
    PAYLOAD_MAPPING_VC2_B = 0x1  # Transcoder B mapped to this VC
    PAYLOAD_MAPPING_VC2_C = 0x2  # Transcoder C mapped to this VC
    PAYLOAD_MAPPING_VC2_D = 0x3  # Transcoder D mapped to this VC


class ENUM_PAYLOAD_MAPPING_VC3(Enum):
    PAYLOAD_MAPPING_VC3_A = 0x0  # Transcoder A mapped to this VC
    PAYLOAD_MAPPING_VC3_B = 0x1  # Transcoder B mapped to this VC
    PAYLOAD_MAPPING_VC3_C = 0x2  # Transcoder C mapped to this VC
    PAYLOAD_MAPPING_VC3_D = 0x3  # Transcoder D mapped to this VC


class ENUM_STREAMS_ENABLED(Enum):
    STREAMS_ENABLED_0 = 0x0
    STREAMS_ENABLED_1 = 0x1
    STREAMS_ENABLED_2 = 0x2
    STREAMS_ENABLED_3 = 0x3
    STREAMS_ENABLED_4 = 0x4


class ENUM_DP_INIT_STATUS(Enum):
    DP_INIT_STATUS_PATTERN1 = 0x0  # Training Pattern 1
    DP_INIT_STATUS_PATTERN2 = 0x1  # Training Pattern 2
    DP_INIT_STATUS_PATTERN3 = 0x2  # Training Pattern 3
    DP_INIT_STATUS_IDLE_SST = 0x4  # Sending SST Idle Pattern
    DP_INIT_STATUS_IDLE_MST = 0x5  # Sending MST Idle Pattern
    DP_INIT_STATUS_ACTIVE_SST = 0x6  # In Active SST Mode
    DP_INIT_STATUS_ACTIVE_MST = 0x7  # In Active MST Mode


class ENUM_DP_STREAM_STATUS(Enum):
    DP_STREAM_STATUS_INIT = 0x0
    DP_STREAM_STATUS_ACTIVE = 0x1


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
    DP_TP_STATUS_A = 0x60544
    DP_TP_STATUS_B = 0x61544
    DP_TP_STATUS_C = 0x62544
    DP_TP_STATUS_D = 0x63544


class _DP_TP_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PayloadMappingVc0', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 2),
        ('PayloadMappingVc1', ctypes.c_uint32, 2),
        ('Reserved6', ctypes.c_uint32, 2),
        ('PayloadMappingVc2', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 2),
        ('PayloadMappingVc3', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 2),
        ('StreamsEnabled', ctypes.c_uint32, 3),
        ('DpInitStatus', ctypes.c_uint32, 3),
        ('DpStreamStatus', ctypes.c_uint32, 1),
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
    PayloadMappingVc3 = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 16
    StreamsEnabled = 0  # bit 16 to 19
    DpInitStatus = 0  # bit 19 to 22
    DpStreamStatus = 0  # bit 22 to 23
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
    DP_COMP_CTL_A = 0x605F0
    DP_COMP_CTL_B = 0x615F0
    DP_COMP_CTL_C = 0x625F0
    DP_COMP_CTL_D = 0x635F0


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
    DP_COMP_PAT_A = 0x605F4
    DP_COMP_PAT_B = 0x615F4
    DP_COMP_PAT_C = 0x625F4
    DP_COMP_PAT_D = 0x635F4


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


class ENUM_IDLE_FRAMES(Enum):
    IDLE_FRAMES_1_IDLE_FRAME = 0x1


class ENUM_TP1_TIME(Enum):
    TP1_TIME_500US = 0x0
    TP1_TIME_100US = 0x1
    TP1_TIME_2_5MS = 0x2
    TP1_TIME_0US = 0x3  # Skip TP1


class ENUM_TP4_TIME(Enum):
    TP4_TIME_500_US = 0x0
    TP4_TIME_100_US = 0x1
    TP4_TIME_2_5_MS = 0x2
    TP4_TIME_0_US = 0x3  # Skip TP4


class ENUM_TP2_TP3_TIME(Enum):
    TP2_TP3_TIME_500US = 0x0
    TP2_TP3_TIME_100US = 0x1
    TP2_TP3_TIME_2_5MS = 0x2
    TP2_TP3_TIME_0US_SKIP_TP2_TP3 = 0x3


class ENUM_CRC_ENABLE(Enum):
    CRC_DISABLE = 0x0  # Disable CRC output in VSC. VSC packet CRC value will be populated by VIDEO_DIP_DATA.
    CRC_ENABLE = 0x1  # Enable CRC output in VSC. VSC packet CRC value will be populated by the calculated CRC v
                             # alue.


class ENUM_TP2_TP3_SELECT(Enum):
    TP2_TP3_SELECT_TP2 = 0x0  # Use TP1 followed by TP2
    TP2_TP3_SELECT_TP3 = 0x1  # Use TP1 followed by TP3


class ENUM_SKIP_AUX_ON_EXIT(Enum):
    SKIP_AUX_ON_EXIT_DO_NOT_SKIP = 0x0
    SKIP_AUX_ON_EXIT_SKIP = 0x1


class ENUM_TPS4_CONTROL(Enum):
    TPS4_CONTROL_COMPLETE = 0x0  # Completes TPS4 pattern after TP4 counter expires.
    TPS4_CONTROL_TERMINATE = 0x1  # Terminates TPS4 pattern after TP4 counter expires.


class ENUM_MAX_SLEEP_TIME(Enum):
    MAX_SLEEP_TIME_1_8_SECOND = 0x1


class ENUM_LINK_CTRL(Enum):
    LINK_CTRL_DISABLE = 0x0  # Link is disabled when in SRD (sleeping)


class ENUM_ADAPTIVE_SYNC_FRAME_UPDATE(Enum):
    ADAPTIVE_SYNC_FRAME_UPDATE_DISABLE = 0x0
    ADAPTIVE_SYNC_FRAME_UPDATE_ENABLE = 0x1


class ENUM_CONTEXT_RESTORE_TO_PSR_ACTIVE(Enum):
    CONTEXT_RESTORE_TO_PSR_ACTIVE_DISABLE = 0x0
    CONTEXT_RESTORE_TO_PSR_ACTIVE_ENABLE = 0x1


class ENUM_SINGLE_FRAME_UPDATE_ENABLE(Enum):
    SINGLE_FRAME_UPDATE_DISABLE = 0x0
    SINGLE_FRAME_UPDATE_ENABLE = 0x1


class ENUM_SRD_ENABLE(Enum):
    SRD_DISABLE = 0x0
    SRD_ENABLE = 0x1


class OFFSET_SRD_CTL:
    SRD_CTL_A = 0x60800
    SRD_CTL_B = 0x61800
    SRD_CTL_C = 0x62800
    SRD_CTL_D = 0x63800


class _SRD_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IdleFrames', ctypes.c_uint32, 4),
        ('Tp1Time', ctypes.c_uint32, 2),
        ('Tp4Time', ctypes.c_uint32, 2),
        ('Tp2Tp3Time', ctypes.c_uint32, 2),
        ('CrcEnable', ctypes.c_uint32, 1),
        ('Tp2Tp3Select', ctypes.c_uint32, 1),
        ('SkipAuxOnExit', ctypes.c_uint32, 1),
        ('Tps4Control', ctypes.c_uint32, 1),
        ('DscCrcLastByte', ctypes.c_uint32, 3),
        ('Reserved17', ctypes.c_uint32, 3),
        ('MaxSleepTime', ctypes.c_uint32, 5),
        ('Reserved25', ctypes.c_uint32, 2),
        ('LinkCtrl', ctypes.c_uint32, 1),
        ('AdaptiveSyncFrameUpdate', ctypes.c_uint32, 1),
        ('ContextRestoreToPsrActive', ctypes.c_uint32, 1),
        ('SingleFrameUpdateEnable', ctypes.c_uint32, 1),
        ('SrdEnable', ctypes.c_uint32, 1),
    ]


class REG_SRD_CTL(ctypes.Union):
    value = 0
    offset = 0

    IdleFrames = 0  # bit 0 to 4
    Tp1Time = 0  # bit 4 to 6
    Tp4Time = 0  # bit 6 to 8
    Tp2Tp3Time = 0  # bit 8 to 10
    CrcEnable = 0  # bit 10 to 11
    Tp2Tp3Select = 0  # bit 11 to 12
    SkipAuxOnExit = 0  # bit 12 to 13
    Tps4Control = 0  # bit 13 to 14
    DscCrcLastByte = 0  # bit 14 to 17
    Reserved17 = 0  # bit 17 to 20
    MaxSleepTime = 0  # bit 20 to 25
    Reserved25 = 0  # bit 25 to 27
    LinkCtrl = 0  # bit 27 to 28
    AdaptiveSyncFrameUpdate = 0  # bit 28 to 29
    ContextRestoreToPsrActive = 0  # bit 29 to 30
    SingleFrameUpdateEnable = 0  # bit 30 to 31
    SrdEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRD_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRD_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SENDING_TP1(Enum):
    SENDING_TP1_NOT_SENDING = 0x0  # Not sending TP1
    SENDING_TP1_SENDING = 0x1  # Sending TP1


class ENUM_SENDING_TP4(Enum):
    SENDING_TP4_NOT_SENDING = 0x0
    SENDING_TP4_SENDING = 0x1


class ENUM_SENDING_TP2_TP3(Enum):
    SENDING_TP2_TP3_NOT_SENDING = 0x0  # Not sending TP2 or TP3
    SENDING_TP2_TP3_SENDING = 0x1  # Sending TP2 or TP3


class ENUM_SENDING_IDLE(Enum):
    SENDING_IDLE_NOT_SENDING = 0x0  # Not sending idle
    SENDING_IDLE_SENDING = 0x1  # Sending idle


class ENUM_SENDING_AUX(Enum):
    SENDING_AUX_NOT_SENDING = 0x0  # Not sending AUX handshake
    SENDING_AUX_SENDING = 0x1  # Sending AUX handshake


class ENUM_AUX_ERROR(Enum):
    AUX_ERROR_NO_ERROR = 0x0  # AUX had no error
    AUX_ERROR_ERROR = 0x1  # AUX error (receive error or timeout) occured


class ENUM_LINK_STATUS(Enum):
    LINK_STATUS_FULL_OFF = 0x0  # Link is fully off
    LINK_STATUS_FULL_ON = 0x1  # Link is fully on


class ENUM_SRD_STATE(Enum):
    SRD_STATE_IDLE = 0x0  # Reset state
    SRD_STATE_SRDONACK = 0x1  # Wait for TG/Stream to send on frame of data after SRD conditions are met
    SRD_STATE_SRDENT = 0x2  # SRD entry with Link OFF
    SRD_STATE_BUFOFF = 0x3  # Wait for buffer turn off
    SRD_STATE_BUFON = 0x4  # Wait for buffer turn on
    SRD_STATE_AUXACK = 0x5  # Wait for AUX to acknowledge on SRD exit
    SRD_STATE_SRDOFFACK = 0x6  # Wait for TG/Stream to acknowledge the SRD VDM exit
    SRD_STATE_SRDENT_ON = 0x7  # SRD entry with Link ON


class OFFSET_SRD_STATUS:
    SRD_STATUS_A = 0x60840
    SRD_STATUS_B = 0x61840
    SRD_STATUS_C = 0x62840
    SRD_STATUS_D = 0x63840


class _SRD_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IdleFrameCounter', ctypes.c_uint32, 4),
        ('SendingTp1', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 2),
        ('SendingTp4', ctypes.c_uint32, 1),
        ('SendingTp2Tp3', ctypes.c_uint32, 1),
        ('SendingIdle', ctypes.c_uint32, 1),
        ('Reserved10', ctypes.c_uint32, 2),
        ('SendingAux', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 2),
        ('AuxError', ctypes.c_uint32, 1),
        ('SrdEntryCount', ctypes.c_uint32, 4),
        ('MaxSleepTimeCounter', ctypes.c_uint32, 5),
        ('Reserved25', ctypes.c_uint32, 1),
        ('LinkStatus', ctypes.c_uint32, 2),
        ('Reserved28', ctypes.c_uint32, 1),
        ('SrdState', ctypes.c_uint32, 3),
    ]


class REG_SRD_STATUS(ctypes.Union):
    value = 0
    offset = 0

    IdleFrameCounter = 0  # bit 0 to 4
    SendingTp1 = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 7
    SendingTp4 = 0  # bit 7 to 8
    SendingTp2Tp3 = 0  # bit 8 to 9
    SendingIdle = 0  # bit 9 to 10
    Reserved10 = 0  # bit 10 to 12
    SendingAux = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 15
    AuxError = 0  # bit 15 to 16
    SrdEntryCount = 0  # bit 16 to 20
    MaxSleepTimeCounter = 0  # bit 20 to 25
    Reserved25 = 0  # bit 25 to 26
    LinkStatus = 0  # bit 26 to 28
    Reserved28 = 0  # bit 28 to 29
    SrdState = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRD_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRD_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PSR_REDUCE_COUNT(Enum):
    PSR_REDUCE_COUNT_NORMAL = 0x0  # Use normal counters
    PSR_REDUCE_COUNT_REDUCE = 0x1  # Reduce count for testing


class ENUM_SRD_ENTRY_COMPLETION(Enum):
    SRD_ENTRY_COMPLETION_NOT_COMPLETE = 0x0
    SRD_ENTRY_COMPLETION_COMPLETE = 0x1


class ENUM_PSR2_CRC_INVALIDATE(Enum):
    PSR2_CRC_INVALIDATE_NOT_INVALIDATE = 0x0
    PSR2_CRC_INVALIDATE_INVALIDATE = 0x1


class ENUM_IDLE_COUNT(Enum):
    IDLE_COUNT_SEND = 0x0
    IDLE_COUNT_SKIP = 0x1


class ENUM_CSR_DELAY_ENABLE(Enum):
    CSR_DELAY_DISABLE = 0x0
    CSR_DELAY_ENABLE = 0x1


class OFFSET_PSR_DEBUG:
    PSR_DEBUG_A = 0x60A60
    PSR_DEBUG_B = 0x61A60
    PSR_DEBUG_C = 0x62A60
    PSR_DEBUG_D = 0x63A60


class _PSR_DEBUG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PsrReduceCount', ctypes.c_uint32, 1),
        ('SrdEntryCompletion', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 4),
        ('Psr2CrcInvalidate', ctypes.c_uint32, 1),
        ('IdleCount', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 9),
        ('CsrDelayTime', ctypes.c_uint32, 10),
        ('CsrDelayEnable', ctypes.c_uint32, 1),
        ('ResetIdleFrameCount', ctypes.c_uint32, 1),
        ('EntryHint', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_PSR_DEBUG(ctypes.Union):
    value = 0
    offset = 0

    PsrReduceCount = 0  # bit 0 to 1
    SrdEntryCompletion = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 6
    Psr2CrcInvalidate = 0  # bit 6 to 7
    IdleCount = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 17
    CsrDelayTime = 0  # bit 17 to 27
    CsrDelayEnable = 0  # bit 27 to 28
    ResetIdleFrameCount = 0  # bit 28 to 29
    EntryHint = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR_DEBUG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR_DEBUG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SRD_DISABLE(Enum):
    SRD_DISABLE_CONDITION_NOT_DETECTED = 0x0
    SRD_DISABLE_CONDITION_DETECTED = 0x1


class ENUM_VBI_ENABLE(Enum):
    VBI_ENABLE_CONDITION_NOT_DETECTED = 0x0
    VBI_ENABLE_CONDITION_DETECTED = 0x1


class ENUM_KVMR_SESSION_ENABLE(Enum):
    KVMR_SESSION_ENABLE_CONDITION_NOT_DETECTED = 0x0
    KVMR_SESSION_ENABLE_CONDITION_DETECTED = 0x1


class ENUM_HDCP_ENABLE(Enum):
    HDCP_ENABLE_CONDITION_NOT_DETECTED = 0x0
    HDCP_ENABLE_CONDITION_DETECTED = 0x1


class ENUM_WATCH_DOG_TIMER_EXPIRE(Enum):
    WATCH_DOG_TIMER_EXPIRE_CONDITION_NOT_DETECTED = 0x0
    WATCH_DOG_TIMER_EXPIRE_CONDITION_DETECTED = 0x1


class ENUM_FRONT_BUFFER_MODIFY(Enum):
    FRONT_BUFFER_MODIFY_CONDITION_NOT_DETECTED = 0x0
    FRONT_BUFFER_MODIFY_CONDITION_DETECTED = 0x1


class ENUM_MEMORY_UP(Enum):
    MEMORY_UP_CONDITION_NOT_DETECTED = 0x0
    MEMORY_UP_CONDITION_DETECTED = 0x1


class ENUM_PCH_INTERRUPT(Enum):
    PCH_INTERRUPT_CONDITION_NOT_DETECTED = 0x0
    PCH_INTERRUPT_CONDITION_DETECTED = 0x1


class ENUM_GRAPHICS_RESET(Enum):
    GRAPHICS_RESET_CONDITION_NOT_DETECTED = 0x0
    GRAPHICS_RESET_CONDITION_DETECTED = 0x1


class ENUM_SELECTIVE_UPDATE_CRC_FIFO_UNDERRUN(Enum):
    SELECTIVE_UPDATE_CRC_FIFO_UNDERRUN_CONDITION_NOT_DETECTED = 0x0
    SELECTIVE_UPDATE_CRC_FIFO_UNDERRUN_CONDITION_DETECTED = 0x1


class ENUM_SELECTIVE_UPDATE_DIRTY_FIFO_UNDERRUN(Enum):
    SELECTIVE_UPDATE_DIRTY_FIFO_UNDERRUN_CONDITION_NOT_DETECTED = 0x0
    SELECTIVE_UPDATE_DIRTY_FIFO_UNDERRUN_CONDITION_DETECTED = 0x1


class ENUM_PSR2_DISABLE(Enum):
    PSR2_DISABLE_CONDITION_NOT_DETECTED = 0x0
    PSR2_DISABLE_CONDITION_DETECTED = 0x1


class ENUM_PSR2_WATCH_DOG_TIMER_EXPIRE(Enum):
    PSR2_WATCH_DOG_TIMER_EXPIRE_CONDITION_NOT_DETECTED = 0x0
    PSR2_WATCH_DOG_TIMER_EXPIRE_CONDITION_DETECTED = 0x1


class OFFSET_PSR_EVENT:
    PSR_EVENT_A = 0x60848
    PSR_EVENT_B = 0x61848
    PSR_EVENT_C = 0x62848
    PSR_EVENT_D = 0x63848


class _PSR_EVENT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SrdDisable', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 1),
        ('VbiEnable', ctypes.c_uint32, 1),
        ('KvmrSessionEnable', ctypes.c_uint32, 1),
        ('HdcpEnable', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 1),
        ('PipeRegistersUpdate', ctypes.c_uint32, 1),
        ('Reserved7', ctypes.c_uint32, 1),
        ('WatchDogTimerExpire', ctypes.c_uint32, 1),
        ('FrontBufferModify', ctypes.c_uint32, 1),
        ('MemoryUp', ctypes.c_uint32, 1),
        ('PchInterrupt', ctypes.c_uint32, 1),
        ('GraphicsReset', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 1),
        ('SelectiveUpdateCrcFifoUnderrun', ctypes.c_uint32, 1),
        ('SelectiveUpdateDirtyFifoUnderrun', ctypes.c_uint32, 1),
        ('Psr2Disable', ctypes.c_uint32, 1),
        ('Psr2WatchDogTimerExpire', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 14),
    ]


class REG_PSR_EVENT(ctypes.Union):
    value = 0
    offset = 0

    SrdDisable = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 2
    VbiEnable = 0  # bit 2 to 3
    KvmrSessionEnable = 0  # bit 3 to 4
    HdcpEnable = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 6
    PipeRegistersUpdate = 0  # bit 6 to 7
    Reserved7 = 0  # bit 7 to 8
    WatchDogTimerExpire = 0  # bit 8 to 9
    FrontBufferModify = 0  # bit 9 to 10
    MemoryUp = 0  # bit 10 to 11
    PchInterrupt = 0  # bit 11 to 12
    GraphicsReset = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 14
    SelectiveUpdateCrcFifoUnderrun = 0  # bit 14 to 15
    SelectiveUpdateDirtyFifoUnderrun = 0  # bit 15 to 16
    Psr2Disable = 0  # bit 16 to 17
    Psr2WatchDogTimerExpire = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR_EVENT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR_EVENT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GLOBAL_MASK(Enum):
    GLOBAL_MASK_NOT_MASKED = 0x0
    GLOBAL_MASK_MASKED = 0x1


class ENUM_EXIT_ON_PIXEL_UNDERRUN_(Enum):
    EXIT_ON_PIXEL_UNDERRUN_NOT_MASKED = 0x0
    EXIT_ON_PIXEL_UNDERRUN_MASKED = 0x1


class ENUM_MASK_FBC_MODIFY(Enum):
    MASK_FBC_MODIFY_NOT_MASKED = 0x0
    MASK_FBC_MODIFY_MASKED = 0x1


class ENUM_MASK_HOTPLUG(Enum):
    MASK_HOTPLUG_NOT_MASKED = 0x0
    MASK_HOTPLUG_MASKED = 0x1


class ENUM_MASK_MEMUP(Enum):
    MASK_MEMUP_NOT_MASKED = 0x0
    MASK_MEMUP_MASKED = 0x1  # Masked - will not be considered in PSR idleness tracking (default)


class ENUM_MASK_LPSP(Enum):
    MASK_LPSP_NOT_MASKED = 0x0
    MASK_LPSP_MASKED = 0x1


class ENUM_MASK_MAX_SLEEP(Enum):
    MASK_MAX_SLEEP_NOT_MASKED = 0x0
    MASK_MAX_SLEEP_MASKED = 0x1


class ENUM_IDLE_FRAME_OVERRIDE(Enum):
    IDLE_FRAME_OVERRIDE_FORCE_IDLE_FRAME = 0x2  # Force Idle Frames to force PSR entry or PSR2 Deep Sleep
    IDLE_FRAME_OVERRIDE_FORCE_NONIDLE_FRAME = 0x3  # Force Non-Idle Frames to force PSR exit or exit from PSR2 Deep Sle
                                                   # ep


class OFFSET_PSR_MASK:
    PSR_MASK_A = 0x60860
    PSR_MASK_B = 0x61860
    PSR_MASK_C = 0x62860
    PSR_MASK_D = 0x63860


class _PSR_MASK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GlobalMask', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 14),
        ('ExitOnPixelUnderrun', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 8),
        ('MaskFbcModify', ctypes.c_uint32, 1),
        ('MaskHotplug', ctypes.c_uint32, 1),
        ('MaskMemup', ctypes.c_uint32, 1),
        ('MaskLpsp', ctypes.c_uint32, 1),
        ('MaskMaxSleep', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 1),
        ('IdleFrameOverride', ctypes.c_uint32, 2),
    ]


class REG_PSR_MASK(ctypes.Union):
    value = 0
    offset = 0

    GlobalMask = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 15
    ExitOnPixelUnderrun = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 24
    MaskFbcModify = 0  # bit 24 to 25
    MaskHotplug = 0  # bit 25 to 26
    MaskMemup = 0  # bit 26 to 27
    MaskLpsp = 0  # bit 27 to 28
    MaskMaxSleep = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 30
    IdleFrameOverride = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR_MASK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR_MASK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


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


class ENUM_YCOORDINATE_ENABLE(Enum):
    YCOORDINATE_ENABLE_DO_NOT_INCLUDE_COUNT = 0x0
    YCOORDINATE_ENABLE_INCLUDE_COUNT = 0x1


class ENUM_YCOORDINATE_VALID(Enum):
    YCOORDINATE_VALID_INCLUDE_YCOORDINATE_VALID_EDP1_4A = 0x0
    YCOORDINATE_VALID_DO_NOT_INCLUDE_YCOORDINATE_VALID_EDP_1_4 = 0x1


class ENUM_AUX_FRAME_SYNC_ENABLE(Enum):
    AUX_FRAME_SYNC_ENABLE = 0x1
    AUX_FRAME_SYNC_DISABLE = 0x0


class ENUM_BLOCK_COUNT_NUMBER(Enum):
    BLOCK_COUNT_NUMBER_2_BLOCKS = 0x0
    BLOCK_COUNT_NUMBER_3_BLOCKS = 0x1


class ENUM_CONTEXT_RESTORE_TO_PSR2_DEEP_SLEEP_STATE(Enum):
    CONTEXT_RESTORE_TO_PSR2_DEEP_SLEEP_STATE_DISABLE = 0x0
    CONTEXT_RESTORE_TO_PSR2_DEEP_SLEEP_STATE_ENABLE = 0x1


class ENUM_SELECTIVE_UPDATE_TRACKING_ENABLE(Enum):
    SELECTIVE_UPDATE_TRACKING_DISABLE = 0x0
    SELECTIVE_UPDATE_TRACKING_ENABLE = 0x1


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
        ('YCoordinateEnable', ctypes.c_uint32, 1),
        ('YCoordinateValid', ctypes.c_uint32, 1),
        ('AuxFrameSyncEnable', ctypes.c_uint32, 1),
        ('BlockCountNumber', ctypes.c_uint32, 1),
        ('ContextRestoreToPsr2DeepSleepState', ctypes.c_uint32, 1),
        ('SelectiveUpdateTrackingEnable', ctypes.c_uint32, 1),
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
    YCoordinateEnable = 0  # bit 25 to 26
    YCoordinateValid = 0  # bit 26 to 27
    AuxFrameSyncEnable = 0  # bit 27 to 28
    BlockCountNumber = 0  # bit 28 to 29
    ContextRestoreToPsr2DeepSleepState = 0  # bit 29 to 30
    SelectiveUpdateTrackingEnable = 0  # bit 30 to 31
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


class ENUM_PSR2_BLOCK_FIFO_UNDERRUN(Enum):
    PSR2_BLOCK_FIFO_UNDERRUN_NO_UNDERRUN = 0x0  # No Underurn
    PSR2_BLOCK_FIFO_UNDERRUN_UNDERRUN = 0x1  # Block FIFO underrun.


class ENUM_PSR2_SU_FIFO_UNDERRUN(Enum):
    PSR2_SU_FIFO_UNDERRUN_NO_UNDERRUN = 0x0  # No Underurn
    PSR2_SU_FIFO_UNDERRUN_UNDERRUN = 0x1  # PSR2 SU FIFO underrun.


class ENUM_SENDING_TP2(Enum):
    SENDING_TP2_NOT_SENDING = 0x0  # Not sending TP2
    SENDING_TP2_SENDING = 0x1  # Sending TP2


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
        ('Psr2BlockFifoUnderrun', ctypes.c_uint32, 1),
        ('Psr2SuFifoUnderrun', ctypes.c_uint32, 1),
        ('SendingTp2', ctypes.c_uint32, 1),
        ('Psr2IdleFrameIndication', ctypes.c_uint32, 1),
        ('Reserved10', ctypes.c_uint32, 2),
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
    Psr2BlockFifoUnderrun = 0  # bit 6 to 7
    Psr2SuFifoUnderrun = 0  # bit 7 to 8
    SendingTp2 = 0  # bit 8 to 9
    Psr2IdleFrameIndication = 0  # bit 9 to 10
    Reserved10 = 0  # bit 10 to 12
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


class OFFSET_SRD_PERF_CNT:
    SRD_PERF_CNT_A = 0x60844
    SRD_PERF_CNT_B = 0x61844
    SRD_PERF_CNT_C = 0x62844
    SRD_PERF_CNT_D = 0x63844


class _SRD_PERF_CNT(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SrdPerfCnt', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_SRD_PERF_CNT(ctypes.Union):
    value = 0
    offset = 0

    SrdPerfCnt = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SRD_PERF_CNT),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SRD_PERF_CNT, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MASK_PSR_PREWARN(Enum):
    MASK_PSR_PREWARN_NOT_MASKED = 0x0
    MASK_PSR_PREWARN_MASKED = 0x1


class ENUM_MASK_PSR_EXIT(Enum):
    MASK_PSR_EXIT_NOT_MASKED = 0x0
    MASK_PSR_EXIT_MASKED = 0x1


class ENUM_MASK_PSR_AUX_ERROR(Enum):
    MASK_PSR_AUX_ERROR_NOT_MASKED = 0x0
    MASK_PSR_AUX_ERROR_MASKED = 0x1


class ENUM_MASK_PUSH_DONE(Enum):
    MASK_PUSH_DONE_NOT_MASKED = 0x0
    MASK_PUSH_DONE_MASKED = 0x1


class OFFSET_PSR_IMR:
    PSR_IMR_A = 0x60814
    PSR_IMR_B = 0x61814
    PSR_IMR_C = 0x62814
    PSR_IMR_D = 0x63814


class _PSR_IMR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MaskPsrPrewarn', ctypes.c_uint32, 1),
        ('MaskPsrExit', ctypes.c_uint32, 1),
        ('MaskPsrAuxError', ctypes.c_uint32, 1),
        ('MaskPushDone', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 28),
    ]


class REG_PSR_IMR(ctypes.Union):
    value = 0
    offset = 0

    MaskPsrPrewarn = 0  # bit 0 to 1
    MaskPsrExit = 0  # bit 1 to 2
    MaskPsrAuxError = 0  # bit 2 to 3
    MaskPushDone = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR_IMR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR_IMR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PSR_PREWARN(Enum):
    PSR_PREWARN_NOT_DETECTED = 0x0
    PSR_PREWARN_CONDITION_DETECTED = 0x1


class ENUM_PSR_EXIT(Enum):
    PSR_EXIT_CONDITION_NOT_DETECTED = 0x0
    PSR_EXIT_CONDITION_DETECTED = 0x1


class ENUM_PSR_AUX_ERROR(Enum):
    PSR_AUX_ERROR_CONDITION_NOT_DETECTED = 0x0
    PSR_AUX_ERROR_CONDITION_DETECTED = 0x1


class ENUM_PUSH_DONE(Enum):
    PUSH_DONE_CONDITION_NOT_DETECTED = 0x0
    PUSH_DONE_CONDITION_DETECTED = 0x1


class OFFSET_PSR_IIR:
    PSR_IIR_A = 0x60818
    PSR_IIR_B = 0x61818
    PSR_IIR_C = 0x62818
    PSR_IIR_D = 0x63818


class _PSR_IIR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PsrPrewarn', ctypes.c_uint32, 1),
        ('PsrExit', ctypes.c_uint32, 1),
        ('PsrAuxError', ctypes.c_uint32, 1),
        ('PushDone', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 28),
    ]


class REG_PSR_IIR(ctypes.Union):
    value = 0
    offset = 0

    PsrPrewarn = 0  # bit 0 to 1
    PsrExit = 0  # bit 1 to 2
    PsrAuxError = 0  # bit 2 to 3
    PushDone = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PSR_IIR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PSR_IIR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GTC_RESET(Enum):
    GTC_RESET_RUN_NORMALLY = 0x0
    GTC_RESET_RESET_TO_ZERO = 0x1


class ENUM_GTC_FUNCTION_ENABLE(Enum):
    GTC_FUNCTION_DISABLE = 0x0
    GTC_FUNCTION_ENABLE = 0x1


class OFFSET_GTC_CTL:
    GTC_CTL = 0x67000


class _GTC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GtcReset', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 12),
        ('Spare2813', ctypes.c_uint32, 16),
        ('Reserved29', ctypes.c_uint32, 2),
        ('GtcFunctionEnable', ctypes.c_uint32, 1),
    ]


class REG_GTC_CTL(ctypes.Union):
    value = 0
    offset = 0

    GtcReset = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 13
    Spare2813 = 0  # bit 13 to 29
    Reserved29 = 0  # bit 29 to 31
    GtcFunctionEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GTC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GTC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_GTC_DDA_M:
    GTC_DDA_M = 0x67010


class _GTC_DDA_M(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GtcDdaM', ctypes.c_uint32, 24),
        ('Spare3124', ctypes.c_uint32, 8),
    ]


class REG_GTC_DDA_M(ctypes.Union):
    value = 0
    offset = 0

    GtcDdaM = 0  # bit 0 to 24
    Spare3124 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GTC_DDA_M),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GTC_DDA_M, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_GTC_DDA_N:
    GTC_DDA_N = 0x67014


class _GTC_DDA_N(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GtcDdaN', ctypes.c_uint32, 24),
        ('GtcAccumInc', ctypes.c_uint32, 8),
    ]


class REG_GTC_DDA_N(ctypes.Union):
    value = 0
    offset = 0

    GtcDdaN = 0  # bit 0 to 24
    GtcAccumInc = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GTC_DDA_N),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GTC_DDA_N, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PORT_RX_LOCK_DONE(Enum):
    PORT_RX_LOCK_DONE_NOT_LOCKED = 0x0
    PORT_RX_LOCK_DONE_LOCKED = 0x1


class ENUM_MAINTENANCE_PHASE_ENABLE(Enum):
    MAINTENANCE_PHASE_ENABLE_LOCK = 0x0  # Lock acquisition phase. The controller writes or reads GTC every 1ms.
    MAINTENANCE_PHASE_ENABLE_MAINTAIN = 0x1  # Lock maintenance phase. The controller writes or reads GTC every 10ms.


class ENUM_PORT_GLOBAL_TIME_CODE_ENABLE(Enum):
    PORT_GLOBAL_TIME_CODE_DISABLE = 0x0
    PORT_GLOBAL_TIME_CODE_ENABLE = 0x1


class OFFSET_GTC_PORT_CTL:
    GTC_PORT_CTL_A = 0x64070
    GTC_PORT_CTL_B = 0x64170
    GTC_PORT_CTL_C = 0x64270
    GTC_PORT_CTL_USBC1 = 0x64370
    GTC_PORT_CTL_USBC2 = 0x64470
    GTC_PORT_CTL_USBC3 = 0x64570
    GTC_PORT_CTL_USBC4 = 0x64670
    GTC_PORT_CTL_USBC5 = 0x64770
    GTC_PORT_CTL_USBC6 = 0x64870


class _GTC_PORT_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PortRxLockDone', ctypes.c_uint32, 1),
        ('Spare231', ctypes.c_uint32, 23),
        ('MaintenancePhaseEnable', ctypes.c_uint32, 1),
        ('Spare3025', ctypes.c_uint32, 6),
        ('PortGlobalTimeCodeEnable', ctypes.c_uint32, 1),
    ]


class REG_GTC_PORT_CTL(ctypes.Union):
    value = 0
    offset = 0

    PortRxLockDone = 0  # bit 0 to 1
    Spare231 = 0  # bit 1 to 24
    MaintenancePhaseEnable = 0  # bit 24 to 25
    Spare3025 = 0  # bit 25 to 31
    PortGlobalTimeCodeEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GTC_PORT_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GTC_PORT_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MIN_LOCK_DURATION(Enum):
    MIN_LOCK_DURATION_10MS = 0xA


class ENUM_GTC_UPDATE_MESSAGE_DELAY(Enum):
    GTC_UPDATE_MESSAGE_DELAY_52_NANOSECONDS = 0x34


class OFFSET_GTC_PORT_MISC:
    GTC_PORT_MISC_A = 0x64094
    GTC_PORT_MISC_B = 0x64194
    GTC_PORT_MISC_C = 0x64294
    GTC_PORT_MISC_USBC1 = 0x64394
    GTC_PORT_MISC_USBC2 = 0x64494
    GTC_PORT_MISC_USBC3 = 0x64594
    GTC_PORT_MISC_USBC4 = 0x64694
    GTC_PORT_MISC_USBC5 = 0x64794
    GTC_PORT_MISC_USBC6 = 0x64894


class _GTC_PORT_MISC(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 8),
        ('MinLockDuration', ctypes.c_uint32, 4),
        ('GtcUpdateMessageDelay', ctypes.c_uint32, 10),
        ('Reserved22', ctypes.c_uint32, 10),
    ]


class REG_GTC_PORT_MISC(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 8
    MinLockDuration = 0  # bit 8 to 12
    GtcUpdateMessageDelay = 0  # bit 12 to 22
    Reserved22 = 0  # bit 22 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GTC_PORT_MISC),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GTC_PORT_MISC, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_FS_MSA_MISC1_DRIVE_INVERT(Enum):
    FS_MSA_MISC1_DRIVE_INVERT_NO_INVERT = 0x0
    FS_MSA_MISC1_DRIVE_INVERT_INVERT = 0x1


class ENUM_FS_MSA_MISC1_DRIVE_EN(Enum):
    FS_MSA_MISC1_DRIVE_EN_DISABLE = 0x0  # Disable hardware driving MSA MISC1 bits 2:1. Allow software to manually prog
                                         # ram MSA MISC1 bits 2:1 through TRANS_MSA_MISC.
    FS_MSA_MISC1_DRIVE_EN_ENABLE = 0x1  # Enable hardware to drive MSA MISC1 bits 2:1 for stereo 3D.


class ENUM_S3D_CURRENT_FIELD(Enum):
    S3D_CURRENT_FIELD_RIGHT_EYE = 0x0
    S3D_CURRENT_FIELD_LEFT_EYE = 0x1


class ENUM_FS_FIELD_CTL(Enum):
    FS_FIELD_CTL_RIGHT_EYE = 0x0
    FS_FIELD_CTL_LEFT_EYE = 0x1


class ENUM_S3D_MODE(Enum):
    S3D_MODE_FS_HW_AUTO = 0x0  # Hardware controlled auto-toggle between left and right eye on each vertical blank.
    S3D_MODE_FS_SW_MANUAL = 0x1  # Software controlled selection between left and right eye
    S3D_MODE_STACKED = 0x2  # Stacked frame mode with both left and right eye images combined in a single tall frame


class ENUM_TRANSCODER_S3D_ENABLE(Enum):
    TRANSCODER_S3D_DISABLE = 0x0
    TRANSCODER_S3D_ENABLE = 0x1


class OFFSET_TRANS_STEREO3D_CTL:
    TRANS_STEREO3D_CTL_A = 0x70020
    TRANS_STEREO3D_CTL_B = 0x71020
    TRANS_STEREO3D_CTL_C = 0x72020
    TRANS_STEREO3D_CTL_D = 0x73020
    TRANS_STEREO3D_CTL_DSI0 = 0x7B020
    TRANS_STEREO3D_CTL_DSI1 = 0x7B820


class _TRANS_STEREO3D_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 22),
        ('FsMsaMisc1DriveInvert', ctypes.c_uint32, 1),
        ('FsMsaMisc1DriveEn', ctypes.c_uint32, 1),
        ('S3DCurrentField', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 1),
        ('FsFieldCtl', ctypes.c_uint32, 1),
        ('S3DMode', ctypes.c_uint32, 2),
        ('Reserved29', ctypes.c_uint32, 2),
        ('TranscoderS3DEnable', ctypes.c_uint32, 1),
    ]


class REG_TRANS_STEREO3D_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 22
    FsMsaMisc1DriveInvert = 0  # bit 22 to 23
    FsMsaMisc1DriveEn = 0  # bit 23 to 24
    S3DCurrentField = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 26
    FsFieldCtl = 0  # bit 26 to 27
    S3DMode = 0  # bit 27 to 29
    Reserved29 = 0  # bit 29 to 31
    TranscoderS3DEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_STEREO3D_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_STEREO3D_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_BLOCK_MODE(Enum):
    BLOCK_MODE_HEADER_VALUES_FROM_HEADER_REGISTER = 0x0
    BLOCK_MODE_HEADER_VALUES_FROM_SW_DSB_WRITTEN_BUFFER = 0x1


class ENUM_SDP_ACTIVE_ERROR(Enum):
    SDP_ACTIVE_ERROR_ALL_SDPS_TRANSMITTED_IN_VBLANK = 0x0
    SDP_ACTIVE_ERROR_ALL_SDPS_NOT_TRANSMITTED_IN_VBLANK_ = 0x1


class ENUM_CHAIN_DONE(Enum):
    CHAIN_DONE_HW_SENDING_PREVIOUS_CHAIN = 0x0
    CHAIN_DONE_HW_COMPLETED_SENDING_PREVIOUS_CHAIN = 0x1


class OFFSET_VSC_EXT_SDP_CONF:
    VSC_EXT_SDP_CONF_A = 0x60288
    VSC_EXT_SDP_CONF_B = 0x61288
    VSC_EXT_SDP_CONF_C = 0x62288
    VSC_EXT_SDP_CONF_D = 0x63288


class _VSC_EXT_SDP_CONF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PacketsPerChain', ctypes.c_uint32, 10),
        ('HblankEarlyIndication', ctypes.c_uint32, 12),
        ('BlockMode', ctypes.c_uint32, 1),
        ('SdpActiveError', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 6),
        ('ChainDone', ctypes.c_uint32, 1),
    ]


class REG_VSC_EXT_SDP_CONF(ctypes.Union):
    value = 0
    offset = 0

    PacketsPerChain = 0  # bit 0 to 10
    HblankEarlyIndication = 0  # bit 10 to 22
    BlockMode = 0  # bit 22 to 23
    SdpActiveError = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 31
    ChainDone = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VSC_EXT_SDP_CONF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VSC_EXT_SDP_CONF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SDP_TYPE(Enum):
    SDP_TYPE_VESA = 0x20
    SDP_TYPE_CEA = 0x21


class ENUM_VARIABLE_PACKET_SEQUENCE_NUMBER(Enum):
    VARIABLE_PACKET_SEQUENCE_NUMBER_PACKET_SEQUENCE_FIELD_IS_FIXED = 0x0
    VARIABLE_PACKET_SEQUENCE_NUMBER_PACKET_SEQUENCE_FIELD_IS_INCREMENTED_WITH_CHAINED_PACKETS = 0x1


class ENUM_MIDDLE_OF_CHAINING(Enum):
    MIDDLE_OF_CHAINING_NO_CHAINED_PACKETS_TO_FOLLOW = 0x0
    MIDDLE_OF_CHAINING_CHAINED_PACKET_S_TO_FOLLOW_ = 0x1


class OFFSET_VSC_EXT_SDP_HEADER:
    VSC_EXT_SDP_HEADER_A = 0x6028C
    VSC_EXT_SDP_HEADER_B = 0x6128C
    VSC_EXT_SDP_HEADER_C = 0x6228C
    VSC_EXT_SDP_HEADER_D = 0x6328C


class _VSC_EXT_SDP_HEADER(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SdpId', ctypes.c_uint32, 8),
        ('SdpType', ctypes.c_uint32, 8),
        ('VscExtVesaSdpFrameworkVer0', ctypes.c_uint32, 2),
        ('VscExtVesaSdpFrameworkVer1', ctypes.c_uint32, 4),
        ('VariablePacketSequenceNumber', ctypes.c_uint32, 1),
        ('MiddleOfChaining', ctypes.c_uint32, 1),
        ('PacketSequence', ctypes.c_uint32, 5),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_VSC_EXT_SDP_HEADER(ctypes.Union):
    value = 0
    offset = 0

    SdpId = 0  # bit 0 to 8
    SdpType = 0  # bit 8 to 16
    VscExtVesaSdpFrameworkVer0 = 0  # bit 16 to 18
    VscExtVesaSdpFrameworkVer1 = 0  # bit 18 to 22
    VariablePacketSequenceNumber = 0  # bit 22 to 23
    MiddleOfChaining = 0  # bit 23 to 24
    PacketSequence = 0  # bit 24 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VSC_EXT_SDP_HEADER),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VSC_EXT_SDP_HEADER, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_VSC_EXT_SDP_DATA:
    VSC_EXT_SDP_DATA_0_A = 0x60298
    VSC_EXT_SDP_DATA_1_A = 0x6029C
    VSC_EXT_SDP_DATA_0_B = 0x61298
    VSC_EXT_SDP_DATA_1_B = 0x6129C
    VSC_EXT_SDP_DATA_0_C = 0x62298
    VSC_EXT_SDP_DATA_1_C = 0x6229C
    VSC_EXT_SDP_DATA_0_D = 0x63298
    VSC_EXT_SDP_DATA_1_D = 0x6329C


class _VSC_EXT_SDP_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Data', ctypes.c_uint32, 32),
    ]


class REG_VSC_EXT_SDP_DATA(ctypes.Union):
    value = 0
    offset = 0

    Data = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VSC_EXT_SDP_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VSC_EXT_SDP_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_BUFFER_READY(Enum):
    BUFFER_READY_READY_FOR_HW_USE = 0x1
    BUFFER_READY_NOT_READY_FOR_HW_USE = 0x0


class ENUM_BUFFER_EMPTY(Enum):
    BUFFER_EMPTY_BUFFER_EMPTY = 0x1
    BUFFER_EMPTY_BUFFER_NOT_EMPTY = 0x0


class ENUM_VSC_EXTENSION_SDP_METADATA_ENABLE(Enum):
    VSC_EXTENSION_SDP_METADATA_DISABLE = 0x0
    VSC_EXTENSION_SDP_METADATA_ENABLE = 0x1


class OFFSET_VSC_EXT_SDP_CTL:
    VSC_EXT_SDP_CTL_0_A = 0x60290
    VSC_EXT_SDP_CTL_1_A = 0x60294
    VSC_EXT_SDP_CTL_0_B = 0x61290
    VSC_EXT_SDP_CTL_1_B = 0x61294
    VSC_EXT_SDP_CTL_0_C = 0x62290
    VSC_EXT_SDP_CTL_1_C = 0x62294
    VSC_EXT_SDP_CTL_0_D = 0x63290
    VSC_EXT_SDP_CTL_1_D = 0x63294


class _VSC_EXT_SDP_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 6),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved15', ctypes.c_uint32, 1),
        ('BufferReady', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 7),
        ('BufferEmpty', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 6),
        ('VscExtensionSdpMetadataEnable', ctypes.c_uint32, 1),
    ]


class REG_VSC_EXT_SDP_CTL(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 14
    IndexAutoIncrement = 0  # bit 14 to 15
    Reserved15 = 0  # bit 15 to 16
    BufferReady = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 24
    BufferEmpty = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 31
    VscExtensionSdpMetadataEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VSC_EXT_SDP_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VSC_EXT_SDP_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TAIL_UPDATE_PERIOD(Enum):
    TAIL_UPDATE_PERIOD_16_LINES = 0x1


class OFFSET_WD_TAIL_CFG:
    WD_TAIL_CFG_0 = 0x6E520
    WD_TAIL_CFG_1 = 0x6ED20


class _WD_TAIL_CFG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 4),
        ('TailUpdatePeriod', ctypes.c_uint32, 8),
        ('Reserved12', ctypes.c_uint32, 4),
        ('TailInitialUpdateDelay', ctypes.c_uint32, 12),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_WD_TAIL_CFG(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 4
    TailUpdatePeriod = 0  # bit 4 to 12
    Reserved12 = 0  # bit 12 to 16
    TailInitialUpdateDelay = 0  # bit 16 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _WD_TAIL_CFG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_WD_TAIL_CFG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_WD_SURF:
    WD_SURF_0 = 0x6E514
    WD_SURF_1 = 0x6ED14


class _WD_SURF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('WdSurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_WD_SURF(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    WdSurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _WD_SURF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_WD_SURF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_WD_STRIDE:
    WD_STRIDE_0 = 0x6E510
    WD_STRIDE_1 = 0x6ED10


class _WD_STRIDE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 6),
        ('WdStride', ctypes.c_uint32, 10),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_WD_STRIDE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 6
    WdStride = 0  # bit 6 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _WD_STRIDE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_WD_STRIDE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_WD_INPUT_SELECT(Enum):
    WD_INPUT_SELECT_PIPE_A = 0x0
    WD_INPUT_SELECT_PIPE_B = 0x5
    WD_INPUT_SELECT_PIPE_C = 0x6
    WD_INPUT_SELECT_PIPE_D = 0x7


class ENUM_VDENC_SESSION_SELECT(Enum):
    VDENC_SESSION_SELECT_0 = 0x0
    VDENC_SESSION_SELECT_1 = 0x1
    VDENC_SESSION_SELECT_2 = 0x2
    VDENC_SESSION_SELECT_3 = 0x3


class ENUM_CONTROL_POINTERS(Enum):
    CONTROL_POINTERS_ENABLE_TAIL_AND_HEAD = 0x0  # Send tail pointer to GT. Follow head pointer from GT.
    CONTROL_POINTERS_ENABLE_TAIL_DISABLE_HEAD = 0x1  # Send tail pointer to GT. Ignore head pointer from GT. Non-cachea
                                                     # ble.
    CONTROL_POINTERS_DISABLE_TAIL_AND_HEAD = 0x3  # Do not send tail pointer to GT. Ignore head pointer from GT. Non-ca
                                                  # cheable.


class ENUM_WD_COLOR_MODE(Enum):
    WD_COLOR_MODE_YUV_444 = 0x0  # YUV 32-bit 4:4:4 packed (8:8:8:8 MSB-Y:U:X:V)
    WD_COLOR_MODE_YUV_422 = 0x1  # YUV 16-bit 4:2:2 packed (8:8:8:8 MSB- Y1:U:Y2:V) Chroma downsampling is programmable
                                 #  according to the Chroma Filtering field.
    WD_COLOR_MODE_XYUV_444 = 0x2  # YUV 32-bit 4:4:4 packed (8:8:8:8 MSB-X:Y:U:V)
    WD_COLOR_MODE_RGBX = 0x3  # RGBX 32-bit (8:8:8:8 MSB-X:B:G:R)
    WD_COLOR_MODE_Y410 = 0x4  # YUV 444 10bpc (MSB-X:V:Y:U)
    WD_COLOR_MODE_YUY2_8B = 0x5  # 8 bit YUV 422 (MSB-V:Y2:U:Y1) Chroma downsampling is programmable according to the C
                                 # hroma Filtering field.
    WD_COLOR_MODE_RGB10 = 0x6  # RGB1010102 (MSB-X:B:G:R)


class ENUM_CHROMA_FILTERING_ENABLE(Enum):
    CHROMA_FILTERING_ENABLE_DROP = 0x0  # Drop U2 and V2
    CHROMA_FILTERING_ENABLE_FILTER = 0x1  # Use a 15-34-15 three tap filter


class ENUM_ENABLE_WRITE_CACHING(Enum):
    ENABLE_WRITE_CACHING_DISABLE = 0x0
    ENABLE_WRITE_CACHING_ENABLE = 0x1


class ENUM_TRIGGERED_CAPTURE_MODE_ENABLE(Enum):
    TRIGGERED_CAPTURE_MODE_DISABLE = 0x0
    TRIGGERED_CAPTURE_MODE_ENABLE = 0x1


class ENUM_WD_FUNCTION_ENABLE(Enum):
    WD_FUNCTION_DISABLE = 0x0
    WD_FUNCTION_ENABLE = 0x1


class OFFSET_TRANS_WD_FUNC_CTL:
    TRANS_WD_FUNC_CTL_0 = 0x6E400
    TRANS_WD_FUNC_CTL_1 = 0x6EC00


class _TRANS_WD_FUNC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FrameNumber', ctypes.c_uint32, 4),
        ('MaximumDifferenceToEnableWriteCaching', ctypes.c_uint32, 8),
        ('WdInputSelect', ctypes.c_uint32, 3),
        ('Reserved15', ctypes.c_uint32, 1),
        ('VdencSessionSelect', ctypes.c_uint32, 2),
        ('ControlPointers', ctypes.c_uint32, 2),
        ('WdColorMode', ctypes.c_uint32, 3),
        ('Reserved23', ctypes.c_uint32, 3),
        ('ChromaFilteringEnable', ctypes.c_uint32, 1),
        ('EnableWriteCaching', ctypes.c_uint32, 1),
        ('StopTriggerFrame', ctypes.c_uint32, 1),
        ('StartTriggerFrame', ctypes.c_uint32, 1),
        ('TriggeredCaptureModeEnable', ctypes.c_uint32, 1),
        ('WdFunctionEnable', ctypes.c_uint32, 1),
    ]


class REG_TRANS_WD_FUNC_CTL(ctypes.Union):
    value = 0
    offset = 0

    FrameNumber = 0  # bit 0 to 4
    MaximumDifferenceToEnableWriteCaching = 0  # bit 4 to 12
    WdInputSelect = 0  # bit 12 to 15
    Reserved15 = 0  # bit 15 to 16
    VdencSessionSelect = 0  # bit 16 to 18
    ControlPointers = 0  # bit 18 to 20
    WdColorMode = 0  # bit 20 to 23
    Reserved23 = 0  # bit 23 to 26
    ChromaFilteringEnable = 0  # bit 26 to 27
    EnableWriteCaching = 0  # bit 27 to 28
    StopTriggerFrame = 0  # bit 28 to 29
    StartTriggerFrame = 0  # bit 29 to 30
    TriggeredCaptureModeEnable = 0  # bit 30 to 31
    WdFunctionEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_WD_FUNC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_WD_FUNC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_WD_LINK_M(Enum):
    WD_LINK_M_2 = 0x2  # M=2


class ENUM_COUNTER_FORCE(Enum):
    COUNTER_FORCE_FORCE_ENABLED = 0x1
    COUNTER_FORCE_DO_NOT_FORCE = 0x0


class OFFSET_WD_27_M:
    WD_27_M_0 = 0x6E524
    WD_27_M_1 = 0x6ED24


class _WD_27_M(ctypes.LittleEndianStructure):
    _fields_ = [
        ('WdLinkM', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 7),
        ('CounterForce', ctypes.c_uint32, 1),
    ]


class REG_WD_27_M(ctypes.Union):
    value = 0
    offset = 0

    WdLinkM = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 31
    CounterForce = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _WD_27_M),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_WD_27_M, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_WD_LINK_N(Enum):
    WD_LINK_N_25 = 0x19  # N=25


class OFFSET_WD_27_N:
    WD_27_N_0 = 0x6E528
    WD_27_N_1 = 0x6EC28


class _WD_27_N(ctypes.LittleEndianStructure):
    _fields_ = [
        ('WdLinkN', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_WD_27_N(ctypes.Union):
    value = 0
    offset = 0

    WdLinkN = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _WD_27_N),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_WD_27_N, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ENABLE_EXIT_LINE(Enum):
    ENABLE_EXIT_LINE_DISABLE = 0x0
    ENABLE_EXIT_LINE_ENABLE = 0x1


class OFFSET_TRANS_EXITLINE:
    TRANS_EXITLINE_A = 0x60018
    TRANS_EXITLINE_B = 0x61018
    TRANS_EXITLINE_C = 0x62018
    TRANS_EXITLINE_D = 0x63018


class _TRANS_EXITLINE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ExitLine', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 18),
        ('EnableExitLine', ctypes.c_uint32, 1),
    ]


class REG_TRANS_EXITLINE(ctypes.Union):
    value = 0
    offset = 0

    ExitLine = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 31
    EnableExitLine = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_EXITLINE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_EXITLINE, self).__init__()
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
        ('Reserved25', ctypes.c_uint32, 2),
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
    Reserved25 = 0  # bit 25 to 27
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


class ENUM_FAKE_ACK_DISABLE(Enum):
    FAKE_ACK_ENABLE_FAKE_ACK = 0x0
    FAKE_ACK_DISABLE_FAKE_ACK = 0x1


class OFFSET_CHICKEN_MISC_5:
    CHICKEN_MISC_5 = 0x42090


class _CHICKEN_MISC_5(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SkipRegisterAck', ctypes.c_uint32, 1),
        ('FakeAckDisable', ctypes.c_uint32, 1),
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
    FakeAckDisable = 0  # bit 1 to 2
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
        ('Reserved18', ctypes.c_uint32, 1),
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
    Reserved18 = 0  # bit 18 to 19
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
    UTIL_PIN_MODE_FRAMESTART = 0x6  # Output the framestart
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


class ENUM_KEY_SELECT(Enum):
    KEY_SELECT_PAVP = 0x0
    KEY_SELECT_ID = 0x1


class ENUM_ENCRYPTION(Enum):
    ENCRYPTION_NOT_ENCRYPTED = 0x0
    ENCRYPTION_ENCRYPTED = 0x1


class ENUM_WD_STATE(Enum):
    WD_STATE_IDLE = 0x0  # Reset state
    WD_STATE_CAPSTART = 0x1  # Start timing generator for normal capture
    WD_STATE_FRAME_START = 0x2  # Send framestart to display pipe
    WD_STATE_CAPACTIVE = 0x3  # Capturing data
    WD_STATE_TG_DONE = 0x4  # Completed writing pixels. Waiting for frame completion.
    WD_STATE_WDX_DONE = 0x5  # Fully completed frame. Waiting to start next frame.
    WD_STATE_QUICK_CAP = 0x6  # Quick capture entry


class OFFSET_WD_FRAME_STATUS:
    WD_FRAME_STATUS_0 = 0x6E568
    WD_FRAME_STATUS_1 = 0x6ED68


class _WD_FRAME_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 20),
        ('KeySelect', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 2),
        ('Encryption', ctypes.c_uint32, 1),
        ('WdState', ctypes.c_uint32, 3),
        ('Reserved27', ctypes.c_uint32, 4),
        ('FrameComplete', ctypes.c_uint32, 1),
    ]


class REG_WD_FRAME_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 20
    KeySelect = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 23
    Encryption = 0  # bit 23 to 24
    WdState = 0  # bit 24 to 27
    Reserved27 = 0  # bit 27 to 31
    FrameComplete = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _WD_FRAME_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_WD_FRAME_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

