import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW2_GRP_A = 0x162D08
PORT_TX_DW2_LN0_A = 0x162508
PORT_TX_DW2_LN1_A = 0x162588
PORT_TX_DW2_LN2_A = 0x162708
PORT_TX_DW2_LN3_A = 0x162788

PORT_TX_DW2_GRP_B = 0x6CD08
PORT_TX_DW2_LN0_B = 0x6C508
PORT_TX_DW2_LN1_B = 0x6C588
PORT_TX_DW2_LN2_B = 0x6C708
PORT_TX_DW2_LN3_B = 0x6C788

PORT_TX_DW2_GRP_C = 0x163D08
PORT_TX_DW2_LN0_C = 0x163508
PORT_TX_DW2_LN1_C = 0x163588
PORT_TX_DW2_LN2_C = 0x163708
PORT_TX_DW2_LN3_C = 0x163788

'''
Register field expected values 
'''
 

'''
Register bitfield defnition structure 
'''
class PORT_TX_DW2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("Reserved_0"    , ctypes.c_uint32, 8), # 0 to 7
        ("ouniqtranscale", ctypes.c_uint32, 8),  # 8 to 15
        ("omargin000", ctypes.c_uint32, 8),  # 16 to 23
        ("Reserved_24" , ctypes.c_uint32, 8), # 24 to 31
    ]

 
class PORT_TX_DW2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
