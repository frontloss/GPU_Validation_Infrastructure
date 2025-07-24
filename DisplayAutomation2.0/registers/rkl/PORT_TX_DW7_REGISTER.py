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
PORT_TX_DW7_GRP_C = 0x16069C
PORT_TX_DW7_LN0_C = 0x16089C
PORT_TX_DW7_LN1_C = 0x16099C
PORT_TX_DW7_LN2_C = 0x160A9C
PORT_TX_DW7_LN3_C = 0x160B9C
PORT_TX_DW7_AUX_C = 0x16039C
PORT_TX_DW7_GRP_D = 0x16169C
PORT_TX_DW7_LN0_D = 0x16189C
PORT_TX_DW7_LN1_D = 0x16199C
PORT_TX_DW7_LN2_D = 0x161A9C
PORT_TX_DW7_LN3_D = 0x161B9C
PORT_TX_DW7_AUX_D = 0x16139C
PORT_TX_DW7_GRP_E = 0x16B69C
PORT_TX_DW7_LN0_E = 0x16B89C
PORT_TX_DW7_LN1_E = 0x16B99C
PORT_TX_DW7_LN2_E = 0x16BA9C
PORT_TX_DW7_LN3_E = 0x16BB9C
PORT_TX_DW7_AUX_E = 0x16B39C
 

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
