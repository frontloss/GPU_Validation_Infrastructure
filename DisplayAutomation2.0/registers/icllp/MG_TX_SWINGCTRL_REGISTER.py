import ctypes

'''
Register instance and offset
'''
MG_TX_SWINGCTRL_TX1LN0_TXPORT1 = 0x168148
MG_TX_SWINGCTRL_TX1LN0_TXPORT2 = 0x169148
MG_TX_SWINGCTRL_TX1LN0_TXPORT3 = 0x16A148
MG_TX_SWINGCTRL_TX1LN0_TXPORT4 = 0x16B148
MG_TX_SWINGCTRL_TX2LN0_TXPORT1 = 0x1680C8
MG_TX_SWINGCTRL_TX2LN0_TXPORT2 = 0x1690C8
MG_TX_SWINGCTRL_TX2LN0_TXPORT3 = 0x16A0C8
MG_TX_SWINGCTRL_TX2LN0_TXPORT4 = 0x16B0C8
MG_TX_SWINGCTRL_TX1LN1_TXPORT1 = 0x168548
MG_TX_SWINGCTRL_TX1LN1_TXPORT2 = 0x169548
MG_TX_SWINGCTRL_TX1LN1_TXPORT3 = 0x16A548
MG_TX_SWINGCTRL_TX1LN1_TXPORT4 = 0x16B548
MG_TX_SWINGCTRL_TX2LN1_TXPORT1 = 0x1684C8
MG_TX_SWINGCTRL_TX2LN1_TXPORT2 = 0x1694C8
MG_TX_SWINGCTRL_TX2LN1_TXPORT3 = 0x16A4C8
MG_TX_SWINGCTRL_TX2LN1_TXPORT4 = 0x16B4C8

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class MG_TX_SWINGCTRL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("cri_txdeemph_override17_12", ctypes.c_uint32, 6),  # 0 to 5
        ("reserved_6", ctypes.c_uint32, 2),  # 6 to 7
        ("rcomp_pullup_h", ctypes.c_uint32, 8),  # 8 to 15
        ("rcomp_pulldown_h", ctypes.c_uint32, 8),  # 16 to 23
        ("reserved_24", ctypes.c_uint32, 8),  # 24 to 31
    ]


class MG_TX_SWINGCTRL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MG_TX_SWINGCTRL_REG),
        ("asUint", ctypes.c_uint32)]