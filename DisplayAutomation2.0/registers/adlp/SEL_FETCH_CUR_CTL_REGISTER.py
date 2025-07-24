##
# BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/50371
import ctypes

# Register instance and offset
SEL_FETCH_CUR_CTL_A = 0x70880
SEL_FETCH_CUR_CTL_B = 0x71880
SEL_FETCH_CUR_CTL_C = 0x72880
SEL_FETCH_CUR_CTL_D = 0x73880


# Register bitfield definition structure
class SelFetchCurCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("cursor_mode_select", ctypes.c_uint32, 6),  # 0 to 5
        ("reserved_6", ctypes.c_uint32, 2),  # 6 to 7
        ("force_alpha_value", ctypes.c_uint32, 2),  # 8 to 9
        ("force_alpha_plane_select", ctypes.c_uint32, 2),  # 10 to 11
        ("reserved_12", ctypes.c_uint32, 3),  # 12 to 14
        ("180_rotation", ctypes.c_uint32, 1),  # 15 to 15
        ("csc_enable", ctypes.c_uint32, 1),  # 16 to 16
        ("reserved_17", ctypes.c_uint32, 1),  # 17 to 17
        ("pre_csc_gamma_enable", ctypes.c_uint32, 1),  # 18 to 18
        ("reserved_19", ctypes.c_uint32, 4),  # 19 to 22
        ("allow_double_buffer_update_disable", ctypes.c_uint32, 1),  # 23 to 23
        ("pipe_csc_enable", ctypes.c_uint32, 1),  # 24 to 24
        ("reserved_25", ctypes.c_uint32, 1),  # 25 to 25
        ("gamma_enable", ctypes.c_uint32, 1),  # 26 to 26
        ("reserved_27", ctypes.c_uint32, 1),  # 27 to 27
        ("pipe_slice_arbitration_slots", ctypes.c_uint32, 3),  # 28 to 30
        ("reserved_31", ctypes.c_uint32, 1),  # 31 to 31
    ]


class SEL_FETCH_CUR_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SelFetchCurCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
