import ctypes

'''
Register instance and offset 
'''
RC_BUF01_0_A = 0x6B234
RC_BUF01_1_A = 0x6BA34
RC_BUF01_0_B = 0x78258
RC_BUF01_1_B = 0x78358
RC_BUF01_0_C = 0x78458
RC_BUF01_1_C = 0x78558


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_BUF_THRESH_01_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_buf_thresh_4", ctypes.c_uint32, 8),
        ("rc_buf_thresh_5", ctypes.c_uint32, 8),
        ("rc_buf_thresh_6", ctypes.c_uint32, 8),
        ("rc_buf_thresh_7", ctypes.c_uint32, 8)
    ]


class DSC_RC_BUF_THRESH_01(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_BUF_THRESH_01_FIELDS),
        ("asUint", ctypes.c_uint32)]
