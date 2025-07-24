import ctypes

'''
Register instance and offset
'''
DE_PLL_ENABLE = 0x46070

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DE_PLL_ENABLE_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 30),  # 0 to 29
        ("pll_lock", ctypes.c_uint32, 1),  # 30 to 30
        ("pll_enable", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DE_PLL_ENABLE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DE_PLL_ENABLE_REG),
        ("asUint", ctypes.c_uint32)]