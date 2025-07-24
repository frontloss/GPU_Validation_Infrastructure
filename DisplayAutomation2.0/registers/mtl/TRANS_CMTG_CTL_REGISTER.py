##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/49396

import ctypes

##
# Register instance and offset
TRANS_CMTG_CTL = 0x6FA88


##
# Register bitfield definition structure
class TransCmtgCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("db_vactive", ctypes.c_uint32, 1),  # 0 to 0.
        ("hold_pll_config", ctypes.c_uint32, 1),  # 1 to 1
        ("reserved1", ctypes.c_uint32, 11),  # 2 to 12
        ("te_mode", ctypes.c_uint32, 2),  # 13 to 14
        ("cmtg_mode", ctypes.c_uint32, 1),  # 15 to 15
        ("reserved2", ctypes.c_uint32, 7),  # 16 to 22
        ("cmtg_state", ctypes.c_uint32, 1),  # 23 to 23
        ("reserved2", ctypes.c_uint32, 7),  # 24 to 30
        ("cmtg_enable", ctypes.c_uint32, 1),  # 31 to 31
    ]


class TRANS_CMTG_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransCmtgCtlReg),
        ("asUint", ctypes.c_uint32)
    ]