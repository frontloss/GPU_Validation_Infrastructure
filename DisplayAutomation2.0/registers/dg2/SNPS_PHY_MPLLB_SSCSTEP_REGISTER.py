import ctypes

'''
Register instance and offset
'''
SNPS_PHY_MPLLB_SSCSTEP_PORT_A = 0x168018
SNPS_PHY_MPLLB_SSCSTEP_PORT_B = 0x169018
SNPS_PHY_MPLLB_SSCSTEP_PORT_C = 0x16A018
SNPS_PHY_MPLLB_SSCSTEP_PORT_D = 0x16B018
SNPS_PHY_MPLLB_SSCSTEP_PORT_TC1 = 0x16C018
'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class SNPS_PHY_MPLLB_SSCSTEP_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 12),  # 0 to 11
        ("dp_mpllb_ssc_stepsize", ctypes.c_uint32, 20),  # 11 to 31
    ]


class SNPS_PHY_MPLLB_SSCSTEP_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SNPS_PHY_MPLLB_SSCSTEP_REG),
        ("asUint", ctypes.c_uint32)]
