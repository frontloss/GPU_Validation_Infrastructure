import ctypes
 
'''
Register instance and offset 
'''
OUTPUT_CSC_PREOFF_A = 0x49068 
OUTPUT_CSC_PREOFF_B = 0x49168 
OUTPUT_CSC_PREOFF_C = 0x49268 
OUTPUT_CSC_PREOFF_D = 0x49368 
 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class OUTPUT_CSC_PREOFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("precsc_offset"  , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"     , ctypes.c_uint32, 19), # 13 to 31 
    ]

 
class OUTPUT_CSC_PREOFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      OUTPUT_CSC_PREOFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
