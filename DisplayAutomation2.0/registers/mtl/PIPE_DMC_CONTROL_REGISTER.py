import ctypes

'''
Register instance and offset
'''
PIPE_DMC_CONTROL = 0x45250


'''
Register bitfield definition structure
'''
class PIPE_DMC_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('pipe_dmc_enable_a', ctypes.c_uint32, 1),
        ('reserved_1', ctypes.c_uint32, 3),
        ('pipe_dmc_enable_b', ctypes.c_uint32, 1),
        ('reserved_5', ctypes.c_uint32, 3),
        ('pipe_dmc_enable_c', ctypes.c_uint32, 1),
        ('reserved_9', ctypes.c_uint32, 3),
        ('pipe_dmc_enable_d', ctypes.c_uint32, 1),
        ('reserved_13', ctypes.c_uint32, 18),
    ]


class PIPE_DMC_CONTROL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_DMC_REG ),
        ("asUint", ctypes.c_uint32 ) ]
