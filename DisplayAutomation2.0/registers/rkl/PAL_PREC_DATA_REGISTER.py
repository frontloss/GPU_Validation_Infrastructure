import ctypes
 
'''
Register instance and offset 
'''
PAL_PREC_DATA_A = 0x4A404 
PAL_PREC_DATA_B = 0x4AC04 
PAL_PREC_DATA_C = 0x4B404 

 
'''
Register field expected values 
'''
 
'''
Register bitfield defnition structure 
'''
class PAL_PREC_DATA_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("blue_precision_palette_entry" , ctypes.c_uint32, 10), # 0 to 9 
        ("green_precision_palette_entry" , ctypes.c_uint32, 10), # 10 to 19 
        ("red_precision_palette_entry"  , ctypes.c_uint32, 10), # 20 to 29 
        ("reserved_30"                  , ctypes.c_uint32, 2), # 30 to 31 
    ]

 
class PAL_PREC_DATA_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PAL_PREC_DATA_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
