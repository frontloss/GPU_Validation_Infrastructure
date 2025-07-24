import ctypes

'''
Register instance and offset 
'''
RC_RANGE30_0_A = 0x78020
RC_RANGE30_1_A = 0x78120
RC_RANGE30_0_B = 0x78220
RC_RANGE30_1_B = 0x78320
RC_RANGE30_0_C = 0x78420
RC_RANGE30_1_C = 0x78520
RC_RANGE30_0_D = 0x78620
RC_RANGE30_1_D = 0x78720

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_RANGE_PARAMS_30_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_min_qp_12", ctypes.c_uint32, 5),
        ("rc_max_qp_12", ctypes.c_uint32, 5),
        ("rc_bpg_offset_12", ctypes.c_uint32, 6),
        ("rc_min_qp_13", ctypes.c_uint32, 5),
        ("rc_max_qp_13", ctypes.c_uint32, 5),
        ("rc_bpg_offset_13", ctypes.c_uint32, 6)
    ]


class DSC_RC_RANGE_PARAMETERS_30(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_RANGE_PARAMS_30_FIELDS),
        ("asUint", ctypes.c_uint32)]
