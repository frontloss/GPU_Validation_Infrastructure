##
# BSpec link https://gfxspecs.intel.com/Predator/Home/Index/49431
import ctypes

'''
Register instance and offset
'''
CLKGATE_DIS_MISC = 0x46534


'''
Register bitfield definition structure
'''

class CLKGATE_DIS_MISC_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('reserved0', ctypes.c_uint32, 11),
        ('dcmp_gating_dis', ctypes.c_uint32, 1),
        ('reserved_12', ctypes.c_uint32, 7),
        ('dmasd_gating_dis', ctypes.c_uint32, 1),
        ('dmasc_ram_gating_dis', ctypes.c_uint32, 1),
        ('dmasc_gating_dis', ctypes.c_uint32, 1),
        ('reserved_22', ctypes.c_uint32, 6),
        ('dbufRam_gating_dis', ctypes.c_uint32, 1),
        ('dbuf_gating_dis', ctypes.c_uint32, 1),
        ('dbrc_gating_dis', ctypes.c_uint32, 1),
        ('dciph_gating_dis', ctypes.c_uint32, 1),
    ]


class CLKGATE_DIS_MISC_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CLKGATE_DIS_MISC_REG ),
        ("asUint", ctypes.c_uint32 ) ]
