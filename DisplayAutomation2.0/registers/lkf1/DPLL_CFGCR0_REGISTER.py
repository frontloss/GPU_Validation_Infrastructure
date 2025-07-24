import ctypes

'''
Register instance and offset
'''

DPLL0_CFGCR0 = 0x164000
DPLL1_CFGCR0 = 0x164080
TBTPLL_CFGCR0 = 0x164100
DPLL4_CFGCR0 = 0x164200

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DPLL_CFGCR0_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dco_integer", ctypes.c_uint32, 10),  # 0 to 9
        ("dco_fraction", ctypes.c_uint32, 15),  # 10 to 24
        ("ssc_enable", ctypes.c_uint32, 1),  # 25 to 25
        ("reserved_26", ctypes.c_uint32, 6)  # 26 to 31
    ]


class DPLL_CFGCR0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPLL_CFGCR0_REG),
        ("asUint", ctypes.c_uint32)]