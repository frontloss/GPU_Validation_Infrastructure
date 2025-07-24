import ctypes

'''
Register instance and offset
'''
PORT_PLL_0_A = 0x162100
PORT_PLL_0_B = 0x6C100
PORT_PLL_0_C = 0x163100

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_0_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_fbdivratio", ctypes.c_uint32, 8),  # 0 to 7
        ("reserved_8", ctypes.c_uint32, 24)  # 8 to 31
    ]


class PORT_PLL_0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_0_REG),
        ("asUint", ctypes.c_uint32)]