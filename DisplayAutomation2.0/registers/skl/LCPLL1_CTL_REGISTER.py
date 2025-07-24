import ctypes
 
'''
Register instance and offset 
'''
LCPLL1_CTL = 0x46010 

 
'''
Register field expected values 
'''
pll_enable_DISABLE = 0b0 
pll_enable_ENABLE = 0b1 
pll_lock_LOCKED = 0b1 
pll_lock_NOT_LOCKED_OR_NOT_ENABLED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class LCPLL1_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"      , ctypes.c_uint32, 28), # 0 to 27 
        ("reference_select" , ctypes.c_uint32, 2), # 28 to 29 
        ("pll_lock"        , ctypes.c_uint32, 1), # 30 to 30 
        ("pll_enable"      , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class LCPLL1_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      LCPLL1_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
