import ctypes
 
'''
Register instance and offset 
'''
PORT_TX_DW5_GRP_AE = 0x162354
PORT_TX_DW5_GRP_B = 0x1623D4
PORT_TX_DW5_GRP_C = 0x162B54
PORT_TX_DW5_GRP_D = 0x162BD4
PORT_TX_DW5_GRP_F = 0x162A54
PORT_TX_DW5_LN0_AE = 0x162454
PORT_TX_DW5_LN0_B = 0x162654
PORT_TX_DW5_LN0_C = 0x162C54
PORT_TX_DW5_LN0_D = 0x162E54
PORT_TX_DW5_LN0_F = 0x162854
 
'''
Register field expected values 
'''
ovrd_resetdata_h_DEFAULT = 0b1 
ovrd_resetdata_l_DEFAULT = 0b1 
ovrd_setdata_h_DEFAULT = 0b1 
ovrd_setdata_l_DEFAULT = 0b1
 
'''
Register bitfield defnition structure 
'''
class PORT_TX_DW5_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("spare_2_0"          , ctypes.c_uint32, 3), # 0 to 2
        ("rterm_select"       , ctypes.c_uint32, 3), # 3 to 5
        ("spare_10_6"         , ctypes.c_uint32, 5), # 6 to  10
        ("cr_scaling_coef"    , ctypes.c_uint32, 5), # 11 to 15
        ("decode_timer_sel"   , ctypes.c_uint32, 2), # 16 to 17
        ("scaling_mode_sel"   , ctypes.c_uint32, 3), # 18 to 20
        ("reserved_21"        , ctypes.c_uint32, 3), # 21 to 23
        ("spare_24"           , ctypes.c_uint32, 1), # 24 to 24
        ("coeff_polarity"     , ctypes.c_uint32, 1), # 25 to 25
        ("cursor_program"     , ctypes.c_uint32, 1), # 26 to 26
        ("spare_28_27"        , ctypes.c_uint32, 2), # 27 to 28
        ("disable_3tap"       , ctypes.c_uint32, 1), # 29 to 29
        ("disable_2tap"       , ctypes.c_uint32, 1), # 30 to 30
        ("tx_training_enable" , ctypes.c_uint32, 1), # 31 to 31
    ]
 
class PORT_TX_DW5_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_TX_DW5_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
