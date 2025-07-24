import ctypes
 
'''
Register instance and offset 
'''
PORT_CL_DW5 = 0x162014 


 
'''
Register field expected values 
'''
force_ = 0b00010010
cri_clock_count_max = 0b0100
iosf_clkdiv_sel = 0b010
enable_port_staggering = 0b1
pg_staggering_control_disable = 0b1
cl_power_down_enable_DISABLE = 0b0
cl_power_down_enable_ENABLE = 0b1
cri_clock_select = 0b1
 
'''
Register bitfield defnition structure 
'''
class PORT_CL_DW5_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("sus_clock_config"             , ctypes.c_uint32, 2), # 0 to 1 
        ("phy_power_ack_override"       , ctypes.c_uint32, 1), # 2 to 2 
        ("cri_clock_select"             , ctypes.c_uint32, 1), # 3 to 3 
        ("cl_power_down_enable"         , ctypes.c_uint32, 1), # 4 to 4 
        ("pg_staggering_control_disable" , ctypes.c_uint32, 1), # 5 to 5 
        ("enable_port_staggering"       , ctypes.c_uint32, 1), # 6 to 6 
        ("reserved_7"                   , ctypes.c_uint32, 1), # 7 to 7 
        ("dl_broadcast_enable"          , ctypes.c_uint32, 1), # 8 to 8 
        ("iosf_clkdiv_sel"              , ctypes.c_uint32, 3), # 9 to 11 
        ("reserved_12"                  , ctypes.c_uint32, 1), # 12 to 12 
        ("iosf_pd_count"                , ctypes.c_uint32, 2), # 13 to 14 
        ("reserved_15"                  , ctypes.c_uint32, 1), # 15 to 15 
        ("cri_clock_count_max"          , ctypes.c_uint32, 4), # 16 to 19 
        ("fuse_repull"                  , ctypes.c_uint32, 1), # 20 to 20 
        ("fusevalid_override"           , ctypes.c_uint32, 1), # 21 to 21 
        ("fusevalid_reset"              , ctypes.c_uint32, 1), # 22 to 22 
        ("reserved_23"                  , ctypes.c_uint32, 1), # 23 to 23 
        ("force"                        , ctypes.c_uint32, 8), # 24 to 31 
    ]

 
class PORT_CL_DW5_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_CL_DW5_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
