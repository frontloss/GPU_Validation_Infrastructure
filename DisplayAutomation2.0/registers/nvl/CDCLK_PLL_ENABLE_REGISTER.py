import ctypes

'''
Register instance and offset
'''
CDCLK_PLL_ENABLE = 0x46070

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class CDCLK_PLL_ENABLE_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("pll_ratio", ctypes.c_uint32, 8),  # 0 to 7
        ("reserved_8", ctypes.c_uint32, 18),  # 8 to 25
        ("slow_clock_lock", ctypes.c_uint32, 1),  # 26 to 26
        ("slow_clock_enable", ctypes.c_uint32, 1),  # 27 to 27
        ("reserved_28", ctypes.c_uint32, 2),  # 28 to 29
        ("pll_lock", ctypes.c_uint32, 1),  # 30 to 30
        ("pll_enable", ctypes.c_uint32, 1)  # 31 to 31
    ]


class CDCLK_PLL_ENABLE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", CDCLK_PLL_ENABLE_REG),
        ("asUint", ctypes.c_uint32)]