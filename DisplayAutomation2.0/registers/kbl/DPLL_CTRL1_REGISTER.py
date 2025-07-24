import ctypes
 
'''
Register instance and offset 
'''
DPLL_CTRL1 = 0x6C058 

 
'''
Register field expected values 
'''
dpll0_enable_force_DO_NOT_FORCE = 0b0 
dpll0_enable_force_FORCE_ENABLED = 0b1 
dpll0_hdmi_mode_DP_MODE = 0b0 
dpll0_hdmi_mode_HDMI_MODE_DEBUG = 0b1 
dpll0_link_rate_1080 = 0b100 
dpll0_link_rate_1350 = 0b001 
dpll0_link_rate_1620 = 0b011 
dpll0_link_rate_2160 = 0b101 
dpll0_link_rate_2700 = 0b000 
dpll0_link_rate_810 = 0b010 
dpll0_link_rate_RESERVED = 0b0 
dpll0_override_DISABLE = 0b0 
dpll0_override_ENABLE = 0b1 
dpll0_ssc_DISABLE = 0b0 
dpll0_ssc_ENABLE_DEBUG = 0b1 
dpll1_enable_force_DO_NOT_FORCE = 0b0 
dpll1_enable_force_FORCE_ENABLED = 0b1 
dpll1_hdmi_mode_DP_MODE = 0b0 
dpll1_hdmi_mode_HDMI_MODE = 0b1 
dpll1_link_rate_1080 = 0b100 
dpll1_link_rate_1350 = 0b001 
dpll1_link_rate_1620 = 0b011 
dpll1_link_rate_2160 = 0b101 
dpll1_link_rate_2700 = 0b000 
dpll1_link_rate_810 = 0b010 
dpll1_link_rate_RESERVED = 0b0 
dpll1_override_DISABLE = 0b0 
dpll1_override_ENABLE = 0b1 
dpll1_ssc_DISABLE = 0b0 
dpll1_ssc_ENABLE = 0b1 
dpll2_enable_force_DO_NOT_FORCE = 0b0 
dpll2_enable_force_FORCE_ENABLED = 0b1 
dpll2_hdmi_mode_DP_MODE = 0b0 
dpll2_hdmi_mode_HDMI_MODE = 0b1 
dpll2_link_rate_1080 = 0b100 
dpll2_link_rate_1350 = 0b001 
dpll2_link_rate_1620 = 0b011 
dpll2_link_rate_2160 = 0b101 
dpll2_link_rate_2700 = 0b000 
dpll2_link_rate_810 = 0b010 
dpll2_link_rate_RESERVED = 0b0 
dpll2_override_DISABLE = 0b0 
dpll2_override_ENABLE = 0b1 
dpll2_ssc_DISABLE = 0b0 
dpll2_ssc_ENABLE = 0b1 
dpll3_enable_force_DO_NOT_FORCE = 0b0 
dpll3_enable_force_FORCE_ENABLED = 0b1 
dpll3_hdmi_mode_DP_MODE = 0b0 
dpll3_hdmi_mode_HDMI_MODE = 0b1 
dpll3_link_rate_1080 = 0b100 
dpll3_link_rate_1350 = 0b001 
dpll3_link_rate_1620 = 0b011 
dpll3_link_rate_2160 = 0b101 
dpll3_link_rate_2700 = 0b000 
dpll3_link_rate_810 = 0b010 
dpll3_link_rate_RESERVED = 0b0 
dpll3_override_DISABLE = 0b0 
dpll3_override_ENABLE = 0b1 
dpll3_ssc_DISABLE = 0b0 
dpll3_ssc_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DPLL_CTRL1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dpll0_override"    , ctypes.c_uint32, 1), # 0 to 0 
        ("dpll0_link_rate"   , ctypes.c_uint32, 3), # 1 to 3 
        ("dpll0_ssc"         , ctypes.c_uint32, 1), # 4 to 4 
        ("dpll0_hdmi_mode"   , ctypes.c_uint32, 1), # 5 to 5 
        ("dpll1_override"    , ctypes.c_uint32, 1), # 6 to 6 
        ("dpll1_link_rate"   , ctypes.c_uint32, 3), # 7 to 9 
        ("dpll1_ssc"         , ctypes.c_uint32, 1), # 10 to 10 
        ("dpll1_hdmi_mode"   , ctypes.c_uint32, 1), # 11 to 11 
        ("dpll2_override"    , ctypes.c_uint32, 1), # 12 to 12 
        ("dpll2_link_rate"   , ctypes.c_uint32, 3), # 13 to 15 
        ("dpll2_ssc"         , ctypes.c_uint32, 1), # 16 to 16 
        ("dpll2_hdmi_mode"   , ctypes.c_uint32, 1), # 17 to 17 
        ("dpll3_override"    , ctypes.c_uint32, 1), # 18 to 18 
        ("dpll3_link_rate"   , ctypes.c_uint32, 3), # 19 to 21 
        ("dpll3_ssc"         , ctypes.c_uint32, 1), # 22 to 22 
        ("dpll3_hdmi_mode"   , ctypes.c_uint32, 1), # 23 to 23 
        ("dpll0_enable_force" , ctypes.c_uint32, 1), # 24 to 24 
        ("dpll1_enable_force" , ctypes.c_uint32, 1), # 25 to 25 
        ("dpll2_enable_force" , ctypes.c_uint32, 1), # 26 to 26 
        ("dpll3_enable_force" , ctypes.c_uint32, 1), # 27 to 27 
        ("reserved_28"       , ctypes.c_uint32, 4), # 28 to 31 
    ]

 
class DPLL_CTRL1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_CTRL1_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
