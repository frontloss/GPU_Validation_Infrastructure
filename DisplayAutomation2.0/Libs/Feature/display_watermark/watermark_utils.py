######################################################################################
# @file         watermark_utils.py
# @addtogroup   PyLibs_DisplayWatermark
# @brief        Module for DisplayWatermark contains imports of dependent libs and constant definitions
# @author       Kumar V,Arun, Bhargav Adigarla
######################################################################################


from Libs.Core.machine_info.machine_info import SystemInfo

machine_info = SystemInfo()
platform = None
gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break

NEXT_PIPE_OFFSET = 0x1000
NEXT_PLANE_OFFSET = 0x100
EDP_OFFSET = 0xF000
NEXT_REGISTER_OFFSET = 0x4
SCALAR_PIPE_B_OFFSET = 0x800
SCALAR_PIPE_C_OFFSET = 0x1000

PIPE_NAME = ['A', 'B', 'C', 'D']
PIPE_A = 0
PIPE_B = 1
PIPE_C = 2
PIPE_D = 3
PLANE_NAME = ['1', '2', '3', '4', '5', '6', '7']

GEN9_PLATFORMS = ['skl', 'bxt', 'kbl', 'cfl']
GEN10_PLATFORMS = ['cnl', 'glk']
GEN11_PLATFORMS = ['icl', 'icllp', 'iclhp', 'lkf1', 'jsl']
GEN12_PLATFORMS = ['tgl', 'ryf', 'dg1', 'rkl', 'adls']
GEN13_PLATFORMS = ['dg2', 'adlp']
GEN14_PLATFORMS = ['mtl', 'elg']
GEN15_PLATFORMS = ['lnl']
GEN16_PLATFORMS = ['ptl']
GEN17_PLATFORMS = ['nvl', 'cls']

PRE_GEN_11_PLATFORMS = GEN9_PLATFORMS + GEN10_PLATFORMS
PRE_GEN_11_P_5_PLATFORMS = PRE_GEN_11_PLATFORMS + GEN11_PLATFORMS
PRE_GEN_12_PLATFORMS = GEN9_PLATFORMS + GEN10_PLATFORMS + GEN11_PLATFORMS
PRE_GEN_13_PLATFORMS = PRE_GEN_12_PLATFORMS + GEN12_PLATFORMS
PRE_GEN_14_PLATFORMS = PRE_GEN_13_PLATFORMS + GEN13_PLATFORMS
PRE_GEN_15_PLATFORMS = PRE_GEN_14_PLATFORMS + GEN14_PLATFORMS
PRE_GEN_16_PLATFORMS = PRE_GEN_15_PLATFORMS + GEN15_PLATFORMS
PRE_GEN_17_PLATFORMS = PRE_GEN_16_PLATFORMS + GEN16_PLATFORMS
PRE_GEN_18_PLATFORMS = PRE_GEN_17_PLATFORMS + GEN17_PLATFORMS

##
# Pixel format Dictionary
# Key : Source Pixel Format value from PLANE_CTL register
# Value : 'pixel_format' = Pixel format name
#         'BPP' = Bytes per pixel for each surface format
GEN9_PIXEL_FORMAT_DICT = {
    0: {'pixel_format': 'YUV16(BPP) 422 PACKED',
        'BPP': 2},
    1: {'pixel_format': 'NV12 YUV 420 PLANAR',
        'BPP': 1},
    2: {'pixel_format': 'RGB10-32BIT',
        'BPP': 4},
    4: {'pixel_format': 'RGB8-32BIT',
        'BPP': 4},
    6: {'pixel_format': 'RGB64',
        'BPP': 8},
    8: {'pixel_format': 'YUV32 444 PACKED',
        'BPP': 4},
    10: {'pixel_format': 'RGB10-32BIT-XR_BIAS',
         'BPP': 4},
    12: {'pixel_format': 'RGB-8BIT_INDEXED',
         'BPP': 1},
    14: {'pixel_format': 'RGB-16BIT 565',
         'BPP': 2},
}

##
# Pixel format Dictionary
# Key : Source Pixel Format value from PLANE_CTL register
# Value : 'pixel_format' = Pixel format name
#         'BPP' = Bytes per pixel for each surface format
GEN10_PIXEL_FORMAT_DICT = {
    0: {'pixel_format': 'YUV16(BPP) 422 PACKED',
        'BPP': 2},
    1: {'pixel_format': 'NV12 YUV 420 PLANAR',
        'BPP': 1},
    2: {'pixel_format': 'RGB10-32BIT',
        'BPP': 4},
    3: {'pixel_format': 'YUV10 420 PLANAR P010',
        'BPP': 2},
    4: {'pixel_format': 'RGB8-32BIT',
        'BPP': 4},
    5: {'pixel_format': 'YUV12 420 PLANAR P012',
        'BPP': 2},
    6: {'pixel_format': 'RGB64 FLOAT',
        'BPP': 8},
    7: {'pixel_format': 'YUV12 420 PLANAR P016',
        'BPP': 2},
    8: {'pixel_format': 'YUV32 444 PACKED',
        'BPP': 4},
    9: {'pixel_format': 'RGB64 UINT',
        'BPP': 8},
    10: {'pixel_format': 'RGB10-32BIT-XR_BIAS',
         'BPP': 4},
    12: {'pixel_format': 'RGB-8BIT_INDEXED',
         'BPP': 1},
    14: {'pixel_format': 'RGB-16BIT',
         'BPP': 2},
}

##
# Pixel format Dictionary
# Key : Source Pixel Format value from PLANE_CTL register
# Value : 'pixel_format' = Pixel format name
#         'BPP' = Bytes per pixel for each surface format
GEN11_PIXEL_FORMAT_DICT = {
    0: {'pixel_format': 'YUV 422 PACKED 8 BPC',
        'BPP': 2},
    1: {'pixel_format': 'YUV 422 PACKED 10 BPC',
        'BPP': 4},
    2: {'pixel_format': 'YUV 420 PLANAR 8 BPC',
        'BPP': 1},  # NV12
    3: {'pixel_format': 'YUV 422 PACKED 12 BPC',
        'BPP': 4},
    4: {'pixel_format': 'RGB 2101010',
        'BPP': 4},  # RGB10 32 Bits
    5: {'pixel_format': 'YUV 422 PACKED 16 BPC',
        'BPP': 4},
    6: {'pixel_format': 'YUV10 420 PLANAR 10 BPC',
        'BPP': 2},  # P010
    7: {'pixel_format': 'YUV 444 PACKED 10 BPC',
        'BPP': 4},
    8: {'pixel_format': 'RGB 8888',
        'BPP': 4},  # RGB8 32 bits
    9: {'pixel_format': 'YUV 444 PACKED 12 BPC',
        'BPP': 8},
    10: {'pixel_format': 'YUV 420 PLANAR 12 BPC',
         'BPP': 2},  # P012
    11: {'pixel_format': 'YUV 444 PACKED 16 BPC',
         'BPP': 8},
    12: {'pixel_format': 'RGB 16161616 FLOAT',
         'BPP': 8},  # FP16
    14: {'pixel_format': 'YUV 420 PLANAR 16 BPC',
         'BPP': 2},  # P016
    16: {'pixel_format': 'YUV 444 PACKED 8 BPC',
         'BPP': 4},
    18: {'pixel_format': 'RGB64 UINT',
         'BPP': 8},
    20: {'pixel_format': 'RGB 2101010 XR_BIAS',
         'BPP': 4},
    24: {'pixel_format': 'INDEXED 8BIT',
         'BPP': 1},
    28: {'pixel_format': 'RGB 565',
         'BPP': 2},
}

##
# Pixel format Dictionary
# Key : Cursor mode select value from CUR_CTL register
# Value : 'size' = Cursor size for given cursor mode
#         'BPP' = Bytes per pixel for each surface format
CURSOR_DETAILS_DICT = {
    0: {'size': 0, 'BPP': 0},
    2: {'size': 128, 'BPP': 4},
    3: {'size': 256, 'BPP': 4},
    4: {'size': 64, 'BPP': 1},
    5: {'size': 64, 'BPP': 1},
    6: {'size': 64, 'BPP': 1},
    7: {'size': 64, 'BPP': 4},
    34: {'size': 128, 'BPP': 4},
    35: {'size': 256, 'BPP': 4},
    36: {'size': 64, 'BPP': 4},
    37: {'size': 128, 'BPP': 4},
    38: {'size': 256, 'BPP': 4},
    39: {'size': 64, 'BPP': 4},
}

MEMORY_TILING_LIST = {
    0: 'LINEAR',
    1: 'X_TILED',
    4: 'Y_LEGACY_TILED',
    5: 'TILED_4',
}

ROTATION_LIST = {
    0: 'NO ROTATION',
    1: '90 ROTATION',
    2: '180 ROTATION',
    3: '270 ROTATION',
}

if platform in ['adlp', 'mtl', 'elg', 'lnl', 'ptl', 'nvl', 'cls']:
    LATENCY_LEVELS = 6
else:
    LATENCY_LEVELS = 8
DEFAULT_SAGV_LATENCY = 10
SAGV_WM_LATENCY_LEVEL = 6
TRANS_SAGV_WM_LATENCY_LEVEL = 7

MAX_PLANES = 4
MAX_PIPES = 3

MAX_PLANES_GEN11 = 7
MAX_PIPES_GEN11 = 4

MAX_PLANES_GEN13 = 5
MAX_PIPES_GEN13 = 4

MAX_PIPES_GEN14 = 4
MAX_PLANES_GEN14 = 5

MAX_PIPES_GEN15 = 3
MAX_PLANES_GEN15 = 5

MAX_PIPES_GEN16 = 4
MAX_PLANES_GEN16 = 5

MAX_PIPES_GEN17 = 4
MAX_PLANES_GEN17 = 5

machine_info = SystemInfo()
platform = None
gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
        platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
        if platform == 'rkl':
            MAX_PLANES_GEN12 = 5
            MAX_PIPES_GEN12 = 3
            break
        elif platform == 'adls':
            MAX_PLANES_GEN12 = 5
            MAX_PIPES_GEN12 = 4
            break
        else:
            MAX_PLANES_GEN12 = 7
            MAX_PIPES_GEN12 = 4

SURFACE_MEMORY_LINEAR = 0b000
SURFACE_MEMORY_X_TILED = 0b001
SURFACE_MEMORY_Y_LEGACY_TILED = 0b100
SURFACE_MEMORY_Y_F_TILED = 0b101
SURFACE_MEMORY_TILED_4 = 0b101

ROTATION_0 = 0b00
ROTATION_90 = 0b01
ROTATION_180 = 0b10
ROTATION_270 = 0b11

PROGRESSIVE = 1
INTERLACED = 2

DBUF_BLOCK_SIZE = 512.0
DBUF_BLOCK_SIZE_YF = 256.0
MIN_DBUF_X_TILE = 8

DBUF_HALF_SLICE_SIZE = 1024
DBUF_SLICE_SIZE = DBUF_HALF_SLICE_SIZE + DBUF_HALF_SLICE_SIZE
DBUF_FULL_BLOCK_SIZE = DBUF_SLICE_SIZE + DBUF_SLICE_SIZE

DBUF_HALF_SLICE_END = DBUF_HALF_SLICE_SIZE - 1
DBUF_SLICE_END = DBUF_SLICE_SIZE - 1
DBUF_FULL_BLOCK_END = DBUF_FULL_BLOCK_SIZE - 1

DBUF_HALF_SLICE_SIZE_CLS = 2048
DBUF_SLICE_SIZE_CLS = DBUF_HALF_SLICE_SIZE_CLS + DBUF_HALF_SLICE_SIZE_CLS
DBUF_FULL_BLOCK_SIZE_CLS = DBUF_SLICE_SIZE_CLS + DBUF_SLICE_SIZE_CLS

DBUF_HALF_SLICE_END_CLS = DBUF_HALF_SLICE_SIZE_CLS - 1
DBUF_SLICE_END_CLS = DBUF_SLICE_SIZE_CLS - 1
DBUF_FULL_BLOCK_END_CLS = DBUF_FULL_BLOCK_SIZE_CLS - 1

TRANS_MINIMUM_GEN9 = 14
TRANS_AMOUNT_GEN9 = 20
TRANS_MINIMUM_GEN10 = 4
TRANS_AMOUNT_GEN10 = 20
TRANS_MINIMUM_GEN11 = 4
TRANS_AMOUNT_GEN11 = 20

DDI_MODE_DP_SST = 0b10
DDI_MODE_DP_MST = 0b11

# Register Offsets - Start

REG_MEMORY_FREQUENCY_BXT = 0x147114
REG_MEMORY_FREQUENCY_GEN9 = 0x145E04
REG_MEMORY_CHANNEL_0_GEN9 = 0x14500C
REG_MEMORY_CHANNEL_1_GEN9 = 0x145010

REG_GTDRIVER_MAILBOX_DATA0 = 0x138128
REG_GTDRIVER_MAILBOX_DATA1 = 0x13812C
REG_GTDRIVER_MAILBOX_INTERFACE = 0x138124

LATENCY_LP0_LP1 = 0x45780
LATENCY_LP2_LP3 = 0X45784
LATENCY_LP4_LP5 = 0X45788
LATENCY_SAGV = 0x4578C

PIPE_MBUS_DBOX_CTL_A = 0x7003C
PIPE_MBUS_DBOX_CTL_B = 0x7103C
PIPE_MBUS_DBOX_CTL_C = 0x7203C
PIPE_MBUS_DBOX_CTL_D = 0x7303C
# Register Offsets - End

# Bitmaps - Start

BITMAP_MEMORY_FREQ_RATIO_BXT = 0x0000003F  # 5-0
BITMAP_MEMORY_FREQ_RATIO_GEN9 = 0x0000000F  # 3-0
BITMAP_MEMORY_CHANNEL_0_BXT = 0x00005000  # 14 # 12
BITMAP_MEMORY_CHANNEL_1_BXT = 0x0000A000  # 15 # 13
BITMAP_MEMORY_RANK_SLOT_0_GEN9 = 0x00000400  # 10
BITMAP_MEMORY_RANK_SLOT_1_GEN9 = 0x04000000  # 26
BITMAP_MEMORY_CHANNEL_ENABLE_GEN9 = 0x0000003F  # 5-0

# Bitmaps - End
