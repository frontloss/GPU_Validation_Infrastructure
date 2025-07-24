import ctypes
 
'''
Register instance and offset 
'''
TRANS_VRR_CTL_A = 0x60420 
TRANS_VRR_CTL_B = 0x61420 
TRANS_VRR_CTL_C = 0x62420 
TRANS_VRR_CTL_D = 0x63420 
TRANS_VRR_CTL_EDP = 0x6F420 

 
'''
Register field expected values 
'''
flip_line_enable_DISABLE = 0b0 
flip_line_enable_ENABLE = 0b1 
framestart_to_pipeline_full_linecount_DEFAULT = 0x20 
ignore_max_shift_DO_NOT_IGNORE = 0b0 
ignore_max_shift_IGNORE = 0b1 
pipeline_full_override_HW_GENERATED_PIPELINE_FULL_LINE_COUNT = 0b0 
pipeline_full_override_PROGRAMMED_PIPELINE_FULL_LINE_COUNT = 0b1 
vrr_enable_DISABLE = 0b0 
vrr_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class TRANS_VRR_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("pipeline_full_override"               , ctypes.c_uint32, 1), # 0 to 0 
        ("reserved_1"                           , ctypes.c_uint32, 2), # 1 to 2 
        ("framestart_to_pipeline_full_linecount" , ctypes.c_uint32, 8), # 3 to 10 
        ("reserved_11"                          , ctypes.c_uint32, 18), # 11 to 28 
        ("reserved_29"                          , ctypes.c_uint32, 1), # 29 to 29 
        ("ignore_max_shift"                     , ctypes.c_uint32, 1), # 30 to 30 
        ("vrr_enable"                           , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class TRANS_VRR_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_VRR_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
