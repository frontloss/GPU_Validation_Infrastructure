import ctypes
 
'''
Register instance and offset 
'''
CGE_CTRL_A = 0x49080 
CGE_CTRL_B = 0x49180 
CGE_CTRL_C = 0x49280 

 
'''
Register field expected values 
'''
cge_enable_DISABLE = 0b0 
cge_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class CGE_CTRL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0" , ctypes.c_uint32, 31), # 0 to 30 
        ("cge_enable" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class CGE_CTRL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CGE_CTRL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
