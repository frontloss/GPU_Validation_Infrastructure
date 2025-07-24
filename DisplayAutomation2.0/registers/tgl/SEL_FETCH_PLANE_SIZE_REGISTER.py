##
# BSpec link: https://gfxspecs.intel.com/Predator/Home/Index/50415

import ctypes

# Register instance and offset
SEL_FETCH_PLANE_SIZE_1_A = 0x70898
SEL_FETCH_PLANE_SIZE_1_B = 0x70998
SEL_FETCH_PLANE_SIZE_2_A = 0x708B8
SEL_FETCH_PLANE_SIZE_2_B = 0x709B8
SEL_FETCH_PLANE_SIZE_3_A = 0x708D8
SEL_FETCH_PLANE_SIZE_3_B = 0x709D8
SEL_FETCH_PLANE_SIZE_4_A = 0x708F8
SEL_FETCH_PLANE_SIZE_4_B = 0x709F8
SEL_FETCH_PLANE_SIZE_5_A = 0x70928
SEL_FETCH_PLANE_SIZE_5_B = 0x70A28
SEL_FETCH_PLANE_SIZE_6_A = 0x70948
SEL_FETCH_PLANE_SIZE_7_A = 0x70968


# Register bitfield definition structure
class SelFetchPlaneSizeReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("width", ctypes.c_uint32, 13),  # 0 to 12
        ("reserved_13", ctypes.c_uint32, 3),  # 13 to 15
        ("height", ctypes.c_uint32, 13),  # 16 to 28
        ("reserved_29", ctypes.c_uint32, 3),  # 29 to 31
    ]

class SEL_FETCH_PLANE_SIZE_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SelFetchPlaneSizeReg),
        ("asUint", ctypes.c_uint32)
    ]