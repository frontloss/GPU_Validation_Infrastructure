import ctypes

'''
Register instance and offset
'''
PORT_PLL_10_A = 0x162128
PORT_PLL_10_B = 0x6C128
PORT_PLL_10_C = 0x163128

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_10_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_dcofine", ctypes.c_uint32, 10),  # 0 to 9
        ("i_dcoamp", ctypes.c_uint32, 4),  # 10 to 13
        ("reserved_14", ctypes.c_uint32, 2),  # 14 to 15
        ("i_dcocoarse", ctypes.c_uint32, 8),  # 16 to 23
        ("i_dcofinesel", ctypes.c_uint32, 2),  # 24 to 25
        ("i_dcocoarse_ovrd_h", ctypes.c_uint32, 1),  # 26 to 26
        ("i_dcoampovrden_h", ctypes.c_uint32, 1),  # 27 to 27
        ("i_pllpwrmode", ctypes.c_uint32, 4)  # 28 to 31
    ]


class PORT_PLL_10_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_10_REG),
        ("asUint", ctypes.c_uint32)]