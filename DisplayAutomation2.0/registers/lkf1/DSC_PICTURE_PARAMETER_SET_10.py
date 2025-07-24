import ctypes

'''
Register instance and offset 
'''
PPS10_0_A = 0x78098
PPS10_1_A = 0x78198
PPS10_0_B = 0x78298
PPS10_1_B = 0x78398
PPS10_0_C = 0x78498
PPS10_1_C = 0x78598
PPS10_0_D = 0x78698
PPS10_1_D = 0x78798

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_10_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_quant_incr_limit0", ctypes.c_uint32, 5),
        ("reserved10", ctypes.c_uint32, 3),
        ("rc_quant_incr_limit1", ctypes.c_uint32, 5),
        ("reserved11", ctypes.c_uint32, 3),
        ("rc_tgt_offset_hi", ctypes.c_uint32, 4),
        ("rc_tgt_offset_lo", ctypes.c_uint32, 4),
        ("reserved12", ctypes.c_uint32, 8)
    ]


class DSC_PICTURE_PARAMETER_SET_10(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_10_FIELDS),
        ("asUint", ctypes.c_uint32) ]
