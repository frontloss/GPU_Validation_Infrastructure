import ctypes
 
'''
Register instance and offset 
'''
PLANE_POS_1_A = 0x7018C 
PLANE_POS_1_B = 0x7118C 
PLANE_POS_1_C = 0x7218C 
PLANE_POS_2_A = 0x7028C 
PLANE_POS_2_B = 0x7128C 
PLANE_POS_2_C = 0x7228C 
PLANE_POS_3_A = 0x7038C 
PLANE_POS_3_B = 0x7138C 
PLANE_POS_3_C = 0x7238C 
PLANE_POS_4_A = 0x7048C 
PLANE_POS_4_B = 0x7148C 
PLANE_POS_4_C = 0x7248C 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_POS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("x_position" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13" , ctypes.c_uint32, 3), # 13 to 15 
        ("y_position" , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29" , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class PLANE_POS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_POS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
