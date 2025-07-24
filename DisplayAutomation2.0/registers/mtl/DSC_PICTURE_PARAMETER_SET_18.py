import ctypes

'''
Register instance and offset 
'''
PPS18_0_A = 0x780B8
PPS18_1_A = 0x781B8
PPS18_0_B = 0x782B8
PPS18_1_B = 0x783B8
PPS18_0_C = 0x784B8
PPS18_1_C = 0x785B8
PPS18_0_D = 0x786B8
PPS18_1_D = 0x787B8

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_18_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("second_line_offset_adj", ctypes.c_uint32, 16),
        ("nsl_bpg_offset", ctypes.c_uint32, 16),
    ]


class DSC_PICTURE_PARAMETER_SET_18(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_18_FIELDS),
        ("asUint", ctypes.c_uint32)]
