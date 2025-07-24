import ctypes

'''
Register instance and offset
'''
PORT_PLL_3_A = 0x16210C
PORT_PLL_3_B = 0x6C10C
PORT_PLL_3_C = 0x16310C

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_3_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_feedfwrdgain", ctypes.c_uint32, 4),  # 0 to 3
        ("reserved_4", ctypes.c_uint32, 4),  # 4 to 7
        ("i_fracmodorder", ctypes.c_uint32, 1),  # 8 to 8
        ("reserved_9", ctypes.c_uint32, 7),  # 9 to 15
        ("i_fracnen_h", ctypes.c_uint32, 1),  # 16 to 16
        ("reserved_17", ctypes.c_uint32, 15)  # 17 to 31
    ]


class PORT_PLL_3_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_3_REG),
        ("asUint", ctypes.c_uint32)]