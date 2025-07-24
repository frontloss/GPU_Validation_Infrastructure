##
# BSpec link https://gfxspecs.intel.com/Predator/Home/Index/66276
import ctypes

'''
Register instance and offset
'''
CLKGATE_DIS_MISC = 0x604E8


'''
Register bitfield definition structure
'''


class CLKGATE_DIS_MISC_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('dptp_gating_dis', ctypes.c_uint32, 1),
        ('dpt_gating_dis', ctypes.c_uint32, 1),
        ('dhdcpddi_gating_dis', ctypes.c_uint32, 1),
        ('hdmi_gating_dis', ctypes.c_uint32, 1),
        ('dsf_gating_dis', ctypes.c_uint32, 1),
        ('dacbe_gating_dis', ctypes.c_uint32, 1),
        ('hdmi_frl_gating_dis', ctypes.c_uint32, 1),
        ('dmasc_gating_dis', ctypes.c_uint32, 1),
        ('reserved_8', ctypes.c_uint32, 24),
    ]


class CLKGATE_DIS_MISC_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CLKGATE_DIS_MISC_REG ),
        ("asUint", ctypes.c_uint32 ) ]
