import ctypes

'''
Register instance and offset 
'''
RC_BUF00_0_A = 0x78054
RC_BUF00_1_A = 0x78154
RC_BUF00_2_A = 0x78854
RC_BUF00_0_B = 0x78254
RC_BUF00_1_B = 0x78354
RC_BUF00_2_B = 0x78954
RC_BUF00_0_C = 0x78454
RC_BUF00_1_C = 0x78554
RC_BUF00_2_C = 0x78A54
RC_BUF00_0_D = 0x78654
RC_BUF00_1_D = 0x78754
RC_BUF00_2_D = 0x78B54

##
# @note    Source: https://gfxspecs.intel.com/Predator/Home/Index/50161
class DSC_RC_BUF_THRESH_00_FIELDS(ctypes.LittleEndianStructure):
    _fields_ = [
        ("rc_buf_thresh_0", ctypes.c_uint32, 8),
        ("rc_buf_thresh_1", ctypes.c_uint32, 8),
        ("rc_buf_thresh_2", ctypes.c_uint32, 8),
        ("rc_buf_thresh_3", ctypes.c_uint32, 8)
    ]


class DSC_RC_BUF_THRESH_00(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSC_RC_BUF_THRESH_00_FIELDS),
        ("asUint", ctypes.c_uint32)
    ]
