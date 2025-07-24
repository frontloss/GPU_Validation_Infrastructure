##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/71709

import ctypes

##
# Register instance and offset
DSC_SU_PARAMETER_SET_A = 0x78064
DSC_SU_PARAMETER_SET_1_A = 0x78164
DSC_SU_PARAMETER_SET_B = 0x78264
DSC_SU_PARAMETER_SET_1_B = 0x78364
DSC_SU_PARAMETER_SET_C = 0x78464
DSC_SU_PARAMETER_SET_1_C = 0x78564
DSC_SU_PARAMETER_SET_D = 0x78664
DSC_SU_PARAMETER_SET_1_D = 0x78764


##
# Register bitfield definition structure
class DscSuParameterSet(ctypes.LittleEndianStructure):
    _fields_ = [
        ('su_pic_height', ctypes.c_uint32, 16),   # 0 to 15
        ('su_slice_row_per_frame', ctypes.c_uint32, 16),  # 16 to 31
    ]


class DSC_SU_PARAMETER_SET_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DscSuParameterSet),
        ("asUint", ctypes.c_uint32)
    ]
