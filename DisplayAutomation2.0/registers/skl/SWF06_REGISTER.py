import ctypes
 
'''
Register instance and offset 
'''
SWF06 = 0x4F018


'''
Register field expected values 
'''


'''
Register bitfield defnition structure 
'''
class SWF06_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("max_cd_clock_supported"   , ctypes.c_uint32, 11), # 0 to 10
        ("reserved_11"              , ctypes.c_uint32, 21), # 11 to 31
    ]

 
class SWF06_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SWF06_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
