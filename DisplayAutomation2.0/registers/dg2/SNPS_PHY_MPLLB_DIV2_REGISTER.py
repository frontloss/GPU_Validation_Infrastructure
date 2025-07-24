import ctypes

'''
Register instance and offset
'''
SNPS_PHY_MPLLB_DIV2_PORT_A = 0x16801C
SNPS_PHY_MPLLB_DIV2_PORT_B = 0x16901C
SNPS_PHY_MPLLB_DIV2_PORT_C = 0x16A01C
SNPS_PHY_MPLLB_DIV2_PORT_D = 0x16B01C
SNPS_PHY_MPLLB_DIV2_PORT_TC1 = 0x16C01C
'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class SNPS_PHY_MPLLB_DIV2_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dp_mpllb_mulitplier", ctypes.c_uint32, 12),  # 0 to 11
        ("dp_ref_clk_mpllb_div", ctypes.c_uint32, 3),  # 12 to 14
        ("hdmi_mpllb_hdmi_div", ctypes.c_uint32, 3),  # 15 to 17
        ("dmi_mpllb_hdmi_pixel_clk_div", ctypes.c_uint32, 2),  # 18 to 19
        ("reserved_20", ctypes.c_uint32, 12),  # 20 to 31
    ]


class SNPS_PHY_MPLLB_DIV2_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SNPS_PHY_MPLLB_DIV2_REG),
        ("asUint", ctypes.c_uint32)]
