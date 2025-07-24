##
# BSpec link https://gfxspecs.intel.com/Predator/Home/Index/71465
import ctypes

# Register instance and offset
SFF_CTL_A = 0x60918
SFF_CTL_B = 0x61918
SFF_CTL_C = 0x62918
SFF_CTL_D = 0x63918



# Register bitfield definition structure
class SffCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("sf_single_full_frame", ctypes.c_uint32, 1),  # 0
        ("reserved", ctypes.c_uint32, 30),  # 1 to 31
    ]


class SFF_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SffCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
