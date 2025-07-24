import ctypes

'''
Register instance and offset 
'''
PPS2_0_A = 0x78078
PPS2_1_A = 0x78178
PPS2_2_A = 0x78878
PPS2_0_B = 0x78278
PPS2_1_B = 0x78378
PPS2_2_B = 0x78978
PPS2_0_C = 0x78478
PPS2_1_C = 0x78578
PPS2_2_C = 0x78A78
PPS2_0_D = 0x78678
PPS2_1_D = 0x78778
PPS2_2_D = 0x78B78

##
# @note     Source: https://gfxspecs.intel.com/Predator/Home/Index/50160
class DSC_PICTURE_PARAMETER_SET_2_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("pic_height", ctypes.c_uint32, 16),
        ("pic_width", ctypes.c_uint32, 16)
    ]


class DSC_PICTURE_PARAMETER_SET_2(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_2_FIELDS),
        ("asUint", ctypes.c_uint32) ]

