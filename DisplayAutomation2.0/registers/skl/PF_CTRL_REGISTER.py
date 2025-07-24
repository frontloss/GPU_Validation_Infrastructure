import ctypes
 
'''
Register instance and offset 
'''
PF_CTRL_A = 0x68080 
PF_CTRL_B = 0x68880 
PF_CTRL_C = 0x69080 

 
'''
Register field expected values 
'''
enable_pipe_scaler_DISABLE = 0b0 
enable_pipe_scaler_ENABLE = 0b1 
filter_select_EDGE_ENHANCE = 0b10 
filter_select_EDGE_SOFTEN = 0b11 
filter_select_MEDIUM = 0b01 
pwrup_in_progress_POWERUP_COMPLETE = 0b0 
pwrup_in_progress_POWERUP_IN_PROGRESS = 0b1 
v_filter_bypass_BYPASS = 0b1 
v_filter_bypass_ENABLE = 0b0 
vadapt_en_DISABLE = 0b0 
vadapt_en_ENABLE = 0b1 
vadapt_mode_LEAST_ADAPTIVE = 0b00 
vadapt_mode_MODERATELY_ADAPTIVE = 0b01 
vadapt_mode_MOST_ADAPTIVE = 0b11 
vadapt_mode_RESERVED = 0b0 
vert3tap_AUTO = 0b0 
vert3tap_FORCE = 0b1 
vertical_int_field_invert_FIELD_0 = 0b1 
vertical_int_field_invert_FIELD_1 = 0b0 

 
'''
Register bitfield defnition structure 
'''
class PF_CTRL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"               , ctypes.c_uint32, 17), # 0 to 16 
        ("pwrup_in_progress"        , ctypes.c_uint32, 1), # 17 to 17 
        ("reserved_18"              , ctypes.c_uint32, 2), # 18 to 19 
        ("vertical_int_field_invert" , ctypes.c_uint32, 1), # 20 to 20 
        ("vert3tap"                 , ctypes.c_uint32, 1), # 21 to 21 
        ("reserved_22"              , ctypes.c_uint32, 1), # 22 to 22 
        ("filter_select"            , ctypes.c_uint32, 2), # 23 to 24 
        ("vadapt_mode"              , ctypes.c_uint32, 2), # 25 to 26 
        ("vadapt_en"                , ctypes.c_uint32, 1), # 27 to 27 
        ("v_filter_bypass"          , ctypes.c_uint32, 1), # 28 to 28 
        ("reserved_29"              , ctypes.c_uint32, 2), # 29 to 30 
        ("enable_pipe_scaler"       , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PF_CTRL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PF_CTRL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
