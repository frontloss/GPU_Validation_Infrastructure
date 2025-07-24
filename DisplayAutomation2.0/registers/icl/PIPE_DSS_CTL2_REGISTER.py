import ctypes
 
'''
Register instance and offset 
'''
PIPE_DSS_CTL2_PA = 0x78004
PIPE_DSS_CTL2_PB = 0x78204
PIPE_DSS_CTL2_PC = 0x78404
PIPE_DSS_CTL2_PD = 0x78604

 
'''
Register field expected values 
'''
left_branch_vdsc_enable_DISABLE = 0b0 
left_branch_vdsc_enable_ENABLE = 0b1 
right_branch_vdsc_enable_DISABLE = 0b0 
right_branch_vdsc_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class PIPE_DSS_CTL2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("right_dl_buffer_target_depth" , ctypes.c_uint32, 12), # 0 to 11 
        ("spare_12"                    , ctypes.c_uint32, 1), # 12 to 12 
        ("spare_13"                    , ctypes.c_uint32, 1), # 13 to 13 
        ("spare_14"                    , ctypes.c_uint32, 1), # 14 to 14 
        ("right_branch_vdsc_enable"    , ctypes.c_uint32, 1), # 15 to 15 
        ("reserved_16"                 , ctypes.c_uint32, 8), # 16 to 23 
        ("spare_24"                    , ctypes.c_uint32, 1), # 24 to 24 
        ("spare_25"                    , ctypes.c_uint32, 1), # 25 to 25 
        ("spare_26"                    , ctypes.c_uint32, 1), # 26 to 26 
        ("reserved_27"                 , ctypes.c_uint32, 4), # 27 to 30 
        ("left_branch_vdsc_enable"     , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PIPE_DSS_CTL2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_DSS_CTL2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
