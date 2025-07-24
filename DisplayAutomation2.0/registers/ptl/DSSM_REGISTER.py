import ctypes

'''
Register instance and offset
'''
DSSM = 0x51004

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DSSM_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("genlock_disable", ctypes.c_uint32, 1),  # 0 to 0
        ("spare_1", ctypes.c_uint32, 1),  # 1 to 1
        ("spare_2", ctypes.c_uint32, 1),  # 2 to 2
        ("dmc_trap_disable", ctypes.c_uint32, 1),  # 3 to 3
        ("spare_3", ctypes.c_uint32, 1),  # 4 to 4
        ("spare_4", ctypes.c_uint32, 1),  # 5 to 5
        ("de_8k_dis", ctypes.c_uint32, 1),  # 6 to 6
        ("reserved_7", ctypes.c_uint32, 22),  # 7 to 28
        ("reference_frequency", ctypes.c_uint32, 3)  # 29 to 31
    ]


class DSSM_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSSM_REG),
        ("asUint", ctypes.c_uint32)]