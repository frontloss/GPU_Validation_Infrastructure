import ctypes
 
'''
Register instance and offset 
'''
PS_WIN_POS_1_A = 0x68170 
PS_WIN_POS_1_B = 0x68970 
PS_WIN_POS_1_C = 0x69170 
PS_WIN_POS_2_A = 0x68270 
PS_WIN_POS_2_B = 0x68A70 
PS_WIN_POS_2_C = 0x69270 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PS_WIN_POS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("ypos"       , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13" , ctypes.c_uint32, 3), # 13 to 15 
        ("xpos"       , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29" , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class PS_WIN_POS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PS_WIN_POS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
