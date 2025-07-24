import ctypes
 
'''
Register instance and offset 
'''
TRANS_FRM_TIME_WD0 = 0x6E020 
TRANS_FRM_TIME_WD1 = 0x6E820 

 
'''
Register field expected values 
'''
frame_time_fraction_0 = 0b00 
frame_time_fraction_1_3 = 0b01 
frame_time_fraction_2_3 = 0b10 
frame_time_fraction_RESERVED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class TRANS_FRM_TIME_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"         , ctypes.c_uint32, 14), # 0 to 13 
        ("frame_time_fraction" , ctypes.c_uint32, 2), # 14 to 15 
        ("frame_time_integer" , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class TRANS_FRM_TIME_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      TRANS_FRM_TIME_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
