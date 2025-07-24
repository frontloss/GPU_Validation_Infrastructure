import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW2_GRP_AE = 0x162348
PORT_TX_DW2_GRP_B = 0x1623C8
PORT_TX_DW2_GRP_C = 0x162B48
PORT_TX_DW2_GRP_D = 0x162BC8
PORT_TX_DW2_GRP_F = 0x162A48
PORT_TX_DW2_LN0_AE = 0x162448
PORT_TX_DW2_LN0_B = 0x162648
PORT_TX_DW2_LN0_C = 0x162C48
PORT_TX_DW2_LN0_D = 0x162E48
PORT_TX_DW2_LN0_F = 0x162848

'''
Register field expected values 
'''
 

'''
Register bitfield defnition structure 
'''
class PORT_TX_DW2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("rcomp_scalar"    , ctypes.c_uint32, 8), # 0 to 7
        ("frclatencyoptim", ctypes.c_uint32, 3),  # 8 to 10
        ("swing_sel_lower", ctypes.c_uint32, 3),  # 11 to 13
        ("cmnmode_sel" , ctypes.c_uint32, 1), # 14 to 14
        ("swing_sel_upper"    , ctypes.c_uint32, 1), # 15 to 15
        ("reserved_16"   , ctypes.c_uint32, 16), # 16 to 31
    ]

 
class PORT_TX_DW2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
