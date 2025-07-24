import ctypes
 
'''
Register instance and offset 
'''
VIDEO_DIP_GCP_A = 0x60210 
VIDEO_DIP_GCP_B = 0x61210 
VIDEO_DIP_GCP_C = 0x62210 

 
'''
Register field expected values 
'''
gcp_av_mute_CLEAR = 0b0 
gcp_av_mute_SET = 0b1 
gcp_color_indication_DONT_INDICATE = 0b0
gcp_color_indication_INDICATE = 0b1 
gcp_default_phase_enable_CLEAR = 0b0 
gcp_default_phase_enable_SET = 0b1 

 
'''
Register bitfield defnition structure 
'''
class VIDEO_DIP_GCP_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("gcp_av_mute"             , ctypes.c_uint32, 1), # 0 to 0 
        ("gcp_default_phase_enable" , ctypes.c_uint32, 1), # 1 to 1 
        ("gcp_color_indication"    , ctypes.c_uint32, 1), # 2 to 2 
        ("reserved_3"              , ctypes.c_uint32, 29), # 3 to 31 
    ]

 
class VIDEO_DIP_GCP_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      VIDEO_DIP_GCP_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
