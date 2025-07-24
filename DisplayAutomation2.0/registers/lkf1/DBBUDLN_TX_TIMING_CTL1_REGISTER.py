import ctypes
 
'''
Register instance and offset 
'''
DBBUDLN_TX_TIMING_CTL1_DL0_A = 0x16229C
DBBUDLN_TX_TIMING_CTL1_DL1_A = 0x16249C
DBBUDLN_TX_TIMING_CTL1_DL2_A = 0x16269C
DBBUDLN_TX_TIMING_CTL1_DL3_A = 0x16289C
DBBUDLN_TX_TIMING_CTL1_DL4_A = 0x162A9C
DBBUDLN_TX_TIMING_CTL1_DL0_B = 0x6C29C
DBBUDLN_TX_TIMING_CTL1_DL1_B = 0x6C49C
DBBUDLN_TX_TIMING_CTL1_DL2_B = 0x6C69C
DBBUDLN_TX_TIMING_CTL1_DL3_B = 0x6C89C
DBBUDLN_TX_TIMING_CTL1_DL4_B = 0x6CA9C

 
'''
Register field expected values 
'''
txhs_early_ppi_ready_generation_enable_DISABLED = 0b0 
txhs_early_ppi_ready_generation_enable_ENABLED = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DBBUDLN_TX_TIMING_CTL1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("thsexit_timer"                         , ctypes.c_uint32, 8), # 0 to 7 
        ("tclk_post_timer"                       , ctypes.c_uint32, 8), # 8 to 15 
        ("tclk_pre_timer"                        , ctypes.c_uint32, 8), # 16 to 23 
        ("txhs_early_ppi_ready_generation_timer" , ctypes.c_uint32, 3), # 24 to 26 
        ("txhs_early_ppi_ready_generation_enable" , ctypes.c_uint32, 1), # 27 to 27 
        ("reserved_28"                           , ctypes.c_uint32, 4), # 28 to 31 
    ]

 
class DBBUDLN_TX_TIMING_CTL1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DBBUDLN_TX_TIMING_CTL1_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
