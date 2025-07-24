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

 
'''
Register field expected values 
'''
swing_sel_lower_DEFAULT = 0b010 
rcomp_scalar_DEFAULT = 0b10011000 

 
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
 
