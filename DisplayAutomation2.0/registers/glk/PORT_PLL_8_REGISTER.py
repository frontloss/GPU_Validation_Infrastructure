import ctypes

'''
Register instance and offset
'''
PORT_PLL_8_A = 0x162120
PORT_PLL_8_B = 0x6C120
PORT_PLL_8_C = 0x163120

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_8_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_tdctargetcnt", ctypes.c_uint32, 10),  # 0 to 9
        ("reserved_10", ctypes.c_uint32, 6),  # 10 to 15
        ("i_tdcsel", ctypes.c_uint32, 2),  # 16 to 17
        ("i_tdccalsetupdeten_h", ctypes.c_uint32, 1),  # 18 to 18
        ("i_fbdivdutycycsel", ctypes.c_uint32, 1),  # 16 to 16
        ("reserved_19", ctypes.c_uint32, 13)  # 19 to 31
    ]


class PORT_PLL_8_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_8_REG),
        ("asUint", ctypes.c_uint32)]