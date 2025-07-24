import ctypes
 
'''
Register instance and offset 
'''
CUR_BASE_A = 0x70084 
CUR_BASE_B = 0x71084 
CUR_BASE_C = 0x72084 

 
'''
Register field expected values 
'''
decryption_request_NOT_REQUESTED = 0b0 
decryption_request_REQUESTED = 0b1 
key_select_ID_1 = 0b001 
key_select_PAVP = 0b000 
key_select_RESERVED = 0b0 
vrr_master_flip_DEFAULT = 0b1 

 
'''
Register bitfield defnition structure 
'''
class CUR_BASE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"        , ctypes.c_uint32, 2), # 0 to 1 
        ("decryption_request" , ctypes.c_uint32, 1), # 2 to 2 
        ("reserved_3"        , ctypes.c_uint32, 1), # 3 to 3 
        ("key_select"        , ctypes.c_uint32, 3), # 4 to 6 
        ("reserved_7"        , ctypes.c_uint32, 4), # 7 to 10 
        ("vrr_master_flip"   , ctypes.c_uint32, 1), # 11 to 11 
        ("cursor_base_31_12" , ctypes.c_uint32, 20), # 12 to 31 
    ]

 
class CUR_BASE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      CUR_BASE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
