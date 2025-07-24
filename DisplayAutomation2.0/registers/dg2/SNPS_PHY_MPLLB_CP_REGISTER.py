import ctypes

'''
Register instance and offset
'''
SNPS_PHY_MPLLB_CP_PORT_A = 0x168000
SNPS_PHY_MPLLB_CP_PORT_B = 0x169000
SNPS_PHY_MPLLB_CP_PORT_C = 0x16A000
SNPS_PHY_MPLLB_CP_PORT_D = 0x16B000
SNPS_PHY_MPLLB_CP_PORT_TC1 = 0x16C000
'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class SNPS_PHY_MPLLB_CP_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dp_shim_div32_clk_sel", ctypes.c_uint32, 1),  # 0 to 0
        ("reserved_1", ctypes.c_uint32, 4),  # 1 to 4
        ("dp_mpllb_tx_clk_div", ctypes.c_uint32, 3),  # 5 to 7
        ("dp_mpllb_word_div2_en", ctypes.c_uint32, 1),  # 8 to 8
        ("dp2_mode", ctypes.c_uint32, 1),  # 9 to 9
        ("dp_mpllb_pmix_en", ctypes.c_uint32, 1),  # 10 to 10
        ("reserved_11", ctypes.c_uint32, 5),  # 11 to 15
        ("dp_mpllb_div_multiplier", ctypes.c_uint32, 8),  # 16 to 23
        ("dp_mpllb_freq_vco", ctypes.c_uint32, 2),  # 24 to 25
        ("dp_mpllb_v2i", ctypes.c_uint32, 2),  # 26 to 27
        ("dp_mpllb_init_cal_disable", ctypes.c_uint32, 1),  # 28 to 28
        ("dp_mpllb_div5_clk_en", ctypes.c_uint32, 1),  # 29 to 29
        ("dp_mpllb_div_clk_en", ctypes.c_uint32, 1),  # 30 to 30
        ("dp_mpllb_force_en", ctypes.c_uint32, 1),  # 31 to 31
    ]


class SNPS_PHY_MPLLB_CP_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SNPS_PHY_MPLLB_CP_REG),
        ("asUint", ctypes.c_uint32)]
