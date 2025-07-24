import ctypes
 
'''
Register instance and offset 
'''
GAMMA_MODE_A = 0x4A480
GAMMA_MODE_B = 0x4AC80
GAMMA_MODE_C = 0x4B480 

 
'''
Register field expected values 
'''
allow_double_buffer_update_disable_ALLOWED = 0b1 
allow_double_buffer_update_disable_NOT_ALLOWED = 0b0 
GAMMA_position_GAMMA_AFTER = 0b0 
GAMMA_position_GAMMA_BEFORE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class GAMMA_MODE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("gamma_mode"  , ctypes.c_uint32,2), # 0 to 1 
	("reserved"  , ctypes.c_uint32, 28), # 2 to 29 
        ("post_csc_gamma_enable" , ctypes.c_uint32, 1), # 30 to 30 
        ("pre_csc_gamma_enable" , ctypes.c_uint32, 1) # 31 to 31 
    ]
    

 
class GAMMA_MODE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      GAMMA_MODE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
