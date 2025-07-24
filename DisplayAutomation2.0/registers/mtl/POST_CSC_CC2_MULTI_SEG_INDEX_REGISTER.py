import ctypes
 
'''
Register instance and offset 
'''
POST_CSC_CC2_MULTI_SEG_INDEX_A = 0x4A510
POST_CSC_CC2_MULTI_SEG_INDEX_B = 0x4AD10

'''
Register field expected values 
'''
index_auto_increment_AUTO_INCREMENT = 0b1 
index_auto_increment_NO_INCREMENT = 0b0 
index_value_DEFAULT = [0, 17]

 
'''
Register bitfield defnition structure 
'''
class POST_CSC_CC2_MULTI_SEG_INDEX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("index_value"         , ctypes.c_uint32, 5), # 0 to 4 
        ("reserved_5"          , ctypes.c_uint32, 10), # 5 to 14 
        ("index_auto_increment" , ctypes.c_uint32, 1), # 15 to 15 
        ("reserved_16"         , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class POST_CSC_CC2_MULTI_SEG_INDEX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      POST_CSC_CC2_MULTI_SEG_INDEX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
