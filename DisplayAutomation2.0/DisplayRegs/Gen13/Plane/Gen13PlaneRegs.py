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
# @file Gen13PlaneRegs.py
# @brief contains Gen13PlaneRegs.py related register definitions

import ctypes
from enum import Enum


class ENUM_FLIP_TYPE(Enum):
    FLIP_TYPE_SYNC_FLIP = 0x0  # Synchronous flip
    FLIP_TYPE_ASYNC_FLIP = 0x1  # Asynchronous flip
    FLIP_TYPE_STEREO_3D = 0x2  # Stereo 3D flip


class ENUM_DECRYPTION_REQUEST(Enum):
    DECRYPTION_REQUEST_NOT_REQUESTED = 0x0  # Decryption not requested
    DECRYPTION_REQUEST_REQUESTED = 0x1  # Decryption requested


class ENUM_FLIP_SOURCE(Enum):
    FLIP_SOURCE_CS = 0x0  # Flip source is CS. Send flip done response to CS.
    FLIP_SOURCE_BCS = 0x1  # Flip source is BCS. Send flip done response to BCS.


class ENUM_KEY_SELECT(Enum):
    KEY_SELECT_PAVP = 0x0
    KEY_SELECT_ID_1 = 0x1  # Isolated Decode key 1. Also used for stout mode.


class OFFSET_MSG_FLIP_SURF:
    MSG_FLIP_SURF_PLANE_1_A = 0x50080
    MSG_FLIP_SURF_PLANE_3_A = 0x50084
    MSG_FLIP_SURF_PLANE_1_B = 0x50088
    MSG_FLIP_SURF_PLANE_1_C = 0x5008C
    MSG_FLIP_SURF_PLANE_2_A = 0x50090
    MSG_FLIP_SURF_PLANE_3_B = 0x50094
    MSG_FLIP_SURF_PLANE_2_B = 0x50098
    MSG_FLIP_SURF_PLANE_2_C = 0x5009C
    MSG_FLIP_SURF_PLANE_3_C = 0x500A0
    MSG_FLIP_SURF_PLANE_4_A = 0x500A4
    MSG_FLIP_SURF_PLANE_4_B = 0x500A8
    MSG_FLIP_SURF_PLANE_4_C = 0x500AC
    MSG_FLIP_SURF_PLANE_5_A = 0x50170
    MSG_FLIP_SURF_PLANE_5_B = 0x5017C
    MSG_FLIP_SURF_PLANE_5_C = 0x50188
    MSG_FLIP_SURF_PLANE_1_D = 0x50194
    MSG_FLIP_SURF_PLANE_2_D = 0x50198
    MSG_FLIP_SURF_PLANE_3_D = 0x5019C
    MSG_FLIP_SURF_PLANE_4_D = 0x501A0
    MSG_FLIP_SURF_PLANE_5_D = 0x501A4


class _MSG_FLIP_SURF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('FlipType', ctypes.c_uint32, 2),
        ('DecryptionRequest', ctypes.c_uint32, 1),
        ('FlipSource', ctypes.c_uint32, 1),
        ('KeySelect', ctypes.c_uint32, 3),
        ('Reserved7', ctypes.c_uint32, 4),
        ('VrrMasterFlip', ctypes.c_uint32, 1),
        ('SurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_MSG_FLIP_SURF(ctypes.Union):
    value = 0
    offset = 0

    FlipType = 0  # bit 0 to 2
    DecryptionRequest = 0  # bit 2 to 3
    FlipSource = 0  # bit 3 to 4
    KeySelect = 0  # bit 4 to 7
    Reserved7 = 0  # bit 7 to 11
    VrrMasterFlip = 0  # bit 11 to 12
    SurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MSG_FLIP_SURF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MSG_FLIP_SURF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TILED_SURFACE(Enum):
    TILED_SURFACE_LINEAR_MEMORY = 0x0
    TILED_SURFACE_TILE_X_MEMORY = 0x1
    TILED_SURFACE_TILE_Y_LEGACY_MEMORY = 0x4
    TILED_SURFACE_TILE_4_MEMORY = 0x5


class OFFSET_MSG_FLIP_STRIDE:
    MSG_FLIP_STRIDE_PLANE_1_A = 0x50000
    MSG_FLIP_STRIDE_PLANE_3_A = 0x50004
    MSG_FLIP_STRIDE_PLANE_1_B = 0x50008
    MSG_FLIP_STRIDE_PLANE_1_C = 0x5000C
    MSG_FLIP_STRIDE_PLANE_2_A = 0x50010
    MSG_FLIP_STRIDE_PLANE_3_B = 0x50014
    MSG_FLIP_STRIDE_PLANE_2_B = 0x50018
    MSG_FLIP_STRIDE_PLANE_2_C = 0x5001C
    MSG_FLIP_STRIDE_PLANE_3_C = 0x50030
    MSG_FLIP_STRIDE_PLANE_4_A = 0x50034
    MSG_FLIP_STRIDE_PLANE_4_B = 0x50038
    MSG_FLIP_STRIDE_PLANE_4_C = 0x5003C
    MSG_FLIP_STRIDE_PLANE_5_A = 0x50130
    MSG_FLIP_STRIDE_PLANE_5_B = 0x5013C
    MSG_FLIP_STRIDE_PLANE_5_C = 0x50148
    MSG_FLIP_STRIDE_PLANE_1_D = 0x50154
    MSG_FLIP_STRIDE_PLANE_2_D = 0x50158
    MSG_FLIP_STRIDE_PLANE_3_D = 0x5015C
    MSG_FLIP_STRIDE_PLANE_4_D = 0x50160
    MSG_FLIP_STRIDE_PLANE_5_D = 0x50164


class _MSG_FLIP_STRIDE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('TiledSurface', ctypes.c_uint32, 3),
        ('Reserved3', ctypes.c_uint32, 3),
        ('Stride', ctypes.c_uint32, 11),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_MSG_FLIP_STRIDE(ctypes.Union):
    value = 0
    offset = 0

    TiledSurface = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 6
    Stride = 0  # bit 6 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _MSG_FLIP_STRIDE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_MSG_FLIP_STRIDE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_PLANE_ROTATION(Enum):
    PLANE_ROTATION_NO_ROTATION = 0x0
    PLANE_ROTATION_180_DEGREE_ROTATION = 0x2


class ENUM_ALLOW_DB_STALL(Enum):
    ALLOW_DB_STALL_NOT_ALLOWED = 0x0
    ALLOW_DB_STALL_ALLOWED = 0x1


class ENUM_MEDIA_DECOMP(Enum):
    MEDIA_DECOMP_DISABLE = 0x0
    MEDIA_DECOMP_ENABLE = 0x1


class ENUM_LOSSY_COMP(Enum):
    LOSSY_COMP_DISABLE = 0x0
    LOSSY_COMP_ENABLE = 0x1


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


class ENUM_SMOOTH_SYNC_PLANE_ENABLE(Enum):
    SMOOTH_SYNC_PLANE_ENABLE_SMOOTH_SYNC_DISABLED = 0x0
    SMOOTH_SYNC_PLANE_ENABLE_SMOOTH_SYNC_ENABLED = 0x1


class ENUM_PLANAR_YUV420_COMPONENT(Enum):
    PLANAR_YUV420_COMPONENT_UV = 0x0  # Planes 1 to 3 can be configured as UV plane. Planes 4 and 5 must not be configu
                                      # red as a UV plane.
    PLANAR_YUV420_COMPONENT_Y = 0x1  # Planes 4 and 5 can be configured as Y plane. Planes 1 to 3 must not be configure
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
    PLANE_CTL_1_B = 0x71180
    PLANE_CTL_2_B = 0x71280
    PLANE_CTL_3_B = 0x71380
    PLANE_CTL_4_B = 0x71480
    PLANE_CTL_5_B = 0x71580
    PLANE_CTL_1_C = 0x72180
    PLANE_CTL_2_C = 0x72280
    PLANE_CTL_3_C = 0x72380
    PLANE_CTL_4_C = 0x72480
    PLANE_CTL_5_C = 0x72580
    PLANE_CTL_1_D = 0x73180
    PLANE_CTL_2_D = 0x73280
    PLANE_CTL_3_D = 0x73380
    PLANE_CTL_4_D = 0x73480
    PLANE_CTL_5_D = 0x73580


class _PLANE_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PlaneRotation', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 1),
        ('AllowDbStall', ctypes.c_uint32, 1),
        ('MediaDecomp', ctypes.c_uint32, 1),
        ('LossyComp', ctypes.c_uint32, 1),
        ('StereoSurfaceVblankMask', ctypes.c_uint32, 2),
        ('HorizontalFlip', ctypes.c_uint32, 1),
        ('AsyncAddressUpdateEnable', ctypes.c_uint32, 1),
        ('TiledSurface', ctypes.c_uint32, 3),
        ('ClearColorDisable', ctypes.c_uint32, 1),
        ('Reserved14', ctypes.c_uint32, 1),
        ('RenderDecomp', ctypes.c_uint32, 1),
        ('Yuv422ByteOrder', ctypes.c_uint32, 2),
        ('SmoothSyncPlaneEnable', ctypes.c_uint32, 1),
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
    AllowDbStall = 0  # bit 3 to 4
    MediaDecomp = 0  # bit 4 to 5
    LossyComp = 0  # bit 5 to 6
    StereoSurfaceVblankMask = 0  # bit 6 to 8
    HorizontalFlip = 0  # bit 8 to 9
    AsyncAddressUpdateEnable = 0  # bit 9 to 10
    TiledSurface = 0  # bit 10 to 13
    ClearColorDisable = 0  # bit 13 to 14
    Reserved14 = 0  # bit 14 to 15
    RenderDecomp = 0  # bit 15 to 16
    Yuv422ByteOrder = 0  # bit 16 to 18
    SmoothSyncPlaneEnable = 0  # bit 18 to 19
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


class OFFSET_PLANE_STRIDE:
    PLANE_STRIDE_1_A = 0x70188
    PLANE_STRIDE_2_A = 0x70288
    PLANE_STRIDE_3_A = 0x70388
    PLANE_STRIDE_4_A = 0x70488
    PLANE_STRIDE_5_A = 0x70588
    PLANE_STRIDE_1_B = 0x71188
    PLANE_STRIDE_2_B = 0x71288
    PLANE_STRIDE_3_B = 0x71388
    PLANE_STRIDE_4_B = 0x71488
    PLANE_STRIDE_5_B = 0x71588
    PLANE_STRIDE_1_C = 0x72188
    PLANE_STRIDE_2_C = 0x72288
    PLANE_STRIDE_3_C = 0x72388
    PLANE_STRIDE_4_C = 0x72488
    PLANE_STRIDE_5_C = 0x72588
    PLANE_STRIDE_1_D = 0x73188
    PLANE_STRIDE_2_D = 0x73288
    PLANE_STRIDE_3_D = 0x73388
    PLANE_STRIDE_4_D = 0x73488
    PLANE_STRIDE_5_D = 0x73588


class _PLANE_STRIDE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Stride', ctypes.c_uint32, 12),
        ('Reserved12', ctypes.c_uint32, 6),
        ('Reserved18', ctypes.c_uint32, 14),
    ]


class REG_PLANE_STRIDE(ctypes.Union):
    value = 0
    offset = 0

    Stride = 0  # bit 0 to 12
    Reserved12 = 0  # bit 12 to 18
    Reserved18 = 0  # bit 18 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_STRIDE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_STRIDE, self).__init__()
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
    PLANE_POS_1_B = 0x7118C
    PLANE_POS_2_B = 0x7128C
    PLANE_POS_3_B = 0x7138C
    PLANE_POS_4_B = 0x7148C
    PLANE_POS_5_B = 0x7158C
    SEL_FETCH_PLANE_POS_1_B = 0x71894
    SEL_FETCH_PLANE_POS_2_B = 0x718B4
    SEL_FETCH_PLANE_POS_3_B = 0x718D4
    SEL_FETCH_PLANE_POS_4_B = 0x718F4
    SEL_FETCH_PLANE_POS_5_B = 0x71924
    PLANE_POS_1_C = 0x7218C
    PLANE_POS_2_C = 0x7228C
    PLANE_POS_3_C = 0x7238C
    PLANE_POS_4_C = 0x7248C
    PLANE_POS_5_C = 0x7258C
    SEL_FETCH_PLANE_POS_1_C = 0x72894
    SEL_FETCH_PLANE_POS_2_C = 0x728B4
    SEL_FETCH_PLANE_POS_3_C = 0x728D4
    SEL_FETCH_PLANE_POS_4_C = 0x728F4
    SEL_FETCH_PLANE_POS_5_C = 0x72924
    PLANE_POS_1_D = 0x7318C
    PLANE_POS_2_D = 0x7328C
    PLANE_POS_3_D = 0x7338C
    PLANE_POS_4_D = 0x7348C
    PLANE_POS_5_D = 0x7358C
    SEL_FETCH_PLANE_POS_1_D = 0x73894
    SEL_FETCH_PLANE_POS_2_D = 0x738B4
    SEL_FETCH_PLANE_POS_3_D = 0x738D4
    SEL_FETCH_PLANE_POS_4_D = 0x738F4
    SEL_FETCH_PLANE_POS_5_D = 0x73924


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
    PLANE_SIZE_1_B = 0x71190
    PLANE_SIZE_2_B = 0x71290
    PLANE_SIZE_3_B = 0x71390
    PLANE_SIZE_4_B = 0x71490
    PLANE_SIZE_5_B = 0x71590
    SEL_FETCH_PLANE_SIZE_1_B = 0x71898
    SEL_FETCH_PLANE_SIZE_2_B = 0x718B8
    SEL_FETCH_PLANE_SIZE_3_B = 0x718D8
    SEL_FETCH_PLANE_SIZE_4_B = 0x718F8
    SEL_FETCH_PLANE_SIZE_5_B = 0x71928
    PLANE_SIZE_1_C = 0x72190
    PLANE_SIZE_2_C = 0x72290
    PLANE_SIZE_3_C = 0x72390
    PLANE_SIZE_4_C = 0x72490
    PLANE_SIZE_5_C = 0x72590
    SEL_FETCH_PLANE_SIZE_1_C = 0x72898
    SEL_FETCH_PLANE_SIZE_2_C = 0x728B8
    SEL_FETCH_PLANE_SIZE_3_C = 0x728D8
    SEL_FETCH_PLANE_SIZE_4_C = 0x728F8
    SEL_FETCH_PLANE_SIZE_5_C = 0x72928
    PLANE_SIZE_1_D = 0x73190
    PLANE_SIZE_2_D = 0x73290
    PLANE_SIZE_3_D = 0x73390
    PLANE_SIZE_4_D = 0x73490
    PLANE_SIZE_5_D = 0x73590
    SEL_FETCH_PLANE_SIZE_1_D = 0x73898
    SEL_FETCH_PLANE_SIZE_2_D = 0x738B8
    SEL_FETCH_PLANE_SIZE_3_D = 0x738D8
    SEL_FETCH_PLANE_SIZE_4_D = 0x738F8
    SEL_FETCH_PLANE_SIZE_5_D = 0x73928


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


class ENUM_RING_FLIP_SOURCE(Enum):
    RING_FLIP_SOURCE_CS = 0x0
    RING_FLIP_SOURCE_BCS = 0x1


class OFFSET_PLANE_SURF:
    PLANE_SURF_1_A = 0x7019C
    PLANE_SURF_2_A = 0x7029C
    PLANE_SURF_3_A = 0x7039C
    PLANE_SURF_4_A = 0x7049C
    PLANE_SURF_5_A = 0x7059C
    PLANE_SURF_1_B = 0x7119C
    PLANE_SURF_2_B = 0x7129C
    PLANE_SURF_3_B = 0x7139C
    PLANE_SURF_4_B = 0x7149C
    PLANE_SURF_5_B = 0x7159C
    PLANE_SURF_1_C = 0x7219C
    PLANE_SURF_2_C = 0x7229C
    PLANE_SURF_3_C = 0x7239C
    PLANE_SURF_4_C = 0x7249C
    PLANE_SURF_5_C = 0x7259C
    PLANE_SURF_1_D = 0x7319C
    PLANE_SURF_2_D = 0x7329C
    PLANE_SURF_3_D = 0x7339C
    PLANE_SURF_4_D = 0x7349C
    PLANE_SURF_5_D = 0x7359C


class _PLANE_SURF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 2),
        ('DecryptionRequest', ctypes.c_uint32, 1),
        ('RingFlipSource', ctypes.c_uint32, 1),
        ('KeySelect', ctypes.c_uint32, 3),
        ('Reserved7', ctypes.c_uint32, 4),
        ('VrrMasterFlip', ctypes.c_uint32, 1),
        ('SurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_PLANE_SURF(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 2
    DecryptionRequest = 0  # bit 2 to 3
    RingFlipSource = 0  # bit 3 to 4
    KeySelect = 0  # bit 4 to 7
    Reserved7 = 0  # bit 7 to 11
    VrrMasterFlip = 0  # bit 11 to 12
    SurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_SURF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_SURF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_LEFT_SURF:
    PLANE_LEFT_SURF_1_A = 0x701B0
    PLANE_LEFT_SURF_2_A = 0x702B0
    PLANE_LEFT_SURF_3_A = 0x703B0
    PLANE_LEFT_SURF_4_A = 0x704B0
    PLANE_LEFT_SURF_5_A = 0x705B0
    PLANE_LEFT_SURF_1_B = 0x711B0
    PLANE_LEFT_SURF_2_B = 0x712B0
    PLANE_LEFT_SURF_3_B = 0x713B0
    PLANE_LEFT_SURF_4_B = 0x714B0
    PLANE_LEFT_SURF_5_B = 0x715B0
    PLANE_LEFT_SURF_1_C = 0x721B0
    PLANE_LEFT_SURF_2_C = 0x722B0
    PLANE_LEFT_SURF_3_C = 0x723B0
    PLANE_LEFT_SURF_4_C = 0x724B0
    PLANE_LEFT_SURF_5_C = 0x725B0
    PLANE_LEFT_SURF_1_D = 0x731B0
    PLANE_LEFT_SURF_2_D = 0x732B0
    PLANE_LEFT_SURF_3_D = 0x733B0
    PLANE_LEFT_SURF_4_D = 0x734B0
    PLANE_LEFT_SURF_5_D = 0x735B0


class _PLANE_LEFT_SURF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('LeftSurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_PLANE_LEFT_SURF(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    LeftSurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_LEFT_SURF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_LEFT_SURF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_AUX_DIST:
    PLANE_AUX_DIST_1_A = 0x701C0
    PLANE_AUX_DIST_2_A = 0x702C0
    PLANE_AUX_DIST_3_A = 0x703C0
    PLANE_AUX_DIST_4_A = 0x704C0
    PLANE_AUX_DIST_5_A = 0x705C0
    PLANE_AUX_DIST_1_B = 0x711C0
    PLANE_AUX_DIST_2_B = 0x712C0
    PLANE_AUX_DIST_3_B = 0x713C0
    PLANE_AUX_DIST_4_B = 0x714C0
    PLANE_AUX_DIST_5_B = 0x715C0
    PLANE_AUX_DIST_1_C = 0x721C0
    PLANE_AUX_DIST_2_C = 0x722C0
    PLANE_AUX_DIST_3_C = 0x723C0
    PLANE_AUX_DIST_4_C = 0x724C0
    PLANE_AUX_DIST_5_C = 0x725C0
    PLANE_AUX_DIST_1_D = 0x731C0
    PLANE_AUX_DIST_2_D = 0x732C0
    PLANE_AUX_DIST_3_D = 0x733C0
    PLANE_AUX_DIST_4_D = 0x734C0
    PLANE_AUX_DIST_5_D = 0x735C0


class _PLANE_AUX_DIST(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 10),
        ('Reserved10', ctypes.c_uint32, 2),
        ('AuxiliarySurfaceDistance', ctypes.c_uint32, 20),
    ]


class REG_PLANE_AUX_DIST(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 10
    Reserved10 = 0  # bit 10 to 12
    AuxiliarySurfaceDistance = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_AUX_DIST),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_AUX_DIST, self).__init__()
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
    PLANE_OFFSET_1_B = 0x711A4
    PLANE_OFFSET_2_B = 0x712A4
    PLANE_OFFSET_3_B = 0x713A4
    PLANE_OFFSET_4_B = 0x714A4
    PLANE_OFFSET_5_B = 0x715A4
    SEL_FETCH_PLANE_OFFSET_1_B = 0x7189C
    SEL_FETCH_PLANE_OFFSET_2_B = 0x718BC
    SEL_FETCH_PLANE_OFFSET_3_B = 0x718DC
    SEL_FETCH_PLANE_OFFSET_4_B = 0x718FC
    SEL_FETCH_PLANE_OFFSET_5_B = 0x7192C
    PLANE_OFFSET_1_C = 0x721A4
    PLANE_OFFSET_2_C = 0x722A4
    PLANE_OFFSET_3_C = 0x723A4
    PLANE_OFFSET_4_C = 0x724A4
    PLANE_OFFSET_5_C = 0x725A4
    SEL_FETCH_PLANE_OFFSET_1_C = 0x7289C
    SEL_FETCH_PLANE_OFFSET_2_C = 0x728BC
    SEL_FETCH_PLANE_OFFSET_3_C = 0x728DC
    SEL_FETCH_PLANE_OFFSET_4_C = 0x728FC
    SEL_FETCH_PLANE_OFFSET_5_C = 0x7292C
    PLANE_OFFSET_1_D = 0x731A4
    PLANE_OFFSET_2_D = 0x732A4
    PLANE_OFFSET_3_D = 0x733A4
    PLANE_OFFSET_4_D = 0x734A4
    PLANE_OFFSET_5_D = 0x735A4
    SEL_FETCH_PLANE_OFFSET_1_D = 0x7389C
    SEL_FETCH_PLANE_OFFSET_2_D = 0x738BC
    SEL_FETCH_PLANE_OFFSET_3_D = 0x738DC
    SEL_FETCH_PLANE_OFFSET_4_D = 0x738FC
    SEL_FETCH_PLANE_OFFSET_5_D = 0x7392C


class _PLANE_OFFSET(ctypes.LittleEndianStructure):
    _fields_ = [
        ('StartXPosition', ctypes.c_uint32, 16),
        ('StartYPosition', ctypes.c_uint32, 16),
    ]


class REG_PLANE_OFFSET(ctypes.Union):
    value = 0
    offset = 0

    StartXPosition = 0  # bit 0 to 16
    StartYPosition = 0  # bit 16 to 32

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


class OFFSET_PLANE_KEYVAL:
    PLANE_KEYVAL_1_A = 0x70194
    PLANE_KEYVAL_2_A = 0x70294
    PLANE_KEYVAL_3_A = 0x70394
    PLANE_KEYVAL_4_A = 0x70494
    PLANE_KEYVAL_5_A = 0x70594
    PLANE_KEYVAL_1_B = 0x71194
    PLANE_KEYVAL_2_B = 0x71294
    PLANE_KEYVAL_3_B = 0x71394
    PLANE_KEYVAL_4_B = 0x71494
    PLANE_KEYVAL_5_B = 0x71594
    PLANE_KEYVAL_1_C = 0x72194
    PLANE_KEYVAL_2_C = 0x72294
    PLANE_KEYVAL_3_C = 0x72394
    PLANE_KEYVAL_4_C = 0x72494
    PLANE_KEYVAL_5_C = 0x72594
    PLANE_KEYVAL_1_D = 0x73194
    PLANE_KEYVAL_2_D = 0x73294
    PLANE_KEYVAL_3_D = 0x73394
    PLANE_KEYVAL_4_D = 0x73494
    PLANE_KEYVAL_5_D = 0x73594


class _PLANE_KEYVAL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('UMinOrBKeyValue', ctypes.c_uint32, 8),
        ('YMinOrGKeyValue', ctypes.c_uint32, 8),
        ('VMinOrRKeyValue', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_PLANE_KEYVAL(ctypes.Union):
    value = 0
    offset = 0

    UMinOrBKeyValue = 0  # bit 0 to 8
    YMinOrGKeyValue = 0  # bit 8 to 16
    VMinOrRKeyValue = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_KEYVAL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_KEYVAL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_U_OR_B_KEY_CHANNEL_ENABLE(Enum):
    U_OR_B_KEY_CHANNEL_DISABLE = 0x0
    U_OR_B_KEY_CHANNEL_ENABLE = 0x1


class ENUM_Y_OR_G_KEY_CHANNEL_ENABLE(Enum):
    Y_OR_G_KEY_CHANNEL_DISABLE = 0x0
    Y_OR_G_KEY_CHANNEL_ENABLE = 0x1


class ENUM_V_OR_R_KEY_CHANNEL_ENABLE(Enum):
    V_OR_R_KEY_CHANNEL_DISABLE = 0x0
    V_OR_R_KEY_CHANNEL_ENABLE = 0x1


class ENUM_PLANE_ALPHA_ENABLE(Enum):
    PLANE_ALPHA_DISABLE = 0x0
    PLANE_ALPHA_ENABLE = 0x1


class OFFSET_PLANE_KEYMSK:
    PLANE_KEYMSK_1_A = 0x70198
    PLANE_KEYMSK_2_A = 0x70298
    PLANE_KEYMSK_3_A = 0x70398
    PLANE_KEYMSK_4_A = 0x70498
    PLANE_KEYMSK_5_A = 0x70598
    PLANE_KEYMSK_1_B = 0x71198
    PLANE_KEYMSK_2_B = 0x71298
    PLANE_KEYMSK_3_B = 0x71398
    PLANE_KEYMSK_4_B = 0x71498
    PLANE_KEYMSK_5_B = 0x71598
    PLANE_KEYMSK_1_C = 0x72198
    PLANE_KEYMSK_2_C = 0x72298
    PLANE_KEYMSK_3_C = 0x72398
    PLANE_KEYMSK_4_C = 0x72498
    PLANE_KEYMSK_5_C = 0x72598
    PLANE_KEYMSK_1_D = 0x73198
    PLANE_KEYMSK_2_D = 0x73298
    PLANE_KEYMSK_3_D = 0x73398
    PLANE_KEYMSK_4_D = 0x73498
    PLANE_KEYMSK_5_D = 0x73598


class _PLANE_KEYMSK(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BKeyMaskValue', ctypes.c_uint32, 8),
        ('GKeyMaskValue', ctypes.c_uint32, 8),
        ('RKeyMaskValue', ctypes.c_uint32, 8),
        ('UOrBKeyChannelEnable', ctypes.c_uint32, 1),
        ('YOrGKeyChannelEnable', ctypes.c_uint32, 1),
        ('VOrRKeyChannelEnable', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 4),
        ('PlaneAlphaEnable', ctypes.c_uint32, 1),
    ]


class REG_PLANE_KEYMSK(ctypes.Union):
    value = 0
    offset = 0

    BKeyMaskValue = 0  # bit 0 to 8
    GKeyMaskValue = 0  # bit 8 to 16
    RKeyMaskValue = 0  # bit 16 to 24
    UOrBKeyChannelEnable = 0  # bit 24 to 25
    YOrGKeyChannelEnable = 0  # bit 25 to 26
    VOrRKeyChannelEnable = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 31
    PlaneAlphaEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_KEYMSK),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_KEYMSK, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_KEYMAX:
    PLANE_KEYMAX_1_A = 0x701A0
    PLANE_KEYMAX_2_A = 0x702A0
    PLANE_KEYMAX_3_A = 0x703A0
    PLANE_KEYMAX_4_A = 0x704A0
    PLANE_KEYMAX_5_A = 0x705A0
    PLANE_KEYMAX_1_B = 0x711A0
    PLANE_KEYMAX_2_B = 0x712A0
    PLANE_KEYMAX_3_B = 0x713A0
    PLANE_KEYMAX_4_B = 0x714A0
    PLANE_KEYMAX_5_B = 0x715A0
    PLANE_KEYMAX_1_C = 0x721A0
    PLANE_KEYMAX_2_C = 0x722A0
    PLANE_KEYMAX_3_C = 0x723A0
    PLANE_KEYMAX_4_C = 0x724A0
    PLANE_KEYMAX_5_C = 0x725A0
    PLANE_KEYMAX_1_D = 0x731A0
    PLANE_KEYMAX_2_D = 0x732A0
    PLANE_KEYMAX_3_D = 0x733A0
    PLANE_KEYMAX_4_D = 0x734A0
    PLANE_KEYMAX_5_D = 0x735A0


class _PLANE_KEYMAX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('UKeyMaxValue', ctypes.c_uint32, 8),
        ('YKeyMaxValue', ctypes.c_uint32, 8),
        ('VKeyMaxValue', ctypes.c_uint32, 8),
        ('PlaneAlphaValue', ctypes.c_uint32, 8),
    ]


class REG_PLANE_KEYMAX(ctypes.Union):
    value = 0
    offset = 0

    UKeyMaxValue = 0  # bit 0 to 8
    YKeyMaxValue = 0  # bit 8 to 16
    VKeyMaxValue = 0  # bit 16 to 24
    PlaneAlphaValue = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_KEYMAX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_KEYMAX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_SURFLIVE:
    PLANE_SURFLIVE_1_A = 0x701AC
    PLANE_LEFT_SURFLIVE_1_A = 0x701BC
    PLANE_SURFLIVE_2_A = 0x702AC
    PLANE_LEFT_SURFLIVE_2_A = 0x702BC
    PLANE_SURFLIVE_3_A = 0x703AC
    PLANE_LEFT_SURFLIVE_3_A = 0x703BC
    PLANE_SURFLIVE_4_A = 0x704AC
    PLANE_LEFT_SURFLIVE_4_A = 0x704BC
    PLANE_SURFLIVE_5_A = 0x705AC
    PLANE_LEFT_SURFLIVE_5_A = 0x705BC
    PLANE_SURFLIVE_1_B = 0x711AC
    PLANE_LEFT_SURFLIVE_1_B = 0x711BC
    PLANE_SURFLIVE_2_B = 0x712AC
    PLANE_LEFT_SURFLIVE_2_B = 0x712BC
    PLANE_SURFLIVE_3_B = 0x713AC
    PLANE_LEFT_SURFLIVE_3_B = 0x713BC
    PLANE_SURFLIVE_4_B = 0x714AC
    PLANE_LEFT_SURFLIVE_4_B = 0x714BC
    PLANE_SURFLIVE_5_B = 0x715AC
    PLANE_LEFT_SURFLIVE_5_B = 0x715BC
    PLANE_SURFLIVE_1_C = 0x721AC
    PLANE_LEFT_SURFLIVE_1_C = 0x721BC
    PLANE_SURFLIVE_2_C = 0x722AC
    PLANE_LEFT_SURFLIVE_2_C = 0x722BC
    PLANE_SURFLIVE_3_C = 0x723AC
    PLANE_LEFT_SURFLIVE_3_C = 0x723BC
    PLANE_SURFLIVE_4_C = 0x724AC
    PLANE_LEFT_SURFLIVE_4_C = 0x724BC
    PLANE_SURFLIVE_5_C = 0x725AC
    PLANE_LEFT_SURFLIVE_5_C = 0x725BC
    PLANE_SURFLIVE_1_D = 0x731AC
    PLANE_LEFT_SURFLIVE_1_D = 0x731BC
    PLANE_SURFLIVE_2_D = 0x732AC
    PLANE_LEFT_SURFLIVE_2_D = 0x732BC
    PLANE_SURFLIVE_3_D = 0x733AC
    PLANE_LEFT_SURFLIVE_3_D = 0x733BC
    PLANE_SURFLIVE_4_D = 0x734AC
    PLANE_LEFT_SURFLIVE_4_D = 0x734BC
    PLANE_SURFLIVE_5_D = 0x735AC
    PLANE_LEFT_SURFLIVE_5_D = 0x735BC


class _PLANE_SURFLIVE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 9),
        ('CurrentFrameCounterEntry', ctypes.c_uint32, 2),
        ('Reserved11', ctypes.c_uint32, 1),
        ('LiveSurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_PLANE_SURFLIVE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 9
    CurrentFrameCounterEntry = 0  # bit 9 to 11
    Reserved11 = 0  # bit 11 to 12
    LiveSurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_SURFLIVE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_SURFLIVE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_IGNORE_LINES(Enum):
    IGNORE_LINES_IGNORE_LINES = 0x1
    IGNORE_LINES_USE_LINES = 0x0


class ENUM_ENABLE(Enum):
    ENABLE_ENABLE = 0x1
    ENABLE_DISABLE = 0x0


class OFFSET_PLANE_WM:
    CUR_WM_0_A = 0x70140
    CUR_WM_1_A = 0x70144
    CUR_WM_2_A = 0x70148
    CUR_WM_3_A = 0x7014C
    CUR_WM_4_A = 0x70150
    CUR_WM_5_A = 0x70154
    CUR_WM_SAGV_A = 0x70158
    CUR_WM_SAGV_TRANS_A = 0x7015C
    CUR_WM_TRANS_A = 0x70168
    PLANE_WM_0_1_A = 0x70240
    PLANE_WM_1_1_A = 0x70244
    PLANE_WM_2_1_A = 0x70248
    PLANE_WM_3_1_A = 0x7024C
    PLANE_WM_4_1_A = 0x70250
    PLANE_WM_5_1_A = 0x70254
    PLANE_WM_SAGV_1_A = 0x70258
    PLANE_WM_SAGV_TRANS_1_A = 0x7025C
    PLANE_WM_TRANS_1_A = 0x70268
    PLANE_WM_0_2_A = 0x70340
    PLANE_WM_1_2_A = 0x70344
    PLANE_WM_2_2_A = 0x70348
    PLANE_WM_3_2_A = 0x7034C
    PLANE_WM_4_2_A = 0x70350
    PLANE_WM_5_2_A = 0x70354
    PLANE_WM_SAGV_2_A = 0x70358
    PLANE_WM_SAGV_TRANS_2_A = 0x7035C
    PLANE_WM_TRANS_2_A = 0x70368
    PLANE_WM_0_3_A = 0x70440
    PLANE_WM_1_3_A = 0x70444
    PLANE_WM_2_3_A = 0x70448
    PLANE_WM_3_3_A = 0x7044C
    PLANE_WM_4_3_A = 0x70450
    PLANE_WM_5_3_A = 0x70454
    PLANE_WM_SAGV_3_A = 0x70458
    PLANE_WM_SAGV_TRANS_3_A = 0x7045C
    PLANE_WM_TRANS_3_A = 0x70468
    PLANE_WM_0_4_A = 0x70540
    PLANE_WM_1_4_A = 0x70544
    PLANE_WM_2_4_A = 0x70548
    PLANE_WM_3_4_A = 0x7054C
    PLANE_WM_4_4_A = 0x70550
    PLANE_WM_5_4_A = 0x70554
    PLANE_WM_SAGV_4_A = 0x70558
    PLANE_WM_SAGV_TRANS_4_A = 0x7055C
    PLANE_WM_TRANS_4_A = 0x70568
    PLANE_WM_0_5_A = 0x70640
    PLANE_WM_1_5_A = 0x70644
    PLANE_WM_2_5_A = 0x70648
    PLANE_WM_3_5_A = 0x7064C
    PLANE_WM_4_5_A = 0x70650
    PLANE_WM_5_5_A = 0x70654
    PLANE_WM_SAGV_5_A = 0x70658
    PLANE_WM_SAGV_TRANS_5_A = 0x7065C
    PLANE_WM_TRANS_5_A = 0x70668
    CUR_WM_0_B = 0x71140
    CUR_WM_1_B = 0x71144
    CUR_WM_2_B = 0x71148
    CUR_WM_3_B = 0x7114C
    CUR_WM_4_B = 0x71150
    CUR_WM_5_B = 0x71154
    CUR_WM_SAGV_B = 0x71158
    CUR_WM_SAGV_TRANS_B = 0x7115C
    CUR_WM_TRANS_B = 0x71168
    PLANE_WM_0_1_B = 0x71240
    PLANE_WM_1_1_B = 0x71244
    PLANE_WM_2_1_B = 0x71248
    PLANE_WM_3_1_B = 0x7124C
    PLANE_WM_4_1_B = 0x71250
    PLANE_WM_5_1_B = 0x71254
    PLANE_WM_SAGV_1_B = 0x71258
    PLANE_WM_SAGV_TRANS_1_B = 0x7125C
    PLANE_WM_TRANS_1_B = 0x71268
    PLANE_WM_0_2_B = 0x71340
    PLANE_WM_1_2_B = 0x71344
    PLANE_WM_2_2_B = 0x71348
    PLANE_WM_3_2_B = 0x7134C
    PLANE_WM_4_2_B = 0x71350
    PLANE_WM_5_2_B = 0x71354
    PLANE_WM_SAGV_2_B = 0x71358
    PLANE_WM_SAGV_TRANS_2_B = 0x7135C
    PLANE_WM_TRANS_2_B = 0x71368
    PLANE_WM_0_3_B = 0x71440
    PLANE_WM_1_3_B = 0x71444
    PLANE_WM_2_3_B = 0x71448
    PLANE_WM_3_3_B = 0x7144C
    PLANE_WM_4_3_B = 0x71450
    PLANE_WM_5_3_B = 0x71454
    PLANE_WM_SAGV_3_B = 0x71458
    PLANE_WM_SAGV_TRANS_3_B = 0x7145C
    PLANE_WM_TRANS_3_B = 0x71468
    PLANE_WM_0_4_B = 0x71540
    PLANE_WM_1_4_B = 0x71544
    PLANE_WM_2_4_B = 0x71548
    PLANE_WM_3_4_B = 0x7154C
    PLANE_WM_4_4_B = 0x71550
    PLANE_WM_5_4_B = 0x71554
    PLANE_WM_SAGV_4_B = 0x71558
    PLANE_WM_SAGV_TRANS_4_B = 0x7155C
    PLANE_WM_TRANS_4_B = 0x71568
    PLANE_WM_0_5_B = 0x71640
    PLANE_WM_1_5_B = 0x71644
    PLANE_WM_2_5_B = 0x71648
    PLANE_WM_3_5_B = 0x7164C
    PLANE_WM_4_5_B = 0x71650
    PLANE_WM_5_5_B = 0x71654
    PLANE_WM_SAGV_5_B = 0x71658
    PLANE_WM_SAGV_TRANS_5_B = 0x7165C
    PLANE_WM_TRANS_5_B = 0x71668
    CUR_WM_0_C = 0x72140
    CUR_WM_1_C = 0x72144
    CUR_WM_2_C = 0x72148
    CUR_WM_3_C = 0x7214C
    CUR_WM_4_C = 0x72150
    CUR_WM_5_C = 0x72154
    CUR_WM_SAGV_C = 0x72158
    CUR_WM_SAGV_TRANS_C = 0x7215C
    CUR_WM_TRANS_C = 0x72168
    PLANE_WM_0_1_C = 0x72240
    PLANE_WM_1_1_C = 0x72244
    PLANE_WM_2_1_C = 0x72248
    PLANE_WM_3_1_C = 0x7224C
    PLANE_WM_4_1_C = 0x72250
    PLANE_WM_5_1_C = 0x72254
    PLANE_WM_SAGV_1_C = 0x72258
    PLANE_WM_SAGV_TRANS_1_C = 0x7225C
    PLANE_WM_TRANS_1_C = 0x72268
    PLANE_WM_0_2_C = 0x72340
    PLANE_WM_1_2_C = 0x72344
    PLANE_WM_2_2_C = 0x72348
    PLANE_WM_3_2_C = 0x7234C
    PLANE_WM_4_2_C = 0x72350
    PLANE_WM_5_2_C = 0x72354
    PLANE_WM_SAGV_2_C = 0x72358
    PLANE_WM_SAGV_TRANS_2_C = 0x7235C
    PLANE_WM_TRANS_2_C = 0x72368
    PLANE_WM_0_3_C = 0x72440
    PLANE_WM_1_3_C = 0x72444
    PLANE_WM_2_3_C = 0x72448
    PLANE_WM_3_3_C = 0x7244C
    PLANE_WM_4_3_C = 0x72450
    PLANE_WM_5_3_C = 0x72454
    PLANE_WM_SAGV_3_C = 0x72458
    PLANE_WM_SAGV_TRANS_3_C = 0x7245C
    PLANE_WM_TRANS_3_C = 0x72468
    PLANE_WM_0_4_C = 0x72540
    PLANE_WM_1_4_C = 0x72544
    PLANE_WM_2_4_C = 0x72548
    PLANE_WM_3_4_C = 0x7254C
    PLANE_WM_4_4_C = 0x72550
    PLANE_WM_5_4_C = 0x72554
    PLANE_WM_SAGV_4_C = 0x72558
    PLANE_WM_SAGV_TRANS_4_C = 0x7255C
    PLANE_WM_TRANS_4_C = 0x72568
    PLANE_WM_0_5_C = 0x72640
    PLANE_WM_1_5_C = 0x72644
    PLANE_WM_2_5_C = 0x72648
    PLANE_WM_3_5_C = 0x7264C
    PLANE_WM_4_5_C = 0x72650
    PLANE_WM_5_5_C = 0x72654
    PLANE_WM_SAGV_5_C = 0x72658
    PLANE_WM_SAGV_TRANS_5_C = 0x7265C
    PLANE_WM_TRANS_5_C = 0x72668
    CUR_WM_0_D = 0x73140
    CUR_WM_1_D = 0x73144
    CUR_WM_2_D = 0x73148
    CUR_WM_3_D = 0x7314C
    CUR_WM_4_D = 0x73150
    CUR_WM_5_D = 0x73154
    CUR_WM_SAGV_D = 0x73158
    CUR_WM_SAGV_TRANS_D = 0x7315C
    CUR_WM_TRANS_D = 0x73168
    PLANE_WM_0_1_D = 0x73240
    PLANE_WM_1_1_D = 0x73244
    PLANE_WM_2_1_D = 0x73248
    PLANE_WM_3_1_D = 0x7324C
    PLANE_WM_4_1_D = 0x73250
    PLANE_WM_5_1_D = 0x73254
    PLANE_WM_SAGV_1_D = 0x73258
    PLANE_WM_SAGV_TRANS_1_D = 0x7325C
    PLANE_WM_TRANS_1_D = 0x73268
    PLANE_WM_0_2_D = 0x73340
    PLANE_WM_1_2_D = 0x73344
    PLANE_WM_2_2_D = 0x73348
    PLANE_WM_3_2_D = 0x7334C
    PLANE_WM_4_2_D = 0x73350
    PLANE_WM_5_2_D = 0x73354
    PLANE_WM_SAGV_2_D = 0x73358
    PLANE_WM_SAGV_TRANS_2_D = 0x7335C
    PLANE_WM_TRANS_2_D = 0x73368
    PLANE_WM_0_3_D = 0x73440
    PLANE_WM_1_3_D = 0x73444
    PLANE_WM_2_3_D = 0x73448
    PLANE_WM_3_3_D = 0x7344C
    PLANE_WM_4_3_D = 0x73450
    PLANE_WM_5_3_D = 0x73454
    PLANE_WM_SAGV_3_D = 0x73458
    PLANE_WM_SAGV_TRANS_3_D = 0x7345C
    PLANE_WM_TRANS_3_D = 0x73468
    PLANE_WM_0_4_D = 0x73540
    PLANE_WM_1_4_D = 0x73544
    PLANE_WM_2_4_D = 0x73548
    PLANE_WM_3_4_D = 0x7354C
    PLANE_WM_4_4_D = 0x73550
    PLANE_WM_5_4_D = 0x73554
    PLANE_WM_SAGV_4_D = 0x73558
    PLANE_WM_SAGV_TRANS_4_D = 0x7355C
    PLANE_WM_TRANS_4_D = 0x73568
    PLANE_WM_0_5_D = 0x73640
    PLANE_WM_1_5_D = 0x73644
    PLANE_WM_2_5_D = 0x73648
    PLANE_WM_3_5_D = 0x7364C
    PLANE_WM_4_5_D = 0x73650
    PLANE_WM_5_5_D = 0x73654
    PLANE_WM_SAGV_5_D = 0x73658
    PLANE_WM_SAGV_TRANS_5_D = 0x7365C
    PLANE_WM_TRANS_5_D = 0x73668


class _PLANE_WM(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Blocks', ctypes.c_uint32, 12),
        ('Reserved12', ctypes.c_uint32, 2),
        ('Lines', ctypes.c_uint32, 13),
        ('Reserved27', ctypes.c_uint32, 3),
        ('IgnoreLines', ctypes.c_uint32, 1),
        ('Enable', ctypes.c_uint32, 1),
    ]


class REG_PLANE_WM(ctypes.Union):
    value = 0
    offset = 0

    Blocks = 0  # bit 0 to 12
    Reserved12 = 0  # bit 12 to 14
    Lines = 0  # bit 14 to 27
    Reserved27 = 0  # bit 27 to 30
    IgnoreLines = 0  # bit 30 to 31
    Enable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_WM),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_WM, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_WM_LINETIME:
    WM_LINETIME_A = 0x45270
    WM_LINETIME_B = 0x45274
    WM_LINETIME_C = 0x45278
    WM_LINETIME_D = 0x4527C


class _WM_LINETIME(ctypes.LittleEndianStructure):
    _fields_ = [
        ('LineTime', ctypes.c_uint32, 9),
        ('Reserved9', ctypes.c_uint32, 23),
    ]


class REG_WM_LINETIME(ctypes.Union):
    value = 0
    offset = 0

    LineTime = 0  # bit 0 to 9
    Reserved9 = 0  # bit 9 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _WM_LINETIME),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_WM_LINETIME, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_BUF_CFG:
    CUR_BUF_CFG_A = 0x7017C
    PLANE_BUF_CFG_1_A = 0x7027C
    PLANE_BUF_CFG_2_A = 0x7037C
    PLANE_BUF_CFG_3_A = 0x7047C
    PLANE_BUF_CFG_4_A = 0x7057C
    PLANE_BUF_CFG_5_A = 0x7067C
    CUR_BUF_CFG_B = 0x7117C
    PLANE_BUF_CFG_1_B = 0x7127C
    PLANE_BUF_CFG_2_B = 0x7137C
    PLANE_BUF_CFG_3_B = 0x7147C
    PLANE_BUF_CFG_4_B = 0x7157C
    PLANE_BUF_CFG_5_B = 0x7167C
    CUR_BUF_CFG_C = 0x7217C
    PLANE_BUF_CFG_1_C = 0x7227C
    PLANE_BUF_CFG_2_C = 0x7237C
    PLANE_BUF_CFG_3_C = 0x7247C
    PLANE_BUF_CFG_4_C = 0x7257C
    PLANE_BUF_CFG_5_C = 0x7267C
    CUR_BUF_CFG_D = 0x7317C
    PLANE_BUF_CFG_1_D = 0x7327C
    PLANE_BUF_CFG_2_D = 0x7337C
    PLANE_BUF_CFG_3_D = 0x7347C
    PLANE_BUF_CFG_4_D = 0x7357C
    PLANE_BUF_CFG_5_D = 0x7367C


class _PLANE_BUF_CFG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BufferStart', ctypes.c_uint32, 12),
        ('Reserved12', ctypes.c_uint32, 4),
        ('BufferEnd', ctypes.c_uint32, 12),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_PLANE_BUF_CFG(ctypes.Union):
    value = 0
    offset = 0

    BufferStart = 0  # bit 0 to 12
    Reserved12 = 0  # bit 12 to 16
    BufferEnd = 0  # bit 16 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_BUF_CFG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_BUF_CFG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_INDEX_AUTO_INCREMENT(Enum):
    INDEX_AUTO_INCREMENT_NO_INCREMENT = 0x0  # Do not automatically increment the index value.
    INDEX_AUTO_INCREMENT_AUTO_INCREMENT = 0x1  # Increment the index value with each read or write to the data register
                                               # .


class OFFSET_PLANE_PRE_CSC_GAMC_INDEX_ENH:
    PLANE_PRE_CSC_GAMC_INDEX_ENH_1_A = 0x701D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_2_A = 0x702D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_3_A = 0x703D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_1_B = 0x711D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_2_B = 0x712D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_3_B = 0x713D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_1_C = 0x721D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_2_C = 0x722D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_3_C = 0x723D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_1_D = 0x731D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_2_D = 0x732D0
    PLANE_PRE_CSC_GAMC_INDEX_ENH_3_D = 0x733D0


class _PLANE_PRE_CSC_GAMC_INDEX_ENH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 2),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PLANE_PRE_CSC_GAMC_INDEX_ENH(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_PRE_CSC_GAMC_INDEX_ENH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_PRE_CSC_GAMC_INDEX_ENH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_PRE_CSC_GAMC_INDEX:
    PLANE_PRE_CSC_GAMC_INDEX_4_A = 0x704D0
    PLANE_PRE_CSC_GAMC_INDEX_5_A = 0x705D0
    PLANE_PRE_CSC_GAMC_INDEX_4_B = 0x714D0
    PLANE_PRE_CSC_GAMC_INDEX_5_B = 0x715D0
    PLANE_PRE_CSC_GAMC_INDEX_4_C = 0x724D0
    PLANE_PRE_CSC_GAMC_INDEX_5_C = 0x725D0
    PLANE_PRE_CSC_GAMC_INDEX_4_D = 0x734D0
    PLANE_PRE_CSC_GAMC_INDEX_5_D = 0x735D0


class _PLANE_PRE_CSC_GAMC_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 4),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PLANE_PRE_CSC_GAMC_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_PRE_CSC_GAMC_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_PRE_CSC_GAMC_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_PRE_CSC_GAMC_DATA_ENH:
    PLANE_PRE_CSC_GAMC_DATA_ENH_1_A = 0x701D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_2_A = 0x702D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_3_A = 0x703D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_1_B = 0x711D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_2_B = 0x712D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_3_B = 0x713D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_1_C = 0x721D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_2_C = 0x722D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_3_C = 0x723D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_1_D = 0x731D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_2_D = 0x732D4
    PLANE_PRE_CSC_GAMC_DATA_ENH_3_D = 0x733D4


class _PLANE_PRE_CSC_GAMC_DATA_ENH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaValue', ctypes.c_uint32, 27),
        ('Reserved27', ctypes.c_uint32, 5),
    ]


class REG_PLANE_PRE_CSC_GAMC_DATA_ENH(ctypes.Union):
    value = 0
    offset = 0

    GammaValue = 0  # bit 0 to 27
    Reserved27 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_PRE_CSC_GAMC_DATA_ENH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_PRE_CSC_GAMC_DATA_ENH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_PRE_CSC_GAMC_DATA:
    PLANE_PRE_CSC_GAMC_DATA_4_A = 0x704D4
    PLANE_PRE_CSC_GAMC_DATA_5_A = 0x705D4
    PLANE_PRE_CSC_GAMC_DATA_4_B = 0x714D4
    PLANE_PRE_CSC_GAMC_DATA_5_B = 0x715D4
    PLANE_PRE_CSC_GAMC_DATA_4_C = 0x724D4
    PLANE_PRE_CSC_GAMC_DATA_5_C = 0x725D4
    PLANE_PRE_CSC_GAMC_DATA_4_D = 0x734D4
    PLANE_PRE_CSC_GAMC_DATA_5_D = 0x735D4


class _PLANE_PRE_CSC_GAMC_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaValue', ctypes.c_uint32, 19),
        ('Reserved19', ctypes.c_uint32, 13),
    ]


class REG_PLANE_PRE_CSC_GAMC_DATA(ctypes.Union):
    value = 0
    offset = 0

    GammaValue = 0  # bit 0 to 19
    Reserved19 = 0  # bit 19 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_PRE_CSC_GAMC_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_PRE_CSC_GAMC_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_POST_CSC_GAMC_INDEX_ENH:
    PLANE_POST_CSC_GAMC_INDEX_ENH_1_A = 0x701D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_2_A = 0x702D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_3_A = 0x703D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_1_B = 0x711D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_2_B = 0x712D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_3_B = 0x713D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_1_C = 0x721D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_2_C = 0x722D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_3_C = 0x723D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_1_D = 0x731D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_2_D = 0x732D8
    PLANE_POST_CSC_GAMC_INDEX_ENH_3_D = 0x733D8


class _PLANE_POST_CSC_GAMC_INDEX_ENH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 4),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PLANE_POST_CSC_GAMC_INDEX_ENH(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_POST_CSC_GAMC_INDEX_ENH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_POST_CSC_GAMC_INDEX_ENH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH:
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_1_A = 0x70160
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_2_A = 0x70260
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_3_A = 0x70360
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_1_B = 0x71160
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_2_B = 0x71260
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_3_B = 0x71360
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_1_C = 0x72160
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_2_C = 0x72260
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_3_C = 0x72360
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_1_D = 0x73160
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_2_D = 0x73260
    PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH_3_D = 0x73360


class _PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 4),
        ('Reserved4', ctypes.c_uint32, 6),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 4
    Reserved4 = 0  # bit 4 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_POST_CSC_GAMC_SEG0_INDEX_ENH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_POST_CSC_GAMC_INDEX:
    PLANE_POST_CSC_GAMC_INDEX_4_A = 0x704D8
    PLANE_POST_CSC_GAMC_INDEX_5_A = 0x705D8
    PLANE_POST_CSC_GAMC_INDEX_4_B = 0x714D8
    PLANE_POST_CSC_GAMC_INDEX_5_B = 0x715D8
    PLANE_POST_CSC_GAMC_INDEX_4_C = 0x724D8
    PLANE_POST_CSC_GAMC_INDEX_5_C = 0x725D8
    PLANE_POST_CSC_GAMC_INDEX_4_D = 0x734D8
    PLANE_POST_CSC_GAMC_INDEX_5_D = 0x735D8


class _PLANE_POST_CSC_GAMC_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 4),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_PLANE_POST_CSC_GAMC_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_POST_CSC_GAMC_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_POST_CSC_GAMC_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_POST_CSC_GAMC_DATA_ENH:
    PLANE_POST_CSC_GAMC_DATA_ENH_1_A = 0x701DC
    PLANE_POST_CSC_GAMC_DATA_ENH_2_A = 0x702DC
    PLANE_POST_CSC_GAMC_DATA_ENH_3_A = 0x703DC
    PLANE_POST_CSC_GAMC_DATA_ENH_1_B = 0x711DC
    PLANE_POST_CSC_GAMC_DATA_ENH_2_B = 0x712DC
    PLANE_POST_CSC_GAMC_DATA_ENH_3_B = 0x713DC
    PLANE_POST_CSC_GAMC_DATA_ENH_1_C = 0x721DC
    PLANE_POST_CSC_GAMC_DATA_ENH_2_C = 0x722DC
    PLANE_POST_CSC_GAMC_DATA_ENH_3_C = 0x723DC
    PLANE_POST_CSC_GAMC_DATA_ENH_1_D = 0x731DC
    PLANE_POST_CSC_GAMC_DATA_ENH_2_D = 0x732DC
    PLANE_POST_CSC_GAMC_DATA_ENH_3_D = 0x733DC


class _PLANE_POST_CSC_GAMC_DATA_ENH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaValue', ctypes.c_uint32, 27),
        ('Reserved27', ctypes.c_uint32, 5),
    ]


class REG_PLANE_POST_CSC_GAMC_DATA_ENH(ctypes.Union):
    value = 0
    offset = 0

    GammaValue = 0  # bit 0 to 27
    Reserved27 = 0  # bit 27 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_POST_CSC_GAMC_DATA_ENH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_POST_CSC_GAMC_DATA_ENH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_POST_CSC_GAMC_SEG0_DATA_ENH:
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_1_A = 0x70164
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_2_A = 0x70264
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_3_A = 0x70364
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_1_B = 0x71164
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_2_B = 0x71264
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_3_B = 0x71364
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_1_C = 0x72164
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_2_C = 0x72264
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_3_C = 0x72364
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_1_D = 0x73164
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_2_D = 0x73264
    PLANE_POST_CSC_GAMC_SEG0_DATA_ENH_3_D = 0x73364


class _PLANE_POST_CSC_GAMC_SEG0_DATA_ENH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaValue', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_PLANE_POST_CSC_GAMC_SEG0_DATA_ENH(ctypes.Union):
    value = 0
    offset = 0

    GammaValue = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_POST_CSC_GAMC_SEG0_DATA_ENH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_POST_CSC_GAMC_SEG0_DATA_ENH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_POST_CSC_GAMC_DATA:
    PLANE_POST_CSC_GAMC_DATA_4_A = 0x704DC
    PLANE_POST_CSC_GAMC_DATA_5_A = 0x705DC
    PLANE_POST_CSC_GAMC_DATA_4_B = 0x714DC
    PLANE_POST_CSC_GAMC_DATA_5_B = 0x715DC
    PLANE_POST_CSC_GAMC_DATA_4_C = 0x724DC
    PLANE_POST_CSC_GAMC_DATA_5_C = 0x725DC
    PLANE_POST_CSC_GAMC_DATA_4_D = 0x734DC
    PLANE_POST_CSC_GAMC_DATA_5_D = 0x735DC


class _PLANE_POST_CSC_GAMC_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaValue', ctypes.c_uint32, 19),
        ('Reserved19', ctypes.c_uint32, 13),
    ]


class REG_PLANE_POST_CSC_GAMC_DATA(ctypes.Union):
    value = 0
    offset = 0

    GammaValue = 0  # bit 0 to 19
    Reserved19 = 0  # bit 19 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_POST_CSC_GAMC_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_POST_CSC_GAMC_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH:
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_1_A = 0x70178
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_2_A = 0x70278
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_3_A = 0x70378
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_1_B = 0x71178
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_2_B = 0x71278
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_3_B = 0x71378
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_1_C = 0x72178
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_2_C = 0x72278
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_3_C = 0x72378
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_1_D = 0x73178
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_2_D = 0x73278
    PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH_3_D = 0x73378


class _PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BlueCoefficient', ctypes.c_uint32, 9),
        ('Reserved9', ctypes.c_uint32, 1),
        ('GreenCoefficient', ctypes.c_uint32, 9),
        ('Reserved19', ctypes.c_uint32, 1),
        ('RedCoefficient', ctypes.c_uint32, 9),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH(ctypes.Union):
    value = 0
    offset = 0

    BlueCoefficient = 0  # bit 0 to 9
    Reserved9 = 0  # bit 9 to 10
    GreenCoefficient = 0  # bit 10 to 19
    Reserved19 = 0  # bit 19 to 20
    RedCoefficient = 0  # bit 20 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_PIXEL_NORMALIZE:
    PLANE_PIXEL_NORMALIZE_1_A = 0x701A8
    PLANE_PIXEL_NORMALIZE_2_A = 0x702A8
    PLANE_PIXEL_NORMALIZE_3_A = 0x703A8
    PLANE_PIXEL_NORMALIZE_1_B = 0x711A8
    PLANE_PIXEL_NORMALIZE_2_B = 0x712A8
    PLANE_PIXEL_NORMALIZE_3_B = 0x713A8
    PLANE_PIXEL_NORMALIZE_1_C = 0x721A8
    PLANE_PIXEL_NORMALIZE_2_C = 0x722A8
    PLANE_PIXEL_NORMALIZE_3_C = 0x723A8
    PLANE_PIXEL_NORMALIZE_1_D = 0x731A8
    PLANE_PIXEL_NORMALIZE_2_D = 0x732A8
    PLANE_PIXEL_NORMALIZE_3_D = 0x733A8


class _PLANE_PIXEL_NORMALIZE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('NormalizationFactor', ctypes.c_uint32, 16),
        ('Reserved16', ctypes.c_uint32, 15),
        ('Enable', ctypes.c_uint32, 1),
    ]


class REG_PLANE_PIXEL_NORMALIZE(ctypes.Union):
    value = 0
    offset = 0

    NormalizationFactor = 0  # bit 0 to 16
    Reserved16 = 0  # bit 16 to 31
    Enable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_PIXEL_NORMALIZE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_PIXEL_NORMALIZE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_INPUT_CSC_COEFF:
    PLANE_INPUT_CSC_COEFF_1_A = 0x701E0
    PLANE_INPUT_CSC_COEFF_2_A = 0x702E0
    PLANE_INPUT_CSC_COEFF_3_A = 0x703E0
    PLANE_INPUT_CSC_COEFF_1_B = 0x711E0
    PLANE_INPUT_CSC_COEFF_2_B = 0x712E0
    PLANE_INPUT_CSC_COEFF_3_B = 0x713E0
    PLANE_INPUT_CSC_COEFF_1_C = 0x721E0
    PLANE_INPUT_CSC_COEFF_2_C = 0x722E0
    PLANE_INPUT_CSC_COEFF_3_C = 0x723E0
    PLANE_INPUT_CSC_COEFF_1_D = 0x731E0
    PLANE_INPUT_CSC_COEFF_2_D = 0x732E0
    PLANE_INPUT_CSC_COEFF_3_D = 0x733E0


class _PLANE_INPUT_CSC_COEFF(ctypes.LittleEndianStructure):
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


class REG_PLANE_INPUT_CSC_COEFF(ctypes.Union):
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
        ('bitMap', _PLANE_INPUT_CSC_COEFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_INPUT_CSC_COEFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_INPUT_CSC_PREOFF:
    PLANE_INPUT_CSC_PREOFF_1_A = 0x701F8
    PLANE_INPUT_CSC_PREOFF_2_A = 0x702F8
    PLANE_INPUT_CSC_PREOFF_3_A = 0x703F8
    PLANE_INPUT_CSC_PREOFF_1_B = 0x711F8
    PLANE_INPUT_CSC_PREOFF_2_B = 0x712F8
    PLANE_INPUT_CSC_PREOFF_3_B = 0x713F8
    PLANE_INPUT_CSC_PREOFF_1_C = 0x721F8
    PLANE_INPUT_CSC_PREOFF_2_C = 0x722F8
    PLANE_INPUT_CSC_PREOFF_3_C = 0x723F8
    PLANE_INPUT_CSC_PREOFF_1_D = 0x731F8
    PLANE_INPUT_CSC_PREOFF_2_D = 0x732F8
    PLANE_INPUT_CSC_PREOFF_3_D = 0x733F8


class _PLANE_INPUT_CSC_PREOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PrecscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_PLANE_INPUT_CSC_PREOFF(ctypes.Union):
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
        ('bitMap', _PLANE_INPUT_CSC_PREOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_INPUT_CSC_PREOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_INPUT_CSC_POSTOFF:
    PLANE_INPUT_CSC_POSTOFF_1_A = 0x70204
    PLANE_INPUT_CSC_POSTOFF_2_A = 0x70304
    PLANE_INPUT_CSC_POSTOFF_3_A = 0x70404
    PLANE_INPUT_CSC_POSTOFF_1_B = 0x71204
    PLANE_INPUT_CSC_POSTOFF_2_B = 0x71304
    PLANE_INPUT_CSC_POSTOFF_3_B = 0x71404
    PLANE_INPUT_CSC_POSTOFF_1_C = 0x72204
    PLANE_INPUT_CSC_POSTOFF_2_C = 0x72304
    PLANE_INPUT_CSC_POSTOFF_3_C = 0x72404
    PLANE_INPUT_CSC_POSTOFF_1_D = 0x73204
    PLANE_INPUT_CSC_POSTOFF_2_D = 0x73304
    PLANE_INPUT_CSC_POSTOFF_3_D = 0x73404


class _PLANE_INPUT_CSC_POSTOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PostcscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_PLANE_INPUT_CSC_POSTOFF(ctypes.Union):
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
        ('bitMap', _PLANE_INPUT_CSC_POSTOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_INPUT_CSC_POSTOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_CSC_COEFF:
    PLANE_CSC_COEFF_1_A = 0x70210
    PLANE_CSC_COEFF_2_A = 0x70310
    PLANE_CSC_COEFF_3_A = 0x70410
    PLANE_CSC_COEFF_1_B = 0x71210
    PLANE_CSC_COEFF_2_B = 0x71310
    PLANE_CSC_COEFF_3_B = 0x71410
    PLANE_CSC_COEFF_1_C = 0x72210
    PLANE_CSC_COEFF_2_C = 0x72310
    PLANE_CSC_COEFF_3_C = 0x72410
    PLANE_CSC_COEFF_1_D = 0x73210
    PLANE_CSC_COEFF_2_D = 0x73310
    PLANE_CSC_COEFF_3_D = 0x73410


class _PLANE_CSC_COEFF(ctypes.LittleEndianStructure):
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


class REG_PLANE_CSC_COEFF(ctypes.Union):
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
        ('bitMap', _PLANE_CSC_COEFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_CSC_COEFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_CSC_PREOFF:
    PLANE_CSC_PREOFF_1_A = 0x70228
    PLANE_CSC_PREOFF_2_A = 0x70328
    PLANE_CSC_PREOFF_3_A = 0x70428
    PLANE_CSC_PREOFF_1_B = 0x71228
    PLANE_CSC_PREOFF_2_B = 0x71328
    PLANE_CSC_PREOFF_3_B = 0x71428
    PLANE_CSC_PREOFF_1_C = 0x72228
    PLANE_CSC_PREOFF_2_C = 0x72328
    PLANE_CSC_PREOFF_3_C = 0x72428
    PLANE_CSC_PREOFF_1_D = 0x73228
    PLANE_CSC_PREOFF_2_D = 0x73328
    PLANE_CSC_PREOFF_3_D = 0x73428


class _PLANE_CSC_PREOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PrecscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PrecscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_PLANE_CSC_PREOFF(ctypes.Union):
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
        ('bitMap', _PLANE_CSC_PREOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_CSC_PREOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_CSC_POSTOFF:
    PLANE_CSC_POSTOFF_1_A = 0x70234
    PLANE_CSC_POSTOFF_2_A = 0x70334
    PLANE_CSC_POSTOFF_3_A = 0x70434
    PLANE_CSC_POSTOFF_1_B = 0x71234
    PLANE_CSC_POSTOFF_2_B = 0x71334
    PLANE_CSC_POSTOFF_3_B = 0x71434
    PLANE_CSC_POSTOFF_1_C = 0x72234
    PLANE_CSC_POSTOFF_2_C = 0x72334
    PLANE_CSC_POSTOFF_3_C = 0x72434
    PLANE_CSC_POSTOFF_1_D = 0x73234
    PLANE_CSC_POSTOFF_2_D = 0x73334
    PLANE_CSC_POSTOFF_3_D = 0x73434


class _PLANE_CSC_POSTOFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PostcscHighOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscMediumOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
        ('PostcscLowOffset', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 19),
    ]


class REG_PLANE_CSC_POSTOFF(ctypes.Union):
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
        ('bitMap', _PLANE_CSC_POSTOFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_CSC_POSTOFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_POWER_GATE_DISABLE(Enum):
    POWER_GATE_ENABLE = 0x0
    POWER_GATE_DISABLE = 0x1


class ENUM_VERT_INITIAL_PHASE(Enum):
    VERT_INITIAL_PHASE_0 = 0x0
    VERT_INITIAL_PHASE_0_25 = 0x1
    VERT_INITIAL_PHASE_0_5 = 0x2


class ENUM_VERT_INITIAL_PHASE_SIGN(Enum):
    VERT_INITIAL_PHASE_SIGN_POSITIVE_INITIAL_PHASE = 0x0
    VERT_INITIAL_PHASE_SIGN_NEGATIVE_INITIAL_PHASE = 0x1


class ENUM_HORZ_INITIAL_PHASE(Enum):
    HORZ_INITIAL_PHASE_0 = 0x0
    HORZ_INITIAL_PHASE_0_25 = 0x1
    HORZ_INITIAL_PHASE_0_5 = 0x2


class ENUM_HORZ_INITIAL_PHASE_SIGN(Enum):
    HORZ_INITIAL_PHASE_SIGN_POSITIVE_INITIAL_PHASE = 0x0
    HORZ_INITIAL_PHASE_SIGN_NEGATIVE_INITIAL_PHASE = 0x1


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


class ENUM_Y_BINDING(Enum):
    Y_BINDING_PLANE_4 = 0x0
    Y_BINDING_PLANE_5 = 0x1


class ENUM_CHROMA_UPSAMPLER_ENABLE(Enum):
    CHROMA_UPSAMPLER_DISABLE = 0x0
    CHROMA_UPSAMPLER_ENABLE = 0x1


class OFFSET_PLANE_CUS_CTL:
    PLANE_CUS_CTL_1_A = 0x701C8
    PLANE_CUS_CTL_2_A = 0x702C8
    PLANE_CUS_CTL_3_A = 0x703C8
    PLANE_CUS_CTL_1_B = 0x711C8
    PLANE_CUS_CTL_2_B = 0x712C8
    PLANE_CUS_CTL_3_B = 0x713C8
    PLANE_CUS_CTL_1_C = 0x721C8
    PLANE_CUS_CTL_2_C = 0x722C8
    PLANE_CUS_CTL_3_C = 0x723C8
    PLANE_CUS_CTL_1_D = 0x731C8
    PLANE_CUS_CTL_2_D = 0x732C8
    PLANE_CUS_CTL_3_D = 0x733C8


class _PLANE_CUS_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PowerUpInProgress', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 3),
        ('EccDoubleError', ctypes.c_uint32, 1),
        ('EccSingleError', ctypes.c_uint32, 1),
        ('Reserved6', ctypes.c_uint32, 2),
        ('EccBypass', ctypes.c_uint32, 1),
        ('PowerUpDelay', ctypes.c_uint32, 2),
        ('PowerGateDisable', ctypes.c_uint32, 1),
        ('VertInitialPhase', ctypes.c_uint32, 2),
        ('Reserved14', ctypes.c_uint32, 1),
        ('VertInitialPhaseSign', ctypes.c_uint32, 1),
        ('HorzInitialPhase', ctypes.c_uint32, 2),
        ('Reserved18', ctypes.c_uint32, 1),
        ('HorzInitialPhaseSign', ctypes.c_uint32, 1),
        ('ErrorInjectionFlipBits', ctypes.c_uint32, 2),
        ('Reserved22', ctypes.c_uint32, 1),
        ('EccErrorInjectionEnable', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 6),
        ('YBinding', ctypes.c_uint32, 1),
        ('ChromaUpsamplerEnable', ctypes.c_uint32, 1),
    ]


class REG_PLANE_CUS_CTL(ctypes.Union):
    value = 0
    offset = 0

    PowerUpInProgress = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 4
    EccDoubleError = 0  # bit 4 to 5
    EccSingleError = 0  # bit 5 to 6
    Reserved6 = 0  # bit 6 to 8
    EccBypass = 0  # bit 8 to 9
    PowerUpDelay = 0  # bit 9 to 11
    PowerGateDisable = 0  # bit 11 to 12
    VertInitialPhase = 0  # bit 12 to 14
    Reserved14 = 0  # bit 14 to 15
    VertInitialPhaseSign = 0  # bit 15 to 16
    HorzInitialPhase = 0  # bit 16 to 18
    Reserved18 = 0  # bit 18 to 19
    HorzInitialPhaseSign = 0  # bit 19 to 20
    ErrorInjectionFlipBits = 0  # bit 20 to 22
    Reserved22 = 0  # bit 22 to 23
    EccErrorInjectionEnable = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 30
    YBinding = 0  # bit 30 to 31
    ChromaUpsamplerEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_CUS_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_CUS_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_GLOBAL_DOUBLE_BUFFER_UPDATE_DISABLE(Enum):
    GLOBAL_DOUBLE_BUFFER_UPDATE_DISABLE_NOT_DISABLED = 0x0
    GLOBAL_DOUBLE_BUFFER_UPDATE_DISABLED = 0x1


class ENUM_PIPE_DB_STALL_A(Enum):
    PIPE_DB_STALL_A_NOT_STALLED = 0x0
    PIPE_DB_STALL_A_STALLED = 0x1


class ENUM_PIPE_DB_STALL_B(Enum):
    PIPE_DB_STALL_B_NOT_STALLED = 0x0
    PIPE_DB_STALL_B_STALLED = 0x1


class ENUM_PIPE_DB_STALL_C(Enum):
    PIPE_DB_STALL_C_NOT_STALLED = 0x0
    PIPE_DB_STALL_C_STALLED = 0x1


class ENUM_PIPE_DB_STALL_D(Enum):
    PIPE_DB_STALL_D_NOT_STALLED = 0x0
    PIPE_DB_STALL_D_STALLED = 0x1


class OFFSET_DOUBLE_BUFFER_CTL:
    DOUBLE_BUFFER_CTL = 0x44500


class _DOUBLE_BUFFER_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GlobalDoubleBufferUpdateDisable', ctypes.c_uint32, 1),
        ('Reserved1', ctypes.c_uint32, 3),
        ('PipeDbStallA', ctypes.c_uint32, 1),
        ('PipeDbStallB', ctypes.c_uint32, 1),
        ('PipeDbStallC', ctypes.c_uint32, 1),
        ('PipeDbStallD', ctypes.c_uint32, 1),
        ('Reserved8', ctypes.c_uint32, 24),
    ]


class REG_DOUBLE_BUFFER_CTL(ctypes.Union):
    value = 0
    offset = 0

    GlobalDoubleBufferUpdateDisable = 0  # bit 0 to 1
    Reserved1 = 0  # bit 1 to 4
    PipeDbStallA = 0  # bit 4 to 5
    PipeDbStallB = 0  # bit 5 to 6
    PipeDbStallC = 0  # bit 6 to 7
    PipeDbStallD = 0  # bit 7 to 8
    Reserved8 = 0  # bit 8 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _DOUBLE_BUFFER_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_DOUBLE_BUFFER_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_PLANE_CC_VAL:
    PLANE_CC_VAL_1_A = 0x701B4
    PLANE_CC_VAL_2_A = 0x702B4
    PLANE_CC_VAL_3_A = 0x703B4
    PLANE_CC_VAL_4_A = 0x704B4
    PLANE_CC_VAL_5_A = 0x705B4
    PLANE_CC_VAL_1_B = 0x711B4
    PLANE_CC_VAL_2_B = 0x712B4
    PLANE_CC_VAL_3_B = 0x713B4
    PLANE_CC_VAL_4_B = 0x714B4
    PLANE_CC_VAL_5_B = 0x715B4
    PLANE_CC_VAL_1_C = 0x721B4
    PLANE_CC_VAL_2_C = 0x722B4
    PLANE_CC_VAL_3_C = 0x723B4
    PLANE_CC_VAL_4_C = 0x724B4
    PLANE_CC_VAL_5_C = 0x725B4
    PLANE_CC_VAL_1_D = 0x731B4
    PLANE_CC_VAL_2_D = 0x732B4
    PLANE_CC_VAL_3_D = 0x733B4
    PLANE_CC_VAL_4_D = 0x734B4
    PLANE_CC_VAL_5_D = 0x735B4


class _PLANE_CC_VAL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ClearColorValueDw0', ctypes.c_uint32, 32),
    ]


class REG_PLANE_CC_VAL(ctypes.Union):
    value = 0
    offset = 0

    ClearColorValueDw0 = 0  # bit 0 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_CC_VAL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_CC_VAL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SMOOTH_SYNC_DITHER_STEP_SIZE(Enum):
    SMOOTH_SYNC_DITHER_STEP_SIZE_STEP_SIZE_OF_1 = 0x0
    SMOOTH_SYNC_DITHER_STEP_SIZE_STEP_SIZE_OF_2 = 0x1
    SMOOTH_SYNC_DITHER_STEP_SIZE_STEP_SIZE_OF_4 = 0x2
    SMOOTH_SYNC_DITHER_STEP_SIZE_STEP_SIZE_OF_8 = 0x3
    SMOOTH_SYNC_DITHER_STEP_SIZE_STEP_SIZE_OF_16 = 0x4


class ENUM_ALPHA_MODE(Enum):
    ALPHA_MODE_DISABLE = 0x0  # Alpha channel ignored.
    ALPHA_MODE_ENABLE_WITH_SW_PREMULTIPLY = 0x2  # Alpha channel used. Color channels should be pre-multiplied with alp
                                                 # ha by software.
    ALPHA_MODE_ENABLE_WITH_HW_PREMULTIPLY = 0x3  # Alpha channel used. Color channels will be pre-multiplied with alpha
                                                 #  by hardware.


class ENUM_COLOR_CORRECTION_DITHERING_ENABLE(Enum):
    COLOR_CORRECTION_DITHERING_DISABLED = 0x0
    COLOR_CORRECTION_DITHERING_ENABLED = 0x1


class ENUM_PLANE_GAMMA_MULTIPLIER_PRECISION(Enum):
    PLANE_GAMMA_MULTIPLIER_PRECISION_U0_24 = 0x0
    PLANE_GAMMA_MULTIPLIER_PRECISION_U8_16 = 0x1


class ENUM_PLANE_GAMMA_MODE(Enum):
    PLANE_GAMMA_MODE_DIRECT = 0x0  # Direct mode is used for regular plane gamma programming. Lookup is based on incomi
                                   # ng pixel individual r, g, b values. The output is a computed by lookup of two
                                   # nearest points and interpolation.
    PLANE_GAMMA_MODE_MULTIPLY = 0x1  # Multiplymode is used when plane gamma is used for HDR tone mapping. The lookup i
                                     # s based on the lunminance of the incoming pixel where the luminance is
                                     # calculated using the following equation: luma = (Kr  red) + (Kg  green) + (Kb
                                     #  blue) The coefficients (K) used to determine the lumanence are programmable
                                     # from the LM_LUMA_COEFF / PLANE_POST_CSC_GAMC_LUMA_COEFF_ENH registers. An
                                     # adjustment factor 'F' is computed by lookup of two nearest points and
                                     # interpolation. Output is computed by multiplying each color channel with the
                                     # adjustment factor F.


class ENUM_PLANE_GAMMA_DISABLE(Enum):
    PLANE_GAMMA_DISABLE = 0x1
    PLANE_GAMMA_ENABLE = 0x0


class ENUM_PLANE_PRE_CSC_GAMMA_ENABLE(Enum):
    PLANE_PRE_CSC_GAMMA_ENABLE = 0x1
    PLANE_PRE_CSC_GAMMA_DISABLE = 0x0


class ENUM_PLANE_POST_CSC_GAMMA_MULTI_SEGMENT_ENABLE(Enum):
    PLANE_POST_CSC_GAMMA_MULTI_SEGMENT_ENABLE = 0x1
    PLANE_POST_CSC_GAMMA_MULTI_SEGMENT_DISABLE = 0x0


class ENUM_PLANE_CSC_MODE(Enum):
    PLANE_CSC_MODE_BYPASS = 0x0  # Pixel data bypasses the plane color space conversion
    PLANE_CSC_MODE_YUV601_TO_RGB601 = 0x1  # YUV BT.601 to RGB BT.601 conversion.
    PLANE_CSC_MODE_YUV709_TO_RGB709 = 0x2  # YUV BT.709 to RGB BT.709 conversion.
    PLANE_CSC_MODE_YUV2020_TO_RGB2020 = 0x3  # YUV BT.2020 to RGB BT.2020 conversion.
    PLANE_CSC_MODE_RGB709_TO_RGB2020 = 0x4  # RGB BT.709 to RGB BT.2020 conversion.


class ENUM_PLANE_INPUT_CSC_ENABLE(Enum):
    PLANE_INPUT_CSC_DISABLE = 0x0
    PLANE_INPUT_CSC_ENABLE = 0x1


class ENUM_PLANE_CSC_ENABLE(Enum):
    PLANE_CSC_DISABLE = 0x0
    PLANE_CSC_ENABLE = 0x1


class ENUM_YUV_RANGE_CORRECTION_OUTPUT(Enum):
    YUV_RANGE_CORRECTION_OUTPUT_WITH_OFFSET = 0x0
    YUV_RANGE_CORRECTION_OUTPUT_WITHOUT_OFFSET = 0x1


class ENUM_PIPE_CSC_ENABLE(Enum):
    PIPE_CSC_DISABLE = 0x0
    PIPE_CSC_ENABLE = 0x1


class ENUM_YUV_RANGE_CORRECTION_DISABLE(Enum):
    YUV_RANGE_CORRECTION_ENABLE = 0x0
    YUV_RANGE_CORRECTION_DISABLE = 0x1


class ENUM_REMOVE_YUV_OFFSET(Enum):
    REMOVE_YUV_OFFSET_REMOVE = 0x0  # Remove 1/2 offset on UV components
    REMOVE_YUV_OFFSET_PRESERVE = 0x1  # Preserve 1/2 offset on UV components


class ENUM_PIPE_GAMMA_ENABLE(Enum):
    PIPE_GAMMA_DISABLE = 0x0
    PIPE_GAMMA_ENABLE = 0x1


class OFFSET_PLANE_COLOR_CTL:
    PLANE_COLOR_CTL_1_A = 0x701CC
    PLANE_COLOR_CTL_2_A = 0x702CC
    PLANE_COLOR_CTL_3_A = 0x703CC
    PLANE_COLOR_CTL_4_A = 0x704CC
    PLANE_COLOR_CTL_5_A = 0x705CC
    PLANE_COLOR_CTL_1_B = 0x711CC
    PLANE_COLOR_CTL_2_B = 0x712CC
    PLANE_COLOR_CTL_3_B = 0x713CC
    PLANE_COLOR_CTL_4_B = 0x714CC
    PLANE_COLOR_CTL_5_B = 0x715CC
    PLANE_COLOR_CTL_1_C = 0x721CC
    PLANE_COLOR_CTL_2_C = 0x722CC
    PLANE_COLOR_CTL_3_C = 0x723CC
    PLANE_COLOR_CTL_4_C = 0x724CC
    PLANE_COLOR_CTL_5_C = 0x725CC
    PLANE_COLOR_CTL_1_D = 0x731CC
    PLANE_COLOR_CTL_2_D = 0x732CC
    PLANE_COLOR_CTL_3_D = 0x733CC
    PLANE_COLOR_CTL_4_D = 0x734CC
    PLANE_COLOR_CTL_5_D = 0x735CC


class _PLANE_COLOR_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SmoothSyncDitherStepSize', ctypes.c_uint32, 3),
        ('Reserved3', ctypes.c_uint32, 1),
        ('AlphaMode', ctypes.c_uint32, 2),
        ('Reserved6', ctypes.c_uint32, 4),
        ('ColorCorrectionDitheringEnable', ctypes.c_uint32, 1),
        ('PlaneGammaMultiplierPrecision', ctypes.c_uint32, 1),
        ('PlaneGammaMode', ctypes.c_uint32, 1),
        ('PlaneGammaDisable', ctypes.c_uint32, 1),
        ('PlanePreCscGammaEnable', ctypes.c_uint32, 1),
        ('PlanePostCscGammaMultiSegmentEnable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 1),
        ('PlaneCscMode', ctypes.c_uint32, 3),
        ('PlaneInputCscEnable', ctypes.c_uint32, 1),
        ('PlaneCscEnable', ctypes.c_uint32, 1),
        ('YuvRangeCorrectionOutput', ctypes.c_uint32, 1),
        ('PipeCscEnable', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 4),
        ('YuvRangeCorrectionDisable', ctypes.c_uint32, 1),
        ('RemoveYuvOffset', ctypes.c_uint32, 1),
        ('PipeGammaEnable', ctypes.c_uint32, 1),
        ('Reserved31', ctypes.c_uint32, 1),
    ]


class REG_PLANE_COLOR_CTL(ctypes.Union):
    value = 0
    offset = 0

    SmoothSyncDitherStepSize = 0  # bit 0 to 3
    Reserved3 = 0  # bit 3 to 4
    AlphaMode = 0  # bit 4 to 6
    Reserved6 = 0  # bit 6 to 10
    ColorCorrectionDitheringEnable = 0  # bit 10 to 11
    PlaneGammaMultiplierPrecision = 0  # bit 11 to 12
    PlaneGammaMode = 0  # bit 12 to 13
    PlaneGammaDisable = 0  # bit 13 to 14
    PlanePreCscGammaEnable = 0  # bit 14 to 15
    PlanePostCscGammaMultiSegmentEnable = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 17
    PlaneCscMode = 0  # bit 17 to 20
    PlaneInputCscEnable = 0  # bit 20 to 21
    PlaneCscEnable = 0  # bit 21 to 22
    YuvRangeCorrectionOutput = 0  # bit 22 to 23
    PipeCscEnable = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 28
    YuvRangeCorrectionDisable = 0  # bit 28 to 29
    RemoveYuvOffset = 0  # bit 29 to 30
    PipeGammaEnable = 0  # bit 30 to 31
    Reserved31 = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _PLANE_COLOR_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_PLANE_COLOR_CTL, self).__init__()
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


class ENUM_GAMMA_ENABLE(Enum):
    GAMMA_DISABLE = 0x0
    GAMMA_ENABLE = 0x1


class OFFSET_CUR_CTL:
    CUR_CTL_A = 0x70080
    SEL_FETCH_CUR_CTL_A = 0x70880
    CUR_CTL_B = 0x71080
    SEL_FETCH_CUR_CTL_B = 0x71880
    CUR_CTL_C = 0x72080
    SEL_FETCH_CUR_CTL_C = 0x72880
    CUR_CTL_D = 0x73080
    SEL_FETCH_CUR_CTL_D = 0x73880


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
        ('AllowDbStall', ctypes.c_uint32, 1),
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
    AllowDbStall = 0  # bit 23 to 24
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


class OFFSET_CUR_BASE:
    CUR_BASE_A = 0x70084
    CUR_BASE_B = 0x71084
    CUR_BASE_C = 0x72084
    CUR_BASE_D = 0x73084


class _CUR_BASE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 2),
        ('DecryptionRequest', ctypes.c_uint32, 1),
        ('Reserved3', ctypes.c_uint32, 1),
        ('KeySelect', ctypes.c_uint32, 3),
        ('Reserved7', ctypes.c_uint32, 4),
        ('VrrMasterFlip', ctypes.c_uint32, 1),
        ('CursorBase', ctypes.c_uint32, 20),
    ]


class REG_CUR_BASE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 2
    DecryptionRequest = 0  # bit 2 to 3
    Reserved3 = 0  # bit 3 to 4
    KeySelect = 0  # bit 4 to 7
    Reserved7 = 0  # bit 7 to 11
    VrrMasterFlip = 0  # bit 11 to 12
    CursorBase = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CUR_BASE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_BASE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CUR_POS:
    CUR_POS_A = 0x70088
    CUR_POS_B = 0x71088
    CUR_POS_C = 0x72088
    CUR_POS_D = 0x73088


class _CUR_POS(ctypes.LittleEndianStructure):
    _fields_ = [
        ('XPositionMagnitude', ctypes.c_uint32, 13),
        ('Reserved13', ctypes.c_uint32, 2),
        ('XPositionSign', ctypes.c_uint32, 1),
        ('YPositionMagnitude', ctypes.c_uint32, 13),
        ('Reserved29', ctypes.c_uint32, 2),
        ('YPositionSign', ctypes.c_uint32, 1),
    ]


class REG_CUR_POS(ctypes.Union):
    value = 0
    offset = 0

    XPositionMagnitude = 0  # bit 0 to 13
    Reserved13 = 0  # bit 13 to 15
    XPositionSign = 0  # bit 15 to 16
    YPositionMagnitude = 0  # bit 16 to 29
    Reserved29 = 0  # bit 29 to 31
    YPositionSign = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CUR_POS),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_POS, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CUR_PAL:
    CUR_PAL_0_A = 0x70090
    CUR_PAL_1_A = 0x70094
    CUR_PAL_2_A = 0x70098
    CUR_PAL_3_A = 0x7009C
    CUR_PAL_0_B = 0x71090
    CUR_PAL_1_B = 0x71094
    CUR_PAL_2_B = 0x71098
    CUR_PAL_3_B = 0x7109C
    CUR_PAL_0_C = 0x72090
    CUR_PAL_1_C = 0x72094
    CUR_PAL_2_C = 0x72098
    CUR_PAL_3_C = 0x7209C
    CUR_PAL_0_D = 0x73090
    CUR_PAL_1_D = 0x73094
    CUR_PAL_2_D = 0x73098
    CUR_PAL_3_D = 0x7309C


class _CUR_PAL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PaletteBlue', ctypes.c_uint32, 8),
        ('PaletteGreen', ctypes.c_uint32, 8),
        ('PaletteRed', ctypes.c_uint32, 8),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_CUR_PAL(ctypes.Union):
    value = 0
    offset = 0

    PaletteBlue = 0  # bit 0 to 8
    PaletteGreen = 0  # bit 8 to 16
    PaletteRed = 0  # bit 16 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CUR_PAL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_PAL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CUR_SURFLIVE:
    CUR_SURFLIVE_A = 0x700AC
    CUR_SURFLIVE_B = 0x710AC
    CUR_SURFLIVE_C = 0x720AC
    CUR_SURFLIVE_D = 0x730AC


class _CUR_SURFLIVE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('LiveSurfaceBaseAddress', ctypes.c_uint32, 20),
    ]


class REG_CUR_SURFLIVE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    LiveSurfaceBaseAddress = 0  # bit 12 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CUR_SURFLIVE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_SURFLIVE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SIZE_REDUCTION_ENABLE(Enum):
    SIZE_REDUCTION_DISABLE = 0x0
    SIZE_REDUCTION_ENABLE = 0x1


class OFFSET_CUR_FBC_CTL:
    CUR_FBC_CTL_A = 0x700A0
    CUR_FBC_CTL_B = 0x710A0
    CUR_FBC_CTL_C = 0x720A0
    CUR_FBC_CTL_D = 0x730A0


class _CUR_FBC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ReducedScanLines', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 23),
        ('SizeReductionEnable', ctypes.c_uint32, 1),
    ]


class REG_CUR_FBC_CTL(ctypes.Union):
    value = 0
    offset = 0

    ReducedScanLines = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 31
    SizeReductionEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CUR_FBC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_FBC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_TONE_MAPPING_ENABLE(Enum):
    TONE_MAPPING_ENABLE = 0x1
    TONE_MAPPING_DISABLE = 0x0


class OFFSET_CUR_COLOR_CTL:
    CUR_COLOR_CTL_A = 0x700C0
    CUR_COLOR_CTL_B = 0x710C0
    CUR_COLOR_CTL_C = 0x720C0
    CUR_COLOR_CTL_D = 0x730C0


class _CUR_COLOR_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ToneMappingFactor', ctypes.c_uint32, 10),
        ('Reserved10', ctypes.c_uint32, 5),
        ('ToneMappingEnable', ctypes.c_uint32, 1),
        ('Reserved16', ctypes.c_uint32, 16),
    ]


class REG_CUR_COLOR_CTL(ctypes.Union):
    value = 0
    offset = 0

    ToneMappingFactor = 0  # bit 0 to 10
    Reserved10 = 0  # bit 10 to 15
    ToneMappingEnable = 0  # bit 15 to 16
    Reserved16 = 0  # bit 16 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CUR_COLOR_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_COLOR_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CUR_CSC_COEFF:
    CUR_CSC_COEFF_A = 0x700D0
    CUR_CSC_COEFF_B = 0x710D0
    CUR_CSC_COEFF_C = 0x720D0
    CUR_CSC_COEFF_D = 0x730D0


class _CUR_CSC_COEFF(ctypes.LittleEndianStructure):
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


class REG_CUR_CSC_COEFF(ctypes.Union):
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
        ('bitMap', _CUR_CSC_COEFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_CSC_COEFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CUR_PRE_CSC_GAMC_INDEX:
    CUR_PRE_CSC_GAMMA_INDEX_A = 0x700B0
    CUR_PRE_CSC_GAMMA_INDEX_B = 0x710B0
    CUR_PRE_CSC_GAMMA_INDEX_C = 0x720B0
    CUR_PRE_CSC_GAMMA_INDEX_D = 0x730B0


class _CUR_PRE_CSC_GAMC_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 6),
        ('Reserved6', ctypes.c_uint32, 4),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 21),
    ]


class REG_CUR_PRE_CSC_GAMC_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 6
    Reserved6 = 0  # bit 6 to 10
    IndexAutoIncrement = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CUR_PRE_CSC_GAMC_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_PRE_CSC_GAMC_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_CUR_PRE_CSC_GAMC_DATA:
    CUR_PRE_CSC_GAMMA_DATA_A = 0x700B4
    CUR_PRE_CSC_GAMMA_DATA_B = 0x710B4
    CUR_PRE_CSC_GAMMA_DATA_C = 0x720B4
    CUR_PRE_CSC_GAMMA_DATA_D = 0x730B4


class _CUR_PRE_CSC_GAMC_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('GammaValue', ctypes.c_uint32, 19),
        ('Reserved19', ctypes.c_uint32, 13),
    ]


class REG_CUR_PRE_CSC_GAMC_DATA(ctypes.Union):
    value = 0
    offset = 0

    GammaValue = 0  # bit 0 to 19
    Reserved19 = 0  # bit 19 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _CUR_PRE_CSC_GAMC_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_CUR_PRE_CSC_GAMC_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_BLINK_DUTY_CYCLE(Enum):
    BLINK_DUTY_CYCLE_100 = 0x0  # 100% Duty Cycle, Full Cursor Rate
    BLINK_DUTY_CYCLE_25 = 0x1  # 25% Duty Cycle, 1/2 Cursor Rate
    BLINK_DUTY_CYCLE_50 = 0x2  # 50% Duty Cycle, 1/2 Cursor Rate
    BLINK_DUTY_CYCLE_75 = 0x3  # 75% Duty Cycle, 1/2 Cursor Rate


class ENUM_VGA_BLANK_THROTTLING_BLANK(Enum):
    VGA_BLANK_THROTTLING_BLANK_50_DEFAULT = 0x9
    VGA_BLANK_THROTTLING_BLANK_50 = 0x1
    VGA_BLANK_THROTTLING_BLANK_33 = 0x2
    VGA_BLANK_THROTTLING_BLANK_25 = 0x3
    VGA_BLANK_THROTTLING_BLANK_20 = 0x4
    VGA_BLANK_THROTTLING_BLANK_17 = 0x5
    VGA_BLANK_THROTTLING_BLANK_15 = 0x6
    VGA_BLANK_THROTTLING_BLANK_10 = 0x7
    VGA_BLANK_THROTTLING_BLANK_66 = 0xA
    VGA_BLANK_THROTTLING_BLANK_75 = 0xB
    VGA_BLANK_THROTTLING_BLANK_80 = 0xC
    VGA_BLANK_THROTTLING_BLANK_90 = 0xD
    VGA_BLANK_THROTTLING_BLANK_85 = 0xE
    VGA_BLANK_THROTTLING_BLANK_82 = 0xF


class ENUM_VGA_DE_THROTTLING(Enum):
    VGA_DE_THROTTLING_33 = 0x2
    VGA_DE_THROTTLING_25 = 0x3
    VGA_DE_THROTTLING_20 = 0x4
    VGA_DE_THROTTLING_17 = 0x5
    VGA_DE_THROTTLING_15 = 0x6
    VGA_DE_THROTTLING_10 = 0x7
    VGA_DE_THROTTLING_66 = 0xA
    VGA_DE_THROTTLING_75 = 0xB
    VGA_DE_THROTTLING_80 = 0xC
    VGA_DE_THROTTLING_90 = 0xD
    VGA_DE_THROTTLING_85 = 0xE
    VGA_DE_THROTTLING_82 = 0xF


class ENUM_NINE_DOT_DISABLE(Enum):
    NINE_DOT_DISABLE_9_DOT = 0x0  # Allow use of 9-dot enable bit in VGA registers
    NINE_DOT_DISABLE_8_DOT = 0x1  # Ignore the 9-dot per character bit and always use 8


class ENUM_PALETTE_BYPASS(Enum):
    PALETTE_BYPASS_PASS = 0x0
    PALETTE_BYPASS_BYPASS = 0x1


class ENUM_LEGACY_8BIT_PALETTE_EN(Enum):
    LEGACY_8BIT_PALETTE_EN_6_BIT_DAC = 0x0
    LEGACY_8BIT_PALETTE_EN_8_BIT_DAC = 0x1


class ENUM_VGA_BORDER_ENABLE(Enum):
    VGA_BORDER_DISABLE = 0x0
    VGA_BORDER_ENABLE = 0x1


class ENUM_VGA_DISPLAY_DISABLE(Enum):
    VGA_DISPLAY_ENABLE = 0x0
    VGA_DISPLAY_DISABLE = 0x1


class OFFSET_VGA_CONTROL:
    VGA_CONTROL = 0x41000


class _VGA_CONTROL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('VsyncBlinkRate', ctypes.c_uint32, 6),
        ('BlinkDutyCycle', ctypes.c_uint32, 2),
        ('VgaBlankThrottlingBlank', ctypes.c_uint32, 4),
        ('VgaDeThrottling', ctypes.c_uint32, 4),
        ('Reserved16', ctypes.c_uint32, 2),
        ('NineDotDisable', ctypes.c_uint32, 1),
        ('PaletteBypass', ctypes.c_uint32, 1),
        ('Legacy8BitPaletteEn', ctypes.c_uint32, 1),
        ('Reserved21', ctypes.c_uint32, 3),
        ('PipeCscEnable', ctypes.c_uint32, 1),
        ('DbufClockGate', ctypes.c_uint32, 1),
        ('VgaBorderEnable', ctypes.c_uint32, 1),
        ('Reserved27', ctypes.c_uint32, 4),
        ('VgaDisplayDisable', ctypes.c_uint32, 1),
    ]


class REG_VGA_CONTROL(ctypes.Union):
    value = 0
    offset = 0

    VsyncBlinkRate = 0  # bit 0 to 6
    BlinkDutyCycle = 0  # bit 6 to 8
    VgaBlankThrottlingBlank = 0  # bit 8 to 12
    VgaDeThrottling = 0  # bit 12 to 16
    Reserved16 = 0  # bit 16 to 18
    NineDotDisable = 0  # bit 18 to 19
    PaletteBypass = 0  # bit 19 to 20
    Legacy8BitPaletteEn = 0  # bit 20 to 21
    Reserved21 = 0  # bit 21 to 24
    PipeCscEnable = 0  # bit 24 to 25
    DbufClockGate = 0  # bit 25 to 26
    VgaBorderEnable = 0  # bit 26 to 27
    Reserved27 = 0  # bit 27 to 31
    VgaDisplayDisable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VGA_CONTROL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VGA_CONTROL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_DBUF_FRAME_RESET(Enum):
    DBUF_FRAME_RESET_DISABLE_RESET_OF_DBUF_ONCE_EACH_VGA_FRAME = 0x1
    DBUF_FRAME_RESET_ENABLE_RESET_OF_DBUF_ONCE_EACH_VGA_FRAME = 0x0


class ENUM_BLANK_STAT_ENABLE(Enum):
    BLANK_STAT_DISABLE_VGA_BLANK_STAT_DURING_HIRES_MODES = 0x0
    BLANK_STAT_ENABLE_VGA_BLANK_STAT_DURING_HIRES_MODES = 0x1


class ENUM__409_STALLREQ_DISABLE(Enum):
    _409_STALLREQ_ENABLE = 0x0  # Threshold stall does not make request go low to 409 mux
    _409_STALLREQ_DISABLE = 0x1  # Threshold stall makes request go low to 409 mux


class ENUM_FLUSH_ONFRAMESTART_DISABLE(Enum):
    FLUSH_ONFRAMESTART_ENABLE_VGA_FLUSH_ON_FRAMESTART = 0x0
    FLUSH_ONFRAMESTART_DISABLE_VGA_FLUSH_ON_FRAMESTART = 0x1


class ENUM_VGA_IO_THROUGH_MMIO_DISABLE(Enum):
    VGA_IO_THROUGH_MMIO_ENABLE = 0x0
    VGA_IO_THROUGH_MMIO_DISABLE = 0x1


class ENUM_PAGEMODE_DEBUG(Enum):
    PAGEMODE_DEBUG_DISABLE = 0x0
    PAGEMODE_DEBUG_ENABLE = 0x1


class ENUM_GATE_VRD_REQUESTS(Enum):
    GATE_VRD_REQUESTS_DISABLE = 0x0
    GATE_VRD_REQUESTS_ENABLE = 0x1


class ENUM_SCREENOFF_FORCE(Enum):
    SCREENOFF_FORCE_NO_FORCE = 0x0
    SCREENOFF_FORCE_FORCE_SCREENOFF = 0x1


class ENUM_FIFO_EMPTY_FIX_SELECT(Enum):
    FIFO_EMPTY_FIX_SELECT_VRD_CI_RREQ = 0x0  # Wait for request to go low
    FIFO_EMPTY_FIX_SELECT_COUNT_COMPARATOR = 0x1  # Wait for certain number of requests


class ENUM_CR_RESET_DISABLE(Enum):
    CR_RESET_ENABLE = 0x0
    CR_RESET_DISABLE = 0x1


class ENUM_CR12_WRITE_COUNTER_RESET(Enum):
    CR12_WRITE_COUNTER_RESET_DISABLE = 0x0
    CR12_WRITE_COUNTER_RESET_ENABLE = 0x1


class ENUM_REQUEST_STALL_THRESHOLD(Enum):
    REQUEST_STALL_THRESHOLD_128_64_CL = 0x0
    REQUEST_STALL_THRESHOLD_64_32_CL = 0x1
    REQUEST_STALL_THRESHOLD_48_24_CL = 0x2
    REQUEST_STALL_THRESHOLD_32_16_CL = 0x3


class ENUM_REQUEST_STALL_DISABLE(Enum):
    REQUEST_STALL_DISABLE_VGA_REQUEST_STALL_THRESHOLD = 0x1
    REQUEST_STALL_ENABLE_VGA_REQUEST_STALL_THRESHOLD = 0x0


class OFFSET_VGA_DEBUG:
    VGA_DEBUG = 0x41004


class _VGA_DEBUG(ctypes.LittleEndianStructure):
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
        ('DbufFrameReset', ctypes.c_uint32, 1),
        ('BlankStatEnable', ctypes.c_uint32, 1),
        ('_409StallreqDisable', ctypes.c_uint32, 1),
        ('FlushOnframestartDisable', ctypes.c_uint32, 1),
        ('Spare14', ctypes.c_uint32, 1),
        ('Spare15', ctypes.c_uint32, 1),
        ('Spare16', ctypes.c_uint32, 1),
        ('Spare17', ctypes.c_uint32, 1),
        ('Spare18', ctypes.c_uint32, 1),
        ('Spare19', ctypes.c_uint32, 1),
        ('VgaIoThroughMmioDisable', ctypes.c_uint32, 1),
        ('PagemodeDebug', ctypes.c_uint32, 1),
        ('GateVrdRequests', ctypes.c_uint32, 1),
        ('ScreenoffForce', ctypes.c_uint32, 1),
        ('Reserved24', ctypes.c_uint32, 2),
        ('FifoEmptyFixSelect', ctypes.c_uint32, 1),
        ('CrResetDisable', ctypes.c_uint32, 1),
        ('Cr12WriteCounterReset', ctypes.c_uint32, 1),
        ('RequestStallThreshold', ctypes.c_uint32, 2),
        ('RequestStallDisable', ctypes.c_uint32, 1),
    ]


class REG_VGA_DEBUG(ctypes.Union):
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
    DbufFrameReset = 0  # bit 10 to 11
    BlankStatEnable = 0  # bit 11 to 12
    _409StallreqDisable = 0  # bit 12 to 13
    FlushOnframestartDisable = 0  # bit 13 to 14
    Spare14 = 0  # bit 14 to 15
    Spare15 = 0  # bit 15 to 16
    Spare16 = 0  # bit 16 to 17
    Spare17 = 0  # bit 17 to 18
    Spare18 = 0  # bit 18 to 19
    Spare19 = 0  # bit 19 to 20
    VgaIoThroughMmioDisable = 0  # bit 20 to 21
    PagemodeDebug = 0  # bit 21 to 22
    GateVrdRequests = 0  # bit 22 to 23
    ScreenoffForce = 0  # bit 23 to 24
    Reserved24 = 0  # bit 24 to 26
    FifoEmptyFixSelect = 0  # bit 26 to 27
    CrResetDisable = 0  # bit 27 to 28
    Cr12WriteCounterReset = 0  # bit 28 to 29
    RequestStallThreshold = 0  # bit 29 to 31
    RequestStallDisable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _VGA_DEBUG),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_VGA_DEBUG, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_WRITE_BACK_WATERMARK(Enum):
    WRITE_BACK_WATERMARK_4 = 0x0  # 4 entries
    WRITE_BACK_WATERMARK_8 = 0x1  # 8 entries
    WRITE_BACK_WATERMARK_16 = 0x2  # 16 entries
    WRITE_BACK_WATERMARK_32 = 0x3  # 32 entries


class ENUM_COMPRESSION_LIMIT(Enum):
    COMPRESSION_LIMIT_11 = 0x0  # Compressed buffer is the same size as the uncompressed buffer.
    COMPRESSION_LIMIT_21 = 0x1  # Compressed buffer is one half the size of the uncompressed buffer.
    COMPRESSION_LIMIT_41 = 0x2  # Compressed buffer is one quarter the size of the uncompressed buffer.


class ENUM_REFILL_FIFO_WRITE_WATERMARK(Enum):
    REFILL_FIFO_WRITE_WATERMARK_16 = 0x0  # 16 entries available
    REFILL_FIFO_WRITE_WATERMARK_32 = 0x1  # 32 entries available
    REFILL_FIFO_WRITE_WATERMARK_64 = 0x2  # 64 entries available
    REFILL_FIFO_WRITE_WATERMARK_96 = 0x3  # 96 entries available


class ENUM_FALSE_COLOR_CONTROL(Enum):
    FALSE_COLOR_CONTROL_DISABLE = 0x0
    FALSE_COLOR_CONTROL_ENABLE = 0x1


class ENUM_SLB_INIT_FLUSH_DISABLE(Enum):
    SLB_INIT_FLUSH_ENABLE = 0x0  # Enable the SLB initialization flush
    SLB_INIT_FLUSH_DISABLE = 0x1  # Disable SLB initialization flush


class ENUM_DISABLE_DELTA(Enum):
    DISABLE_DELTA_DEBUG_DISABLE = 0x1
    DISABLE_DELTA_ENABLE = 0x0


class ENUM_DISABLE_PAL(Enum):
    DISABLE_PAL_DEBUG_DISABLE = 0x1
    DISABLE_PAL_ENABLE = 0x0


class ENUM_DISABLE_RUN(Enum):
    DISABLE_RUN_DEBUG_DISABLE = 0x1
    DISABLE_RUN_ENABLE = 0x0


class ENUM_ENABLE_FBC(Enum):
    ENABLE_FBC_DISABLE = 0x0
    ENABLE_FBC_ENABLE = 0x1


class OFFSET_FBC_CTL:
    FBC_CTL_A = 0x43208
    FBC_CTL_B = 0x43248


class _FBC_CTL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 4),
        ('WriteBackWatermark', ctypes.c_uint32, 2),
        ('CompressionLimit', ctypes.c_uint32, 2),
        ('RefillFifoWriteWatermark', ctypes.c_uint32, 2),
        ('FalseColorControl', ctypes.c_uint32, 1),
        ('Reserved11', ctypes.c_uint32, 2),
        ('Reserved13', ctypes.c_uint32, 2),
        ('SlbInitFlushDisable', ctypes.c_uint32, 1),
        ('DisableDelta', ctypes.c_uint32, 1),
        ('DisablePal', ctypes.c_uint32, 1),
        ('DisableRun', ctypes.c_uint32, 1),
        ('Reserved19', ctypes.c_uint32, 9),
        ('Reserved28', ctypes.c_uint32, 1),
        ('Reserved29', ctypes.c_uint32, 1),
        ('AllowDbStall', ctypes.c_uint32, 1),
        ('EnableFbc', ctypes.c_uint32, 1),
    ]


class REG_FBC_CTL(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 4
    WriteBackWatermark = 0  # bit 4 to 6
    CompressionLimit = 0  # bit 6 to 8
    RefillFifoWriteWatermark = 0  # bit 8 to 10
    FalseColorControl = 0  # bit 10 to 11
    Reserved11 = 0  # bit 11 to 13
    Reserved13 = 0  # bit 13 to 15
    SlbInitFlushDisable = 0  # bit 15 to 16
    DisableDelta = 0  # bit 16 to 17
    DisablePal = 0  # bit 17 to 18
    DisableRun = 0  # bit 18 to 19
    Reserved19 = 0  # bit 19 to 28
    Reserved28 = 0  # bit 28 to 29
    Reserved29 = 0  # bit 29 to 30
    AllowDbStall = 0  # bit 30 to 31
    EnableFbc = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _FBC_CTL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_FBC_CTL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_FBC_CFB_BASE:
    FBC_CFB_BASE_A = 0x43200
    FBC_CFB_BASE_B = 0x43240


class _FBC_CFB_BASE(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 12),
        ('CfbOffsetAddress', ctypes.c_uint32, 16),
        ('Reserved28', ctypes.c_uint32, 4),
    ]


class REG_FBC_CFB_BASE(ctypes.Union):
    value = 0
    offset = 0

    Reserved0 = 0  # bit 0 to 12
    CfbOffsetAddress = 0  # bit 12 to 28
    Reserved28 = 0  # bit 28 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _FBC_CFB_BASE),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_FBC_CFB_BASE, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_COMPTAG_GATING_FIX_DISABLE(Enum):
    COMPTAG_GATING_FIX_ENABLE_FIX = 0x0
    COMPTAG_GATING_FIX_DISABLE_FIX = 0x1


class ENUM_SLB_INVALIDATE_NUKE_FIX_DISABLE(Enum):
    SLB_INVALIDATE_NUKE_FIX_ENABLE_FIX = 0x0
    SLB_INVALIDATE_NUKE_FIX_DISABLE_FIX = 0x1


class ENUM_DECOMP_BUBBLE_FIX_DISABLE(Enum):
    DECOMP_BUBBLE_FIX_ENABLE_FIX = 0x0
    DECOMP_BUBBLE_FIX_DISABLE_FIX = 0x1


class ENUM_UNDERRUN_2PPC_FIX_DISABLE(Enum):
    UNDERRUN_2PPC_FIX_ENABLE_FIX = 0x0
    UNDERRUN_2PPC_FIX_DISABLE_FIX = 0x1


class ENUM_RC_NUKE_FOR_PSR_FIX_DISABLE(Enum):
    RC_NUKE_FOR_PSR_FIX_ENABLE_FIX = 0x0
    RC_NUKE_FOR_PSR_FIX_DISABLE_FIX = 0x1


class ENUM_OVERRIDE_AUTOMATIC_DISABLE(Enum):
    OVERRIDE_AUTOMATIC_ENABLE = 0x0
    OVERRIDE_AUTOMATIC_DISABLE = 0x1


class ENUM_DIS_DUMMY0(Enum):
    DIS_DUMMY0_ENABLE_DUMMY0 = 0x0
    DIS_DUMMY0_DISABLE_DUMMY0 = 0x1


class ENUM_FORCE_OFF(Enum):
    FORCE_OFF_DO_NOT_FORCE_OFF_FBC = 0x0
    FORCE_OFF_FORCE_OFF_FBC = 0x1


class ENUM_SKIP_SEG_ENABLE(Enum):
    SKIP_SEG_DISABLE = 0x0
    SKIP_SEG_ENABLE = 0x1


class ENUM_FORCE_SLB_INVALIDATION(Enum):
    FORCE_SLB_INVALIDATION_DISABLE = 0x0
    FORCE_SLB_INVALIDATION_ENABLE = 0x1


class ENUM_COMP_DUMMY_PIXEL(Enum):
    COMP_DUMMY_PIXEL_DISABLE = 0x0
    COMP_DUMMY_PIXEL_ENABLE = 0x1


class ENUM_PSR_LINK_OFF_NUKE_FIX_DISABLE(Enum):
    PSR_LINK_OFF_NUKE_FIX_ENABLE = 0x0
    PSR_LINK_OFF_NUKE_FIX_DISABLE = 0x1


class ENUM_INIT_STATE_CLEAR_FIX_DISABLE(Enum):
    INIT_STATE_CLEAR_FIX_DISABLE_FIX_ENABLED = 0x0
    INIT_STATE_CLEAR_FIX_DISABLE_FIX_DISABLED = 0x1


class ENUM_FLUSH_LAST_SEGMENT_FIX_ENABLE(Enum):
    FLUSH_LAST_SEGMENT_FIX_ENABLE = 0x0
    FLUSH_LAST_SEGMENT_FIX_DISABLE = 0x1


class ENUM_LP_RW_FRAMESTART_HOLD_DISABLE(Enum):
    LP_RW_FRAMESTART_HOLD_ENABLE = 0x0
    LP_RW_FRAMESTART_HOLD_DISABLE = 0x1


class ENUM_DISABLE_SLB_READ_COUNT_HOLD(Enum):
    DISABLE_SLB_READ_COUNT_HOLD_FIX_DISABLED = 0x1
    DISABLE_SLB_READ_COUNT_HOLD_FIX_ENABLED = 0x0


class ENUM_DISABLE_DUMMY_READ_LAST_SEG_FIX(Enum):
    DISABLE_DUMMY_READ_LAST_SEG_FIX_FIX_DISABLED = 0x1
    DISABLE_DUMMY_READ_LAST_SEG_FIX_FIX_ENABLED = 0x0


class ENUM_DIS_VTD_FAULT_NUKE(Enum):
    DIS_VTD_FAULT_NUKE_DO_NOT_NUKE_ON_VTD_FAULT = 0x1
    DIS_VTD_FAULT_NUKE_NUKE_ON_VTD_FAULT = 0x0


class ENUM_HEIGHT_4096_FIX_DISABLE(Enum):
    HEIGHT_4096_FIX_ENABLE = 0x0
    HEIGHT_4096_FIX_DISABLE = 0x1


class ENUM_READ_WRITE_COLLISION_FIX_DISABLE(Enum):
    READ_WRITE_COLLISION_FIX_ENABLE_FIX_FOR_READ_WRITE_COLLISION = 0x0
    READ_WRITE_COLLISION_FIX_DISABLE_FIX_FOR_READ_WRITE_COLLISION = 0x1


class ENUM_WB_IGNORE_FILL(Enum):
    WB_IGNORE_FILL_WRITE_BACK_COMPRESSED_DATA_USING_DCPR_FILL_SIGNAL_AND_DPFC_INTERNAL_WATERMARK = 0x0
    WB_IGNORE_FILL_WRITE_BACK_COMPRESSED_DATA_IGNORING_DCPR_FILL_SIGNAL_AND_DPFC_INTERNAL_WATERMARK = 0x1


class ENUM_DIS_COMPTAG_UNDERRUN_NUKE(Enum):
    DIS_COMPTAG_UNDERRUN_NUKE_ENABLE_COMPTAG_UNDERRUN_MESSAGE_NUKE = 0x0
    DIS_COMPTAG_UNDERRUN_NUKE_DISABLE_COMPTAG_UNDERRUN_MESSAGE_NUKE = 0x1


class ENUM_DIS_FLIP_NUKE(Enum):
    DIS_FLIP_NUKE_ENABLE_FLIP_NUKE = 0x0
    DIS_FLIP_NUKE_DISABLE_FLIP_NUKE = 0x1


class ENUM_DIS_PIPE_UNDERRUN_NUKE(Enum):
    DIS_PIPE_UNDERRUN_NUKE_ENABLE_PIPE_UNDERRUN_NUKE = 0x0
    DIS_PIPE_UNDERRUN_NUKE_DISABLE_PIPE_UNDERRUN_NUKE = 0x1


class ENUM_DIS_COUNT_NUKE(Enum):
    DIS_COUNT_NUKE_ENABLE_PIXEL_COUNT_MISMATCH_NUKE = 0x0
    DIS_COUNT_NUKE_DISABLE_PIXEL_COUNT_MISMATCH_NUKE = 0x1


class ENUM_DIS_CWB_NUKE(Enum):
    DIS_CWB_NUKE_ENABLE_CWB_FIFO_NOT_EMPTY_NUKE = 0x0
    DIS_CWB_NUKE_DISABLE_CWB_FIFO_NOT_EMPTY_NUKE = 0x1


class OFFSET_FBC_CHICKEN:
    FBC_CHICKEN_A = 0x43224
    FBC_CHICKEN_B = 0x43264


class _FBC_CHICKEN(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ComptagGatingFixDisable', ctypes.c_uint32, 1),
        ('SlbInvalidateNukeFixDisable', ctypes.c_uint32, 1),
        ('DecompBubbleFixDisable', ctypes.c_uint32, 1),
        ('Underrun2PpcFixDisable', ctypes.c_uint32, 1),
        ('RcNukeForPsrFixDisable', ctypes.c_uint32, 1),
        ('OverrideAutomaticDisable', ctypes.c_uint32, 1),
        ('DstComptagOffset', ctypes.c_uint32, 2),
        ('DisDummy0', ctypes.c_uint32, 1),
        ('ForceOff', ctypes.c_uint32, 1),
        ('SkipSegCount', ctypes.c_uint32, 2),
        ('SkipSegEnable', ctypes.c_uint32, 1),
        ('ForceSlbInvalidation', ctypes.c_uint32, 1),
        ('CompDummyPixel', ctypes.c_uint32, 1),
        ('PsrLinkOffNukeFixDisable', ctypes.c_uint32, 1),
        ('InitStateClearFixDisable', ctypes.c_uint32, 1),
        ('FlushLastSegmentFixEnable', ctypes.c_uint32, 1),
        ('LpRwFramestartHoldDisable', ctypes.c_uint32, 1),
        ('DisableSlbReadCountHold', ctypes.c_uint32, 1),
        ('DisableDummyReadLastSegFix', ctypes.c_uint32, 1),
        ('DisVtdFaultNuke', ctypes.c_uint32, 1),
        ('Height4096FixDisable', ctypes.c_uint32, 1),
        ('Spare23', ctypes.c_uint32, 1),
        ('ReadWriteCollisionFixDisable', ctypes.c_uint32, 1),
        ('WbIgnoreFill', ctypes.c_uint32, 1),
        ('DisComptagUnderrunNuke', ctypes.c_uint32, 1),
        ('Spare27', ctypes.c_uint32, 1),
        ('DisFlipNuke', ctypes.c_uint32, 1),
        ('DisPipeUnderrunNuke', ctypes.c_uint32, 1),
        ('DisCountNuke', ctypes.c_uint32, 1),
        ('DisCwbNuke', ctypes.c_uint32, 1),
    ]


class REG_FBC_CHICKEN(ctypes.Union):
    value = 0
    offset = 0

    ComptagGatingFixDisable = 0  # bit 0 to 1
    SlbInvalidateNukeFixDisable = 0  # bit 1 to 2
    DecompBubbleFixDisable = 0  # bit 2 to 3
    Underrun2PpcFixDisable = 0  # bit 3 to 4
    RcNukeForPsrFixDisable = 0  # bit 4 to 5
    OverrideAutomaticDisable = 0  # bit 5 to 6
    DstComptagOffset = 0  # bit 6 to 8
    DisDummy0 = 0  # bit 8 to 9
    ForceOff = 0  # bit 9 to 10
    SkipSegCount = 0  # bit 10 to 12
    SkipSegEnable = 0  # bit 12 to 13
    ForceSlbInvalidation = 0  # bit 13 to 14
    CompDummyPixel = 0  # bit 14 to 15
    PsrLinkOffNukeFixDisable = 0  # bit 15 to 16
    InitStateClearFixDisable = 0  # bit 16 to 17
    FlushLastSegmentFixEnable = 0  # bit 17 to 18
    LpRwFramestartHoldDisable = 0  # bit 18 to 19
    DisableSlbReadCountHold = 0  # bit 19 to 20
    DisableDummyReadLastSegFix = 0  # bit 20 to 21
    DisVtdFaultNuke = 0  # bit 21 to 22
    Height4096FixDisable = 0  # bit 22 to 23
    Spare23 = 0  # bit 23 to 24
    ReadWriteCollisionFixDisable = 0  # bit 24 to 25
    WbIgnoreFill = 0  # bit 25 to 26
    DisComptagUnderrunNuke = 0  # bit 26 to 27
    Spare27 = 0  # bit 27 to 28
    DisFlipNuke = 0  # bit 28 to 29
    DisPipeUnderrunNuke = 0  # bit 29 to 30
    DisCountNuke = 0  # bit 30 to 31
    DisCwbNuke = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _FBC_CHICKEN),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_FBC_CHICKEN, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_SELECTIVE_FETCH_PLANE_ENABLE(Enum):
    SELECTIVE_FETCH_PLANE_DISABLE = 0x0
    SELECTIVE_FETCH_PLANE_ENABLE = 0x1


class OFFSET_SEL_FETCH_PLANE_CTL:
    SEL_FETCH_PLANE_CTL_1_A = 0x70890
    SEL_FETCH_PLANE_CTL_2_A = 0x708B0
    SEL_FETCH_PLANE_CTL_3_A = 0x708D0
    SEL_FETCH_PLANE_CTL_4_A = 0x708F0
    SEL_FETCH_PLANE_CTL_5_A = 0x70920
    SEL_FETCH_PLANE_CTL_1_B = 0x71890
    SEL_FETCH_PLANE_CTL_2_B = 0x718B0
    SEL_FETCH_PLANE_CTL_3_B = 0x718D0
    SEL_FETCH_PLANE_CTL_4_B = 0x718F0
    SEL_FETCH_PLANE_CTL_5_B = 0x71920
    SEL_FETCH_PLANE_CTL_1_C = 0x72890
    SEL_FETCH_PLANE_CTL_2_C = 0x728B0
    SEL_FETCH_PLANE_CTL_3_C = 0x728D0
    SEL_FETCH_PLANE_CTL_4_C = 0x728F0
    SEL_FETCH_PLANE_CTL_5_C = 0x72920
    SEL_FETCH_PLANE_CTL_1_D = 0x73890
    SEL_FETCH_PLANE_CTL_2_D = 0x738B0
    SEL_FETCH_PLANE_CTL_3_D = 0x738D0
    SEL_FETCH_PLANE_CTL_4_D = 0x738F0
    SEL_FETCH_PLANE_CTL_5_D = 0x73920


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


class ENUM_PLANE_BINDING(Enum):
    PLANE_BINDING_PLANE_1 = 0x0
    PLANE_BINDING_PLANE_2 = 0x1
    PLANE_BINDING_PLANE_3 = 0x2


class ENUM_LUMINANCE_MAPPER_ENABLE(Enum):
    LUMINANCE_MAPPER_DISABLED = 0x0
    LUMINANCE_MAPPER_ENABLED = 0x1


class OFFSET_LM_CTRL:
    LM_CTRL_1_A = 0x68300
    LM_CTRL_1_B = 0x68B00
    LM_CTRL_1_C = 0x69300
    LM_CTRL_1_D = 0x69B00


class _LM_CTRL(ctypes.LittleEndianStructure):
    _fields_ = [
        ('PlaneBinding', ctypes.c_uint32, 2),
        ('Reserved2', ctypes.c_uint32, 29),
        ('LuminanceMapperEnable', ctypes.c_uint32, 1),
    ]


class REG_LM_CTRL(ctypes.Union):
    value = 0
    offset = 0

    PlaneBinding = 0  # bit 0 to 2
    Reserved2 = 0  # bit 2 to 31
    LuminanceMapperEnable = 0  # bit 31 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LM_CTRL),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LM_CTRL, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LM_LUMA_COEFF:
    LM_LUMA_COEFF_1_A = 0x6830C
    LM_LUMA_COEFF_1_B = 0x68B0C
    LM_LUMA_COEFF_1_C = 0x6930C
    LM_LUMA_COEFF_1_D = 0x69B0C


class _LM_LUMA_COEFF(ctypes.LittleEndianStructure):
    _fields_ = [
        ('BlueCoefficient', ctypes.c_uint32, 9),
        ('Reserved9', ctypes.c_uint32, 1),
        ('GreenCoefficient', ctypes.c_uint32, 9),
        ('Reserved19', ctypes.c_uint32, 1),
        ('RedCoefficient', ctypes.c_uint32, 9),
        ('Reserved29', ctypes.c_uint32, 3),
    ]


class REG_LM_LUMA_COEFF(ctypes.Union):
    value = 0
    offset = 0

    BlueCoefficient = 0  # bit 0 to 9
    Reserved9 = 0  # bit 9 to 10
    GreenCoefficient = 0  # bit 10 to 19
    Reserved19 = 0  # bit 19 to 20
    RedCoefficient = 0  # bit 20 to 29
    Reserved29 = 0  # bit 29 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LM_LUMA_COEFF),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LM_LUMA_COEFF, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LM_TONEFACT_DATA:
    LM_TONEFACT_DATA_1_A = 0x68308
    LM_TONEFACT_DATA_1_B = 0x68B08
    LM_TONEFACT_DATA_1_C = 0x69308
    LM_TONEFACT_DATA_1_D = 0x69B08


class _LM_TONEFACT_DATA(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ToneMappingFactor', ctypes.c_uint32, 24),
        ('Reserved24', ctypes.c_uint32, 8),
    ]


class REG_LM_TONEFACT_DATA(ctypes.Union):
    value = 0
    offset = 0

    ToneMappingFactor = 0  # bit 0 to 24
    Reserved24 = 0  # bit 24 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LM_TONEFACT_DATA),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LM_TONEFACT_DATA, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class OFFSET_LM_TONEFACT_INDEX:
    LM_TONEFACT_INDEX_1_A = 0x68304
    LM_TONEFACT_INDEX_1_B = 0x68B04
    LM_TONEFACT_INDEX_1_C = 0x69304
    LM_TONEFACT_INDEX_1_D = 0x69B04


class _LM_TONEFACT_INDEX(ctypes.LittleEndianStructure):
    _fields_ = [
        ('IndexValue', ctypes.c_uint32, 8),
        ('Reserved8', ctypes.c_uint32, 8),
        ('IndexAutoIncrement', ctypes.c_uint32, 1),
        ('Reserved17', ctypes.c_uint32, 15),
    ]


class REG_LM_TONEFACT_INDEX(ctypes.Union):
    value = 0
    offset = 0

    IndexValue = 0  # bit 0 to 8
    Reserved8 = 0  # bit 8 to 16
    IndexAutoIncrement = 0  # bit 16 to 17
    Reserved17 = 0  # bit 17 to 32

    _anonymous_ = ("bitMap",)
    _fields_ = [
        ('bitMap', _LM_TONEFACT_INDEX),
        ('value', ctypes.c_uint32)
    ]

    def __init__(self, offset=None, value=None):
        assert not (offset is None and value is None)
        super(REG_LM_TONEFACT_INDEX, self).__init__()
        if offset is not None:
            self.offset = offset
        if value is not None:
            self.value = value


class ENUM_OVERRIDE_STRIDE_ENABLE(Enum):
    OVERRIDE_STRIDE_ENABLE_OVERRIDE_DISABLE = 0x0
    OVERRIDE_STRIDE_ENABLE_OVERRIDE_ENABLE = 0x1


class OFFSET_FBC_STRIDE:
    FBC_STRIDE_A = 0x43228
    FBC_STRIDE_B = 0x43268


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

