import ctypes

'''
Register instance and offset
'''
VIDEO_DIP_GMP_DATA_0_A = 0x602E0
VIDEO_DIP_GMP_DATA_0_B = 0x612E0
VIDEO_DIP_GMP_DATA_0_C = 0x622E0
VIDEO_DIP_GMP_DATA_0_D = 0x632E0

VIDEO_DIP_GMP_DATA_1_A = 0x602E4
VIDEO_DIP_GMP_DATA_1_B = 0x612E4
VIDEO_DIP_GMP_DATA_1_C = 0x622E4
VIDEO_DIP_GMP_DATA_1_D = 0x632E4

VIDEO_DIP_GMP_DATA_2_A = 0x602E8
VIDEO_DIP_GMP_DATA_2_B = 0x612E8
VIDEO_DIP_GMP_DATA_2_C = 0x622E8
VIDEO_DIP_GMP_DATA_2_D = 0x632E8


'''
Register field expected values
'''

'''
Register bitfield definition structure
'''
class VIDEO_DIP_GMP_DATA_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("data" , ctypes.c_uint32, 32), # 0 to 31
    ]

class VIDEO_DIP_GMP_DATA_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      VIDEO_DIP_GMP_DATA_REG ),
        ("asUint", ctypes.c_uint32 ) ]

