##
# BSpec Link: https://gfxspecs.intel.com/Predator/Home/Index/7726

import ctypes
 
##
# Register instance and offset
SRD_STATUS_A = 0x60840
SRD_STATUS_B = 0x61840
SRD_STATUS_C = 0x62840
SRD_STATUS_D = 0x63840
SRD_STATUS_EDP = 0x6F840

 
##
# Register bitfield definition structure
class SrdStatusReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ("idle_frame_counter", ctypes.c_uint32, 4),             # 0 to 3
        ("sending_tp1", ctypes.c_uint32, 1),                    # 4 to 4
        ("reserved_2", ctypes.c_uint32, 2),                     # 5 to 6
        ("sending_tp4", ctypes.c_uint32, 1),                     # 7 to 7
        ("sending_tp2_tp3", ctypes.c_uint32, 1),                # 8 to 8
        ("sending_idle", ctypes.c_uint32, 1),                   # 9 to 9
        ("reserved_2", ctypes.c_uint32, 2),                     # 10 to 11
        ("sending_aux", ctypes.c_uint32, 1),                    # 12 to 12
        ("reserved_2", ctypes.c_uint32, 2),                     # 13 to 14
        ("aux_error", ctypes.c_uint32, 1),                      # 15 to 15
        ("srd_entry_count", ctypes.c_uint32, 4),                # 16 to 19
        ("max_sleep_time_counter", ctypes.c_uint32, 5),         # 20 to 24
        ("reserved_1", ctypes.c_uint32, 1),                     # 25 to 25
        ("link_status", ctypes.c_uint32, 2),                    # 26 to 27
        ("reserved_1", ctypes.c_uint32, 1),                     # 28 to 28
        ("srd_state", ctypes.c_uint32, 3),                      # 29 to 31
    ]

 
class SRD_STATUS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SrdStatusReg),
        ("asUint", ctypes.c_uint32)
    ]
