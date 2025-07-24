import ctypes
 
'''
Register instance and offset 
'''
PIPE_FRMCNT_A = 0x70040 
PIPE_FRMCNT_B = 0x71040 
PIPE_FRMCNT_C = 0x72040
PIPE_FRMCNT_D = 0x73040

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PIPE_FRMCNT_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("pipe_frame_counter"  , ctypes.c_uint32, 32), # 0 to 31 
    ]

 
class PIPE_FRMCNT_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_FRMCNT_REG ),
        ("asUint", ctypes.c_uint32 ) ]