import ctypes

'''
Register instance and offset
'''
DPCLKA_CFGCR1 = 0x1642BC

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DPCLKA_CFGCR1_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("ddij_mux_select", ctypes.c_uint32, 2),  # 0 to 1
        ("ddik_mux_select", ctypes.c_uint32, 2),  # 2 to 3
        ("ddij_clock_off", ctypes.c_uint32, 1),  # 4 to 4
        ("ddik_clock_off", ctypes.c_uint32, 1),  # 5 to 5
        ("reserved_6", ctypes.c_uint32, 10),  # 6 to 15
        ("fuse_freq_mon_status", ctypes.c_uint32, 12),  # 16 to 27
        ("reserved_28", ctypes.c_uint32, 4)  # 28 to 31
    ]


class DPCLKA_CFGCR1_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPCLKA_CFGCR1_REG),
        ("asUint", ctypes.c_uint32)]