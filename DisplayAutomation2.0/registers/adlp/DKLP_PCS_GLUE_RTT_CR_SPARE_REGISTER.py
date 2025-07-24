import ctypes

'''
Register instance and offset
'''

DKLP_PCS_GLUE_RTT_CR_SPARE_TC1 = 0x1682D4
DKLP_PCS_GLUE_RTT_CR_SPARE_TC2 = 0x1692D4
DKLP_PCS_GLUE_RTT_CR_SPARE_TC3 = 0x16A2D4
DKLP_PCS_GLUE_RTT_CR_SPARE_TC4 = 0x16B2D4

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_PCS_GLUE_RTT_CR_SPARE_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reg_value", ctypes.c_uint32, 32)  # 0 to 31
    ]


class DKLP_PCS_GLUE_RTT_CR_SPARE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_PCS_GLUE_RTT_CR_SPARE_REG),
        ("asUint", ctypes.c_uint32)]