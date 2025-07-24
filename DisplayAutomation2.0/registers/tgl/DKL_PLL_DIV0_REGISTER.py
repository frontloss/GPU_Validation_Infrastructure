import ctypes

'''
Register instance and offset
'''

DKL_PLL_DIV0_D = 0x168200
DKL_PLL_DIV0_E = 0x169200
DKL_PLL_DIV0_F = 0x16A200
DKL_PLL_DIV0_G = 0x16B200
DKL_PLL_DIV0_H = 0x16C200
DKL_PLL_DIV0_I = 0x16D200

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_PLL_DIV0_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_fbdiv_intgr", ctypes.c_uint32, 8),  # 0 to 7
        ("i_fbprediv_3_0", ctypes.c_uint32, 4),  # 8 to 11
        ("i_prop_coeff_3_0", ctypes.c_uint32, 4),  # 12 to 15
        ("i_int_coeff_4_0", ctypes.c_uint32, 5),  # 16 to 20
        ("i_gainctrl_2_0", ctypes.c_uint32, 3),  # 21 to 23
        ("i_divretimeren", ctypes.c_uint32, 1),  # 24 to 24
        ("i_afc_startup_2_0", ctypes.c_uint32, 3),  # 25 to 27
        ("i_earlylock_criteria_1_0", ctypes.c_uint32, 2),  # 28 to 29
        ("i_truelock_criteria_1_0", ctypes.c_uint32, 2)  # 30 to 31
    ]

class DKL_PLL_DIV0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_PLL_DIV0_REG),
        ("asUint", ctypes.c_uint32)]