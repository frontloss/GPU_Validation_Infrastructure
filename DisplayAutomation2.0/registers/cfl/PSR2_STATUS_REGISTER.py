##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/7716

import ctypes
 
##
# Register instance and offset
PSR2_STATUS_EDP = 0x6F940

 
##
# Register bitfield definition structure
class Psr2StatusReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("idle_frame_counter", ctypes.c_uint32, 4),                 # 0 to 3
        ("psr2_su_entry_completion", ctypes.c_uint32, 1),           # 4 to 4
        ("psr2_deep_sleep_entry_completion", ctypes.c_uint32, 1),   # 5 to 5
        ("psr2_block_fifo_under_run", ctypes.c_uint32, 1),          # 6 to 6
        ("psr2_su_fifo_under_run", ctypes.c_uint32, 1),             # 7 to 7
        ("sending_tp2", ctypes.c_uint32, 1),                        # 8 to 8
        ("reserved_1", ctypes.c_uint32, 1),                         # 9 to 9
        ("reserved_6", ctypes.c_uint32, 6),                         # 10 to 15
        ("psr2_deep_sleep_entry_count", ctypes.c_uint32, 4),        # 16 to 19
        ("max_sleep_time_counter", ctypes.c_uint32, 5),             # 20 to 24
        ("reserved_1", ctypes.c_uint32, 1),                         # 25 to 25
        ("link_status", ctypes.c_uint32, 2),                        # 26 to 27
        ("psr2_state", ctypes.c_uint32, 4),                         # 28 to 31
    ]

 
class PSR2_STATUS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", Psr2StatusReg),
        ("asUint", ctypes.c_uint32)
    ]
