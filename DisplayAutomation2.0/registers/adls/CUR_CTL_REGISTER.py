import ctypes
 
'''
Register instance and offset 
'''
CUR_CTL_A = 0x70080 
CUR_CTL_B = 0x71080 
CUR_CTL_C = 0x72080 
CUR_CTL_D = 0x73080

 
'''
Register field expected values 
'''
z0_rotation_180_DEGREE_ROTATION = 0b1 
z0_rotation_NO_ROTATION = 0b0 
allow_double_buffer_update_disable_ALLOWED = 0b1 
allow_double_buffer_update_disable_NOT_ALLOWED = 0b0 
cursor_mode_select_128X128_32BPP_AND_INV = 0b000010 
cursor_mode_select_128X128_32BPP_AND_XOR = 0b100101 
cursor_mode_select_128X128_32BPP_ARGB = 0b100010 
cursor_mode_select_256X256_32BPP_AND_INV = 0b000011 
cursor_mode_select_256X256_32BPP_AND_XOR = 0b100110 
cursor_mode_select_256X256_32BPP_ARGB = 0b100011 
cursor_mode_select_64X64_2BPP_2_COLOR = 0b000101 
cursor_mode_select_64X64_2BPP_3_COLOR = 0b000100 
cursor_mode_select_64X64_2BPP_4_COLOR = 0b000110 
cursor_mode_select_64X64_32BPP_AND_INV = 0b000111 
cursor_mode_select_64X64_32BPP_AND_XOR = 0b100100 
cursor_mode_select_64X64_32BPP_ARGB = 0b100111 
cursor_mode_select_DISABLE = 0b000000 
cursor_mode_select_RESERVED = 0b0 
force_alpha_plane_select_BOTH = 0b11 
force_alpha_plane_select_DISABLE = 0b00 
force_alpha_plane_select_PIPE_CSC_DISABLED = 0b10 
force_alpha_plane_select_PIPE_CSC_ENABLED = 0b01 
force_alpha_plane_select_PRIMARY = 0b10 
force_alpha_plane_select_RESERVED = 0b0 
force_alpha_plane_select_SPRITE = 0b01 
force_alpha_value_100 = 0b11 
force_alpha_value_50 = 0b01 
force_alpha_value_75 = 0b10 
force_alpha_value_DISABLE = 0b00 
gamma_enable_DISABLE = 0b0 
gamma_enable_ENABLE = 0b1 
pipe_csc_enable_DISABLE = 0b0 
pipe_csc_enable_ENABLE = 0b1 
popup_mode_NON_POPUP = 0b0 
trickle_feed_enable_DISABLE = 0b1 
trickle_feed_enable_ENABLE = 0b0 

 
'''
Register bitfield defnition structure 
'''
class CUR_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("cursor_mode_select"                , ctypes.c_uint32, 6), # 0 to 5 
        ("reserved_6"                        , ctypes.c_uint32, 2), # 6 to 7 
        ("force_alpha_value"                 , ctypes.c_uint32, 2), # 8 to 9 
        ("force_alpha_plane_select"          , ctypes.c_uint32, 2), # 10 to 11 
        ("reserved_12"                       , ctypes.c_uint32, 3), # 12 to 14
        ("180_rotation"                      , ctypes.c_uint32, 1), # 14 to 15
        ("csc_enable"                        , ctypes.c_uint32, 1), # 16 to 16 
        ("reserved_17"                       , ctypes.c_uint32, 1), # 17 to 17 
        ("pre_csc_gamma_enable"              , ctypes.c_uint32, 1), # 18 to 18 
        ("reserved_19"                       , ctypes.c_uint32, 4), # 19 to 22 
        ("allow_double_buffer_update_disable" , ctypes.c_uint32, 1), # 23 to 23 
        ("pipe_csc_enable"                   , ctypes.c_uint32, 1), # 24 to 24 
        ("reserved_25"                       , ctypes.c_uint32, 1), # 25 to 25 
        ("gamma_enable"                      , ctypes.c_uint32, 1), # 26 to 26
        ("reserved_27"                       , ctypes.c_uint32, 1), # 27 to 27 
        ("pipe_slice_arbitration_slots"      , ctypes.c_uint32, 3), # 28 to 30 
        ("reserved_31"                       , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class CUR_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CUR_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
