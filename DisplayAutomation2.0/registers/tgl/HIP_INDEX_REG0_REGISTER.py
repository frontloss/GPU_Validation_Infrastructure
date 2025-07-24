import ctypes

'''
Register instance and offset
'''

HIP_INDEX_REG0 = 0x1010A0

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class HIP_INDEX_REG0_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("HIP_168_Index", ctypes.c_uint32, 8),  # 0 to 7
        ("HIP_169_Index", ctypes.c_uint32, 8),  # 8 to 15
        ("HIP_16A_Index", ctypes.c_uint32, 8),  # 16 to 23
        ("HIP_16B_Index", ctypes.c_uint32, 8)  # 24 to 31
    ]


class HIP_INDEX_REG0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", HIP_INDEX_REG0_REG),
        ("asUint", ctypes.c_uint32)]