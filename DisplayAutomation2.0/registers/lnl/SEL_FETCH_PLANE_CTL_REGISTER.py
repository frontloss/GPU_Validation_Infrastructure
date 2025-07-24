##
# BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/50420
import ctypes

# Register instance and offset

SEL_FETCH_PLANE_CTL_1_A = 0x70890
SEL_FETCH_PLANE_CTL_2_A = 0x708B0
SEL_FETCH_PLANE_CTL_3_A = 0x708D0
SEL_FETCH_PLANE_CTL_4_A = 0x708F0
SEL_FETCH_PLANE_CTL_5_A = 0x70920
SEL_FETCH_PLANE_CTL_1_B = 0x71890
SEL_FETCH_PLANE_CTL_2_B = 0x718B0
SEL_FETCH_PLANE_CTL_3_B = 0x718D0
SEL_FETCH_PLANE_CTL_4_B = 0x718F0
SEL_FETCH_PLANE_CTL_5_B = 0x71920
SEL_FETCH_PLANE_CTL_1_C = 0x72890
SEL_FETCH_PLANE_CTL_2_C = 0x728B0
SEL_FETCH_PLANE_CTL_3_C = 0x728D0
SEL_FETCH_PLANE_CTL_4_C = 0x728F0
SEL_FETCH_PLANE_CTL_5_C = 0x72920
SEL_FETCH_PLANE_CTL_1_D = 0x73890
SEL_FETCH_PLANE_CTL_2_D = 0x738B0
SEL_FETCH_PLANE_CTL_3_D = 0x738D0
SEL_FETCH_PLANE_CTL_4_D = 0x738F0
SEL_FETCH_PLANE_CTL_5_D = 0x73920


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