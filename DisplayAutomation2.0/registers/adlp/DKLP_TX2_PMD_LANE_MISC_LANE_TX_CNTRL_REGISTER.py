import ctypes

'''
Register instance and offset
'''

DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_TC1 = 0x168E20
DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_TC2 = 0x169E20
DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_TC3 = 0x16AE20
DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_TC4 = 0x16BE20

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reg_value", ctypes.c_uint32, 32)  # 0 to 31
    ]


class DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_TX2_PMD_LANE_MISC_LANE_TX_CNTRL_REG),
        ("asUint", ctypes.c_uint32)]