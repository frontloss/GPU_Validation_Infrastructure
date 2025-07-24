##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/71014

import ctypes

##
# Register instance and offset

PR_ALPM_CTL_A = 0x60948
PR_ALPM_CTL_B = 0x61948


##
# Register bitfield definition structure
class PrAlpmCtlReg(ctypes.LittleEndianStructure):

    _fields_ = [
        ('adaptive_sync_sdp_position', ctypes.c_uint32, 2),  # 0 to 1
        ('reserved_2', ctypes.c_uint32, 2),  # 2 to 3
        ('as_sdp_transmission_disabled_in_active', ctypes.c_uint32, 1),  # 4 to 4
        ('rfb_update_control', ctypes.c_uint32, 1),  # 5 to 5
        ('allow_link_off_between_as_sdp_su', ctypes.c_uint32, 1),  # 6 to 6
        ('reserved_7', ctypes.c_uint32, 25)  # 7 to 31
    ]


class PR_ALPM_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PrAlpmCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
