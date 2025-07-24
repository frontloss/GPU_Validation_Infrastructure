import ctypes
 
'''
Register instance and offset 
'''
PLANE_INPUT_CSC_COEFF_1_A = 0x701E0 
PLANE_INPUT_CSC_COEFF_1_B = 0x711E0 
PLANE_INPUT_CSC_COEFF_1_C = 0x721E0 
PLANE_INPUT_CSC_COEFF_2_A = 0x702E0 
PLANE_INPUT_CSC_COEFF_2_B = 0x712E0 
PLANE_INPUT_CSC_COEFF_2_C = 0x722E0 
PLANE_INPUT_CSC_COEFF_3_A = 0x703E0 
PLANE_INPUT_CSC_COEFF_3_B = 0x713E0 
PLANE_INPUT_CSC_COEFF_3_C = 0x723E0 
PLANE_INPUT_CSC_COEFF_4_A = 0x704E0 
PLANE_INPUT_CSC_COEFF_4_B = 0x714E0 
PLANE_INPUT_CSC_COEFF_4_C = 0x724E0 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_INPUT_CSC_COEFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("coeff2"        , ctypes.c_uint32, 16), # 0 to 15 
          
        ("coeff1"        , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class PLANE_INPUT_CSC_COEFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_INPUT_CSC_COEFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
