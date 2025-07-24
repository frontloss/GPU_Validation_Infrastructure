import ctypes

'''
Register instance and offset
'''
PIPE_DMC_CONTROL_A = 0x45250
PIPE_DMC_CONTROL_B = 0x45254
PIPE_DMC_CONTROL_C = 0x45258
PIPE_DMC_CONTROL_D = 0x4525C


'''
Register bitfield definition structure
'''
class PIPE_DMC_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('pipe_dmc_enable', ctypes.c_uint32, 1),
        ('reserved_1', ctypes.c_uint32, 30),
    ]


class PIPE_DMC_CONTROL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_DMC_REG ),
        ("asUint", ctypes.c_uint32 ) ]
	
