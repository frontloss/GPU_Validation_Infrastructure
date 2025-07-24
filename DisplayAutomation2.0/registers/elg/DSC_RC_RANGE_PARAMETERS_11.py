import ctypes

'''
Register instance and offset 
'''
RC_RANGE11_0_A = 0x78014
RC_RANGE11_1_A = 0x78114
RC_RANGE11_2_A = 0x78814
RC_RANGE11_0_B = 0x78214
RC_RANGE11_1_B = 0x78314
RC_RANGE11_2_B = 0x78914
RC_RANGE11_0_C = 0x78414
RC_RANGE11_1_C = 0x78514
RC_RANGE11_2_C = 0x78A14
RC_RANGE11_0_D = 0x78614
RC_RANGE11_1_D = 0x78714
RC_RANGE11_2_D = 0x78B14


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
