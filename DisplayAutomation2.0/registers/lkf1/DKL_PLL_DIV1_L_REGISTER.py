import ctypes

'''
Register instance and offset
'''

DKL_PLL_DIV1_L_NULL_D = 0x168204
DKL_PLL_DIV1_L_NULL_E = 0x169204

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_PLL_DIV1_L_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_fbprediv", ctypes.c_uint32, 4),  # 0 to 3
        ("i_fbprediv", ctypes.c_uint32, 4),  # 4 to 7
        ("i_dutycyccorr_en_h", ctypes.c_uint32, 1),  # 8 to 8
        ("i_pllc_reg_fbclkext_sel", ctypes.c_uint32, 1),  # 9 to 9
        ("i_pllc_reg_longloopclk_sel", ctypes.c_uint32, 1),  # 10 to 10
        ("i_divretimer_en", ctypes.c_uint32, 1),  # 11 to 11
        ("i_dither_div", ctypes.c_uint32, 2),  # 12 to 13
        ("i_m1_longloop_sel", ctypes.c_uint32, 1),  # 14 to 14
        ("reserved_15", ctypes.c_uint32, 1),  # 15 to 15
        ("i_bonus_iref_ndivratio", ctypes.c_uint32, 3),  # 16 to 18
        ("reserved_19", ctypes.c_uint32, 5),  # 19 to 23
        ("i_rodiv_sel", ctypes.c_uint32, 4),  # 24 to 27
        ("i_dfx_div_clko", ctypes.c_uint32, 2),  # 28 to 29
        ("reserved_30", ctypes.c_uint32, 2),  # 30 to 31
    ]


class DKL_PLL_DIV1_L_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_PLL_DIV1_L_REG),
        ("asUint", ctypes.c_uint32)]