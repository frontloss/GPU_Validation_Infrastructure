import ctypes
 
'''
Register instance and offset 
'''
MIPIA_DBI_FIFO_THRTL_REG = 0x6B024 
MIPIC_DBI_FIFO_THRTL_REG = 0x6B824 

 
'''
Register field expected values 
'''
dbi_fifo_thrtl_EMPTY = 0b10 
dbi_fifo_thrtl_HALF = 0b00 
dbi_fifo_thrtl_QUARTER = 0b01 
dbi_fifo_thrtl_RESERVED = 0b0 

 
'''
Register bitfield defnition structure 
'''
class MIPI_DBI_FIFO_THRTL_REG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dbi_fifo_thrtl" , ctypes.c_uint32, 2), # 0 to 1 
        ("reserved_2"    , ctypes.c_uint32, 30), # 2 to 31 
    ]

 
class MIPI_DBI_FIFO_THRTL_REG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_DBI_FIFO_THRTL_REG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
