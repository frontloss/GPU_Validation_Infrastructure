import ctypes
 
'''
Register instance and offset 
'''
CSC_COEFF_A = 0x49010 
CSC_COEFF_B = 0x49110 
CSC_COEFF_C = 0x49210 
CSC_COEFF_D = 0x49310 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class CSC_COEFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("coeff2"        , ctypes.c_uint32, 16), # 0 to 15 
          
        ("coeff1"        , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class CSC_COEFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CSC_COEFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
