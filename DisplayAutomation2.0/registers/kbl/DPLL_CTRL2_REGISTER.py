import ctypes
 
'''
Register instance and offset 
'''
DPLL_CTRL2 = 0x6C05C 

 
'''
Register field expected values 
'''
ddia_clock_off_OFF = 0b1 
ddia_clock_off_ON = 0b0 
ddia_clock_select_DPLL0 = 0b00 
ddia_clock_select_DPLL1 = 0b01 
ddia_clock_select_DPLL2 = 0b10 
ddia_clock_select_DPLL3 = 0b11 
ddia_select_override_DISABLE = 0b0 
ddia_select_override_ENABLE = 0b1 
ddib_clock_off_OFF = 0b1 
ddib_clock_off_ON = 0b0 
ddib_clock_select_DPLL0 = 0b00 
ddib_clock_select_DPLL1 = 0b01 
ddib_clock_select_DPLL2 = 0b10 
ddib_clock_select_DPLL3 = 0b11 
ddib_select_override_DISABLE = 0b0 
ddib_select_override_ENABLE = 0b1 
ddic_clock_off_OFF = 0b1 
ddic_clock_off_ON = 0b0 
ddic_clock_select_DPLL0 = 0b00 
ddic_clock_select_DPLL1 = 0b01 
ddic_clock_select_DPLL2 = 0b10 
ddic_clock_select_DPLL3 = 0b11 
ddic_select_override_DISABLE = 0b0 
ddic_select_override_ENABLE = 0b1 
ddid_clock_off_OFF = 0b1 
ddid_clock_off_ON = 0b0 
ddid_clock_select_DPLL0 = 0b00 
ddid_clock_select_DPLL1 = 0b01 
ddid_clock_select_DPLL2 = 0b10 
ddid_clock_select_DPLL3 = 0b11 
ddid_select_override_DISABLE = 0b0 
ddid_select_override_ENABLE = 0b1 
ddie_clock_off_OFF = 0b1 
ddie_clock_off_ON = 0b0 
ddie_clock_select_DPLL0 = 0b00 
ddie_clock_select_DPLL1 = 0b01 
ddie_clock_select_DPLL2 = 0b10 
ddie_clock_select_DPLL3 = 0b11 
ddie_select_override_DISABLE = 0b0 
ddie_select_override_ENABLE = 0b1 
dpll0_inverse_ref_INVERSE = 0b1 
dpll0_inverse_ref_NOT_INVERSE = 0b0 
dpll1_inverse_ref_INVERSE = 0b1 
dpll1_inverse_ref_NOT_INVERSE = 0b0 
dpll2_inverse_ref_INVERSE = 0b1 
dpll2_inverse_ref_NOT_INVERSE = 0b0 
dpll3_inverse_ref_INVERSE = 0b1 
dpll3_inverse_ref_NOT_INVERSE = 0b0 

 
'''
Register bitfield defnition structure 
'''
class DPLL_CTRL2_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("ddia_select_override" , ctypes.c_uint32, 1), # 0 to 0 
        ("ddia_clock_select"   , ctypes.c_uint32, 2), # 1 to 2 
        ("ddib_select_override" , ctypes.c_uint32, 1), # 3 to 3 
        ("ddib_clock_select"   , ctypes.c_uint32, 2), # 4 to 5 
        ("ddic_select_override" , ctypes.c_uint32, 1), # 6 to 6 
        ("ddic_clock_select"   , ctypes.c_uint32, 2), # 7 to 8 
        ("ddid_select_override" , ctypes.c_uint32, 1), # 9 to 9 
        ("ddid_clock_select"   , ctypes.c_uint32, 2), # 10 to 11 
        ("ddie_select_override" , ctypes.c_uint32, 1), # 12 to 12 
        ("ddie_clock_select"   , ctypes.c_uint32, 2), # 13 to 14 
        ("ddia_clock_off"      , ctypes.c_uint32, 1), # 15 to 15 
        ("ddib_clock_off"      , ctypes.c_uint32, 1), # 16 to 16 
        ("ddic_clock_off"      , ctypes.c_uint32, 1), # 17 to 17 
        ("ddid_clock_off"      , ctypes.c_uint32, 1), # 18 to 18 
        ("ddie_clock_off"      , ctypes.c_uint32, 1), # 19 to 19 
        ("dpll0_inverse_ref"   , ctypes.c_uint32, 1), # 20 to 20 
        ("dpll1_inverse_ref"   , ctypes.c_uint32, 1), # 21 to 21 
        ("dpll2_inverse_ref"   , ctypes.c_uint32, 1), # 22 to 22 
        ("dpll3_inverse_ref"   , ctypes.c_uint32, 1), # 23 to 23 
        ("reserved_24"         , ctypes.c_uint32, 8), # 24 to 31 
    ]

 
class DPLL_CTRL2_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_CTRL2_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
