import ctypes

'''
Register instance and offset
'''

DKL_CLKTOP2_CORECLKCTL1_NULL_D = 0x1680D8
DKL_CLKTOP2_CORECLKCTL1_NULL_E = 0x1690D8

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_CLKTOP2_CORECLKCTL1_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 1),  # 0 to 0
        ("od_clktop2_coreclka_divretimeren_h", ctypes.c_uint32, 1),  # 1 to 1
        ("od_clktop2_coreclka_bypass", ctypes.c_uint32, 1),  # 2 to 2
        ("reserved_3", ctypes.c_uint32, 1),  # 3 to 3
        ("od_clktop2_coreclkb_divretimeren_h", ctypes.c_uint32, 1),  # 4 to 4
        ("od_clktop2_coreclkb_bypass", ctypes.c_uint32, 1),  # 5 to 5
        ("reserved_6", ctypes.c_uint32, 2),  # 6 to 7
        ("od_clktop2_coreclka_divratio", ctypes.c_uint32, 8),  # 8 to 15
        ("od_clktop2_coreclkb_divratio", ctypes.c_uint32, 8),  # 16 to 23
        ("reserved_24", ctypes.c_uint32, 1),  # 24 to 24
        ("od_clktop2_coreclkc_divretimeren_h", ctypes.c_uint32, 1),  # 25 to 25
        ("od_clktop2_coreclkc_bypass", ctypes.c_uint32, 1),  # 26 to 26
        ("reserved_27", ctypes.c_uint32, 1),  # 27 to 27
        ("od_clktop2_coreclkd_divretimeren_h", ctypes.c_uint32, 1),  # 28 to 28
        ("od_clktop2_coreclkd_bypass", ctypes.c_uint32, 1),  # 29 to 29
        ("reserved_30", ctypes.c_uint32, 2)  # 30 to 31
    ]


class DKL_CLKTOP2_CORECLKCTL1_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_CLKTOP2_CORECLKCTL1_REG),
        ("asUint", ctypes.c_uint32)]