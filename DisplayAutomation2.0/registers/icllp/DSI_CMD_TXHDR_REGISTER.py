import ctypes
 
'''
Register instance and offset 
'''
DSI_CMD_TXHDR_DSI0 = 0x6B100 
DSI_CMD_TXHDR_DSI1 = 0x6B900 

 
'''
Register field expected values 
'''
lpdt_CMD_TRANSMITTED_IN_HS_STATE = 0b0 
lpdt_CMD_TRANSMITTED_IN_LP_ESCAPE_MODE = 0b1 
payload_LONG_PACKET_FORMAT_PAYLOAD = 0b1 
payload_SHORT_PACKET_FORMAT_NO_PAYLOAD = 0b0 
vertical_blank_fence_CMD_WILL_BE_FENCED = 0b1 
vertical_blank_fence_CMD_WILL_NOT_BE_FENCED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class DSI_CMD_TXHDR_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("data_type"              , ctypes.c_uint32, 6), # 0 to 5 
        ("virtual_channel"        , ctypes.c_uint32, 2), # 6 to 7 
        ("word_count_-_parameters" , ctypes.c_uint32, 16), # 8 to 23 
        ("reserved_24"            , ctypes.c_uint32, 5), # 24 to 28 
        ("vertical_blank_fence"   , ctypes.c_uint32, 1), # 29 to 29 
        ("lpdt"                   , ctypes.c_uint32, 1), # 30 to 30 
        ("payload"                , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DSI_CMD_TXHDR_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DSI_CMD_TXHDR_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
