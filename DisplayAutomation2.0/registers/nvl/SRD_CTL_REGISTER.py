##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/7723

import ctypes
 
##
# Register instance and offset
SRD_CTL_A = 0x60800
SRD_CTL_B = 0x61800
SRD_CTL_C = 0x62800
SRD_CTL_D = 0x63800

 
##
# Register bitfield definition structure
class SrdCtlReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("idle_frame", ctypes.c_uint32, 4),                     # 0 to 3.
        ("tp1_time", ctypes.c_uint32, 2),                       # 4 to 5
        ("tp4_time", ctypes.c_uint32, 2),                       # 6 to 7
        ("tp2_tp3_time", ctypes.c_uint32, 2),                   # 8 to 9
        ("crc_enable", ctypes.c_uint32, 1),                     # 10 to 10
        ("tp2_tp3_select", ctypes.c_uint32, 1),                 # 11 to 11
        ("skip_aux_on_exit", ctypes.c_uint32, 1),               # 12 to 12
        ("tps4_control", ctypes.c_uint32, 1),                   # 13 to 13
        ("reserved_14", ctypes.c_uint32, 2),                    # 14 to 15
        ("psr_entry_setup_frames", ctypes.c_uint32, 2),         # 16 to 17
        ("reserved_18", ctypes.c_uint32, 9),                    # 18 to 26
        ("link_ctrl", ctypes.c_uint32, 1),                      # 27 to 27
        ("reserved_28", ctypes.c_uint32, 3),                    # 28 to 30
        ("srd_enable", ctypes.c_uint32, 1),                     # 31 to 31
    ]

 
class SRD_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SrdCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
