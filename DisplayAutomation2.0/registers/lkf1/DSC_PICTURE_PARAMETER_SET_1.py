import ctypes

'''
Register instance and offset 
'''
PPS1_0_A = 0x78074
PPS1_1_A = 0x78174
PPS1_0_B = 0x78274
PPS1_1_B = 0x78374
PPS1_0_C = 0x78474
PPS1_1_C = 0x78574
PPS1_0_D = 0x78674
PPS1_1_D = 0x78774

##
# @note  Source: https://gfxspecs.intel.com/Predator/Home/Index/50152
class DSC_PICTURE_PARAMETER_SET_1_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("bits_per_pixel", ctypes.c_uint32, 10),
        ("reserved_10", ctypes.c_uint32, 22)
    ]


class DSC_PICTURE_PARAMETER_SET_1(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_1_FIELDS),
        ("asUint", ctypes.c_uint32) ]

