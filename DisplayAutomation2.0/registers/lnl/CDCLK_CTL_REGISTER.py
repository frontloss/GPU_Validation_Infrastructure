import ctypes
 
'''
Register instance and offset 
'''
CDCLK_CTL = 0x46000

 
'''
Register field expected values 
'''
cd2x_divider_select_DIVIDE_BY_1 = 0b00 
cd2x_divider_select_DIVIDE_BY_1_5 = 0b01 
cd2x_divider_select_DIVIDE_BY_2 = 0b10 
cd2x_divider_select_DIVIDE_BY_4 = 0b11 
cd2x_pipe_select_NONE = 0b111 
cd2x_pipe_select_PIPE_A = 0b000 
cd2x_pipe_select_PIPE_B = 0b010 
cd2x_pipe_select_PIPE_C = 0b100 
cd2x_pipe_select_PIPE_D = 0b110
override_to_crystal_NORMAL = 0b0 
override_to_crystal_OVERRIDE = 0b1 
override_to_slow_clock_NORMAL = 0b0 
override_to_slow_clock_OVERRIDE = 0b1 
par0_cd_divmux_override_NORMAL = 0b0 
par0_cd_divmux_override_OVERRIDE_TO_DIVMUX = 0b1 
ssa_precharge_enable_DISABLE = 0b0 
md_clk_source_select_cd2xclk = 0b0
md_clk_source_select_cdclk_pll = 0b1
 
'''
Register bitfield defnition structure 
'''
class CDCLK_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"              , ctypes.c_uint32, 11), # 10 to 0
        ("par0_cd_divmux_override" , ctypes.c_uint32, 5), # 11 to 15
        ("ssa_precharge_enable"   , ctypes.c_uint32, 1), # 16 to 16 
        ("override_to_crystal"    , ctypes.c_uint32, 1), # 17 to 17 
        ("override_to_slow_clock" , ctypes.c_uint32, 1), # 18 to 18 
        ("cd2x_pipe_select"       , ctypes.c_uint32, 3), # 21 to 19 
        ("cd2x_divider_select"    , ctypes.c_uint32, 2), # 23 to 22
        ("reserved_24"            , ctypes.c_uint32, 1), # 24 to 24
        ("md_clk_source_select"   , ctypes.c_uint32, 1), # 25 to 25
        ("reserved_24"            , ctypes.c_uint32, 6), # 26 to 31
    ]

 
class CDCLK_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CDCLK_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
