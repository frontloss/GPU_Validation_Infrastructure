import ctypes

'''
Register instance and offset 
'''
RC_RANGE31_0_A = 0x78024
RC_RANGE31_1_A = 0x78124
RC_RANGE31_0_B = 0x78224
RC_RANGE31_1_B = 0x78324
RC_RANGE31_0_C = 0x78424
RC_RANGE31_1_C = 0x78524


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_RANGE_PARAMS_31_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_min_qp_14", ctypes.c_uint32, 5),
        ("rc_max_qp_14", ctypes.c_uint32, 5),
        ("rc_bpg_offset_14", ctypes.c_uint32, 6),
        ("reserved15", ctypes.c_uint32, 16),
    ]


class DSC_RC_RANGE_PARAMETERS_31(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_RANGE_PARAMS_31_FIELDS),
        ("asUint", ctypes.c_uint32)]
