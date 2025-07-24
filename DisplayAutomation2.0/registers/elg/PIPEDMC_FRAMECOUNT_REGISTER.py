##
# BSpec link https://gfxspecs.intel.com/Predator/Home/Index/67586
import ctypes
 
##
# Register instance and offset
PIPEDMC_FRAMECOUNT_CMTG_A = 0x5F148
PIPEDMC_FRAMECOUNT_CMTG_B = 0x5F548
PIPEDMC_FRAMECOUNT_CMTG_C = 0x5F948
PIPEDMC_FRAMECOUNT_CMTG_D = 0x5FD48


##
# Register bitfield definition structure
class PipeDmcFrameCountReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("frame_count", ctypes.c_uint32, 32)                         # 0 to 31
    ]


class PIPEDMC_FRAMECOUNT_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PipeDmcFrameCountReg),
        ("asUint", ctypes.c_uint32)
    ]
