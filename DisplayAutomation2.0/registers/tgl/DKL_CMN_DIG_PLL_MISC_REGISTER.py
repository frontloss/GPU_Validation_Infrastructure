import ctypes

'''
Register instance and offset
'''
DKL_CMN_DIG_PLL_MISC_D = 0x16803C
DKL_CMN_DIG_PLL_MISC_E = 0x16903C
DKL_CMN_DIG_PLL_MISC_F = 0x16A03C
DKL_CMN_DIG_PLL_MISC_G = 0x16B03C
DKL_CMN_DIG_PLL_MISC_H = 0x16C03C
DKL_CMN_DIG_PLL_MISC_I = 0x16D03C

'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class DKL_CMN_DIG_PLL_MISC_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("od_cri_pll2_pcie_enable", ctypes.c_uint32, 1),  # 0 to 0
        ("Reserved", ctypes.c_uint32, 15),  # 1 to 15
        ("od_cri_cascaded_pll1_enable", ctypes.c_uint32, 1),  # 16 to 16
        ("od_cri_cascaded_pll2_enable", ctypes.c_uint32, 1),  # 17 to 17
        ("Reserved", ctypes.c_uint32, 14)  # 18 to 31
    ]


class DKL_CMN_DIG_PLL_MISC_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_CMN_DIG_PLL_MISC_REG),
        ("asUint", ctypes.c_uint32)]
