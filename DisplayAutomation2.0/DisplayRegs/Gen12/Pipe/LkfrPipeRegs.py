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
# @file LkfrPipeRegs.py
# @brief contains LkfrPipeRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE(Enum):
    ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE_NOT_ALLOWED = 0x0
    ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE_ALLOWED = 0x1


class ENUM_NEW_LUT_READY(Enum):
    NEW_LUT_READY_NEW_LUT_NOT_READY = 0x0  # New LUT is not yet ready/hardware finished loading the LUT buffer in to in
                                           # ternal working RAM.
    NEW_LUT_READY_NEW_LUT_READY = 0x1  # New LUT is ready.


class ENUM_LUT_3D_ENABLE(Enum):
    LUT_3D_DISABLE = 0x0
    LUT_3D_ENABLE = 0x1


class OFFSET_LUT_3D_CTL:
    LUT_3D_CTL_A = 0x490A4
    LUT_3D_CTL_B = 0x491A4


class _LUT_3D_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 29),
        ('AllowDoubleBufferUpdateDisable', ctypes.c_uint32, 1),
        ('NewLutReady', ctypes.c_uint32, 1),
        ('Lut3DEnable', ctypes.c_uint32, 1),
    ]


class REG_LUT_3D_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 29
    AllowDoubleBufferUpdateDisable = 0  # bit 29 to 30
    NewLutReady = 0  # bit 30 to 31
    Lut3DEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LUT_3D_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LUT_3D_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_INDEX_AUTO_INCREMENT(Enum):
    INDEX_AUTO_INCREMENT_NO_INCREMENT = 0x0
    INDEX_AUTO_INCREMENT_AUTO_INCREMENT = 0x1


class OFFSET_LUT_3D_INDEX:
    LUT_3D_INDEX_A = 0x490A8
    LUT_3D_INDEX_B = 0x491A8


class _LUT_3D_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 13),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 18),
    ]


class REG_LUT_3D_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 13
    IndexAutoIncrement = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LUT_3D_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LUT_3D_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LUT_3D_DATA:
    LUT_3D_DATA_A = 0x490AC
    LUT_3D_DATA_B = 0x491AC


class _LUT_3D_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Lut3DEntry', ctypes.c_uint32, 30),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_LUT_3D_DATA(ctypes.Union):
    value = 0
    offset = 0

    Lut3DEntry = 0  # bit 0 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LUT_3D_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LUT_3D_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TILE_SIZE(Enum):
    TILE_SIZE_256X256 = 0x0
    TILE_SIZE_128X128 = 0x1


class ENUM_ENHANCEMENT_MODE(Enum):
    ENHANCEMENT_MODE_DIRECT = 0x0  # Direct look up Mode
    ENHANCEMENT_MODE_MULTIPLICATIVE = 0x1  # Multiplicative Mode


class ENUM_HIST_DISABLE_MODE(Enum):
    HIST_DISABLE_MODE_DISABLE = 0x0
    HIST_DISABLE_MODE_ENABLE = 0x1


class ENUM_ARBITRATION_OPTION(Enum):
    ARBITRATION_OPTION_1 = 0x0
    ARBITRATION_OPTION_2 = 0x1


class ENUM_MASK_DMC_TRIGGER(Enum):
    MASK_DMC_TRIGGER_DISABLE = 0x0
    MASK_DMC_TRIGGER_ENABLE = 0x1


class ENUM_HISTOGRAM_RAM_READBACK_RETURN(Enum):
    HISTOGRAM_RAM_READBACK_RETURN_DISABLE = 0x0
    HISTOGRAM_RAM_READBACK_RETURN_ENABLE = 0x1


class ENUM_FAST_ACCESS_MODE_ENABLE(Enum):
    FAST_ACCESS_MODE_DISABLE = 0x0
    FAST_ACCESS_MODE_ENABLE = 0x1


class ENUM_IE_BUFFER_ID(Enum):
    IE_BUFFER_ID_BANK0 = 0x0  # Reading correction factors from Bank 0
    IE_BUFFER_ID_BANK1 = 0x1  # Reading correction factors from Bank 0


class ENUM_HISTOGRAM_BUFFER_ID(Enum):
    HISTOGRAM_BUFFER_ID_BANK0 = 0x0  # Creating Histogram in Bank0
    HISTOGRAM_BUFFER_ID_BANK1 = 0x1  # Creating Histogram in Bank1


class ENUM_FRAME_HISTOGRAM_DONE(Enum):
    FRAME_HISTOGRAM_DONE_NOT_DONE = 0x0  # Histogram creation not done
    FRAME_HISTOGRAM_DONE_DONE = 0x1  # Histogram creation done


class ENUM_ORIENTATION(Enum):
    ORIENTATION_LANDSCAPE = 0x0  # 16x9 tile arrangement
    ORIENTATION_PORTRAIT = 0x1  # 9x16 tile arrangement


class ENUM_LOAD_IE(Enum):
    LOAD_IE_READY_DONE = 0x0
    LOAD_IE_LOADING = 0x1


class ENUM_IE_ENABLE(Enum):
    IE_DISABLE = 0x0  # Input pixels are routed to output with no modification
    IE_ENABLE = 0x1  # Input pixels will go through image enhancement before output


class ENUM_FUNCTION_ENABLE(Enum):
    FUNCTION_DISABLE = 0x0
    FUNCTION_ENABLE = 0x1


class OFFSET_DPLC_CTL:
    DPLC_CTL_A = 0x49400
    DPLC_CTL_B = 0x49480


class _DPLC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TileSize', ctypes.c_uint32, 1),
        ('HistBufferDelay', ctypes.c_uint32, 1),
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
        ('EnhancementMode', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 5),
        ('HistDisableMode', ctypes.c_uint32, 1),
        ('ArbitrationOption', ctypes.c_uint32, 1),
        ('MaskDmcTrigger', ctypes.c_uint32, 1),
        ('HistogramRamReadbackReturn', ctypes.c_uint32, 1),
        ('FastAccessModeEnable', ctypes.c_uint32, 1),
        ('AllowDoubleBufferUpdateDisable', ctypes.c_uint32, 1),
        ('IeBufferId', ctypes.c_uint32, 1),
        ('HistogramBufferId', ctypes.c_uint32, 1),
        ('FrameHistogramDone', ctypes.c_uint32, 1),
        ('Orientation', ctypes.c_uint32, 1),
        ('LoadIe', ctypes.c_uint32, 1),
        ('IeEnable', ctypes.c_uint32, 1),
        ('FunctionEnable', ctypes.c_uint32, 1),
    ]


class REG_DPLC_CTL(ctypes.Union):
    value = 0
    offset = 0

    TileSize = 0  # bit 0 to 1
    HistBufferDelay = 0  # bit 1 to 2
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
    EnhancementMode = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 19
    HistDisableMode = 0  # bit 19 to 20
    ArbitrationOption = 0  # bit 20 to 21
    MaskDmcTrigger = 0  # bit 21 to 22
    HistogramRamReadbackReturn = 0  # bit 22 to 23
    FastAccessModeEnable = 0  # bit 23 to 24
    AllowDoubleBufferUpdateDisable = 0  # bit 24 to 25
    IeBufferId = 0  # bit 25 to 26
    HistogramBufferId = 0  # bit 26 to 27
    FrameHistogramDone = 0  # bit 27 to 28
    Orientation = 0  # bit 28 to 29
    LoadIe = 0  # bit 29 to 30
    IeEnable = 0  # bit 30 to 31
    FunctionEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_HIST_INDEX:
    DPLC_HIST_INDEX_A = 0x49404
    DPLC_HIST_INDEX_B = 0x49484


class _DPLC_HIST_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DwIndex', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 3),
        ('XIndex', ctypes.c_uint32, 5),
        ('Reserved13', ctypes.c_uint32, 3),
        ('YIndex', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DPLC_HIST_INDEX(ctypes.Union):
    value = 0
    offset = 0

    DwIndex = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 8
    XIndex = 0  # bit 8 to 13
    Reserved13 = 0  # bit 13 to 16
    YIndex = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_HIST_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_HIST_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_HIST_DATA:
    DPLC_HIST_DATA_A = 0x49408
    DPLC_HIST_DATA_B = 0x49488


class _DPLC_HIST_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Bin', ctypes.c_uint32, 17),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_DPLC_HIST_DATA(ctypes.Union):
    value = 0
    offset = 0

    Bin = 0  # bit 0 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_HIST_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_HIST_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_IE_INDEX:
    DPLC_IE_INDEX_A = 0x4940C
    DPLC_IE_INDEX_B = 0x4948C


class _DPLC_IE_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DwIndex', ctypes.c_uint32, 5),
        ('Reserved5', ctypes.c_uint32, 3),
        ('XIndex', ctypes.c_uint32, 5),
        ('Reserved13', ctypes.c_uint32, 3),
        ('YIndex', ctypes.c_uint32, 5),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DPLC_IE_INDEX(ctypes.Union):
    value = 0
    offset = 0

    DwIndex = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 8
    XIndex = 0  # bit 8 to 13
    Reserved13 = 0  # bit 13 to 16
    YIndex = 0  # bit 16 to 21
    Reserved21 = 0  # bit 21 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_IE_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_IE_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_IE_DATA:
    DPLC_IE_DATA_A = 0x49410
    DPLC_IE_DATA_B = 0x49490


class _DPLC_IE_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('EvenPoint', ctypes.c_uint32, 12),
        ('Reserved12', ctypes.c_uint32, 4),
        ('OddPoint', ctypes.c_uint32, 12),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_DPLC_IE_DATA(ctypes.Union):
    value = 0
    offset = 0

    EvenPoint = 0  # bit 0 to 12
    Reserved12 = 0  # bit 12 to 16
    OddPoint = 0  # bit 16 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_IE_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_IE_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_PART_CTL:
    DPLC_PART_CTL_A = 0x49430
    DPLC_PART_CTL_B = 0x494B0


class _DPLC_PART_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PartAStartTileRow', ctypes.c_uint32, 5),
        ('PartAEndTileRow', ctypes.c_uint32, 5),
        ('Reserved10', ctypes.c_uint32, 6),
        ('PartBStartTileRow', ctypes.c_uint32, 5),
        ('PartBEndTileRow', ctypes.c_uint32, 5),
        ('Reserved26', ctypes.c_uint32, 6),
    ]


class REG_DPLC_PART_CTL(ctypes.Union):
    value = 0
    offset = 0

    PartAStartTileRow = 0  # bit 0 to 5
    PartAEndTileRow = 0  # bit 5 to 10
    Reserved10 = 0  # bit 10 to 16
    PartBStartTileRow = 0  # bit 16 to 21
    PartBEndTileRow = 0  # bit 21 to 26
    Reserved26 = 0  # bit 26 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_PART_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_PART_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_PTRCFG:
    DPLC_PTRCFG_PARTA_A = 0x49434
    DPLC_PTRCFG_PARTB_A = 0x49438
    DPLC_PTRCFG_PARTA_B = 0x494B4
    DPLC_PTRCFG_PARTB_B = 0x494B8


class _DPLC_PTRCFG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HistogramIndex', ctypes.c_uint32, 32),
    ]


class REG_DPLC_PTRCFG(ctypes.Union):
    value = 0
    offset = 0

    HistogramIndex = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_PTRCFG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_PTRCFG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_PTRCFG_LIVE:
    DPLC_PTRCFG_LIVE_PARTA_A = 0x49444
    DPLC_PTRCFG_LIVE_PARTB_A = 0x49448
    DPLC_PTRCFG_LIVE_PARTA_B = 0x494C4
    DPLC_PTRCFG_LIVE_PARTB_B = 0x494C8


class _DPLC_PTRCFG_LIVE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('HistogramIndex', ctypes.c_uint32, 32),
    ]


class REG_DPLC_PTRCFG_LIVE(ctypes.Union):
    value = 0
    offset = 0

    HistogramIndex = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_PTRCFG_LIVE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_PTRCFG_LIVE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_RDLENGTH:
    DPLC_RDLENGTH_PARTA_A = 0x4943C
    DPLC_RDLENGTH_PARTB_A = 0x49440
    DPLC_RDLENGTH_PARTA_B = 0x494BC
    DPLC_RDLENGTH_PARTB_B = 0x494C0


class _DPLC_RDLENGTH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ReadLength', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DPLC_RDLENGTH(ctypes.Union):
    value = 0
    offset = 0

    ReadLength = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_RDLENGTH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_RDLENGTH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_RDLENGTH_LIVE:
    DPLC_RDLENGTH_LIVE_PARTA_A = 0x4944C
    DPLC_RDLENGTH_LIVE_PARTB_A = 0x49450
    DPLC_RDLENGTH_LIVE_PARTA_B = 0x494CC
    DPLC_RDLENGTH_LIVE_PARTB_B = 0x494D0


class _DPLC_RDLENGTH_LIVE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ReadLength', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_DPLC_RDLENGTH_LIVE(ctypes.Union):
    value = 0
    offset = 0

    ReadLength = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_RDLENGTH_LIVE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_RDLENGTH_LIVE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PART_A_HISTOGRAM_READY(Enum):
    PART_A_HISTOGRAM_READY_NOT_READY = 0x0
    PART_A_HISTOGRAM_READY_READY = 0x1


class ENUM_PART_A_LOAD_IE(Enum):
    PART_A_LOAD_IE_READY_DONE = 0x0
    PART_A_LOAD_IE_LOADING = 0x1


class ENUM_PART_A_HISTOGRAM_COPY_DONE(Enum):
    PART_A_HISTOGRAM_COPY_DONE_NOT_DONE = 0x0
    PART_A_HISTOGRAM_COPY_DONE_DONE = 0x1


class ENUM_PART_B_HISTOGRAM_READY(Enum):
    PART_B_HISTOGRAM_READY_NOT_READY = 0x0
    PART_B_HISTOGRAM_READY_READY = 0x1


class ENUM_PART_B_LOAD_IE(Enum):
    PART_B_LOAD_IE_READY_DONE = 0x0
    PART_B_LOAD_IE_LOADING = 0x1


class ENUM_PART_B_HISTOGRAM_COPY_DONE(Enum):
    PART_B_HISTOGRAM_COPY_DONE_NOT_DONE = 0x0
    PART_B_HISTOGRAM_COPY_DONE_DONE = 0x1


class OFFSET_DPLC_FA_STATUS:
    DPLC_FA_STATUS_A = 0x49460
    DPLC_FA_STATUS_B = 0x494E0


class _DPLC_FA_STATUS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PartAHistogramReady', ctypes.c_uint32, 1),
        ('PartALoadIe', ctypes.c_uint32, 1),
        ('PartAHistogramCopyDone', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 13),
        ('PartBHistogramReady', ctypes.c_uint32, 1),
        ('PartBLoadIe', ctypes.c_uint32, 1),
        ('PartBHistogramCopyDone', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 13),
    ]


class REG_DPLC_FA_STATUS(ctypes.Union):
    value = 0
    offset = 0

    PartAHistogramReady = 0  # bit 0 to 1
    PartALoadIe = 0  # bit 1 to 2
    PartAHistogramCopyDone = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 16
    PartBHistogramReady = 0  # bit 16 to 17
    PartBLoadIe = 0  # bit 17 to 18
    PartBHistogramCopyDone = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_STATUS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_STATUS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_FA_SURF:
    DPLC_FA_SURF_PARTA_A = 0x49470
    DPLC_FA_SURF_PARTB_A = 0x49474
    DPLC_FA_SURF_PARTA_B = 0x494F0
    DPLC_FA_SURF_PARTB_B = 0x494F4


class _DPLC_FA_SURF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('SurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_DPLC_FA_SURF(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    SurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_SURF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_SURF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_DPLC_FA_SURF_LIVE:
    DPLC_FA_SURF_LIVE_PARTA_A = 0x49478
    DPLC_FA_SURF_LIVE_PARTB_A = 0x4947C
    DPLC_FA_SURF_LIVE_PARTA_B = 0x494F8
    DPLC_FA_SURF_LIVE_PARTB_B = 0x494FC


class _DPLC_FA_SURF_LIVE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('SurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_DPLC_FA_SURF_LIVE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    SurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DPLC_FA_SURF_LIVE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DPLC_FA_SURF_LIVE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CSC_CC2_COEFF:
    CSC_CC2_COEFF_A = 0x4A518
    CSC_CC2_COEFF_B = 0x4AD18


class _CSC_CC2_COEFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Gy', ctypes.c_uint32, 16),
        ('Ry', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('By', ctypes.c_uint32, 16),
        ('Gu', ctypes.c_uint32, 16),
        ('Ru', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('Bu', ctypes.c_uint32, 16),
        ('Gv', ctypes.c_uint32, 16),
        ('Rv', ctypes.c_uint32, 16),
        ('Reserved0', ctypes.c_uint32, 16),
        ('Bv', ctypes.c_uint32, 16),
    ]


class REG_CSC_CC2_COEFF(ctypes.Union):
    value = 0
    offset = 0

    Gy = 0  # bit 0 to 16
    Ry = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    By = 0  # bit 16 to 32
    Gu = 0  # bit 0 to 16
    Ru = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    Bu = 0  # bit 16 to 32
    Gv = 0  # bit 0 to 16
    Rv = 0  # bit 16 to 32
    Reserved0 = 0  # bit 0 to 16
    Bv = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_CC2_COEFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_CC2_COEFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CSC_CC2_PREOFF:
    CSC_CC2_PREOFF_A = 0x4A530
    CSC_CC2_PREOFF_B = 0x4AD30


class _CSC_CC2_PREOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PrecscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_CSC_CC2_PREOFF(ctypes.Union):
    value = 0
    offset = 0

    PrecscHighOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PrecscMediumOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PrecscLowOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_CC2_PREOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_CC2_PREOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CSC_CC2_POSTOFF:
    CSC_CC2_POSTOFF_A = 0x4A53C
    CSC_CC2_POSTOFF_B = 0x4AD3C


class _CSC_CC2_POSTOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PostcscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_CSC_CC2_POSTOFF(ctypes.Union):
    value = 0
    offset = 0

    PostcscHighOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PostcscMediumOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32
    PostcscLowOffset = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_CC2_POSTOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_CC2_POSTOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PRE_CSC_CC2_GAMC_INDEX:
    PRE_CSC_CC2_GAMC_INDEX_A = 0x4A500
    PRE_CSC_CC2_GAMC_INDEX_B = 0x4AD00


class _PRE_CSC_CC2_GAMC_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 2),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PRE_CSC_CC2_GAMC_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PRE_CSC_CC2_GAMC_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PRE_CSC_CC2_GAMC_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PRE_CSC_CC2_GAMC_DATA:
    PRE_CSC_CC2_GAMC_DATA_A = 0x4A504
    PRE_CSC_CC2_GAMC_DATA_B = 0x4AD04


class _PRE_CSC_CC2_GAMC_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaValue', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 12),
        ('Reserved25', ctypes.c_uint32, 7),
    ]


class REG_PRE_CSC_CC2_GAMC_DATA(ctypes.Union):
    value = 0
    offset = 0

    GammaValue = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 25
    Reserved25 = 0  # bit 25 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PRE_CSC_CC2_GAMC_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PRE_CSC_CC2_GAMC_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_POST_CSC_CC2_INDEX:
    POST_CSC_CC2_INDEX_A = 0x4A508
    POST_CSC_CC2_INDEX_B = 0x4AD08


class _POST_CSC_CC2_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 10),
        ('Reserved10', ctypes.c_uint32, 5),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_POST_CSC_CC2_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 10
    Reserved10 = 0  # bit 10 to 15
    IndexAutoIncrement = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _POST_CSC_CC2_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_POST_CSC_CC2_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_POST_CSC_CC2_DATA:
    POST_CSC_CC2_DATA_A = 0x4A50C
    POST_CSC_CC2_DATA_B = 0x4AD0C


class _POST_CSC_CC2_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BluePrecisionPaletteEntry', ctypes.c_uint32, 10),
        ('GreenPrecisionPaletteEntry', ctypes.c_uint32, 10),
        ('RedPrecisionPaletteEntry', ctypes.c_uint32, 10),
        ('Reserved30', ctypes.c_uint32, 2),
    ]


class REG_POST_CSC_CC2_DATA(ctypes.Union):
    value = 0
    offset = 0

    BluePrecisionPaletteEntry = 0  # bit 0 to 10
    GreenPrecisionPaletteEntry = 0  # bit 10 to 20
    RedPrecisionPaletteEntry = 0  # bit 20 to 30
    Reserved30 = 0  # bit 30 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _POST_CSC_CC2_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_POST_CSC_CC2_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GAMMA_MODE(Enum):
    GAMMA_MODE_8_BIT = 0x0  # 8-bit Legacy Palette Mode
    GAMMA_MODE_10_BIT = 0x1  # 10-bit Precision Palette Mode
    GAMMA_MODE_12_BIT = 0x2  # 12-bit Interpolated Gamma Mode
    GAMMA_MODE_12_BIT_MULTI_SEGMENT = 0x3  # 12-bit Multi-segmented Gamma Mode


class ENUM_GAMMA_MODE_CC2(Enum):
    GAMMA_MODE_CC2_10_BIT = 0x1  # 10-bit Precision Palette Mode
    GAMMA_MODE_CC2_12_BIT = 0x2  # 12-bit Interpolated Gamma Mode
    GAMMA_MODE_CC2_12_BIT_MULTI_SEGMENT = 0x3  # 12-bit Multi-segmented Gamma Mode


class ENUM_PALETTE_ANTICOL_DIS(Enum):
    PALETTE_ANTICOL_DIS_ENABLE = 0x0
    PALETTE_ANTICOL_DIS_DISABLE = 0x1


class ENUM_POST_CSC_CC2_GAMMA_ENABLE(Enum):
    POST_CSC_CC2_GAMMA_ENABLE = 0x1
    POST_CSC_CC2_GAMMA_DISABLE = 0x0


class ENUM_PRE_CSC_CC2_GAMMA_ENABLE(Enum):
    PRE_CSC_CC2_GAMMA_ENABLE = 0x1
    PRE_CSC_CC2_GAMMA_DISABLE = 0x0


class ENUM_POST_CSC_GAMMA_ENABLE(Enum):
    POST_CSC_GAMMA_ENABLE = 0x1
    POST_CSC_GAMMA_DISABLE = 0x0


class ENUM_PRE_CSC_GAMMA_ENABLE(Enum):
    PRE_CSC_GAMMA_ENABLE = 0x1
    PRE_CSC_GAMMA_DISABLE = 0x0


class OFFSET_GAMMA_MODE:
    GAMMA_MODE_A = 0x4A480
    GAMMA_MODE_B = 0x4AC80
    GAMMA_MODE_C = 0x4B480
    GAMMA_MODE_D = 0x4BC80


class _GAMMA_MODE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaMode', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('GammaModeCc2', ctypes.c_uint32, 2),
        ('Reserved5', ctypes.c_uint32, 10),
        ('PaletteAnticolDis', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 9),
        ('Reserved25', ctypes.c_uint32, 2),
        ('PostCscCc2GammaEnable', ctypes.c_uint32, 1),
        ('PreCscCc2GammaEnable', ctypes.c_uint32, 1),
        ('AllowDoubleBufferUpdateDisable', ctypes.c_uint32, 1),
        ('PostCscGammaEnable', ctypes.c_uint32, 1),
        ('PreCscGammaEnable', ctypes.c_uint32, 1),
    ]


class REG_GAMMA_MODE(ctypes.Union):
    value = 0
    offset = 0

    GammaMode = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    GammaModeCc2 = 0  # bit 3 to 5
    Reserved5 = 0  # bit 5 to 15
    PaletteAnticolDis = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 25
    Reserved25 = 0  # bit 25 to 27
    PostCscCc2GammaEnable = 0  # bit 27 to 28
    PreCscCc2GammaEnable = 0  # bit 28 to 29
    AllowDoubleBufferUpdateDisable = 0  # bit 29 to 30
    PostCscGammaEnable = 0  # bit 30 to 31
    PreCscGammaEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _GAMMA_MODE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_GAMMA_MODE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PIPE_CSC_CC2_ENABLE(Enum):
    PIPE_CSC_CC2_DISABLE = 0x0
    PIPE_CSC_CC2_ENABLE = 0x1


class OFFSET_CSC_MODE:
    CSC_MODE_A = 0x49028
    CSC_MODE_B = 0x49128
    CSC_MODE_C = 0x49228
    CSC_MODE_D = 0x49328


class _CSC_MODE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 28),
        ('PipeCscCC2Enable', ctypes.c_uint32, 1),
        ('AllowDoubleBufferUpdateDisable', ctypes.c_uint32, 1),
        ('PipeOutputCscEnable', ctypes.c_uint32, 1),
        ('PipeCscEnable', ctypes.c_uint32, 1),
    ]


class REG_CSC_MODE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 28
    PipeCscCC2Enable = 0  # bit 28 to 29
    AllowDoubleBufferUpdateDisable = 0  # bit 29 to 30
    PipeOutputCscEnable = 0  # bit 30 to 31
    PipeCscEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CSC_MODE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CSC_MODE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

