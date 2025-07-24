import ctypes
 
'''
Register instance and offset 
'''
CSC_CC2_COEFF_A = 0x4A518
CSC_CC2_COEFF_B = 0x4AD18

'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class CSC_CC2_COEFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("coeff2"        , ctypes.c_uint32, 16), # 0 to 15 
          
        ("coeff1"        , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class CSC_CC2_COEFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CSC_CC2_COEFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
