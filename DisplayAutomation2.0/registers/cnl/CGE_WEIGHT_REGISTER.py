import ctypes
 
'''
Register instance and offset 
'''
CGE_WEIGHT_A = 0x49090
CGE_WEIGHT_B = 0x49190
CGE_WEIGHT_C = 0x49290

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class CGE_WEIGHT_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("cge_weight_index_0" , ctypes.c_uint32, 6), # 0 to 5 
        ("reserved_6"        , ctypes.c_uint32, 2), # 6 to 7 
        ("cge_weight_index_1" , ctypes.c_uint32, 6), # 8 to 13 
        ("reserved_14"       , ctypes.c_uint32, 2), # 14 to 15 
        ("cge_weight_index_2" , ctypes.c_uint32, 6), # 16 to 21 
        ("reserved_22"       , ctypes.c_uint32, 2), # 22 to 23 
        ("cge_weight_index_3" , ctypes.c_uint32, 6), # 24 to 29 
        ("reserved_30"       , ctypes.c_uint32, 2), # 30 to 31 
    ]

 
class CGE_WEIGHT_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CGE_WEIGHT_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
