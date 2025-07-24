import ctypes

'''
Register instance and offset 
'''
PPS9_0_A = 0x78094
PPS9_1_A = 0x78194
PPS9_2_A = 0x78894
PPS9_0_B = 0x78294
PPS9_1_B = 0x78394
PPS9_2_B = 0x78994
PPS9_0_C = 0x78494
PPS9_1_C = 0x78594
PPS9_2_C = 0x78A94
PPS9_0_D = 0x78694
PPS9_1_D = 0x78794
PPS9_2_D = 0x78B94


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_9_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_model_Size", ctypes.c_uint32, 16),
        ("rc_edge_factor", ctypes.c_uint32, 4),
        ("reserved9", ctypes.c_uint32, 12)
    ]


class DSC_PICTURE_PARAMETER_SET_9(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_9_FIELDS),
        ("asUint", ctypes.c_uint32) ]
