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
        ("reserved_4", ctypes.c_uint32, 29),  # 2 to 30
        ("reference_frequency", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DSSM_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DSSM_REG),
        ("asUint", ctypes.c_uint32)]
