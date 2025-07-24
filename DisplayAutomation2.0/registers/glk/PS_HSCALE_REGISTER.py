import ctypes
 
'''
Register instance and offset 
'''
PS_HSCALE_1_A = 0x68190 
PS_HSCALE_1_B = 0x68990 
PS_HSCALE_1_C = 0x69190 
PS_HSCALE_2_A = 0x68290 
PS_HSCALE_2_B = 0x68A90 
PS_HSCALE_2_C = 0x69290 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PS_HSCALE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("hscale_frac" , ctypes.c_uint32, 15), # 0 to 14 
        ("hscale_int" , ctypes.c_uint32, 3), # 15 to 17 
        ("reserved_18" , ctypes.c_uint32, 14), # 18 to 31 
    ]

 
class PS_HSCALE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PS_HSCALE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
