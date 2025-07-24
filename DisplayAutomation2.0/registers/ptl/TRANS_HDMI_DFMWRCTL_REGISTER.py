import ctypes

'''
Register instance and offset 
'''
TRANS_HDMI_DFMWRCTL_A = 0x600C0
TRANS_HDMI_DFMWRCTL_B = 0x610C0
TRANS_HDMI_DFMWRCTL_C = 0x620C0
TRANS_HDMI_DFMWRCTL_D = 0x630C0

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class TRANS_HDMI_DFMWRCTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("tb_actual_offset", ctypes.c_uint32, 9),  # 0 to 8
        ("reserved", ctypes.c_uint32, 23),  # 9 to 31
    ]


class TRANS_HDMI_DFMWRCTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TRANS_HDMI_DFMWRCTL_REG),
        ("asUint", ctypes.c_uint32)]


