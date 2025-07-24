import ctypes
 
'''
Register instance and offset 
'''
PIPE_BOTTOM_COLOR_A = 0x70034 
PIPE_BOTTOM_COLOR_B = 0x71034 
PIPE_BOTTOM_COLOR_C = 0x72034 

 
'''
Register field expected values 
'''
pipe_csc_enable_DISABLE = 0b0 
pipe_csc_enable_ENABLE = 0b1 
pipe_gamma_enable_DISABLE = 0b0 
pipe_gamma_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class PIPE_BOTTOM_COLOR_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("u_b_bottom_color" , ctypes.c_uint32, 10), # 0 to 9 
        ("y_g_bottom_color" , ctypes.c_uint32, 10), # 10 to 19 
        ("v_r_bottom_color" , ctypes.c_uint32, 10), # 20 to 29 
        ("pipe_csc_enable"  , ctypes.c_uint32, 1), # 30 to 30 
        ("pipe_gamma_enable" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PIPE_BOTTOM_COLOR_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_BOTTOM_COLOR_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
