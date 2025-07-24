import ctypes

'''
Register instance and offset 
'''
CSC_POSTOFF_A = 0x49040
CSC_POSTOFF_B = 0x49140
CSC_POSTOFF_C = 0x49240

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class CSC_POSTOFF_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("postcsc_low__offset", ctypes.c_uint32, 13),  # 0 to 12
        ("postcsc_medium_offset", ctypes.c_uint32, 13),  # 0 to 12
        ("postcsc_high_offset", ctypes.c_uint32, 13),  # 0 to 12
        ("reserved_13", ctypes.c_uint32, 19),  # 13 to 31
    ]


class CSC_POSTOFF_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", CSC_POSTOFF_REG),
        ("asUint", ctypes.c_uint32)]

