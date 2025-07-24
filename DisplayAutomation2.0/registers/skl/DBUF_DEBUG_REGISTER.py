import ctypes
 
'''
Register instance and offset 
'''
DBUF_DEBUG = 0x45014 
DBUF_DEBUG_S1 = 0x45014 
DBUF_DEBUG_S2 = 0x44FF4 

 
'''
Register field expected values 
'''
bypass_read_ecc_BYPASS = 0b1 
bypass_read_ecc_DO_NOT_BYPASS = 0b0 
clear_all_trackers_CLEAR = 0b1 
clear_all_trackers_DO_NOT_CLEAR = 0b0 
clear_pipe_a_trackers_CLEAR = 0b1 
clear_pipe_a_trackers_DO_NOT_CLEAR = 0b0 
clear_pipe_b_trackers_CLEAR = 0b1 
clear_pipe_b_trackers_DO_NOT_CLEAR = 0b0 
clear_pipe_c_trackers_CLEAR = 0b1 
clear_pipe_c_trackers_DO_NOT_CLEAR = 0b0 
clear_pipe_d_trackers_CLEAR = 0b1 
clear_pipe_d_trackers_DO_NOT_CLEAR = 0b0 
global_clear_all_CLEAR = 0b1 
global_clear_all_DO_NOT_CLEAR = 0b0 
reset_packetization_sm_DO_NOT_RESET = 0b0 
reset_packetization_sm_RESET = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DBUF_DEBUG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("clear_all_trackers"    , ctypes.c_uint32, 1), # 0 to 0 
        ("spare_1"               , ctypes.c_uint32, 1), # 1 to 1 
        ("reset_packetization_sm" , ctypes.c_uint32, 1), # 2 to 2 
        ("global_clear_all"      , ctypes.c_uint32, 1), # 3 to 3 
        ("reserved_4"            , ctypes.c_uint32, 3), # 4 to 6 
        ("bypass_read_ecc"       , ctypes.c_uint32, 1), # 7 to 7 
        ("clear_pipe_a_trackers" , ctypes.c_uint32, 1), # 8 to 8 
        ("clear_pipe_b_trackers" , ctypes.c_uint32, 1), # 9 to 9 
        ("clear_pipe_c_trackers" , ctypes.c_uint32, 1), # 10 to 10 
        ("clear_pipe_d_trackers" , ctypes.c_uint32, 1), # 11 to 11 
        ("spare_12"              , ctypes.c_uint32, 1), # 12 to 12 
        ("spare_13"              , ctypes.c_uint32, 1), # 13 to 13 
        ("spare_14"              , ctypes.c_uint32, 1), # 14 to 14 
        ("spare_15"              , ctypes.c_uint32, 1), # 15 to 15 
        ("spare_16"              , ctypes.c_uint32, 1), # 16 to 16 
        ("spare_17"              , ctypes.c_uint32, 1), # 17 to 17 
        ("spare_18"              , ctypes.c_uint32, 1), # 18 to 18 
        ("spare_19"              , ctypes.c_uint32, 1), # 19 to 19 
        ("spare_20"              , ctypes.c_uint32, 1), # 20 to 20 
        ("spare_21"              , ctypes.c_uint32, 1), # 21 to 21 
        ("spare_22"              , ctypes.c_uint32, 1), # 22 to 22 
        ("spare_23"              , ctypes.c_uint32, 1), # 23 to 23 
        ("reserved_24"           , ctypes.c_uint32, 8), # 24 to 31 
    ]

 
class DBUF_DEBUG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DBUF_DEBUG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
