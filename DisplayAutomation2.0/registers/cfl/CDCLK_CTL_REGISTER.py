import ctypes
 
'''
Register instance and offset 
'''
CDCLK_CTL = 0x46000 

 
'''
Register field expected values 
'''
cd2x_divider_select_DIVIDE_BY_1 = 0b00 
cd2x_divider_select_DIVIDE_BY_2 = 0b10 
cd2x_pipe_select_NONE = 0b111 
cd2x_pipe_select_PIPE_A = 0b000 
cd2x_pipe_select_PIPE_B = 0b010 
cd2x_pipe_select_PIPE_C = 0b100 
cd2x_pipe_select_PIPE_D = 0b110 
cd2x_source_DPLL0 = 0b0 
cd2x_source_DPLL1 = 0b1 
cd_frequency_decimal_144_MHZ_CD = 0b00100011110 
cd_frequency_decimal_158_4_MHZ_CD = 0b00100111011 
cd_frequency_decimal_168_MHZ_CD = 0b00101001110 
cd_frequency_decimal_288_MHZ_CD = 0b01000111110 
cd_frequency_decimal_308_57_MHZ_CD = 0b01001100111 
cd_frequency_decimal_316_8_MHZ_CD = 0b01001111000 
cd_frequency_decimal_336_MHZ_CD = 0b01010011110 
cd_frequency_decimal_337_5_MHZ_CD = 0b01010100001 
cd_frequency_decimal_384_MHZ_CD = 0b01011111110 
cd_frequency_decimal_432_MHZ_CD = 0b01101011110 
cd_frequency_decimal_450_MHZ_CD = 0b01110000010 
cd_frequency_decimal_528_MHZ_CD = 0b10000011110 
cd_frequency_decimal_540_MHZ_CD = 0b10000110110 
cd_frequency_decimal_576_MHZ_CD = 0b10001111110 
cd_frequency_decimal_617_14_MHZ_CD = 0b10011010000 
cd_frequency_decimal_624_MHZ_CD = 0b10011011110 
cd_frequency_decimal_675_MHZ_CD = 0b10101000100 
cd_frequency_select_337_5_OR_308_57_MHZ = 0b10 
cd_frequency_select_450_OR_432_MHZ = 0b00 
cd_frequency_select_540_MHZ = 0b01 
cd_frequency_select_675_OR_617_14_MHZ = 0b11 
de_cd2x_divider_select_DIVIDE_BY_1 = 0b00 
de_cd2x_divider_select_DIVIDE_BY_1_5 = 0b01 
de_cd2x_divider_select_DIVIDE_BY_2 = 0b10 
de_cd2x_divider_select_DIVIDE_BY_4 = 0b11 
de_cd2x_pipe_select_NONE = 0b11 
de_cd2x_pipe_select_PIPE_A = 0b00 
de_cd2x_pipe_select_PIPE_B = 0b01 
de_cd2x_pipe_select_PIPE_C = 0b10 
divmux_cd_override_NORMAL = 0b0 
divmux_cd_override_OVERRIDE_TO_NON_SPREAD = 0b1 
par0_cd_divmux_override_NORMAL = 0b0 
par0_cd_divmux_override_OVERRIDE_TO_DIVMUX = 0b1 
par0_cd_source_override_NORMAL = 0b0 
par0_cd_source_override_OVERRIDE_TO_NON_SPREAD = 0b1 
ssa_precharge_enable_DISABLE = 0b0 
ssa_precharge_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class CDCLK_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("cd_frequency_decimal"   , ctypes.c_uint32, 11), # 0 to 10 
        ("reserved_11"            , ctypes.c_uint32, 4), # 11 to 14 
        ("par0_cd_divmux_override" , ctypes.c_uint32, 1), # 15 to 15 
        ("ssa_precharge_enable"   , ctypes.c_uint32, 1), # 16 to 16 
        ("cd2x_source"            , ctypes.c_uint32, 1), # 17 to 17 
        ("divmux_cd_override"     , ctypes.c_uint32, 1), # 17 to 17 
        ("reserved_17"            , ctypes.c_uint32, 1), # 17 to 17 
        ("par0_cd_source_override" , ctypes.c_uint32, 1), # 18 to 18 
        ("cd2x_pipe_select"       , ctypes.c_uint32, 3), # 19 to 21 
        ("de_cd2x_pipe_select"    , ctypes.c_uint32, 2), # 20 to 21 
        ("reserved_20"            , ctypes.c_uint32, 6), # 20 to 25 
        ("cd2x_divider_select"    , ctypes.c_uint32, 2), # 22 to 23 
        ("de_cd2x_divider_select" , ctypes.c_uint32, 2), # 22 to 23 
        ("reserved_24"            , ctypes.c_uint32, 8), # 24 to 31 
        ("cd_frequency_select"    , ctypes.c_uint32, 2), # 26 to 27 
        ("reserved_28"            , ctypes.c_uint32, 4), # 28 to 31 
    ]

 
class CDCLK_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CDCLK_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
