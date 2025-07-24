import ctypes

'''
Register instance and offset
'''
SNPS_PHY_MPLLB_FRACN1_PORT_A = 0x168008
SNPS_PHY_MPLLB_FRACN1_PORT_B = 0x169008
SNPS_PHY_MPLLB_FRACN1_PORT_C = 0x16A008
SNPS_PHY_MPLLB_FRACN1_PORT_D = 0x16B008
SNPS_PHY_MPLLB_FRACN1_PORT_TC1 = 0x16C008
'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class SNPS_PHY_MPLLB_FRACN1_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dp_mpllb_fracn_den", ctypes.c_uint32, 16),  # 0 to 15
        ("reserved_16", ctypes.c_uint32, 14),  # 16 to 29
        ("dp_mpllb_fracn_cfg_update_en", ctypes.c_uint32, 1),  # 30 to 30
        ("dp_mpllb_fracn_en", ctypes.c_uint32, 1),  # 31 to 31
    ]


class SNPS_PHY_MPLLB_FRACN1_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SNPS_PHY_MPLLB_FRACN1_REG),
        ("asUint", ctypes.c_uint32)]
