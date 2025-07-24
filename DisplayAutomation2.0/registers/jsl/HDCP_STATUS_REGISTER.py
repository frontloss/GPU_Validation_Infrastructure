import ctypes

'''
Register instance and offset
'''
HDCP_STATUS_DDIB = 0x6651C
HDCP_STATUS_DDIC = 0x6661C
HDCP_STATUS_DDID = 0x6671C
HDCP_STATUS_DDIA = 0x6681C
HDCP_STATUS_DDIF = 0x6691C
HDCP_STATUS_DDIE = 0x66A1C

'''
Register field expected values
'''
an_ready_status_NOT_READY = 0b0
an_ready_status_READY = 0b1
authentication_status_AUTHENTICATED = 0b1
authentication_status_NOT_AUTHENTICATED = 0b0
cipher_status_MATCH = 0b1
cipher_status_NOT_MATCH = 0b0
link_encryption_status_ENCRYPTING = 0b1
link_encryption_status_NOT_ENCRYPTING = 0b0
r0_ready_status_NOT_READY = 0b0
r0_ready_status_READY = 0b1
ri_prime_match_status_MATCH = 0b1
ri_prime_match_status_NOT_MATCH = 0b0
stream_encryption_status_a_ENCRYPTING = 0b1
stream_encryption_status_a_NOT_ENCRYPTING = 0b0
stream_encryption_status_b_ENCRYPTING = 0b1
stream_encryption_status_b_NOT_ENCRYPTING = 0b0
stream_encryption_status_c_ENCRYPTING = 0b1
stream_encryption_status_c_NOT_ENCRYPTING = 0b0


'''
Register bitfield definition structure
'''


class HDCP_STATUS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0"                , ctypes.c_uint32, 8),  # 0 to 7
        ("frame_count"               , ctypes.c_uint32, 8),  # 8 to 15
        ("cipher_status"             , ctypes.c_uint32, 1),  # 16 to 16
        ("an_ready_status"           , ctypes.c_uint32, 1),  # 17 to 17
        ("r0_ready_status"           , ctypes.c_uint32, 1),  # 18 to 18
        ("ri_prime_match_status"     , ctypes.c_uint32, 1),  # 19 to 19
        ("link_encryption_status"    , ctypes.c_uint32, 1),  # 20 to 20
        ("authentication_status"     , ctypes.c_uint32, 1),  # 21 to 21
        ("reserved_22"               , ctypes.c_uint32, 6),  # 22 to 27
        ("reserved_28"               , ctypes.c_uint32, 1),  # 28 to 28
        ("stream_encryption_status_c" , ctypes.c_uint32, 1),  # 29 to 29
        ("stream_encryption_status_b" , ctypes.c_uint32, 1),  # 30 to 30
        ("stream_encryption_status_a" , ctypes.c_uint32, 1),  # 31 to 31
    ]


class HDCP_STATUS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      HDCP_STATUS_REG),
        ("asUint", ctypes.c_uint32)]

