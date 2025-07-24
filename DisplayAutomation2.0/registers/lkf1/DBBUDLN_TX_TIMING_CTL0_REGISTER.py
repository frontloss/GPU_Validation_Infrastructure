import ctypes
 
'''
Register instance and offset 
'''
DBBUDLN_TX_TIMING_CTL0_DL0_A = 0x162298
DBBUDLN_TX_TIMING_CTL0_DL1_A = 0x162498
DBBUDLN_TX_TIMING_CTL0_DL2_A = 0x162698
DBBUDLN_TX_TIMING_CTL0_DL3_A = 0x162898
DBBUDLN_TX_TIMING_CTL0_DL4_A = 0x162A98
DBBUDLN_TX_TIMING_CTL0_DL0_B = 0x6C298
DBBUDLN_TX_TIMING_CTL0_DL1_B = 0x6C498
DBBUDLN_TX_TIMING_CTL0_DL2_B = 0x6C698
DBBUDLN_TX_TIMING_CTL0_DL3_B = 0x6C898
DBBUDLN_TX_TIMING_CTL0_DL4_B = 0x6CA98


'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DBBUDLN_TX_TIMING_CTL0_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("hs-req_timer"  , ctypes.c_uint32, 8), # 0 to 7 
        ("tprepare_timer" , ctypes.c_uint32, 8), # 8 to 15 
        ("tzero_timer"   , ctypes.c_uint32, 8), # 16 to 23 
        ("ttrail_timer"  , ctypes.c_uint32, 8), # 24 to 31 
    ]

 
class DBBUDLN_TX_TIMING_CTL0_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DBBUDLN_TX_TIMING_CTL0_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
