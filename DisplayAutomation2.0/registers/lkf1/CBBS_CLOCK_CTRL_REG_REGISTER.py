import ctypes
 
'''
Register instance and offset 
'''
CBBS_CLOCK_CTRL_REG_A = 0x162030
CBBS_CLOCK_CTRL_REG_B = 0x6C030

 
'''
Register field expected values 
'''
clock_mcd_request_override_enable_DISABLED = 0b1 
clock_mcd_request_override_enable_ENABLED = 0b0 
clock_pgl_request_override_enable_DISABLED = 0b1 
clock_pgl_request_override_enable_ENABLED = 0b0 
cri_clock_count_max_16_CYCLES = 0b00 
cri_clock_count_max_32_CYCLES = 0b01 
cri_clock_count_max_48_CYCLES = 0b10 
cri_clock_count_max_63_CYCLES = 0b11 
dfe_clock_divider_DEFAULT = 0xF
dfe_clock_select_override_enable_DISABLED = 0b0 
dfe_clock_select_override_enable_ENABLED = 0b1 
dfe_clock_select_override_val_SOC_IS_NOT_SOURCE = 0b0 
dfe_clock_select_override_val_SOC_IS_THE_SOURCE = 0b1 
disable_clock_mcd_req_ack_chassis_compliance_DISABLED = 0b1 
disable_clock_mcd_req_ack_chassis_compliance_ENABLED = 0b0 
disable_clock_pgl_req_ack_chassis_compliance_DISABLED = 0b1 
disable_clock_pgl_req_ack_chassis_compliance_ENABLED = 0b0 
escape_clock_divider_optional_DEFAULT = 0xA
hs_clock_distribution_to_left_enable_DISABLED = 0b0 
hs_clock_distribution_to_left_enable_ENABLED = 0b1 
hs_clock_distribution_to_right_enable_DISABLED = 0b0 
hs_clock_distribution_to_right_enable_ENABLED = 0b1 
hs_clock_gate_enable_DISABLED = 0b0 
hs_clock_gate_enable_ENABLED = 0b1 
hs_tx_word_clock_divider_DIVIDE_BY_1 = 0b0000 
hs_tx_word_clock_divider_DIVIDE_BY_16 = 0b0100 
hs_tx_word_clock_divider_DIVIDE_BY_2 = 0b0001 
hs_tx_word_clock_divider_DIVIDE_BY_32 = 0b0101 
hs_tx_word_clock_divider_DIVIDE_BY_4 = 0b0010 
hs_tx_word_clock_divider_DIVIDE_BY_8 = 0b0011 

 
'''
Register bitfield defnition structure 
'''
class CBBS_CLOCK_CTRL_REG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("clock_mcd_request_override_enable"           , ctypes.c_uint32, 1), # 0 to 0 
        ("clock_mcd_request_override_value"            , ctypes.c_uint32, 1), # 1 to 1 
        ("disable_clock_mcd_req-ack_chassis_compliance" , ctypes.c_uint32, 1), # 2 to 2 
        ("clock_pgl_request_override_enable"           , ctypes.c_uint32, 1), # 3 to 3 
        ("clock_pgl_request_override_value"            , ctypes.c_uint32, 1), # 4 to 4 
        ("disable_clock_pgl_req-ack_chassis_compliance" , ctypes.c_uint32, 1), # 5 to 5 
        ("dfe_clock_select_override_enable"            , ctypes.c_uint32, 1), # 6 to 6 
        ("dfe_clock_select_override_val"               , ctypes.c_uint32, 1), # 7 to 7 
        ("hs_clock_gate_enable"                        , ctypes.c_uint32, 1), # 8 to 8 
        ("dfe_clock_divider"                           , ctypes.c_uint32, 6), # 9 to 14 
        ("hs_tx_word_clock_divider"                    , ctypes.c_uint32, 4), # 15 to 18 
        ("escape_clock_divider_optional"               , ctypes.c_uint32, 7), # 19 to 25 
        ("hs_clock_distribution_to_right_enable"       , ctypes.c_uint32, 1), # 26 to 26 
        ("hs_clock_distribution_to_left_enable"        , ctypes.c_uint32, 1), # 27 to 27 
        ("cri_clock_count_max"                         , ctypes.c_uint32, 2), # 28 to 29 
        ("reserved_30"                                 , ctypes.c_uint32, 2), # 30 to 31 
    ]

 
class CBBS_CLOCK_CTRL_REG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CBBS_CLOCK_CTRL_REG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
