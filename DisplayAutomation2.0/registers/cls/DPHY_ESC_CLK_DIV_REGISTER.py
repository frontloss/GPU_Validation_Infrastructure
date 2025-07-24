import ctypes
 
'''
Register instance and offset 
'''
DPHY_ESC_CLK_DIV_0 = 0x162190
DPHY_ESC_CLK_DIV_1 = 0x6C190

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DPHY_ESC_CLK_DIV_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("escape_clock_divider_m"      , ctypes.c_uint32, 9), # 0 to 8 
        ("reserved_9"                  , ctypes.c_uint32, 7), # 9 to 15 
        ("byte_clocks_per_escape_clock" , ctypes.c_uint32, 5), # 16 to 20 
        ("reserved_21"                 , ctypes.c_uint32, 11), # 21 to 31 
    ]

 
class DPHY_ESC_CLK_DIV_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPHY_ESC_CLK_DIV_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
