import ctypes
 
'''
Register instance and offset 
'''
PAL_PREC_INDEX_A = 0x4A400 
PAL_PREC_INDEX_B = 0x4AC00 
PAL_PREC_INDEX_C = 0x4B400 

 
'''
Register field expected values 
'''
index_auto_increment_AUTO_INCREMENT = 0b1 
index_auto_increment_NO_INCREMENT = 0b0 
index_value_DEFAULT = [0, 1023]
precision_palette_format_NON_SPLIT = 0b0 
precision_palette_format_SPLIT = 0b1 

 
'''
Register bitfield defnition structure 
'''
class PAL_PREC_INDEX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("index_value"         , ctypes.c_uint32, 10), # 0 to 9 
        ("reserved_10"         , ctypes.c_uint32, 5), # 10 to 14 
        ("index_auto_increment" , ctypes.c_uint32, 1), # 15 to 15 
        ("reserved_16"         , ctypes.c_uint32, 15), # 16 to 30 
        ("reserved_31"         , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PAL_PREC_INDEX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PAL_PREC_INDEX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
