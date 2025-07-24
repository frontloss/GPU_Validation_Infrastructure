import ctypes
 
'''
Register instance and offset 
'''
CDCLK_SQUASH_CTL = 0x46008

 
'''
Register field expected values 
'''

'''
Register bitfield definition structure 
'''
class CDCLK_SQUASH_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("squash_waveform", ctypes.c_uint32, 16), # 15 to 0
        ("reserved_30", ctypes.c_uint32, 8), # 23 to 16
        ("squash_window_size", ctypes.c_uint32, 4), # 27 to 24
        ("reserved_30", ctypes.c_uint32, 3),  # 30 to 28
        ("squash_Enable", ctypes.c_uint32, 1), # 31 to 31
    ]

 
class CDCLK_SQUASH_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CDCLK_SQUASH_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
