import ctypes
 
'''
Register instance and offset 
'''
PS_VSCALE_1_A = 0x68184 
PS_VSCALE_1_B = 0x68984 
PS_VSCALE_1_C = 0x69184 
PS_VSCALE_2_A = 0x68284 
PS_VSCALE_2_B = 0x68A84 
PS_VSCALE_2_C = 0x69284 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PS_VSCALE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("vscale_frac" , ctypes.c_uint32, 15), # 0 to 14 
        ("vscale_int" , ctypes.c_uint32, 3), # 15 to 17 
        ("reserved_18" , ctypes.c_uint32, 14), # 18 to 31 
    ]

 
class PS_VSCALE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PS_VSCALE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
