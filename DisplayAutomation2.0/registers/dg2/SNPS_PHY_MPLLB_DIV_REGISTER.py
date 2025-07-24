import ctypes

'''
Register instance and offset
'''
SNPS_PHY_MPLLB_DIV_PORT_A = 0x168004
SNPS_PHY_MPLLB_DIV_PORT_B = 0x169004
SNPS_PHY_MPLLB_DIV_PORT_C = 0x16A004
SNPS_PHY_MPLLB_DIV_PORT_D = 0x16B004
SNPS_PHY_MPLLB_DIV_PORT_TC1 = 0x16C004
'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class SNPS_PHY_MPLLB_DIV_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 13),  # 0 to 12
        ("filter_pll_input_mux_select", ctypes.c_uint32, 1),  # 13 to 13
        ("filter_pll_lock", ctypes.c_uint32, 1),  # 14 to 14
        ("filter_pll_enable", ctypes.c_uint32, 1),  # 15 to 15
        ("reserved_16", ctypes.c_uint32, 8),  # 16 to 23
        ("refclk_mux_select", ctypes.c_uint32, 1),  # 24 to 24
        ("dp_ref_clk_req", ctypes.c_uint32, 1),  # 25 to 25
        ("dp_ref_clk_en", ctypes.c_uint32, 1),  # 26 to 26
        ("ref_range", ctypes.c_uint32, 5),  # 27 to 31
    ]


class SNPS_PHY_MPLLB_DIV_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SNPS_PHY_MPLLB_DIV_REG),
        ("asUint", ctypes.c_uint32)]
