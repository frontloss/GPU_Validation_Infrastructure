import ctypes

'''
Register instance and offset
'''
LUT_3D_DATA_A = 0x490AC
LUT_3D_DATA_B = 0x491AC

'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class LUT_3D_DATA_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("lut_3d_entry", ctypes.c_uint32, 30),  # 0 to 29
        ("reserved_30", ctypes.c_uint32, 2),  # 30 to 31
    ]


class LUT_3D_DATA_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", LUT_3D_DATA_REG),
        ("asUint", ctypes.c_uint32)]
