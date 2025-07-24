import ctypes

# bspec link - https://gfxspecs.intel.com/Predator/Home/Index/67597

'''
Register instance and offset 
'''
PIPE_DMC_SCANLINE_CMP_UPPER_A = 0x5F124
PIPE_DMC_SCANLINE_CMP_UPPER_B = 0x5F524
PIPE_DMC_SCANLINE_CMP_UPPER_C = 0x5F924
PIPE_DMC_SCANLINE_CMP_UPPER_D = 0x5FD24


'''
Register bitfield defnition structure 
'''


class PIPE_DMC_SCANLINE_CMP_UPPER_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('scanline_upper', ctypes.c_uint32, 21),
        ('reserved_21', ctypes.c_uint32, 11)
    ]


class PIPE_DMC_SCANLINE_CMP_UPPER_REGISTER( ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_DMC_SCANLINE_CMP_UPPER_REG),
        ("asUint", ctypes.c_uint32)]
