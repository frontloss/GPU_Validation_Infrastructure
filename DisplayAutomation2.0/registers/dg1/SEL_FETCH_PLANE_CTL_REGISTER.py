##
# BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/50420
import ctypes

# Register instance and offset
SEL_FETCH_PLANE_CTL_1_A = 0x70890
SEL_FETCH_PLANE_CTL_1_B = 0x70990
SEL_FETCH_PLANE_CTL_2_A = 0x708B0
SEL_FETCH_PLANE_CTL_2_B = 0x709B0
SEL_FETCH_PLANE_CTL_3_A = 0x708D0
SEL_FETCH_PLANE_CTL_3_B = 0x709D0
SEL_FETCH_PLANE_CTL_4_A = 0x708F0
SEL_FETCH_PLANE_CTL_4_B = 0x709F0
SEL_FETCH_PLANE_CTL_5_A = 0x70920
SEL_FETCH_PLANE_CTL_5_B = 0x70A20
SEL_FETCH_PLANE_CTL_6_A = 0x70940
SEL_FETCH_PLANE_CTL_7_A = 0x70960


# Register bitfield definition structure
class SelFetchPlaneCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 31),  # 0 to 30
        ("selective_fetch_plane_enable", ctypes.c_uint32, 1),  # 31 to 31
    ]


class SEL_FETCH_PLANE_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SelFetchPlaneCtlReg),
        ("asUint", ctypes.c_uint32)
    ]