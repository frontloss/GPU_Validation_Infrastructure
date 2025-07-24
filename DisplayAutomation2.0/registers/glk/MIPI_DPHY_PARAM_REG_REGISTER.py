import ctypes
 
'''
Register instance and offset 
'''
MIPIA_DPHY_PARAM_REG = 0x6B080 
MIPIC_DPHY_PARAM_REG = 0x6B880 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class MIPI_DPHY_PARAM_REG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("prepare_count"  , ctypes.c_uint32, 8), # 0 to 7 
        ("clk_zero_count" , ctypes.c_uint32, 8), # 8 to 15 
        ("trail_count"    , ctypes.c_uint32, 8), # 16 to 23 
        ("exit_zero_count" , ctypes.c_uint32, 8), # 24 to 31 
    ]

 
class MIPI_DPHY_PARAM_REG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      MIPI_DPHY_PARAM_REG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
