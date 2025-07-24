import ctypes

'''
Register instance and offset
'''
SNPS_PHY_MPLLB_SSCEN_PORT_A = 0x168014
SNPS_PHY_MPLLB_SSCEN_PORT_B = 0x169014
SNPS_PHY_MPLLB_SSCEN_PORT_C = 0x16A014
SNPS_PHY_MPLLB_SSCEN_PORT_D = 0x16B014
SNPS_PHY_MPLLB_SSCEN_PORT_TC1 = 0x16C014
'''
Register field expected values
'''
dp_mpllb_ssc_en_ENABLE = 0b1
dp_mpllb_ssc_en_DISABLE = 0b0

'''
Register bitfield definition structure
'''


class SNPS_PHY_MPLLB_SSCEN_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 10),  # 0 to 9
        ("dp_mpllb_ssc_peak", ctypes.c_uint32, 20),  # 10 to 29
        ("dp_mpllb_ssc_up_spread", ctypes.c_uint32, 1),  # 30 to 30
        ("dp_mpllb_ssc_en", ctypes.c_uint32, 1),  # 31 to 31
    ]


class SNPS_PHY_MPLLB_SSCEN_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SNPS_PHY_MPLLB_SSCEN_REG),
        ("asUint", ctypes.c_uint32)]
