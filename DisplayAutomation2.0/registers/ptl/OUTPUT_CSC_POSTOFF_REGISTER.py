import ctypes
 
'''
Register instance and offset 
'''
OUTPUT_CSC_POSTOFF_A = 0x49074 
OUTPUT_CSC_POSTOFF_B = 0x49174 
OUTPUT_CSC_POSTOFF_C = 0x49274 
OUTPUT_CSC_POSTOFF_D = 0x49374 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class OUTPUT_CSC_POSTOFF_REG( ctypes.LittleEndianStructure ):
   _fields_ = [
        ("postcsc_offset"  , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"     , ctypes.c_uint32, 19), # 13 to 31 
    ]

 
class OUTPUT_CSC_POSTOFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      OUTPUT_CSC_POSTOFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
