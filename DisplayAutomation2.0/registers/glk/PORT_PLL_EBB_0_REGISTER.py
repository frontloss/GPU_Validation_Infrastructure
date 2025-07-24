import ctypes

'''
Register instance and offset
'''
PORT_PLL_EBB_0_A = 0x162034
PORT_PLL_EBB_0_B = 0x6C034
PORT_PLL_EBB_0_C = 0x163034

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_EBB_0_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_plllock", ctypes.c_uint32, 1),  # 0 to 0
        ("i_pllfreqlock", ctypes.c_uint32, 1),  # 1 to 1
        ("reserved_2", ctypes.c_uint32, 6),  # 2 to 7
        ("o_dtp2divsel", ctypes.c_uint32, 5),  # 8 to 12
        ("o_dtp1divsel", ctypes.c_uint32, 3),  # 13 to 15
        ("reserved_15", ctypes.c_uint32, 17)  # 15 to 31
    ]


class PORT_PLL_EBB_0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_EBB_0_REG),
        ("asUint", ctypes.c_uint32)]