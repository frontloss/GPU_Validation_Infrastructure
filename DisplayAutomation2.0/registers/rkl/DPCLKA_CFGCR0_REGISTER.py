import ctypes

'''
Register instance and offset
'''
DPCLKA_CFGCR0 = 0x164280

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DPCLKA_CFGCR0_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("ddia_clock_select", ctypes.c_uint32, 2),  # 0 to 1
        ("ddib_clock_select", ctypes.c_uint32, 2),  # 2 to 3
        ("ddic_clock_select", ctypes.c_uint32, 2),  # 4 to 5
        ("reserved_6", ctypes.c_uint32, 4),  # 6 to 9
        ("ddia_clock_off", ctypes.c_uint32, 1),  # 10 to 10
        ("ddib_clock_off", ctypes.c_uint32, 1),  # 11 to 11
        ("ddic_clock_off", ctypes.c_uint32, 1),  # 12 to 12
        ("ddid_clock_off", ctypes.c_uint32, 1),  # 13 to 13
        ("reserved_14", ctypes.c_uint32, 1),  # 14 to 14
        ("dpll0_inverse_ref", ctypes.c_uint32, 1),  # 15 to 15
        ("dpll1_inverse_ref", ctypes.c_uint32, 1),  # 16 to 16
        ("dpll4_inverse_ref", ctypes.c_uint32, 1),  # 17 to 17
        ("dpll0_enable_override", ctypes.c_uint32, 1),  # 18 to 18
        ("dpll1_enable_override", ctypes.c_uint32, 1),  # 19 to 19
        ("dpll4_enable_override", ctypes.c_uint32, 1),  # 20 to 20
        ("reserved_21", ctypes.c_uint32, 7),  # 21 to 27
        ("ddid_clock_select", ctypes.c_uint32, 2),  # 28 to 29
        ("iref_inverse_ref", ctypes.c_uint32, 1),  # 30 to 30
        ("reserved_31", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DPCLKA_CFGCR0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPCLKA_CFGCR0_REG),
        ("asUint", ctypes.c_uint32)]