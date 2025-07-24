import ctypes

'''
Register instance and offset
'''
MG_PLL1_FRAC_LOCK_PORT1 = 0x168A0C
MG_PLL1_FRAC_LOCK_PORT2 = 0x169A0C
MG_PLL1_FRAC_LOCK_PORT3 = 0x16AA0C
MG_PLL1_FRAC_LOCK_PORT4 = 0x16BA0C

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class MG_PLL_FRAC_LOCK_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_feedfwrdgain", ctypes.c_uint32, 8),  # 0 to 7
        ("i_feedfwrdcal_en_h", ctypes.c_uint32, 1),  # 8 to 8
        ("i_feedfwrdcal_pause_h", ctypes.c_uint32, 1),  # 9 to 9
        ("i_dcoditheren_h", ctypes.c_uint32, 1),  # 10 to 10
        ("i_lockthresh", ctypes.c_uint32, 4),  # 11 to 14
        ("i_dcodither_config", ctypes.c_uint32, 1),  # 15 to 15
        ("i_earlylock_criteria", ctypes.c_uint32, 2),  # 16 to 17
        ("i_truelock_criteria", ctypes.c_uint32, 2),  # 18 to 19
        ("i_lf_half_cyc_en", ctypes.c_uint32, 1),  # 20 to 20
        ("i_dither_ovrd", ctypes.c_uint32, 1),  # 21 to 21
        ("i_plllc_restore_reg", ctypes.c_uint32, 1),  # 22 to 22
        ("i_plllc_restore_mode_ctrl", ctypes.c_uint32, 1),  # 23 to 23
        ("i_pllrampen_h", ctypes.c_uint32, 1),  # 24 to 24
        ("i_fbdiv_strobe_h", ctypes.c_uint32, 1),  # 25 to 25
        ("i_ovc_snapshot_h", ctypes.c_uint32, 1),  # 26 to 26
        ("i_dither_value", ctypes.c_uint32, 5)  # 27 to 31
    ]


class MG_PLL_FRAC_LOCK_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MG_PLL_FRAC_LOCK_REG),
        ("asUint", ctypes.c_uint32)]