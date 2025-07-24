import ctypes
 
'''
Register instance and offset 
'''
MIPIA_HORIZ_BACK_PORCH_COUNT = 0x6B02C 
MIPIC_HORIZ_BACK_PORCH_COUNT = 0x6B82C 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class MIPI_HORIZ_BACK_PORCH_COUNT_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("horizontal_back_porch_count" , ctypes.c_uint32, 16), # 0 to 15 
        ("reserved_16"                , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class MIPI_HORIZ_BACK_PORCH_COUNT_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_HORIZ_BACK_PORCH_COUNT_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
