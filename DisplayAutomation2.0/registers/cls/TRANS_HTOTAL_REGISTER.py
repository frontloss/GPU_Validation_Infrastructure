import ctypes
 
'''
Register instance and offset 
'''
TRANS_HTOTAL_A = 0x60000 
TRANS_HTOTAL_B = 0x61000 
TRANS_HTOTAL_C = 0x62000 
TRANS_HTOTAL_D = 0x63000
TRANS_HTOTAL_WD0 = 0x6E000 
TRANS_HTOTAL_WD1 = 0x6E800
TRANS_HTOTAL_CMTG0 = 0x6F000
TRANS_HTOTAL_CMTG1 = 0x6F100

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class TRANS_HTOTAL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("horizontal_active" , ctypes.c_uint32, 14), # 0 to 13 
        ("reserved_14"      , ctypes.c_uint32, 2), # 14 to 15 
        ("horizontal_total" , ctypes.c_uint32, 14), # 16 to 29 
        ("reserved_30"      , ctypes.c_uint32, 2), # 30 to 31 
    ]

 
class TRANS_HTOTAL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_HTOTAL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
