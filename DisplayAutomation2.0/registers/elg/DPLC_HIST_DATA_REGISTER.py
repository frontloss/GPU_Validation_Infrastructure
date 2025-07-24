import ctypes

'''
Register instance and offset
'''
DPLC_HIST_DATA_A = 0x49408
DPLC_HIST_DATA_B = 0x49488


'''
Register field expected values
'''


'''
Register bitfield definition structure
'''
class DPLC_HIST_DATA_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("bin"        , ctypes.c_uint32, 17), # 0 to 16
        ("reserved_17" , ctypes.c_uint32, 15), # 17 to 31
    ]


class DPLC_HIST_DATA_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLC_HIST_DATA_REG ),
        ("asUint", ctypes.c_uint32 ) ]

