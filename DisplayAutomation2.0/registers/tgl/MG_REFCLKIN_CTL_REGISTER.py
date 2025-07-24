import ctypes

'''
Register instance and offset
'''
MG_REFCLKIN_CTL_PORT1 = 0x16892C
MG_REFCLKIN_CTL_PORT2 = 0x16992C
MG_REFCLKIN_CTL_PORT3 = 0x16A92C
MG_REFCLKIN_CTL_PORT4 = 0x16B92C

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class MG_REFCLKIN_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("od_refclkin1_refclkmux", ctypes.c_uint32, 3),  # 0 to 2
        ("od_refclkin1_refclkinjmux", ctypes.c_uint32, 1),  # 3 to 3
        ("reserved_4", ctypes.c_uint32, 4),  # 4 to 7
        ("od_refclkin2_refclkmux", ctypes.c_uint32, 3),  # 8 to 10
        ("od_refclkin2_refclkinjmux", ctypes.c_uint32, 1),  # 11 to 11
        ("reserved_12", ctypes.c_uint32, 20)  # 12 to 31
    ]


class MG_REFCLKIN_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MG_REFCLKIN_CTL_REG),
        ("asUint", ctypes.c_uint32)]