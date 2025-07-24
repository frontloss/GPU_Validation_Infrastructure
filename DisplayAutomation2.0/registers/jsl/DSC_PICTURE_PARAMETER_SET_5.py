import ctypes

'''
Register instance and offset 
'''
PPS5_0_A = 0x6B214
PPS5_1_A = 0x6BA14
PPS5_0_B = 0x78284
PPS5_1_B = 0x78384
PPS5_0_C = 0x78484
PPS5_1_C = 0x78584


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_5_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("scale_increment_interval", ctypes.c_uint32, 16),
        ("scale_decrement_interval", ctypes.c_uint32, 12),
        ("reserved4", ctypes.c_uint32, 4)
    ]


class DSC_PICTURE_PARAMETER_SET_5(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_5_FIELDS),
        ("asUint", ctypes.c_uint32) ]

