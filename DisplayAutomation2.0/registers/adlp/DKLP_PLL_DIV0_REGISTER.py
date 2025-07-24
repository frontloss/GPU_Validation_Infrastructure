import ctypes

'''
Register instance and offset
'''
DKLP_PLL0_DIV0_TC1 = 0x168180
DKLP_PLL0_DIV0_TC2 = 0x169180
DKLP_PLL0_DIV0_TC3 = 0x16A180
DKLP_PLL0_DIV0_TC4 = 0x16B180

DKLP_PLL1_DIV0_TC1 = 0x168200
DKLP_PLL1_DIV0_TC2 = 0x169200
DKLP_PLL1_DIV0_TC3 = 0x16A200
DKLP_PLL1_DIV0_TC4 = 0x16B200

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_PLL_DIV0_REG(ctypes.LittleEndianStructure):
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

class DKLP_PLL_DIV0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_PLL_DIV0_REG),
        ("asUint", ctypes.c_uint32)]