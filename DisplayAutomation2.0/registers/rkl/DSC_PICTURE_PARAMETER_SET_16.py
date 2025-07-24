import ctypes

'''
Register instance and offset 
'''
PPS16_0_A = 0x780B0
PPS16_1_A = 0x781B0
PPS16_0_B = 0x782B0
PPS16_1_B = 0x783B0
PPS16_0_C = 0x784B0
PPS16_1_C = 0x785B0


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_16_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("slice_chunk_size", ctypes.c_uint32, 16),
        ("slice_per_line", ctypes.c_uint32, 3),
        ("reserved13", ctypes.c_uint32, 1),
        ("slice_row_per_frame", ctypes.c_uint32, 12)
    ]


class DSC_PICTURE_PARAMETER_SET_16(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_16_FIELDS),
        ("asUint", ctypes.c_uint32)]
