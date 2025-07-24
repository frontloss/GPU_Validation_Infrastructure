import ctypes

'''
Register instance and offset
'''
MG_PLL1_DIV0_PORT1 = 0x168A00
MG_PLL1_DIV0_PORT2 = 0x169A00
MG_PLL1_DIV0_PORT3 = 0x16AA00
MG_PLL1_DIV0_PORT4 = 0x16BA00

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class MG_PLL_DIV0_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_fbdiv_intgr", ctypes.c_uint32, 8),  # 0 to 7
        ("i_fbdiv_frac", ctypes.c_uint32, 22),  # 8 to 29
        ("i_fracnen_h", ctypes.c_uint32, 1),  # 30 to 30
        ("i_direct_pin_if_en", ctypes.c_uint32, 1)  # 31 to 31
    ]


class MG_PLL_DIV0_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MG_PLL_DIV0_REG),
        ("asUint", ctypes.c_uint32)]