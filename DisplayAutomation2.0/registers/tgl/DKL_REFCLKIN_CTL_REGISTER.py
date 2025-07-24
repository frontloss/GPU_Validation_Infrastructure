import ctypes

'''
Register instance and offset
'''

DKL_REFCLKIN_CTL_NULL_D = 0x16812c
DKL_REFCLKIN_CTL_NULL_E = 0x16912c
DKL_REFCLKIN_CTL_NULL_F = 0x16A12c
DKL_REFCLKIN_CTL_NULL_G = 0x16B12c
DKL_REFCLKIN_CTL_NULL_H = 0x16C12c
DKL_REFCLKIN_CTL_NULL_I = 0x16D12c

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_REFCLKIN_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("od_refclkin1_refclkmux", ctypes.c_uint32, 3),  # 0 to 2
        ("od_refclkin1_refclkinjmux", ctypes.c_uint32, 1),  # 3 to 3
        ("reserved_4", ctypes.c_uint32, 4),  # 4 to 7
        ("od_refclkin2_refclkmux", ctypes.c_uint32, 3),  # 8 to 10
        ("od_refclkin2_refclkinjmux", ctypes.c_uint32, 1),  # 11 to 11
        ("reserved_12", ctypes.c_uint32, 20) # 12 to 31
    ]


class DKL_REFCLKIN_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_REFCLKIN_CTL_REG),
        ("asUint", ctypes.c_uint32)]