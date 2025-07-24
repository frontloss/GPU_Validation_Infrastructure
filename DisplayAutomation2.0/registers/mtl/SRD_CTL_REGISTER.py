##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/7723

import ctypes
 
##
# Register instance and offset
SRD_CTL_A = 0x60800
SRD_CTL_B = 0x61800
SRD_CTL_C = 0x62800
SRD_CTL_D = 0x63800
SRD_CTL_EDP = 0x6F800

 
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
        ("dsc_crc_last_byte", ctypes.c_uint32, 3),              # 14 to 16
        ("reserved_3", ctypes.c_uint32, 3),                     # 17 to 19
        ("max_sleep_time", ctypes.c_uint32, 5),                 # 20 to 24
        ("reserved_2", ctypes.c_uint32, 2),                     # 25 to 26
        ("link_ctrl", ctypes.c_uint32, 1),                      # 27 to 27
        ("adaptive_sync_frame_update", ctypes.c_uint32, 1),     # 28 to 28
        ("context_restore_to_psr_active", ctypes.c_uint32, 1),  # 29 to 29
        ("single_frame_update_enable", ctypes.c_uint32, 1),     # 30 to 30
        ("srd_enable", ctypes.c_uint32, 1),                     # 31 to 31
    ]

 
class SRD_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SrdCtlReg),
        ("asUint", ctypes.c_uint32)
    ]
