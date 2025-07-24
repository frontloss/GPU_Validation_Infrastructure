import ctypes
 
'''
Register instance and offset 
'''
DBBUDLN_MST_SLV_INIT_CTL_DL0_A = 0x162294
DBBUDLN_MST_SLV_INIT_CTL_DL1_A = 0x162494
DBBUDLN_MST_SLV_INIT_CTL_DL2_A = 0x162694
DBBUDLN_MST_SLV_INIT_CTL_DL3_A = 0x162894
DBBUDLN_MST_SLV_INIT_CTL_DL4_A = 0x162A94
DBBUDLN_MST_SLV_INIT_CTL_DL0_B = 0x6C294
DBBUDLN_MST_SLV_INIT_CTL_DL1_B = 0x6C494
DBBUDLN_MST_SLV_INIT_CTL_DL2_B = 0x6C694
DBBUDLN_MST_SLV_INIT_CTL_DL3_B = 0x6C894
DBBUDLN_MST_SLV_INIT_CTL_DL4_B = 0x6CA94

 
'''
Register field expected values 
'''
master_slave_init_timer_configuration_DEFAULT = 0xFB

 
'''
Register bitfield defnition structure 
'''
class DBBUDLN_MST_SLV_INIT_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("master_slave_init_timer_configuration" , ctypes.c_uint32, 12), # 0 to 11
        ("reserved_12"                          , ctypes.c_uint32, 4), # 12 to 15 
        ("udln_ready_timer"                     , ctypes.c_uint32, 3), # 16 to 18 
        ("reserved_19"                          , ctypes.c_uint32, 13), # 19 to 31 
    ]

 
class DBBUDLN_MST_SLV_INIT_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DBBUDLN_MST_SLV_INIT_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
