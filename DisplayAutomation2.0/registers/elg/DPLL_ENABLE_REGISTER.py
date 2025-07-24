import ctypes
 
'''
Register instance and offset 
'''
DPLL0_ENABLE = 0x46010
DPLL1_ENABLE = 0x46014
DPLL4_ENABLE = 0x46018
LJPLL0_ENABLE = 0x46050
LJPLL1_ENABLE = 0x46054
MGPLL1_ENABLE = 0x46030
MGPLL2_ENABLE = 0x46034
MGPLL3_ENABLE = 0x46038
MGPLL4_ENABLE = 0x4603C
MGPLL5_ENABLE = 0x46040
MGPLL6_ENABLE = 0x46044
TBT_PLL_ENABLE = 0x46020

 
'''
Register field expected values 
'''
pll_enable_DISABLE = 0b0 
pll_enable_ENABLE = 0b1 
pll_lock_LOCKED = 0b1 
pll_lock_NOT_LOCKED_OR_NOT_ENABLED = 0b0 
pll_refclk_select_GENLOCK = 0b1 
pll_refclk_select_REFCLK = 0b0 
power_enable_DISABLE = 0b0 
power_enable_ENABLE = 0b1 
power_state_DISABLED = 0b0 
power_state_ENABLED = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DPLL_ENABLE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
		("reserved_0", ctypes.c_uint32, 11),  # 10 to 0
        ("unexpected_loss_lock" , ctypes.c_uint32, 1), # 11 to 11
		("reserved_12", ctypes.c_uint32, 14),  # 25 to 12 
        ("power_state"         , ctypes.c_uint32, 1), # 26 to 26 
        ("power_enable"        , ctypes.c_uint32, 1), # 27 to 27
		("reserved_28", ctypes.c_uint32, 1),  # 28 to 28 
        ("pll_refclk_select"   , ctypes.c_uint32, 1), # 29 to 29 
        ("pll_lock"            , ctypes.c_uint32, 1), # 30 to 30 
        ("pll_enable"          , ctypes.c_uint32, 1) # 31 to 31 
    ]

 
class DPLL_ENABLE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_ENABLE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
