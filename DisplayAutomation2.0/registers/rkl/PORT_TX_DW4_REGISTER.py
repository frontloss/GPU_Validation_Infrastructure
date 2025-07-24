import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW4_GRP_A = 0x162690  
PORT_TX_DW4_LN0_A = 0x162890 
PORT_TX_DW4_LN1_A = 0x162990 
PORT_TX_DW4_LN2_A = 0x162A90 
PORT_TX_DW4_LN3_A = 0x162B90 
PORT_TX_DW4_AUX_A = 0x162390
PORT_TX_DW4_GRP_B = 0x6C690 
PORT_TX_DW4_LN0_B = 0x6C890 
PORT_TX_DW4_LN1_B = 0x6C990 
PORT_TX_DW4_LN2_B = 0x6CA90 
PORT_TX_DW4_LN3_B = 0x6CB90 
PORT_TX_DW4_AUX_B = 0x6C390
PORT_TX_DW4_GRP_C = 0x160690
PORT_TX_DW4_LN0_C = 0x160890
PORT_TX_DW4_LN1_C = 0x160990
PORT_TX_DW4_LN2_C = 0x160A90
PORT_TX_DW4_LN3_C = 0x160B90
PORT_TX_DW4_AUX_C = 0x160390
PORT_TX_DW4_GRP_D = 0x161690
PORT_TX_DW4_LN0_D = 0x161890
PORT_TX_DW4_LN1_D = 0x161990
PORT_TX_DW4_LN2_D = 0x161A90
PORT_TX_DW4_LN3_D = 0x161B90
PORT_TX_DW4_AUX_D = 0x161390
PORT_TX_DW4_GRP_E = 0x16B690
PORT_TX_DW4_LN0_E = 0x16B890
PORT_TX_DW4_LN1_E = 0x16B990
PORT_TX_DW4_LN2_E = 0x16BA90
PORT_TX_DW4_LN3_E = 0x16BB90
PORT_TX_DW4_AUX_E = 0x16B390

'''
Register field expected values 
'''
rterm_limit_default = 0b10000

 
'''
Register bitfield defnition structure 
'''
class PORT_TX_DW4_REG( ctypes.LittleEndianStructure ):
    _fields_ = [        
        ("cursor_coeff"   , ctypes.c_uint32, 6), # 0 to 5 
        ("post_cursor_2"  , ctypes.c_uint32, 6), # 6 to 11
        ("post_cursor_1"  , ctypes.c_uint32, 6), # 12 to 17
        ("rterm_limit"    , ctypes.c_uint32, 5), # 18 to 22 
        ("bs_comp_ovrd"   , ctypes.c_uint32, 1), # 23 to 23 
        ("spare"          , ctypes.c_uint32, 7), # 24 to 30 
        ("loadgen_select" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PORT_TX_DW4_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW4_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
