import ctypes

'''
Register instance and offset 
'''
PPS0_0_A = 0x78070
PPS0_1_A = 0x78170
PPS0_0_B = 0x78270
PPS0_1_B = 0x78370
PPS0_0_C = 0x78470
PPS0_1_C = 0x78570
PPS0_0_D = 0x78670
PPS0_1_D = 0x78770

##
# @note  Source: https://gfxspecs.intel.com/Predator/Home/Index/50151
class DSC_PICTURE_PARAMETER_SET_0_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dsc_version_major", ctypes.c_uint32, 4),
        ("dsc_version_minor", ctypes.c_uint32, 4),
        ("bits_per_component", ctypes.c_uint32, 4),
        ("linebuf_depth", ctypes.c_uint32, 4),
        ("block_pred_enable", ctypes.c_uint32, 1),
        ("convert_rgb", ctypes.c_uint32, 1),
        ("enable_422", ctypes.c_uint32, 1),
        ("vbr_enable", ctypes.c_uint32, 1),
        ("alt_ich_select", ctypes.c_uint32, 1),
        ("reserved1", ctypes.c_uint32, 10),
        ("allow_double_buf_update_disable", ctypes.c_uint32, 1)
    ]

class DSC_PICTURE_PARAMETER_SET_0(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_PICTURE_PARAMETER_SET_0_FIELDS),
        ("asUint", ctypes.c_uint32) ]

