##
# BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/50402
import ctypes

# Register instance and offset
SEL_FETCH_PLANE_POS_1_A = 0x70894
SEL_FETCH_PLANE_POS_1_B = 0x70994
SEL_FETCH_PLANE_POS_2_A = 0x708B4
SEL_FETCH_PLANE_POS_2_B = 0x709B4
SEL_FETCH_PLANE_POS_3_A = 0x708D4
SEL_FETCH_PLANE_POS_3_B = 0x709D4
SEL_FETCH_PLANE_POS_4_A = 0x708F4
SEL_FETCH_PLANE_POS_4_B = 0x709F4
SEL_FETCH_PLANE_POS_5_A = 0x70924
SEL_FETCH_PLANE_POS_5_B = 0x70A24
SEL_FETCH_PLANE_POS_6_A = 0x70944
SEL_FETCH_PLANE_POS_7_A = 0x70964


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