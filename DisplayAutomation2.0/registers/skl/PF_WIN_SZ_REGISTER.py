import ctypes
 
'''
Register instance and offset 
'''
PF_WIN_SZ_A = 0x68074 
PF_WIN_SZ_B = 0x68874 
PF_WIN_SZ_C = 0x69074 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PF_WIN_SZ_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("ysize"      , ctypes.c_uint32, 12), # 0 to 11 
        ("reserved_12" , ctypes.c_uint32, 4), # 12 to 15 
        ("xsize"      , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29" , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class PF_WIN_SZ_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PF_WIN_SZ_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
