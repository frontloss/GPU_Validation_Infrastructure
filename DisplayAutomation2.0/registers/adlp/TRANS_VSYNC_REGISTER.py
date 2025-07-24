import ctypes
 
'''
Register instance and offset 
'''
TRANS_VSYNC_A = 0x60014 
TRANS_VSYNC_B = 0x61014 
TRANS_VSYNC_C = 0x62014 
TRANS_VSYNC_D = 0x63014 
TRANS_VSYNC_DSI0 = 0x6B014 
TRANS_VSYNC_DSI1 = 0x6B814 
TRANS_VSYNC_EDP = 0x6F014 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class TRANS_VSYNC_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("vertical_sync_start" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"        , ctypes.c_uint32, 3), # 13 to 15 
        ("vertical_sync_end"  , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29"        , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class TRANS_VSYNC_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_VSYNC_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
