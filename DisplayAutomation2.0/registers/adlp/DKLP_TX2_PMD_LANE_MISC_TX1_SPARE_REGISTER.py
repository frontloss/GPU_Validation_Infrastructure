import ctypes

'''
Register instance and offset
'''

DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_TC1 = 0x168E5C
DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_TC2 = 0x169E5C
DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_TC3 = 0x16AE5C
DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_TC4 = 0x16BE5C

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reg_value", ctypes.c_uint32, 32)  # 0 to 31
    ]


class DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_TX2_PMD_LANE_MISC_TX1_SPARE_REG),
        ("asUint", ctypes.c_uint32)]