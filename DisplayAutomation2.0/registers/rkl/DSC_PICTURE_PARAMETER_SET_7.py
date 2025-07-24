import ctypes

'''
Register instance and offset 
'''
PPS7_0_A = 0x7808C
PPS7_1_A = 0x7818C
PPS7_0_B = 0x7828C
PPS7_1_B = 0x7838C
PPS7_0_C = 0x7848C
PPS7_1_C = 0x7858C


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_7_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("slice_bpg_offset", ctypes.c_uint32, 16),
        ("nfl_bpg_offset", ctypes.c_uint32, 16)
    ]


class DSC_PICTURE_PARAMETER_SET_7(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_7_FIELDS),
        ("asUint", ctypes.c_uint32) ]
