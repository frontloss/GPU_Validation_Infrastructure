import ctypes

'''
Register instance and offset
'''
PORT_PLL_9_A = 0x162124
PORT_PLL_9_B = 0x6C124
PORT_PLL_9_C = 0x163124

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_9_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_lockthreshsel", ctypes.c_uint32, 1),  # 0 to 0
        ("i_lockthresh", ctypes.c_uint32, 3),  # 1 to 3
        ("reserved_4", ctypes.c_uint32, 4),  # 4 to 7
        ("i_afccntsel", ctypes.c_uint32, 1),  # 8 to 8
        ("i_dcoditheren_h", ctypes.c_uint32, 1),  # 9 to 9
        ("i_useidvdata_h", ctypes.c_uint32, 1),  # 10 to 10
        ("reserved_11", ctypes.c_uint32, 5),  # 11 to 15
        ("i_pllwait_cntr", ctypes.c_uint32, 3),  # 16 to 18
        ("reserved_19", ctypes.c_uint32, 13)  # 19 to 31
    ]


class PORT_PLL_9_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_9_REG),
        ("asUint", ctypes.c_uint32)]