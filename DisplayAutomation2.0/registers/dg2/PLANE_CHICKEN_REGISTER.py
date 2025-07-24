import ctypes
 
'''
Register instance and offset 
'''
PLANE_CHICKEN_1_A  = 0x7026c 
PLANE_CHICKEN_1_B  = 0x7126c 
PLANE_CHICKEN_1_C  = 0x7226c 
PLANE_CHICKEN_1_D  = 0x7326c 

PLANE_CHICKEN_2_A  = 0x7036c 
PLANE_CHICKEN_2_B  = 0x7136c 
PLANE_CHICKEN_2_C  = 0x7236c 
PLANE_CHICKEN_2_D  = 0x7336c 

PLANE_CHICKEN_3_A  = 0x7046c 
PLANE_CHICKEN_3_B  = 0x7146c 
PLANE_CHICKEN_3_C  = 0x7246c 
PLANE_CHICKEN_3_D  = 0x7346c 

PLANE_CHICKEN_4_A  = 0x7056c 
PLANE_CHICKEN_4_B  = 0x7156c 
PLANE_CHICKEN_4_C  = 0x7256c 
PLANE_CHICKEN_4_D  = 0x7356c 

PLANE_CHICKEN_5_A  = 0x7066c 
PLANE_CHICKEN_5_B  = 0x7166c 
PLANE_CHICKEN_5_C  = 0x7266c 
PLANE_CHICKEN_5_D  = 0x7366c


'''
Register field expected values 
'''
alpha_blend_bypass_disable_DISABLE = 0b1 
alpha_blend_bypass_disable_ENABLE = 0b0 
linear_interlace_extended_stride_disable_DISABLE = 0b1 
linear_interlace_extended_stride_disable_ENABLE = 0b0 
fp16_non_linear_support_DISABLE = 0b1 
fp16_non_linear_support_ENABLE = 0b0 
enable_line_number_start_advertisement_ENABLE = 0b1 
enable_line_number_start_advertisement_DISABLE = 0b0 
revert_smooth_sync_surface_base_mux_ENABLE = 0b1 
revert_smooth_sync_surface_base_mux_DISABLE = 0b0 


 
'''
Register bitfield defnition structure 
'''
class PLANE_CHICKEN_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("alpha_blend_bypass_disable"                , ctypes.c_uint32, 1), # 0 to 0 
        ("linear_interlace_extended_stride_disable"  , ctypes.c_uint32, 1), # 1 to 1 
        ("fp16_non_linear_support"                   , ctypes.c_uint32, 1), # 2 to 2 
        ("enable_line_number_start_advertisement"    , ctypes.c_uint32, 1), # 3 to 3 
        ("revert_smooth_sync_surface_base_mux"       , ctypes.c_uint32, 1), # 4 to 4 
        ("spare_5"                                   , ctypes.c_uint32, 1), # 5 to 5 
        ("spare_6"                                   , ctypes.c_uint32, 1), # 6 to 6 
        ("spare_7"                                   , ctypes.c_uint32, 1), # 7 to 7 
        ("spare_8"                                   , ctypes.c_uint32, 1), # 8 to 8 
        ("spare_9"                                   , ctypes.c_uint32, 1), # 9 to 9 
        ("spare_10"                                  , ctypes.c_uint32, 1), # 10 to 10 
        ("spare_11"                                  , ctypes.c_uint32, 1), # 11 to 11 
        ("spare_12"                                  , ctypes.c_uint32, 1), # 12 to 12 
        ("spare_13"                                  , ctypes.c_uint32, 1), # 13 to 13 
        ("spare_14"                                  , ctypes.c_uint32, 1), # 14 to 14 
        ("spare_15"                                  , ctypes.c_uint32, 1), # 15 to 15 
        ("spare_16"                                  , ctypes.c_uint32, 1), # 16 to 16 
        ("spare_17"                                  , ctypes.c_uint32, 1), # 17 to 17 
        ("spare_18"                                  , ctypes.c_uint32, 1), # 18 to 18 
        ("spare_19"                                  , ctypes.c_uint32, 1), # 19 to 19 
        ("spare_20"                                  , ctypes.c_uint32, 1), # 20 to 20 
        ("spare_21"                                  , ctypes.c_uint32, 1), # 21 to 21 
        ("spare_22"                                  , ctypes.c_uint32, 1), # 22 to 22 
        ("spare_23"                                  , ctypes.c_uint32, 1), # 23 to 23 
        ("spare_24"                                  , ctypes.c_uint32, 1), # 24 to 24 
        ("spare_25"                                  , ctypes.c_uint32, 1), # 25 to 25 
        ("spare_26"                                  , ctypes.c_uint32, 1), # 26 to 26 
        ("spare_27"                                  , ctypes.c_uint32, 1), # 27 to 27 
        ("spare_28"                                  , ctypes.c_uint32, 1), # 28 to 28 
        ("spare_29"                                  , ctypes.c_uint32, 1), # 29 to 29 
        ("spare_30"                                  , ctypes.c_uint32, 1), # 30 to 30 
        ("spare_31"                                  , ctypes.c_uint32, 1), # 31 to 31 

    ]

 
class PLANE_CHICKEN_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_CHICKEN_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
