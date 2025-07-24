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

power_well_a_request_DISABLE = 0b0
power_well_a_request_ENABLE = 0b1
power_well_a_state_DISABLED = 0b0
power_well_a_state_ENABLED = 0b1

power_well_b_request_DISABLE = 0b0
power_well_b_request_ENABLE = 0b1
power_well_b_state_DISABLED = 0b0
power_well_b_state_ENABLED = 0b1

power_well_c_request_DISABLE = 0b0
power_well_c_request_ENABLE = 0b1
power_well_c_state_DISABLED = 0b0
power_well_c_state_ENABLED = 0b1

power_well_d_request_DISABLE = 0b0
power_well_d_request_ENABLE = 0b1
power_well_d_state_DISABLED = 0b0
power_well_d_state_ENABLED = 0b1

 
'''
Register bitfield definition structure 
'''
class PWR_WELL_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("power_well_1_state",      ctypes.c_uint32, 1),    # 0 to 0
        ("power_well_1_request",    ctypes.c_uint32, 1),    # 1 to 1
        ("power_well_2_state",      ctypes.c_uint32, 1),    # 2 to 2
        ("power_well_2_request",    ctypes.c_uint32, 1),    # 3 to 3
        ("power_well_3_state",      ctypes.c_uint32, 1),    # 4 to 4
        ("power_well_3_request",    ctypes.c_uint32, 1),    # 4 to 5
        ("power_well_4_state",      ctypes.c_uint32, 1),    # 6 to 6
        ("power_well_4_request",    ctypes.c_uint32, 1),    # 7 to 7
        ("power_well_5_state",      ctypes.c_uint32, 1),    # 8 to 8
        ("power_well_5_request",    ctypes.c_uint32, 1),    # 9 to 9
        ("power_well_a_state",      ctypes.c_uint32, 1),    # 10
        ("power_well_a_request",    ctypes.c_uint32, 1),    # 11
        ("power_well_b_state",      ctypes.c_uint32, 1),    # 12
        ("power_well_b_request",    ctypes.c_uint32, 1),    # 13
        ("power_well_c_state",      ctypes.c_uint32, 1),    # 14
        ("power_well_c_request",    ctypes.c_uint32, 1),    # 15
        ("power_well_d_state",      ctypes.c_uint32, 1),    # 16
        ("power_well_d_request",    ctypes.c_uint32, 1),    # 17
        ("power_well_e_state",      ctypes.c_uint32, 1),    # 18
        ("power_well_e_request",    ctypes.c_uint32, 1),    # 19
        ("power_well_f_state",      ctypes.c_uint32, 1),    # 20
        ("power_well_f_request",    ctypes.c_uint32, 1),    # 21
        ("reserved_1",              ctypes.c_uint32, 10),   # 22 to 31
    ]

 
class PWR_WELL_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PWR_WELL_CTL_REG),
        ("asUint", ctypes.c_uint32)
    ]
