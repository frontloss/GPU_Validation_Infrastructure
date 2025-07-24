import ctypes
 
'''
Register instance and offset 
'''
WRPLL_CTL1 = 0x46040 
WRPLL_CTL2 = 0x46060 

 
'''
Register field expected values 
'''
feedback_divider_32 = 0x20 
pll_enable_DISABLE = 0b0 
pll_enable_ENABLE = 0b1 
post_divider_36 = 0x24 
reference_divider_24 = 0x18 
reference_select_BCLK = 0b00 
reference_select_LCPLL_2700 = 0b11 
reference_select_MUXED_SSC = 0b10 
reference_select_PCH_SSC = 0b01 

 
'''
Register bitfield defnition structure 
'''
class WRPLL_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reference_divider" , ctypes.c_uint32, 8), # 0 to 7 
        ("post_divider"     , ctypes.c_uint32, 6), # 8 to 13 
        ("reserved_14"      , ctypes.c_uint32, 2), # 14 to 15 
        ("feedback_divider" , ctypes.c_uint32, 8), # 16 to 23 
        ("reserved_24"      , ctypes.c_uint32, 4), # 24 to 27 
        ("reference_select" , ctypes.c_uint32, 2), # 28 to 29 
        ("reserved_30"      , ctypes.c_uint32, 1), # 30 to 30 
        ("pll_enable"       , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class WRPLL_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      WRPLL_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
