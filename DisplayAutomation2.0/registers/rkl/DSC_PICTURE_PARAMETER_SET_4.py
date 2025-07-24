import ctypes

'''
Register instance and offset 
'''
PPS4_0_A = 0x78080
PPS4_1_A = 0x78180
PPS4_0_B = 0x78280
PPS4_1_B = 0x78380
PPS4_0_C = 0x78480
PPS4_1_C = 0x78580


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_4_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("initial_xmit_delay", ctypes.c_uint32, 10),
        ("reserved3", ctypes.c_uint32, 6),
        ("initial_dec_delay", ctypes.c_uint32, 16)
    ]


class DSC_PICTURE_PARAMETER_SET_4(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_4_FIELDS),
        ("asUint", ctypes.c_uint32) ]

