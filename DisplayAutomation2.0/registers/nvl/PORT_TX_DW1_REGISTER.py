import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW1_GRP_A = 0x162684
PORT_TX_DW1_LN0_A = 0x162884
PORT_TX_DW1_LN1_A = 0x162984
PORT_TX_DW1_LN2_A = 0x162A84
PORT_TX_DW1_LN3_A = 0x162B84
PORT_TX_DW1_AUX_A = 0x162384
PORT_TX_DW1_GRP_B = 0x6C684
PORT_TX_DW1_LN0_B = 0x6C884
PORT_TX_DW1_LN1_B = 0x6C984
PORT_TX_DW1_LN2_B = 0x6CA84
PORT_TX_DW1_LN3_B = 0x6CB84
PORT_TX_DW1_AUX_B = 0x6C384
PORT_TX_DW1_GRP_C = 0x160684
PORT_TX_DW1_LN0_C = 0x160884
PORT_TX_DW1_LN1_C = 0x160984
PORT_TX_DW1_LN2_C = 0x160A84
PORT_TX_DW1_LN3_C = 0x160B84
PORT_TX_DW1_AUX_C = 0x160384
PORT_TX_DW1_GRP_D = 0x161684
PORT_TX_DW1_LN0_D = 0x161884
PORT_TX_DW1_LN1_D = 0x161984
PORT_TX_DW1_LN2_D = 0x161A84
PORT_TX_DW1_LN3_D = 0x161B84
PORT_TX_DW1_AUX_D = 0x161384
PORT_TX_DW1_GRP_E = 0x16B684
PORT_TX_DW1_LN0_E= 0x16B884
PORT_TX_DW1_LN1_E = 0x16B984
PORT_TX_DW1_LN2_E = 0x16BA84
PORT_TX_DW1_LN3_E = 0x16BB84
PORT_TX_DW1_AUX_E = 0x16B384

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''
class PORT_TX_DW1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("o_vref_nom_en", ctypes.c_uint32, 1), # 0 to 0
        ("o_vref_hi_en", ctypes.c_uint32, 1), # 1 to 1
        ("o_vref_low_en", ctypes.c_uint32, 1), # 2 to 2
        ("o_tx_slew_ctrl", ctypes.c_uint32, 2), # 3 to 4
        (" o_iref_ctrl", ctypes.c_uint32, 2), # 5 to 6
        ("o_iref_config", ctypes.c_uint32, 1), # 7 to 7
        ("reserved_8", ctypes.c_uint32,24)  # 8 to 31
    ]

 
class PORT_TX_DW1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW1_REG),
        ("asUint", ctypes.c_uint32)]
 
