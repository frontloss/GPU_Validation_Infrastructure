import ctypes
 
'''
Register instance and offset 
'''
MIPIA_AUTOPWG = 0x6B0C8 
MIPIC_AUTOPWG = 0x6B8C8 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class MIPI_AUTOPWG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("mipi_auto_pwg_enable" , ctypes.c_uint32, 1), # 0 to 0 
        ("reserved_1"          , ctypes.c_uint32, 31), # 1 to 31 
    ]

 
class MIPI_AUTOPWG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_AUTOPWG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
