import ctypes
 
'''
Register instance and offset 
'''
TRANS_HBLANK_A = 0x60004 
TRANS_HBLANK_B = 0x61004 
TRANS_HBLANK_C = 0x62004 
TRANS_HBLANK_EDP = 0x6F004 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class TRANS_HBLANK_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("horizontal_blank_start" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"            , ctypes.c_uint32, 1), # 13 to 13
        ("reserved_14"          , ctypes.c_uint32, 2), # 14 to 15 
        ("horizontal_blank_end"  , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29"           , ctypes.c_uint32, 1), # 29 to 29
        ("reserved_30"          , ctypes.c_uint32, 2), # 30 to 31 
    ]

 
class TRANS_HBLANK_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_HBLANK_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
