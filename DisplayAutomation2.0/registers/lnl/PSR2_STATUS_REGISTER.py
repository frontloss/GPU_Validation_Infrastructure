##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/7716

import ctypes
 
##
# Register instance and offset
PSR2_STATUS_A = 0x60940
PSR2_STATUS_B = 0x61940

 
##
# Register bitfield definition structure
class Psr2StatusReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("idle_frame_counter", ctypes.c_uint32, 4),                 # 0 to 3
        ("psr2_su_entry_completion", ctypes.c_uint32, 1),           # 4 to 4
        ("psr2_deep_sleep_entry_completion", ctypes.c_uint32, 1),   # 5 to 5
        ("reserved_6", ctypes.c_uint32, 2),                         # 6 to 7
        ("sending_tp2", ctypes.c_uint32, 1),                        # 8 to 8
        ("psr2_idle_frame_indication", ctypes.c_uint32, 1),         # 9 to 9
        ("idle_not_allowed", ctypes.c_uint32, 1),                   # 10 to 10
        ("as_sdp_trr_change", ctypes.c_uint32, 1),                   # 11 to 11
        ("as_sdp_transmission_enabled_in_pr_active", ctypes.c_uint32, 1),  # 12 to 12
        ("reserved_13", ctypes.c_uint32, 3),                         # 13 to 15
        ("psr2_deep_sleep_entry_count", ctypes.c_uint32, 4),        # 16 to 19
        ("psr2_pr_state", ctypes.c_uint32, 3),                      # 20 to 22
        ("reserved_23", ctypes.c_uint32, 3),                        # 23 to 25
        ("link_status", ctypes.c_uint32, 2),                        # 26 to 27
        ("psr2_state", ctypes.c_uint32, 4),                         # 28 to 31
    ]

 
class PSR2_STATUS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", Psr2StatusReg),
        ("asUint", ctypes.c_uint32)
    ]
