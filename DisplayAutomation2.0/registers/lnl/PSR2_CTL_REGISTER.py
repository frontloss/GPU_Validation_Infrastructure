##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/7713

import ctypes
 
##
# Register instance and offset
PSR2_CTL_A = 0x60900
PSR2_CTL_B = 0x61900

 
##
# Register bitfield definition structure
class Psr2CtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("idle_frame", ctypes.c_uint32, 4),                                 # 0 to 3.
        ("frame_before_su_entry", ctypes.c_uint32, 4),                      # 4 to 7
        ("tp2_time", ctypes.c_uint32, 2),                                   # 8 to 9
        ("fast_wake", ctypes.c_uint32, 3),                                  # 10 to 12
        ("io_buffer_wake", ctypes.c_uint32, 6),                             # 13 to 18
        ("reserved_19", ctypes.c_uint32, 1),                                # 19 to 19
        ('max_su_disable_time', ctypes.c_uint32, 5),                        # 20 to 24
        ('su_sdp_scanline_indication', ctypes.c_uint32, 1),                 # 25 to 25
        ('reserved_26', ctypes.c_uint32, 1),                                # 26 to 26
        ('enable_early_transport', ctypes.c_uint32, 1),                     # 27 to 27
        ('reserved_28', ctypes.c_uint32, 1),                                # 28 to 28
        ('context_restore_to_psr2_deep_sleep_state', ctypes.c_uint32, 1),   # 29 to 29
        ('restore_to_sleep', ctypes.c_uint32, 1),                           # 30 to 30
        ("psr2_enable", ctypes.c_uint32, 1),                                # 31 to 31
    ]

 
class PSR2_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      Psr2CtlReg),
        ("asUint", ctypes.c_uint32)
    ]
