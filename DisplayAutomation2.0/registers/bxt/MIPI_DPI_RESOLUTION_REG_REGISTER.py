import ctypes
 
'''
Register instance and offset 
'''
MIPIA_DPI_RESOLUTION_REG = 0x6B020 
MIPIC_DPI_RESOLUTION_REG = 0x6B820 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class MIPI_DPI_RESOLUTION_REG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("horizontal_address" , ctypes.c_uint32, 16), # 0 to 15 
        ("vertical_address"  , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class MIPI_DPI_RESOLUTION_REG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_DPI_RESOLUTION_REG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
