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
# @file LkfPlaneRegs.py
# @brief contains LkfPlaneRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_PLANE_ROTATION(Enum):
    PLANE_ROTATION_NO_ROTATION = 0x0
    PLANE_ROTATION_90_DEGREE_ROTATION = 0x1
    PLANE_ROTATION_180_DEGREE_ROTATION = 0x2
    PLANE_ROTATION_270_DEGREE_ROTATION = 0x3


class ENUM_ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE(Enum):
    ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE_NOT_ALLOWED = 0x0
    ALLOW_DOUBLE_BUFFER_UPDATE_DISABLE_ALLOWED = 0x1


class ENUM_MEDIA_DECOMP(Enum):
    MEDIA_DECOMP_DISABLE = 0x0
    MEDIA_DECOMP_ENABLE = 0x1


class ENUM_STEREO_SURFACE_VBLANK_MASK(Enum):
    STEREO_SURFACE_VBLANK_MASK_MASK_NONE = 0x0  # Both the left and right eye vertical blanks will be used.
    STEREO_SURFACE_VBLANK_MASK_MASK_LEFT = 0x1  # Mask the left eye vertical blank. Only the right eye vertical blank w
                                                # ill be used.
    STEREO_SURFACE_VBLANK_MASK_MASK_RIGHT = 0x2  # Mask the right eye vertical blank. Only the left eye vertical blank 
                                                 # will be used.


class ENUM_HORIZONTAL_FLIP(Enum):
    HORIZONTAL_FLIP_DISABLE = 0x0
    HORIZONTAL_FLIP_ENABLE = 0x1


class ENUM_ASYNC_ADDRESS_UPDATE_ENABLE(Enum):
    ASYNC_ADDRESS_UPDATE_ENABLE_SYNC = 0x0  # Surface Address MMIO writes will update synchronous to start of vertical 
                                            # blank
    ASYNC_ADDRESS_UPDATE_ENABLE_ASYNC = 0x1  # Surface Address MMIO writes will update asynchronous to start of vertica
                                             # l blank


class ENUM_TILED_SURFACE(Enum):
    TILED_SURFACE_LINEAR_MEMORY = 0x0
    TILED_SURFACE_TILE_X_MEMORY = 0x1
    TILED_SURFACE_TILE_Y_LEGACY_MEMORY = 0x4
    TILED_SURFACE_TILE_Y_F_MEMORY = 0x5


class ENUM_CLEAR_COLOR_DISABLE(Enum):
    CLEAR_COLOR_DISABLE = 0x1
    CLEAR_COLOR_ENABLE = 0x0


class ENUM_RENDER_DECOMP(Enum):
    RENDER_DECOMP_DISABLE = 0x0
    RENDER_DECOMP_ENABLE = 0x1


class ENUM_YUV_422_BYTE_ORDER(Enum):
    YUV_422_BYTE_ORDER_YUYV = 0x0  # YUYV (MSB-V:Y2:U:Y1)
    YUV_422_BYTE_ORDER_UYVY = 0x1  # UYVY (MSB-Y2:V:Y1:U)
    YUV_422_BYTE_ORDER_YVYU = 0x2  # YVYU (MSB-U:Y2:V:Y1)
    YUV_422_BYTE_ORDER_VYUY = 0x3  # VYUY (MSB-Y2:U:Y1:V)


class ENUM_PLANAR_YUV420_COMPONENT(Enum):
    PLANAR_YUV420_COMPONENT_UV = 0x0  # Planes 1 to 5 can be configured as UV plane. Planes 6 and 7 must not be configu
                                      # red as a UV plane.
    PLANAR_YUV420_COMPONENT_Y = 0x1  # Planes 6 and 7 can be configured as Y plane. Planes 1 to 5 must not be configure
                                     # d as a Y plane.


class ENUM_RGB_COLOR_ORDER(Enum):
    RGB_COLOR_ORDER_BGRX = 0x0  # BGRX (MSB-X:R:G:B)
    RGB_COLOR_ORDER_RGBX = 0x1  # RGBX (MSB-X:B:G:R)


class ENUM_KEY_ENABLE(Enum):
    KEY_DISABLE = 0x0  # Disable keying for this plane.
    KEY_ENABLE_SOURCE_KEY_ENABLE = 0x1  # This plane's pixels will be checked for a key match. The blend between this p
                                        # lane and the plane below will treat the key matched pixels as transparent.
    KEY_ENABLE_DESTINATION_KEY_ENABLE = 0x2  # This plane's pixels will be checked for a key match. The blend between t
                                             # his plane and the plane above will treat the pixels above as opaque only
                                             # where this plane is key matched and the plane above is opaque. When
                                             # plane gamma is enabled, the gamma processing may shift the pixel color
                                             # values sent to blender and may cause it to not match the key color as
                                             # desired. The recommendation is to use the pipe gamma when destination
                                             # keying is enabled.
    KEY_ENABLE_SOURCE_KEY_WINDOW_ENABLE = 0x3  # This plane's pixels will be checked for a key match. The blend between
                                               #  this plane and the plane below will treat the key matched pixels as
                                               # transparent only where the plane below is opaque.


class ENUM_SOURCE_PIXEL_FORMAT(Enum):
    SOURCE_PIXEL_FORMAT_YUV_422_PACKED_8_BPC = 0x0  # YUV 4:2:2 packed, 8 bpc
    SOURCE_PIXEL_FORMAT_YUV_420_PLANAR_8_BPC = 0x2  # YUV 4:2:0 Planar, 8 bpc - NV12
    SOURCE_PIXEL_FORMAT_RGB_2101010 = 0x4  # RGB 2:10:10:10, 32 bit.
    SOURCE_PIXEL_FORMAT_YUV_420_PLANAR_10_BPC = 0x6  # YUV 4:2:0 Planar, 10 bpc - P010
    SOURCE_PIXEL_FORMAT_RGB_8888 = 0x8  # RGB 8:8:8:8, 32 bit
    SOURCE_PIXEL_FORMAT_YUV_420_PLANAR_12_BPC = 0xA  # YUV 4:2:0 Planar 12 bpc - P012
    SOURCE_PIXEL_FORMAT_RGB_16161616_FLOAT = 0xC  # RGB 16:16:16:16 Floating Point, 64 bit (FP16)
    SOURCE_PIXEL_FORMAT_YUV_420_PLANAR_16_BPC = 0xE  # YUV 4:2:0 Planar, 16 bpc - P016
    SOURCE_PIXEL_FORMAT_YUV_444_PACKED_8_BPC = 0x10  # YUV 4:4:4 packed (MSB-X:Y:U:V), 8bpc
    SOURCE_PIXEL_FORMAT_RGB_16161616_UINT = 0x12  # RGB 16:16:16:16 Unsigned Int, 64 bit
    SOURCE_PIXEL_FORMAT_RGB_2101010_XR_BIAS = 0x14  # RGB 2:10:10:10 Extended Range Bias (MSB-X:B:G:R), 32 bit
    SOURCE_PIXEL_FORMAT_INDEXED_8_BIT = 0x18  # Indexed 8-bit
    SOURCE_PIXEL_FORMAT_RGB_565 = 0x1C  # RGB 5:6:5 (MSB-R:G:B), 16 bit
    SOURCE_PIXEL_FORMAT_YUV_422_PACKED_10_BPC = 0x1  # YUV 4:2:2 packed, 10 bpc - Y210
    SOURCE_PIXEL_FORMAT_YUV_422_PACKED_12_BPC = 0x3  # YUV 4:2:2 packed, 12 bpc - Y212
    SOURCE_PIXEL_FORMAT_YUV_422_PACKED_16_BPC = 0x5  # YUV 4:2:2 packed, 16 bpc - Y216
    SOURCE_PIXEL_FORMAT_YUV_444_PACKED_10_BPC = 0x7  # YUV 4:4:4 packed (MSB-X:V:Y:U), 10 bpc - Y410
    SOURCE_PIXEL_FORMAT_YUV_444_PACKED_12_BPC = 0x9  # YUV 4:4:4 packed (MSB-X:V:Y:U), 12 bpc - Y412
    SOURCE_PIXEL_FORMAT_YUV_444_PACKED_16_BPC = 0xB  # YUV 4:4:4 packed (MSB-X:V:Y:U), 16 bpc - Y416


class ENUM_PLANE_ENABLE(Enum):
    PLANE_DISABLE = 0x0
    PLANE_ENABLE = 0x1


class OFFSET_PLANE_CTL:
    PLANE_CTL_1_A = 0x70180
    PLANE_CTL_2_A = 0x70280
    PLANE_CTL_3_A = 0x70380
    PLANE_CTL_4_A = 0x70480
    PLANE_CTL_5_A = 0x70580
    PLANE_CTL_6_A = 0x70680
    PLANE_CTL_7_A = 0x70780
    PLANE_CTL_1_B = 0x71180
    PLANE_CTL_2_B = 0x71280
    PLANE_CTL_3_B = 0x71380
    PLANE_CTL_4_B = 0x71480
    PLANE_CTL_5_B = 0x71580
    PLANE_CTL_6_B = 0x71680
    PLANE_CTL_7_B = 0x71780
    PLANE_CTL_1_C = 0x72180
    PLANE_CTL_2_C = 0x72280
    PLANE_CTL_3_C = 0x72380
    PLANE_CTL_4_C = 0x72480
    PLANE_CTL_5_C = 0x72580
    PLANE_CTL_6_C = 0x72680
    PLANE_CTL_7_C = 0x72780
    PLANE_CTL_1_D = 0x73180
    PLANE_CTL_2_D = 0x73280
    PLANE_CTL_3_D = 0x73380
    PLANE_CTL_4_D = 0x73480
    PLANE_CTL_5_D = 0x73580
    PLANE_CTL_6_D = 0x73680
    PLANE_CTL_7_D = 0x73780


class _PLANE_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PlaneRotation', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('AllowDoubleBufferUpdateDisable', ctypes.c_uint32, 1),
        ('MediaDecomp', ctypes.c_uint32, 1),
        ('Reserved5', ctypes.c_uint32, 1),
        ('StereoSurfaceVblankMask', ctypes.c_uint32, 2),
        ('HorizontalFlip', ctypes.c_uint32, 1),
        ('AsyncAddressUpdateEnable', ctypes.c_uint32, 1),
        ('TiledSurface', ctypes.c_uint32, 3),
        ('ClearColorDisable', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 1),
        ('RenderDecomp', ctypes.c_uint32, 1),
        ('Yuv422ByteOrder', ctypes.c_uint32, 2),
        ('Reserved18', ctypes.c_uint32, 1),
        ('PlanarYuv420Component', ctypes.c_uint32, 1),
        ('RgbColorOrder', ctypes.c_uint32, 1),
        ('KeyEnable', ctypes.c_uint32, 2),
        ('SourcePixelFormat', ctypes.c_uint32, 5),
        ('PipeSliceArbitrationSlots', ctypes.c_uint32, 3),
        ('PlaneEnable', ctypes.c_uint32, 1),
    ]


class REG_PLANE_CTL(ctypes.Union):
    value = 0
    offset = 0

    PlaneRotation = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 3
    AllowDoubleBufferUpdateDisable = 0  # bit 3 to 4
    MediaDecomp = 0  # bit 4 to 5
    Reserved5 = 0  # bit 5 to 6
    StereoSurfaceVblankMask = 0  # bit 6 to 8
    HorizontalFlip = 0  # bit 8 to 9
    AsyncAddressUpdateEnable = 0  # bit 9 to 10
    TiledSurface = 0  # bit 10 to 13
    ClearColorDisable = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 15
    RenderDecomp = 0  # bit 15 to 16
    Yuv422ByteOrder = 0  # bit 16 to 18
    Reserved18 = 0  # bit 18 to 19
    PlanarYuv420Component = 0  # bit 19 to 20
    RgbColorOrder = 0  # bit 20 to 21
    KeyEnable = 0  # bit 21 to 23
    SourcePixelFormat = 0  # bit 23 to 28
    PipeSliceArbitrationSlots = 0  # bit 28 to 31
    PlaneEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_OVERRIDE_STRIDE_ENABLE(Enum):
    OVERRIDE_STRIDE_ENABLE_OVERRIDE_DISABLE = 0x0
    OVERRIDE_STRIDE_ENABLE_OVERRIDE_ENABLE = 0x1


class OFFSET_FBC_STRIDE:
    FBC_STRIDE = 0x43228


class _FBC_STRIDE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('OverrideStride', ctypes.c_uint32, 14),
        ('Spare14', ctypes.c_uint32, 1),
        ('OverrideStrideEnable', ctypes.c_uint32, 1),
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


class REG_FBC_STRIDE(ctypes.Union):
    value = 0
    offset = 0

    OverrideStride = 0  # bit 0 to 14
    Spare14 = 0  # bit 14 to 15
    OverrideStrideEnable = 0  # bit 15 to 16
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
        ('bitMap', _FBC_STRIDE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_FBC_STRIDE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value

