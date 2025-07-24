import ctypes

'''
Register instance and offset
'''
DKL_PLL_LF_D = 0x168208
DKL_PLL_LF_E = 0x169208
DKL_PLL_LF_F = 0x16A208
DKL_PLL_LF_G = 0x16B208
DKL_PLL_LF_H = 0x16C208
DKL_PLL_LF_I = 0x16D208

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_PLL_LF_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_bbthresh1_2_0", ctypes.c_uint32, 2),  # 0 to 1
        ("i_bbthresh1_2_0", ctypes.c_uint32, 3),  # 2 to 4
        ("i_bbthresh2_2_0", ctypes.c_uint32, 3),  # 5 to 7
        ("i_dcoampovrrden_h", ctypes.c_uint32, 1),  # 8 to 8
        ("i_dcoamp_3_0", ctypes.c_uint32, 4),  # 9 to 12
        ("i_bw_lowerbound_2_0", ctypes.c_uint32, 3),  # 13 to 15
        ("i_bw_upperbound_2_0", ctypes.c_uint32, 3),  # 16 to 18
        ("i_bw_mode_1_0", ctypes.c_uint32, 2),  # 19 to 20
        ("i_ft_mode_sel_2_0", ctypes.c_uint32, 3),  # 21 to 23
        ("i_bwphase_4_0", ctypes.c_uint32, 5),  # 24 to 28
        ("i_plllock_sel_1_0", ctypes.c_uint32, 2),  # 29 to 30
        ("i_afc_divratio", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DKL_PLL_LF_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_PLL_LF_REG),
        ("asUint", ctypes.c_uint32)]
