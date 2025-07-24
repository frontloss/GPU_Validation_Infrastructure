import ctypes

'''
Register instance and offset
'''

DKL_PLL_LF_L_NULL_D = 0x168208
DKL_PLL_LF_L_NULL_E = 0x169208

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_PLL_LF_L_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_prop_coeff", ctypes.c_uint32, 4),  # 0 to 3
        ("i_fll_int_coeff", ctypes.c_uint32, 4),  # 4 to 7
        (" i_int_coeff", ctypes.c_uint32, 5),  # 8 to 12
        ("i_fll_en_h", ctypes.c_uint32, 1),  # 13 to 13
        ("i_tdc_fine_res", ctypes.c_uint32, 1),  # 14 to 14
        ("i_dcofine_resolution", ctypes.c_uint32, 1),  # 15 to 15
        ("i_gainctrl", ctypes.c_uint32, 3),  # 16 to 18
        ("i_afc_divratio", ctypes.c_uint32, 1),  # 19 to 19
        ("i_afccntsel", ctypes.c_uint32, 1),  # 20 to 20
        ("i_afc_startup", ctypes.c_uint32, 2),  # 21 to 22
        ("reserved_23", ctypes.c_uint32, 1),  # 23 to 23
        ("i_tdctargetcnt", ctypes.c_uint32, 8)  # 24 to 31
    ]


class DKL_PLL_LF_L_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_PLL_LF_L_REG),
        ("asUint", ctypes.c_uint32)]