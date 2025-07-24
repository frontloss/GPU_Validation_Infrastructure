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
        ("ddia_mux_select", ctypes.c_uint32, 2),  # 0 to 1
        ("ddib_mux_select", ctypes.c_uint32, 2),  # 2 to 3
        ("ddii_mux_select", ctypes.c_uint32, 2),  # 4 to 5
        ("mipia_hvm_sel", ctypes.c_uint32, 2),  # 6 to 7
        ("mipic_hvm_select", ctypes.c_uint32, 2),  # 8 to 9
        ("ddia_clock_off", ctypes.c_uint32, 1),  # 10 to 10
        ("ddib_clock_off", ctypes.c_uint32, 1),  # 11 to 11
        ("ddic_clock_off", ctypes.c_uint32, 1),  # 12 to 12
        ("ddid_clock_off", ctypes.c_uint32, 1),  # 13 to 13
        ("ddie_clock_off", ctypes.c_uint32, 1),  # 14 to 14
        ("dpll0_inverse_ref", ctypes.c_uint32, 1),  # 15 to 15
        ("dpll1_inverse_ref", ctypes.c_uint32, 1),  # 16 to 16
        ("dpll2_inverse_ref", ctypes.c_uint32, 1),  # 17 to 17
        ("dpll0_enable_override", ctypes.c_uint32, 1),  # 18 to 18
        ("dpll1_enable_override", ctypes.c_uint32, 1),  # 19 to 19
        ("dpll2_enable_override", ctypes.c_uint32, 1),  # 20 to 20
        ("ddif_clock_off", ctypes.c_uint32, 1),  # 21 to 21
        ("ddig_clock_off", ctypes.c_uint32, 1),  # 22 to 22
        ("ddih_clock_off", ctypes.c_uint32, 1),  # 23 to 23
        ("ddii_clock_off", ctypes.c_uint32, 1),  # 24 to 24
        ("dpll3_inverse_ref", ctypes.c_uint32, 1),  # 25 to 25
        ("dpll4_inverse_ref", ctypes.c_uint32, 1),  # 26 to 26
        ("dpll3_enable_override", ctypes.c_uint32, 1),  # 27 to 27
        ("tc_genlock_ref_select", ctypes.c_uint32, 1),  # 28 to 28
        ("hvm_independent_mipi_enable", ctypes.c_uint32, 1),  # 29 to 29
        ("iref_inverse_ref", ctypes.c_uint32, 1),  # 30 to 30
        ("reserved_31", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DPCLKA_CFGCR0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPCLKA_CFGCR0_REG),
        ("asUint", ctypes.c_uint32)]