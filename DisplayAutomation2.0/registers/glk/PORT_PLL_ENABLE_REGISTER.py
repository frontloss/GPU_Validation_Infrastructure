import ctypes

'''
Register instance and offset
'''
PORT_PLL_ENABLE_A = 0x46074
PORT_PLL_ENABLE_B = 0x46078
PORT_PLL_ENABLE_C = 0x4607C

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_ENABLE_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 25),  # 0 to 24
        ("power_state", ctypes.c_uint32, 1),  # 25 to 25
        ("power_enable", ctypes.c_uint32, 1),  # 26 to 26
        ("reference_select", ctypes.c_uint32, 1),  # 27 to 27
        ("reserved_28", ctypes.c_uint32, 2),  # 28 to 29
        ("pll_lock", ctypes.c_uint32, 1),  # 30 to 30
        ("pll_enable", ctypes.c_uint32, 1)  # 31 to 31
    ]


class PORT_PLL_ENABLE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_ENABLE_REG),
        ("asUint", ctypes.c_uint32)]