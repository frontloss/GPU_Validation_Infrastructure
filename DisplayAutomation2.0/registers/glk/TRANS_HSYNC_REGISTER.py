import ctypes
 
'''
Register instance and offset 
'''
TRANS_HSYNC_A = 0x60008 
TRANS_HSYNC_B = 0x61008 
TRANS_HSYNC_C = 0x62008 
TRANS_HSYNC_D = 0x63008 
TRANS_HSYNC_DSI0 = 0x6B008 
TRANS_HSYNC_DSI1 = 0x6B808 
TRANS_HSYNC_EDP = 0x6F008 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class TRANS_HSYNC_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("horizontal_sync_start" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"          , ctypes.c_uint32, 3), # 13 to 15 
        ("horizontal_sync_end"  , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29"          , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class TRANS_HSYNC_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_HSYNC_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
