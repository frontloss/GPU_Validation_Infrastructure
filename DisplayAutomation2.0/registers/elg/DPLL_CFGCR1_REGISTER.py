import ctypes
 
'''
Register instance and offset 
'''
DPLL0_CFGCR1 = 0x164288
DPLL1_CFGCR1 = 0x164290
DPLL2_CFGCR1 = 0x16C288
DPLL3_CFGCR1 = 0x16C290
DPLL4_CFGCR1 = 0x164298
TBTPLL_CFGCR1 = 0x1642A0

 
'''
Register field expected values 
'''
cfselovrd_FILTERED_GENLOCK_REF = 0b11 
cfselovrd_NORMAL_XTAL = 0b00 
cfselovrd_RESERVED = 0b0 
cfselovrd_UNFILTERED_GENLOCK_REF = 0b01 
kdiv_1 = 0b001 
kdiv_2 = 0b010 
kdiv_3 = 0b100 
pdiv_2 = 0b0001 
pdiv_3 = 0b0010 
pdiv_5 = 0b0100 
pdiv_7 = 0b1000 
qdiv_mode_DISABLE = 0b0 
qdiv_mode_ENABLE = 0b1 

 
'''
Register bitfield defnition structure 
'''
class DPLL_CFGCR1_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("cfselovrd" , ctypes.c_uint32, 2), # 1 to 0 
        ("pdiv"      , ctypes.c_uint32, 4), # 5 to 2 
        ("kdiv"      , ctypes.c_uint32, 3), # 8 to 6 
        ("qdiv_mode" , ctypes.c_uint32, 1), # 9 to 9 
        ("qdiv_ratio" , ctypes.c_uint32, 8), # 17 to 10 
		("reserved_18", ctypes.c_uint32, 14)  # 18 to 31
    ]

 
class DPLL_CFGCR1_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_CFGCR1_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
