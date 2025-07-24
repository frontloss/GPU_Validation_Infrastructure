import ctypes

'''
Register instance and offset
'''
MG_PLL1_DIV1_PORT1 = 0x168A04
MG_PLL1_DIV1_PORT2 = 0x169A04
MG_PLL1_DIV1_PORT3 = 0x16AA04
MG_PLL1_DIV1_PORT4 = 0x16BA04

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class MG_PLL_DIV1_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_fbprediv", ctypes.c_uint32, 4),  # 0 to 3
        ("i_ndivratio", ctypes.c_uint32, 4),  # 4 to 7
        ("i_dutycyccorr_en_h", ctypes.c_uint32, 1),  # 8 to 8
        ("i_plllc_reg_fbclkext_sel", ctypes.c_uint32, 1),  # 9 to 9
        ("i_plllc_reg_longloopclk_sel", ctypes.c_uint32, 1),  # 10 to 10
        ("i_divretimeren", ctypes.c_uint32, 1),  # 11 to 11
        ("i_dither_div", ctypes.c_uint32, 2),  # 12 to 13
        ("reserved_14", ctypes.c_uint32, 2),  # 14 to 15
        ("i_iref_ndivratio", ctypes.c_uint32, 3),  # 16 to 18
        ("reserved_19", ctypes.c_uint32, 5),  # 19 to 23
        ("i_rodiv_sel", ctypes.c_uint32, 4),  # 24 to 27
        ("i_dfx_div_cklo", ctypes.c_uint32, 2),  # 28 to 29
        ("i_dfx_div_ckhi", ctypes.c_uint32, 2)  # 30 to 31
    ]


class MG_PLL_DIV1_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MG_PLL_DIV1_REG),
        ("asUint", ctypes.c_uint32)]