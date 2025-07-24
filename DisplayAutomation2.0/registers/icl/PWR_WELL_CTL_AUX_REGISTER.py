import ctypes
 
'''
Register instance and offset 
'''
PWR_WELL_CTL_AUX2 = 0x45444 
PWR_WELL_CTL_AUX4 = 0x4544C

 
'''
Register field expected values 
'''
aux_a_io_power_request_DISABLE = 0b0
aux_a_io_power_request_ENABLE = 0b1
aux_a_io_power_state_DISABLED = 0b0 
aux_a_io_power_state_ENABLED = 0b1

aux_b_io_power_request_DISABLE = 0b0
aux_b_io_power_request_ENABLE = 0b1
aux_b_io_power_state_DISABLED = 0b0 
aux_b_io_power_state_ENABLED = 0b1

aux_c_io_power_request_DISABLE = 0b0
aux_c_io_power_request_ENABLE = 0b1
aux_c_io_power_state_DISABLED = 0b0
aux_c_io_power_state_ENABLED = 0b1

aux_d_io_power_request_DISABLE = 0b0
aux_d_io_power_request_ENABLE = 0b1 
aux_d_io_power_state_DISABLED = 0b0
aux_d_io_power_state_ENABLED = 0b1

aux_e_io_power_request_DISABLE = 0b0
aux_e_io_power_request_ENABLE = 0b1 
aux_e_io_power_state_DISABLED = 0b0
aux_e_io_power_state_ENABLED = 0b1

aux_f_io_power_request_DISABLE = 0b0
aux_f_io_power_request_ENABLE = 0b1 
aux_f_io_power_state_DISABLED = 0b0
aux_f_io_power_state_ENABLED = 0b1

 
'''
Register bitfield defnition structure 
'''
class PWR_WELL_CTL_AUX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("aux_a_io_power_state",    ctypes.c_uint32, 1), # 0 to 0 
        ("aux_a_io_power_request",  ctypes.c_uint32, 1), # 1 to 1 
        ("aux_b_io_power_state",    ctypes.c_uint32, 1), # 2 to 2 
        ("aux_b_io_power_request",  ctypes.c_uint32, 1), # 3 to 3 
        ("aux_c_io_power_state",    ctypes.c_uint32, 1), # 4 to 4 
        ("aux_c_io_power_request",  ctypes.c_uint32, 1), # 5 to 5
        ("aux_d_io_power_state",    ctypes.c_uint32, 1), # 6 to 6 
        ("aux_d_io_power_request",  ctypes.c_uint32, 1), # 7 to 7
        ("aux_e_io_power_state",    ctypes.c_uint32, 1), # 8 to 8
        ("aux_e_io_power_request",  ctypes.c_uint32, 1), # 9 to 9
        ("aux_f_io_power_state",    ctypes.c_uint32, 1), # 10 to 10 
        ("aux_f_io_power_request",  ctypes.c_uint32, 1), # 11 to 11 
        ("reserved_4", ctypes.c_uint32, 4),                 # 12 to 15
        ("aux_tbt_c_io_power_state", ctypes.c_uint32, 1),   # 16 to 16
        ("aux_tbt_c_io_power_request", ctypes.c_uint32, 1), # 17 to 17
        ("aux_tbt_d_io_power_state", ctypes.c_uint32, 1),   # 18 to 18
        ("aux_tbt_d_io_power_request", ctypes.c_uint32, 1), # 19 to 19
        ("aux_tbt_e_io_power_state", ctypes.c_uint32, 1),   # 20 to 20
        ("aux_tbt_e_io_power_request", ctypes.c_uint32, 1), # 21 to 21
        ("aux_tbt_f_io_power_state", ctypes.c_uint32, 1),   # 22 to 22
        ("aux_tbt_f_io_power_request", ctypes.c_uint32, 1), # 23 to 23
        ("reserved_8", ctypes.c_uint32, 8),                 # 24 to 31
    ]

 
class PWR_WELL_CTL_AUX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PWR_WELL_CTL_AUX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
