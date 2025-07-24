import ctypes

'''
Register instance and offset
'''
PORT_PLL_1_A = 0x162104
PORT_PLL_1_B = 0x6C104
PORT_PLL_1_C = 0x163104

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_1_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_fbpredivratio", ctypes.c_uint32, 3),  # 0 to 2
        ("reserved_3", ctypes.c_uint32, 5),  # 3 to 7
        ("i_ndivratio", ctypes.c_uint32, 4),  # 8 to 11
        ("reserved_12", ctypes.c_uint32, 4),  # 12 to 15
        ("i_fbdivdutycycsel", ctypes.c_uint32, 1),  # 16 to 16
        ("i_divretimeren", ctypes.c_uint32, 1),  # 17 to 17
        ("reserved_18", ctypes.c_uint32, 14)  # 18 to 31
    ]


class PORT_PLL_1_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_1_REG),
        ("asUint", ctypes.c_uint32)]