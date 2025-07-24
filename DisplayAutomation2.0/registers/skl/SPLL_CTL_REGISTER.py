import ctypes
 
'''
Register instance and offset 
'''
SPLL_CTL = 0x46020 

 
'''
Register field expected values 
'''
frequency_select_1350_MHZ = 0b01 
frequency_select_2700_MHZ = 0b10 
frequency_select_810_MHZ = 0b00 
frequency_select_RESERVED = 0b0 
pll_enable_DISABLE = 0b0 
pll_enable_ENABLE = 0b1 
reference_select_BCLK = 0b00 
reference_select_LCPLL_2700 = 0b11 
reference_select_MUXED_SSC = 0b01 
reference_select_PCH_SSC = 0b10 

 
'''
Register bitfield defnition structure 
'''
class SPLL_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0"      , ctypes.c_uint32, 26), # 0 to 25 
        ("frequency_select" , ctypes.c_uint32, 2), # 26 to 27 
        ("reference_select" , ctypes.c_uint32, 2), # 28 to 29 
        ("reserved_30"     , ctypes.c_uint32, 1), # 30 to 30 
        ("pll_enable"      , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class SPLL_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      SPLL_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
