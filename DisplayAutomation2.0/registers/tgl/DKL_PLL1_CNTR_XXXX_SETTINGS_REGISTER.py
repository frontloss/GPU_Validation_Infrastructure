import ctypes

'''
Register instance and offset
'''

DKL_PLL1_CNTR_XXXX_SETTINGS_D = 0x168244
DKL_PLL1_CNTR_XXXX_SETTINGS_E = 0x169244
DKL_PLL1_CNTR_XXXX_SETTINGS_F = 0x16A244
DKL_PLL1_CNTR_XXXX_SETTINGS_G = 0x16B244
DKL_PLL1_CNTR_XXXX_SETTINGS_H = 0x16C244
DKL_PLL1_CNTR_XXXX_SETTINGS_I = 0x16D244

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_PLL1_CNTR_XXXX_SETTINGS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("I_IREFGEN_SETTLING_TIME_CNTR_7_0", ctypes.c_uint32, 8),  # 0 to 7
        ("I_IREFGEN_SETTLING_TIME_RO_STANDBY_1_0", ctypes.c_uint32, 2),  # 8 to 9
        ("RESERVED196", ctypes.c_uint32, 5),  # 10 to 14
        ("RESERVED197", ctypes.c_uint32, 1),  # 15 to 15
        ("AI_PLLLC_REG_FBCLKEXT_SEL", ctypes.c_uint32, 1),  # 16 to 16
        ("I_PLLLC_REG_LONGLOOPCLK_SEL", ctypes.c_uint32, 1),  # 17 to 17
        ("I_DITHER_DIV_1_0", ctypes.c_uint32, 2),  # 18 to 19
        ("I_M1_LONGLOOP_SEL", ctypes.c_uint32, 1),  # 20 to 20
        ("I_DFX_DIV_CKLO_1_0", ctypes.c_uint32, 2),  # 21 to 22
        ("RESERVED203", ctypes.c_uint32, 1),  # 23 to 23
        ("RESERVED204", ctypes.c_uint32, 4),  # 24 to 27
        ("RESERVED205", ctypes.c_uint32, 4)  # 28 to 31
    ]


class DKL_PLL1_CNTR_XXXX_SETTINGS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_PLL1_CNTR_XXXX_SETTINGS_REG),
        ("asUint", ctypes.c_uint32)]