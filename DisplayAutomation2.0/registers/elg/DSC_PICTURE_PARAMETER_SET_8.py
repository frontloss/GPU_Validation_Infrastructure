import ctypes

'''
Register instance and offset 
'''
PPS8_0_A = 0x78090
PPS8_1_A = 0x78190
PPS8_2_A = 0x78890
PPS8_0_B = 0x78290
PPS8_1_B = 0x78390
PPS8_2_B = 0x78990
PPS8_0_C = 0x78490
PPS8_1_C = 0x78590
PPS8_2_C = 0x78A90
PPS8_0_D = 0x78690
PPS8_1_D = 0x78790
PPS8_2_D = 0x78B90

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_PICTURE_PARAMETER_SET_8_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("final_offset", ctypes.c_uint32, 16),
        ("initial_offset", ctypes.c_uint32, 16)
    ]


class DSC_PICTURE_PARAMETER_SET_8(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_8_FIELDS),
        ("asUint", ctypes.c_uint32) ]
