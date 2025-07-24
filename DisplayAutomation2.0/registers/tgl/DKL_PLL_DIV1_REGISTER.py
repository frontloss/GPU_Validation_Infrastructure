import ctypes

'''
Register instance and offset
'''

DKL_PLL_DIV1_D = 0x168204
DKL_PLL_DIV1_E = 0x169204
DKL_PLL_DIV1_F = 0x16A204
DKL_PLL_DIV1_G = 0x16B204
DKL_PLL_DIV1_H = 0x16C204
DKL_PLL_DIV1_I = 0x16D204

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_PLL_DIV1_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_tdctargetcnt_7_0", ctypes.c_uint32, 8),  # 0 to 7
        ("i_lockthresh_3_0", ctypes.c_uint32, 4),  # 8 to 11
        ("i_dcodither_config", ctypes.c_uint32, 1),  # 12 to 12
        ("i_biascal_en_h", ctypes.c_uint32, 1),  # 13 to 13
        ("i_bias_filter_en", ctypes.c_uint32, 1),  # 14 to 14
        ("i_biasfilter_en_delay", ctypes.c_uint32, 1),  # 15 to 15
        ("i_ireftrim_4_0", ctypes.c_uint32, 5),  # 16 to 20
        ("i_bias_r_programmability", ctypes.c_uint32, 2),  # 21 to 22
        ("i_fastlock_internal_reset", ctypes.c_uint32, 1),  # 23 to 23
        ("i_ctrim_4_0", ctypes.c_uint32, 5),  # 24 to 28
        ("i_bias_calib_stepsize_1_0", ctypes.c_uint32, 2),  # 29 to 30
        ("i_bw_ampmeas_window", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DKL_PLL_DIV1_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_PLL_DIV1_REG),
        ("asUint", ctypes.c_uint32)]