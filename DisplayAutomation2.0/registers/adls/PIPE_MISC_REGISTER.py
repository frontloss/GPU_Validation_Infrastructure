import ctypes
 
'''
Register instance and offset 
'''
PIPE_MISC_A = 0x70030 
PIPE_MISC_B = 0x71030 
PIPE_MISC_C = 0x72030 
PIPE_MISC_D = 0x73030 

'''
Register field expected values 
'''
allow_db_stall_ALLOWED = 0b1
allow_db_stall_NOT_ALLOWED = 0b0
allow_double_buffer_update_disable_ALLOWED = 0b1
allow_double_buffer_update_disable_NOT_ALLOWED = 0b0
bfi_enable_DISABLE = 0b0
bfi_enable_ENABLE = 0b1
change_mask_for_ldpst_MASKED = 0b1
change_mask_for_ldpst_NOT_MASKED = 0b0
change_mask_for_register_write_MASKED = 0b1
change_mask_for_register_write_NOT_MASKED = 0b0
change_mask_for_vblank_vsync_int_MASKED = 0b1
change_mask_for_vblank_vsync_int_NOT_MASKED = 0b0
dithering_bpc_10_BPC = 0b001
dithering_bpc_6_BPC = 0b010
dithering_bpc_8_BPC = 0b000
dithering_bpc_RESERVED = 0b0
dithering_enable_DISABLE = 0b0
dithering_enable_ENABLE = 0b1
dithering_type_SPATIAL = 0b00
dithering_type_ST1 = 0b01
dithering_type_ST2 = 0b10
dithering_type_TEMPORAL = 0b11
hdr_mode_DISABLE = 0b0
hdr_mode_ENABLE = 0b1
oled_compensation_DISABLE = 0b0
oled_compensation_ENABLE = 0b1
override_blue_channel_BLUE_0S = 0b0
override_blue_channel_BLUE_1S = 0b1
override_green_channel_GREEN_0S = 0b0
override_green_channel_GREEN_1S = 0b1
override_pipe_output_NO_OVERRIDE = 0b0
override_pipe_output_OVERRIDE = 0b1
override_red_channel_RED_0S = 0b0
override_red_channel_RED_1S = 0b1
pipe_gamma_input_clamp_disable_DISABLE = 0b1
pipe_gamma_input_clamp_disable_ENABLE = 0b0
pipe_output_color_space_select_RGB = 0b0
pipe_output_color_space_select_YUV = 0b1
pixel_extension_MSB_EXTEND = 0b0
pixel_extension_ZERO_EXTEND = 0b1
pixel_rounding_ROUND_UP = 0b0
pixel_rounding_TRUNCATE = 0b1
rotation_info_180 = 0b10
rotation_info_270 = 0b11
rotation_info_90 = 0b01
rotation_info_NONE = 0b00
stereo_mask_pipe_int_MASK_LEFT = 0b01
stereo_mask_pipe_int_MASK_NONE = 0b00
stereo_mask_pipe_int_MASK_RIGHT = 0b10
stereo_mask_pipe_int_RESERVED = 0b0
stereo_mask_pipe_render_MASK_LEFT = 0b01
stereo_mask_pipe_render_MASK_NONE = 0b00
stereo_mask_pipe_render_MASK_RIGHT = 0b10
stereo_mask_pipe_render_RESERVED = 0b0
xvycc_color_range_limit_FULL = 0b0
xvycc_color_range_limit_LIMIT = 0b1
yuv420_enable_DISABLE = 0b0
yuv420_enable_ENABLE = 0b1
yuv420_mode_BYPASS = 0b0
yuv420_mode_FULL_BLEND = 0b1


'''
Register bitfield defnition structure
'''
class PIPE_MISC_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("bfi_enable"                        , ctypes.c_uint32, 1), # 0 to 0
        ("reserved_1"                        , ctypes.c_uint32, 1), # 1 to 1
        ("dithering_type"                    , ctypes.c_uint32, 2), # 2 to 3
        ("dithering_enable"                  , ctypes.c_uint32, 1), # 4 to 4
        ("dithering_bpc"                     , ctypes.c_uint32, 3), # 5 to 7
        ("pixel_rounding"                    , ctypes.c_uint32, 1), # 8 to 8
        ("pixel_extension"                   , ctypes.c_uint32, 1), # 9 to 9
        ("xvycc_color_range_limit"           , ctypes.c_uint32, 1), # 10 to 10
        ("pipe_output_color_space_select"    , ctypes.c_uint32, 1), # 11 to 11
        ("oled_compensation"                 , ctypes.c_uint32, 1), # 12 to 12
        ("reserved_13"                       , ctypes.c_uint32, 1), # 13 to 13
        ("rotation_info"                     , ctypes.c_uint32, 2), # 14 to 15
        ("override_blue_channel"             , ctypes.c_uint32, 1), # 16 to 16
        ("override_green_channel"            , ctypes.c_uint32, 1), # 17 to 17
        ("override_red_channel"              , ctypes.c_uint32, 1), # 18 to 18
        ("override_pipe_output"              , ctypes.c_uint32, 1), # 19 to 19
        ("change_mask_for_vblank_vsync_int"  , ctypes.c_uint32, 1), # 20 to 20
        ("change_mask_for_register_write"    , ctypes.c_uint32, 1), # 21 to 21
        ("change_mask_for_ldpst"             , ctypes.c_uint32, 1), # 22 to 22
        ("hdr_mode"                          , ctypes.c_uint32, 1), # 23 to 23
        ("allow_double_buffer_update_disable", ctypes.c_uint32, 1), # 24 to 24
        ("allow_db_stall"                    , ctypes.c_uint32, 1),  # 24 to 24
        ("pipe_gamma_input_clamp_disable"    , ctypes.c_uint32, 1), # 25 to 25
        ("yuv420_mode"                       , ctypes.c_uint32, 1), # 26 to 26
        ("yuv420_enable"                     , ctypes.c_uint32, 1), # 27 to 27
        ("stereo_mask_pipe_render"           , ctypes.c_uint32, 2), # 28 to 29
        ("stereo_mask_pipe_int"              , ctypes.c_uint32, 2), # 30 to 31
    ]


class PIPE_MISC_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_MISC_REG ),
        ("asUint", ctypes.c_uint32 ) ]