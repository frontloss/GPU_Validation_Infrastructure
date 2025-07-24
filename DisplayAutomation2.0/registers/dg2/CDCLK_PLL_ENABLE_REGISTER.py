import ctypes
 
'''
Register instance and offset 
'''
CDCLK_PLL_ENABLE = 0x46070

 
'''
Register field expected values 
'''
freq_change_ack_NO_PENDING_REQUEST_OR_REQUEST_NOT_FINISHED = 0b0 
freq_change_ack_REQUEST_FINISHED = 0b1 
freq_change_req_NO_REQUEST_PENDING = 0b0 
freq_change_req_REQUEST_PENDING = 0b1 
pll_enable_DISABLE = 0b0 
pll_enable_ENABLE = 0b1 
pll_lock_LOCKED = 0b1 
pll_lock_NOT_LOCKED_OR_NOT_ENABLED = 0b0 
pll_ratio_28_DEFAULT = 0x1C
slow_clock_enable_DISABLE = 0b0 
slow_clock_enable_ENABLE = 0b1 
slow_clock_lock_LOCKED = 0b1 
slow_clock_lock_NOT_LOCKED_OR_NOT_ENABLED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class CDCLK_PLL_ENABLE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("pll_ratio"           , ctypes.c_uint32, 8), # 7 to 0 
		("reserved_8", ctypes.c_uint32, 3),  # 10 to 8
        ("unexpected_loss_lock" , ctypes.c_uint32, 1), # 11 to 11 
		("reserved_12", ctypes.c_uint32, 10),  # 21 to 12
        ("freq_change_ack"     , ctypes.c_uint32, 1), # 22 to 22 
        ("freq_change_req"     , ctypes.c_uint32, 1), # 23 to 23
		("reserved_24", ctypes.c_uint32, 2),  # 25 to 24 
        ("slow_clock_lock"     , ctypes.c_uint32, 1), # 26 to 26 
        ("slow_clock_enable"   , ctypes.c_uint32, 1), # 27 to 27
		("reserved_28", ctypes.c_uint32, 2),  # 29 to 28 
        ("pll_lock"            , ctypes.c_uint32, 1), # 30 to 30 
        ("pll_enable"          , ctypes.c_uint32, 1) # 31 to 31 
    ]

 
class CDCLK_PLL_ENABLE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CDCLK_PLL_ENABLE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
