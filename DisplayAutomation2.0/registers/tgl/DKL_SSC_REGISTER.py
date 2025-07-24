import ctypes

'''
Register instance and offset
'''

DKL_SSC_NULL_D = 0x168210
DKL_SSC_NULL_E = 0x169210
DKL_SSC_NULL_F = 0x16A210
DKL_SSC_NULL_G = 0x16B210
DKL_SSC_NULL_H = 0x16C210
DKL_SSC_NULL_I = 0x16D210

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_SSC_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_init_dcoamp_5_0", ctypes.c_uint32, 6),  # 0 to 5
        ("i_bias_gb_sel_1_0", ctypes.c_uint32, 2),  # 6 to 7
        ("i_sscfllen_h", ctypes.c_uint32, 1),  # 8 to 8
        ("i_sscen_h", ctypes.c_uint32, 1),  # 9 to 9
        ("i_ssc_openloop_en_h", ctypes.c_uint32, 1),  # 10 to 10
        ("i_sscstepnum_2_0", ctypes.c_uint32, 3),  # 11 to 13
        ("i_sscfll_update_sel_1_0", ctypes.c_uint32, 2),  # 14 to 15
        ("i_sscsteplength_7_0", ctypes.c_uint32, 8),  # 16 to 23
        ("i_sscinj_en_h", ctypes.c_uint32, 1),  # 24 to 24
        ("i_sscinj_adapt_en_h", ctypes.c_uint32, 1),  # 25 to 25
        ("ssc_stepnum_offset_2_0", ctypes.c_uint32, 3),  # 26 to 28
        ("i_iref_ndivratio_2_0", ctypes.c_uint32, 3)  # 29 to 31
    ]


class DKL_SSC_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_SSC_REG),
        ("asUint", ctypes.c_uint32)]