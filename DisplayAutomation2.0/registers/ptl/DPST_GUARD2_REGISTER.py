##
# BSpec Link:   https://gfxspecs.intel.com/Predator/Home/Index/72191

import ctypes
 
##
# Register instance and offset
DPST_GUARD2_A = 0x490EC
DPST_GUARD2_B = 0x491EC
DPST_GUARD2_C = 0x492EC
DPST_GUARD2_D = 0x493EC


##
# Register bitfield definition structure
class DpstGuard2Reg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("high_threshold_guardband", ctypes.c_uint32, 31),  # 0 to 30
        ("high_threshold_enable", ctypes.c_uint32, 1),      # 31
    ]


class DPST_GUARD2_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstGuard2Reg),
        ("asUint", ctypes.c_uint32)
    ]
