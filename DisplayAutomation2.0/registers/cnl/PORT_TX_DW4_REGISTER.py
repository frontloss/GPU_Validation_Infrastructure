import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW4_GRP_AE = 0x162350
PORT_TX_DW4_GRP_B =	0x1623D0
PORT_TX_DW4_GRP_C =	0x162B50
PORT_TX_DW4_GRP_D = 0x162BD0
PORT_TX_DW4_GRP_F =	0x162A50
PORT_TX_DW4_LN0_AE = 0x162450
PORT_TX_DW4_LN0_B =	0x162650
PORT_TX_DW4_LN0_C = 0x162C50
PORT_TX_DW4_LN0_D = 0x162E50
PORT_TX_DW4_LN0_F = 0x162850
PORT_TX_DW4_LN1_AE = 0x1624D0
PORT_TX_DW4_LN1_B = 0x1626D0
PORT_TX_DW4_LN1_C = 0x162CD0
PORT_TX_DW4_LN1_D = 0x162ED0
PORT_TX_DW4_LN1_F = 0x1628D0
PORT_TX_DW4_LN2_AE = 0x162550
PORT_TX_DW4_LN2_B = 0x162750
PORT_TX_DW4_LN2_C = 0x162D50
PORT_TX_DW4_LN2_D = 0x162F50
PORT_TX_DW4_LN2_F = 0x162950
PORT_TX_DW4_LN3_AE = 0x1625D0
PORT_TX_DW4_LN3_B = 0x1627D0
PORT_TX_DW4_LN3_C = 0x162DD0
PORT_TX_DW4_LN3_D = 0x162FD0
PORT_TX_DW4_LN3_F = 0x1629D0
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PORT_TX_DW4_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("cursor_coeff",   ctypes.c_uint32, 6),  # 0 to 5
        ("post_cursor2",   ctypes.c_uint32, 6),  # 6 to 11
        ("post_cursor1",   ctypes.c_uint32, 6),  # 12 to 17
        ("rterm_limit",    ctypes.c_uint32, 5),  # 18 to 22
        ("bs_comp_ovrd",   ctypes.c_uint32, 1),  # 23 to 23
        ("spare",          ctypes.c_uint32, 7),  # 24 to 30
        ("loadgen_select", ctypes.c_uint32, 1),  # 31 to 31
    ]

 
class PORT_TX_DW4_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW4_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
