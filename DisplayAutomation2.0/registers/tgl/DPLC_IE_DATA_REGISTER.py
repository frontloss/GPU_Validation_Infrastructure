import ctypes
 
'''
Register instance and offset 
'''
DPLC_IE_DATA_A = 0x49410 
DPLC_IE_DATA_B = 0x49490 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DPLC_IE_DATA_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("even_point" , ctypes.c_uint32, 12), # 0 to 11 
        ("reserved_12" , ctypes.c_uint32, 4), # 12 to 15 
        ("odd_point"  , ctypes.c_uint32, 12), # 16 to 27 
        ("reserved_28" , ctypes.c_uint32, 4), # 28 to 31 
    ]

 
class DPLC_IE_DATA_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLC_IE_DATA_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
