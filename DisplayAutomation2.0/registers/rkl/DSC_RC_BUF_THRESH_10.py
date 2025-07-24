import ctypes

'''
Register instance and offset 
'''
RC_BUF10_0_A = 0x7805C
RC_BUF10_1_A = 0x7815C
RC_BUF10_0_B = 0x7825C
RC_BUF10_1_B = 0x7835C
RC_BUF10_0_C = 0x7845C
RC_BUF10_1_C = 0x7855C

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_BUF_THRESH_10_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_buf_thresh_8", ctypes.c_uint32, 8),
        ("rc_buf_thresh_9", ctypes.c_uint32, 8),
        ("rc_buf_thresh_10", ctypes.c_uint32, 8),
        ("rc_buf_thresh_11", ctypes.c_uint32, 8)
    ]


class DSC_RC_BUF_THRESH_10(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_BUF_THRESH_10_FIELDS),
        ("asUint", ctypes.c_uint32)]
