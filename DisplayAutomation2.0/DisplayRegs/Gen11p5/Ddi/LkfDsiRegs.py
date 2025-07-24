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
# @file LkfDsiRegs.py
# @brief contains LkfDsiRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_EOTP_DISABLED(Enum):
    EOTP_DISABLED_EOTP_ENABLED = 0x0
    EOTP_DISABLED_EOTP_DISABLED = 0x1


class ENUM_S3D_ORIENTATION(Enum):
    S3D_ORIENTATION_PORTRAIT_ORIENTATION = 0x0
    S3D_ORIENTATION_LANDSCAPE_ORIENTATION = 0x1


class ENUM_BLANKING_PACKET_DURING_BLLP(Enum):
    BLANKING_PACKET_DURING_BLLP_DISABLED = 0x0  # LP allowed in BLLP regions
    BLANKING_PACKET_DURING_BLLP_ENABLED = 0x1  # Blanking packets transmitted in BLLP regions


class ENUM_LINK_CALIBRATION(Enum):
    LINK_CALIBRATION_CALIBRATION_DISABLED = 0x0
    LINK_CALIBRATION_CALIBRATION_ENABLED_INITIAL_ONLY = 0x2
    LINK_CALIBRATION_CALIBRATION_ENABLED_INITIAL_AND_PERIODIC = 0x3


class ENUM_LP_CLOCK_DURING_LPM(Enum):
    LP_CLOCK_DURING_LPM_DISABLED = 0x0  # Clock Lane does not follow the Data Lanes
    LP_CLOCK_DURING_LPM_ENABLE = 0x1  # Clock Lane follows the Data Lanes


class ENUM_CONTINUOUS_CLOCK(Enum):
    CONTINUOUS_CLOCK_ALWAYS_ENTER_LP_AFTER_DATA_LANES = 0x0
    CONTINUOUS_CLOCK_OPPORTUNISTICALLY_KEEP_CLOCK_IN_HS_OR_LP = 0x2
    CONTINUOUS_CLOCK_CONTINUOUS_HS_CLOCK = 0x3


class ENUM_PIXEL_BUFFER_THRESHOLD(Enum):
    PIXEL_BUFFER_THRESHOLD_THE_PIXEL_BUFFER_WILL_HAVE_TO_BE_1_4_FULL = 0x0
    PIXEL_BUFFER_THRESHOLD_THE_PIXEL_BUFFER_WILL_HAVE_TO_BE_1_2_FULL = 0x1
    PIXEL_BUFFER_THRESHOLD_THE_PIXEL_BUFFER_WILL_HAVE_TO_BE_3_4_FULL = 0x2
    PIXEL_BUFFER_THRESHOLD_THE_PIXEL_BUFFER_WILL_HAVE_TO_BE_FULL = 0x3


class ENUM_BGR_TRANSMISSION(Enum):
    BGR_TRANSMISSION_TRANSMIT_ORDER_IS_RGB = 0x0
    BGR_TRANSMISSION_TRANSMIT_ORDER_IS_BGR = 0x1


class ENUM_PIXEL_FORMAT(Enum):
    PIXEL_FORMAT_16BIT_RGB_565 = 0x0
    PIXEL_FORMAT_18BIT_RGB_666_PACKED = 0x1
    PIXEL_FORMAT_18BIT_RGB_666_LOOSE = 0x2
    PIXEL_FORMAT_24BIT_RGB_888 = 0x3
    PIXEL_FORMAT_30BIT_RGB_101010 = 0x4
    PIXEL_FORMAT_36BIT_RGB_121212 = 0x5
    PIXEL_FORMAT_COMPRESSED = 0x6


class ENUM_LINK_READY(Enum):
    LINK_READY_LINK_IS_NOT_READY_TO_ACCEPT_TRAFFIC = 0x0
    LINK_READY_LINK_IS_READY_TO_ACCEPT_TRAFFIC = 0x1


class ENUM_TE_ACCUMULATION(Enum):
    TE_ACCUMULATION_DISABLED = 0x0
    TE_ACCUMULATION_ENABLED = 0x1


class ENUM_TE_DEGLITCH_ENABLE(Enum):
    TE_DEGLITCH_DISABLED = 0x0
    TE_DEGLITCH_ENABLED = 0x1


class ENUM_TE_SOURCE(Enum):
    TE_SOURCE_INBAND_TE_EVENT_SOURCE = 0x0
    TE_SOURCE_OUTOFBAND_TE_EVENT_SOURCE_I_E_GPIO = 0x1


class ENUM_MODE_OF_OPERATION(Enum):
    MODE_OF_OPERATION_COMMAND_MODE_NO_GATE = 0x0
    MODE_OF_OPERATION_COMMAND_MODE_TE_GATE = 0x1
    MODE_OF_OPERATION_VIDEO_MODE_SYNC_EVENT = 0x2
    MODE_OF_OPERATION_VIDEO_MODE_SYNC_PULSE = 0x3


class OFFSET_TRANS_DSI_FUNC_CONF:
    TRANS_DSI_FUNC_CONF_0 = 0x6B030
    TRANS_DSI_FUNC_CONF_1 = 0x6B830


class _TRANS_DSI_FUNC_CONF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EotpDisabled', ctypes.c_uint32, 1),
        ('S3DOrientation', ctypes.c_uint32, 1),
        ('BlankingPacketDuringBllp', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 1),
        ('LinkCalibration', ctypes.c_uint32, 2),
        ('Reserved6', ctypes.c_uint32, 1),
        ('LpClockDuringLpm', ctypes.c_uint32, 1),
        ('ContinuousClock', ctypes.c_uint32, 2),
        ('PixelBufferThreshold', ctypes.c_uint32, 2),
        ('PixelVirtualChannel', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 1),
        ('BgrTransmission', ctypes.c_uint32, 1),
        ('PixelFormat', ctypes.c_uint32, 3),
        ('Reserved19', ctypes.c_uint32, 1),
        ('LinkReady', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 4),
        ('TeAccumulation', ctypes.c_uint32, 1),
        ('TeDeglitchEnable', ctypes.c_uint32, 1),
        ('TeSource', ctypes.c_uint32, 1),
        ('ModeOfOperation', ctypes.c_uint32, 2),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_TRANS_DSI_FUNC_CONF(ctypes.Union):
    value = 0
    offset = 0

    EotpDisabled = 0  # bit 0 to 1
    S3DOrientation = 0  # bit 1 to 2
    BlankingPacketDuringBllp = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 4
    LinkCalibration = 0  # bit 4 to 6
    Reserved6 = 0  # bit 6 to 7
    LpClockDuringLpm = 0  # bit 7 to 8
    ContinuousClock = 0  # bit 8 to 10
    PixelBufferThreshold = 0  # bit 10 to 12
    PixelVirtualChannel = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 15
    BgrTransmission = 0  # bit 15 to 16
    PixelFormat = 0  # bit 16 to 19
    Reserved19 = 0  # bit 19 to 20
    LinkReady = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 25
    TeAccumulation = 0  # bit 25 to 26
    TeDeglitchEnable = 0  # bit 26 to 27
    TeSource = 0  # bit 27 to 28
    ModeOfOperation = 0  # bit 28 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _TRANS_DSI_FUNC_CONF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_TRANS_DSI_FUNC_CONF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CLK_TRAIL_OVERRIDE(Enum):
    CLK_TRAIL_OVERRIDE_HW_MAINTAINS = 0x0
    CLK_TRAIL_OVERRIDE_SW_OVERRIDES = 0x1


class ENUM_CLK_POST_OVERRIDE(Enum):
    CLK_POST_OVERRIDE_HW_MAINTAINS = 0x0
    CLK_POST_OVERRIDE_SW_OVERRIDES = 0x1


class ENUM_CLK_PRE_OVERRIDE(Enum):
    CLK_PRE_OVERRIDE_HW_MAINTAINS = 0x0
    CLK_PRE_OVERRIDE_SW_OVERRIDES = 0x1


class ENUM_CLK_ZERO_OVERRIDE(Enum):
    CLK_ZERO_OVERRIDE_HW_MAINTAINS = 0x0
    CLK_ZERO_OVERRIDE_SW_OVERRIDES = 0x1


class ENUM_CLK_PREPARE(Enum):
    CLK_PREPARE_0_25_ESCAPE_CLOCKS = 0x1
    CLK_PREPARE_0_50_ESCAPE_CLOCKS = 0x2
    CLK_PREPARE_0_75_ESCAPE_CLOCKS = 0x3
    CLK_PREPARE_1_00_ESCAPE_CLOCKS = 0x4
    CLK_PREPARE_1_25_ESCAPE_CLOCKS = 0x5
    CLK_PREPARE_1_50_ESCAPE_CLOCKS = 0x6
    CLK_PREPARE_1_75_ESCAPE_CLOCKS = 0x7


class ENUM_CLK_PREPARE_OVERRIDE(Enum):
    CLK_PREPARE_OVERRIDE_HW_MAINTAINS = 0x0
    CLK_PREPARE_OVERRIDE_SW_OVERRIDES = 0x1


class OFFSET_DSI_CLK_TIMING_PARAM:
    DSI_CLK_TIMING_PARAM_0 = 0x6B080
    DSI_CLK_TIMING_PARAM_1 = 0x6B880


class _DSI_CLK_TIMING_PARAM(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Clk_Trail', ctypes.c_uint32, 3),
        ('Reserved3', ctypes.c_uint32, 4),
        ('Clk_TrailOverride', ctypes.c_uint32, 1),
        ('Clk_Post', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 4),
        ('Clk_PostOverride', ctypes.c_uint32, 1),
        ('Clk_Pre', ctypes.c_uint32, 2),
        ('Reserved18', ctypes.c_uint32, 1),
        ('Clk_PreOverride', ctypes.c_uint32, 1),
        ('Clk_Zero', ctypes.c_uint32, 4),
        ('Reserved24', ctypes.c_uint32, 3),
        ('Clk_ZeroOverride', ctypes.c_uint32, 1),
        ('Clk_Prepare', ctypes.c_uint32, 3),
        ('Clk_PrepareOverride', ctypes.c_uint32, 1),
    ]


class REG_DSI_CLK_TIMING_PARAM(ctypes.Union):
    value = 0
    offset = 0

    Clk_Trail = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 7
    Clk_TrailOverride = 0  # bit 7 to 8
    Clk_Post = 0  # bit 8 to 11
    Reserved11 = 0  # bit 11 to 15
    Clk_PostOverride = 0  # bit 15 to 16
    Clk_Pre = 0  # bit 16 to 18
    Reserved18 = 0  # bit 18 to 19
    Clk_PreOverride = 0  # bit 19 to 20
    Clk_Zero = 0  # bit 20 to 24
    Reserved24 = 0  # bit 24 to 27
    Clk_ZeroOverride = 0  # bit 27 to 28
    Clk_Prepare = 0  # bit 28 to 31
    Clk_PrepareOverride = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CLK_TIMING_PARAM),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CLK_TIMING_PARAM, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_HS_EXIT_OVERRIDE(Enum):
    HS_EXIT_OVERRIDE_HW_MAINTAINS = 0x0
    HS_EXIT_OVERRIDE_SW_OVERRIDES = 0x1


class ENUM_HS_TRAIL_OVERRIDE(Enum):
    HS_TRAIL_OVERRIDE_HW_MAINTAINS = 0x0
    HS_TRAIL_OVERRIDE_SW_OVERRIDES = 0x1


class ENUM_HS_ZERO_OVERRIDE(Enum):
    HS_ZERO_OVERRIDE_HW_MAINTAINS = 0x0
    HS_ZERO_OVERRIDE_SW_OVERRIDES = 0x1


class ENUM_HS_PREPARE(Enum):
    HS_PREPARE_0_25_ESCAPE_CLOCKS = 0x1
    HS_PREPARE_0_50_ESCAPE_CLOCKS = 0x2
    HS_PREPARE_0_75_ESCAPE_CLOCKS = 0x3
    HS_PREPARE_1_0_ESCAPE_CLOCKS = 0x4
    HS_PREPARE_1_25_ESCAPE_CLOCKS = 0x5
    HS_PREPARE_1_50_ESCAPE_CLOCKS = 0x6
    HS_PREPARE_1_75_ESCAPE_CLOCKS = 0x7


class ENUM_HS_PREPARE_OVERRIDE(Enum):
    HS_PREPARE_OVERRIDE_HW_MAINTAINS = 0x0
    HS_PREPARE_OVERRIDE_SW_OVERRIDES = 0x1


class OFFSET_DSI_DATA_TIMING_PARAM:
    DSI_DATA_TIMING_PARAM_0 = 0x6B084
    DSI_DATA_TIMING_PARAM_1 = 0x6B884


class _DSI_DATA_TIMING_PARAM(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Hs_Exit', ctypes.c_uint32, 3),
        ('Reserved3', ctypes.c_uint32, 4),
        ('Hs_ExitOverride', ctypes.c_uint32, 1),
        ('Hs_Trail', ctypes.c_uint32, 3),
        ('Reserved11', ctypes.c_uint32, 4),
        ('Hs_TrailOverride', ctypes.c_uint32, 1),
        ('Hs_Zero', ctypes.c_uint32, 4),
        ('Reserved20', ctypes.c_uint32, 3),
        ('Hs_ZeroOverride', ctypes.c_uint32, 1),
        ('Hs_Prepare', ctypes.c_uint32, 3),
        ('Reserved27', ctypes.c_uint32, 4),
        ('Hs_PrepareOverride', ctypes.c_uint32, 1),
    ]


class REG_DSI_DATA_TIMING_PARAM(ctypes.Union):
    value = 0
    offset = 0

    Hs_Exit = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 7
    Hs_ExitOverride = 0  # bit 7 to 8
    Hs_Trail = 0  # bit 8 to 11
    Reserved11 = 0  # bit 11 to 15
    Hs_TrailOverride = 0  # bit 15 to 16
    Hs_Zero = 0  # bit 16 to 20
    Reserved20 = 0  # bit 20 to 23
    Hs_ZeroOverride = 0  # bit 23 to 24
    Hs_Prepare = 0  # bit 24 to 27
    Reserved27 = 0  # bit 27 to 31
    Hs_PrepareOverride = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_DATA_TIMING_PARAM),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_DATA_TIMING_PARAM, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_ESC_CLK_DIV:
    DSI_ESC_CLK_DIV_0 = 0x6B090
    DSI_ESC_CLK_DIV_1 = 0x6B890


class _DSI_ESC_CLK_DIV(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EscapeClockDividerM', ctypes.c_uint32, 9),
        ('Reserved9', ctypes.c_uint32, 7),
        ('ByteClocksPerEscapeClock', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DSI_ESC_CLK_DIV(ctypes.Union):
    value = 0
    offset = 0

    EscapeClockDividerM = 0  # bit 0 to 9
    Reserved9 = 0  # bit 9 to 16
    ByteClocksPerEscapeClock = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_ESC_CLK_DIV),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_ESC_CLK_DIV, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_T_INIT_MASTER:
    DSI_T_INIT_MASTER_0 = 0x6B088
    DSI_T_INIT_MASTER_1 = 0x6B888


class _DSI_T_INIT_MASTER(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MasterInitializationTime', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DSI_T_INIT_MASTER(ctypes.Union):
    value = 0
    offset = 0

    MasterInitializationTime = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_T_INIT_MASTER),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_T_INIT_MASTER, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_T_WAKEUP:
    DSI_T_WAKEUP_0 = 0x6B08C
    DSI_T_WAKEUP_1 = 0x6B88C


class _DSI_T_WAKEUP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('WakeupTime', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DSI_T_WAKEUP(ctypes.Union):
    value = 0
    offset = 0

    WakeupTime = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_T_WAKEUP),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_T_WAKEUP, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_CALIB_TO:
    DSI_CALIB_TO_0 = 0x6B050
    DSI_CALIB_TO_1 = 0x6B850


class _DSI_CALIB_TO(ctypes.LittleEndianStructure):
    _fields_ = [
        ('InitialCalibrationTimeout', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 4),
        ('PeriodicCalibrationTimeout', ctypes.c_uint32, 12),
    ]


class REG_DSI_CALIB_TO(ctypes.Union):
    value = 0
    offset = 0

    InitialCalibrationTimeout = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 20
    PeriodicCalibrationTimeout = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CALIB_TO),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CALIB_TO, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_STEREOSCOPIC_3D_HBP_AS_VERTICAL_SPACE(Enum):
    STEREOSCOPIC_3D_HBP_AS_VERTICAL_SPACE_HFP_USED_AS_V_SPACE = 0x0
    STEREOSCOPIC_3D_HBP_AS_VERTICAL_SPACE_HBP_USED_AS_V_SPACE = 0x1


class ENUM_STEREOSCOPIC_3D_UPDATE_FREQUENCY(Enum):
    STEREOSCOPIC_3D_UPDATE_FREQUENCY_UPDATE_EVERY_VSS = 0x0  # As long as S3D is enabled, S3D control information will 
                                                             # be sent out in every VSS packet
    STEREOSCOPIC_3D_UPDATE_FREQUENCY_UPDATE_ON_S3D_CHANGES = 0x1  # S3D control information will only be sent when S3D 
                                                                  # programming changes


class ENUM_DUAL_LINK_MIRRORING_DISABLE(Enum):
    DUAL_LINK_MIRRORING_DISABLE_MIRRORING_ENABLED = 0x0
    DUAL_LINK_MIRRORING_DISABLE_MIRRORING_DISABLED = 0x1


class ENUM_DCS_PAYLOAD_FORMAT_DISABLE(Enum):
    DCS_PAYLOAD_FORMAT_ENABLED = 0x0
    DCS_PAYLOAD_FORMAT_DISABLED = 0x1


class ENUM_IGNORE_RESET_WARNING(Enum):
    IGNORE_RESET_WARNING_DON_T_IGNORE = 0x0
    IGNORE_RESET_WARNING_IGNORE = 0x1


class OFFSET_DSI_CHKN_REG0:
    DSI_CHKN_REG0_0 = 0x6B0C0
    DSI_CHKN_REG0_1 = 0x6B8C0


class _DSI_CHKN_REG0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HsToHsTurnaroundGuardband', ctypes.c_uint32, 8),
        ('Spare8', ctypes.c_uint32, 1),
        ('Spare9', ctypes.c_uint32, 1),
        ('Spare10', ctypes.c_uint32, 1),
        ('Spare11', ctypes.c_uint32, 1),
        ('LpToHsWakeupGuardband', ctypes.c_uint32, 4),
        ('Stereoscopic3DHbpAsVerticalSpace', ctypes.c_uint32, 1),
        ('Stereoscopic3DUpdateFrequency', ctypes.c_uint32, 1),
        ('DualLinkMirroringDisable', ctypes.c_uint32, 1),
        ('DcsPayloadFormatDisable', ctypes.c_uint32, 1),
        ('IgnoreResetWarning', ctypes.c_uint32, 1),
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


class REG_DSI_CHKN_REG0(ctypes.Union):
    value = 0
    offset = 0

    HsToHsTurnaroundGuardband = 0  # bit 0 to 8
    Spare8 = 0  # bit 8 to 9
    Spare9 = 0  # bit 9 to 10
    Spare10 = 0  # bit 10 to 11
    Spare11 = 0  # bit 11 to 12
    LpToHsWakeupGuardband = 0  # bit 12 to 16
    Stereoscopic3DHbpAsVerticalSpace = 0  # bit 16 to 17
    Stereoscopic3DUpdateFrequency = 0  # bit 17 to 18
    DualLinkMirroringDisable = 0  # bit 18 to 19
    DcsPayloadFormatDisable = 0  # bit 19 to 20
    IgnoreResetWarning = 0  # bit 20 to 21
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
        ('bitMap', _DSI_CHKN_REG0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CHKN_REG0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CRC_CAPTURE(Enum):
    CRC_CAPTURE_NO_CAPTURE_REQUEST = 0x0
    CRC_CAPTURE_CAPTURE_REQUEST = 0x1


class ENUM_ENABLE_CRC(Enum):
    ENABLE_CRC_CRC_DISABLED = 0x0
    ENABLE_CRC_CRC_ENABLED = 0x1


class OFFSET_DSI_CMDCRC_CTL:
    DSI_CMDCRC_CTL_0 = 0x6B0A8
    DSI_CMDCRC_CTL_1 = 0x6B8A8


class _DSI_CMDCRC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 30),
        ('CrcCapture', ctypes.c_uint32, 1),
        ('EnableCrc', ctypes.c_uint32, 1),
    ]


class REG_DSI_CMDCRC_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 30
    CrcCapture = 0  # bit 30 to 31
    EnableCrc = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CMDCRC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CMDCRC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_FORWARD_FRAME_UPDATE_REQUEST(Enum):
    FORWARD_FRAME_UPDATE_REQUEST_REQUEST_NOT_FORWARDED = 0x0
    FORWARD_FRAME_UPDATE_REQUEST_REQUEST_FORWARDED = 0x1


class ENUM_ACCUMULATE_FRAME_UPDATE_REQUESTS(Enum):
    ACCUMULATE_FRAME_UPDATE_REQUESTS_NO_ACCUMULATION = 0x0
    ACCUMULATE_FRAME_UPDATE_REQUESTS_ACCUMULATE = 0x1


class ENUM_SINGLE_PANEL_UPDATE(Enum):
    SINGLE_PANEL_UPDATE_DUAL_PANEL_UPDATE = 0x0
    SINGLE_PANEL_UPDATE_SINGLE_PANEL_UPDATE = 0x1


class ENUM_NULL_PACKET_ENABLE(Enum):
    NULL_PACKET_ENABLE_NULL_PACKET_INJECTION_DISABLED = 0x0
    NULL_PACKET_ENABLE_NULL_PACKET_INJECTION_ENABLED = 0x1


class ENUM_PERIODIC_FRAME_UPDATE_ENABLE(Enum):
    PERIODIC_FRAME_UPDATE_ENABLE_PERIODIC_FRAME_UPDATE_DISABLED = 0x0
    PERIODIC_FRAME_UPDATE_ENABLE_PERIODIC_FRAME_UPDATE_ENABLED = 0x1


class ENUM_FRAME_UPDATE_REQUEST(Enum):
    FRAME_UPDATE_REQUEST_NO_FRAME_REQUEST_PRESENT = 0x0
    FRAME_UPDATE_REQUEST_FRAME_REQUEST_PRESENT = 0x1


class OFFSET_DSI_CMD_FRMCTL:
    DSI_CMD_FRMCTL_0 = 0x6B034
    DSI_CMD_FRMCTL_1 = 0x6B834


class _DSI_CMD_FRMCTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FrameInProgress', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 24),
        ('ForwardFrameUpdateRequest', ctypes.c_uint32, 1),
        ('AccumulateFrameUpdateRequests', ctypes.c_uint32, 1),
        ('SinglePanelUpdate', ctypes.c_uint32, 1),
        ('NullPacketEnable', ctypes.c_uint32, 1),
        ('PeriodicFrameUpdateEnable', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 1),
        ('FrameUpdateRequest', ctypes.c_uint32, 1),
    ]


class REG_DSI_CMD_FRMCTL(ctypes.Union):
    value = 0
    offset = 0

    FrameInProgress = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 25
    ForwardFrameUpdateRequest = 0  # bit 25 to 26
    AccumulateFrameUpdateRequests = 0  # bit 26 to 27
    SinglePanelUpdate = 0  # bit 27 to 28
    NullPacketEnable = 0  # bit 28 to 29
    PeriodicFrameUpdateEnable = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 31
    FrameUpdateRequest = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CMD_FRMCTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CMD_FRMCTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_RECEIVED_CRC_WAS_LOST(Enum):
    RECEIVED_CRC_WAS_LOST_NO_CRC_BYTES_DROPPED = 0x0
    RECEIVED_CRC_WAS_LOST_CRC_BYTES_DROPPED = 0x1


class ENUM_RECEIVED_PAYLOAD_WAS_LOST(Enum):
    RECEIVED_PAYLOAD_WAS_LOST_NO_PAYLOAD_BYTES_DROPPED = 0x0
    RECEIVED_PAYLOAD_WAS_LOST_PAYLOAD_BYTES_DROPPED = 0x1


class ENUM_RECEIVED_RESET_TRIGGER(Enum):
    RECEIVED_RESET_TRIGGER_TRIGGER_MESSAGE_NOT_RECEIVED = 0x0
    RECEIVED_RESET_TRIGGER_TRIGGER_MESSAGE_RECEIVED = 0x1


class ENUM_RECEIVED_TEAR_EFFECT_TRIGGER(Enum):
    RECEIVED_TEAR_EFFECT_TRIGGER_TRIGGER_MESSAGE_NOT_RECEIVED = 0x0
    RECEIVED_TEAR_EFFECT_TRIGGER_TRIGGER_MESSAGE_RECEIVED = 0x1


class ENUM_RECEIVED_ACKNOWLEDGE_TRIGGER(Enum):
    RECEIVED_ACKNOWLEDGE_TRIGGER_TRIGGER_MESSAGE_NOT_RECEIVED = 0x0
    RECEIVED_ACKNOWLEDGE_TRIGGER_TRIGGER_MESSAGE_RECEIVED = 0x1


class ENUM_RECEIVED_UNASSIGNED_TRIGGER(Enum):
    RECEIVED_UNASSIGNED_TRIGGER_TRIGGER_MESSAGE_NOT_RECEIVED = 0x0
    RECEIVED_UNASSIGNED_TRIGGER_TRIGGER_MESSAGE_RECEIVED = 0x1


class ENUM_READ_UNLOADS_DW(Enum):
    READ_UNLOADS_DW_DSI_RXDATA_READS_DO_NOT_UNLOAD_DW = 0x0
    READ_UNLOADS_DW_DSI_RXDATA_READS_UNLOAD_DW = 0x1


class OFFSET_DSI_CMD_RXCTL:
    DSI_CMD_RXCTL_0 = 0x6B0D4
    DSI_CMD_RXCTL_1 = 0x6B8D4


class _DSI_CMD_RXCTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('NumberRxPayloadDw', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 2),
        ('ReceivedCrcWasLost', ctypes.c_uint32, 1),
        ('ReceivedPayloadWasLost', ctypes.c_uint32, 1),
        ('ReceivedResetTrigger', ctypes.c_uint32, 1),
        ('ReceivedTearEffectTrigger', ctypes.c_uint32, 1),
        ('ReceivedAcknowledgeTrigger', ctypes.c_uint32, 1),
        ('ReceivedUnassignedTrigger', ctypes.c_uint32, 1),
        ('ReadUnloadsDw', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_DSI_CMD_RXCTL(ctypes.Union):
    value = 0
    offset = 0

    NumberRxPayloadDw = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 10
    ReceivedCrcWasLost = 0  # bit 10 to 11
    ReceivedPayloadWasLost = 0  # bit 11 to 12
    ReceivedResetTrigger = 0  # bit 12 to 13
    ReceivedTearEffectTrigger = 0  # bit 13 to 14
    ReceivedAcknowledgeTrigger = 0  # bit 14 to 15
    ReceivedUnassignedTrigger = 0  # bit 15 to 16
    ReadUnloadsDw = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CMD_RXCTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CMD_RXCTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_CMD_RXPYLD:
    DSI_CMD_RXPYLD_0 = 0x6B0E4
    DSI_CMD_RXPYLD_1 = 0x6B8E4


class _DSI_CMD_RXPYLD(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ReceivedPayload', ctypes.c_uint32, 32),
    ]


class REG_DSI_CMD_RXPYLD(ctypes.Union):
    value = 0
    offset = 0

    ReceivedPayload = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CMD_RXPYLD),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CMD_RXPYLD, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_CMD_TXCTL:
    DSI_CMD_TXCTL_0 = 0x6B0D0
    DSI_CMD_TXCTL_1 = 0x6B8D0


class _DSI_CMD_TXCTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FreePayloadCredits', ctypes.c_uint32, 8),
        ('FreeHeaderCredits', ctypes.c_uint32, 5),
        ('Reserved13', ctypes.c_uint32, 11),
        ('KeepLinkInHs', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 7),
    ]


class REG_DSI_CMD_TXCTL(ctypes.Union):
    value = 0
    offset = 0

    FreePayloadCredits = 0  # bit 0 to 8
    FreeHeaderCredits = 0  # bit 8 to 13
    Reserved13 = 0  # bit 13 to 24
    KeepLinkInHs = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CMD_TXCTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CMD_TXCTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_VERTICAL_BLANK_FENCE(Enum):
    VERTICAL_BLANK_FENCE_CMD_WILL_NOT_BE_FENCED = 0x0
    VERTICAL_BLANK_FENCE_CMD_WILL_BE_FENCED = 0x1


class ENUM_LPDT(Enum):
    LPDT_CMD_TRANSMITTED_IN_HS_STATE = 0x0
    LPDT_CMD_TRANSMITTED_IN_LP_ESCAPE_MODE = 0x1


class ENUM_PAYLOAD(Enum):
    PAYLOAD_SHORT_PACKET_FORMAT_NO_PAYLOAD = 0x0
    PAYLOAD_LONG_PACKET_FORMAT_PAYLOAD = 0x1


class OFFSET_DSI_CMD_TXHDR:
    DSI_CMD_TXHDR_0 = 0x6B100
    DSI_CMD_TXHDR_1 = 0x6B900


class _DSI_CMD_TXHDR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DataType', ctypes.c_uint32, 6),
        ('VirtualChannel', ctypes.c_uint32, 2),
        ('WordCountParameters', ctypes.c_uint32, 16),
        ('Reserved24', ctypes.c_uint32, 5),
        ('VerticalBlankFence', ctypes.c_uint32, 1),
        ('Lpdt', ctypes.c_uint32, 1),
        ('Payload', ctypes.c_uint32, 1),
    ]


class REG_DSI_CMD_TXHDR(ctypes.Union):
    value = 0
    offset = 0

    DataType = 0  # bit 0 to 6
    VirtualChannel = 0  # bit 6 to 8
    WordCountParameters = 0  # bit 8 to 24
    Reserved24 = 0  # bit 24 to 29
    VerticalBlankFence = 0  # bit 29 to 30
    Lpdt = 0  # bit 30 to 31
    Payload = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CMD_TXHDR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CMD_TXHDR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_CMD_TXPYLD:
    DSI_CMD_TXPYLD_0 = 0x6B104
    DSI_CMD_TXPYLD_1 = 0x6B904


class _DSI_CMD_TXPYLD(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PayloadData', ctypes.c_uint32, 32),
    ]


class REG_DSI_CMD_TXPYLD(ctypes.Union):
    value = 0
    offset = 0

    PayloadData = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CMD_TXPYLD),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CMD_TXPYLD, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TE_EVENT_INJECTION(Enum):
    TE_EVENT_INJECTION_NO_TE_INJECTION = 0x0
    TE_EVENT_INJECTION_TE_INJECTION = 0x1


class ENUM_PPI_RX_DIRECTION_CONTROL(Enum):
    PPI_RX_DIRECTION_CONTROL_FORWARD_DIRECTION = 0x0
    PPI_RX_DIRECTION_CONTROL_REVERSE_DIRECTION = 0x1


class ENUM_PPI_TX_DIRECTION_CONTROL(Enum):
    PPI_TX_DIRECTION_CONTROL_FORWARD_DIRECTION = 0x0
    PPI_TX_DIRECTION_CONTROL_REVERSE_DIRECTION = 0x1


class ENUM_PPI_LP_TX_READY_CONTROL(Enum):
    PPI_LP_TX_READY_CONTROL_LP_TX_NOT_READY = 0x0
    PPI_LP_TX_READY_CONTROL_LP_TX_READY = 0x1


class ENUM_PPI_DATA_ULPS_ACTIVE_NOT_CONTROL(Enum):
    PPI_DATA_ULPS_ACTIVE_NOT_CONTROL_DATA_LANES_IN_ULPS = 0x0
    PPI_DATA_ULPS_ACTIVE_NOT_CONTROL_DATA_LANES_NOT_IN_ULPS = 0x1


class ENUM_PPI_CLOCK_ULPS_ACTIVE_NOT_CONTROL(Enum):
    PPI_CLOCK_ULPS_ACTIVE_NOT_CONTROL_CLOCK_LANE_IN_ULPS = 0x0
    PPI_CLOCK_ULPS_ACTIVE_NOT_CONTROL_CLOCK_LANE_NOT_IN_ULPS = 0x1


class ENUM_PPI_DATA_STOPSTATE_CONTROL(Enum):
    PPI_DATA_STOPSTATE_CONTROL_DATA_LANES_NOT_IN_STOP_STATE = 0x0
    PPI_DATA_STOPSTATE_CONTROL_DATA_LANES_IN_STOP_STATE = 0x1


class ENUM_PPI_CLOCK_STOPSTATE_CONTROL(Enum):
    PPI_CLOCK_STOPSTATE_CONTROL_CLOCK_LANE_NOT_IN_STOP_STATE = 0x0
    PPI_CLOCK_STOPSTATE_CONTROL_CLOCK_LANE_IN_STOP_STATE = 0x1


class ENUM_TE_EVENT_STATUS(Enum):
    TE_EVENT_STATUS_NO_TE_EVENT_PRESENT = 0x0
    TE_EVENT_STATUS_TE_EVENT_PRESENT = 0x1


class ENUM_STOPSTATE_ISOLATION_OVERRIDE(Enum):
    STOPSTATE_ISOLATION_OVERRIDE_NO_OVERRIDE = 0x0
    STOPSTATE_ISOLATION_OVERRIDE_OVERRIDE = 0x1


class ENUM_TX_TO_RX_LPDT_LOOPBACK_ENABLE(Enum):
    TX_TO_RX_LPDT_LOOPBACK_DISABLED = 0x0
    TX_TO_RX_LPDT_LOOPBACK_ENABLED = 0x1


class ENUM_TE_ISOLATION_MODE_ENABLE(Enum):
    TE_ISOLATION_MODE_ENABLE_ISOLATION_MODE_DISABLED = 0x0
    TE_ISOLATION_MODE_ENABLE_ISOLATION_MODE_ENABLED = 0x1


class ENUM_PPI_ISOLATION_MODE_ENABLE(Enum):
    PPI_ISOLATION_MODE_DISABLED = 0x0
    PPI_ISOLATION_MODE_ENABLED = 0x1


class OFFSET_DSI_DFX_CTL:
    DSI_DFX_CTL_0 = 0x6B0C4
    DSI_DFX_CTL_1 = 0x6B8C4


class _DSI_DFX_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TeEventInjection', ctypes.c_uint32, 1),
        ('PpiRxDirectionControl', ctypes.c_uint32, 1),
        ('PpiTxDirectionControl', ctypes.c_uint32, 1),
        ('PpiLpTxReadyControl', ctypes.c_uint32, 1),
        ('PpiDataUlpsActiveNotControl', ctypes.c_uint32, 1),
        ('PpiClockUlpsActiveNotControl', ctypes.c_uint32, 1),
        ('PpiDataStopstateControl', ctypes.c_uint32, 1),
        ('PpiClockStopstateControl', ctypes.c_uint32, 1),
        ('TeHoldoffTime', ctypes.c_uint32, 2),
        ('Reserved10', ctypes.c_uint32, 2),
        ('TeAssertionTime', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 2),
        ('TeEventStatus', ctypes.c_uint32, 1),
        ('LpTxValidStatus', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 2),
        ('ClockLaneUlpsExitStatus', ctypes.c_uint32, 1),
        ('DataLaneUlpsExitStatus', ctypes.c_uint32, 1),
        ('ClockLaneUlpsEntryStatus', ctypes.c_uint32, 1),
        ('DataLaneUlpsEntryStatus', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 4),
        ('StopstateIsolationOverride', ctypes.c_uint32, 1),
        ('TxToRxLpdtLoopbackEnable', ctypes.c_uint32, 1),
        ('TeIsolationModeEnable', ctypes.c_uint32, 1),
        ('PpiIsolationModeEnable', ctypes.c_uint32, 1),
    ]


class REG_DSI_DFX_CTL(ctypes.Union):
    value = 0
    offset = 0

    TeEventInjection = 0  # bit 0 to 1
    PpiRxDirectionControl = 0  # bit 1 to 2
    PpiTxDirectionControl = 0  # bit 2 to 3
    PpiLpTxReadyControl = 0  # bit 3 to 4
    PpiDataUlpsActiveNotControl = 0  # bit 4 to 5
    PpiClockUlpsActiveNotControl = 0  # bit 5 to 6
    PpiDataStopstateControl = 0  # bit 6 to 7
    PpiClockStopstateControl = 0  # bit 7 to 8
    TeHoldoffTime = 0  # bit 8 to 10
    Reserved10 = 0  # bit 10 to 12
    TeAssertionTime = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 16
    TeEventStatus = 0  # bit 16 to 17
    LpTxValidStatus = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 20
    ClockLaneUlpsExitStatus = 0  # bit 20 to 21
    DataLaneUlpsExitStatus = 0  # bit 21 to 22
    ClockLaneUlpsEntryStatus = 0  # bit 22 to 23
    DataLaneUlpsEntryStatus = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 28
    StopstateIsolationOverride = 0  # bit 28 to 29
    TxToRxLpdtLoopbackEnable = 0  # bit 29 to 30
    TeIsolationModeEnable = 0  # bit 30 to 31
    PpiIsolationModeEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_DFX_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_DFX_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ACCUM_ENABLE(Enum):
    ACCUM_ENABLE_ACCUM_DISABLE = 0x0
    ACCUM_ENABLE_ACCUM_ENABLE = 0x1


class ENUM_CRC_FIELD_EYE(Enum):
    CRC_FIELD_EYE_FIELD_0_OR_RIGHT_EYE = 0x0
    CRC_FIELD_EYE_FIELD_1_OR_LEFT_EYE = 0x1


class ENUM_CRC_DONE(Enum):
    CRC_DONE_NOT_DONE = 0x0
    CRC_DONE_DONE = 0x1


class ENUM_CRC_CHANGE(Enum):
    CRC_CHANGE_NO_CHANGE = 0x0
    CRC_CHANGE_CHANGE = 0x1


class OFFSET_DSI_FRMCRC_CTL:
    DSI_FRMCRC_CTL_0 = 0x6B0A0
    DSI_FRMCRC_CTL_1 = 0x6B8A0


class _DSI_FRMCRC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('AccumStartFrame', ctypes.c_uint32, 4),
        ('AccumEndFrame', ctypes.c_uint32, 4),
        ('AccumEnable', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 14),
        ('CrcFieldEye', ctypes.c_uint32, 1),
        ('CrcDone', ctypes.c_uint32, 1),
        ('CrcChange', ctypes.c_uint32, 1),
        ('Reserved26', ctypes.c_uint32, 5),
        ('EnableCrc', ctypes.c_uint32, 1),
    ]


class REG_DSI_FRMCRC_CTL(ctypes.Union):
    value = 0
    offset = 0

    AccumStartFrame = 0  # bit 0 to 4
    AccumEndFrame = 0  # bit 4 to 8
    AccumEnable = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 23
    CrcFieldEye = 0  # bit 23 to 24
    CrcDone = 0  # bit 24 to 25
    CrcChange = 0  # bit 25 to 26
    Reserved26 = 0  # bit 26 to 31
    EnableCrc = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_FRMCRC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_FRMCRC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_FRMCRC_RES:
    DSI_FRMCRC_RES_0 = 0x6B0A4
    DSI_FRMCRC_RES_1 = 0x6B8A4


class _DSI_FRMCRC_RES(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CrcResultValue', ctypes.c_uint32, 32),
    ]


class REG_DSI_FRMCRC_RES(ctypes.Union):
    value = 0
    offset = 0

    CrcResultValue = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_FRMCRC_RES),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_FRMCRC_RES, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_HTX_TO:
    DSI_HTX_TO_0 = 0x6B044
    DSI_HTX_TO_1 = 0x6B844


class _DSI_HTX_TO(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Htx_To', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 15),
        ('HsTxTimeout', ctypes.c_uint32, 16),
    ]


class REG_DSI_HTX_TO(ctypes.Union):
    value = 0
    offset = 0

    Htx_To = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 16
    HsTxTimeout = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_HTX_TO),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_HTX_TO, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_INTER_IDENT_REG:
    DSI_INTER_IDENT_REG_0 = 0x6B074
    DSI_INTER_IDENT_REG_1 = 0x6B874


class _DSI_INTER_IDENT_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SotError', ctypes.c_uint32, 1),
        ('SotSyncError', ctypes.c_uint32, 1),
        ('EotSyncError', ctypes.c_uint32, 1),
        ('PeripheralEscapeModeEntryCommandError', ctypes.c_uint32, 1),
        ('PeripheralLowPowerTransmitSyncError', ctypes.c_uint32, 1),
        ('PeripheralTimeoutError', ctypes.c_uint32, 1),
        ('PeripheralFalseControlError', ctypes.c_uint32, 1),
        ('PeripheralContentionDetected', ctypes.c_uint32, 1),
        ('PeripheralSingleEccError', ctypes.c_uint32, 1),
        ('PeripheralMultiEccError', ctypes.c_uint32, 1),
        ('PeripheralChecksumError', ctypes.c_uint32, 1),
        ('InvalidDataType', ctypes.c_uint32, 1),
        ('InvalidVc', ctypes.c_uint32, 1),
        ('InvalidTxLength', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('ProtocolViolation', ctypes.c_uint32, 1),
        ('FrameUpdateDone', ctypes.c_uint32, 1),
        ('Spare18_17', ctypes.c_uint32, 2),
        ('HostEscapeModeEntryCommandError', ctypes.c_uint32, 1),
        ('HostLowPowerTransmitSyncError', ctypes.c_uint32, 1),
        ('HostTimeoutError', ctypes.c_uint32, 1),
        ('HostFalseControlError', ctypes.c_uint32, 1),
        ('HostContentionDetected', ctypes.c_uint32, 1),
        ('HostSingleEccError', ctypes.c_uint32, 1),
        ('HostMultiEccError', ctypes.c_uint32, 1),
        ('HostChecksumError', ctypes.c_uint32, 1),
        ('NonTeTriggerReceived', ctypes.c_uint32, 1),
        ('UlpsEntryDone', ctypes.c_uint32, 1),
        ('TxData', ctypes.c_uint32, 1),
        ('RxDataBtaTerminated', ctypes.c_uint32, 1),
        ('TeEvent', ctypes.c_uint32, 1),
    ]


class REG_DSI_INTER_IDENT_REG(ctypes.Union):
    value = 0
    offset = 0

    SotError = 0  # bit 0 to 1
    SotSyncError = 0  # bit 1 to 2
    EotSyncError = 0  # bit 2 to 3
    PeripheralEscapeModeEntryCommandError = 0  # bit 3 to 4
    PeripheralLowPowerTransmitSyncError = 0  # bit 4 to 5
    PeripheralTimeoutError = 0  # bit 5 to 6
    PeripheralFalseControlError = 0  # bit 6 to 7
    PeripheralContentionDetected = 0  # bit 7 to 8
    PeripheralSingleEccError = 0  # bit 8 to 9
    PeripheralMultiEccError = 0  # bit 9 to 10
    PeripheralChecksumError = 0  # bit 10 to 11
    InvalidDataType = 0  # bit 11 to 12
    InvalidVc = 0  # bit 12 to 13
    InvalidTxLength = 0  # bit 13 to 14
    Spare14 = 0  # bit 14 to 15
    ProtocolViolation = 0  # bit 15 to 16
    FrameUpdateDone = 0  # bit 16 to 17
    Spare18_17 = 0  # bit 17 to 19
    HostEscapeModeEntryCommandError = 0  # bit 19 to 20
    HostLowPowerTransmitSyncError = 0  # bit 20 to 21
    HostTimeoutError = 0  # bit 21 to 22
    HostFalseControlError = 0  # bit 22 to 23
    HostContentionDetected = 0  # bit 23 to 24
    HostSingleEccError = 0  # bit 24 to 25
    HostMultiEccError = 0  # bit 25 to 26
    HostChecksumError = 0  # bit 26 to 27
    NonTeTriggerReceived = 0  # bit 27 to 28
    UlpsEntryDone = 0  # bit 28 to 29
    TxData = 0  # bit 29 to 30
    RxDataBtaTerminated = 0  # bit 30 to 31
    TeEvent = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_INTER_IDENT_REG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_INTER_IDENT_REG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SOT_ERROR(Enum):
    SOT_ERROR_EVENT_UNMASKED = 0x0
    SOT_ERROR_EVENT_MASKED = 0x1


class ENUM_SOT_SYNC_ERROR(Enum):
    SOT_SYNC_ERROR_EVENT_UNMASKED = 0x0
    SOT_SYNC_ERROR_EVENT_MASKED = 0x1


class ENUM_EOT_SYNC_ERROR(Enum):
    EOT_SYNC_ERROR_EVENT_UNMASKED = 0x0
    EOT_SYNC_ERROR_EVENT_MASKED = 0x1


class ENUM_PERIPHERAL_ESCAPE_MODE_ENTRY_COMMAND_ERROR(Enum):
    PERIPHERAL_ESCAPE_MODE_ENTRY_COMMAND_ERROR_EVENT_UNMASKED = 0x0
    PERIPHERAL_ESCAPE_MODE_ENTRY_COMMAND_ERROR_EVENT_MASKED = 0x1


class ENUM_PERIPHERAL_LOW_POWER_TRANSMIT_SYNC_ERROR(Enum):
    PERIPHERAL_LOW_POWER_TRANSMIT_SYNC_ERROR_EVENT_UNMASKED = 0x0
    PERIPHERAL_LOW_POWER_TRANSMIT_SYNC_ERROR_EVENT_MASKED = 0x1


class ENUM_PERIPHERAL_TIMEOUT_ERROR(Enum):
    PERIPHERAL_TIMEOUT_ERROR_EVENT_UNMASKED = 0x0
    PERIPHERAL_TIMEOUT_ERROR_EVENT_MASKED = 0x1


class ENUM_PERIPHERAL_FALSE_CONTROL_ERROR(Enum):
    PERIPHERAL_FALSE_CONTROL_ERROR_EVENT_UNMASKED = 0x0
    PERIPHERAL_FALSE_CONTROL_ERROR_EVENT_MASKED = 0x1


class ENUM_PERIPHERAL_CONTENTION_DETECTED(Enum):
    PERIPHERAL_CONTENTION_DETECTED_EVENT_UNMASKED = 0x0
    PERIPHERAL_CONTENTION_DETECTED_EVENT_MASKED = 0x1


class ENUM_PERIPHERAL_SINGLE_ECC_ERROR(Enum):
    PERIPHERAL_SINGLE_ECC_ERROR_EVENT_UNMASKED = 0x0
    PERIPHERAL_SINGLE_ECC_ERROR_EVENT_MASKED = 0x1


class ENUM_PERIPHERAL_MULTI_ECC_ERROR(Enum):
    PERIPHERAL_MULTI_ECC_ERROR_EVENT_UNMASKED = 0x0
    PERIPHERAL_MULTI_ECC_ERROR_EVENT_MASKED = 0x1


class ENUM_PERIPHERAL_CHECKSUM_ERROR(Enum):
    PERIPHERAL_CHECKSUM_ERROR_EVENT_UNMASKED = 0x0
    PERIPHERAL_CHECKSUM_ERROR_EVENT_MASKED = 0x1


class ENUM_INVALID_DATA_TYPE(Enum):
    INVALID_DATA_TYPE_EVENT_UNMASKED = 0x0
    INVALID_DATA_TYPE_EVENT_MASKED = 0x1


class ENUM_INVALID_VC(Enum):
    INVALID_VC_EVENT_UNMASKED = 0x0
    INVALID_VC_EVENT_MASKED = 0x1


class ENUM_INVALID_TX_LENGTH(Enum):
    INVALID_TX_LENGTH_EVENT_UNMASKED = 0x0
    INVALID_TX_LENGTH_EVENT_MASKED = 0x1


class ENUM_PROTOCOL_VIOLATION(Enum):
    PROTOCOL_VIOLATION_EVENT_UNMASKED = 0x0
    PROTOCOL_VIOLATION_EVENT_MASKED = 0x1


class ENUM_FRAME_UPDATE_DONE(Enum):
    FRAME_UPDATE_DONE_EVENT_UNMASKED = 0x0
    FRAME_UPDATE_DONE_EVENT_MASKED = 0x1


class ENUM_HOST_ESCAPE_MODE_ENTRY_COMMAND_ERROR(Enum):
    HOST_ESCAPE_MODE_ENTRY_COMMAND_ERROR_EVENT_UNMASKED = 0x0
    HOST_ESCAPE_MODE_ENTRY_COMMAND_ERROR_EVENT_MASKED = 0x1


class ENUM_HOST_LOW_POWER_TRANSMIT_SYNC_ERROR(Enum):
    HOST_LOW_POWER_TRANSMIT_SYNC_ERROR_EVENT_UNMASKED = 0x0
    HOST_LOW_POWER_TRANSMIT_SYNC_ERROR_EVENT_MASKED = 0x1


class ENUM_HOST_TIMEOUT_ERROR(Enum):
    HOST_TIMEOUT_ERROR_EVENT_UNMASKED = 0x0
    HOST_TIMEOUT_ERROR_EVENT_MASKED = 0x1


class ENUM_HOST_FALSE_CONTROL_ERROR(Enum):
    HOST_FALSE_CONTROL_ERROR_EVENT_UNMASKED = 0x0
    HOST_FALSE_CONTROL_ERROR_EVENT_MASKED = 0x1


class ENUM_HOST_CONTENTION_DETECTED(Enum):
    HOST_CONTENTION_DETECTED_EVENT_UNMASKED = 0x0
    HOST_CONTENTION_DETECTED_EVENT_MASKED = 0x1


class ENUM_HOST_SINGLE_ECC_ERROR(Enum):
    HOST_SINGLE_ECC_ERROR_EVENT_UNMASKED = 0x0
    HOST_SINGLE_ECC_ERROR_EVENT_MASKED = 0x1


class ENUM_HOST_MULTI_ECC_ERROR(Enum):
    HOST_MULTI_ECC_ERROR_EVENT_UNMASKED = 0x0
    HOST_MULTI_ECC_ERROR_EVENT_MASKED = 0x1


class ENUM_HOST_CHECKSUM_ERROR(Enum):
    HOST_CHECKSUM_ERROR_EVENT_UNMASKED = 0x0
    HOST_CHECKSUM_ERROR_EVENT_MASKED = 0x1


class ENUM_NONTE_TRIGGER_RECEIVED(Enum):
    NONTE_TRIGGER_RECEIVED_EVENT_UNMASKED = 0x0
    NONTE_TRIGGER_RECEIVED_EVENT_MASKED = 0x1


class ENUM_ULPS_ENTRY_DONE(Enum):
    ULPS_ENTRY_DONE_EVENT_UNMASKED = 0x0
    ULPS_ENTRY_DONE_EVENT_MASKED = 0x1


class ENUM_TX_DATA(Enum):
    TX_DATA_EVENT_UNMASKED = 0x0
    TX_DATA_EVENT_MASKED = 0x1


class ENUM_RX_DATA_BTA_TERMINATED(Enum):
    RX_DATA_BTA_TERMINATED_EVENT_UNMASKED = 0x0
    RX_DATA_BTA_TERMINATED_EVENT_MASKED = 0x1


class ENUM_TE_EVENT(Enum):
    TE_EVENT_EVENT_UNMASKED = 0x0
    TE_EVENT_EVENT_MASKED = 0x1


class OFFSET_DSI_INTER_MSK_REG:
    DSI_INTER_MSK_REG_0 = 0x6B070
    DSI_INTER_MSK_REG_1 = 0x6B870


class _DSI_INTER_MSK_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SotError', ctypes.c_uint32, 1),
        ('SotSyncError', ctypes.c_uint32, 1),
        ('EotSyncError', ctypes.c_uint32, 1),
        ('PeripheralEscapeModeEntryCommandError', ctypes.c_uint32, 1),
        ('PeripheralLowPowerTransmitSyncError', ctypes.c_uint32, 1),
        ('PeripheralTimeoutError', ctypes.c_uint32, 1),
        ('PeripheralFalseControlError', ctypes.c_uint32, 1),
        ('PeripheralContentionDetected', ctypes.c_uint32, 1),
        ('PeripheralSingleEccError', ctypes.c_uint32, 1),
        ('PeripheralMultiEccError', ctypes.c_uint32, 1),
        ('PeripheralChecksumError', ctypes.c_uint32, 1),
        ('InvalidDataType', ctypes.c_uint32, 1),
        ('InvalidVc', ctypes.c_uint32, 1),
        ('InvalidTxLength', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('ProtocolViolation', ctypes.c_uint32, 1),
        ('FrameUpdateDone', ctypes.c_uint32, 1),
        ('Spare18_17', ctypes.c_uint32, 2),
        ('HostEscapeModeEntryCommandError', ctypes.c_uint32, 1),
        ('HostLowPowerTransmitSyncError', ctypes.c_uint32, 1),
        ('HostTimeoutError', ctypes.c_uint32, 1),
        ('HostFalseControlError', ctypes.c_uint32, 1),
        ('HostContentionDetected', ctypes.c_uint32, 1),
        ('HostSingleEccError', ctypes.c_uint32, 1),
        ('HostMultiEccError', ctypes.c_uint32, 1),
        ('HostChecksumError', ctypes.c_uint32, 1),
        ('NonTeTriggerReceived', ctypes.c_uint32, 1),
        ('UlpsEntryDone', ctypes.c_uint32, 1),
        ('TxData', ctypes.c_uint32, 1),
        ('RxDataBtaTerminated', ctypes.c_uint32, 1),
        ('TeEvent', ctypes.c_uint32, 1),
    ]


class REG_DSI_INTER_MSK_REG(ctypes.Union):
    value = 0
    offset = 0

    SotError = 0  # bit 0 to 1
    SotSyncError = 0  # bit 1 to 2
    EotSyncError = 0  # bit 2 to 3
    PeripheralEscapeModeEntryCommandError = 0  # bit 3 to 4
    PeripheralLowPowerTransmitSyncError = 0  # bit 4 to 5
    PeripheralTimeoutError = 0  # bit 5 to 6
    PeripheralFalseControlError = 0  # bit 6 to 7
    PeripheralContentionDetected = 0  # bit 7 to 8
    PeripheralSingleEccError = 0  # bit 8 to 9
    PeripheralMultiEccError = 0  # bit 9 to 10
    PeripheralChecksumError = 0  # bit 10 to 11
    InvalidDataType = 0  # bit 11 to 12
    InvalidVc = 0  # bit 12 to 13
    InvalidTxLength = 0  # bit 13 to 14
    Spare14 = 0  # bit 14 to 15
    ProtocolViolation = 0  # bit 15 to 16
    FrameUpdateDone = 0  # bit 16 to 17
    Spare18_17 = 0  # bit 17 to 19
    HostEscapeModeEntryCommandError = 0  # bit 19 to 20
    HostLowPowerTransmitSyncError = 0  # bit 20 to 21
    HostTimeoutError = 0  # bit 21 to 22
    HostFalseControlError = 0  # bit 22 to 23
    HostContentionDetected = 0  # bit 23 to 24
    HostSingleEccError = 0  # bit 24 to 25
    HostMultiEccError = 0  # bit 25 to 26
    HostChecksumError = 0  # bit 26 to 27
    NonTeTriggerReceived = 0  # bit 27 to 28
    UlpsEntryDone = 0  # bit 28 to 29
    TxData = 0  # bit 29 to 30
    RxDataBtaTerminated = 0  # bit 30 to 31
    TeEvent = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_INTER_MSK_REG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_INTER_MSK_REG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_COMBO_PHY_MODE(Enum):
    COMBO_PHY_MODE_DDI_MODE_NO_CLOCK_REQUEST = 0x0
    COMBO_PHY_MODE_MIPI_DSI_MODE_CLOCK_REQUEST = 0x1


class ENUM_HS_CLOCK_ACKNOWLEDGE(Enum):
    HS_CLOCK_ACKNOWLEDGE_NOT_ACKNOWLEDGED = 0x0
    HS_CLOCK_ACKNOWLEDGE_ACKNOWLEDGED = 0x1


class OFFSET_DSI_IO_MODECTL:
    DSI_IO_MODECTL_0 = 0x6B094
    DSI_IO_MODECTL_1 = 0x6B894


class _DSI_IO_MODECTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ComboPhyMode', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 7),
        ('HsClockAcknowledge', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 23),
    ]


class REG_DSI_IO_MODECTL(ctypes.Union):
    value = 0
    offset = 0

    ComboPhyMode = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 8
    HsClockAcknowledge = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_IO_MODECTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_IO_MODECTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_ULPS_TYPE(Enum):
    ULPS_TYPE_LP00 = 0x0  # Lanes will be left in the LP-00 state
    ULPS_TYPE_LP11 = 0x1  # Lanes will be left in the LP-11 state


class ENUM_TRIGGER_TYPE(Enum):
    TRIGGER_TYPE_RESET_TRIGGER = 0x0  # Entry Command [lsb:msb]: 01100010
    TRIGGER_TYPE_UNKNOWN_3 = 0x1  # Entry Command [lsb:msb]: 01011101
    TRIGGER_TYPE_UNKNOWN_4 = 0x2  # Entry Command [lsb:msb]: 00100001
    TRIGGER_TYPE_UNKNOWN_5 = 0x3  # Entry Command [lsb:msb]: 10100000


class ENUM_IN_ULPS(Enum):
    IN_ULPS_THE_DSI_LINK_IS_NOT_IN_ULPS = 0x0
    IN_ULPS_THE_DSI_LINK_IS_IN_ULPS = 0x1


class ENUM_LP_TX_IN_PROGRESS(Enum):
    LP_TX_IN_PROGRESS_TRANSCODER_IS_NOT_TRANSMITTING_IN_THE_LP_ESC_MODE = 0x0
    LP_TX_IN_PROGRESS_TRANSCODER_IS_TRANSMITTING_IN_THE_LP_ESC_MODE = 0x1


class ENUM_LINK_DIRECTION(Enum):
    LINK_DIRECTION_LINK_IS_IN_THE_FORWARD_DIRECTION = 0x0
    LINK_DIRECTION_LINK_IS_IN_THE_REVERSE_DIRECTION = 0x1


class OFFSET_DSI_LP_MSG:
    DSI_LP_MSG_0 = 0x6B0D8
    DSI_LP_MSG_1 = 0x6B8D8


class _DSI_LP_MSG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('UlpsEntry', ctypes.c_uint32, 1),
        ('BusTurnaround', ctypes.c_uint32, 1),
        ('TriggerMessage', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 5),
        ('UlpsType', ctypes.c_uint32, 1),
        ('TriggerType', ctypes.c_uint32, 2),
        ('Reserved11', ctypes.c_uint32, 5),
        ('InUlps', ctypes.c_uint32, 1),
        ('LpTxInProgress', ctypes.c_uint32, 1),
        ('LinkDirection', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 13),
    ]


class REG_DSI_LP_MSG(ctypes.Union):
    value = 0
    offset = 0

    UlpsEntry = 0  # bit 0 to 1
    BusTurnaround = 0  # bit 1 to 2
    TriggerMessage = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 8
    UlpsType = 0  # bit 8 to 9
    TriggerType = 0  # bit 9 to 11
    Reserved11 = 0  # bit 11 to 16
    InUlps = 0  # bit 16 to 17
    LpTxInProgress = 0  # bit 17 to 18
    LinkDirection = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_LP_MSG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_LP_MSG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_LRX_H_TO:
    DSI_LRX_H_TO_0 = 0x6B048
    DSI_LRX_H_TO_1 = 0x6B848


class _DSI_LRX_H_TO(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LpRx_HTimeout', ctypes.c_uint32, 16),
        ('Lrx_H_To', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_DSI_LRX_H_TO(ctypes.Union):
    value = 0
    offset = 0

    LpRx_HTimeout = 0  # bit 0 to 16
    Lrx_H_To = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_LRX_H_TO),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_LRX_H_TO, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_PWAIT_TO:
    DSI_PWAIT_TO_0 = 0x6B040
    DSI_PWAIT_TO_1 = 0x6B840


class _DSI_PWAIT_TO(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PeripheralResponseTimeout', ctypes.c_uint32, 16),
        ('PeripheralResetTimeout', ctypes.c_uint32, 16),
    ]


class REG_DSI_PWAIT_TO(ctypes.Union):
    value = 0
    offset = 0

    PeripheralResponseTimeout = 0  # bit 0 to 16
    PeripheralResetTimeout = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_PWAIT_TO),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_PWAIT_TO, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_CMD_RXHDR:
    DSI_CMD_RXHDR_0 = 0x6B0E0
    DSI_CMD_RXHDR_1 = 0x6B8E0


class _DSI_CMD_RXHDR(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ReceivedHeader', ctypes.c_uint32, 32),
    ]


class REG_DSI_CMD_RXHDR(ctypes.Union):
    value = 0
    offset = 0

    ReceivedHeader = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_CMD_RXHDR),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_CMD_RXHDR, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DSI_TA_TO:
    DSI_TA_TO_0 = 0x6B04C
    DSI_TA_TO_1 = 0x6B84C


class _DSI_TA_TO(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TurnaroundTimeout', ctypes.c_uint32, 16),
        ('Ta_To', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_DSI_TA_TO(ctypes.Union):
    value = 0
    offset = 0

    TurnaroundTimeout = 0  # bit 0 to 16
    Ta_To = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_TA_TO),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_TA_TO, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GLOBAL_UDLN_RESET_OVERRIDE_VALUE(Enum):
    GLOBAL_UDLN_RESET_OVERRIDE_VALUE_IN_RESET = 0x0  # Global UDLN reset is asserted, if override enabled
    GLOBAL_UDLN_RESET_OVERRIDE_VALUE_OUT_OF_RESET = 0x1  # Global UDLN reset is de-asserted, if override enabled


class ENUM_TXLP_LATCH_CONTROL_LOGIC_RESET_OVERRIDE_VALUE(Enum):
    TXLP_LATCH_CONTROL_LOGIC_RESET_OVERRIDE_VALUE_IN_RESET = 0x0  # Latch control logic reset is asserted, if override 
                                                                  # enabled
    TXLP_LATCH_CONTROL_LOGIC_RESET_OVERRIDE_VALUE_OUT_OF_RESET = 0x1  # Latch control logic reset is de-asserted, if ov
                                                                      # erride enabled


class ENUM_GLOBAL_UDLN_RESET_OVERRIDE_ENABLE(Enum):
    GLOBAL_UDLN_RESET_OVERRIDE_ENABLE_NOT_OVERRIDDEN = 0x0
    GLOBAL_UDLN_RESET_OVERRIDE_ENABLE_OVERRIDDEN = 0x1  # Global reset is overridden with DBBUDLN_SOFT_RST_CTL.udln_rst
                                                        # _ovr_val


class ENUM_TXLP_LATCH_CONTROL_LOGIC_RESET_OVERRIDE_ENABLE(Enum):
    TXLP_LATCH_CONTROL_LOGIC_RESET_OVERRIDE_ENABLE_NOT_OVERRIDDEN = 0x0
    TXLP_LATCH_CONTROL_LOGIC_RESET_OVERRIDE_ENABLE_OVERRIDDEN = 0x1  # Latch control logic reset is overridden with DBB
                                                                     # UDLN_SOFT_RST_CTL.txlp_latctl_rst_ovr_val


class OFFSET_DBBUDLN_SOFT_RST_CTL:
    DBBUDLN_SOFT_RST_CTL_DL0_B = 0x6C288
    DBBUDLN_SOFT_RST_CTL_DL1_B = 0x6C488
    DBBUDLN_SOFT_RST_CTL_DL2_B = 0x6C688
    DBBUDLN_SOFT_RST_CTL_DL3_B = 0x6C888
    DBBUDLN_SOFT_RST_CTL_DL4_B = 0x6CA88
    DBBUDLN_SOFT_RST_CTL_DL0_A = 0x162288
    DBBUDLN_SOFT_RST_CTL_DL1_A = 0x162488
    DBBUDLN_SOFT_RST_CTL_DL2_A = 0x162688
    DBBUDLN_SOFT_RST_CTL_DL3_A = 0x162888
    DBBUDLN_SOFT_RST_CTL_DL4_A = 0x162A88


class _DBBUDLN_SOFT_RST_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GlobalUdlnResetOverrideValue', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 4),
        ('TxlpLatchControlLogicResetOverrideValue', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 10),
        ('GlobalUdlnResetOverrideEnable', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 4),
        ('TxlpLatchControlLogicResetOverrideEnable', ctypes.c_uint32, 1),
        ('Reserved22', ctypes.c_uint32, 10),
    ]


class REG_DBBUDLN_SOFT_RST_CTL(ctypes.Union):
    value = 0
    offset = 0

    GlobalUdlnResetOverrideValue = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 5
    TxlpLatchControlLogicResetOverrideValue = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 16
    GlobalUdlnResetOverrideEnable = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 21
    TxlpLatchControlLogicResetOverrideEnable = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBBUDLN_SOFT_RST_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBBUDLN_SOFT_RST_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CLOCK_MCD_REQUEST_OVERRIDE_ENABLE(Enum):
    CLOCK_MCD_REQUEST_OVERRIDE_ENABLED = 0x0
    CLOCK_MCD_REQUEST_OVERRIDE_DISABLED = 0x1


class ENUM_DISABLE_CLOCK_MCD_REQACK_CHASSIS_COMPLIANCE(Enum):
    DISABLE_CLOCK_MCD_REQACK_CHASSIS_COMPLIANCE_ENABLED = 0x0
    DISABLE_CLOCK_MCD_REQACK_CHASSIS_COMPLIANCE_DISABLED = 0x1


class ENUM_CLOCK_PGL_REQUEST_OVERRIDE_ENABLE(Enum):
    CLOCK_PGL_REQUEST_OVERRIDE_ENABLED = 0x0
    CLOCK_PGL_REQUEST_OVERRIDE_DISABLED = 0x1


class ENUM_DISABLE_CLOCK_PGL_REQACK_CHASSIS_COMPLIANCE(Enum):
    DISABLE_CLOCK_PGL_REQACK_CHASSIS_COMPLIANCE_ENABLED = 0x0
    DISABLE_CLOCK_PGL_REQACK_CHASSIS_COMPLIANCE_DISABLED = 0x1


class ENUM_DFE_CLOCK_SELECT_OVERRIDE_ENABLE(Enum):
    DFE_CLOCK_SELECT_OVERRIDE_DISABLED = 0x0
    DFE_CLOCK_SELECT_OVERRIDE_ENABLED = 0x1


class ENUM_DFE_CLOCK_SELECT_OVERRIDE_VAL(Enum):
    DFE_CLOCK_SELECT_OVERRIDE_VAL_SOC_IS_NOT_SOURCE = 0x0
    DFE_CLOCK_SELECT_OVERRIDE_VAL_SOC_IS_THE_SOURCE = 0x1


class ENUM_HS_CLOCK_GATE_ENABLE(Enum):
    HS_CLOCK_GATE_DISABLED = 0x0
    HS_CLOCK_GATE_ENABLED = 0x1


class ENUM_HS_TX_WORD_CLOCK_DIVIDER(Enum):
    HS_TX_WORD_CLOCK_DIVIDER_DIVIDE_BY_1 = 0x0
    HS_TX_WORD_CLOCK_DIVIDER_DIVIDE_BY_2 = 0x1
    HS_TX_WORD_CLOCK_DIVIDER_DIVIDE_BY_4 = 0x2
    HS_TX_WORD_CLOCK_DIVIDER_DIVIDE_BY_8 = 0x3
    HS_TX_WORD_CLOCK_DIVIDER_DIVIDE_BY_16 = 0x4
    HS_TX_WORD_CLOCK_DIVIDER_DIVIDE_BY_32 = 0x5


class ENUM_HS_CLOCK_DISTRIBUTION_TO_RIGHT_ENABLE(Enum):
    HS_CLOCK_DISTRIBUTION_TO_RIGHT_DISABLED = 0x0
    HS_CLOCK_DISTRIBUTION_TO_RIGHT_ENABLED = 0x1


class ENUM_HS_CLOCK_DISTRIBUTION_TO_LEFT_ENABLE(Enum):
    HS_CLOCK_DISTRIBUTION_TO_LEFT_DISABLED = 0x0
    HS_CLOCK_DISTRIBUTION_TO_LEFT_ENABLED = 0x1


class ENUM_CRI_CLOCK_COUNT_MAX(Enum):
    CRI_CLOCK_COUNT_MAX_16_CYCLES = 0x0
    CRI_CLOCK_COUNT_MAX_32_CYCLES = 0x1
    CRI_CLOCK_COUNT_MAX_48_CYCLES = 0x2
    CRI_CLOCK_COUNT_MAX_63_CYCLES = 0x3


class ENUM_TX_WORD_CLOCK_GATE_DISABLE(Enum):
    TX_WORD_CLOCK_GATE_ENABLED = 0x0
    TX_WORD_CLOCK_GATE_DISABLED = 0x1


class ENUM_TX_ESCAPE_CLOCK_GATE_DISABLE(Enum):
    TX_ESCAPE_CLOCK_GATE_ENABLED = 0x0
    TX_ESCAPE_CLOCK_GATE_DISABLED = 0x1


class OFFSET_CBBS_CLOCK_CTRL_REG:
    CBBS_CLOCK_CTRL_REG_B = 0x6C030
    CBBS_CLOCK_CTRL_REG_A = 0x162030


class _CBBS_CLOCK_CTRL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ClockMcdRequestOverrideEnable', ctypes.c_uint32, 1),
        ('ClockMcdRequestOverrideValue', ctypes.c_uint32, 1),
        ('DisableClockMcdReqAckChassisCompliance', ctypes.c_uint32, 1),
        ('ClockPglRequestOverrideEnable', ctypes.c_uint32, 1),
        ('ClockPglRequestOverrideValue', ctypes.c_uint32, 1),
        ('DisableClockPglReqAckChassisCompliance', ctypes.c_uint32, 1),
        ('DfeClockSelectOverrideEnable', ctypes.c_uint32, 1),
        ('DfeClockSelectOverrideVal', ctypes.c_uint32, 1),
        ('HsClockGateEnable', ctypes.c_uint32, 1),
        ('DfeClockDivider', ctypes.c_uint32, 6),
        ('HsTxWordClockDivider', ctypes.c_uint32, 4),
        ('EscapeClockDivider_Optional', ctypes.c_uint32, 7),
        ('HsClockDistributionToRightEnable', ctypes.c_uint32, 1),
        ('HsClockDistributionToLeftEnable', ctypes.c_uint32, 1),
        ('CriClockCountMax', ctypes.c_uint32, 2),
        ('TxWordClockGateDisable', ctypes.c_uint32, 1),
        ('TxEscapeClockGateDisable', ctypes.c_uint32, 1),
    ]


class REG_CBBS_CLOCK_CTRL_REG(ctypes.Union):
    value = 0
    offset = 0

    ClockMcdRequestOverrideEnable = 0  # bit 0 to 1
    ClockMcdRequestOverrideValue = 0  # bit 1 to 2
    DisableClockMcdReqAckChassisCompliance = 0  # bit 2 to 3
    ClockPglRequestOverrideEnable = 0  # bit 3 to 4
    ClockPglRequestOverrideValue = 0  # bit 4 to 5
    DisableClockPglReqAckChassisCompliance = 0  # bit 5 to 6
    DfeClockSelectOverrideEnable = 0  # bit 6 to 7
    DfeClockSelectOverrideVal = 0  # bit 7 to 8
    HsClockGateEnable = 0  # bit 8 to 9
    DfeClockDivider = 0  # bit 9 to 15
    HsTxWordClockDivider = 0  # bit 15 to 19
    EscapeClockDivider_Optional = 0  # bit 19 to 26
    HsClockDistributionToRightEnable = 0  # bit 26 to 27
    HsClockDistributionToLeftEnable = 0  # bit 27 to 28
    CriClockCountMax = 0  # bit 28 to 30
    TxWordClockGateDisable = 0  # bit 30 to 31
    TxEscapeClockGateDisable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CBBS_CLOCK_CTRL_REG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CBBS_CLOCK_CTRL_REG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TXLP_LATCH_OPEN_OVERRIDE_VALUE(Enum):
    TXLP_LATCH_OPEN_OVERRIDE_VALUE_LATCHES_CLOSED = 0x0
    TXLP_LATCH_OPEN_OVERRIDE_VALUE_LATCHES_OPEN = 0x1


class ENUM_TXLP_LATCH_OPEN_OVERRIDE_ENABLE(Enum):
    TXLP_LATCH_OPEN_OVERRIDE_ENABLE_LATCHES_CONTROLLED_BY_HW = 0x0
    TXLP_LATCH_OPEN_OVERRIDE_ENABLE_LATCHES_CONTROLLED_BY_SW = 0x1


class ENUM_CONNECTIVITY_IO_MODE(Enum):
    CONNECTIVITY_IO_MODE_DISABLED = 0x0
    CONNECTIVITY_IO_MODE_ENABLED = 0x1


class OFFSET_DBBSUPAR_TXRXLP_AFE_CTL:
    DBBSUPAR_TXRXLP_AFE_CTL_DL0_B = 0x6C318
    DBBSUPAR_TXRXLP_AFE_CTL_DL1_B = 0x6C518
    DBBSUPAR_TXRXLP_AFE_CTL_DL2_B = 0x6C718
    DBBSUPAR_TXRXLP_AFE_CTL_DL3_B = 0x6C918
    DBBSUPAR_TXRXLP_AFE_CTL_DL4_B = 0x6CB18
    DBBSUPAR_TXRXLP_AFE_CTL_DL0_A = 0x162318
    DBBSUPAR_TXRXLP_AFE_CTL_DL1_A = 0x162518
    DBBSUPAR_TXRXLP_AFE_CTL_DL2_A = 0x162718
    DBBSUPAR_TXRXLP_AFE_CTL_DL3_A = 0x162918
    DBBSUPAR_TXRXLP_AFE_CTL_DL4_A = 0x162B18


class _DBBSUPAR_TXRXLP_AFE_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LpcdThreshold', ctypes.c_uint32, 4),
        ('ContentionDetectorEnable', ctypes.c_uint32, 1),
        ('TxlpLatchOpenOverrideValue', ctypes.c_uint32, 1),
        ('TxlpLatchOpenOverrideEnable', ctypes.c_uint32, 1),
        ('LpTxPStaticLegDisable', ctypes.c_uint32, 1),
        ('LpTxNStaticLegDisable', ctypes.c_uint32, 1),
        ('LpTxDriverSelect', ctypes.c_uint32, 4),
        ('ConnectivityIoMode', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 18),
    ]


class REG_DBBSUPAR_TXRXLP_AFE_CTL(ctypes.Union):
    value = 0
    offset = 0

    LpcdThreshold = 0  # bit 0 to 4
    ContentionDetectorEnable = 0  # bit 4 to 5
    TxlpLatchOpenOverrideValue = 0  # bit 5 to 6
    TxlpLatchOpenOverrideEnable = 0  # bit 6 to 7
    LpTxPStaticLegDisable = 0  # bit 7 to 8
    LpTxNStaticLegDisable = 0  # bit 8 to 9
    LpTxDriverSelect = 0  # bit 9 to 13
    ConnectivityIoMode = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBBSUPAR_TXRXLP_AFE_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBBSUPAR_TXRXLP_AFE_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DBBUDLN_MST_SLV_INIT_CTL:
    DBBUDLN_MST_SLV_INIT_CTL_DL0_B = 0x6C294
    DBBUDLN_MST_SLV_INIT_CTL_DL1_B = 0x6C494
    DBBUDLN_MST_SLV_INIT_CTL_DL2_B = 0x6C694
    DBBUDLN_MST_SLV_INIT_CTL_DL3_B = 0x6C894
    DBBUDLN_MST_SLV_INIT_CTL_DL4_B = 0x6CA94
    DBBUDLN_MST_SLV_INIT_CTL_DL0_A = 0x162294
    DBBUDLN_MST_SLV_INIT_CTL_DL1_A = 0x162494
    DBBUDLN_MST_SLV_INIT_CTL_DL2_A = 0x162694
    DBBUDLN_MST_SLV_INIT_CTL_DL3_A = 0x162894
    DBBUDLN_MST_SLV_INIT_CTL_DL4_A = 0x162A94


class _DBBUDLN_MST_SLV_INIT_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MasterSlaveInitTimerConfiguration', ctypes.c_uint32, 12),
        ('Reserved12', ctypes.c_uint32, 4),
        ('UdlnReadyTimer', ctypes.c_uint32, 3),
        ('Reserved19', ctypes.c_uint32, 13),
    ]


class REG_DBBUDLN_MST_SLV_INIT_CTL(ctypes.Union):
    value = 0
    offset = 0

    MasterSlaveInitTimerConfiguration = 0  # bit 0 to 12
    Reserved12 = 0  # bit 12 to 16
    UdlnReadyTimer = 0  # bit 16 to 19
    Reserved19 = 0  # bit 19 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBBUDLN_MST_SLV_INIT_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBBUDLN_MST_SLV_INIT_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DBBUDLN_TX_TIMING_CTL0:
    DBBUDLN_TX_TIMING_CTL0_DL0_B = 0x6C298
    DBBUDLN_TX_TIMING_CTL0_DL1_B = 0x6C498
    DBBUDLN_TX_TIMING_CTL0_DL2_B = 0x6C698
    DBBUDLN_TX_TIMING_CTL0_DL3_B = 0x6C898
    DBBUDLN_TX_TIMING_CTL0_DL4_B = 0x6CA98
    DBBUDLN_TX_TIMING_CTL0_DL0_A = 0x162298
    DBBUDLN_TX_TIMING_CTL0_DL1_A = 0x162498
    DBBUDLN_TX_TIMING_CTL0_DL2_A = 0x162698
    DBBUDLN_TX_TIMING_CTL0_DL3_A = 0x162898
    DBBUDLN_TX_TIMING_CTL0_DL4_A = 0x162A98


class _DBBUDLN_TX_TIMING_CTL0(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HsReqTimer', ctypes.c_uint32, 8),
        ('TprepareTimer', ctypes.c_uint32, 8),
        ('TzeroTimer', ctypes.c_uint32, 8),
        ('TtrailTimer', ctypes.c_uint32, 8),
    ]


class REG_DBBUDLN_TX_TIMING_CTL0(ctypes.Union):
    value = 0
    offset = 0

    HsReqTimer = 0  # bit 0 to 8
    TprepareTimer = 0  # bit 8 to 16
    TzeroTimer = 0  # bit 16 to 24
    TtrailTimer = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBBUDLN_TX_TIMING_CTL0),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBBUDLN_TX_TIMING_CTL0, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TXHS_EARLY_PPI_READY_GENERATION_ENABLE(Enum):
    TXHS_EARLY_PPI_READY_GENERATION_DISABLED = 0x0
    TXHS_EARLY_PPI_READY_GENERATION_ENABLED = 0x1


class OFFSET_DBBUDLN_TX_TIMING_CTL1:
    DBBUDLN_TX_TIMING_CTL1_DL0_B = 0x6C29C
    DBBUDLN_TX_TIMING_CTL1_DL1_B = 0x6C49C
    DBBUDLN_TX_TIMING_CTL1_DL2_B = 0x6C69C
    DBBUDLN_TX_TIMING_CTL1_DL3_B = 0x6C89C
    DBBUDLN_TX_TIMING_CTL1_DL4_B = 0x6CA9C
    DBBUDLN_TX_TIMING_CTL1_DL0_A = 0x16229C
    DBBUDLN_TX_TIMING_CTL1_DL1_A = 0x16249C
    DBBUDLN_TX_TIMING_CTL1_DL2_A = 0x16269C
    DBBUDLN_TX_TIMING_CTL1_DL3_A = 0x16289C
    DBBUDLN_TX_TIMING_CTL1_DL4_A = 0x162A9C


class _DBBUDLN_TX_TIMING_CTL1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ThsexitTimer', ctypes.c_uint32, 8),
        ('Tclk_PostTimer', ctypes.c_uint32, 8),
        ('Tclk_PreTimer', ctypes.c_uint32, 8),
        ('TxhsEarlyPpiReadyGenerationTimer', ctypes.c_uint32, 3),
        ('TxhsEarlyPpiReadyGenerationEnable', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_DBBUDLN_TX_TIMING_CTL1(ctypes.Union):
    value = 0
    offset = 0

    ThsexitTimer = 0  # bit 0 to 8
    Tclk_PostTimer = 0  # bit 8 to 16
    Tclk_PreTimer = 0  # bit 16 to 24
    TxhsEarlyPpiReadyGenerationTimer = 0  # bit 24 to 27
    TxhsEarlyPpiReadyGenerationEnable = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBBUDLN_TX_TIMING_CTL1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBBUDLN_TX_TIMING_CTL1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TX_HS_AUTO_INITIAL_DESKEW_ENABLE(Enum):
    TX_HS_AUTO_INITIAL_DESKEW_DISABLED = 0x0
    TX_HS_AUTO_INITIAL_DESKEW_ENABLED = 0x1


class OFFSET_DBBUDLN_TX_TIMING_CTL2:
    DBBUDLN_TX_TIMING_CTL2_DL0_B = 0x6C2A0
    DBBUDLN_TX_TIMING_CTL2_DL1_B = 0x6C4A0
    DBBUDLN_TX_TIMING_CTL2_DL2_B = 0x6C6A0
    DBBUDLN_TX_TIMING_CTL2_DL3_B = 0x6C8A0
    DBBUDLN_TX_TIMING_CTL2_DL4_B = 0x6CAA0
    DBBUDLN_TX_TIMING_CTL2_DL0_A = 0x1622A0
    DBBUDLN_TX_TIMING_CTL2_DL1_A = 0x1624A0
    DBBUDLN_TX_TIMING_CTL2_DL2_A = 0x1626A0
    DBBUDLN_TX_TIMING_CTL2_DL3_A = 0x1628A0
    DBBUDLN_TX_TIMING_CTL2_DL4_A = 0x162AA0


class _DBBUDLN_TX_TIMING_CTL2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TxHsMasterOffTimer', ctypes.c_uint32, 8),
        ('TxHsAutoInitialDeskewTimer', ctypes.c_uint32, 8),
        ('TxHsAlternativeSkewTimer', ctypes.c_uint32, 8),
        ('TxHsPreambleTimer', ctypes.c_uint32, 5),
        ('TxHsAutoInitialDeskewEnable', ctypes.c_uint32, 1),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_DBBUDLN_TX_TIMING_CTL2(ctypes.Union):
    value = 0
    offset = 0

    TxHsMasterOffTimer = 0  # bit 0 to 8
    TxHsAutoInitialDeskewTimer = 0  # bit 8 to 16
    TxHsAlternativeSkewTimer = 0  # bit 16 to 24
    TxHsPreambleTimer = 0  # bit 24 to 29
    TxHsAutoInitialDeskewEnable = 0  # bit 29 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBBUDLN_TX_TIMING_CTL2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBBUDLN_TX_TIMING_CTL2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DBBUDLN_TX_TIMING_CTL3:
    DBBUDLN_TX_TIMING_CTL3_DL0_B = 0x6C2A4
    DBBUDLN_TX_TIMING_CTL3_DL1_B = 0x6C4A4
    DBBUDLN_TX_TIMING_CTL3_DL2_B = 0x6C6A4
    DBBUDLN_TX_TIMING_CTL3_DL3_B = 0x6C8A4
    DBBUDLN_TX_TIMING_CTL3_DL4_B = 0x6CAA4
    DBBUDLN_TX_TIMING_CTL3_DL0_A = 0x1622A4
    DBBUDLN_TX_TIMING_CTL3_DL1_A = 0x1624A4
    DBBUDLN_TX_TIMING_CTL3_DL2_A = 0x1626A4
    DBBUDLN_TX_TIMING_CTL3_DL3_A = 0x1628A4
    DBBUDLN_TX_TIMING_CTL3_DL4_A = 0x162AA4


class _DBBUDLN_TX_TIMING_CTL3(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TlpxTimer', ctypes.c_uint32, 8),
        ('TxLpTurnAroundGoTimer', ctypes.c_uint32, 8),
        ('TxLpTurnAroundGetTimer', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_DBBUDLN_TX_TIMING_CTL3(ctypes.Union):
    value = 0
    offset = 0

    TlpxTimer = 0  # bit 0 to 8
    TxLpTurnAroundGoTimer = 0  # bit 8 to 16
    TxLpTurnAroundGetTimer = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBBUDLN_TX_TIMING_CTL3),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBBUDLN_TX_TIMING_CTL3, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_LOW_POWER_FILTER_ENABLE(Enum):
    LOW_POWER_FILTER_DISABLED = 0x0
    LOW_POWER_FILTER_ENABLED = 0x1


class ENUM_TRIGGER_ORDER(Enum):
    TRIGGER_ORDER_NORMAL_ORDER = 0x0  # TriggerEsc[0]: Reset TriggerEsc[1]: Entry HS Test Mode TriggerEsc[2]: Unknown-4
                                      #  TriggerEsc[3]: Unknown-5
    TRIGGER_ORDER_REVERSE_ORDER = 0x1  # TriggerEsc[0]:Unknown-5 TriggerEsc[1]: Unknown-4 TriggerEsc[2]:Entry HS Test M
                                       # ode TriggerEsc[3]: Reset


class ENUM_PREAMPLE_ENABLE(Enum):
    PREAMPLE_DISABLED = 0x0
    PREAMPLE_ENABLED = 0x1


class ENUM_TX_HS_PREAMBLE_PATTERN_INVERT(Enum):
    TX_HS_PREAMBLE_PATTERN_INVERT_AAH_PATTERN = 0x0
    TX_HS_PREAMBLE_PATTERN_INVERT_55H_PATTERN = 0x1


class ENUM_ALTERNATE_SKEW_CALIBRATION_ENABLE(Enum):
    ALTERNATE_SKEW_CALIBRATION_DISABLED = 0x0
    ALTERNATE_SKEW_CALIBRATION_ENABLED = 0x1


class ENUM_TX_HS_SKEW_CALIBRATION_PATTERN_INVERT(Enum):
    TX_HS_SKEW_CALIBRATION_PATTERN_INVERT_AAH_PATTERN = 0x0
    TX_HS_SKEW_CALIBRATION_PATTERN_INVERT_55H_PATTERN = 0x1


class ENUM_TX_HS_CLOCK_PATTERN_INVERT(Enum):
    TX_HS_CLOCK_PATTERN_INVERT_AAH_PATTERN = 0x0
    TX_HS_CLOCK_PATTERN_INVERT_55H_PATTERN = 0x1


class ENUM_PORT_TX_STOPSTATE_ENABLE(Enum):
    PORT_TX_STOPSTATE_ENABLE_INDEPENDENT = 0x0
    PORT_TX_STOPSTATE_ENABLE_COMBINED = 0x1


class ENUM_RX_HS_DESKEW_CALIBRATION_ENABLE_ENABLE(Enum):
    RX_HS_DESKEW_CALIBRATION_ENABLE_DISABLED = 0x0  # DPHY RXHS Deskew Calibration Detection is not enabled
    RX_HS_DESKEW_CALIBRATION_ENABLE_ENABLED = 0x1  # DPHY RXHS Deskew Calibration Detection is enabled


class ENUM_RX_LOW_POWER_SIGNALING_FILTER_ENABLE(Enum):
    RX_LOW_POWER_SIGNALING_FILTER_DISABLED = 0x0  # Rx Low power signaling is synchronized to DFE clock but not 
                                                         # filtered for potential glitches.
    RX_LOW_POWER_SIGNALING_FILTER_ENABLED = 0x1  # Rx Low power signaling is synchronized to DFE clock and filte
                                                        # red for potential glitches, by ensuring LP states remain in
                                                        # same state for two dfe clock cycles before declaring the LP
                                                        # state.


class ENUM_RX_STOP_STATE_MODE(Enum):
    RX_STOP_STATE_MODE_REAL_TIME_MODE = 0x0  # PPI Rx StopState is a real time signal reflecting the actual LP bus stat
                                             # e
    RX_STOP_STATE_MODE_NON_REAL_TIME_MODE = 0x1  # PPI Rx StopState is not a real time signal, instead it will be set e
                                                 # very time PPI Rx Active is low. Note, by using this mode the Rx
                                                 # escape modes are not supported


class ENUM_PPI_STATUS_CLEAR(Enum):
    PPI_STATUS_CLEAR_DON_T_CLEAR_STICKY_BITS = 0x0
    PPI_STATUS_CLEAR_CLEAR_STICKY_BITS = 0x1


class ENUM_ERROR_STATUS_CLEAR(Enum):
    ERROR_STATUS_CLEAR_DON_T_CLEAR_STICKY_BITS = 0x0
    ERROR_STATUS_CLEAR_CLEAR_STICKY_BITS = 0x1


class OFFSET_DBBUDLN_TXRX_CTL:
    DBBUDLN_TXRX_CTL_DL0_B = 0x6C290
    DBBUDLN_TXRX_CTL_DL1_B = 0x6C490
    DBBUDLN_TXRX_CTL_DL2_B = 0x6C690
    DBBUDLN_TXRX_CTL_DL3_B = 0x6C890
    DBBUDLN_TXRX_CTL_DL4_B = 0x6CA90
    DBBUDLN_TXRX_CTL_DL0_A = 0x162290
    DBBUDLN_TXRX_CTL_DL1_A = 0x162490
    DBBUDLN_TXRX_CTL_DL2_A = 0x162690
    DBBUDLN_TXRX_CTL_DL3_A = 0x162890
    DBBUDLN_TXRX_CTL_DL4_A = 0x162A90


class _DBBUDLN_TXRX_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LowPowerFilterEnable', ctypes.c_uint32, 1),
        ('LowPowerFilterTimer', ctypes.c_uint32, 3),
        ('TriggerOrder', ctypes.c_uint32, 1),
        ('PreampleEnable', ctypes.c_uint32, 1),
        ('TxHsPreamblePatternInvert', ctypes.c_uint32, 1),
        ('AlternateSkewCalibrationEnable', ctypes.c_uint32, 1),
        ('TxHsSkewCalibrationPatternInvert', ctypes.c_uint32, 1),
        ('TxHsClockPatternInvert', ctypes.c_uint32, 1),
        ('PortTxStopstateEnable', ctypes.c_uint32, 1),
        ('RxHsDeskewCalibrationEnableEnable', ctypes.c_uint32, 1),
        ('RxLowPowerSignalingFilterEnable', ctypes.c_uint32, 1),
        ('RxStopStateMode', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 16),
        ('PpiStatusClear', ctypes.c_uint32, 1),
        ('ErrorStatusClear', ctypes.c_uint32, 1),
    ]


class REG_DBBUDLN_TXRX_CTL(ctypes.Union):
    value = 0
    offset = 0

    LowPowerFilterEnable = 0  # bit 0 to 1
    LowPowerFilterTimer = 0  # bit 1 to 4
    TriggerOrder = 0  # bit 4 to 5
    PreampleEnable = 0  # bit 5 to 6
    TxHsPreamblePatternInvert = 0  # bit 6 to 7
    AlternateSkewCalibrationEnable = 0  # bit 7 to 8
    TxHsSkewCalibrationPatternInvert = 0  # bit 8 to 9
    TxHsClockPatternInvert = 0  # bit 9 to 10
    PortTxStopstateEnable = 0  # bit 10 to 11
    RxHsDeskewCalibrationEnableEnable = 0  # bit 11 to 12
    RxLowPowerSignalingFilterEnable = 0  # bit 12 to 13
    RxStopStateMode = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 30
    PpiStatusClear = 0  # bit 30 to 31
    ErrorStatusClear = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DBBUDLN_TXRX_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DBBUDLN_TXRX_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DSI_BLOCK(Enum):
    DSI_BLOCK_NO_BLOCKING = 0x0
    DSI_BLOCK_BLOCKING = 0x1


class ENUM_DSI_DCCO_ALLOWED(Enum):
    DSI_DCCO_ALLOWED_NOT_ALLOWED = 0x0
    DSI_DCCO_ALLOWED_ALLOWED = 0x1


class OFFSET_DSI_DCSTATE_CTL:
    DSI_DCSTATE_CTL = 0x6B038


class _DSI_DCSTATE_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DsiBlock', ctypes.c_uint32, 1),
        ('DsiIdle', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 29),
        ('DsiDccoAllowed', ctypes.c_uint32, 1),
    ]


class REG_DSI_DCSTATE_CTL(ctypes.Union):
    value = 0
    offset = 0

    DsiBlock = 0  # bit 0 to 1
    DsiIdle = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 31
    DsiDccoAllowed = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DSI_DCSTATE_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DSI_DCSTATE_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

