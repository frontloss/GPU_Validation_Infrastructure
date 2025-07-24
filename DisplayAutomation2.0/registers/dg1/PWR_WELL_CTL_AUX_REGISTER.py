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


'''
Register bitfield defnition structure 
'''
class PWR_WELL_CTL_AUX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("aux_a_io_power_state",    ctypes.c_uint32, 1), # 0 to 0 
        ("aux_a_io_power_request",  ctypes.c_uint32, 1), # 1 to 1 
        ("aux_b_io_power_state",    ctypes.c_uint32, 1), # 2 to 2 
        ("aux_b_io_power_request",  ctypes.c_uint32, 1), # 3 to 3
        ("reserved_4", ctypes.c_uint32, 1),              # 4 to 4
        ("reserved_5", ctypes.c_uint32, 1),              # 5 to 5
        ("aux_usb_c_1_io_power_state",    ctypes.c_uint32, 1), # 6 to 6
        ("aux_usb_c_1_io_power_request",  ctypes.c_uint32, 1), # 7 to 7
        ("aux_usb_c_2_io_power_state",    ctypes.c_uint32, 1), # 8 to 8
        ("aux_usb_c_2_io_power_request",  ctypes.c_uint32, 1), # 9 to 9
        ("reserved_2", ctypes.c_uint32, 22),              # 10 to 31
    ]

 
class PWR_WELL_CTL_AUX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PWR_WELL_CTL_AUX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
