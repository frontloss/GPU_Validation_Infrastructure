import ctypes

'''
Register instance and offset
'''
MG_CLKTOP_HSCLKCTL_PORT1 = 0x1688D4
MG_CLKTOP_HSCLKCTL_PORT2 = 0x1698D4
MG_CLKTOP_HSCLKCTL_PORT3 = 0x16A8D4
MG_CLKTOP_HSCLKCTL_PORT4 = 0x16B8D4

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class MG_CLKTOP_HSCLKCTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("od_clktop_hsdiv_en_h", ctypes.c_uint32, 1),  # 0 to 0
        ("reserved_1", ctypes.c_uint32, 1),  # 1 to 1
        ("od_clktop_dsdiv_en_h", ctypes.c_uint32, 1),  # 2 to 2
        ("od_clktop_tlinedrv_enright_h_ovrd", ctypes.c_uint32, 1),  # 3 to 3
        ("od_clktop_tlinedrv_enleft_h_ovrd", ctypes.c_uint32, 1),  # 4 to 4
        ("od_clktop_tlinedrv_enright_ded_h_ovrd", ctypes.c_uint32, 1),  # 5 to 5
        ("od_clktop_tlinedrv_enleft_ded_h_ovrd", ctypes.c_uint32, 1),  # 6 to 6
        ("od_clktop_tlinedrv_overrideen", ctypes.c_uint32, 1),  # 7 to 7
        ("od_clktop_dsdiv_divratio", ctypes.c_uint32, 4),  # 8 to 11
        ("od_clktop_hsdiv_divratio", ctypes.c_uint32, 2),  # 12 to 13
        ("od_clktop_tlinedrv_clksel", ctypes.c_uint32, 2),  # 14 to 15
        ("od_clktop_coreclk_inputsel", ctypes.c_uint32, 1),  # 16 to 16
        ("reserved_17", ctypes.c_uint32, 1),  # 17 to 17
        ("od_clktop_outclk_bypassen_h", ctypes.c_uint32, 1),  # 18 to 18
        ("reserved_19", ctypes.c_uint32, 1),  # 19 to 19
        ("od_clktop_clktop_vhfclk_testen_h", ctypes.c_uint32, 2),  # 20 to 21
        ("reserved_22", ctypes.c_uint32, 2),  # 22 to 23
        ("od_clktop_clk2obs_en_h", ctypes.c_uint32, 1),  # 24 to 24
        ("od_clktop_clkobs_muxsel", ctypes.c_uint32, 2),  # 25 to 26
        ("reserved_27", ctypes.c_uint32, 5)  # 27 to 31
    ]


class MG_CLKTOP_HSCLKCTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MG_CLKTOP_HSCLKCTL_REG),
        ("asUint", ctypes.c_uint32)]