##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/69726

import ctypes

##
# Register instance and offset
DPST_SF_CTL_A = 0x490D0
DPST_SF_CTL_B = 0x491D0
DPST_SF_CTL_C = 0x492D0
DPST_SF_CTL_D = 0x493D0


##
# Register bitfield definition structure
class DpstSfCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 27),                                # 0 to 26
        ("bypass_arming", ctypes.c_uint32, 1),                              # 27 to 27
        ("reserved_28", ctypes.c_uint32, 3),                                # 28 to 30
        ("selective_fetch_enable", ctypes.c_uint32, 1)                      # 31 to 31
    ]


class DPST_SF_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstSfCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
