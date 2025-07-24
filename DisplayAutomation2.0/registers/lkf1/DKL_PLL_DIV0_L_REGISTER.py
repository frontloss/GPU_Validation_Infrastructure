import ctypes

'''
Register instance and offset
'''

DKL_PLL_DIV0_L_NULL_D = 0x168200
DKL_PLL_DIV0_L_NULL_E = 0x169200

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_PLL_DIV0_L_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_fbdiv_intgr", ctypes.c_uint32, 8),  # 0 to 7
        ("i_fbdiv_frac", ctypes.c_uint32, 22),  # 8 to 29
        ("i_fracnen_h", ctypes.c_uint32, 1),  # 30 to 30
        ("i_direct_pin_if_en", ctypes.c_uint32, 1)  # 31 to 31
    ]

class DKL_PLL_DIV0_L_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_PLL_DIV0_L_REG),
        ("asUint", ctypes.c_uint32)]