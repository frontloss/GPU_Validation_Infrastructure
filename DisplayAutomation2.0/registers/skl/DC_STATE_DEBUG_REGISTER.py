import ctypes
 
'''
Register instance and offset 
'''
DC_STATE_DEBUG = 0x45520 

 
'''
Register field expected values 
'''
mask_cores_DO_NOT_MASK = 0b0 
mask_cores_MASK = 0b1 
mask_memory_up_DO_NOT_MASK = 0b0 
mask_memory_up_MASK = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DC_STATE_DEBUG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("mask_cores"    , ctypes.c_uint32, 1), # 0 to 0 
        ("mask_memory_up" , ctypes.c_uint32, 1), # 1 to 1 
        ("reserved_2"    , ctypes.c_uint32, 30), # 2 to 31 
    ]

 
class DC_STATE_DEBUG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DC_STATE_DEBUG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
