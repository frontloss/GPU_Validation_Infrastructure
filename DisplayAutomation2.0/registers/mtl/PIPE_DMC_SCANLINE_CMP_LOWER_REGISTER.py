import ctypes

# bspec link - https://gfxspecs.intel.com/Predator/Home/Index/67597

'''
Register instance and offset 
'''
PIPE_DMC_SCANLINE_CMP_LOWER_A = 0x5F120
PIPE_DMC_SCANLINE_CMP_LOWER_B = 0x5F520
PIPE_DMC_SCANLINE_CMP_LOWER_C = 0x5F920
PIPE_DMC_SCANLINE_CMP_LOWER_D = 0x5FD20


'''
Register bitfield defnition structure 
'''


class PIPE_DMC_SCANLINE_CMP_LOWER_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('scanline_lower', ctypes.c_uint32, 21),
        ('reserved_21', ctypes.c_uint32, 9),
        ('scanline_out_range_cmp_en', ctypes.c_uint32, 1),
        ('scanline_in_range_cmp_en', ctypes.c_uint32, 1),
    ]


class PIPE_DMC_SCANLINE_CMP_LOWER_REGISTER( ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PIPE_DMC_SCANLINE_CMP_LOWER_REG),
        ("asUint", ctypes.c_uint32)]
