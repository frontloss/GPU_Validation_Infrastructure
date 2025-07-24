import ctypes

##
# Register instance and offset
PORT_TX_DW7_GRP_A = 0x16269C
PORT_TX_DW7_LN0_A = 0x16289C
PORT_TX_DW7_LN1_A = 0x16299C
PORT_TX_DW7_LN2_A = 0x162A9C
PORT_TX_DW7_LN3_A = 0x162B9C
PORT_TX_DW7_AUX_A = 0x16239C
PORT_TX_DW7_GRP_B = 0x6C69C
PORT_TX_DW7_LN0_B = 0x6C89C
PORT_TX_DW7_LN1_B = 0x6C99C
PORT_TX_DW7_LN2_B = 0x6CA9C
PORT_TX_DW7_LN3_B = 0x6CB9C
PORT_TX_DW7_AUX_B = 0x6C39C
 

##
# Register bitfield definition structure
class PORT_TX_DW7_REG(ctypes.LittleEndianStructure):
    _fields_ = [        
        ("Spare23", ctypes.c_uint32, 24),  # 0 to 23
        ("NScalar", ctypes.c_uint32, 7),   # 24 to 30
        ("Spare31", ctypes.c_uint32, 1),   # 31 to 31
    ]

 
class PORT_TX_DW7_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW7_REG),
        ("asUint", ctypes.c_uint32)
    ]
