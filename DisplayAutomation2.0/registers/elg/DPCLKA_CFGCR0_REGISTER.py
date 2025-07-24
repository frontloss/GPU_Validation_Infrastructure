import ctypes
 
'''
Register instance and offset 
'''
DPCLKA_CFGCR0 = 0x164280

 
'''
Register field expected values 
'''
ddia_clock_off_OFF = 0b1 
ddia_clock_off_ON = 0b0 
ddia_clock_select_DPLL0 = 0b00 
ddia_clock_select_DPLL1 = 0b01 
ddia_clock_select_DPLL4 = 0b10 
ddia_clock_select_LJPLL0 = 0b10 
ddia_clock_select_LJPLL1 = 0b11 
ddib_clock_off_OFF = 0b1 
ddib_clock_off_ON = 0b0 
ddib_clock_select_DPLL0 = 0b00 
ddib_clock_select_DPLL1 = 0b01 
ddib_clock_select_DPLL4 = 0b10 
ddib_clock_select_LJPLL0 = 0b10 
ddib_clock_select_LJPLL1 = 0b11 
ddic_clock_off_OFF = 0b1 
ddic_clock_off_ON = 0b0 
ddic_clock_select_DPLL0 = 0b00 
ddic_clock_select_DPLL1 = 0b01 
ddic_clock_select_DPLL4 = 0b10 
dpll0_enable_override_FORCE_ENABLE = 0b1 
dpll0_enable_override_NOT_FORCED = 0b0 
dpll0_inverse_ref_INVERSE = 0b1 
dpll0_inverse_ref_NOT_INVERSE = 0b0 
dpll1_enable_override_FORCE_ENABLE = 0b1 
dpll1_enable_override_NOT_FORCED = 0b0 
dpll1_inverse_ref_INVERSE = 0b1 
dpll1_inverse_ref_NOT_INVERSE = 0b0 
dpll3_inverse_ref_INVERSE = 0b1 
dpll3_inverse_ref_NOT_INVERSE = 0b0 
dpll4_enable_override_FORCE_ENABLE = 0b1 
dpll4_enable_override_NOT_FORCED = 0b0 
dpll4_inverse_ref_INVERSE = 0b1 
dpll4_inverse_ref_NOT_INVERSE = 0b0 
iref_inverse_ref_INVERSE = 0b1 
iref_inverse_ref_NOT_INVERSE = 0b0 
tbtpll_enable_override_FORCE_ENABLE = 0b1 
tbtpll_enable_override_NOT_FORCED = 0b0 
tbtpll_inverse_ref_INVERSE = 0b1 
tbtpll_inverse_ref_NOT_INVERSE = 0b0 
tc1_clock_off_OFF = 0b1 
tc1_clock_off_ON = 0b0 
tc2_clock_off_OFF = 0b1 
tc2_clock_off_ON = 0b0 
tc3_clock_off_OFF = 0b1 
tc3_clock_off_ON = 0b0 
tc4_clock_off_OFF = 0b1 
tc4_clock_off_ON = 0b0 
tc5_clock_off_OFF = 0b1 
tc5_clock_off_ON = 0b0 
tc6_clock_off_OFF = 0b1 
tc6_clock_off_ON = 0b0 

 
'''
Register bitfield defnition structure 
'''
class DPCLKA_CFGCR0_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("ddia_clock_select"          , ctypes.c_uint32, 2), # 1 to 0 
        ("ddib_clock_select"          , ctypes.c_uint32, 2), # 3 to 2 
        ("ddic_clock_select"          , ctypes.c_uint32, 2), # 5 to 4 
        ("mipia_hvm_sel"              , ctypes.c_uint32, 2), # 7 to 6 
        ("mipic_hvm_sel"              , ctypes.c_uint32, 2), # 9 to 8 
        ("ddia_clock_off"             , ctypes.c_uint32, 1), # 10 to 10 
        ("ddib_clock_off"             , ctypes.c_uint32, 1), # 11 to 11 
        ("tc1_clock_off"              , ctypes.c_uint32, 1), # 12 to 12 
        ("tc2_clock_off"              , ctypes.c_uint32, 1), # 13 to 13 
        ("tc3_clock_off"              , ctypes.c_uint32, 1), # 14 to 14 
        ("dpll0_inverse_ref"          , ctypes.c_uint32, 1), # 15 to 15 
        ("dpll1_inverse_ref"          , ctypes.c_uint32, 1), # 16 to 16 
        ("tbtpll_inverse_ref"         , ctypes.c_uint32, 1), # 17 to 17 
        ("dpll0_enable_override"      , ctypes.c_uint32, 1), # 18 to 18 
        ("dpll1_enable_override"      , ctypes.c_uint32, 1), # 19 to 19 
        ("dpll4_enable_override"      , ctypes.c_uint32, 1), # 20 to 20 
        ("tc4_clock_off"              , ctypes.c_uint32, 1), # 21 to 21 
        ("tc5_clock_off"              , ctypes.c_uint32, 1), # 22 to 22 
        ("tc6_clock_off"              , ctypes.c_uint32, 1), # 23 to 23 
        ("ddic_clock_off"             , ctypes.c_uint32, 1), # 24 to 24 
        ("dpll3_inverse_ref"          , ctypes.c_uint32, 1), # 25 to 25 
        ("dpll4_inverse_ref"          , ctypes.c_uint32, 1), # 26 to 26
		("reserved_27", ctypes.c_uint32, 2),  # 28 to 27 
        ("hvm_independent_mipi_enable" , ctypes.c_uint32, 1), # 29 to 29 
        ("iref_inverse_ref"           , ctypes.c_uint32, 1), # 30 to 30 
        ("tbtpll_enable_override"     , ctypes.c_uint32, 1), # 31 to 31 
    ]

 
class DPCLKA_CFGCR0_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPCLKA_CFGCR0_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
