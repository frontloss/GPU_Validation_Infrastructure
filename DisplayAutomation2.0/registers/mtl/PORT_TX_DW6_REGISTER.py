import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW6_AUX_A = 0x162398
PORT_TX_DW6_GRP_A = 0x162698
PORT_TX_DW6_LN0_A = 0x162898
PORT_TX_DW6_LN1_A = 0x162998
PORT_TX_DW6_LN2_A = 0x162A98
PORT_TX_DW6_LN3_A = 0x160B98
PORT_TX_DW6_AUX_B = 0x6C398
PORT_TX_DW6_GRP_B = 0x6C698
PORT_TX_DW6_LN0_B = 0x6C898
PORT_TX_DW6_LN1_B = 0x6C998
PORT_TX_DW6_LN2_B = 0x6CA98
PORT_TX_DW6_LN3_B = 0x6CB98
PORT_TX_DW6_AUX_C = 0x160398
PORT_TX_DW6_GRP_C = 0x160698
PORT_TX_DW6_LN0_C = 0x160898
PORT_TX_DW6_LN1_C = 0x160998
PORT_TX_DW6_LN2_C = 0x160A98
PORT_TX_DW6_LN3_C = 0x160B98
PORT_TX_DW6_GRP_D = 0x161698
PORT_TX_DW6_LN0_D = 0x161898
PORT_TX_DW6_LN1_D = 0x161998
PORT_TX_DW6_LN2_D = 0x161A98
PORT_TX_DW6_LN3_D = 0x161B98
PORT_TX_DW6_AUX_D = 0x161398
PORT_TX_DW6_GRP_E = 0x16B698
PORT_TX_DW6_LN0_E= 0x16B898
PORT_TX_DW6_LN1_E = 0x16B998
PORT_TX_DW6_LN2_E = 0x16BA98
PORT_TX_DW6_LN3_E = 0x16BB98
PORT_TX_DW6_AUX_E = 0x16B398

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''
class PORT_TX_DW6_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("o_ldo_bypass_cri", ctypes.c_uint32, 1), # 0 to 0
        ("o_ldo_ref_sel_cri", ctypes.c_uint32, 6), # 1 to 6
        ("o_func_ovrd_en", ctypes.c_uint32, 1), # 7 to 7
        ("reserved_8", ctypes.c_uint32, 24) # 8 to 31
    ]

 
class PORT_TX_DW6_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW6_REG),
        ("asUint", ctypes.c_uint32)]
 
