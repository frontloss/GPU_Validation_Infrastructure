import ctypes
 
'''
Register instance and offset 
'''
PLANE_CTL_1_A  = 0x70180 
PLANE_CTL_1_B  = 0x71180 
PLANE_CTL_1_C  = 0x72180 
PLANE_CTL_1_D  = 0x73180 

PLANE_CTL_2_A  = 0x70280 
PLANE_CTL_2_B  = 0x71280 
PLANE_CTL_2_C  = 0x72280 
PLANE_CTL_2_D  = 0x73280 

PLANE_CTL_3_A  = 0x70380 
PLANE_CTL_3_B  = 0x71380 
PLANE_CTL_3_C  = 0x72380 
PLANE_CTL_3_D  = 0x73380 

PLANE_CTL_4_A  = 0x70480 
PLANE_CTL_4_B  = 0x71480 
PLANE_CTL_4_C  = 0x72480 
PLANE_CTL_4_D  = 0x73480 

PLANE_CTL_5_A  = 0x70580 
PLANE_CTL_5_B  = 0x71580 
PLANE_CTL_5_C  = 0x72580 
PLANE_CTL_5_D  = 0x73580 

'''
Register field expected values
'''
plane_enable_DISABLE = 0b0
plane_enable_ENABLE = 0b1
source_pixel_format_YUV_422_PACKED_8_BPC = 0b00000
source_pixel_format_YUV_422_PACKED_10_BPC = 0b00001
source_pixel_format_NV12_YUV_420 = 0b00010
source_pixel_format_YUV_422_PACKED_12_BPC = 0b00011
source_pixel_format_RGB_2101010 = 0b00100
source_pixel_format_YUV_422_PACKED_16_BPC = 0b00101
source_pixel_format_P010_YUV_420_10_BIT = 0b00110
source_pixel_format_YUV_444_PACKED_10_BPC = 0b00111
source_pixel_format_RGB_8888 = 0b01000
source_pixel_format_YUV_444_PACKED_12_BPC = 0b01001
source_pixel_format_P012_YUV_420_12_BIT = 0b01010
source_pixel_format_YUV_444_PACKED_16_BPC = 0b01011
source_pixel_format_RGB_16161616_FLOAT = 0b01100
source_pixel_format_P016_YUV_420_16_BIT = 0b01110
source_pixel_format_YUV_444_PACKED_8_BPC = 0b10000
source_pixel_format_RGB_64_BIT_16161616_UINT = 0b10010
source_pixel_format_RGB_2101010_XR_BIAS = 0b10100
source_pixel_format_INDEXED_8_BIT = 0b11000
source_pixel_format_RGB_565 = 0b11100
key_enable_DISABLE = 0b00
key_enable_SOURCE_KEY_ENABLE = 0b01
key_enable_DESTINATION_KEY_ENABLE = 0b10
key_enable_SOURCE_KEY_WINDOW_ENABLE = 0b11
rgb_color_order_BGRX = 0b0
rgb_color_order_RGBX = 0b1
planar_yuv420_component_UV = 0b0
planar_yuv420_component_Y = 0b1
yuv_422_byte_order_YUYV = 0b00
yuv_422_byte_order_UYVY = 0b01
yuv_422_byte_order_YVYU = 0b10
yuv_422_byte_order_VYUY = 0b11
render_decomp_DISABLE = 0b0
render_decomp_ENABLE = 0b1
media_decomp_DISABLE = 0b0
media_decomp_ENABLE = 0b1
lossy_comp_DISABLE = 0b0
lossy_comp_ENABLE = 0b1
trickle_feed_enable_ENABLE = 0b0
trickle_feed_enable_DISABLE = 0b1
tiled_surface_LINEAR_MEMORY = 0b000
tiled_surface_TILE_X_MEMORY = 0b001
tiled_surface_TILE_Y_LEGACY_MEMORY = 0b100
tiled_surface_TILE_Y_F_MEMORY = 0b101
async_address_update_enable_SYNC = 0b0
async_address_update_enable_ASYNC = 0b1
horizontal_flip_DISABLE = 0b0
horizontal_flip_ENABLE = 0b1
stereo_surface_vblank_mask_MASK_NONE = 0b00
stereo_surface_vblank_mask_MASK_LEFT = 0b01
stereo_surface_vblank_mask_MASK_RIGHT = 0b10
allow_double_buffer_update_disable_NOT_ALLOWED = 0b0
allow_double_buffer_update_disable_ALLOWED = 0b1
plane_rotation_NO_ROTATION = 0b00
plane_rotation_90_DEGREE_ROTATION = 0b01
plane_rotation_180_DEGREE_ROTATION = 0b10
plane_rotation_270_DEGREE_ROTATION = 0b11


'''
Register bitfield defnition structure 
'''
class PLANE_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("plane_rotation",                          ctypes.c_uint32,2), # 0 to 1 
        ("reserved_2",                              ctypes.c_uint32,1), # 2 to 2 
        ("allow_double_buffer_update_disable",      ctypes.c_uint32,1), # 3 to 3 
        ("media_decomp",                            ctypes.c_uint32,1), # 4 to 4
        ("lossy_comp",                              ctypes.c_uint32,1), # 5 to 5
        ("stereo_surface_vblank_mask",              ctypes.c_uint32,2), # 6 to 7 
        ("horizontal_flip",                         ctypes.c_uint32,1), # 8 to 8 
        ("async_address_update_enable",             ctypes.c_uint32,1), # 9 to 9 
        ("tiled_surface",                           ctypes.c_uint32,3), # 10 to 12 
        ("clear_color_disable",                     ctypes.c_uint32,1), # 13 to 13 
        ("trickle_feed_enable",                     ctypes.c_uint32,1), # 14 to 14 
        ("render_decomp",                           ctypes.c_uint32,1), # 15 to 15 
        ("yuv_422_byte_order",                      ctypes.c_uint32,2), # 16 to 17 
        ("reserved_18",                             ctypes.c_uint32,1), # 18 to 18 
        ("planar_yuv420_component",                 ctypes.c_uint32,1), # 19 to 19 
        ("rgb_color_order",                         ctypes.c_uint32,1), # 20 to 20 
        ("key_enable",                              ctypes.c_uint32,2), # 21 to 22 
        ("source_pixel_format",                     ctypes.c_uint32,5), # 23 to 27 
        ("pipe_slice_srbitration_slots",            ctypes.c_uint32,3), # 28 to 30 
        ("plane_enable",                            ctypes.c_uint32,1), # 31 to 31 
    ]

 
class PLANE_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]