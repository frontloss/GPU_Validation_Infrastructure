import ctypes

'''
Register instance and offset
'''
SNPS_PHY_MPLLB_FRACN2_PORT_A = 0x16800C
SNPS_PHY_MPLLB_FRACN2_PORT_B = 0x16900C
SNPS_PHY_MPLLB_FRACN2_PORT_C = 0x16A00C
SNPS_PHY_MPLLB_FRACN2_PORT_D = 0x16B00C
SNPS_PHY_MPLLB_FRACN2_PORT_TC1 = 0x16C00C
'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class SNPS_PHY_MPLLB_FRACN2_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dp_mpllb_fracn_rem", ctypes.c_uint32, 16),  # 16 to 31
        ("dp_mpllb_fracn_quot", ctypes.c_uint32, 16),  # 0 to 16
    ]


class SNPS_PHY_MPLLB_FRACN2_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SNPS_PHY_MPLLB_FRACN2_REG),
        ("asUint", ctypes.c_uint32)]
