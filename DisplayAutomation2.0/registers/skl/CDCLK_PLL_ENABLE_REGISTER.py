import ctypes
 
'''
Register instance and offset 
'''
CDCLK_PLL_ENABLE = 0x46070 

 
'''
Register field expected values 
'''
pll_enable_DISABLE = 0b0 
pll_enable_ENABLE = 0b1 
pll_lock_LOCKED = 0b1 
pll_lock_NOT_LOCKED_OR_NOT_ENABLED = 0b0 
pll_ratio_28 = 0x1C
pll_ratio_44 = 0x2C
pll_ratio_RESERVED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class CDCLK_PLL_ENABLE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("pll_ratio" , ctypes.c_uint32, 8), # 0 to 7 
        ("reserved_8" , ctypes.c_uint32, 22), # 8 to 29 
        ("pll_lock"  , ctypes.c_uint32, 1), # 30 to 30 
        ("pll_enable" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class CDCLK_PLL_ENABLE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CDCLK_PLL_ENABLE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
