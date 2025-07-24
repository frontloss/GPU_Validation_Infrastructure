import ctypes
 
'''
Register instance and offset 
'''
DSSM = 0x51004

 
'''
Register field expected values 
'''
audio_io_flop_bypass_BYPASS = 0b1 
audio_io_flop_bypass_DONT_BYPASS = 0b0
audio_io_select_NORTH = 0b1 
audio_io_select_SOUTH = 0b0 
de_8k_dis_DISABLE = 0b1 
de_8k_dis_ENABLE = 0b0 
displayport_a_present_NOT_PRESENT = 0b0 
displayport_a_present_PRESENT = 0b1 
part_is_soc_NOT_SOC = 0b0 
part_is_soc_SOC = 0b1 
pavp_gt_gen_select_GEN10_AND_EARLIER = 0b1 
pavp_gt_gen_select_GEN11_AND_ONWARDS = 0b0 
reference_frequency_19_2_MHZ = 0b001 
reference_frequency_24_MHZ = 0b000 
reference_frequency_25_MHZ_TEST = 0b011 
reference_frequency_38_4_MHZ = 0b010 
wd_video_fault_continue_CONTINUE_WRITES = 0b1 
wd_video_fault_continue_STOP_WRITES = 0b0 

 
'''
Register bitfield defnition structure 
'''
class DSSM_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("displayport_a_present"  , ctypes.c_uint32, 1), # 0 to 0 
        ("part_is_soc"            , ctypes.c_uint32, 1), # 1 to 1 
        ("pavp_gt_gen_select"     , ctypes.c_uint32, 1), # 2 to 2 
        ("wd_video_fault_continue" , ctypes.c_uint32, 1), # 3 to 3 
        ("audio_io_select"        , ctypes.c_uint32, 1), # 4 to 4 
        ("audio_io_flop_bypass"   , ctypes.c_uint32, 1), # 5 to 5 
        ("de_8k_dis"              , ctypes.c_uint32, 1), # 6 to 6 
        ("spare_7"                , ctypes.c_uint32, 1), # 7 to 7 
        ("spare_8"                , ctypes.c_uint32, 1), # 8 to 8 
        ("spare_9"                , ctypes.c_uint32, 1), # 9 to 9 
        ("spare_10"               , ctypes.c_uint32, 1), # 10 to 10 
        ("spare_11"               , ctypes.c_uint32, 1), # 11 to 11 
        ("spare_12"               , ctypes.c_uint32, 1), # 12 to 12 
        ("spare_13"               , ctypes.c_uint32, 1), # 13 to 13 
        ("spare_14"               , ctypes.c_uint32, 1), # 14 to 14 
        ("spare_15"               , ctypes.c_uint32, 1), # 15 to 15 
        ("spare_16"               , ctypes.c_uint32, 1), # 16 to 16 
        ("spare_17"               , ctypes.c_uint32, 1), # 17 to 17 
        ("spare_18"               , ctypes.c_uint32, 1), # 18 to 18 
        ("spare_19"               , ctypes.c_uint32, 1), # 19 to 19 
        ("spare_20"               , ctypes.c_uint32, 1), # 20 to 20 
        ("spare_21"               , ctypes.c_uint32, 1), # 21 to 21 
        ("spare_22"               , ctypes.c_uint32, 1), # 22 to 22 
        ("spare_23"               , ctypes.c_uint32, 1), # 23 to 23 
        ("spare_24"               , ctypes.c_uint32, 1), # 24 to 24 
        ("spare_25"               , ctypes.c_uint32, 1), # 25 to 25 
        ("spare_26"               , ctypes.c_uint32, 1), # 26 to 26 
        ("spare_27"               , ctypes.c_uint32, 1), # 27 to 27 
        ("spare_28"               , ctypes.c_uint32, 1), # 28 to 28 
        ("reference_frequency"    , ctypes.c_uint32, 3) # 31 to 29 
    ]

 
class DSSM_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSSM_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
