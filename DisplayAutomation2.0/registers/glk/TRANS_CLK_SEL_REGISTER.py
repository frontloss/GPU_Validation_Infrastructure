import ctypes

'''
Register instance and offset
'''
TRANS_CLK_SEL_A = 0x46140
TRANS_CLK_SEL_B = 0x46144
TRANS_CLK_SEL_C = 0x46148

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class TRANS_CLK_SEL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 28),  # 0 to 27
        ("reserved_28", ctypes.c_uint32, 1),  # 28 to 28
        ("trans_clock_select", ctypes.c_uint32, 3)  # 29 to 31
    ]


class TRANS_CLK_SEL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TRANS_CLK_SEL_REG),
        ("asUint", ctypes.c_uint32)]