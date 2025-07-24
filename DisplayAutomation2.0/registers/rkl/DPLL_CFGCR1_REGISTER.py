import ctypes

'''
Register instance and offset
'''

DPLL0_CFGCR1 = 0x164288
DPLL1_CFGCR1 = 0x164290
TBTPLL_CFGCR1 = 0x1642A0
DPLL4_CFGCR1 = 0x164298

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DPLL_CFGCR1_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("central_frequency", ctypes.c_uint32, 2),  # 0 to 1
        ("pdiv", ctypes.c_uint32, 4),  # 2 to 5
        ("kdiv", ctypes.c_uint32, 3),  # 6 to 8
        ("qdiv", ctypes.c_uint32, 1),  # 9 to 9
        ("qdiv_ratio", ctypes.c_uint32, 8),  # 10 to 17
        ("reserved_18", ctypes.c_uint32, 14)  # 18 to 31
    ]


class DPLL_CFGCR1_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPLL_CFGCR1_REG),
        ("asUint", ctypes.c_uint32)]