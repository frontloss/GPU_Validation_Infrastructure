import ctypes
 
'''
Register instance and offset 
'''
DPLL1_CFGCR2 = 0x6C044 
DPLL2_CFGCR2 = 0x6C04C 
DPLL3_CFGCR2 = 0x6C054 

 
'''
Register field expected values 
'''
central_frequency_8400_MHZ = 0b11 
central_frequency_9000_MHZ = 0b01 
central_frequency_9600_MHZ = 0b00 
central_frequency_RESERVED = 0b0 
kdiv_1 = 0b11 
kdiv_2 = 0b01 
kdiv_3 = 0b10 
kdiv_5 = 0b00 
pdiv_1 = 0b000 
pdiv_2 = 0b001 
pdiv_3 = 0b010 
pdiv_7 = 0b100 
qdiv_mode_DISABLE = 0b0 
qdiv_mode_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DPLL_CFGCR2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("central_frequency" , ctypes.c_uint32, 2), # 0 to 1 
        ("pdiv"             , ctypes.c_uint32, 3), # 2 to 4 
        ("kdiv"             , ctypes.c_uint32, 2), # 5 to 6 
        ("qdiv_mode"        , ctypes.c_uint32, 1), # 7 to 7 
        ("qdiv_ratio"       , ctypes.c_uint32, 8), # 8 to 15 
        ("reserved_16"      , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class DPLL_CFGCR2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_CFGCR2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
