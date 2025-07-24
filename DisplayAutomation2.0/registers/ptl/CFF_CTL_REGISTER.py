##
# BSpec link https://gfxspecs.intel.com/Predator/Home/Index/71466
import ctypes

# Register instance and offset
CFF_CTL_A = 0x6091C
CFF_CTL_B = 0x6191C
CFF_CTL_C = 0x6291C
CFF_CTL_D = 0x6391C


# Register bitfield definition structure
class CffCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("sf_continuous_full_frame", ctypes.c_uint32, 1),  # 0
        ("reserved", ctypes.c_uint32, 31),  # 1 to 31
    ]


class CFF_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", CffCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
