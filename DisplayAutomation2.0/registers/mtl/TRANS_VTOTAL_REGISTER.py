import ctypes
 
'''
Register instance and offset 
'''
TRANS_VTOTAL_A = 0x6000C 
TRANS_VTOTAL_B = 0x6100C 
TRANS_VTOTAL_C = 0x6200C 
TRANS_VTOTAL_D = 0x6300C 
TRANS_VTOTAL_DSI0 = 0x6B00C 
TRANS_VTOTAL_DSI1 = 0x6B80C 
TRANS_VTOTAL_WD0 = 0x6E00C 
TRANS_VTOTAL_WD1 = 0x6E80C
TRANS_VTOTAL_CMTG = 0x6F00C

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class TRANS_VTOTAL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("vertical_active" , ctypes.c_uint32, 13), # 0 to 12         
        ("reserved_13"    , ctypes.c_uint32, 3), # 13 to 15 
        ("vertical_total" , ctypes.c_uint32, 13), # 16 to 28 
        ("reserved_29"    , ctypes.c_uint32, 3), # 29 to 31 
    ]

 
class TRANS_VTOTAL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_VTOTAL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
