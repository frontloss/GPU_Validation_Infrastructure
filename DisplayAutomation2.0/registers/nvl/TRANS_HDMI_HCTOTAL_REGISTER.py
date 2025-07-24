import ctypes

'''
Register instance and offset 
'''
TRANS_HDMI_HCTOTAL_A = 0x600B8
TRANS_HDMI_HCTOTAL_B = 0x610B8
TRANS_HDMI_HCTOTAL_C = 0x620B8
TRANS_HDMI_HCTOTAL_D = 0x630B8

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class TRANS_HDMI_HC_TOTAL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("hc_active", ctypes.c_uint32, 14),  # 0 to 13
        ("reserved_1", ctypes.c_uint32, 2),  # 14 to 15
        ("hc_total", ctypes.c_uint32, 14),  # 16 to 29
        ("reserved_2", ctypes.c_uint32, 2),  # 30 to 31
    ]


class TRANS_HDMI_HCTOTAL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TRANS_HDMI_HC_TOTAL_REG),
        ("asUint", ctypes.c_uint32)]


