import ctypes

'''
Register instance and offset
'''
#TODO: Need to check as in bspec DPLL2 and DPLL4 have same offset
DPLL0_ENABLE = 0x46010
DPLL1_ENABLE = 0x46014
# Reference: https://gfxspecs.intel.com/Predator/Home/Index/53723
# Due to current BSpec filtering limitations, the DPLL4_CRCFG0/1 (164294h/164298h) are used to control the DPLL2.
DPLL4_ENABLE = 0x46018
DPLL3_ENABLE = 0x46030
MGPLL2_ENABLE = 0x46034

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
        ("reserved_28", ctypes.c_uint32, 1),  # 28 to 28
        ("pll_refclk_select", ctypes.c_uint32, 1),  # 29 to 29
        ("pll_lock", ctypes.c_uint32, 1),  # 30 to 30
        ("pll_enable", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DPLL_ENABLE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPLL_ENABLE_REG),
        ("asUint", ctypes.c_uint32)]