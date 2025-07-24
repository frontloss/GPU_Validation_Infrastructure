import ctypes

'''
Register instance and offset
'''
DPLL0_CFGCR0 = 0x6C000
DPLL1_CFGCR0 = 0x6C080
DPLL2_CFGCR0 = 0x6C100

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DPLL_CFGCR0_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dco_integer ", ctypes.c_uint32, 10),  # 0 to 9
        ("dco_fraction", ctypes.c_uint32, 15),  # 10 to 24
        ("dp_link_rate", ctypes.c_uint32, 4),  # 25 to 28
        ("ssc_enable  ", ctypes.c_uint32, 1),  # 29 to 29
        ("hdmi_mode   ", ctypes.c_uint32, 1),  # 10 to 30
        ("reserved_31 ", ctypes.c_uint32, 1),  # 31 to 31
    ]


class DPLL_CFGCR0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPLL_CFGCR0_REG),
        ("asUint", ctypes.c_uint32)]

