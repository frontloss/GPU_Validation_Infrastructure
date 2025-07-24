import ctypes

'''
Register instance and offset
'''
DPLC_PART_CTL_A = 0x49430
DPLC_PART_CTL_B = 0x494B0


'''
Register field expected values
'''


'''
Register bitfield definition structure
'''
class DPLC_PART_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("part_a_start_tile_row" , ctypes.c_uint32, 5), # 0 to 4
        ("part_a_end_tile_row"  , ctypes.c_uint32, 5), # 5 to 9
        ("reserved_10"          , ctypes.c_uint32, 6), # 10 to 15
        ("part_b_start_tile_row" , ctypes.c_uint32, 5), # 16 to 20
        ("part_b_end_tile_row"  , ctypes.c_uint32, 5), # 21 to 25
        ("reserved_26"          , ctypes.c_uint32, 6), # 26 to 31
    ]


class DPLC_PART_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLC_PART_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]

