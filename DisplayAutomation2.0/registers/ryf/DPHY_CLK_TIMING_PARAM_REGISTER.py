import ctypes
 
'''
Register instance and offset 
'''
DPHY_CLK_TIMING_PARAM_DSI0 = 0x162180 
DPHY_CLK_TIMING_PARAM_DSI1 = 0x06C180 

 
'''
Register field expected values 
'''
clk_post_override_HW_MAINTAINS = 0 
clk_post_override_SW_OVERRIDES = 1 
clk_pre_override_HW_MAINTAINS = 0 
clk_pre_override_SW_OVERRIDES = 1 
clk_prepare_0_25_ESCAPE_CLOCKS = 0b001 
clk_prepare_0_50_ESCAPE_CLOCKS = 0b010 
clk_prepare_0_75_ESCAPE_CLOCKS = 0b011 
clk_prepare_1_00_ESCAPE_CLOCKS = 0b100 
clk_prepare_1_25_ESCAPE_CLOCKS = 0b101 
clk_prepare_1_50_ESCAPE_CLOCKS = 0b110 
clk_prepare_1_75_ESCAPE_CLOCKS = 0b111 
clk_prepare_RESERVED = 0b0 
clk_prepare_override_HW_MAINTAINS = 0b0 
clk_prepare_override_SW_OVERRIDES = 0b1 
clk_trail_override_HW_MAINTAINS = 0 
clk_trail_override_SW_OVERRIDES = 1 
clk_zero_override_HW_MAINTAINS = 0 
clk_zero_override_SW_OVERRIDES = 1 

 
'''
Register bitfield defnition structure 
'''
class DPHY_CLK_TIMING_PARAM_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("clk_trail"           , ctypes.c_uint32, 3), # 0 to 2 
        ("reserved_3"          , ctypes.c_uint32, 4), # 3 to 6 
        ("clk_trail_override"  , ctypes.c_uint32, 1), # 7 to 7 
        ("clk_post"            , ctypes.c_uint32, 3), # 8 to 10 
        ("reserved_11"         , ctypes.c_uint32, 4), # 11 to 14 
        ("clk_post_override"   , ctypes.c_uint32, 1), # 15 to 15 
        ("clk_pre"             , ctypes.c_uint32, 2), # 16 to 17 
        ("reserved_18"         , ctypes.c_uint32, 1), # 18 to 18 
        ("clk_pre_override"    , ctypes.c_uint32, 1), # 19 to 19 
        ("clk_zero"            , ctypes.c_uint32, 4), # 20 to 23 
        ("reserved_24"         , ctypes.c_uint32, 3), # 24 to 26 
        ("clk_zero_override"   , ctypes.c_uint32, 1), # 27 to 27 
        ("clk_prepare"         , ctypes.c_uint32, 3), # 28 to 30 
        ("clk_prepare_override" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DPHY_CLK_TIMING_PARAM_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPHY_CLK_TIMING_PARAM_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
