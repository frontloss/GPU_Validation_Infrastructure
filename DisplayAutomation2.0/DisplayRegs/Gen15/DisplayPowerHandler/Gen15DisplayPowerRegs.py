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
# @file Gen15DisplayPowerRegs.py
# @brief contains Gen15DisplayPowerRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_DC_STATE_SELECT(Enum):
    DC_STATE_SELECT_0 = 0x0
    DC_STATE_SELECT_1 = 0x1
    DC_STATE_SELECT_2 = 0x2
    DC_STATE_SELECT_3 = 0x3
    DC_STATE_SELECT_4 = 0x4
    DC_STATE_SELECT_5 = 0x5
    DC_STATE_SELECT_6 = 0x6
    DC_STATE_SELECT_7 = 0x7
    DC_STATE_SELECT_8_DC6V = 0x8


class OFFSET_DC_STATE_SEL:
    DC_STATE_SEL = 0x45500

class _DC_STATE_SEL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DcStateSelect', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 28),
    ]


class REG_DC_STATE_SEL(ctypes.Union):
    value = 0
    offset = 0

    DcStateSelect = 0  # bit 0 to 3
    Reserved4 = 0  # bit 4 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DC_STATE_SEL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DC_STATE_SEL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DYNAMIC_DC_STATE_ENABLE(Enum):
    DYNAMIC_DC_STATE_DISABLE = 0x0
    DYNAMIC_DC_STATE_ENABLE_UP_TO_DC5 = 0x1
    DYNAMIC_DC_STATE_ENABLE_UP_TO_DC6 = 0x2
    DYNAMIC_DC_STATE_ENABLE_DC6V = 0x3


class ENUM_DC9_ALLOW(Enum):
    DC9_ALLOW_DO_NOT_ALLOW = 0x0
    DC9_ALLOW_ALLOW = 0x1


class ENUM_MASK_POKE(Enum):
    MASK_POKE_UNMASK = 0x0
    MASK_POKE_MASK = 0x1


class ENUM_DC6V_BACKWARD_COMPATIBILITY(Enum):
    DC6V_BACKWARD_COMPATIBILITY_DISABLE = 0x0
    DC6V_BACKWARD_COMPATIBILITY_ENABLE = 0x1


class ENUM_BLOCK_OUTBOUND_TRAFFIC(Enum):
    BLOCK_OUTBOUND_TRAFFIC_DO_NOT_BLOCK = 0x0
    BLOCK_OUTBOUND_TRAFFIC_BLOCK = 0x1


class ENUM_IN_CSR_FLOW(Enum):
    IN_CSR_FLOW_NOT_IN_CSR = 0x0
    IN_CSR_FLOW_IN_CSR = 0x1


class ENUM_MIPI_ENABLED_STATUS(Enum):
    MIPI_ENABLED_STATUS_MIPI_DISABLED = 0x0
    MIPI_ENABLED_STATUS_MIPI_ENABLED = 0x1


class ENUM_DISPLAY_DCCO_STATE_STATUS_DSI(Enum):
    DISPLAY_DCCO_STATE_STATUS_DSI_DMC_DCCO_EXIT_COMPLETED_FOR_DSI = 0x1


class ENUM_DISPLAY_CLOCK_OFF_ENABLE_DSI(Enum):
    DISPLAY_CLOCK_OFF_ENABLE_DSI_DCCO_IS_DISALLOWED_FOR_DSI = 0x0
    DISPLAY_CLOCK_OFF_ENABLE_DSI_DCCO_IS_ALLOWED_FOR_DSI = 0x1


class ENUM_DSI_PLLS_TURN_OFF_DISALLOWED(Enum):
    DSI_PLLS_TURN_OFF_DISALLOWED_DSI_PLLS_TURN_OFF_ALLOWED = 0x0
    DSI_PLLS_TURN_OFF_DISALLOWED_DSI_PLLS_TURN_OFF_DISALLOWED = 0x1


class ENUM_DISPLAY_DCCO_STATE_STATUS_EDP(Enum):
    DISPLAY_DCCO_STATE_STATUS_EDP_DMC_DCCO_EXIT_COMPLETED_FOR_EDP = 0x1


class ENUM_DISPLAY_CLOCK_OFF_ENABLE_EDP(Enum):
    DISPLAY_CLOCK_OFF_ENABLE_EDP_DCCO_IS_DISALLOWED_FOR_EDP = 0x0
    DISPLAY_CLOCK_OFF_ENABLE_EDP_DCCO_IS_ALLOWED_FOR_EDP = 0x1


class ENUM_MODE_SET_IN_PROGRESS(Enum):
    MODE_SET_IN_PROGRESS_CSR_START_GENERATION_NOT_GATED = 0x0
    MODE_SET_IN_PROGRESS_CSR_START_GENERATION_IS_GATED = 0x1


class OFFSET_DC_STATE_EN:
    DC_STATE_EN = 0x45504

class _DC_STATE_EN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DynamicDcStateEnable', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('Dc9Allow', ctypes.c_uint32, 1),
        ('MaskPoke', ctypes.c_uint32, 1),
        ('Dc6VBackwardCompatibility', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('BlockOutboundTraffic', ctypes.c_uint32, 1),
        ('InCsrFlow', ctypes.c_uint32, 1),
        ('CsrMask', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 5),
        ('LongLatencyToleranceIndicator', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 3),
        ('Reserved20', ctypes.c_uint32, 2),
        ('Reserved22', ctypes.c_uint32, 2),
        ('Dc5Abort', ctypes.c_uint32, 1),
        ('MipiEnabledStatus', ctypes.c_uint32, 1),
        ('DisplayDcCoStateStatusDsi', ctypes.c_uint32, 1),
        ('DisplayClockOffEnableDsi', ctypes.c_uint32, 1),
        ('DsiPllsTurnOffDisallowed', ctypes.c_uint32, 1),
        ('DisplayDcCoStateStatusEdp', ctypes.c_uint32, 1),
        ('DisplayClockOffEnableEdp', ctypes.c_uint32, 1),
        ('ModeSetInProgress', ctypes.c_uint32, 1),
    ]


class REG_DC_STATE_EN(ctypes.Union):
    value = 0
    offset = 0

    DynamicDcStateEnable = 0  # bit 0 to 1
    Reserved2 = 0  # bit 2 to 2
    Dc9Allow = 0  # bit 3 to 3
    MaskPoke = 0  # bit 4 to 4
    Dc6VBackwardCompatibility = 0  # bit 5 to 5
    Reserved6 = 0  # bit 6 to 7
    BlockOutboundTraffic = 0  # bit 8 to 8
    InCsrFlow = 0  # bit 9 to 9
    CsrMask = 0  # bit 10 to 10
    Reserved11 = 0  # bit 11 to 15
    LongLatencyToleranceIndicator = 0  # bit 16 to 16
    Reserved17 = 0  # bit 17 to 19
    Reserved20 = 0  # bit 20 to 21
    Reserved22 = 0  # bit 22 to 23
    Dc5Abort = 0  # bit 24 to 24
    MipiEnabledStatus = 0  # bit 25 to 25
    DisplayDcCoStateStatusDsi = 0  # bit 26 to 26
    DisplayClockOffEnableDsi = 0  # bit 27 to 27
    DsiPllsTurnOffDisallowed = 0  # bit 28 to 28
    DisplayDcCoStateStatusEdp = 0  # bit 29 to 29
    DisplayClockOffEnableEdp = 0  # bit 30 to 30
    ModeSetInProgress = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DC_STATE_EN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DC_STATE_EN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_MASK_CORES(Enum):
    MASK_CORES_DO_NOT_MASK = 0x0  # Wait until cores are idle before starting CSR
    MASK_CORES_MASK = 0x1  # Do not wait until cores are idle before starting CSR


class ENUM_MASK_MEMORY_UP(Enum):
    MASK_MEMORY_UP_DO_NOT_MASK = 0x0  # Wait until memory up is deasserted before starting CSR
    MASK_MEMORY_UP_MASK = 0x1  # Do not wait until memory up is deasserted before starting CSR


class OFFSET_DC_STATE_DEBUG:
    DC_STATE_DEBUG = 0x45520

class _DC_STATE_DEBUG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('MaskCores', ctypes.c_uint32, 1),
        ('MaskMemoryUp', ctypes.c_uint32, 1),
        ('Reserved2', ctypes.c_uint32, 30),
    ]


class REG_DC_STATE_DEBUG(ctypes.Union):
    value = 0
    offset = 0

    MaskCores = 0  # bit 0 to 0
    MaskMemoryUp = 0  # bit 1 to 1
    Reserved2 = 0  # bit 2 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DC_STATE_DEBUG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DC_STATE_DEBUG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PIPE_A_B_SELECT(Enum):
    PIPE_A_B_SELECT_PIPE_A_AND_PIPEB = 0x3
    PIPE_A_B_SELECT_PIPEA_ONLY = 0x1
    PIPE_A_B_SELECT_PIPEB_ONLY = 0x2


class OFFSET_DC_STATE_PIPE_SEL:
    DC_STATE_PIPE_SEL = 0x452C0

class _DC_STATE_PIPE_SEL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PipeABSelect', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 30),
    ]


class REG_DC_STATE_PIPE_SEL(ctypes.Union):
    value = 0
    offset = 0

    PipeABSelect = 0  # bit 0 to 1
    Reserved2 = 0  # bit 2 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DC_STATE_PIPE_SEL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DC_STATE_PIPE_SEL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_SCANLINE_GB1:
    SCANLINE_GB1_A = 0x456A0
    SCANLINE_GB1_B = 0x456C0

class _SCANLINE_GB1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Lowerboundguardband1', ctypes.c_uint32, 20),
        ('Reserved20', ctypes.c_uint32, 12),
        ('Upperboundguardband1', ctypes.c_uint32, 20),
        ('Reserved52', ctypes.c_uint32, 12),
    ]


class REG_SCANLINE_GB1(ctypes.Union):
    value = []
    offset = 0

    Lowerboundguardband1 = 0  # bit 0 to 19
    Reserved20 = 0  # bit 20 to 31
    Upperboundguardband1 = 0  # bit 32 to 51
    Reserved52 = 0  # bit 52 to 63

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SCANLINE_GB1),
        ('value', ctypes.c_uint32 * 2)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SCANLINE_GB1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            for i, v in enumerate(value):
                self.value[i] = v


class OFFSET_DC6V_RESTORE_TIME:
    DC6V_RESTORE_TIME = 0x45594

class _DC6V_RESTORE_TIME(ctypes.LittleEndianStructure):
    _fields_ = [
        ('RestoreProgrammingTime', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DC6V_RESTORE_TIME(ctypes.Union):
    value = 0
    offset = 0

    RestoreProgrammingTime = 0  # bit 0 to 15
    Reserved16 = 0  # bit 16 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DC6V_RESTORE_TIME),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DC6V_RESTORE_TIME, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_WM_LINETIME_DC6V:
    WM_LINETIME_DC6V = 0x4558C

class _WM_LINETIME_DC6V(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Linetime', ctypes.c_uint32, 32),
    ]


class REG_WM_LINETIME_DC6V(ctypes.Union):
    value = 0
    offset = 0

    Linetime = 0  # bit 0 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _WM_LINETIME_DC6V),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_WM_LINETIME_DC6V, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_FRAME_COUNT_DC6V:
    FRAME_COUNT_DC6V = 0x455A4

class _FRAME_COUNT_DC6V(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FrameCountDc6V', ctypes.c_uint32, 32),
    ]


class REG_FRAME_COUNT_DC6V(ctypes.Union):
    value = 0
    offset = 0

    FrameCountDc6V = 0  # bit 0 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _FRAME_COUNT_DC6V),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_FRAME_COUNT_DC6V, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LINES_TO_VBI_DC6V:
    LINES_TO_VBI_DC6V = 0x455A0

class _LINES_TO_VBI_DC6V(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LinesToVbi', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_LINES_TO_VBI_DC6V(ctypes.Union):
    value = 0
    offset = 0

    LinesToVbi = 0  # bit 0 to 12
    Reserved13 = 0  # bit 13 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LINES_TO_VBI_DC6V),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LINES_TO_VBI_DC6V, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LINES_TO_W2:
    LINES_TO_W2_A = 0x46450
    LINES_TO_W2_B = 0x46454
    LINES_TO_W2_C = 0x46458
    LINES_TO_W2_D = 0x4645C

class _LINES_TO_W2(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LinesToW2', ctypes.c_uint32, 32),
    ]


class REG_LINES_TO_W2(ctypes.Union):
    value = 0
    offset = 0

    LinesToW2 = 0  # bit 0 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LINES_TO_W2),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LINES_TO_W2, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_POWER_WELL_1_STATE(Enum):
    POWER_WELL_1_STATE_DISABLED = 0x0
    POWER_WELL_1_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_1_REQUEST(Enum):
    POWER_WELL_1_REQUEST_DISABLE = 0x0
    POWER_WELL_1_REQUEST_ENABLE = 0x1


class ENUM_POWER_WELL_2_STATE(Enum):
    POWER_WELL_2_STATE_DISABLED = 0x0
    POWER_WELL_2_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_2_REQUEST(Enum):
    POWER_WELL_2_REQUEST_DISABLE = 0x0
    POWER_WELL_2_REQUEST_ENABLE = 0x1


class ENUM_POWER_WELL_A_STATE(Enum):
    POWER_WELL_A_STATE_DISABLED = 0x0
    POWER_WELL_A_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_A_REQUEST(Enum):
    POWER_WELL_A_REQUEST_DISABLE = 0x0
    POWER_WELL_A_REQUEST_ENABLE = 0x1


class ENUM_POWER_WELL_B_STATE(Enum):
    POWER_WELL_B_STATE_DISABLED = 0x0
    POWER_WELL_B_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_B_REQUEST(Enum):
    POWER_WELL_B_REQUEST_DISABLE = 0x0
    POWER_WELL_B_REQUEST_ENABLE = 0x1


class ENUM_POWER_WELL_C_STATE(Enum):
    POWER_WELL_C_STATE_DISABLED = 0x0
    POWER_WELL_C_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_C_REQUEST(Enum):
    POWER_WELL_C_REQUEST_DISABLE = 0x0
    POWER_WELL_C_REQUEST_ENABLE = 0x1


class ENUM_POWER_WELL_D_STATE(Enum):
    POWER_WELL_D_STATE_DISABLED = 0x0
    POWER_WELL_D_STATE_ENABLED = 0x1


class ENUM_POWER_WELL_D_REQUEST(Enum):
    POWER_WELL_D_REQUEST_DISABLE = 0x0
    POWER_WELL_D_REQUEST_ENABLE = 0x1


class OFFSET_PWR_WELL_CTL:
    PWR_WELL_CTL1 = 0x45400
    PWR_WELL_CTL2 = 0x45404
    PWR_WELL_CTL4 = 0x4540C

class _PWR_WELL_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PowerWell1State', ctypes.c_uint32, 1),
        ('PowerWell1Request', ctypes.c_uint32, 1),
        ('PowerWell2State', ctypes.c_uint32, 1),
        ('PowerWell2Request', ctypes.c_uint32, 1),
        ('Reserved4', ctypes.c_uint32, 6),
        ('PowerWellAState', ctypes.c_uint32, 1),
        ('PowerWellARequest', ctypes.c_uint32, 1),
        ('PowerWellBState', ctypes.c_uint32, 1),
        ('PowerWellBRequest', ctypes.c_uint32, 1),
        ('PowerWellCState', ctypes.c_uint32, 1),
        ('PowerWellCRequest', ctypes.c_uint32, 1),
        ('PowerWellDState', ctypes.c_uint32, 1),
        ('PowerWellDRequest', ctypes.c_uint32, 1),
        ('Reserved18', ctypes.c_uint32, 14),
    ]


class REG_PWR_WELL_CTL(ctypes.Union):
    value = 0
    offset = 0

    PowerWell1State = 0  # bit 0 to 0
    PowerWell1Request = 0  # bit 1 to 1
    PowerWell2State = 0  # bit 2 to 2
    PowerWell2Request = 0  # bit 3 to 3
    Reserved4 = 0  # bit 4 to 9
    PowerWellAState = 0  # bit 10 to 10
    PowerWellARequest = 0  # bit 11 to 11
    PowerWellBState = 0  # bit 12 to 12
    PowerWellBRequest = 0  # bit 13 to 13
    PowerWellCState = 0  # bit 14 to 14
    PowerWellCRequest = 0  # bit 15 to 15
    PowerWellDState = 0  # bit 16 to 16
    PowerWellDRequest = 0  # bit 17 to 17
    Reserved18 = 0  # bit 18 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PWR_WELL_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PWR_WELL_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PICA_PWR_WELL_CTL:
    PICA_PWR_WELL_CTL_0 = 0x16FE04

class _PICA_PWR_WELL_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 30),
        ('PowerWell1State', ctypes.c_uint32, 1),
        ('PowerWell1Request', ctypes.c_uint32, 1),
    ]


class REG_PICA_PWR_WELL_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 29
    PowerWell1State = 0  # bit 30 to 30
    PowerWell1Request = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PICA_PWR_WELL_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PICA_PWR_WELL_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_FUSE_PGD_DISTRIBUTION_STATUS(Enum):
    FUSE_PGD_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PGD_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PGC_DISTRIBUTION_STATUS(Enum):
    FUSE_PGC_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PGC_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PGB_DISTRIBUTION_STATUS(Enum):
    FUSE_PGB_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PGB_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PGA_DISTRIBUTION_STATUS(Enum):
    FUSE_PGA_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PGA_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PG2_DISTRIBUTION_STATUS(Enum):
    FUSE_PG2_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PG2_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PG1_DISTRIBUTION_STATUS(Enum):
    FUSE_PG1_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PG1_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_PG0_DISTRIBUTION_STATUS(Enum):
    FUSE_PG0_DISTRIBUTION_STATUS_NOT_DONE = 0x0
    FUSE_PG0_DISTRIBUTION_STATUS_DONE = 0x1


class ENUM_FUSE_DOWNLOAD_STATUS(Enum):
    FUSE_DOWNLOAD_STATUS_NOT_DONE = 0x0
    FUSE_DOWNLOAD_STATUS_DONE = 0x1


class OFFSET_FUSE_STATUS:
    FUSE_STATUS = 0x42000

class _FUSE_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 18),
        ('FusePgdDistributionStatus', ctypes.c_uint32, 1),
        ('FusePgcDistributionStatus', ctypes.c_uint32, 1),
        ('FusePgbDistributionStatus', ctypes.c_uint32, 1),
        ('FusePgaDistributionStatus', ctypes.c_uint32, 1),
        ('Reserved22', ctypes.c_uint32, 3),
        ('FusePg2DistributionStatus', ctypes.c_uint32, 1),
        ('FusePg1DistributionStatus', ctypes.c_uint32, 1),
        ('FusePg0DistributionStatus', ctypes.c_uint32, 1),
        ('Reserved28', ctypes.c_uint32, 3),
        ('FuseDownloadStatus', ctypes.c_uint32, 1),
    ]


class REG_FUSE_STATUS(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 17
    FusePgdDistributionStatus = 0  # bit 18 to 18
    FusePgcDistributionStatus = 0  # bit 19 to 19
    FusePgbDistributionStatus = 0  # bit 20 to 20
    FusePgaDistributionStatus = 0  # bit 21 to 21
    Reserved22 = 0  # bit 22 to 24
    FusePg2DistributionStatus = 0  # bit 25 to 25
    FusePg1DistributionStatus = 0  # bit 26 to 26
    FusePg0DistributionStatus = 0  # bit 27 to 27
    Reserved28 = 0  # bit 28 to 30
    FuseDownloadStatus = 0  # bit 31 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _FUSE_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_FUSE_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PIPEDMC_CONTROL:
    PIPEDMC_CONTROL = 0x45250

class _PIPEDMC_CONTROL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Pipedmc_EnableA', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 3),
        ('Pipedmc_EnableB', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 3),
        ('Pipedmc_EnableC', ctypes.c_uint32, 1),
        ('Reserved9', ctypes.c_uint32, 3),
        ('Pipedmc_EnableD', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_PIPEDMC_CONTROL(ctypes.Union):
    value = 0
    offset = 0

    Pipedmc_EnableA = 0  # bit 0 to 0
    Reserved1 = 0  # bit 1 to 3
    Pipedmc_EnableB = 0  # bit 4 to 4
    Reserved5 = 0  # bit 5 to 7
    Pipedmc_EnableC = 0  # bit 8 to 8
    Reserved9 = 0  # bit 9 to 11
    Pipedmc_EnableD = 0  # bit 12 to 12
    Reserved13 = 0  # bit 13 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PIPEDMC_CONTROL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PIPEDMC_CONTROL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PKG_C_LATENCY(Enum):
    PKG_C_LATENCY_DISABLED = 0xFFFF


class OFFSET_PKG_C_LATENCY:
    PKG_C_LATENCY = 0x46460

class _PKG_C_LATENCY(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PkgCLatency', ctypes.c_uint32, 32),
    ]


class REG_PKG_C_LATENCY(ctypes.Union):
    value = 0
    offset = 0

    PkgCLatency = 0  # bit 0 to 31

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PKG_C_LATENCY),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PKG_C_LATENCY, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

