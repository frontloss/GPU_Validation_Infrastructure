import ctypes

'''
Register instance and offset
'''

DKLP_PCS_GLUE_TX1_FW_CALIB_TC1 = 0x1682F8
DKLP_PCS_GLUE_TX1_FW_CALIB_TC2 = 0x1692F8
DKLP_PCS_GLUE_TX1_FW_CALIB_TC3 = 0x16A2F8
DKLP_PCS_GLUE_TX1_FW_CALIB_TC4 = 0x16B2F8

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_PCS_GLUE_TX1_FW_CALIB_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reg_value", ctypes.c_uint32, 32)  # 0 to 31
    ]


class DKLP_PCS_GLUE_TX1_FW_CALIB_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_PCS_GLUE_TX1_FW_CALIB_REG),
        ("asUint", ctypes.c_uint32)]