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
# @file LkfrPlaneRegs.py
# @brief contains LkfrPlaneRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_SELECTIVE_FETCH_PLANE_ENABLE(Enum):
    SELECTIVE_FETCH_PLANE_DISABLE = 0x0
    SELECTIVE_FETCH_PLANE_ENABLE = 0x1


class OFFSET_SEL_FETCH_PLANE_CTL:
    SEL_FETCH_PLANE_CTL_1_A = 0x70890
    SEL_FETCH_PLANE_CTL_2_A = 0x708B0
    SEL_FETCH_PLANE_CTL_3_A = 0x708D0
    SEL_FETCH_PLANE_CTL_4_A = 0x708F0
    SEL_FETCH_PLANE_CTL_5_A = 0x70920
    SEL_FETCH_PLANE_CTL_1_B = 0x70990
    SEL_FETCH_PLANE_CTL_2_B = 0x709B0
    SEL_FETCH_PLANE_CTL_3_B = 0x709D0
    SEL_FETCH_PLANE_CTL_4_B = 0x709F0
    SEL_FETCH_PLANE_CTL_5_B = 0x70A20


class _SEL_FETCH_PLANE_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Spares', ctypes.c_uint32, 31),
        ('SelectiveFetchPlaneEnable', ctypes.c_uint32, 1),
    ]


class REG_SEL_FETCH_PLANE_CTL(ctypes.Union):
    value = 0
    offset = 0

    Spares = 0  # bit 0 to 31
    SelectiveFetchPlaneEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _SEL_FETCH_PLANE_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_SEL_FETCH_PLANE_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_POS:
    PLANE_POS_1_A = 0x7018C
    PLANE_POS_2_A = 0x7028C
    PLANE_POS_3_A = 0x7038C
    PLANE_POS_4_A = 0x7048C
    PLANE_POS_5_A = 0x7058C
    SEL_FETCH_PLANE_POS_1_A = 0x70894
    SEL_FETCH_PLANE_POS_2_A = 0x708B4
    SEL_FETCH_PLANE_POS_3_A = 0x708D4
    SEL_FETCH_PLANE_POS_4_A = 0x708F4
    SEL_FETCH_PLANE_POS_5_A = 0x70924
    SEL_FETCH_PLANE_POS_1_B = 0x70994
    SEL_FETCH_PLANE_POS_2_B = 0x709B4
    SEL_FETCH_PLANE_POS_3_B = 0x709D4
    SEL_FETCH_PLANE_POS_4_B = 0x709F4
    SEL_FETCH_PLANE_POS_5_B = 0x70A24
    PLANE_POS_1_B = 0x7118C
    PLANE_POS_2_B = 0x7128C
    PLANE_POS_3_B = 0x7138C
    PLANE_POS_4_B = 0x7148C
    PLANE_POS_5_B = 0x7158C
    PLANE_POS_1_C = 0x7218C
    PLANE_POS_2_C = 0x7228C
    PLANE_POS_3_C = 0x7238C
    PLANE_POS_4_C = 0x7248C
    PLANE_POS_5_C = 0x7258C
    PLANE_POS_1_D = 0x7318C
    PLANE_POS_2_D = 0x7328C
    PLANE_POS_3_D = 0x7338C
    PLANE_POS_4_D = 0x7348C
    PLANE_POS_5_D = 0x7358C


class _PLANE_POS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('XPosition', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('YPosition', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PLANE_POS(ctypes.Union):
    value = 0
    offset = 0

    XPosition = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    YPosition = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_POS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_POS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_SIZE:
    PLANE_SIZE_1_A = 0x70190
    PLANE_SIZE_2_A = 0x70290
    PLANE_SIZE_3_A = 0x70390
    PLANE_SIZE_4_A = 0x70490
    PLANE_SIZE_5_A = 0x70590
    SEL_FETCH_PLANE_SIZE_1_A = 0x70898
    SEL_FETCH_PLANE_SIZE_2_A = 0x708B8
    SEL_FETCH_PLANE_SIZE_3_A = 0x708D8
    SEL_FETCH_PLANE_SIZE_4_A = 0x708F8
    SEL_FETCH_PLANE_SIZE_5_A = 0x70928
    SEL_FETCH_PLANE_SIZE_1_B = 0x70998
    SEL_FETCH_PLANE_SIZE_2_B = 0x709B8
    SEL_FETCH_PLANE_SIZE_3_B = 0x709D8
    SEL_FETCH_PLANE_SIZE_4_B = 0x709F8
    SEL_FETCH_PLANE_SIZE_5_B = 0x70A28
    PLANE_SIZE_1_B = 0x71190
    PLANE_SIZE_2_B = 0x71290
    PLANE_SIZE_3_B = 0x71390
    PLANE_SIZE_4_B = 0x71490
    PLANE_SIZE_5_B = 0x71590
    PLANE_SIZE_1_C = 0x72190
    PLANE_SIZE_2_C = 0x72290
    PLANE_SIZE_3_C = 0x72390
    PLANE_SIZE_4_C = 0x72490
    PLANE_SIZE_5_C = 0x72590
    PLANE_SIZE_1_D = 0x73190
    PLANE_SIZE_2_D = 0x73290
    PLANE_SIZE_3_D = 0x73390
    PLANE_SIZE_4_D = 0x73490
    PLANE_SIZE_5_D = 0x73590


class _PLANE_SIZE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Width', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('Height', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PLANE_SIZE(ctypes.Union):
    value = 0
    offset = 0

    Width = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    Height = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_SIZE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_SIZE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_OFFSET:
    PLANE_OFFSET_1_A = 0x701A4
    PLANE_OFFSET_2_A = 0x702A4
    PLANE_OFFSET_3_A = 0x703A4
    PLANE_OFFSET_4_A = 0x704A4
    PLANE_OFFSET_5_A = 0x705A4
    SEL_FETCH_PLANE_OFFSET_1_A = 0x7089C
    SEL_FETCH_PLANE_OFFSET_2_A = 0x708BC
    SEL_FETCH_PLANE_OFFSET_3_A = 0x708DC
    SEL_FETCH_PLANE_OFFSET_4_A = 0x708FC
    SEL_FETCH_PLANE_OFFSET_5_A = 0x7092C
    SEL_FETCH_PLANE_OFFSET_1_B = 0x7099C
    SEL_FETCH_PLANE_OFFSET_2_B = 0x709BC
    SEL_FETCH_PLANE_OFFSET_3_B = 0x709DC
    SEL_FETCH_PLANE_OFFSET_4_B = 0x709FC
    SEL_FETCH_PLANE_OFFSET_5_B = 0x70A2C
    PLANE_OFFSET_1_B = 0x711A4
    PLANE_OFFSET_2_B = 0x712A4
    PLANE_OFFSET_3_B = 0x713A4
    PLANE_OFFSET_4_B = 0x714A4
    PLANE_OFFSET_5_B = 0x715A4
    PLANE_OFFSET_1_C = 0x721A4
    PLANE_OFFSET_2_C = 0x722A4
    PLANE_OFFSET_3_C = 0x723A4
    PLANE_OFFSET_4_C = 0x724A4
    PLANE_OFFSET_5_C = 0x725A4
    PLANE_OFFSET_1_D = 0x731A4
    PLANE_OFFSET_2_D = 0x732A4
    PLANE_OFFSET_3_D = 0x733A4
    PLANE_OFFSET_4_D = 0x734A4
    PLANE_OFFSET_5_D = 0x735A4


class _PLANE_OFFSET(ctypes.LittleEndianStructure):
    _fields_ = [
        ('StartXPosition', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 3),
        ('StartYPosition', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PLANE_OFFSET(ctypes.Union):
    value = 0
    offset = 0

    StartXPosition = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 16
    StartYPosition = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_OFFSET),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_OFFSET, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_CURSOR_MODE_SELECT(Enum):
    CURSOR_MODE_SELECT_DISABLE = 0x0  # Cursor is disabled
    CURSOR_MODE_SELECT_128X128_32BPP_AND_INV = 0x2  # 128x128 32bpp AND/INVERT
    CURSOR_MODE_SELECT_256X256_32BPP_AND_INV = 0x3  # 256x256 32bpp AND/INVERT
    CURSOR_MODE_SELECT_64X64_2BPP_3COLOR = 0x4  # 64x64 2bpp Indexed 3-color and transparency
    CURSOR_MODE_SELECT_64X64_2BPP_2COLOR = 0x5  # 64x64 2bpp Indexed AND/XOR 2-color
    CURSOR_MODE_SELECT_64X64_2BPP_4COLOR = 0x6  # 64x64 2bpp Indexed 4-color
    CURSOR_MODE_SELECT_64X64_32BPP_AND_INV = 0x7  # 64x64 32bpp AND/INVERT
    CURSOR_MODE_SELECT_128X128_32BPP_ARGB = 0x22  # 128x128 32bpp ARGB (8:8:8:8 MSB-A:R:G:B)
    CURSOR_MODE_SELECT_256X256_32BPP_ARGB = 0x23  # 256x256 32bpp ARGB (8:8:8:8 MSB-A:R:G:B)
    CURSOR_MODE_SELECT_64X64_32BPP_AND_XOR = 0x24  # 64x64 32bpp AND/XOR
    CURSOR_MODE_SELECT_128X128_32BPP_AND_XOR = 0x25  # 128x128 32bpp AND/XOR
    CURSOR_MODE_SELECT_256X256_32BPP_AND_XOR = 0x26  # 256x256 32bpp AND/XOR
    CURSOR_MODE_SELECT_64X64_32BPP_ARGB = 0x27  # 64x64 32bpp ARGB (8:8:8:8 MSB-A:R:G:B)


class ENUM_FORCE_ALPHA_VALUE(Enum):
    FORCE_ALPHA_VALUE_DISABLE = 0x0  # Cursor pixels alpha blend normally over any plane.
    FORCE_ALPHA_VALUE_50 = 0x1  # Cursor pixels with alpha &gt;= 50% are made fully opaque where they overlap the sele
                                 # cted plane(s). Cursor pixels with alpha &lt; 50% are made fully transparent where
                                 # they overlap the selected plane(s).
    FORCE_ALPHA_VALUE_75 = 0x2  # Cursor pixels with alpha &gt;= 75% are made fully opaque where they overlap the sele
                                 # cted plane(s). Cursor pixels with alpha &lt; 75% are made fully transparent where
                                 # they overlap the selected plane(s).
    FORCE_ALPHA_VALUE_100 = 0x3  # Cursor pixels with alpha = 100% are made fully opaque where they overlap the select
                                  # ed plane(s). Cursor pixels with alpha &lt; 100% are made fully transparent where
                                  # they overlap the selected plane(s).


class ENUM_FORCE_ALPHA_PLANE_SELECT(Enum):
    FORCE_ALPHA_PLANE_SELECT_DISABLE = 0x0  # Disable alpha forcing
    FORCE_ALPHA_PLANE_SELECT_PIPE_CSC_ENABLED = 0x1  # Enable alpha forcing where cursor overlaps a plane that has enab
                                                     # led pipe CSC
    FORCE_ALPHA_PLANE_SELECT_PIPE_CSC_DISABLED = 0x2  # Enable alpha forcing where cursor overlaps plane that has disab
                                                      # led pipe CSC


class ENUM__180_ROTATION(Enum):
    _180_ROTATION_NO_ROTATION = 0x0
    _180_ROTATION_180_DEGREE_ROTATION = 0x1


class ENUM_CSC_ENABLE(Enum):
    CSC_DISABLE = 0x0
    CSC_ENABLE = 0x1


class ENUM_PRE_CSC_GAMMA_ENABLE(Enum):
    PRE_CSC_GAMMA_DISABLE = 0x0
    PRE_CSC_GAMMA_ENABLE = 0x1


class ENUM_ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE(Enum):
    ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE_NOT_ALLOWED = 0x0
    ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE_ALLOWED = 0x1


class ENUM_PIPE_CSC_ENABLE(Enum):
    PIPE_CSC_DISABLE = 0x0
    PIPE_CSC_ENABLE = 0x1


class ENUM_GAMMA_ENABLE(Enum):
    GAMMA_DISABLE = 0x0
    GAMMA_ENABLE = 0x1


class OFFSET_CUR_CTL:
    CUR_CTL_A = 0x70080
    SEL_FETCH_CUR_CTL_A = 0x70880
    SEL_FETCH_CUR_CTL_B = 0x70980
    CUR_CTL_B = 0x71080
    CUR_CTL_C = 0x72080
    CUR_CTL_D = 0x73080


class _CUR_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('CursorModeSelect', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 2),
        ('ForceAlphaValue', ctypes.c_uint32, 2),
        ('ForceAlphaPlaneSelect', ctypes.c_uint32, 2),
        ('Reserved12', ctypes.c_uint32, 3),
        ('_180Rotation', ctypes.c_uint32, 1),
        ('CscEnable', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 1),
        ('PreCscGammaEnable', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 4),
        ('AllowDoubleBufferUpdateDisable', ctypes.c_uint32, 1),
        ('PipeCscEnable', ctypes.c_uint32, 1),
        ('Reserved25', ctypes.c_uint32, 1),
        ('GammaEnable', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 1),
        ('PipeSliceArbitrationSlots', ctypes.c_uint32, 3),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_CUR_CTL(ctypes.Union):
    value = 0
    offset = 0

    CursorModeSelect = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 8
    ForceAlphaValue = 0  # bit 8 to 10
    ForceAlphaPlaneSelect = 0  # bit 10 to 12
    Reserved12 = 0  # bit 12 to 15
    _180Rotation = 0  # bit 15 to 16
    CscEnable = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 18
    PreCscGammaEnable = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 23
    AllowDoubleBufferUpdateDisable = 0  # bit 23 to 24
    PipeCscEnable = 0  # bit 24 to 25
    Reserved25 = 0  # bit 25 to 26
    GammaEnable = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 28
    PipeSliceArbitrationSlots = 0  # bit 28 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CUR_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

