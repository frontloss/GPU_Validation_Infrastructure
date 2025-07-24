import ctypes
 
'''
Register instance and offset 
'''
DSS_CTL1 = 0x67400


'''
Register field expected values 
'''
dual_link_mode_FRONT_BACK_MODE = 0b0 
dual_link_mode_INTERLEAVE_MODE = 0b1 
joiner_enable_DISABLE = 0b0 
joiner_enable_ENABLE = 0b1 
splitter_enable_DISABLE = 0b0 
splitter_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DSS_CTL1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("left_dl_buffer_target_depth" , ctypes.c_uint32, 12), # 0 to 11 
        ("reserved_12"                , ctypes.c_uint32, 4), # 12 to 15 
        ("overlap"                    , ctypes.c_uint32, 4), # 16 to 19 
        ("reserved_20"                , ctypes.c_uint32, 4), # 20 to 23 
        ("dual_link_mode"             , ctypes.c_uint32, 1), # 24 to 24 
        ("reserved_25"                , ctypes.c_uint32, 5), # 25 to 29 
        ("joiner_enable"              , ctypes.c_uint32, 1), # 30 to 30 
        ("splitter_enable"            , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DSS_CTL1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSS_CTL1_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
