##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/70135

import ctypes

##
# Register instance and offset
DPST_PROG_COEF_A = 0x490E0
DPST_PROG_COEF_B = 0x491E0
DPST_PROG_COEF_C = 0x492E0
DPST_PROG_COEF_D = 0x493E0


##
# Register bitfield definition structure
class DpstProgCoefReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("blue_coefficient", ctypes.c_uint32, 9),           # 0 to 8
        ("reserved_9", ctypes.c_uint32, 1),                 # 9 to 9
        ("green_coefficient", ctypes.c_uint32, 9),          # 10 to 18
        ("reserved_19", ctypes.c_uint32, 1),                # 19 to 19
        ("red_coefficient", ctypes.c_uint32, 9),            # 20 to 28
        ("reserved_29", ctypes.c_uint32, 3)                 # 29 to 31
    ]


class DPST_PROG_COEF_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstProgCoefReg),
        ("asUint", ctypes.c_uint32)
    ]
