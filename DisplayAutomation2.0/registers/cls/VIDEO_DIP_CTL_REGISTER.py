import ctypes
 
'''
Register instance and offset 
'''
VIDEO_DIP_CTL_A = 0x60200 
VIDEO_DIP_CTL_B = 0x61200 
VIDEO_DIP_CTL_C = 0x62200
VIDEO_DIP_CTL_D = 0x63200
VIDEO_DIP_CTL_EDP = 0x6F200 

 
'''
Register field expected values 
'''
adaptive_sync_sdp_enable_DISABLE = 0b0 
adaptive_sync_sdp_enable_ENABLE = 0b1 
drm_dip_enable_DRM_DIP_DISABLE = 0b0 
drm_dip_enable_DRM_DIP_ENABLE = 0b1 
gmp_vsc_avi_drm_double_buffer_disable_DISABLE = 0b1 
gmp_vsc_avi_drm_double_buffer_disable_ENABLE = 0b0 
psr_psr2_vsc_bit_7_DO_NOT_SET = 0b0 
psr_psr2_vsc_bit_7_SET = 0b1 
vdip_enable_avi_DISABLE_AVI_DIP = 0b0 
vdip_enable_avi_ENABLE_AVI_DIP = 0b1 
vdip_enable_gcp_DISABLE_GCP_DIP = 0b0 
vdip_enable_gcp_ENABLE_GCP_DIP = 0b1 
vdip_enable_gmp_DISABLE_GMP_DIP = 0b0 
vdip_enable_gmp_ENABLE_GMP_DIP = 0b1 
vdip_enable_pps_DISABLE = 0b0 
vdip_enable_pps_ENABLE = 0b1 
vdip_enable_spd_DISABLE_SPD_DIP = 0b0 
vdip_enable_spd_ENABLE_SPD_DIP = 0b1 
vdip_enable_vs_DISABLE_VS_DIP = 0b0 
vdip_enable_vs_ENABLE_VS_DIP = 0b1 
vdip_enable_vsc_DISABLE_VSC_DIP = 0b0 
vdip_enable_vsc_ENABLE_VSC_DIP = 0b1 
vsc_select_DATA_ONLY = 0b10 
vsc_select_HEADER_AND_DATA = 0b00 
vsc_select_HEADER_ONLY = 0b01 
vsc_select_NONE = 0b11 

 
'''
Register bitfield defnition structure 
'''
class VIDEO_DIP_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("vdip_enable_spd", ctypes.c_uint32, 1), # 0 to 0
        ("reserved_1"     , ctypes.c_uint32, 3), # 1 to 3 
        ("vdip_enable_gmp", ctypes.c_uint32, 1), # 4 to 4
        ("reserved_5"     , ctypes.c_uint32, 3), # 5 to 7 
        ("vdip_enable_vs" , ctypes.c_uint32, 1), # 8 to 8
        ("reserved_9"     , ctypes.c_uint32, 3), # 9 to 11 
        ("vdip_enable_avi", ctypes.c_uint32, 1), # 12 to 12
        ("reserved_13"    , ctypes.c_uint32, 3), # 13 to 15 
        ("vdip_enable_gcp", ctypes.c_uint32, 1), # 16 to 16
        ("reserved_17"    , ctypes.c_uint32, 3), # 17 to 19 
        ("vdip_enable_vsc", ctypes.c_uint32, 1), # 20 to 20
        ("reserved_21",     ctypes.c_uint32, 2), # 21 to 22
        ("adaptive_sync_sdp_enable", ctypes.c_uint32, 1), # 23 to 23
        ("vdip_enable_pps", ctypes.c_uint32, 1), # 24 to 24
        ("vsc_select"     , ctypes.c_uint32, 2), # 25 to 26
        ("psr_psr2_vsc_bit_7", ctypes.c_uint32, 1), # 27 to 27
        ("drm_dip_enable" , ctypes.c_uint32, 1), # 28 to 28
        ("gmp-vsc-avi-drm_double_buffer_disable" , ctypes.c_uint32, 1), # 29 to 29
        ("reserved_30",     ctypes.c_uint32, 2),  # 30 to 31
    ]

 
class VIDEO_DIP_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      VIDEO_DIP_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
