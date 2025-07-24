import ctypes

'''
Register instance and offset
'''

DPLL0_SSC = 0x164B10
DPLL1_SSC = 0x164C10
DPLL4_SSC = 0x164E10

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DPLL_SSC_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("init_dcoamp", ctypes.c_uint32, 6),  # 0 to 5
        ("bias_gb_sel", ctypes.c_uint32, 2),  # 6 to 7
        ("sscfllen", ctypes.c_uint32, 1),  # 8 to 8
        ("sscen", ctypes.c_uint32, 1),  # 9 to 9
        ("ssc_openloop_en", ctypes.c_uint32, 1),  # 10 to 10
        ("sscstepnum", ctypes.c_uint32, 3),  # 11 to 13
        ("sscfll_update_sel", ctypes.c_uint32, 2),  # 14 to 15
        ("sscsteplength", ctypes.c_uint32, 8),  # 16 to 23
        ("sscinj_en_h", ctypes.c_uint32, 1),  # 24 to 24
        ("sscinj_adapt_en_h", ctypes.c_uint32, 1),  # 25 to 25
        ("sscstepnum_offset", ctypes.c_uint32, 3),  # 26 to 28
        ("iref_ndivratio", ctypes.c_uint32, 3)  # 29 to 31
    ]


class DPLL_SSC_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DPLL_SSC_REG),
        ("asUint", ctypes.c_uint32)]