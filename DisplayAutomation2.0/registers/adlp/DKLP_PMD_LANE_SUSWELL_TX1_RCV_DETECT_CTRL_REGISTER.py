import ctypes

'''
Register instance and offset
'''

DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_TC1 = 0x168F90
DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_TC2 = 0x169F90
DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_TC3 = 0x16AF90
DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_TC4 = 0x16BF90

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reg_value", ctypes.c_uint32, 32)  # 0 to 31
    ]


class DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_PMD_LANE_SUSWELL_TX1_RCV_DETECT_CTRL_REG),
        ("asUint", ctypes.c_uint32)]