import ctypes

'''
Register instance and offset
'''
DPLL0_ENABLE = 0x46010
DPLL1_ENABLE = 0x46014
DPLL4_ENABLE = 0x46018
TBT_PLL_ENABLE = 0x46020
MGPLL1_ENABLE = 0x46030
MGPLL2_ENABLE = 0x46034
MGPLL3_ENABLE = 0x46038
MGPLL4_ENABLE = 0x4603C
MGPLL5_ENABLE = 0x46040
MGPLL6_ENABLE = 0x46044
MGPLL7_ENABLE = 0x46048
MGPLL8_ENABLE = 0x4604C

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DPLL_ENABLE_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 26),  # 0 to 25
        ("power_state", ctypes.c_uint32, 1),  # 26 to 26
        ("power_enable", ctypes.c_uint32, 1),  # 27 to 27
        ("reserved_28", ctypes.c_uint32, 2),  # 28 to 29
        ("pll_lock", ctypes.c_uint32, 1),  # 30 to 30
        ("pll_enable", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DPLL_ENABLE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPLL_ENABLE_REG),
        ("asUint", ctypes.c_uint32)]