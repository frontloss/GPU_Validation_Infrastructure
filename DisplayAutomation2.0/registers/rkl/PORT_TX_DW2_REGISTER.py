import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW2_GRP_A = 0x162688 
PORT_TX_DW2_LN0_A = 0x162888
PORT_TX_DW2_LN1_A = 0x162988
PORT_TX_DW2_LN2_A = 0x162A88
PORT_TX_DW2_LN3_A = 0x162B88
PORT_TX_DW2_AUX_A = 0x162388
PORT_TX_DW2_GRP_B = 0x6C688 
PORT_TX_DW2_LN0_B = 0x6C888
PORT_TX_DW2_LN1_B = 0x6C988
PORT_TX_DW2_LN2_B = 0x6CA88
PORT_TX_DW2_LN3_B = 0x6CB88
PORT_TX_DW2_AUX_B = 0x6C388
PORT_TX_DW2_GRP_C = 0x160688
PORT_TX_DW2_LN0_C = 0x160888
PORT_TX_DW2_LN1_C = 0x160988
PORT_TX_DW2_LN2_C = 0x160A88
PORT_TX_DW2_LN3_C = 0x160B88
PORT_TX_DW2_AUX_C = 0x160388
PORT_TX_DW2_GRP_D = 0x161688
PORT_TX_DW2_LN0_D = 0x161888
PORT_TX_DW2_LN1_D = 0x161988
PORT_TX_DW2_LN2_D = 0x161A88
PORT_TX_DW2_LN3_D = 0x161B88
PORT_TX_DW2_AUX_D = 0x161388
PORT_TX_DW2_GRP_E = 0x16B688
PORT_TX_DW2_LN0_E = 0x16B888
PORT_TX_DW2_LN1_E = 0x16B988
PORT_TX_DW2_LN2_E = 0x16BA88
PORT_TX_DW2_LN3_E = 0x16BB88
PORT_TX_DW2_AUX_E = 0x16B388

 
'''
Register field expected values 
'''
swing_sel_lower_default = 0b010
rcomp_scalar_default = 0b10011000

 
'''
Register bitfield defnition structure 
'''
class PORT_TX_DW2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("rcomp_scalar"    , ctypes.c_uint32, 8), # 0 to 7 
        ("frclatencyoptim" , ctypes.c_uint32, 3), # 8 to 10 
        ("swing_sel_lower" , ctypes.c_uint32, 3), # 11 to 13 
        ("cmnmode_sel"    , ctypes.c_uint32, 1), # 14 to 14 
        ("swing_sel_upper" , ctypes.c_uint32, 1), # 15 to 15 
        ("reserved_16"    , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class PORT_TX_DW2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
