import ctypes

'''
Register instance and offset 
'''
PS_SHARPNESS_CTRL_A = 0x682B0
PS_SHARPNESS_CTRL_B = 0x68AB0
PS_SHARPNESS_CTRL_C = 0x692B0
PS_SHARPNESS_CTRL_D = 0x69AB0

'''
Register field expected values 
'''
sharpness_filter_DISABLE = 0x0
sharpness_filter_ENABLE = 0x1

'''
Register bitfield definition structure 
'''


class PS_SHARPNESS_CTRL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('sharpness_filter_size',   ctypes.c_uint32, 2),    # 0 to 1
        ('reserved2',               ctypes.c_uint32, 6),    # 2 to 7
        ('strength',                ctypes.c_uint32, 8),    # 8 to 15
        ('reserved16',              ctypes.c_uint32, 15),   # 16 to 30
        ('sharpness_filter_enable', ctypes.c_uint32, 1),    # 31 to 31
    ]


class PS_SHARPNESS_CTRL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PS_SHARPNESS_CTRL_REG),
        ("asUint", ctypes.c_uint32)]
