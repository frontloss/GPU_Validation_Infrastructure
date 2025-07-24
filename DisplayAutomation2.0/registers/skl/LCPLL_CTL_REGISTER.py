import ctypes
 
'''
Register instance and offset 
'''
LCPLL_CTL = 0x130040 

 
'''
Register field expected values 
'''
cd2x_clock_disable_DISABLE = 0b1 
cd2x_clock_disable_ENABLE = 0b0 
cd_clock_disable_DISABLE = 0b1 
cd_clock_disable_ENABLE = 0b0 
cd_frequency_select_337_5_MHZ = 0b10 
cd_frequency_select_450_MHZ = 0b00 
cd_frequency_select_540_MHZ = 0b01 
cd_frequency_select_675_MHZ = 0b11 
cd_source_fclk_DONE = 0b1 
cd_source_fclk_NOT_DONE = 0b0 
cd_source_select_FCLK = 0b1 
cd_source_select_LCPLL = 0b0 
cd_source_switching_IN_PROGRESS = 0b1 
cd_source_switching_NOT_IN_PROGRESS = 0b0 
display_power_down_allow_ALLOW = 0b1 
display_power_down_allow_DO_NOT_ALLOW = 0b0 
pll_disable_DISABLE = 0b1 
pll_disable_ENABLE = 0b0 
pll_lock_LOCKED = 0b1 
pll_lock_NOT_LOCKED_OR_NOT_ENABLED = 0b0 
reference_select_BCLK = 0b10 
reference_select_NON_SSC = 0b00 
reference_select_RESERVED = 0b0 
reference_select_SSC = 0b11 
root_cd2x_clock_disable_DISABLE = 0b1 
root_cd2x_clock_disable_ENABLE = 0b0 

 
'''
Register bitfield defnition structure 
'''
class LCPLL_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"              , ctypes.c_uint32, 19), # 0 to 18 
        ("cd_source_fclk"          , ctypes.c_uint32, 1), # 19 to 19 
        ("cd_source_switching"     , ctypes.c_uint32, 1), # 20 to 20 
        ("cd_source_select"        , ctypes.c_uint32, 1), # 21 to 21 
        ("display_power_down_allow" , ctypes.c_uint32, 1), # 22 to 22 
        ("cd2x_clock_disable"      , ctypes.c_uint32, 1), # 23 to 23 
        ("root_cd2x_clock_disable" , ctypes.c_uint32, 1), # 24 to 24 
        ("cd_clock_disable"        , ctypes.c_uint32, 1), # 25 to 25 
        ("cd_frequency_select"     , ctypes.c_uint32, 2), # 26 to 27 
        ("reference_select"        , ctypes.c_uint32, 2), # 28 to 29 
        ("pll_lock"                , ctypes.c_uint32, 1), # 30 to 30 
        ("pll_disable"             , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class LCPLL_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      LCPLL_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
