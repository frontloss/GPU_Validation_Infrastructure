import ctypes

# Bspec link : https://gfxspecs.intel.com/Predator/Home/Index/50216

'''
Register instance and offset 
'''
TRANS_CLK_SEL_A = 0x46140
TRANS_CLK_SEL_B = 0x46144
TRANS_CLK_SEL_C = 0x46148
TRANS_CLK_SEL_D = 0X4614C

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class TRANS_CLK_SEL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 27),  # 0 to 26
        ("reserved_27", ctypes.c_uint32, 1),  # 27 to 27
        ("trans_clock_select", ctypes.c_uint32, 4)  # 28 to 31
    ]


class TRANS_CLK_SEL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TRANS_CLK_SEL_REG),
        ("asUint", ctypes.c_uint32)]