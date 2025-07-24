import ctypes
 
'''
Register instance and offset 
'''
WM_LINETIME_A = 0x45270 
WM_LINETIME_B = 0x45274 
WM_LINETIME_C = 0x45278
WM_LINETIME_D = 0x4527C

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class WM_LINETIME_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("line_time"    , ctypes.c_uint32, 9), # 0 to 8 
        ("reserved_9"   , ctypes.c_uint32, 7), # 9 to 15 
        ("reserved_16"  , ctypes.c_uint32, 9), # 16 to 24 
        ("reserved_25"  , ctypes.c_uint32, 7), # 25 to 31 
    ]

 
class WM_LINETIME_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      WM_LINETIME_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
