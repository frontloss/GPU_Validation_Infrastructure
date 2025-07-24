import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW3_GRP_A = 0x162D0C
PORT_TX_DW3_LN0_A = 0x16250C
PORT_TX_DW3_LN1_A = 0x16258C
PORT_TX_DW3_LN2_A = 0x16270C
PORT_TX_DW3_LN3_A = 0x16278C

PORT_TX_DW3_GRP_B = 0x6CD0C
PORT_TX_DW3_LN0_B = 0x6C50C
PORT_TX_DW3_LN1_B = 0x6C58C
PORT_TX_DW3_LN2_B = 0x6C70C
PORT_TX_DW3_LN3_B = 0x6C78C

PORT_TX_DW3_GRP_C = 0x163D0C
PORT_TX_DW3_LN0_C = 0x16350C
PORT_TX_DW3_LN1_C = 0x16358C
PORT_TX_DW3_LN2_C = 0x16370C
PORT_TX_DW3_LN3_C = 0x16378C

'''
Register field expected values 
'''
 

'''
Register bitfield defnition structure 
'''
class PORT_TX_DW3_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("Reserved_0"    , ctypes.c_uint32, 26), # 0 to 25
        ("oscaledcompmethod", ctypes.c_uint32, 1),  # 26 to 26
        ("ouniqetrangenmethod", ctypes.c_uint32, 1),  # 27 to 27
        ("Reserved_28" , ctypes.c_uint32, 4), # 28 to 31
    ]

 
class PORT_TX_DW3_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW3_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
