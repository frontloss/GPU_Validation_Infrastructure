import ctypes
 
'''
Register instance and offset 
'''
PIPE_SRCSZ_A = 0x6001C 
PIPE_SRCSZ_B = 0x6101C 
PIPE_SRCSZ_C = 0x6201C
PIPE_SRCSZ_D = 0x6301C
PIPE_SRCSZ_ERLY_TPT_A = 0x70074
PIPE_SRCSZ_TPT_B = 0x71074
PIPE_SRCSZ_TPT_C = 0x72074
PIPE_SRCSZ_TPT_D = 0x73074
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PIPE_SRCSZ_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("vertical_source_size"  , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"           , ctypes.c_uint32, 3), # 13 to 15 
        ("horizontal_source_size" , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29"           , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class PIPE_SRCSZ_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_SRCSZ_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
