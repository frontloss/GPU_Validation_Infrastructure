##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/70294

import ctypes

##
# Register instance and offset
ALPM_CTL_A = 0x60950
ALPM_CTL_B = 0x61950


##
# Register bitfield definition structure
class AlpmCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ('aux_less_wake_time', ctypes.c_uint32, 6),  # 0 to 5
        ('reserved_6', ctypes.c_uint32, 2),   # 6 to 7
        ('extended_fast_wake_time', ctypes.c_uint32, 6),  # 8 to 13
        ('reserved_14', ctypes.c_uint32, 2),  # 14 to 15
        ('alpm_entry_check', ctypes.c_uint32, 4),  # 16 to 19
        ('aux_wake_sleep_hold_enable', ctypes.c_uint32, 1),  # 20 to 20
        ('aux_less_sleep_hold_time', ctypes.c_uint32, 3),  # 21 to 23
        ('restore_to_deep_sleep', ctypes.c_uint32, 1),  # 24 to 24
        ('restore_to_sleep', ctypes.c_uint32, 1),  # 25 to 25
        ('reserved_26', ctypes.c_uint32, 2),  # 26 to 27
        ('extended_fast_wake_enable', ctypes.c_uint32, 1),  # 28 to 28
        ('link_Off_between_frames_enable', ctypes.c_uint32, 1),  # 29 to 29
        ('alpm_aux_less_enable', ctypes.c_uint32, 1),  # 30 to 30
        ('alpm_enable', ctypes.c_uint32, 1),  # 31 to 31
    ]


class ALPM_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", AlpmCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
