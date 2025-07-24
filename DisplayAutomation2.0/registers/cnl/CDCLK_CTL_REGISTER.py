import ctypes

'''
Register instance and offset
'''
CDCLK_CTL = 0x46000

'''
Register field expected values
'''
   
'''
Register bitfield defnition structure
'''


class CDCLK_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("cd_frequency_decimal", ctypes.c_uint32, 11),  # 0 to 10
        ("reserved_11", ctypes.c_uint32, 4),  # 11 to 14
        ("par0_cd_divmux_override", ctypes.c_uint32, 1),  # 15 to 15
        ("ssa_precharge_enable", ctypes.c_uint32, 1),  # 16 to 16
        ("reserved_17", ctypes.c_uint32, 1),  # 17 to 17
        ("par0_cd_source_override", ctypes.c_uint32, 1),  # 18 to 18
        ("divmux_cd_override", ctypes.c_uint32, 1),  # 19 to 19
        ("cd2x_pipe_select", ctypes.c_uint32, 2),  # 20 to 21
        ("cd2x_divider_select", ctypes.c_uint32, 2),  # 22 to 23
        ("reserved_24", ctypes.c_uint32, 8)  # 24 to 31
    ]


class CDCLK_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", CDCLK_CTL_REG),
        ("asUint", ctypes.c_uint32)]
