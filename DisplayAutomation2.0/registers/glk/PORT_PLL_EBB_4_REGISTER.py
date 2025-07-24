import ctypes

'''
Register instance and offset
'''
PORT_PLL_EBB_4_A = 0x162038
PORT_PLL_EBB_4_B = 0x6C038
PORT_PLL_EBB_4_C = 0x163038

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_PLL_EBB_4_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 13),  # 0 to 12
        ("o_dtdclkpen_h", ctypes.c_uint32, 1),  # 13 to 13
        ("o_dtafcrecal", ctypes.c_uint32, 1),  # 14 to 14
        ("reserved_15", ctypes.c_uint32, 17)  # 15 to 31
    ]


class PORT_PLL_EBB_4_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_PLL_EBB_4_REG),
        ("asUint", ctypes.c_uint32)]