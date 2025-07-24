import ctypes

'''
Register instance and offset
'''
DKL_PLL_FRAC_LOCK_D = 0x16820C
DKL_PLL_FRAC_LOCK_E = 0x16920C
DKL_PLL_FRAC_LOCK_F = 0x16A20C
DKL_PLL_FRAC_LOCK_G = 0x16B20C
DKL_PLL_FRAC_LOCK_H = 0x16C20C
DKL_PLL_FRAC_LOCK_I = 0x16D20C

'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class DKL_PLL_FRAC_LOCK_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_init_cselafc_7_0", ctypes.c_uint32, 8),  # 0 to 7
        ("i_max_cselafc_7_0", ctypes.c_uint32, 8),  # 8 to 15
        ("i_fllafc_lockcnt_2_0", ctypes.c_uint32, 3),  # 16 to 18
        ("i_fllafc_gain_3_0", ctypes.c_uint32, 4),  # 19 to 22
        ("i_fastlock_en_h", ctypes.c_uint32, 1),  # 23 to 23
        ("i_bb_gain1_2_0", ctypes.c_uint32, 3),  # 24 to 26
        ("i_bb_gain2_2_0", ctypes.c_uint32, 3),  # 27 to 29
        ("i_cml2cmosbonus_1_0", ctypes.c_uint32, 2)  # 30 to 31
    ]


class DKL_PLL_FRAC_LOCK_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_PLL_FRAC_LOCK_REG),
        ("asUint", ctypes.c_uint32)]
