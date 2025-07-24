##
# BSpec link https://gfxspecs.intel.com/Predator/Home/Index/50424
import ctypes

# Register instance and offset
PSR2_MAN_TRK_CTL_A = 0x60910
PSR2_MAN_TRK_CTL_B = 0x61910
PSR2_MAN_TRK_CTL_C = 0x62910
PSR2_MAN_TRK_CTL_D = 0x63910


# Register bitfield definition structure
class Psr2ManTrkCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("su_region_end_address", ctypes.c_uint32, 13),  # 0 to 12
        ("sf_continuous_full_frame", ctypes.c_uint32, 1),  # 13 to 13
        ("sf_single_full_frame", ctypes.c_uint32, 1),  # 14 to 14
        ("reserved_1", ctypes.c_uint32, 1),  # 15 to 15
        ("su_region_start_address", ctypes.c_uint32, 13),  # 16 to 28
        ("reserved_2", ctypes.c_uint32, 1),  # 29 to 29
        ("allow_db_stall", ctypes.c_uint32, 1),  # 30 to 30
        ("sf_partial_frame_enable", ctypes.c_uint32, 1),  # 31 to 31
    ]


class PSR2_MAN_TRK_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", Psr2ManTrkCtlReg),
        ("asUint", ctypes.c_uint32)
    ]