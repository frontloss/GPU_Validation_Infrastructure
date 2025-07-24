import ctypes

'''
Register instance and offset
'''
PORT_PLL_6_A = 0x162118
PORT_PLL_6_B = 0x6C118
PORT_PLL_6_C = 0x163118

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_6_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_prop_coeff", ctypes.c_uint32, 4),  # 0 to 3
        ("reserved_4", ctypes.c_uint32, 4),  # 4 to 7
        ("i_int_coeff", ctypes.c_uint32, 5),  # 8 to 12
        ("reserved_13", ctypes.c_uint32, 3),  # 13 to 15
        ("i_gainctrl", ctypes.c_uint32, 3),  # 16 to 18
        ("reserved_19", ctypes.c_uint32, 13)  # 19 to 31
    ]


class PORT_PLL_6_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_6_REG),
        ("asUint", ctypes.c_uint32)]