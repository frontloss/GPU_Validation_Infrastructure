import ctypes
 
'''
Register instance and offset 
'''
MIPIA_VERT_SYNC_PADDING_COUNT = 0x6B038 
MIPIC_VERT_SYNC_PADDING_COUNT = 0x6B838 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class MIPI_VERT_SYNC_PADDING_COUNT_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("vertical_sync_padding_count" , ctypes.c_uint32, 16), # 0 to 15 
        ("reserved_16"                , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class MIPI_VERT_SYNC_PADDING_COUNT_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_VERT_SYNC_PADDING_COUNT_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
