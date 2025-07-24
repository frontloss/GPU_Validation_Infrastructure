##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/67077

import ctypes

##
# Register instance and offset
CMTG_CLK_SEL = 0x46160


##
# Register bitfield definition structure
class CmtgClkSelReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 29),  # 0 to 28
        ("cmtg_a_clk_sel", ctypes.c_uint32, 3),  # 29 to 31
    ]


class CMTG_CLK_SEL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", CmtgClkSelReg),
        ("asUint", ctypes.c_uint32)
    ]
