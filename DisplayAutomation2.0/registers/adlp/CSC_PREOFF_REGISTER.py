import ctypes

'''
Register instance and offset 
'''
CSC_PREOFF_A = 0x49030
CSC_PREOFF_B = 0x49130
CSC_PREOFF_C = 0x49230

'''
Register field expected values 
'''

'''
Register bitfield defnition structure 
'''


class CSC_PREOFF_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("precsc_medium_offset", ctypes.c_uint32, 13),  # 0 to 12
        ("precsc_low_offset", ctypes.c_uint32, 13),  # 0 to 12
        ("precsc_high_offset", ctypes.c_uint32, 13),  # 0 to 12
        ("reserved_13", ctypes.c_uint32, 19),  # 13 to 31
    ]


class CSC_PREOFF_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", CSC_PREOFF_REG),
        ("asUint", ctypes.c_uint32)]

