import ctypes
 
'''
Register instance and offset 
'''
PIPE_SCANLINE_A = 0x70000 
PIPE_SCANLINE_B = 0x71000 
PIPE_SCANLINE_C = 0x72000 

 
'''
Register field expected values 
'''
current_field_EVEN = 0b1 
current_field_ODD = 0b0 

 
'''
Register bitfield defnition structure 
'''
class PIPE_SCANLINE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("line_counter_for_display" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"             , ctypes.c_uint32, 18), # 13 to 30 
        ("current_field"           , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PIPE_SCANLINE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_SCANLINE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
