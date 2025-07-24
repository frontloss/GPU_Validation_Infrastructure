##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/7713

import ctypes
 
##
# Register instance and offset
PSR2_CTL_A = 0x60900
PSR2_CTL_B = 0x61900
PSR2_CTL_C = 0x62900
PSR2_CTL_D = 0x63900
PSR2_CTL_EDP = 0x6F900

 
##
# Register bitfield definition structure
class Psr2CtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("idle_frame", ctypes.c_uint32, 4),                                 # 0 to 3.
        ("frame_before_su_entry", ctypes.c_uint32, 4),                      # 4 to 7
        ("tp2_time", ctypes.c_uint32, 2),                                   # 8 to 9
        ("reserved_1", ctypes.c_uint32, 1),                                 # 10 to 10
        ("fast_wake", ctypes.c_uint32, 2),                                  # 11 to 12
        ("io_buffer_wake", ctypes.c_uint32, 2),                             # 13 to 14
        ("reserved_5", ctypes.c_uint32, 5),                                 # 15 to 19
        ("max_su_disable_time", ctypes.c_uint32, 5),                        # 20 to 24
        ("y_coordinate_enable", ctypes.c_uint32, 1),                        # 25 to 25
        ("y_coordinate_valid", ctypes.c_uint32, 1),                         # 26 to 26
        ("reserved_2", ctypes.c_uint32, 2),                                 # 27 to 28
        ("context_restore_to_psr2_deep_sleep_state", ctypes.c_uint32, 1),   # 29 to 29
        ("selective_update_tracking_enable", ctypes.c_uint32, 1),           # 30 to 30
        ("psr2_enable", ctypes.c_uint32, 1),                                # 31 to 31
    ]

 
class PSR2_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      Psr2CtlReg),
        ("asUint", ctypes.c_uint32)
    ]
