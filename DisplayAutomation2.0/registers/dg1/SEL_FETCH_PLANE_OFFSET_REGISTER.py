##
# BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/50399
import ctypes

# Register instance and offset
SEL_FETCH_PLANE_OFFSET_1_A = 0x7089C
SEL_FETCH_PLANE_OFFSET_1_B = 0x7099C
SEL_FETCH_PLANE_OFFSET_2_A = 0x708BC
SEL_FETCH_PLANE_OFFSET_2_B = 0x709BC
SEL_FETCH_PLANE_OFFSET_3_A = 0x708DC
SEL_FETCH_PLANE_OFFSET_3_B = 0x709DC
SEL_FETCH_PLANE_OFFSET_4_A = 0x708FC
SEL_FETCH_PLANE_OFFSET_4_B = 0x709FC
SEL_FETCH_PLANE_OFFSET_5_A = 0x7092C
SEL_FETCH_PLANE_OFFSET_5_B = 0x70A2C
SEL_FETCH_PLANE_OFFSET_6_A = 0x7094C
SEL_FETCH_PLANE_OFFSET_7_A = 0x7096C


# Register bitfield definition structure
class SelFetchPlaneOffsetReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("start_x_position", ctypes.c_uint32, 13),  # 0 to 12
        ("reserved_13", ctypes.c_uint32, 3),  # 13 to 15
        ("start_y_position", ctypes.c_uint32, 13),  # 16 to 28
        ("reserved_29", ctypes.c_uint32, 3),  # 29 to 31
    ]


class SEL_FETCH_PLANE_OFFSET_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SelFetchPlaneOffsetReg),
        ("asUint", ctypes.c_uint32)
    ]
