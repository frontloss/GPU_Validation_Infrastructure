
import ctypes
 
'''
Register instance and offset 
'''
PS_CTRL_1_A = 0x68180 
PS_CTRL_1_B = 0x68980 
PS_CTRL_1_C = 0x69180 
PS_CTRL_1_D = 0x69980
PS_CTRL_2_A = 0x68280 
PS_CTRL_2_B = 0x68A80 
PS_CTRL_2_C = 0x69280 
PS_CTRL_2_D = 0x69A80
 
'''
Register field expected values 
'''
adaptive_filter_select_EDGE_ENHANCE = 0b1 
adaptive_filter_select_MEDIUM = 0b0 
adaptive_filtering_DISABLE = 0x0 
adaptive_filtering_ENABLE = 0x1 
enable_scaler_DISABLE = 0b0 
enable_scaler_ENABLE = 0b1 
filter_select_BILINEAR = 0b11 
filter_select_EDGE_ENHANCE = 0b10 
filter_select_MEDIUM = 0b00 
filter_select_MEDIUM_ = 0b01 
filter_select_PROGRAMMED = 0b01 
pwrup_in_progress_POWERUP_COMPLETE = 0b0 
pwrup_in_progress_POWERUP_IN_PROGRESS = 0b1 
scaler_binding_PIPE_SCALER = 0b000 
scaler_binding_PLANE_1_SCALER = 0b001 
scaler_binding_PLANE_2_SCALER = 0b010 
scaler_binding_PLANE_3_SCALER = 0b011 
scaler_binding_PLANE_4_SCALER = 0b100 
scaler_binding_PLANE_5_SCALER = 0b101 
scaler_binding_PLANE_6_SCALER = 0b110 
scaler_binding_PLANE_7_SCALER = 0b111 
scaler_binding_y_PLANE_6_SCALER = 0b110 
scaler_binding_y_PLANE_7_SCALER = 0b111 
scaler_mode_NORMAL = 0b0 
scaler_mode_PLANAR = 0b1 
uv_horz_filter_set_sel__SET_0 = 0b0 
uv_horz_filter_set_sel__SET_1 = 0b1 
uv_vert_filter_set_sel_SET_0 = 0b0 
uv_vert_filter_set_sel_SET_1 = 0b1 
v_filter_bypass_BYPASS = 0b1 
v_filter_bypass_ENABLE = 0b0 
vertical_int_field_invert_FIELD_0 = 0b1 
vertical_int_field_invert_FIELD_1 = 0b0 
y_horz_filter_set_sel__SET_0 = 0b0 
y_horz_filter_set_sel__SET_1 = 0b1 
y_vert_filter_set_sel_SET_0 = 0b0 
y_vert_filter_set_sel_SET_1 = 0b1 

 
'''
Register bitfield defnition structure 
'''
class PS_CTRL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"                              , ctypes.c_uint32, 1), # 0 to 0 
        ("uv_horz_filter_set_sel_"                 , ctypes.c_uint32, 1), # 1 to 1 
        ("uv_vert_filter_set_sel"                  , ctypes.c_uint32, 1), # 2 to 2 
        ("y_horz_filter_set_sel_"                  , ctypes.c_uint32, 1), # 3 to 3 
        ("y_vert_filter_set_sel"                   , ctypes.c_uint32, 1), # 4 to 4 
        ("scaler_binding_y"                        , ctypes.c_uint32, 3), # 5 to 7 
        ("v_filter_bypass"                         , ctypes.c_uint32, 1), # 8 to 8
        ("allow_double_buffer_update_disable"      , ctypes.c_uint32, 1), # 9 to 9 
        ("reserved_10"                             , ctypes.c_uint32, 7), # 10 to 16 
        ("pwrup_in_progress"                       , ctypes.c_uint32, 1), # 17 to 17 
        ("reserved_18"                             , ctypes.c_uint32, 2), # 18 to 19 
        ("vertical_int_field_invert"               , ctypes.c_uint32, 1), # 20 to 20 
        ("reserved_21"                             , ctypes.c_uint32, 1), # 21 to 21 
        ("adaptive_filter_select"                  , ctypes.c_uint32, 1), # 22 to 22 
        ("filter_select"                           , ctypes.c_uint32, 2), # 23 to 24 
        ("scaler_binding"                          , ctypes.c_uint32, 3), # 25 to 27 
        ("adaptive_filtering"                      , ctypes.c_uint32, 1), # 28 to 28 
        ("scaler_mode"                             , ctypes.c_uint32, 1), # 29 to 29 
        ("scaler_type"                             , ctypes.c_uint32, 1), # 30 to 30 
        ("enable_scaler"                           , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PS_CTRL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PS_CTRL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
