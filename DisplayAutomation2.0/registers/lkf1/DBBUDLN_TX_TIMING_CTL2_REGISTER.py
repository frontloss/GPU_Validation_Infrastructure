import ctypes
 
'''
Register instance and offset 
'''
DBBUDLN_TX_TIMING_CTL2_DL0_A = 0x1622A0
DBBUDLN_TX_TIMING_CTL2_DL1_A = 0x1624A0
DBBUDLN_TX_TIMING_CTL2_DL2_A = 0x1626A0
DBBUDLN_TX_TIMING_CTL2_DL3_A = 0x1628A0
DBBUDLN_TX_TIMING_CTL2_DL4_A = 0x162AA0
DBBUDLN_TX_TIMING_CTL2_DL0_B = 0x6C2A0
DBBUDLN_TX_TIMING_CTL2_DL1_B = 0x6C4A0
DBBUDLN_TX_TIMING_CTL2_DL2_B = 0x6C6A0
DBBUDLN_TX_TIMING_CTL2_DL3_B = 0x6C8A0
DBBUDLN_TX_TIMING_CTL2_DL4_B = 0x6CAA0


'''
Register field expected values 
'''
tx_hs_alternative_skew_timer_DEFAULT = 0x7F
tx_hs_auto_initial_deskew_enable_DISABLED = 0b0 
tx_hs_auto_initial_deskew_enable_ENABLED = 0b1 
tx_hs_master_off_timer_DEFAULT = 0xFA
tx_hs_preamble_timer_DEFAULT = 0x01 

 
'''
Register bitfield defnition structure 
'''
class DBBUDLN_TX_TIMING_CTL2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("tx_hs_master_off_timer"          , ctypes.c_uint32, 8), # 0 to 7 
        ("tx_hs_auto_initial_deskew_timer" , ctypes.c_uint32, 8), # 8 to 15 
        ("tx_hs_alternative_skew_timer"    , ctypes.c_uint32, 8), # 16 to 23 
        ("tx_hs_preamble_timer"            , ctypes.c_uint32, 5), # 24 to 28 
        ("tx_hs_auto_initial_deskew_enable" , ctypes.c_uint32, 1), # 29 to 29 
        ("reserved_30"                     , ctypes.c_uint32, 2), # 30 to 31 
    ]

 
class DBBUDLN_TX_TIMING_CTL2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DBBUDLN_TX_TIMING_CTL2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
