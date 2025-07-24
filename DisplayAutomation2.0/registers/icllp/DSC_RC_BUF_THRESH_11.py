import ctypes

'''
Register instance and offset 
'''
RC_BUF11_0_A = 0x6B23C
RC_BUF11_1_A = 0x6BA3C
RC_BUF11_0_B = 0x78260
RC_BUF11_1_B = 0x78360
RC_BUF11_0_C = 0x78460
RC_BUF11_1_C = 0x78560


##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_BUF_THRESH_11_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_buf_thresh_12", ctypes.c_uint32, 8),
        ("rc_buf_thresh_13", ctypes.c_uint32, 8)
    ]


class DSC_RC_BUF_THRESH_11(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_BUF_THRESH_11_FIELDS),
        ("asUint", ctypes.c_uint32)]
