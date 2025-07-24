import ctypes

'''
Register instance and offset 
'''
MBUS_CTL = 0x4438C

'''
Register field expected values 
'''
mbus_joining_DISABLE = 0b0
mbus_joining_ENABLE = 0b1
hashing_mode_2X2_HASHING = 0b0
hashing_mode_1X4_HASHING = 0b1

'''
Register bitfield defnition structure 
'''


class MBUS_CTL_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("mbus2_c_ring_packet_drop", ctypes.c_uint32, 1),  # 0 to 0
        ("mbus1_c_ring_packet_drop", ctypes.c_uint32, 1),  # 1 to 1
        ("mbus2_d_ring_packet_drop", ctypes.c_uint32, 1),  # 2 to 2
        ("mbus1_d_ring_packet_drop", ctypes.c_uint32, 1),  # 3 to 3
        ("mbus2_c_ring_packet_error_status", ctypes.c_uint32, 1),  # 4 to 4
        ("mbus1_c_ring_packet_error_status", ctypes.c_uint32, 1),  # 5 to 5
        ("mbus2_d_ring_packet_error_status", ctypes.c_uint32, 1),  # 6 to 6
        ("mbus1_d_ring_packet_error_status", ctypes.c_uint32, 1),  # 7 to 7
        ("reserved_8", ctypes.c_uint32, 18),  # 8 to 25
        ("mbus_joining_pipe_select", ctypes.c_uint32, 3),  # 26 to 28
        ("reserved_29", ctypes.c_uint32, 1),  # 29 to 29
        ("hashing_mode", ctypes.c_uint32, 1),  # 30 to 30
        ("mbus_joining", ctypes.c_uint32, 1),  # 31 to 31
    ]


class MBUS_CTL_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MBUS_CTL_REG),
        ("asUint", ctypes.c_uint32)]
