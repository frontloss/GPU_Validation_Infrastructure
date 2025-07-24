import ctypes

'''
Register instance and offset
'''
DPCLKA1_CFGCR0 = 0x16C280

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DPCLKA1_CFGCR0_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("ddic_clock_select", ctypes.c_uint32, 2),  # 0 to 1
        ("ddid_clock_select", ctypes.c_uint32, 2),  # 2 to 3
        ("reserved_4", ctypes.c_uint32, 6),  # 4 to 9
        ("ddic_clock_off", ctypes.c_uint32, 1),  # 10 to 10
        ("ddid_clock_off", ctypes.c_uint32, 1),  # 11 to 11
        ("reserved_12", ctypes.c_uint32, 3),  # 12 to 14
        ("dpll2_inverse_ref", ctypes.c_uint32, 1),  # 15 to 15
        ("dpll3_inverse_ref", ctypes.c_uint32, 1),  # 16 to 16
        ("reserved_17", ctypes.c_uint32, 1),  # 17 to 17
        ("dpll2_enable_override", ctypes.c_uint32, 1),  # 18 to 18
        ("dpll3_enable_override", ctypes.c_uint32, 1),  # 19 to 19
        ("reserved_21", ctypes.c_uint32, 12)  # 20 to 31
    ]

class DPCLKA1_CFGCR0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPCLKA1_CFGCR0_REG),
        ("asUint", ctypes.c_uint32)]