import ctypes

'''
Register instance and offset
'''
MG_TX_DRVCTRL_TX1LN0_TXPORT1 = 0x168144
MG_TX_DRVCTRL_TX1LN0_TXPORT2 = 0x169144
MG_TX_DRVCTRL_TX1LN0_TXPORT3 = 0x16A144
MG_TX_DRVCTRL_TX1LN0_TXPORT4 = 0x16B144
MG_TX_DRVCTRL_TX2LN0_TXPORT1 = 0x1680C4
MG_TX_DRVCTRL_TX2LN0_TXPORT2 = 0x1690C4
MG_TX_DRVCTRL_TX2LN0_TXPORT3 = 0x16A0C4
MG_TX_DRVCTRL_TX2LN0_TXPORT4 = 0x16B0C4
MG_TX_DRVCTRL_TX1LN1_TXPORT1 = 0x168544
MG_TX_DRVCTRL_TX1LN1_TXPORT2 = 0x169544
MG_TX_DRVCTRL_TX1LN1_TXPORT3 = 0x16A544
MG_TX_DRVCTRL_TX1LN1_TXPORT4 = 0x16B544
MG_TX_DRVCTRL_TX2LN1_TXPORT1 = 0x1684C4
MG_TX_DRVCTRL_TX2LN1_TXPORT2 = 0x1694C4
MG_TX_DRVCTRL_TX2LN1_TXPORT3 = 0x16A4C4
MG_TX_DRVCTRL_TX2LN1_TXPORT4 = 0x16B4C4

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class MG_TX_DRVCTRL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("bin_bypassdata", ctypes.c_uint32, 1),  # 0 to 0
        ("onehot_bypass_mode_h", ctypes.c_uint32, 1),  # 1 to 1
        ("postc_bypassen_h", ctypes.c_uint32, 3),  # 2 to 4
        ("prec_bypassen_h", ctypes.c_uint32, 3),  # 5 to 7
        ("o_frcstrongcmen", ctypes.c_uint32, 1),  # 8 to 8
        ("reserved_9", ctypes.c_uint32, 2),  # 9 to 10
        ("o_use_rcomp_in_bypass_h", ctypes.c_uint32, 1), # 11 to 11
        ("cri_loadgen_sel", ctypes.c_uint32, 2),  # 12 to 13
        ("continuous_rcomp_mode_h", ctypes.c_uint32, 1),  # 14 to 14
        ("reserved_15", ctypes.c_uint32, 1),  # 15 to 15
        ("cri_txdeemph_override_5_0", ctypes.c_uint32, 6),  # 16 to 21
        ("cri_txdeemph_override_en", ctypes.c_uint32, 1),  # 22 to 22
        ("reserved_23", ctypes.c_uint32, 1),  # 23 to 23
        ("cri_txdeemph_override_11_6", ctypes.c_uint32, 6),  # 24 to 29
        ("reserved_30", ctypes.c_uint32, 2),  # 30 to 31
    ]


class MG_TX_DRVCTRL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MG_TX_DRVCTRL_REG),
        ("asUint", ctypes.c_uint32)]