import ctypes
 
'''
Register instance and offset 
'''
LUT_3D_CTL_A = 0x490A4 
LUT_3D_CTL_B = 0x491A4
 
'''
Register field expected values 
'''
lut_3d_enable_DISABLE = 0b0 
lut_3d_enable_ENABLE = 0b1 
new_lut_ready_NEW_LUT_NOT_READY = 0b0 
new_lut_ready_NEW_LUT_READY = 0b1 

 
'''
Register bitfield defnition structure 
'''
class LUT_3D_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"   , ctypes.c_uint32, 30), # 0 to 29 
        ("new_lut_ready" , ctypes.c_uint32, 1), # 30 to 30 
        ("lut_3d_enable" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class LUT_3D_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      LUT_3D_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
