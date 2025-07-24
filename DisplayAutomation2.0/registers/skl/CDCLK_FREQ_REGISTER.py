import ctypes
 
'''
Register instance and offset 
'''
CDCLK_FREQ = 0x46200 

 
'''
Register field expected values 
'''
cdclk_frequency_450MHZ = 0b0111000001 

 
'''
Register bitfield defnition structure 
'''
class CDCLK_FREQ_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("cdclk_frequency" , ctypes.c_uint32, 10), # 0 to 9 
        ("reserved_10"    , ctypes.c_uint32, 22), # 10 to 31 
    ]

 
class CDCLK_FREQ_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CDCLK_FREQ_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
