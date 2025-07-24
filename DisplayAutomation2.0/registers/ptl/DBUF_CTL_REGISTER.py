import ctypes

'''
Register instance and offset 
'''
DBUF_CTL_S0 = 0x45008
DBUF_CTL_S1 = 0x44FE8
DBUF_CTL_S2 = 0x44300
DBUF_CTL_S3 = 0x44304

'''
Register field expected values 
'''
dbuf_power_state_DISABLE = 0b0
dbuf_power_state_ENABLE = 0b1

'''
Register bitfield defnition structure 
'''


class DBUF_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0",                      ctypes.c_uint32, 4),  # 0 to 3
        ("error_injection_flip_bits",       ctypes.c_uint32, 2),  # 4 to 5
        ("reserved_6",                      ctypes.c_uint32, 1),  # 6 to 6
        ("ecc_error_injection_enable",      ctypes.c_uint32, 1),  # 7 to 7
        ("b2b_write_disable",               ctypes.c_uint32, 1),  # 8 to 8
        ("b2b_read_disable",                ctypes.c_uint32, 1),  # 9 to 9
        ("reserved_10",                     ctypes.c_uint32, 2),  # 10 to 11
        ("cc_block_valid_state_service",    ctypes.c_uint32, 4),  # 12 to 15
        ("min_tracker_state_service",       ctypes.c_uint32, 3),  # 16 to 18
        ("max_tracker_state_service",       ctypes.c_uint32, 5),  # 19 to 23
        ("power_gate_delay",                ctypes.c_uint32, 2),  # 24 to 25
        ("display_reorder_buffer_disable",  ctypes.c_uint32, 1),  # 26 to 26
        ("power_gate_dis_override",         ctypes.c_uint32, 1),  # 27 to 27
        ("reserved_28",                     ctypes.c_uint32, 2),  # 28 to 29
        ("dbuf_power_state",                ctypes.c_uint32, 1),  # 30 to 30
        ("dbuf_power_request",              ctypes.c_uint32, 1),  # 31 to 31
    ]


class DBUF_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DBUF_CTL_REG),
        ("asUint", ctypes.c_uint32)]
