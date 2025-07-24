import ctypes
 
'''
Register instance and offset 
'''
CSC_COEFF_1_A = 0x49010
CSC_COEFF_1_B = 0x49110
CSC_COEFF_1_C = 0x49210

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class CSC_COEFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("gy" , ctypes.c_uint32, 16), # 0 to 15 
        ("ry" , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class CSC_COEFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CSC_COEFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
