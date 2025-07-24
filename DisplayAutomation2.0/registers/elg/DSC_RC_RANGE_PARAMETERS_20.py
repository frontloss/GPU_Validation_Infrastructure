import ctypes

'''
Register instance and offset 
'''
RC_RANGE20_0_A = 0x78018
RC_RANGE20_1_A = 0x78118
RC_RANGE20_2_A = 0x78818
RC_RANGE20_0_B = 0x78218
RC_RANGE20_1_B = 0x78318
RC_RANGE20_2_B = 0x78918
RC_RANGE20_0_C = 0x78418
RC_RANGE20_1_C = 0x78518
RC_RANGE20_2_C = 0x78A18
RC_RANGE20_0_D = 0x78618
RC_RANGE20_1_D = 0x78718
RC_RANGE20_2_D = 0x78B18


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_RANGE_PARAMS_20_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_min_qp_8", ctypes.c_uint32, 5),
        ("rc_max_qp_8", ctypes.c_uint32, 5),
        ("rc_bpg_offset_8", ctypes.c_uint32, 6),
        ("rc_min_qp_9", ctypes.c_uint32, 5),
        ("rc_max_qp_9", ctypes.c_uint32, 5),
        ("rc_bpg_offset_9", ctypes.c_uint32, 6)
    ]


class DSC_RC_RANGE_PARAMETERS_20(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_RANGE_PARAMS_20_FIELDS),
        ("asUint", ctypes.c_uint32)]
