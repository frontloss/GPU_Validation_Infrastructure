import ctypes

'''
Register instance and offset
'''

DKLP_PLL0_BIAS_TC1 = 0x168194
DKLP_PLL0_BIAS_TC2 = 0x169194
DKLP_PLL0_BIAS_TC3 = 0x16A194
DKLP_PLL0_BIAS_TC4 = 0x16B194

DKLP_PLL1_BIAS_TC1 = 0x168214
DKLP_PLL1_BIAS_TC2 = 0x169214
DKLP_PLL1_BIAS_TC3 = 0x16A214
DKLP_PLL1_BIAS_TC4 = 0x16B214

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_PLL_BIAS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_sscinj_stepsize_7_0", ctypes.c_uint32, 8),  # 0 to 7
        ("i_fbdiv_frac_7_0", ctypes.c_uint32, 8),  # 8 to 15
        ("i_fbdiv_frac_15_8", ctypes.c_uint32, 8),  # 16 to 23
        ("i_fbdiv_frac_21_16", ctypes.c_uint32, 6),  # 24 to 29
        ("i_fracnen_h", ctypes.c_uint32, 1),  # 30 to 30
        ("i_tdc_fine_res", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DKLP_PLL_BIAS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_PLL_BIAS_REG),
        ("asUint", ctypes.c_uint32)]