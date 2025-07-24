import ctypes

'''
Register instance and offset
'''
PORT_PLL_2_A = 0x162108
PORT_PLL_2_B = 0x6C108
PORT_PLL_2_C = 0x163108

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_2_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_fracdiv", ctypes.c_uint32, 22),  # 0 to 21
        ("reserved_22", ctypes.c_uint32, 10)  # 22 to 31
    ]


class PORT_PLL_2_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_2_REG),
        ("asUint", ctypes.c_uint32)]