import ctypes
 
'''
Register instance and offset 
'''
TRANS_HSYNC_A = 0x60008 
TRANS_HSYNC_B = 0x61008 
TRANS_HSYNC_C = 0x62008 
TRANS_HSYNC_D = 0x63008 
TRANS_HSYNC_CMTG0 = 0x6F008
TRANS_HSYNC_CMTG1 = 0x6F108

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class TRANS_HSYNC_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("horizontal_sync_start" , ctypes.c_uint32, 14), # 0 to 13 
        ("reserved_14"          , ctypes.c_uint32, 2), # 14 to 15 
        ("horizontal_sync_end"  , ctypes.c_uint32, 14), # 16 to 29 
        ("reserved_30"          , ctypes.c_uint32, 2), # 30 to 31 
    ]

 
class TRANS_HSYNC_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_HSYNC_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
