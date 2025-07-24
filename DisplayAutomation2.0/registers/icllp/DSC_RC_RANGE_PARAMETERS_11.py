import ctypes

'''
Register instance and offset 
'''
RC_RANGE11_0_A = 0x6B24C
RC_RANGE11_1_A = 0x6BA4C
RC_RANGE11_0_B = 0x78214
RC_RANGE11_1_B = 0x78314
RC_RANGE11_0_C = 0x78414
RC_RANGE11_1_C = 0x78514


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_RANGE_PARAMS_11_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_min_qp_6", ctypes.c_uint32, 5),
        ("rc_max_qp_6", ctypes.c_uint32, 5),
        ("rc_bpg_offset_6", ctypes.c_uint32, 6),
        ("rc_min_qp_7", ctypes.c_uint32, 5),
        ("rc_max_qp_7", ctypes.c_uint32, 5),
        ("rc_bpg_offset_7", ctypes.c_uint32, 6)
    ]


class DSC_RC_RANGE_PARAMETERS_11(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_RANGE_PARAMS_11_FIELDS),
        ("asUint", ctypes.c_uint32)]
