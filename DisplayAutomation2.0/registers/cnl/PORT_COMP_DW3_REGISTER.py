import ctypes
 
'''
Register instance and offset 
'''
PORT_COMP_DW3 = 0x16210C
 
'''
Register field expected values 
'''
process_info_DOT_0 = 0b000 
process_info_DOT_1 = 0b001 
process_info_DOT_4 = 0b010

voltage_info_0_85V = 0b00 
voltage_info_0_95V = 0b01 
voltage_info_1_05 = 0b10 

 
'''
Register bitfield defnition structure 
'''
class PORT_COMP_DW3_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("mipi_lpdn_code"   , ctypes.c_uint32, 6), # 0 to 5 
        ("lpdn_code_minout" , ctypes.c_uint32, 1), # 6 to 6 
        ("lpdn_code_maxout" , ctypes.c_uint32, 1), # 7 to 7 
        ("icomp_code"       , ctypes.c_uint32, 7), # 8 to 14 
        ("reserved_15"      , ctypes.c_uint32, 4), # 15 to 18 
        ("icomp_code_minout" , ctypes.c_uint32, 1), # 19 to 19 
        ("icomp_code_maxout" , ctypes.c_uint32, 1), # 20 to 20 
        ("procmon_done"     , ctypes.c_uint32, 1), # 21 to 21 
        ("first_comp_done"  , ctypes.c_uint32, 1), # 22 to 22 
        ("pll_ddi_pwr_ack"  , ctypes.c_uint32, 1), # 23 to 23 
        ("voltage_info"     , ctypes.c_uint32, 2), # 24 to 25 
        ("process_info"     , ctypes.c_uint32, 3), # 26 to 28 
        ("reserved_29"      , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class PORT_COMP_DW3_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PORT_COMP_DW3_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
