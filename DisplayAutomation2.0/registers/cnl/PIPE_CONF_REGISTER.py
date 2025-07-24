import ctypes
 
'''
Register instance and offset 
'''
PIPE_CONF_A = 0x70008 
PIPE_CONF_B = 0x71008 
PIPE_CONF_C = 0x72008 

 
'''
Register field expected values 
'''
bfi_enable_DISABLE = 0b0 
bfi_enable_ENABLE = 0b1 
bits_per_color_10_BPC = 0b001 
bits_per_color_12_BPC = 0b011 
bits_per_color_6_BPC = 0b010 
bits_per_color_8_BPC = 0b000 
bits_per_color_RESERVED = 0b0 
color_range_select_CE = 0b1 
color_range_select_FULL = 0b0 
display_power_mode_switch_LOW_POWER = 0b1 
display_power_mode_switch_NORMAL = 0b0 
display_rotation_info_180 = 0b10 
display_rotation_info_270 = 0b11 
display_rotation_info_90 = 0b01 
display_rotation_info_NONE = 0b00 
dithering_enable_DISABLE = 0b0 
dithering_enable_ENABLE = 0b1 
dithering_type_SPATIAL = 0b00 
dithering_type_ST1 = 0b01 
dithering_type_ST2 = 0b10 
dithering_type_TEMPORAL = 0b11 
frame_start_delay_FIRST = 0b00 
frame_start_delay_FOURTH = 0b11 
frame_start_delay_SECOND = 0b01 
frame_start_delay_THIRD = 0b10 
interlaced_mode_IF_ID = 0b011 
interlaced_mode_PF_ID = 0b001 
interlaced_mode_PF_PD = 0b000 
interlaced_mode_RESERVED = 0b0 
msa_timing_delay_LINE1 = 0b00 
msa_timing_delay_LINE2 = 0b01 
msa_timing_delay_LINE3 = 0b10 
msa_timing_delay_LINE4 = 0b11 
pipe_enable_DISABLE = 0b0 
pipe_enable_ENABLE = 0b1 
pipe_output_color_space_select_RESERVED = 0b0 
pipe_output_color_space_select_RGB = 0b00 
pipe_output_color_space_select_YUV_601 = 0b01 
pipe_output_color_space_select_YUV_709 = 0b10 
pipe_palette_gamma_mode_10_BT = 0b01 
pipe_palette_gamma_mode_12_BIT = 0b10 
pipe_palette_gamma_mode_8_BIT = 0b00 
pipe_palette_gamma_mode_SPLIT = 0b11 
pipe_state_DISABLED = 0b0 
pipe_state_ENABLED = 0b1 
xcycc_color_range_limit_FULL = 0b0 
xcycc_color_range_limit_LIMIT = 0b1 

 
'''
Register bitfield defnition structure 
'''
class PIPE_CONF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"                    , ctypes.c_uint32, 2), # 0 to 1 
        ("dithering_type"                , ctypes.c_uint32, 2), # 2 to 3 
        ("dithering_enable"              , ctypes.c_uint32, 1), # 4 to 4 
        ("bits_per_color"                , ctypes.c_uint32, 3), # 5 to 7 
        ("bfi_enable"                    , ctypes.c_uint32, 1), # 8 to 8 
        ("reserved_9"                    , ctypes.c_uint32, 1), # 9 to 9 
        ("xcycc_color_range_limit"       , ctypes.c_uint32, 1), # 10 to 10 
        ("pipe_output_color_space_select" , ctypes.c_uint32, 2), # 11 to 12 
        ("color_range_select"            , ctypes.c_uint32, 1), # 13 to 13 
        ("display_rotation_info"         , ctypes.c_uint32, 2), # 14 to 15 
        ("reserved_16"                   , ctypes.c_uint32, 2), # 16 to 17 
        ("msa_timing_delay"              , ctypes.c_uint32, 2), # 18 to 19 
        ("display_power_mode_switch"     , ctypes.c_uint32, 1), # 20 to 20 
        ("interlaced_mode"               , ctypes.c_uint32, 3), # 21 to 23 
        ("pipe_palette_gamma_mode"       , ctypes.c_uint32, 2), # 24 to 25 
        ("reserved_26"                   , ctypes.c_uint32, 1), # 26 to 26 
        ("frame_start_delay"             , ctypes.c_uint32, 2), # 27 to 28 
        ("reserved_29"                   , ctypes.c_uint32, 1), # 29 to 29 
        ("pipe_state"                    , ctypes.c_uint32, 1), # 30 to 30 
        ("pipe_enable"                   , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PIPE_CONF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_CONF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
