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
cd_frequency_decimal_168_MHZ_CD = 0b00101001110 
cd_frequency_decimal_172_8_MHZ_CD = 0b00101011000 
cd_frequency_decimal_180_MHZ_CD = 0b00101100110 
cd_frequency_decimal_192_MHZ_CD = 0b00101111110 
cd_frequency_decimal_307_2_MHZ_CD = 0b01001100100 
cd_frequency_decimal_312_MHZ_CD = 0b01001101110 
cd_frequency_decimal_552_MHZ_CD = 0b10001001110 
cd_frequency_decimal_556_8_MHZ_CD = 0b10001011000 
cd_frequency_decimal_648_MHZ_CD = 0b10100001110 
cd_frequency_decimal_652_8_MHZ_CD = 0b10100011000 
override_to_crystal_NORMAL = 0b0 
override_to_crystal_OVERRIDE = 0b1 
override_to_slow_clock_NORMAL = 0b0 
override_to_slow_clock_OVERRIDE = 0b1 
par0_cd_divmux_override_NORMAL = 0b0 
par0_cd_divmux_override_OVERRIDE_TO_DIVMUX = 0b1 
ssa_precharge_enable_DISABLE = 0b0 

 
'''
Register bitfield defnition structure 
'''
class CDCLK_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("cd_frequency_decimal"   , ctypes.c_uint32, 11), # 10 to 0 
        ("par0_cd_divmux_override" , ctypes.c_uint32, 1), # 15 to 15 
        ("ssa_precharge_enable"   , ctypes.c_uint32, 1), # 16 to 16 
        ("override_to_crystal"    , ctypes.c_uint32, 1), # 17 to 17 
        ("override_to_slow_clock" , ctypes.c_uint32, 1), # 18 to 18 
        ("cd2x_pipe_select"       , ctypes.c_uint32, 3), # 21 to 19 
        ("cd2x_divider_select"    , ctypes.c_uint32, 2), # 23 to 22 
    ]

 
class CDCLK_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CDCLK_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
