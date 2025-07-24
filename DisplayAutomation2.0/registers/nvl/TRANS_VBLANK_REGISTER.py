import ctypes
 
'''
Register instance and offset 
'''
TRANS_VBLANK_A = 0x60010 
TRANS_VBLANK_B = 0x61010 
TRANS_VBLANK_C = 0x62010 
TRANS_VBLANK_D = 0x63010 
TRANS_VBLANK_CMTG0 = 0x6F010
TRANS_VBLANK_CMTG1 = 0x6F110

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class TRANS_VBLANK_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("vertical_blank_start" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"        , ctypes.c_uint32, 3), # 13 to 15 
        ("vertical_blank_end"  , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29"        , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class TRANS_VBLANK_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_VBLANK_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
