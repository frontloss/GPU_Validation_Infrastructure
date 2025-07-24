import ctypes
 
'''
Register instance and offset 
'''
DC_STATE_BOOTSTRAP = 0x45510 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DC_STATE_BOOTSTRAP_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("head_pointer" , ctypes.c_uint32, 16), # 0 to 15 
        ("tail_pointer" , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class DC_STATE_BOOTSTRAP_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DC_STATE_BOOTSTRAP_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
