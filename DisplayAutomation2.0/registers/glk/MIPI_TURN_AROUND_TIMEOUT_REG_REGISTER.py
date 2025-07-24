import ctypes
 
'''
Register instance and offset 
'''
MIPIA_TURN_AROUND_TIMEOUT_REG = 0x6B018 
MIPIC_TURN_AROUND_TIMEOUT_REG = 0x6B818 

 
'''
Register field expected values 
'''
turn_around_timeout_register_DEFAULT = 0x17 

 
'''
Register bitfield defnition structure 
'''
class MIPI_TURN_AROUND_TIMEOUT_REG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("turn_around_timeout_register" , ctypes.c_uint32, 6), # 0 to 5 
        ("reserved_6"                  , ctypes.c_uint32, 26), # 6 to 31 
    ]

 
class MIPI_TURN_AROUND_TIMEOUT_REG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_TURN_AROUND_TIMEOUT_REG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
