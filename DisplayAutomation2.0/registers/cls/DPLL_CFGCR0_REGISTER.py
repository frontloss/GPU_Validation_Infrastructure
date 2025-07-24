import ctypes
 
'''
Register instance and offset 
'''
DPLL0_CFGCR0 = 0x164284
DPLL1_CFGCR0 = 0x16428C
DPLL2_CFGCR0 = 0x16C284
DPLL3_CFGCR0 = 0x16C28C
DPLL4_CFGCR0 = 0x164294
TBTPLL_CFGCR0 = 0x16429C

 
'''
Register field expected values 
'''
dco_fraction_DEFAULT = 0x4000 
dco_integer_DEFAULT = 0x151 
ssc_enable_DISABLE = 0b0 
ssc_enable_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DPLL_CFGCR0_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dco_integer" , ctypes.c_uint32, 10), # 9 to 0 
        ("dco_fraction" , ctypes.c_uint32, 15), # 24 to 10 
        ("ssc_enable"  , ctypes.c_uint32, 1), # 25 to 25 
		("reserved_26", ctypes.c_uint32, 6)  # 26 to 31
    ]

 
class DPLL_CFGCR0_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_CFGCR0_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
