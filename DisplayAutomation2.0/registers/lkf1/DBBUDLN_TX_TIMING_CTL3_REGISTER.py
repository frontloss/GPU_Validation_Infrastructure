import ctypes
 
'''
Register instance and offset 
'''
DBBUDLN_TX_TIMING_CTL3_DL0_A = 0x1622A4
DBBUDLN_TX_TIMING_CTL3_DL1_A = 0x1624A4
DBBUDLN_TX_TIMING_CTL3_DL2_A = 0x1626A4
DBBUDLN_TX_TIMING_CTL3_DL3_A = 0x1628A4
DBBUDLN_TX_TIMING_CTL3_DL4_A = 0x162AA4
DBBUDLN_TX_TIMING_CTL3_DL0_B = 0x6C2A4
DBBUDLN_TX_TIMING_CTL3_DL1_B = 0x6C4A4
DBBUDLN_TX_TIMING_CTL3_DL2_B = 0x6C6A4
DBBUDLN_TX_TIMING_CTL3_DL3_B = 0x6C8A4
DBBUDLN_TX_TIMING_CTL3_DL4_B = 0x6CAA4


'''
Register field expected values 
'''
tx_lp_turn_around_get_timer_DEFAULT = 0x05 
tx_lp_turn_around_go_timer_DEFAULT = 0x03 

 
'''
Register bitfield defnition structure 
'''
class DBBUDLN_TX_TIMING_CTL3_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("tlpx_timer"                 , ctypes.c_uint32, 8), # 0 to 7 
        ("tx_lp_turn_around_go_timer" , ctypes.c_uint32, 8), # 8 to 15 
        ("tx_lp_turn_around_get_timer" , ctypes.c_uint32, 8), # 16 to 23 
        ("reserved_24"                , ctypes.c_uint32, 8), # 24 to 31 
    ]

 
class DBBUDLN_TX_TIMING_CTL3_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DBBUDLN_TX_TIMING_CTL3_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
