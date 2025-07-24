##
# BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/50399
import ctypes

# Register instance and offset
SEL_FETCH_PLANE_OFFSET_1_A = 0x7089C
SEL_FETCH_PLANE_OFFSET_2_A = 0x708BC
SEL_FETCH_PLANE_OFFSET_3_A = 0x708DC
SEL_FETCH_PLANE_OFFSET_4_A = 0x708FC
SEL_FETCH_PLANE_OFFSET_5_A = 0x7092C
SEL_FETCH_PLANE_OFFSET_1_B = 0x7189C
SEL_FETCH_PLANE_OFFSET_2_B = 0x718BC
SEL_FETCH_PLANE_OFFSET_3_B = 0x718DC
SEL_FETCH_PLANE_OFFSET_4_B = 0x718FC
SEL_FETCH_PLANE_OFFSET_5_B = 0x7192C
SEL_FETCH_PLANE_OFFSET_1_C = 0x7289C
SEL_FETCH_PLANE_OFFSET_2_C = 0x728BC
SEL_FETCH_PLANE_OFFSET_3_C = 0x728DC
SEL_FETCH_PLANE_OFFSET_4_C = 0x728FC
SEL_FETCH_PLANE_OFFSET_5_C = 0x7292C
SEL_FETCH_PLANE_OFFSET_1_D = 0x7389C
SEL_FETCH_PLANE_OFFSET_2_D = 0x738BC
SEL_FETCH_PLANE_OFFSET_3_D = 0x738DC
SEL_FETCH_PLANE_OFFSET_4_D = 0x738FC
SEL_FETCH_PLANE_OFFSET_5_D = 0x7392C


# Register bitfield definition structure
class SelFetchPlaneOffsetReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("start_x_position", ctypes.c_uint32, 16),  # 0 to 15
        ("start_y_position", ctypes.c_uint32, 16),  # 16 to 31
    ]


class SEL_FETCH_PLANE_OFFSET_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SelFetchPlaneOffsetReg),
        ("asUint", ctypes.c_uint32)
    ]
