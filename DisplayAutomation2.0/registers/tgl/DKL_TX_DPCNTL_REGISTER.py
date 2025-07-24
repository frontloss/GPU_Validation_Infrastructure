import ctypes

'''
Register instance and offset
'''
DKL_TX_DPCNTL0_PORT1 = 0x1682C0
DKL_TX_DPCNTL1_PORT1 = 0x1682C4
DKL_TX_DPCNTL2_PORT1 = 0x1682C0
DKL_TX_DPCNTL3_PORT1 = 0x1682C4
DKL_TX_DPCNTL0_PORT2 = 0x1692C0
DKL_TX_DPCNTL1_PORT2 = 0x1692C4
DKL_TX_DPCNTL2_PORT2 = 0x1692C0
DKL_TX_DPCNTL3_PORT2 = 0x1692C4
DKL_TX_DPCNTL0_PORT3 = 0x16A2C0
DKL_TX_DPCNTL1_PORT3 = 0x16A2C4
DKL_TX_DPCNTL2_PORT3 = 0x16A2C0
DKL_TX_DPCNTL3_PORT3 = 0x16A2C4
DKL_TX_DPCNTL0_PORT4 = 0x16B2C0
DKL_TX_DPCNTL1_PORT4 = 0x16B2C4
DKL_TX_DPCNTL2_PORT4 = 0x16B2C0
DKL_TX_DPCNTL3_PORT4 = 0x16B2C4
DKL_TX_DPCNTL0_PORT5 = 0x1682C0
DKL_TX_DPCNTL1_PORT5 = 0x1682C4
DKL_TX_DPCNTL2_PORT5 = 0x1682C0
DKL_TX_DPCNTL3_PORT5 = 0x1682C4
DKL_TX_DPCNTL0_PORT6 = 0x1682C0
DKL_TX_DPCNTL1_PORT6 = 0x1682C4
DKL_TX_DPCNTL2_PORT6 = 0x1682C0
DKL_TX_DPCNTL3_PORT6 = 0x1682C4

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_TX_DPCNTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("vswing_control_tx", ctypes.c_uint32, 3),  # 0 to 2
        ("cursor_control_tx", ctypes.c_uint32, 5),  # 3 to 7
        ("de_emphasis_control_l0_tx", ctypes.c_uint32, 5),  # 8 to 12
        ("preshoot_control_l0", ctypes.c_uint32, 5),  # 13 to 17
        ("shunt_cp_tx", ctypes.c_uint32, 5),  # 18 to 22
        ("shunt_cm_tx", ctypes.c_uint32, 5),  # 23 to 27
        ("slow_trim_enable_tx", ctypes.c_uint32, 1),  # 28 to 28
        ("pipe_select_tx", ctypes.c_uint32, 1),  # 29 to 29
        ("trainingen_tx", ctypes.c_uint32, 1),  # 30 to 30
        ("reserved_31", ctypes.c_uint32, 1),  # 31 to 31
    ]


class DKL_TX_DPCNTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_TX_DPCNTL_REG),
        ("asUint", ctypes.c_uint32)]