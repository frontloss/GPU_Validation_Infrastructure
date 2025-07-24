import ctypes
 
'''
Register instance and offset 
'''
PAL_GC_MAX_A = 0x4A410 
PAL_GC_MAX_B = 0x4AC10 
PAL_GC_MAX_C = 0x4B410 

 
'''
Register field expected values 
'''
blue_max_gc_point_DEFAULT = 0b10000000000000000 
green_max_gc_point_DEFAULT = 0b10000000000000000 
red_max_gc_point_DEFAULT = 0b10000000000000000 

 
'''
Register bitfield defnition structure 
'''
class PAL_GC_MAX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("red_max_gc_point"  , ctypes.c_uint32, 17), # 0 to 16 
        ("blue_max_gc_point" , ctypes.c_uint32, 17), # 0 to 16 
        ("green_max_gc_point" , ctypes.c_uint32, 17), # 0 to 16 
        ("reserved_17"       , ctypes.c_uint32, 15), # 17 to 31 
    ]

 
class PAL_GC_MAX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PAL_GC_MAX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
