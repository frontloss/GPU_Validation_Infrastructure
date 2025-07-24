import ctypes

'''
Register instance and offset
'''

PORT_TX_DFLEXDPSP1_FIA1 = 0x1638A0
PORT_TX_DFLEXDPSP2_FIA1 = 0x1638A4
PORT_TX_DFLEXDPSP3_FIA1 = 0x1638A8
PORT_TX_DFLEXDPSP4_FIA1 = 0x1638AC
PORT_TX_DFLEXDPSP1_FIA2 = 0x16E8A0
PORT_TX_DFLEXDPSP2_FIA2 = 0x16E8A4
PORT_TX_DFLEXDPSP3_FIA2 = 0x16E8A8
PORT_TX_DFLEXDPSP4_FIA2 = 0x16E8AC
PORT_TX_DFLEXDPSP1_FIA3 = 0x16F8A0
PORT_TX_DFLEXDPSP2_FIA3 = 0x16F8A4
PORT_TX_DFLEXDPSP3_FIA3 = 0x16F8A8
PORT_TX_DFLEXDPSP4_FIA3 = 0x16F8AC

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class PORT_TX_DFLEXDPSP_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector0', ctypes.c_uint32, 4),  # 0 to 3
        ('ModularFia_Mf', ctypes.c_uint32, 1),  # 4 to 4
        ('Tc0LiveState', ctypes.c_uint32, 2),  # 5 to 6
        ('Reserved7', ctypes.c_uint32, 1),  # 7 to 7
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector1', ctypes.c_uint32, 4),  # 8 to 11
        ('IomFwVersion', ctypes.c_uint32, 1),  # 12 to 12
        ('Tc1LiveState', ctypes.c_uint32, 2),  # 13 to 14
        ('Reserved15', ctypes.c_uint32, 1),  # 15 to 15
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector2', ctypes.c_uint32, 4),  # 16 to 19
        ('Reserved20', ctypes.c_uint32, 1),  # 20 to 20
        ('Tc2LiveState', ctypes.c_uint32, 2),  # 21 to 22
        ('Reserved23', ctypes.c_uint32, 1),  # 23 to 23
        ('DisplayPortX4TxLaneAssignmentForTypeCConnector3', ctypes.c_uint32, 4),  # 24 to 27
        ('Reserved28', ctypes.c_uint32, 1),  # 28 to 28
        ('Tc3LiveState', ctypes.c_uint32, 2),  # 29 to 30
        ('Reserved31', ctypes.c_uint32, 1)    # 31 to 31
    ]


class PORT_TX_DFLEXDPSP_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", PORT_TX_DFLEXDPSP_REG),
        ("asUint", ctypes.c_uint32)]