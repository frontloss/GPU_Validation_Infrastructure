import ctypes

'''
Register instance and offset 
'''
RC_RANGE01_0_A = 0x7800C
RC_RANGE01_1_A = 0x7810C
RC_RANGE01_0_B = 0x7820C
RC_RANGE01_1_B = 0x7830C
RC_RANGE01_0_C = 0x7840C
RC_RANGE01_1_C = 0x7850C
RC_RANGE01_0_D = 0x7860C
RC_RANGE01_1_D = 0x7870C

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_RANGE_PARAMS_01_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_min_qp_2", ctypes.c_uint32, 5),
        ("rc_max_qp_2", ctypes.c_uint32, 5),
        ("rc_bpg_offset_2", ctypes.c_uint32, 6),
        ("rc_min_qp_3", ctypes.c_uint32, 5),
        ("rc_max_qp_3", ctypes.c_uint32, 5),
        ("rc_bpg_offset_3", ctypes.c_uint32, 6)
    ]


class DSC_RC_RANGE_PARAMETERS_01(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_RANGE_PARAMS_01_FIELDS),
        ("asUint", ctypes.c_uint32)]
