import ctypes
 
'''
Register instance and offset 
'''
PWR_WELL_CTL1 = 0x45400
PWR_WELL_CTL2 = 0x45404
PWR_WELL_CTL4 = 0x4540C

 
'''
Register field expected values 
'''
power_well_1_request_DISABLE = 0b0
power_well_1_request_ENABLE = 0b1
power_well_1_state_DISABLED = 0b0
power_well_1_state_ENABLED = 0b1

power_well_2_request_DISABLE = 0b0
power_well_2_request_ENABLE = 0b1
power_well_2_state_DISABLED = 0b0
power_well_2_state_ENABLED = 0b1

power_well_3_request_DISABLE = 0b0
power_well_3_request_ENABLE = 0b1
power_well_3_state_DISABLED = 0b0 
power_well_3_state_ENABLED = 0b1

power_well_4_request_DISABLE = 0b0
power_well_4_request_ENABLE = 0b1
power_well_4_state_DISABLED = 0b0
power_well_4_state_ENABLED = 0b1

power_well_5_request_DISABLE = 0b0
power_well_5_request_ENABLE = 0b1
power_well_5_state_DISABLED = 0b0
power_well_5_state_ENABLED = 0b1

 
'''
Register bitfield defnition structure 
'''
class PWR_WELL_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("power_well_1_state",      ctypes.c_uint32, 1),  # 0 to 0 
        ("power_well_1_request",    ctypes.c_uint32, 1),  # 1 to 1 
        ("power_well_2_state",      ctypes.c_uint32, 1),  # 2 to 2 
        ("power_well_2_request",    ctypes.c_uint32, 1),  # 3 to 3 
        ("power_well_3_state",      ctypes.c_uint32, 1),  # 4 to 4 
        ("power_well_3_request",    ctypes.c_uint32, 1),  # 4 to 5 
        ("power_well_4_state",      ctypes.c_uint32, 1),  # 6 to 6
        ("power_well_4_request",    ctypes.c_uint32, 1),  # 7 to 7
        ("power_well_5_state",      ctypes.c_uint32, 1),  # 8 to 8
        ("power_well_5_request",    ctypes.c_uint32, 1),  # 9 to 9
        ("reserved_8",              ctypes.c_uint32, 22), # 10 to 31
    ]

 
class PWR_WELL_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PWR_WELL_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
