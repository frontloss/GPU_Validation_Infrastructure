import ctypes
 
'''
Register instance and offset 
'''
DP_TP_CTL_A = 0x64040 
DP_TP_CTL_B = 0x64140 
DP_TP_CTL_C = 0x64240 
DP_TP_CTL_D = 0x64340 
DP_TP_CTL_E = 0x64440 
DP_TP_CTL_F = 0x64540 

 
'''
Register field expected values 
'''
alternate_sr_enable_DISABLE = 0b0 
alternate_sr_enable_ENABLE = 0b1 
dp_link_training_enable_IDLE = 0b010 
dp_link_training_enable_NORMAL = 0b011 
dp_link_training_enable_PATTERN_1 = 0b000 
dp_link_training_enable_PATTERN_2 = 0b001 
dp_link_training_enable_PATTERN_3 = 0b100 
dp_link_training_enable_PATTERN_4 = 0b101 
enhanced_framing_enable_DISABLED = 0b0 
enhanced_framing_enable_ENABLED = 0b1 
force_act_DO_NOT_FORCE = 0b0 
force_act_FORCE = 0b1 
scrambling_disable_DISABLE = 0b1 
scrambling_disable_ENABLE = 0b0 
training_pattern_4_select_RESERVED = 0b1 
training_pattern_4_select_TRAINING_PATTERN_4A = 0b00 
training_pattern_4_select_TRAINING_PATTERN_4B = 0b01 
training_pattern_4_select_TRAINING_PATTERN_4C = 0b10 
transport_enable_DISABLE = 0b0 
transport_enable_ENABLE = 0b1 
transport_mode_select_MST_MODE = 0b1 
transport_mode_select_SST_MODE = 0b0 
forward_error_correction_ENABLE = 0b1
forward_error_correction_DISABLE = 0b0

'''
Register bitfield defnition structure 
'''
class DP_TP_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0",                  ctypes.c_uint32,6), # 0 to 5 
        ("alternate_sr_enable",         ctypes.c_uint32,1), # 6 to 6 
        ("scrambling_disable",          ctypes.c_uint32,1), # 7 to 7 
        ("dp_link_training_enable",     ctypes.c_uint32,3), # 8 to 10 
        ("reserved_11",                 ctypes.c_uint32,4), # 11 to 14 
        ("reserved_15",                 ctypes.c_uint32,1), # 15 to 15 
        ("reserved_16",                 ctypes.c_uint32,2), # 16 to 17 
        ("enhanced_framing_enable",     ctypes.c_uint32,1), # 18 to 18 
        ("training_pattern_4_select",   ctypes.c_uint32,2), # 19 to 20 
        ("reserved_21",                 ctypes.c_uint32,4), # 21 to 24 
        ("force_act",                   ctypes.c_uint32,1), # 25 to 25 
        ("reserved_26",                 ctypes.c_uint32,1), # 26 to 26 
        ("transport_mode_select",       ctypes.c_uint32,1), # 27 to 27 
        ("reserved_28",                 ctypes.c_uint32,2), # 28 to 29
        ("fec_enable",                  ctypes.c_uint32,1), # 30 to 30
        ("transport_enable",            ctypes.c_uint32,1), # 31 to 31 
    ]

 
class DP_TP_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DP_TP_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]