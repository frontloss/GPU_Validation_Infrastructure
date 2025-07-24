########################################################################################################################
# @file         PLANE_CTL_REGISTER.py
# @brief        This script contains register values of PLANE_CTL_REGISTER
# @author       Shetty, Anjali N
########################################################################################################################
import ctypes

'''
Register instance and offset 
'''
PLANE_CTL_1_A = 0x70180
PLANE_CTL_1_B = 0x71180
PLANE_CTL_1_C = 0x72180
PLANE_CTL_2_A = 0x70280
PLANE_CTL_2_B = 0x71280
PLANE_CTL_2_C = 0x72280
PLANE_CTL_3_A = 0x70380
PLANE_CTL_3_B = 0x71380
PLANE_CTL_3_C = 0x72380
PLANE_CTL_4_A = 0x70480
PLANE_CTL_4_B = 0x71480
PLANE_CTL_4_C = 0x72480

'''
Register field expected values 
'''
allow_double_buffer_update_disable_ALLOWED = 0b1
allow_double_buffer_update_disable_NOT_ALLOWED = 0b0
async_address_update_enable_ASYNC = 0b1
async_address_update_enable_SYNC = 0b0
key_enable_DESTINATION_KEY_ENABLE = 0b10
key_enable_DISABLE = 0b00
key_enable_SOURCE_KEY_ENABLE = 0b01
key_enable_SOURCE_KEY_WINDOW_ENABLE = 0b11
planar_yuv420_component_UV = 0b0
planar_yuv420_component_Y = 0b1
plane_enable_DISABLE = 0b0
plane_enable_ENABLE = 0b1
pipe_gamma_enable_DISABLE = 0b0
pipe_gamma_enable_ENABLE = 0b1
remove_yuv_offset_REMOVE = 0b0
remove_yuv_offset_PRESERVE = 0b1
yuv_range_correction_disable_ENABLE = 0b0
yuv_range_correction_disable_DISABLE = 0b1
plane_rotation_180_DEGREE_ROTATION = 0b10
plane_rotation_270_DEGREE_ROTATION = 0b11
plane_rotation_90_DEGREE_ROTATION = 0b01
plane_rotation_NO_ROTATION = 0b00
render_decomp_DISABLE = 0b0
render_decomp_ENABLE = 0b1
rgb_color_order_BGRX = 0b0
rgb_color_order_RGBX = 0b1
source_pixel_format_INDEXED_8_BIT = 0b1100
source_pixel_format_RGB_16161616_FLOAT = 0b0110
source_pixel_format_RGB_2101010 = 0b0010
source_pixel_format_RGB_2101010_XR_BIAS = 0b1010
source_pixel_format_RGB_565 = 0b1110
source_pixel_format_RGB_8888 = 0b0100
source_pixel_format_YUV_420_PLANAR_8_BPC = 0b0001
source_pixel_format_YUV_422_PACKED_8_BPC = 0b0000
source_pixel_format_YUV_444_PACKED_8_BPC = 0b1000
pipe_csc_enable_ENABLE = 0b1
pipe_csc_enable_DISABLE = 0b0
plane_yuv_to_rgb_csc_dis_ENABLE = 0b0
plane_yuv_to_rgb_csc_dis_DISABLE = 0b1
plane_yuv_to_rgb_csc_format_BT_601 = 0b0
plane_yuv_to_rgb_csc_format_BT_709 = 0b1
stereo_surface_vblank_mask_MASK_LEFT = 0b01
stereo_surface_vblank_mask_MASK_NONE = 0b00
stereo_surface_vblank_mask_MASK_RIGHT = 0b10
tiled_surface_LINEAR_MEMORY = 0b000
tiled_surface_TILE_X_MEMORY = 0b001
tiled_surface_TILE_Y_F_MEMORY = 0b101
tiled_surface_TILE_Y_LEGACY_MEMORY = 0b100
trickle_feed_enable_DISABLE = 0b1
trickle_feed_enable_ENABLE = 0b0
yuv_422_byte_order_UYVY = 0b01
yuv_422_byte_order_VYUY = 0b11
yuv_422_byte_order_YUYV = 0b00
yuv_422_byte_order_YVYU = 0b10
alpha_mode_DISABLE = 0b00
alpha_mode_ENABLE_WITH_SW_PREMULTIPLY = 0b10
alpha_mode_ENABLE_WITH_HW_PREMULTIPLY = 0b11

'''
Register bitfield defnition structure 
'''

##
# @brief    This class contains structure of plane control register
class PLANE_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("plane_rotation", ctypes.c_uint32, 2),  # 0 to 1
        ("reserved_2", ctypes.c_uint32, 1),  # 2 to 2
        ("allow_double_buffer_update_disable", ctypes.c_uint32, 1),  # 3 to 3
        ("alpha_mode", ctypes.c_uint32, 2),  # 4 to 5
        ("stereo_surface_vblank_mask", ctypes.c_uint32, 2),  # 6 to 7
        ("reserved_8", ctypes.c_uint32, 1),  # 8 to 8
        ("async_address_update_enable", ctypes.c_uint32, 1),  # 9 to 9
        ("tiled_surface", ctypes.c_uint32, 3),  # 10 to 12
        ("plane_gamma_disable", ctypes.c_uint32, 1),  # 13 to 13
        ("trickle_feed_enable", ctypes.c_uint32, 1),  # 14 to 14
        ("render_decomp", ctypes.c_uint32, 1),  # 15 to 15
        ("yuv_422_byte_order", ctypes.c_uint32, 2),  # 16 to 17
        ("plane_yuv_to_rgb_csc_dis", ctypes.c_uint32, 1),  # 18 to 18
        ("plane_yuv_to_rgb_csc_format", ctypes.c_uint32, 1),  # 19 to 19
        ("rgb_color_order", ctypes.c_uint32, 1),  # 20 to 20
        ("key_enable", ctypes.c_uint32, 2),  # 21 to 22
        ("pipe_csc_enable", ctypes.c_uint32, 1),  # 23 to 23
        ("source_pixel_format", ctypes.c_uint32, 4),  # 24 to 27
        ("yuv_range_correction_disable", ctypes.c_uint32, 1),  # 28 to 28
        ("remove_yuv_offset", ctypes.c_uint32, 1),  # 29 to 29
        ("pipe_gamma_enable", ctypes.c_uint32, 1),  # 30 to 30
        ("plane_enable", ctypes.c_uint32, 1),  # 31 to 31
    ]

##
# @brief    Plane Control Register Union
class PLANE_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PLANE_CTL_REG),
        ("asUint", ctypes.c_uint32)]
