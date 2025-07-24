import ctypes
 
'''
Register instance and offset 
'''
PIPE_MISC_A = 0x70030 
PIPE_MISC_B = 0x71030 
PIPE_MISC_C = 0x72030 

'''
Register field expected values 
'''
bits_per_color_10_BPC = 0b001
bits_per_color_12_BPC = 0b011
bits_per_color_6_BPC = 0b010
bits_per_color_8_BPC = 0b000
yuv420_enable_ENABLE = 0b1
yuv420_enable_DISABLE = 0b0
yuv420_mode_BYPASS = 0b0
yuv420_mode_FULL_BLEND = 0b1
hdr_mode_DISABLE = 0b0
hdr_mode_ENABLE = 0b1
pipe_output_color_space_select_RGB = 0b0
pipe_output_color_space_select_YUV = 0b1
dithering_bpc_8BPC = 0b000
dithering_bpc_10BPC = 0b001
dithering_bpc_6BPC = 0b010
dithering_enable_DISABLE = 0b0
dithering_enable_ENABLE = 0b1
dithering_type_SPATIAL = 0b00
dithering_type_ST1 = 0b01
dithering_type_ST2 = 0b10
dithering_type_TEMPORAL = 0b11


 
'''
Register bitfield defnition structure 
'''
class PIPE_MISC_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("bfi_enable",                          ctypes.c_uint32,1), # 0 to 0 
        ("reserved_1",                          ctypes.c_uint32,1), # 1 to 1 
        ("dithering_type",                      ctypes.c_uint32,2), # 2 to 3 
        ("dithering_enable",                    ctypes.c_uint32,1), # 4 to 4 
        ("dithering_bpc",                       ctypes.c_uint32,3), # 5 to 7 
        ("reserved_8",                          ctypes.c_uint32,2), # 8 to 9 
        ("xvycc_color_range_limit",             ctypes.c_uint32,1), # 10 to 10 
        ("pipe_output_color_space_select",      ctypes.c_uint32,1), # 11 to 11 
        ("reserved_12",                         ctypes.c_uint32,2), # 12 to 13 
        ("rotation_info",                       ctypes.c_uint32,2), # 14 to 15 
        ("override_blue_channel",               ctypes.c_uint32,1), # 16 to 16 //debug
        ("override_green_channel",              ctypes.c_uint32,1), # 17 to 17 //debug
        ("override_red_channel",                ctypes.c_uint32,1), # 18 to 18 //debug
        ("override_pipe_output",                ctypes.c_uint32,1), # 19 to 19 //debug
        ("change_mask_for_vblank_vsync_int",    ctypes.c_uint32,1), # 20 to 20 
        ("change_mask_for_register_write",      ctypes.c_uint32,1), # 21 to 21 
        ("change_mask_for_ldpst",               ctypes.c_uint32,1), # 22 to 22 
        ("reserved_23",                         ctypes.c_uint32,1), # 23 to 23 
        ("reserved_24",                         ctypes.c_uint32,2), # 24 to 25 
        ("yuv420_mode",                         ctypes.c_uint32,1), # 26 to 26 
        ("yuv420_enable",                       ctypes.c_uint32,1), # 27 to 27 
        ("stereo_mask_pipe_render",             ctypes.c_uint32,2), # 28 to 29 
        ("stereo_mask_pipe_int",                ctypes.c_uint32,2), # 30 to 31 
    ]

 
class PIPE_MISC_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_MISC_REG ),
        ("asUint", ctypes.c_uint32 ) ]