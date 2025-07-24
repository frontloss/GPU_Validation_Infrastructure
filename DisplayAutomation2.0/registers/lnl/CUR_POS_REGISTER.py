import ctypes

CUR_POS_A = 0x70088
CUR_POS_B = 0x71088
CUR_POS_C = 0x72088
CUR_POS_D = 0x73088
CUR_POS_ERLY_TPT_A = 0x7008C
CUR_POS_ERLY_TPT_B = 0x7108C
CUR_POS_ERLY_TPT_C = 0x7208C
CUR_POS_ERLY_TPT_D = 0x7308C


class CurPosErlyTpt(ctypes.LittleEndianStructure):
    _fields_ = [
        ('x_position_magnitude', ctypes.c_uint32, 13),
        ('reserved_13', ctypes.c_uint32, 2),
        ('x_position_sign', ctypes.c_uint32, 1),
        ('y_position_magnitude', ctypes.c_uint32, 13),
        ('reserved_29', ctypes.c_uint32, 2),
        ('y_position_sign', ctypes.c_uint32, 1),
    ]


class CUR_POS_ERLY_TPT_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", CurPosErlyTpt),
        ("asUint", ctypes.c_uint32)
    ]
