##
# BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/50402
import ctypes

# Register instance and offset
SEL_FETCH_PLANE_POS_1_A = 0x70894
SEL_FETCH_PLANE_POS_2_A = 0x708B4
SEL_FETCH_PLANE_POS_3_A = 0x708D4
SEL_FETCH_PLANE_POS_4_A = 0x708F4
SEL_FETCH_PLANE_POS_5_A = 0x70924
SEL_FETCH_PLANE_POS_1_B = 0x71894
SEL_FETCH_PLANE_POS_2_B = 0x718B4
SEL_FETCH_PLANE_POS_3_B = 0x718D4
SEL_FETCH_PLANE_POS_4_B = 0x718F4
SEL_FETCH_PLANE_POS_5_B = 0x71924
SEL_FETCH_PLANE_POS_1_C = 0x72894
SEL_FETCH_PLANE_POS_2_C = 0x728B4
SEL_FETCH_PLANE_POS_3_C = 0x728D4
SEL_FETCH_PLANE_POS_4_C = 0x728F4
SEL_FETCH_PLANE_POS_5_C = 0x72924
SEL_FETCH_PLANE_POS_1_D = 0x73894
SEL_FETCH_PLANE_POS_2_D = 0x738B4
SEL_FETCH_PLANE_POS_3_D = 0x738D4
SEL_FETCH_PLANE_POS_4_D = 0x738F4
SEL_FETCH_PLANE_POS_5_D = 0x73924


# Register bitfield definition structure
class SelFetchPlanePosReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("x_position", ctypes.c_uint32, 13),  # 0 to 12
        ("reserved_13", ctypes.c_uint32, 3),  # 13 to 15
        ("y_position", ctypes.c_uint32, 13),  # 16 to 28
        ("reserved_29", ctypes.c_uint32, 3),  # 29 to 31
    ]


class SEL_FETCH_PLANE_POS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SelFetchPlanePosReg),
        ("asUint", ctypes.c_uint32)
    ]