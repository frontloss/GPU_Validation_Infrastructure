import ctypes

'''
Register instance and offset
'''
HDCP2_STATUS_TCA = 0x664B4
HDCP2_STATUS_TCB = 0x665B4
HDCP2_STATUS_TCC = 0x666B4
HDCP2_STATUS_TCD = 0x667B4


'''
Register field expected values
'''
link_authentication_status_AUTHENTICATED = 0b1
link_authentication_status_NOT_AUTHENTICATED = 0b0
link_encryption_status_ENCRYPTING = 0b1
link_encryption_status_NOT_ENCRYPTING = 0b0
link_type_status_TYPE_0 = 0b0
link_type_status_TYPE_1 = 0b1


'''
Register bitfield definition structure
'''


class HDCP2_STATUS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"                , ctypes.c_uint32, 20),  # 0 to 19
        ("link_encryption_status"    , ctypes.c_uint32, 1),  # 20 to 20
        ("link_authentication_status" , ctypes.c_uint32, 1),  # 21 to 21
        ("link_type_status"          , ctypes.c_uint32, 1),  # 22 to 22
        ("reserved_23"               , ctypes.c_uint32, 6),  # 23 to 28
        ("reserved_29"               , ctypes.c_uint32, 3),  # 29 to 31
    ]


class HDCP2_STATUS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      HDCP2_STATUS_REG ),
        ("asUint", ctypes.c_uint32 ) ]

