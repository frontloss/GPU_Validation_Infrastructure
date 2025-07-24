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
# @file LkfPipeRegs.py
# @brief contains LkfPipeRegs.py related register definitions

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
        ('Reserved19', ctypes.c_uint32, 1),
        ('Reserved20', ctypes.c_uint32, 3),
        ('Reserved23', ctypes.c_uint32, 1),
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
    Reserved19 = 0  # bit 19 to 20
    Reserved20 = 0  # bit 20 to 23
    Reserved23 = 0  # bit 23 to 24
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
        ('XIndex', ctypes.c_uint32, 4),
        ('Reserved12', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 3),
        ('YIndex', ctypes.c_uint32, 4),
        ('Reserved20', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DPLC_HIST_INDEX(ctypes.Union):
    value = 0
    offset = 0

    DwIndex = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 8
    XIndex = 0  # bit 8 to 12
    Reserved12 = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 16
    YIndex = 0  # bit 16 to 20
    Reserved20 = 0  # bit 20 to 21
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
        ('XIndex', ctypes.c_uint32, 4),
        ('Reserved12', ctypes.c_uint32, 1),
        ('Reserved13', ctypes.c_uint32, 3),
        ('YIndex', ctypes.c_uint32, 4),
        ('Reserved20', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 11),
    ]


class REG_DPLC_IE_INDEX(ctypes.Union):
    value = 0
    offset = 0

    DwIndex = 0  # bit 0 to 5
    Reserved5 = 0  # bit 5 to 8
    XIndex = 0  # bit 8 to 12
    Reserved12 = 0  # bit 12 to 13
    Reserved13 = 0  # bit 13 to 16
    YIndex = 0  # bit 16 to 20
    Reserved20 = 0  # bit 20 to 21
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

