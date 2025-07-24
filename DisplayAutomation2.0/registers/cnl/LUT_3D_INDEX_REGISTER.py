import ctypes
 
'''
Register instance and offset 
'''
LUT_3D_INDEX_A = 0x490A8 

 
'''
Register field expected values 
'''
index_auto_increment_AUTO_INCREMENT = 0b1 
index_auto_increment_NO_INCREMENT = 0b0 
index_value_DEFAULT = [0,4912]

 
'''
Register bitfield defnition structure 
'''
class LUT_3D_INDEX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("index_value"         , ctypes.c_uint32, 13), # 0 to 12 
        ("index_auto_increment" , ctypes.c_uint32, 1), # 13 to 13 
        ("reserved_14"         , ctypes.c_uint32, 18), # 14 to 31 
    ]

 
class LUT_3D_INDEX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      LUT_3D_INDEX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
