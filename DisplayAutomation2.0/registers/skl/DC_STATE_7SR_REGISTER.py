import ctypes
 
'''
Register instance and offset 
'''
DC_STATE_7SR = 0x45514 

 
'''
Register field expected values 
'''
restore_done_DONE = 0b1 
restore_done_NOT_DONE = 0b0 
save_start_DO_NOT_START = 0b0 
save_start_START = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DC_STATE_7SR_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("save_start"  , ctypes.c_uint32, 1), # 0 to 0 
        ("reserved_1"  , ctypes.c_uint32, 15), # 1 to 15 
        ("restore_done" , ctypes.c_uint32, 1), # 16 to 16 
        ("reserved_17" , ctypes.c_uint32, 15), # 17 to 31 
    ]

 
class DC_STATE_7SR_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DC_STATE_7SR_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
