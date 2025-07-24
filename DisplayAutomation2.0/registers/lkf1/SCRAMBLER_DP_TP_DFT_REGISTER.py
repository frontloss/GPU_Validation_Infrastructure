import ctypes

'''
Register instance and offset 
'''
SCRAMBLER_DP_TP_DFT_A = 0x605E0
SCRAMBLER_DP_TP_DFT_B = 0x615E0
SCRAMBLER_DP_TP_DFT_C = 0x625E0
SCRAMBLER_DP_TP_DFT_D = 0x635E0

'''
Register bitfield defnition structure 
'''


class SCRAMBLER_DP_TP_DFT_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("dp_sr_once_a_frame", ctypes.c_uint32, 1),  # 0 to 0
        ("reserved_1", ctypes.c_uint32, 3),  # 1 to 3
        ("dp_idle_speedup", ctypes.c_uint32, 1),  # 4 to 4
        ("reserved_5", ctypes.c_uint32, 2),  # 5 to 6
        ("reserved_7", ctypes.c_uint32, 1),  # 7 to 7
        ("dp_disparity_reset", ctypes.c_uint32, 1),  # 8 to 8
        ("reserved_9", ctypes.c_uint32, 1),  # 9 to 9
        ("dp_reduce_link_frame", ctypes.c_uint32, 1),  # 10 to 10
        ("fec_debug", ctypes.c_uint32, 1),  # 11 to 11
        ("fec_cd_adj", ctypes.c_uint32, 1),  # 12 to 12
        ("reserved_13", ctypes.c_uint32, 19),  # 13 to 31
    ]


class SCRAMBLER_DP_TP_DFT_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", SCRAMBLER_DP_TP_DFT_REG),
        ("asUint", ctypes.c_uint32)]
