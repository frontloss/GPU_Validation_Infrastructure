##
# Bspec link: https://gfxspecs.intel.com/Predator/Home/Index/69722

import ctypes

##
# Register instance and offset
DPST_HIST_BIN_A = 0x490C4
DPST_HIST_BIN_B = 0x491C4
DPST_HIST_BIN_C = 0x492C4
DPST_HIST_BIN_D = 0x493C4


##
# Register bitfield definition structure
class DpstHistBinReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("data", ctypes.c_uint32, 28),  # 0 to 27
        ("reserved", ctypes.c_uint32, 3),  # 28 to 30
        ("busy_bit", ctypes.c_uint32, 1),  # 31
    ]


class DPST_HIST_BIN_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstHistBinReg),
        ("asUint", ctypes.c_uint32)
    ]
