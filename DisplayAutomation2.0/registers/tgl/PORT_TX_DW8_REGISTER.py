import ctypes

##
# Register instance and offset
PORT_TX_DW8_GRP_A = 0x1626A0
PORT_TX_DW8_LN0_A = 0x1628A0
PORT_TX_DW8_LN1_A = 0x1629A0
PORT_TX_DW8_LN2_A = 0x162AA0
PORT_TX_DW8_LN3_A = 0x162BA0
PORT_TX_DW8_AUX_A = 0x1623A0
PORT_TX_DW8_GRP_B = 0x6C6A0
PORT_TX_DW8_LN0_B = 0x6C8A0
PORT_TX_DW8_LN1_B = 0x6C9A0
PORT_TX_DW8_LN2_B = 0x6CAA0
PORT_TX_DW8_LN3_B = 0x6CBA0
PORT_TX_DW8_AUX_B = 0x6C3A0
PORT_TX_DW8_GRP_C = 0x1606A0
PORT_TX_DW8_LN0_C = 0x1608A0
PORT_TX_DW8_LN1_C = 0x1609A0
PORT_TX_DW8_LN2_C = 0x160AA0
PORT_TX_DW8_LN3_C = 0x160BA0
PORT_TX_DW8_AUX_C = 0x1603A0
 

##
# Register bitfield definition structure
class PORT_TX_DW8_REG(ctypes.LittleEndianStructure):
    _fields_ = [        
        ("odcc_upper_limit", ctypes.c_uint32, 5),  # 0 to 4
        ("idcc_code_therm_2_0", ctypes.c_uint32, 3),   # 5 to 7
        ("idcc_code", ctypes.c_uint32, 5),   # 8 to 12
        ("idcc_code_therm_4_3", ctypes.c_uint32, 2),  # 13 to 14
        ("reserved_15", ctypes.c_uint32, 1),  # 15 to 15
        ("odcc_lower_limit", ctypes.c_uint32, 5),  # 16 to 20
        ("reserved_21", ctypes.c_uint32, 1),  # 21 to 21
        ("odccfuse_en", ctypes.c_uint32, 1),  # 22 to 22
        ("odcc_code_ovrd_en", ctypes.c_uint32, 1),  # 23 to 23
        ("odcc_code_ovrd", ctypes.c_uint32, 5),  # 24 to 28
        ("odcc_clk_div_sel", ctypes.c_uint32, 2),  # 29 to 30
        ("odcc_clksel", ctypes.c_uint32, 1)  # 31 to 31
    ]

 
class PORT_TX_DW8_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW8_REG),
        ("asUint", ctypes.c_uint32)
    ]
