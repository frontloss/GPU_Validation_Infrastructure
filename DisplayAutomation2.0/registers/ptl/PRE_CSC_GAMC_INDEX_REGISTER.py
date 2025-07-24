import ctypes
 
'''
Register instance and offset 
'''
PRE_CSC_GAMC_INDEX_A = 0x4A484 
PRE_CSC_GAMC_INDEX_B = 0x4AC84 
PRE_CSC_GAMC_INDEX_C = 0x4B484 
PRE_CSC_GAMC_INDEX_D = 0x4BC84 
 
'''
Register field expected values 
'''
index_auto_increment_AUTO_INCREMENT = 0b1 
index_auto_increment_NO_INCREMENT = 0b0 
index_value_DEFAULT = [0, 34]

 
'''
Register bitfield defnition structure 
'''
class PRE_CSC_GAMC_INDEX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("index_value"         , ctypes.c_uint32, 6), # 0 to 5 
        ("reserved_6"          , ctypes.c_uint32, 4), # 6 to 9 
        ("index_auto_increment" , ctypes.c_uint32, 1), # 10 to 10 
        ("reserved_11"         , ctypes.c_uint32, 21), # 11 to 31 
    ]

 
class PRE_CSC_GAMC_INDEX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PRE_CSC_GAMC_INDEX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
