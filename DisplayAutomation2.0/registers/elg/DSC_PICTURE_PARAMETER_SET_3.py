import ctypes

'''
Register instance and offset 
'''
PPS3_0_A = 0x7807C
PPS3_1_A = 0x7817C
PPS3_2_A = 0x7887C
PPS3_0_B = 0x7827C
PPS3_1_B = 0x7837C
PPS3_2_B = 0x7897C
PPS3_0_C = 0x7847C
PPS3_1_C = 0x7857C
PPS3_2_C = 0x78A7C
PPS3_0_D = 0x7867C
PPS3_1_D = 0x7877C
PPS3_2_D = 0x78B7C

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_3_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("slice_height", ctypes.c_uint32, 16),
        ("slice_width", ctypes.c_uint32, 16)
    ]


class DSC_PICTURE_PARAMETER_SET_3(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_3_FIELDS),
        ("asUint", ctypes.c_uint32) ]

