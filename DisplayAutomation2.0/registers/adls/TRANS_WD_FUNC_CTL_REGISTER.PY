import ctypes
 
'''
Register instance and offset 
'''
TRANS_WD_FUNC_CTL_0 = 0x6E400 
TRANS_WD_FUNC_CTL_1 = 0x6EC00 

 
'''
Register field expected values 
'''
wd_function_enable_DISABLE = 0b0 
wd_function_enable_ENABLE = 0b1
triggered_capture_mode_enable_DISABLE = 0b0 
triggered_capture_mode_enable_ENABLE = 0b1
#start_trigger_frame_DISABLE = 0b0 Not required, will be never reset by driver, will be reset by only HW
start_trigger_frame_ENABLE = 0b1
#stop_trigger_frame_DISABLE = 0b0 
stop_trigger_frame_ENABLE = 0b1
enable_write_caching_DISABLE = 0b0 
enable_write_caching_ENABLE = 0b1
chroma_filtering_enable_DROP = 0b0 
chroma_filtering_enable_FILTER = 0b1 

wd_color_mode_RGB10 = 0b110
wd_color_mode_YUY2 = 0b101
wd_color_mode_Y410 = 0b100
wd_color_mode_RGBX = 0b011
wd_color_mode_XYUV_444 = 0b010
wd_color_mode_YUV_422 = 0b001
wd_color_mode_YUV_444 = 0b000 

control_pointers_00 = 0b00 
control_pointers_01 = 0b01
control_pointers_11 = 0b11

vdenc_session_select_00 = 0b00 
vdenc_session_select_01 = 0b01
vdenc_session_select_10 = 0b10
vdenc_session_select_11 = 0b11

wd_input_select_PIPE_A = 0b000 
wd_input_select_PIPE_B = 0b101 
wd_input_select_PIPE_C = 0b110 
wd_input_select_PIPE_D = 0b111 
wd_input_select_RESERVED = 0b0

maximum_defference_to_enable_write_caching_0 = 0b00000000
 
'''
Register bitfield defnition structure 
'''
class TRANS_WD_FUNC_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [        
        ("frame_number"                                         , ctypes.c_uint32, 4), # 0 to 3
        ("maximum_defference_to_enable_write_caching"           , ctypes.c_uint32, 8), # 4 to 11 
        ("wd_input_select"                                      , ctypes.c_uint32, 3), # 12 to 14 
        ("reserved_15"                                          , ctypes.c_uint32, 1), # 15 to 15 
        ("vdenc_session_select"                                 , ctypes.c_uint32, 2), # 16 to 17 
        ("control_pointers"                                     , ctypes.c_uint32, 2), # 18 to 19 
        ("wd_color_mode"                                        , ctypes.c_uint32, 3), # 20 to 22 
        ("reserved_23"                                          , ctypes.c_uint32, 3), # 23 to 25 
        ("chroma_filtering_enable"                              , ctypes.c_uint32, 1), # 26 to 26  
        ("enable_write_caching"                                 , ctypes.c_uint32, 1), # 27 to 27
        ("stop_trigger_frame"                                   , ctypes.c_uint32, 1), # 28 to 28
        ("start_trigger_frame"                                  , ctypes.c_uint32, 1), # 29 to 29
        ("triggered_capture_mode_enable"                        , ctypes.c_uint32, 1), # 30 to 30        
        ("wd_function_enable"                                   , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class TRANS_WD_FUNC_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_WD_FUNC_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
