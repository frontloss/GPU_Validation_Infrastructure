import ctypes
 
'''
Register instance and offset 
'''
TRANS_CONF_A = 0x70008 
TRANS_CONF_B = 0x71008 
TRANS_CONF_C = 0x72008 
TRANS_CONF_D = 0x73008 
TRANS_CONF_WD0 = 0x7E008
TRANS_CONF_WD1 = 0x7D008 

 
'''
Register field expected values 
'''
dp_audio_symbol_watermark_36_ENTRIES = 0x24 
interlaced_mode_IF_ID = 0b11 
interlaced_mode_PF_ID = 0b01 
interlaced_mode_PF_PD = 0b00 
interlaced_mode_RESERVED = 0b0 
stop_frame_enable_DISABLED = 0b0 
stop_frame_enable_ENABLED = 0b1 
transcoder_enable_DISABLE = 0b0 
transcoder_enable_ENABLE = 0b1 
transcoder_state_DISABLED = 0b0 
transcoder_state_ENABLED = 0b1 

 
'''
Register bitfield defnition structure 
'''
class TRANS_CONF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dp_audio_symbol_watermark" , ctypes.c_uint32, 7), # 6 to 0 
        ("stop_frame_enable"        , ctypes.c_uint32, 1), # 7 to 7 
        ("stop_frame_count"         , ctypes.c_uint32, 4), # 11 to 8 
        ("interlaced_mode"          , ctypes.c_uint32, 11), # 22 to 21 
		("reserved_23"              , ctypes.c_uint32, 7), # 23 to 29 
        ("transcoder_state"         , ctypes.c_uint32, 1), # 30 to 30 
        ("transcoder_enable"        , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class TRANS_CONF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_CONF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
