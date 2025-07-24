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
        ("allow_double_buffer_update_disable", ctypes.c_uint32, 1),  # 0 to 0
        ("sf_partial_frame_enable", ctypes.c_uint32, 1),  # 1 to 1
        ("sf_continuous_full_frame", ctypes.c_uint32, 1),  # 2 to 2
        ("sf_single_full_frame", ctypes.c_uint32, 1),  # 3 to 3
        ("reserved_4", ctypes.c_uint32, 7),  # 4 to 10
        ("su_region_end_address", ctypes.c_uint32, 10),  # 11 to 20
        ("su_region_start_address", ctypes.c_uint32, 10),  # 21 to 30
        ("psr2_manual_tracking_enable", ctypes.c_uint32, 1),  # 31 to 31
    ]


class PSR2_MAN_TRK_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", Psr2ManTrkCtlReg),
        ("asUint", ctypes.c_uint32)
    ]