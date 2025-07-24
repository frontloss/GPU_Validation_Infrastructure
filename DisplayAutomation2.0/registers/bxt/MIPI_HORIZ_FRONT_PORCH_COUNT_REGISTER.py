import ctypes
 
'''
Register instance and offset 
'''
MIPIA_HORIZ_FRONT_PORCH_COUNT = 0x6B030 
MIPIC_HORIZ_FRONT_PORCH_COUNT = 0x6B830 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class MIPI_HORIZ_FRONT_PORCH_COUNT_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("horizontal_front_porch_count" , ctypes.c_uint32, 16), # 0 to 15 
        ("reserved_16"                 , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class MIPI_HORIZ_FRONT_PORCH_COUNT_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_HORIZ_FRONT_PORCH_COUNT_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
