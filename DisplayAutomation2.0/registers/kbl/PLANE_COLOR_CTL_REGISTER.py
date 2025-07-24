import ctypes
 
'''
Register instance and offset 
'''
PLANE_COLOR_CTL_1_A = 0x701CC 
PLANE_COLOR_CTL_1_B = 0x711CC 
PLANE_COLOR_CTL_1_C = 0x721CC 
PLANE_COLOR_CTL_2_A = 0x702CC 
PLANE_COLOR_CTL_2_B = 0x712CC 
PLANE_COLOR_CTL_2_C = 0x722CC 
PLANE_COLOR_CTL_3_A = 0x703CC 
PLANE_COLOR_CTL_3_B = 0x713CC 
PLANE_COLOR_CTL_3_C = 0x723CC 
PLANE_COLOR_CTL_4_A = 0x704CC 
PLANE_COLOR_CTL_4_B = 0x714CC 
PLANE_COLOR_CTL_4_C = 0x724CC 

 
'''
Register field expected values 
'''
alpha_mode_DISABLE = 0b00 
alpha_mode_ENABLE_WITH_HW_PRE_MULTIPLY = 0b11 
alpha_mode_ENABLE_WITH_SW_PRE_MULTIPLY = 0b10 
pipe_csc_enable_DISABLE = 0b0 
pipe_csc_enable_ENABLE = 0b1 
pipe_gamma_enable_DISABLE = 0b0 
pipe_gamma_enable_ENABLE = 0b1 
plane_csc_mode_BYPASS = 0b000 
plane_csc_mode_RGB709_TO_RGB2020 = 0b100 
plane_csc_mode_YUV2020_TO_RGB2020 = 0b011 
plane_csc_mode_YUV601_TO_RGB709 = 0b001 
plane_csc_mode_YUV709_TO_RGB709 = 0b010 
plane_gamma_disable_DISABLE = 0b1 
plane_gamma_disable_ENABLE = 0b0 
plane_pre_csc_gamma_enable_DISABLE = 0b0 
plane_pre_csc_gamma_enable_ENABLE = 0b1 
remove_yuv_offset_PRESERVE = 0b1
remove_yuv_offset_REMOVE = 0b0 
yuv_range_correction_disable_DISABLE = 0b1 
yuv_range_correction_disable_ENABLE = 0b0 

 
'''
Register bitfield defnition structure 
'''
class PLANE_COLOR_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"                  , ctypes.c_uint32, 4), # 0 to 3 
        ("alpha_mode"                  , ctypes.c_uint32, 2), # 4 to 5 
        ("reserved_6"                  , ctypes.c_uint32, 7), # 6 to 12 
        ("plane_gamma_disable"         , ctypes.c_uint32, 1), # 13 to 13 
        ("plane_pre_csc_gamma_enable"  , ctypes.c_uint32, 1), # 14 to 14 
        ("reserved_15"                 , ctypes.c_uint32, 2), # 15 to 16 
        ("plane_csc_mode"              , ctypes.c_uint32, 3), # 17 to 19 
        ("reserved_20"                 , ctypes.c_uint32, 3), # 20 to 22 
        ("pipe_csc_enable"             , ctypes.c_uint32, 1), # 23 to 23 
        ("reserved_24"                 , ctypes.c_uint32, 4), # 24 to 27 
        ("yuv_range_correction_disable" , ctypes.c_uint32, 1), # 28 to 28 
        ("remove_yuv_offset"           , ctypes.c_uint32, 1), # 29 to 29 
        ("pipe_gamma_enable"           , ctypes.c_uint32, 1), # 30 to 30 
        ("reserved_31"                 , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PLANE_COLOR_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_COLOR_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
