import ctypes
 
'''
Register instance and offset 
'''
PRE_CSC_CC2_GAMC_INDEX_A = 0x4A500
PRE_CSC_CC2_GAMC_INDEX_B = 0x4AD00

 
'''
Register field expected values 
'''
index_auto_increment_AUTO_INCREMENT = 0b1 
index_auto_increment_NO_INCREMENT = 0b0 
index_value_DEFAULT = [0, 34]

 
'''
Register bitfield defnition structure 
'''
class PRE_CSC_CC2_GAMC_INDEX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("index_value"         , ctypes.c_uint32, 8), # 0 to 7
        ("reserved_6"          , ctypes.c_uint32, 2), # 8 to 9
        ("index_auto_increment" , ctypes.c_uint32, 1), # 10 to 10 
        ("reserved_11"         , ctypes.c_uint32, 21), # 11 to 31 
    ]

 
class PRE_CSC_CC2_GAMC_INDEX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PRE_CSC_CC2_GAMC_INDEX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
