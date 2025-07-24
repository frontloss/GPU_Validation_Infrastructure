import ctypes

'''
Register instance and offset
'''
DSSM = 0x51004

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DSSM_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("display_porta_present", ctypes.c_uint32, 1),  # 0 to 0
        ("part_is_soc", ctypes.c_uint32, 1),  # 1 to 1
        ("pavp_gt_gen_select", ctypes.c_uint32, 1),  # 2 to 2
        ("wd_video_fault_continue", ctypes.c_uint32, 1),  # 3 to 3
        ("reserved_4", ctypes.c_uint32, 25),  # 4 to 28
        ("reference_frequency", ctypes.c_uint32, 3)  # 29 to 31
    ]


class DSSM_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSSM_REG),
        ("asUint", ctypes.c_uint32)]