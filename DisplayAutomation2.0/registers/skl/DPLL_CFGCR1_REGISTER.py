import ctypes
 
'''
Register instance and offset 
'''
DPLL1_CFGCR1 = 0x6C040 
DPLL2_CFGCR1 = 0x6C048 
DPLL3_CFGCR1 = 0x6C050 

 
'''
Register field expected values 
'''
frequency_enable_DISABLE = 0b0 
frequency_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DPLL_CFGCR1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dco_integer"     , ctypes.c_uint32, 9), # 0 to 8 
        ("dco_fraction"    , ctypes.c_uint32, 15), # 9 to 23 
        ("reserved_24"     , ctypes.c_uint32, 7), # 24 to 30 
        ("frequency_enable" , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DPLL_CFGCR1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_CFGCR1_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
