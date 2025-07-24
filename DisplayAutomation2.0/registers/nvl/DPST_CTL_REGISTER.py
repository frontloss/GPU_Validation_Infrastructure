##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/69720

import ctypes

##
# Register instance and offset
DPST_CTL_A = 0x490C0
DPST_CTL_B = 0x491C0
DPST_CTL_C = 0x492C0
DPST_CTL_D = 0x493C0


##
# Register bitfield definition structure
class DpstCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 7),                                 # 0 to 6
        ("allow_dsb_stall", ctypes.c_uint32, 1),                            # 7 to 7
        ("force_histogram_load", ctypes.c_uint32, 1),                       # 8 to 8
        ("reserved_9", ctypes.c_uint32, 4),                                 # 9 to 12
        ("enhancement_mode", ctypes.c_uint32, 2),                           # 13 to 14
        ("reserved_15", ctypes.c_uint32, 1),                                # 15 to 15
        ("guardband_interrupt_delay_counter", ctypes.c_uint32, 8),          # 16 to 23
        ("histogram_mode_select", ctypes.c_uint32, 1),                      # 24 to 24
        ("reserved_25", ctypes.c_uint32, 2),                                # 25 to 26
        ("ie_modification_table_enable", ctypes.c_uint32, 1),               # 27 to 27
        ("restore_dpst", ctypes.c_uint32, 1),                               # 28 to 28
        ("reserved_29", ctypes.c_uint32, 2),                                # 29 to 30
        ("ie_histogram_enable", ctypes.c_uint32, 1),                        # 31 to 31
    ]


class DPST_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DpstCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
