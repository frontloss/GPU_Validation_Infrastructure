import ctypes
 
'''
Register instance and offset 
'''
PORT_PCS_DW1_AUX_A = 0x162304 
PORT_PCS_DW1_AUX_B = 0x6C304 
PORT_PCS_DW1_GRP_A = 0x162604 
PORT_PCS_DW1_GRP_AE = 0x162304 
PORT_PCS_DW1_GRP_B = 0x6C604 
PORT_PCS_DW1_GRP_C = 0x162B04 
PORT_PCS_DW1_GRP_D = 0x162B84 
PORT_PCS_DW1_GRP_F = 0x162A04 
PORT_PCS_DW1_LN0_AE = 0x162404 
PORT_PCS_DW1_LN0_B = 0x162604 
PORT_PCS_DW1_LN0_C = 0x162C04 
PORT_PCS_DW1_LN0_D = 0x162E04 
PORT_PCS_DW1_LN0_F = 0x162804 

 
'''
Register field expected values 
'''
pg_pwrdownen_DISABLE = 0b0
pg_pwrdownen_ENABLE = 0b1
cmnkeeper_enable_DISABLE = 0b0 
cmnkeeper_enable_ENABLE = 0b1
latencyoptim_DEFAULT = 0b01
softreset_enable_DISABLE = 0b0
softreset_enable_ENABLE = 0b1
soft_reset_n_DEFAULT = 0b1
 
'''
Register bitfield defnition structure 
'''
class PORT_PCS_DW1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("soft_reset_n"            , ctypes.c_uint32, 1), # 0 to 0 
        ("softreset_enable"        , ctypes.c_uint32, 1), # 1 to 1 
        ("latencyoptim"            , ctypes.c_uint32, 2), # 2 to 3 
        ("txdeemp"                 , ctypes.c_uint32, 1), # 4 to 4 
        ("txfifo_rst_master_ovrd"  , ctypes.c_uint32, 1), # 5 to 5 
        ("txfifo_rst_master_ovrden" , ctypes.c_uint32, 1), # 6 to 6 
        ("tbc_as_symbclk"          , ctypes.c_uint32, 1), # 7 to 7 
        ("reserved_8"              , ctypes.c_uint32, 16), # 8 to 23 
        ("cmnkeep_biasctr"         , ctypes.c_uint32, 2), # 24 to 25 
        ("cmnkeeper_enable"        , ctypes.c_uint32, 1), # 26 to 26 
        ("pg_pwrdownen"            , ctypes.c_uint32, 1), # 27 to 27 
        ("reserved_28"             , ctypes.c_uint32, 4), # 28 to 31 
    ]

 
class PORT_PCS_DW1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_PCS_DW1_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
