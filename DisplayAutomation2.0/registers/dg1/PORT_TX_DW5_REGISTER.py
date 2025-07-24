import ctypes
 
##
# Register instance and offset
PORT_TX_DW5_AUX_B = 0x6C394
PORT_TX_DW5_GRP_B = 0x6C694
PORT_TX_DW5_LN0_B = 0x6C894
PORT_TX_DW5_LN1_B = 0x6C994
PORT_TX_DW5_LN2_B = 0x6CA94
PORT_TX_DW5_LN3_B = 0x6CB94
PORT_TX_DW5_AUX_A = 0x162394
PORT_TX_DW5_GRP_A = 0x162694
PORT_TX_DW5_LN0_A = 0x162894
PORT_TX_DW5_LN1_A = 0x162994
PORT_TX_DW5_LN2_A = 0x162A94
PORT_TX_DW5_LN3_A = 0x162B94
PORT_TX_DW5_AUX_C = 0x160394
PORT_TX_DW5_GRP_C = 0x160694
PORT_TX_DW5_LN0_C = 0x160894
PORT_TX_DW5_LN1_C = 0x160994
PORT_TX_DW5_LN2_C = 0x160A94
PORT_TX_DW5_LN3_C = 0x160B94
PORT_TX_DW5_AUX_D = 0x161394
PORT_TX_DW5_GRP_D = 0x161694
PORT_TX_DW5_LN0_D = 0x161894
PORT_TX_DW5_LN1_D = 0x161994
PORT_TX_DW5_LN2_D = 0x161A94
PORT_TX_DW5_LN3_D = 0x161B94

 
##
# Register bitfield definition structure
class PORT_TX_DW5_REG(ctypes.LittleEndianStructure):
    _fields_ = [        
        ("Spare20",             ctypes.c_uint32, 3),  # 0 to 2
        ("RtermSelect",         ctypes.c_uint32, 3),  # 3 to 5
        ("Spare106",            ctypes.c_uint32, 5),  # 6 to 10
        ("CrScalingCoef",       ctypes.c_uint32, 5),  # 11 to 15
        ("DecodeTimerSel",      ctypes.c_uint32, 2),  # 16 to 17
        ("ScalingModeSel",      ctypes.c_uint32, 3),  # 18 to 20
        ("Reserved",            ctypes.c_uint32, 3),  # 21 to 23
        ("Spare24",             ctypes.c_uint32, 1),  # 24 to 24
        ("CoeffPolarity",       ctypes.c_uint32, 1),  # 25 to 25
        ("CursorProgram",       ctypes.c_uint32, 1),  # 26 to 26
        ("Spare2827",           ctypes.c_uint32, 2),  # 27 to 28
        ("Disable3Tap",         ctypes.c_uint32, 1),  # 29 to 29
        ("Disable2Tap",         ctypes.c_uint32, 1),  # 30 to 30
        ("TxTrainingEnable",    ctypes.c_uint32, 1),  # 31 to 31
    ]

 
class PORT_TX_DW5_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW5_REG),
        ("asUint", ctypes.c_uint32)
    ]
