import ctypes
 
'''
Register instance and offset 
'''
VIDEO_DIP_CTL_A = 0x60200 
VIDEO_DIP_CTL_B = 0x61200 
VIDEO_DIP_CTL_C = 0x62200 
VIDEO_DIP_CTL_EDP = 0x6F200 

 
'''
Register field expected values 
'''
vdip_enable_avi_DISABLE_AVI_DIP = 0b0 
vdip_enable_avi_ENABLE_AVI_DIP = 0b1 
vdip_enable_gcp_DISABLE_GCP_DIP = 0b0 
vdip_enable_gcp_ENABLE_GCP_DIP = 0b1 
vdip_enable_gmp_DISABLE_GMP_DIP = 0b0 
vdip_enable_gmp_ENABLE_GMP_DIP = 0b1 
vdip_enable_spd_DISABLE_SPD_DIP = 0b0 
vdip_enable_spd_ENABLE_SPD_DIP = 0b1 
vdip_enable_vs_DISABLE_VS_DIP = 0b0 
vdip_enable_vs_ENABLE_VS_DIP = 0b1 
vdip_enable_vsc_DISABLE_VSC_DIP = 0b0 
vdip_enable_vsc_ENABLE_VSC_DIP = 0b1 

 
'''
Register bitfield defnition structure 
'''
class VIDEO_DIP_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("vdip_enable_spd" , ctypes.c_uint32, 1), # 0 to 0 
        ("reserved_1"     , ctypes.c_uint32, 3), # 1 to 3 
        ("vdip_enable_gmp" , ctypes.c_uint32, 1), # 4 to 4 
        ("reserved_5"     , ctypes.c_uint32, 3), # 5 to 7 
        ("vdip_enable_vs" , ctypes.c_uint32, 1), # 8 to 8 
        ("reserved_9"     , ctypes.c_uint32, 3), # 9 to 11 
        ("vdip_enable_avi" , ctypes.c_uint32, 1), # 12 to 12 
        ("reserved_13"    , ctypes.c_uint32, 3), # 13 to 15 
        ("vdip_enable_gcp" , ctypes.c_uint32, 1), # 16 to 16 
        ("reserved_17"    , ctypes.c_uint32, 3), # 17 to 19 
        ("vdip_enable_vsc" , ctypes.c_uint32, 1), # 20 to 20 
        ("reserved_21"    , ctypes.c_uint32, 11), # 21 to 31 
    ]

 
class VIDEO_DIP_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      VIDEO_DIP_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
