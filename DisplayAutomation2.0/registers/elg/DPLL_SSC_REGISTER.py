import ctypes
 
'''
Register instance and offset 
'''
DPLL0_SSC = 0x164B10
DPLL1_SSC = 0x164C10
DPLL2_SSC = 0x16CB10
DPLL3_SSC = 0x16CC10
DPLL4_SSC = 0x164E10

 
'''
Register field expected values 
'''
bias_gb_sel_DEFAULT = 0x3 
init_dcoamp_DEFAULT = 0x3F 
iref_ndivratio_DEFAULT = 0x4 
sscen_DISABLE = 0b0 
sscen_ENABLE = 0b1 
sscinj_adapt_en_h_DISABLE = 0b0 
sscinj_adapt_en_h_ENABLE = 0b1 
sscinj_en_h_DISABLE = 0b0 
sscinj_en_h_ENABLE = 0b1 
sscstepnum_DEFAULT = 0x4 

 
'''
Register bitfield defnition structure 
'''
class DPLL_SSC_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("init_dcoamp"      , ctypes.c_uint32, 6), # 5 to 0 
        ("bias_gb_sel"      , ctypes.c_uint32, 2), # 7 to 6 
        ("sscfllen"         , ctypes.c_uint32, 1), # 8 to 8 
        ("sscen"            , ctypes.c_uint32, 1), # 9 to 9 
        ("ssc_openloop_en"  , ctypes.c_uint32, 1), # 10 to 10 
        ("sscstepnum"       , ctypes.c_uint32, 3), # 13 to 11 
        ("sscfll_update_sel" , ctypes.c_uint32, 2), # 15 to 14 
        ("sscsteplength"    , ctypes.c_uint32, 8), # 23 to 16 
        ("sscinj_en_h"      , ctypes.c_uint32, 1), # 24 to 24 
        ("sscinj_adapt_en_h" , ctypes.c_uint32, 1), # 25 to 25 
        ("sscstepnum_offset" , ctypes.c_uint32, 3), # 28 to 26 
        ("iref_ndivratio"   , ctypes.c_uint32, 3) # 31 to 29 
    ]

 
class DPLL_SSC_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLL_SSC_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
