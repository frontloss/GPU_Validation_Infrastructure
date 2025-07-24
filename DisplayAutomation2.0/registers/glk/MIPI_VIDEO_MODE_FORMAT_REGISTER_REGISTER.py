import ctypes
 
'''
Register instance and offset 
'''
MIPIA_VIDEO_MODE_FORMAT_REGISTER = 0x6B058 
MIPIC_VIDEO_MODE_FORMAT_REGISTER = 0x6B858 

 
'''
Register field expected values 
'''
de_feature_DISABLED = 0 
de_feature_ENABLED = 1 
disable_turn_on_LEGACY = 1 
disable_turn_on_NEW = 0 
ip_tg_config_DISABLE = 0 
ip_tg_config_ENABLE = 1 
video_bta_disable_DISABLE = 1 
video_bta_disable_ENABLE = 0 
video_mode_fmt_BURST_MODE = 0b11 
video_mode_fmt_NON_BURST_MODE_WITH_SYNC_EVENTS = 0b10 
video_mode_fmt_NON_BURST_MODE_WITH_SYNC_PULSE = 0b01 
video_mode_fmt_RESERVED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class MIPI_VIDEO_MODE_FORMAT_REGISTER_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("video_mode_fmt"   , ctypes.c_uint32, 2), # 0 to 1 
        ("ip_tg_config"     , ctypes.c_uint32, 1), # 2 to 2 
        ("video_bta_disable" , ctypes.c_uint32, 1), # 3 to 3 
        ("de_feature"       , ctypes.c_uint32, 1), # 4 to 4 
        ("reserved_5"       , ctypes.c_uint32, 1), # 5 to 5 
        ("reserved_6"       , ctypes.c_uint32, 26), # 6 to 31 
    ]

 
class MIPI_VIDEO_MODE_FORMAT_REGISTER_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_VIDEO_MODE_FORMAT_REGISTER_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
