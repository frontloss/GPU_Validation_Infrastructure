import ctypes
 
'''
Register instance and offset 
'''
PLANE_STRIDE_1_A = 0x70188 
PLANE_STRIDE_1_B = 0x71188 
PLANE_STRIDE_1_C = 0x72188 
PLANE_STRIDE_2_A = 0x70288 
PLANE_STRIDE_2_B = 0x71288 
PLANE_STRIDE_2_C = 0x72288 
PLANE_STRIDE_3_A = 0x70388 
PLANE_STRIDE_3_B = 0x71388 
PLANE_STRIDE_3_C = 0x72388 
PLANE_STRIDE_4_A = 0x70488 
PLANE_STRIDE_4_B = 0x71488 
PLANE_STRIDE_4_C = 0x72488 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_STRIDE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("stride"     , ctypes.c_uint32, 10), # 0 to 9 
        ("reserved_10" , ctypes.c_uint32, 22), # 10 to 31 
    ]

 
class PLANE_STRIDE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_STRIDE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
