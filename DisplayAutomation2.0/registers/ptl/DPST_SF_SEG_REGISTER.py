##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/69727

import ctypes

##
# Register instance and offset
DPST_SF_SEG_A = 0x490D4
DPST_SF_SEG_B = 0x491D4
DPST_SF_SEG_C = 0x492D4
DPST_SF_SEG_D = 0x493D4


##
# Register bitfield definition structure
class DpstSfSegReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("segment_size", ctypes.c_uint32, 16),               # 0 to 15
        ("segment_end", ctypes.c_uint32, 7),                 # 16 to 22
        ("reserved_23", ctypes.c_uint32, 1),                 # 23 to 23
        ("segment_start", ctypes.c_uint32, 7),               # 24 to 30
        ("reserved_31", ctypes.c_uint32, 1)                  # 31 to 31
    ]


class DPST_SF_SEG_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstSfSegReg),
        ("asUint", ctypes.c_uint32)
    ]
