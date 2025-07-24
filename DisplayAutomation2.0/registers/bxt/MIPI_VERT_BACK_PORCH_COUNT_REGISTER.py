import ctypes
 
'''
Register instance and offset 
'''
MIPIA_VERT_BACK_PORCH_COUNT = 0x6B03C 
MIPIC_VERT_BACK_PORCH_COUNT = 0x6B83C 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class MIPI_VERT_BACK_PORCH_COUNT_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("vertical_back_porch_count" , ctypes.c_uint32, 16), # 0 to 15 
        ("reserved_16"              , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class MIPI_VERT_BACK_PORCH_COUNT_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_VERT_BACK_PORCH_COUNT_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
