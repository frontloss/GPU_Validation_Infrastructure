import ctypes
 
'''
Register instance and offset 
'''
CSC_MODE_A = 0x49028 
CSC_MODE_B = 0x49128 
CSC_MODE_C = 0x49228 
CSC_MODE_D = 0x49328 
 
'''
Register field expected values 
'''
allow_double_buffer_update_disable_ALLOWED = 0b1 
allow_double_buffer_update_disable_NOT_ALLOWED = 0b0 
csc_position_CSC_AFTER = 0b0 
csc_position_CSC_BEFORE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class CSC_MODE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"  , ctypes.c_uint32, 30), # 0 to 29 
        ("pipe_output_csc_enable" , ctypes.c_uint32, 1), # 30 to 30 
        ("pipe_csc_enable" , ctypes.c_uint32, 1), # 31 to 31 
    ]
    

 
class CSC_MODE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CSC_MODE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
