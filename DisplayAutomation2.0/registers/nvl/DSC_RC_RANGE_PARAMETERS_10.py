import ctypes

'''
Register instance and offset 
'''
RC_RANGE10_0_A = 0x78010
RC_RANGE10_1_A = 0x78110
RC_RANGE10_0_B = 0x78210
RC_RANGE10_1_B = 0x78310
RC_RANGE10_0_C = 0x78410
RC_RANGE10_1_C = 0x78510
RC_RANGE10_0_D = 0x78610
RC_RANGE10_1_D = 0x78710

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_RANGE_PARAMS_10_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_min_qp_4", ctypes.c_uint32, 5),
        ("rc_max_qp_4", ctypes.c_uint32, 5),
        ("rc_bpg_offset_4", ctypes.c_uint32, 6),
        ("rc_min_qp_5", ctypes.c_uint32, 5),
        ("rc_max_qp_5", ctypes.c_uint32, 5),
        ("rc_bpg_offset_5", ctypes.c_uint32, 6)
    ]


class DSC_RC_RANGE_PARAMETERS_10(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_RANGE_PARAMS_10_FIELDS),
        ("asUint", ctypes.c_uint32)]
