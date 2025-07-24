import ctypes

'''
Register instance and offset
'''

DKL_PLL_FRAC_LOCK_L_NULL_D = 0x16820C
DKL_PLL_FRAC_LOCK_L_NULL_E = 0x16920C

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_PLL_FRAC_LOCK_L_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_feedfwrdgain", ctypes.c_uint32, 8),  # 0 to 7
        ("i_feedfwrdcal_en", ctypes.c_uint32, 1),  # 8 to 8
        ("i_feedfwrdcal_pause_hi", ctypes.c_uint32, 1),  # 9 to 9
        ("i_dcoditheren_h", ctypes.c_uint32, 1),  # 10 to 10
        ("i_lockthresh", ctypes.c_uint32, 4),  # 11 to 14
        ("i_dcodither_config", ctypes.c_uint32, 1),  # 15 to 15
        ("i_earlylock_criterion", ctypes.c_uint32, 2),  # 16 to 17
        ("i_truelock_criterion", ctypes.c_uint32, 2),  # 18 to 19
        ("i_lf_half_cyc_en", ctypes.c_uint32, 1),  # 20 to 20
        ("i_dither_ovrd", ctypes.c_uint32, 1),  # 21 to 21
        ("i_pllc_restore_reg", ctypes.c_uint32, 1),  # 22 to 22
        ("i_pllc_restore_mode_ctrl", ctypes.c_uint32, 1),  # 23 to 23
        ("i_pllrampen_h", ctypes.c_uint32, 1),  # 24 to 24
        ("i_fbdiv_strobe_h", ctypes.c_uint32, 1),  # 25 to 25
        ("i_ovc_snapshot_h", ctypes.c_uint32, 1),  # 26 to 26
        ("i_dither_value", ctypes.c_uint32, 1)  # 27 to 31
    ]


class DKL_PLL_FRAC_LOCK_L_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_PLL_FRAC_LOCK_L_REG),
        ("asUint", ctypes.c_uint32)]