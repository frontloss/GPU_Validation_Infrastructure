import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW7_GRP_AE = 0x16235C
PORT_TX_DW7_GRP_B = 0x1623DC
PORT_TX_DW7_GRP_C = 0x162B5C
PORT_TX_DW7_GRP_D = 0x162BDC
PORT_TX_DW7_GRP_F = 0x162A5C
PORT_TX_DW7_LN0_AE = 0x16245C
PORT_TX_DW7_LN0_B = 0x16265C
PORT_TX_DW7_LN0_C = 0x162C5C
PORT_TX_DW7_LN0_D = 0x162E5C
PORT_TX_DW7_LN0_F = 0x16285C
 
'''
Register field expected values 
'''
 
'''
Register bitfield defnition structure 
'''
class PORT_TX_DW7_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("spare_23_0" , ctypes.c_uint32, 24), # 0 to 23 
        ("n_scalar"  , ctypes.c_uint32, 7), # 24 to 30 
        ("spare_31"  , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class PORT_TX_DW7_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW7_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
