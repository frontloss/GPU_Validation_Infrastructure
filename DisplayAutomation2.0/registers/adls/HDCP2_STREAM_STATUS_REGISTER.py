import ctypes

'''
Register instance and offset
'''
HDCP2_STREAM_STATUS_TCA = 0x664C0
HDCP2_STREAM_STATUS_TCB = 0x665C0
HDCP2_STREAM_STATUS_TCC = 0x666C0
HDCP2_STREAM_STATUS_TCD = 0x667C0 


'''
Register field expected values
'''
stream_encryption_status_ENCRYPTING = 0b1
stream_encryption_status_NOT_ENCRYPTING = 0b0
stream_type_status_TYPE_0 = 0b0
stream_type_status_TYPE_1 = 0b1


'''
Register bitfield definition structure
'''


class HDCP2_STREAM_STATUS_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0"              , ctypes.c_uint32, 30),  # 0 to 29
        ("stream_type_status"      , ctypes.c_uint32, 1),  # 30 to 30
        ("stream_encryption_status" , ctypes.c_uint32, 1),  # 31 to 31
    ]

 
class HDCP2_STREAM_STATUS_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      HDCP2_STREAM_STATUS_REG),
        ("asUint", ctypes.c_uint32)]
 
