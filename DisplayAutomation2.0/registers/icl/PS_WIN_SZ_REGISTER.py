import ctypes
 
'''
Register instance and offset 
'''
PS_WIN_SZ_1_A = 0x68174 
PS_WIN_SZ_1_B = 0x68974 
PS_WIN_SZ_1_C = 0x69174 
PS_WIN_SZ_2_A = 0x68274 
PS_WIN_SZ_2_B = 0x68A74 
PS_WIN_SZ_2_C = 0x69274
PS_WIN_SZ_1_D = 0x69974
PS_WIN_SZ_2_D = 0x69A74

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PS_WIN_SZ_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("ysize"      , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13" , ctypes.c_uint32, 3), # 13 to 15 
        ("xsize"      , ctypes.c_uint32, 14), # 16 to 29 
        ("reserved_30" , ctypes.c_uint32, 2), # 30 to 31 
    ]

 
class PS_WIN_SZ_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PS_WIN_SZ_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
