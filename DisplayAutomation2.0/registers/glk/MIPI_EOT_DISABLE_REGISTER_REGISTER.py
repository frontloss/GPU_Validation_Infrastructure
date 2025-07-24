import ctypes
 
'''
Register instance and offset 
'''
MIPIA_EOT_DISABLE_REGISTER = 0x6B05C 
MIPIC_EOT_DISABLE_REGISTER = 0x6B85C 

 
'''
Register field expected values 
'''
clockstop_DISABLE = 0 
clockstop_ENABLE = 1 
defeature_dpi_fifo_ctr_DISABLE = 0 
defeature_dpi_fifo_ctr_ENABLE = 1 
dphy_defeature_en_DISABLE = 0 
dphy_defeature_en_ENABLE = 1 
eot_dis_DISABLE = 1 
eot_dis_ENABLE = 0 
high_contention_recovery_disable_DISABLE = 1 
high_contention_recovery_disable_ENABLE = 0 
hs_tx_timeout_error_recovery_disable_DISABLE = 1 
hs_tx_timeout_error_recovery_disable_ENABLE = 0 
low_contention_recovery_disable_DISABLE = 1 
low_contention_recovery_disable_ENABLE = 0 
lp_rx_timeout_error_recovery_disable_DISABLE = 1 
lp_rx_timeout_error_recovery_disable_ENABLE = 0 
txdsi_type_not_recognised_error_recovery_disable_DISABLE = 1 
txdsi_type_not_recognised_error_recovery_disable_ENABLE = 0 
txecc_multibit_err_recovery_disable_DISABLE = 1 
txecc_multibit_err_recovery_disable_ENABLE = 0 

 
'''
Register bitfield defnition structure 
'''
class MIPI_EOT_DISABLE_REGISTER_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("eot_dis"                                         , ctypes.c_uint32, 1), # 0 to 0 
        ("clockstop"                                       , ctypes.c_uint32, 1), # 1 to 1 
        ("txecc_multibit_err_recovery_disable"             , ctypes.c_uint32, 1), # 2 to 2 
        ("txdsi_type_not_recognised_error_recovery_disable" , ctypes.c_uint32, 1), # 3 to 3 
        ("high_contention_recovery_disable"                , ctypes.c_uint32, 1), # 4 to 4 
        ("low_contention_recovery_disable"                 , ctypes.c_uint32, 1), # 5 to 5 
        ("hs_tx_timeout_error_recovery_disable"            , ctypes.c_uint32, 1), # 6 to 6 
        ("lp_rx_timeout_error_recovery_disable"            , ctypes.c_uint32, 1), # 7 to 7 
        ("dphy_defeature_en"                               , ctypes.c_uint32, 1), # 8 to 8 
        ("defeature_dpi_fifo_ctr"                          , ctypes.c_uint32, 1), # 9 to 9 
        ("reserved_10"                                     , ctypes.c_uint32, 22), # 10 to 31 
    ]

 
class MIPI_EOT_DISABLE_REGISTER_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_EOT_DISABLE_REGISTER_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
