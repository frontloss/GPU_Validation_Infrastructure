import ctypes

'''
Register instance and offset 
'''
PPS6_0_A = 0x78088
PPS6_1_A = 0x78188
PPS6_2_A = 0x78888
PPS6_0_B = 0x78288
PPS6_1_B = 0x78388
PPS6_2_B = 0x78988
PPS6_0_C = 0x78488
PPS6_1_C = 0x78588
PPS6_2_C = 0x78A88
PPS6_0_D = 0x78688
PPS6_1_D = 0x78788
PPS6_2_D = 0x78B88



##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_6_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("initial_scale_value", ctypes.c_uint32, 6),
        ("reserved5", ctypes.c_uint32, 2),
        ("first_line_bpg_offset", ctypes.c_uint32, 5),
        ("reserved6", ctypes.c_uint32, 3),
        ("flatness_min_qp", ctypes.c_uint32, 5),
        ("reserved7", ctypes.c_uint32, 3),
        ("flatness_max_qp", ctypes.c_uint32, 5),
        ("reserved8", ctypes.c_uint32, 3)
    ]


class DSC_PICTURE_PARAMETER_SET_6(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_6_FIELDS),
        ("asUint", ctypes.c_uint32) ]
