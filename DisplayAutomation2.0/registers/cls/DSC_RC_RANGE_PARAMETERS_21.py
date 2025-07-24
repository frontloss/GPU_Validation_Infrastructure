import ctypes

'''
Register instance and offset 
'''
RC_RANGE21_0_A = 0x7801C
RC_RANGE21_1_A = 0x7811C
RC_RANGE21_0_B = 0x7821C
RC_RANGE21_1_B = 0x7831C
RC_RANGE21_0_C = 0x7841C
RC_RANGE21_1_C = 0x7851C
RC_RANGE21_0_D = 0x7861C
RC_RANGE21_1_D = 0x7871C

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_RANGE_PARAMS_21_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_min_qp_10", ctypes.c_uint32, 5),
        ("rc_max_qp_10", ctypes.c_uint32, 5),
        ("rc_bpg_offset_10", ctypes.c_uint32, 6),
        ("rc_min_qp_11", ctypes.c_uint32, 5),
        ("rc_max_qp_11", ctypes.c_uint32, 5),
        ("rc_bpg_offset_11", ctypes.c_uint32, 6)
    ]


class DSC_RC_RANGE_PARAMETERS_21(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_RANGE_PARAMS_21_FIELDS),
        ("asUint", ctypes.c_uint32)]
