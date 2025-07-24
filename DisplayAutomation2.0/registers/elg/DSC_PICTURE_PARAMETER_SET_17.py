import ctypes

'''
Register instance and offset 
'''
PPS17_0_A = 0x780B4
PPS17_1_A = 0x781B4
PPS17_2_A = 0x788B4
PPS17_0_B = 0x782B4
PPS17_1_B = 0x783B4
PPS17_2_B = 0x789B4
PPS17_0_C = 0x784B4
PPS17_1_C = 0x785B4
PPS17_2_C = 0x78AB4
PPS17_0_D = 0x786B4
PPS17_1_D = 0x787B4
PPS17_2_D = 0x78BB4


##

# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_17_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved", ctypes.c_uint32, 27),
        ("second_line_bpg_offset", ctypes.c_uint32, 5),
    ]


class DSC_PICTURE_PARAMETER_SET_17(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_17_FIELDS),
        ("asUint", ctypes.c_uint32)]
