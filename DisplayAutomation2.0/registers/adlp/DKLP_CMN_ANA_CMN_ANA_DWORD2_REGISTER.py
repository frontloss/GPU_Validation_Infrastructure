import ctypes

'''
Register instance and offset
'''

DKLP_CMN_ANA_CMN_ANA_DWORD2_TC1 = 0x1680C8
DKLP_CMN_ANA_CMN_ANA_DWORD2_TC2 = 0x1690C8
DKLP_CMN_ANA_CMN_ANA_DWORD2_TC3 = 0x16A0C8
DKLP_CMN_ANA_CMN_ANA_DWORD2_TC4 = 0x16B0C8

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_CMN_ANA_CMN_ANA_DWORD2_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("od_clktop1_coreclkc_divratio_7_0",        ctypes.c_uint32, 8),  # 0 to 7
        ("od_clktop1_coreclkd_divratio_7_0",        ctypes.c_uint32, 8),  # 8 to 15
        ("reserved_16",                             ctypes.c_uint32, 1),  # 16 to 16
        ("od_clktop1_coreclke_divretimeren_h",      ctypes.c_uint32, 1),  # 17 to 17
        ("od_clktop1_coreclke_bypass",              ctypes.c_uint32, 1),  # 18 to 18
        ("reserved_19",                             ctypes.c_uint32, 1),  # 19 to 19
        ("od_clktop1_coreclkf_divretimeren_h",      ctypes.c_uint32, 1),  # 20 to 20
        ("od_clktop1_coreclkf_bypass",              ctypes.c_uint32, 1),  # 21 to 21
        ("reserved_22",                             ctypes.c_uint32, 2),  # 22 to 23
        ("od_clktop1_coreclke_divratio_7_0",        ctypes.c_uint32, 8)   # 24 to 31
    ]


class DKLP_CMN_ANA_CMN_ANA_DWORD2_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_CMN_ANA_CMN_ANA_DWORD2_REG),
        ("asUint", ctypes.c_uint32)]