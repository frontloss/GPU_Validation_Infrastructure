##
# BSpec link https://gfxspecs.intel.com/Predator/Home/Index/53314

import ctypes

# Register instance and offset
TRANS_DP2_CTL_A = 0x600A0
TRANS_DP2_CTL_B = 0x610A0
TRANS_DP2_CTL_C = 0x620A0
TRANS_DP2_CTL_D = 0x630A0

# Register bitfield definition structure
class TransDP2CtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserve_1", ctypes.c_uint32, 23),  # 0 to 22
        ("dp2_debug", ctypes.c_uint32, 1),  # 23 to 23
        ("reserve_2", ctypes.c_uint32, 2),  # 24 to 25
        ("pr_bw_optimization", ctypes.c_uint32, 1),  # 26 to 26
        ("reserve_3", ctypes.c_uint32, 3),  # 27 to 29
        ("pr_enable", ctypes.c_uint32, 1),  # 30 to 30
        ("128b_132b_channel_coding", ctypes.c_uint32, 1),  # 31 to 31
    ]


class TRANS_DP2_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransDP2CtlReg),
        ("asUint", ctypes.c_uint32)
    ]
