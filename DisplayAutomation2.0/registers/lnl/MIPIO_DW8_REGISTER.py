import ctypes

'''
Register instance and offset 
'''
MIPIO_DW8_MIPI_A = 0x1621A0
MIPIO_DW8_MIPI_C = 0x6C1A0

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class MIPIO_DW8_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 16),  # 0 to 15
        ("escape_clock_divider_m", ctypes.c_uint32, 8),  # 16 to 23
        ("reserved_24", ctypes.c_uint32, 8)  # 24 to 31
    ]


class MIPIO_DW8_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MIPIO_DW8_REG),
        ("asUint", ctypes.c_uint32)]

