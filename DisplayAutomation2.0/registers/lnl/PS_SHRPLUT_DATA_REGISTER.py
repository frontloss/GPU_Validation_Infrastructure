import ctypes

'''
Register instance and offset 
'''
PS_SHRPLUT_DATA_A = 0x682B8
PS_SHRPLUT_DATA_B = 0x68AB8
PS_SHRPLUT_DATA_C = 0x692B8
PS_SHRPLUT_DATA_D = 0x69AB8

'''
Register bitfield definition structure 
'''


class PS_SHRPLUT_DATA_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("adaptive_sharpness_lut_data", ctypes.c_uint32, 12),  # 0 to 11
        ('reserved12',                  ctypes.c_uint32, 20),  # 12 to 31
    ]


class PS_SHRPLUT_DATA_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PS_SHRPLUT_DATA_REG),
        ("asUint", ctypes.c_uint32)]
