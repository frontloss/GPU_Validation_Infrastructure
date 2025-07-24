import ctypes
 
'''
Register instance and offset 
'''
PAL_EXT2_GC_MAX_A = 0x4A430 
PAL_EXT2_GC_MAX_B = 0x4AC30 
PAL_EXT2_GC_MAX_C = 0x4B430 

 
'''
Register field expected values 
'''
blue_ext_max_gc_point_DEFAULT = 0b1111111111111111111 
green_ext_max_gc_point_DEFAULT = 0b1111111111111111111 
red_ext_max_gc_point_DEFAULT = 0b1111111111111111111 

 
'''
Register bitfield defnition structure 
'''
class PAL_EXT2_GC_MAX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("red_ext_max_gc_point"  , ctypes.c_uint32, 19), # 0 to 18 
        ("blue_ext_max_gc_point" , ctypes.c_uint32, 19), # 0 to 18 
        ("green_ext_max_gc_point" , ctypes.c_uint32, 19), # 0 to 18 
        ("reserved_19"           , ctypes.c_uint32, 13), # 19 to 31 
    ]

 
class PAL_EXT2_GC_MAX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PAL_EXT2_GC_MAX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
