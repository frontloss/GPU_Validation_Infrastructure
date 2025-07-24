import ctypes

##
# Register instance and offset
PORT_PCS_DW1_GRP_A = 0x162604
PORT_PCS_DW1_LN0_A = 0x162804
PORT_PCS_DW1_LN1_A = 0x162904
PORT_PCS_DW1_LN2_A = 0x162A04
PORT_PCS_DW1_LN3_A = 0x162B04
PORT_PCS_DW1_AUX_A = 0x162304
PORT_PCS_DW1_GRP_B = 0x6C604
PORT_PCS_DW1_LN0_B = 0x6C804
PORT_PCS_DW1_LN1_B = 0x6C904
PORT_PCS_DW1_LN2_B = 0x6CA04
PORT_PCS_DW1_LN3_B = 0x6CB04
PORT_PCS_DW1_AUX_B = 0x6C304
PORT_PCS_DW1_GRP_C = 0x160604
PORT_PCS_DW1_LN0_C = 0x160804
PORT_PCS_DW1_LN1_C = 0x160904
PORT_PCS_DW1_LN2_C = 0x160A04
PORT_PCS_DW1_LN3_C = 0x160B04
PORT_PCS_DW1_AUX_C = 0x160304
 

##
# Register bitfield definition structure
class PORT_PCS_DW1_REG(ctypes.LittleEndianStructure):
    _fields_ = [        
        ("soft_reset_n", ctypes.c_uint32, 1),  # 0 to 0
        ("softreset_enable", ctypes.c_uint32, 1),   # 1 to 1
        ("latencyoptim", ctypes.c_uint32, 2),   # 2 to 3
        ("txdeemp", ctypes.c_uint32, 1),  # 4 to 4
        ("txfifo_rst_master_ovrd", ctypes.c_uint32, 1),  # 5 to 5
        ("txfifo_rst_master_ovrden", ctypes.c_uint32, 1),  # 6 to 6
        ("tbc_as_symbclk", ctypes.c_uint32, 1),  # 7 to 7
        ("clkreq", ctypes.c_uint32, 2),  # 8 to 9
        ("reserved_10", ctypes.c_uint32, 2),  # 10 to 11
        ("txhigh", ctypes.c_uint32, 2),  # 12 to 13
        ("reserved_14", ctypes.c_uint32, 3),  # 14 to 16
        ("tx_dcc_calib_enable", ctypes.c_uint32, 1),  # 17 to 17
        ("reg_dcc_calib_wake_en", ctypes.c_uint32, 1),  # 18 to 18
        ("reg_dcc_calib_wake_en", ctypes.c_uint32, 1),  # 19 to 19
        ("dcc_mode_select", ctypes.c_uint32, 2),  # 20 to 21
        ("reserved_2", ctypes.c_uint32, 2),  # 22 to 23
        ("cmnkeep_biasctr", ctypes.c_uint32, 2),  # 24 to 25
        ("cmnkeeper_enable", ctypes.c_uint32, 3),  # 26 to 26
        ("pg_pwrdownen", ctypes.c_uint32, 1),  # 27 to 27
        ("cmnkeeper_enable_in_pg", ctypes.c_uint32, 1),  # 28 to 28
        ("reserved_29", ctypes.c_uint32, 3)  # 29 to 31
    ]

 
class PORT_PCS_DW1_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_PCS_DW1_REG),
        ("asUint", ctypes.c_uint32)
    ]
