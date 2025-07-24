import ctypes
 
'''
Register instance and offset 
'''
PLANE_CSC_COEFF_1_A = 0x70210 
PLANE_CSC_COEFF_1_B = 0x71210 
PLANE_CSC_COEFF_1_C = 0x72210 
PLANE_CSC_COEFF_2_A = 0x70310 
PLANE_CSC_COEFF_2_B = 0x71310 
PLANE_CSC_COEFF_2_C = 0x72310 
PLANE_CSC_COEFF_3_A = 0x70410 
PLANE_CSC_COEFF_3_B = 0x71410 
PLANE_CSC_COEFF_3_C = 0x72410 
PLANE_CSC_COEFF_4_A = 0x70510 
PLANE_CSC_COEFF_4_B = 0x71510 
PLANE_CSC_COEFF_4_C = 0x72510 
 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_CSC_COEFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("coeff2"        , ctypes.c_uint32, 16), # 0 to 15 
          
        ("coeff1"        , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class PLANE_CSC_COEFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_CSC_COEFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
