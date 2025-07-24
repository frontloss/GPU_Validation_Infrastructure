import ctypes
 
##
# Register instance and offset
SNPS_PHY_TX_REQ_PORT_A = 0x168200
SNPS_PHY_TX_REQ_PORT_B = 0x169200
SNPS_PHY_TX_REQ_PORT_C = 0x16A200
SNPS_PHY_TX_REQ_PORT_D = 0x16B200
SNPS_PHY_TX_REQ_PORT_TC1 = 0x16C200

 
##
# Register bitfield definition structure
class SnpsPhyReg(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Reserved0', ctypes.c_uint32, 2),                              # bit 0 to 2          
        ('Dp_Tx_Width', ctypes.c_uint32, 2),                            # bit 2 to 4
        ('Reserved4', ctypes.c_uint32, 8),                              # bit 4 to 12
        ('Dp_Tx3_Lpd', ctypes.c_uint32, 1),                             # bit 12 to 13
        ('Dp_Tx2_Lpd', ctypes.c_uint32, 1),                             # bit 13 to 14
        ('Dp_Tx1_Lpd', ctypes.c_uint32, 1),                             # bit 14 to 15
        ('Dp_Tx0_Lpd', ctypes.c_uint32, 1),                             # bit 15 to 16
        ('Dp_Tx_Rate', ctypes.c_uint32, 3),                             # bit 16 to 19
        ('Reserved19', ctypes.c_uint32, 11),                            # bit 19 to 30
        ('LaneDisablePowerStateInPsr', ctypes.c_uint32, 2),             # bit 30 to 32
    ]

 
class SNPS_PHY_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SnpsPhyReg),
        ("asUint", ctypes.c_uint32)
    ]
