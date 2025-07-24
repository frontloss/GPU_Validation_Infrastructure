import ctypes

'''
Register instance and offset
'''
MG_PLL1_LF_PORT1 = 0x168A08
MG_PLL1_LF_PORT2 = 0x169A08
MG_PLL1_LF_PORT3 = 0x16AA08
MG_PLL1_LF_PORT4 = 0x16BA08

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class MG_PLL_LF_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_prop_coeff", ctypes.c_uint32, 4),  # 0 to 3
        ("i_fll_int_coeff", ctypes.c_uint32, 4),  # 4 to 7
        ("i_int_coeff", ctypes.c_uint32, 5),  # 8 to 12
        ("i_fll_en_h", ctypes.c_uint32, 1),  # 13 to 13
        ("i_tdc_fine_res", ctypes.c_uint32, 1),  # 14 to 14
        ("reserved_15", ctypes.c_uint32, 1),  # 15 to 15
        ("i_gainctrl", ctypes.c_uint32, 3),  # 16 to 18
        ("i_afc_divratio", ctypes.c_uint32, 1),  # 19 to 19
        ("i_afccntsel", ctypes.c_uint32, 1),  # 20 to 20
        ("i_afc_startup", ctypes.c_uint32, 2),  # 21 to 22
        ("i_dcofine_resolution", ctypes.c_uint32, 1),  # 23 to 23
        ("i_tdctargetcnt", ctypes.c_uint32, 9)  # 23 to 31
    ]


class MG_PLL_LF_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MG_PLL_LF_REG),
        ("asUint", ctypes.c_uint32)]