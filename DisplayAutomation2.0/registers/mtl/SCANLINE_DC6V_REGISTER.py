import ctypes

'''
Register instance and offset 
'''
SCANLINE_DC6V = 0x4559C


'''
Register bitfield definition structure 
'''
class SCANLINE_DC6V_REG( ctypes.LittleEndianStructure):
    _fields_ = [
        ("line_counter_for_display", ctypes.c_uint32, 20),  # 0 to 19
        ("reserved_20", ctypes.c_uint32, 12),  # 20 to 31
    ]


class SCANLINE_DC6V_REGISTER( ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SCANLINE_DC6V_REG),
        ("asUint", ctypes.c_uint32)
    ]

