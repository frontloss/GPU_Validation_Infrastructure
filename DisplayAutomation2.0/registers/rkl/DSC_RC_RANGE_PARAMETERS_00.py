import ctypes

'''
Register instance and offset 
'''
RC_RANGE00_0_A = 0x78008
RC_RANGE00_1_A = 0x78108
RC_RANGE00_0_B = 0x78208
RC_RANGE00_1_B = 0x78308
RC_RANGE00_0_C = 0x78408
RC_RANGE00_1_C = 0x78508


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_RANGE_PARAMS_00_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_min_qp_0", ctypes.c_uint32, 5),
        ("rc_max_qp_0", ctypes.c_uint32, 5),
        ("rc_bpg_offset_0", ctypes.c_uint32, 6),
        ("rc_min_qp_1", ctypes.c_uint32, 5),
        ("rc_max_qp_1", ctypes.c_uint32, 5),
        ("rc_bpg_offset_1", ctypes.c_uint32, 6)
    ]


class DSC_RC_RANGE_PARAMETERS_00(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_RANGE_PARAMS_00_FIELDS),
        ("asUint", ctypes.c_uint32)]
