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
# @file Gen14DisplayPowerRegs.py
# @brief contains Gen14DisplayPowerRegs.py related register definitions

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

    DcStateSelect = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 32

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


class ENUM_PHY_PG1_LATCH(Enum):
    PHY_PG1_LATCH_PASSTHROUGH_VALUES = 0x0
    PHY_PG1_LATCH_HOLD_VALUES = 0x1


class ENUM_PHY_CLKREQ_PG1_LATCH(Enum):
    PHY_CLKREQ_PG1_LATCH_PASSTHROUGH_VALUES = 0x0
    PHY_CLKREQ_PG1_LATCH_HOLD_VALUES = 0x1


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
        ('PhyPg1Latch', ctypes.c_uint32, 1),
        ('PhyClkreqPg1Latch', ctypes.c_uint32, 1),
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

    DynamicDcStateEnable = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    Dc9Allow = 0  # bit 3 to 4
    MaskPoke = 0  # bit 4 to 5
    Dc6VBackwardCompatibility = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    BlockOutboundTraffic = 0  # bit 8 to 9
    InCsrFlow = 0  # bit 9 to 10
    CsrMask = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 16
    LongLatencyToleranceIndicator = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 20
    PhyPg1Latch = 0  # bit 20 to 21
    PhyClkreqPg1Latch = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 24
    Dc5Abort = 0  # bit 24 to 25
    MipiEnabledStatus = 0  # bit 25 to 26
    DisplayDcCoStateStatusDsi = 0  # bit 26 to 27
    DisplayClockOffEnableDsi = 0  # bit 27 to 28
    DsiPllsTurnOffDisallowed = 0  # bit 28 to 29
    DisplayDcCoStateStatusEdp = 0  # bit 29 to 30
    DisplayClockOffEnableEdp = 0  # bit 30 to 31
    ModeSetInProgress = 0  # bit 31 to 32

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

    MaskCores = 0  # bit 0 to 1
    MaskMemoryUp = 0  # bit 1 to 2
    Reserved2 = 0  # bit 2 to 32

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


class OFFSET_SCANLINE_GB1:
    SCANLINE_GB1 = 0x456A0


class _SCANLINE_GB1(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Lowerboundguardband1', ctypes.c_uint32, 20),
        ('Reserved20', ctypes.c_uint32, 12),
        ('Upperboundguardband1', ctypes.c_uint32, 20),
        ('Reserved20', ctypes.c_uint32, 12),
    ]


class REG_SCANLINE_GB1(ctypes.Union):
    value = 0
    offset = 0

    Lowerboundguardband1 = 0  # bit 0 to 20
    Reserved20 = 0  # bit 20 to 32
    Upperboundguardband1 = 0  # bit 0 to 20
    Reserved20 = 0  # bit 20 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SCANLINE_GB1),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SCANLINE_GB1, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


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

    RestoreProgrammingTime = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

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

    Linetime = 0  # bit 0 to 32

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
        ('Reserved18', ctypes.c_uint32, 4),
        ('Reserved22', ctypes.c_uint32, 10),
    ]


class REG_PWR_WELL_CTL(ctypes.Union):
    value = 0
    offset = 0

    PowerWell1State = 0  # bit 0 to 1
    PowerWell1Request = 0  # bit 1 to 2
    PowerWell2State = 0  # bit 2 to 3
    PowerWell2Request = 0  # bit 3 to 4
    Reserved4 = 0  # bit 4 to 10
    PowerWellAState = 0  # bit 10 to 11
    PowerWellARequest = 0  # bit 11 to 12
    PowerWellBState = 0  # bit 12 to 13
    PowerWellBRequest = 0  # bit 13 to 14
    PowerWellCState = 0  # bit 14 to 15
    PowerWellCRequest = 0  # bit 15 to 16
    PowerWellDState = 0  # bit 16 to 17
    PowerWellDRequest = 0  # bit 17 to 18
    Reserved18 = 0  # bit 18 to 22
    Reserved22 = 0  # bit 22 to 32

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
        ('Reserved0', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 2),
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

    Reserved0 = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 18
    FusePgdDistributionStatus = 0  # bit 18 to 19
    FusePgcDistributionStatus = 0  # bit 19 to 20
    FusePgbDistributionStatus = 0  # bit 20 to 21
    FusePgaDistributionStatus = 0  # bit 21 to 22
    Reserved22 = 0  # bit 22 to 25
    FusePg2DistributionStatus = 0  # bit 25 to 26
    FusePg1DistributionStatus = 0  # bit 26 to 27
    FusePg0DistributionStatus = 0  # bit 27 to 28
    Reserved28 = 0  # bit 28 to 31
    FuseDownloadStatus = 0  # bit 31 to 32

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

    Pipedmc_EnableA = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 4
    Pipedmc_EnableB = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 8
    Pipedmc_EnableC = 0  # bit 8 to 9
    Reserved9 = 0  # bit 9 to 12
    Pipedmc_EnableD = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 32

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

