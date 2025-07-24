import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW4_GRP_A = 0x162D10
PORT_TX_DW4_LN0_A = 0x162510
PORT_TX_DW4_LN1_A = 0x162590
PORT_TX_DW4_LN2_A = 0x162710
PORT_TX_DW4_LN3_A = 0x162790

PORT_TX_DW4_GRP_B = 0x6CD10
PORT_TX_DW4_LN0_B = 0x6C510
PORT_TX_DW4_LN1_B = 0x6C590
PORT_TX_DW4_LN2_B = 0x6C710
PORT_TX_DW4_LN3_B = 0x6C790

PORT_TX_DW4_GRP_C = 0x163D10
PORT_TX_DW4_LN0_C = 0x163510
PORT_TX_DW4_LN1_C = 0x163590
PORT_TX_DW4_LN2_C = 0x163710
PORT_TX_DW4_LN3_C = 0x163790

'''
Register field expected values 
'''
 

'''
Register bitfield defnition structure 
'''
class PORT_TX_DW4_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("Reserved_0"    , ctypes.c_uint32, 24), # 0 to 23
        ("ow2tapdeemph9p5", ctypes.c_uint32, 8),  # 24 to 31
    ]

 
class PORT_TX_DW4_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW4_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
