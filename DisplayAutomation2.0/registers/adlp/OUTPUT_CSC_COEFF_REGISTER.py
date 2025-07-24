import ctypes
 
'''
Register instance and offset 
'''
OUTPUT_CSC_COEFF_A = 0x49050 
OUTPUT_CSC_COEFF_B = 0x49150 
OUTPUT_CSC_COEFF_C = 0x49250 
OUTPUT_CSC_COEFF_D = 0x49350 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class OUTPUT_CSC_COEFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("coeff2"        , ctypes.c_uint32, 16), # 0 to 15 
          
        ("coeff1"        , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class OUTPUT_CSC_COEFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      OUTPUT_CSC_COEFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
