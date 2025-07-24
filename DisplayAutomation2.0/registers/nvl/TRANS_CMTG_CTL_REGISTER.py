##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/69088

import ctypes

##
# Register instance and offset
TRANS_CMTG_CTL_A = 0x6FA88
TRANS_CMTG_CTL_B = 0x6FB88


##
# Register bitfield definition structure
class TransCmtgCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("db_vactive", ctypes.c_uint32, 1),  # 0 to 0.
        ("hold_pll_config", ctypes.c_uint32, 1),  # 1 to 1
        ("reserved_2", ctypes.c_uint32, 21),  # 2 to 22
        ("cmtg_state", ctypes.c_uint32, 1),  # 23 to 23
        ("reserved2", ctypes.c_uint32, 5),  # 24 to 28
        ("cmtg_sync_to_port", ctypes.c_uint32, 1),  # 29 to 29
        ("cmtg_configuration", ctypes.c_uint32, 1),  # 30 to 30
        ("cmtg_enable", ctypes.c_uint32, 1),  # 31 to 31
    ]


class TRANS_CMTG_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", TransCmtgCtlReg),
        ("asUint", ctypes.c_uint32)
    ]