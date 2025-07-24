import ctypes

'''
Register instance and offset
'''

DKLP_CMN_ANA_CMN_ANA_DWORD1_TC1 = 0x1680C4
DKLP_CMN_ANA_CMN_ANA_DWORD1_TC2 = 0x1690C4
DKLP_CMN_ANA_CMN_ANA_DWORD1_TC3 = 0x16A0C4
DKLP_CMN_ANA_CMN_ANA_DWORD1_TC4 = 0x16B0C4

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_CMN_ANA_CMN_ANA_DWORD1_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved_0", ctypes.c_uint32, 1),  # 0 to 0
        ("od_clktop1_coreclka_divretimeren_h", ctypes.c_uint32, 1),  # 1 to 1
        ("od_clktop1_coreclka_bypass", ctypes.c_uint32, 1),  # 2 to 2
        ("reserved_3", ctypes.c_uint32, 1),  # 3 to 3
        ("od_clktop1_coreclkb_divretimeren_h", ctypes.c_uint32, 1),  # 4 to 4
        ("od_clktop1_coreclkb_bypass", ctypes.c_uint32, 1),  # 5 to 5
        ("cfg_on_pll12coreclka_select", ctypes.c_uint32, 1),  # 6 to 6
        ("cfg_on_pll12coreclkd_select", ctypes.c_uint32, 1),  # 7 to 7
        ("od_clktop1_coreclka_divratio", ctypes.c_uint32, 8) , # 8 to 15
        ("od_clktop1_coreclkb_divratio", ctypes.c_uint32, 8),  # 16 to 23
        ("reserved_24", ctypes.c_uint32, 1),  # 24 to 24
        ("od_clktop1_coreclkc_divretimeren_h", ctypes.c_uint32, 1),  # 25 to 25
        ("od_clktop1_coreclkc_bypass", ctypes.c_uint32, 1),  # 26 to 26
        ("reserved_27", ctypes.c_uint32, 1),  # 27 to 27
        ("od_clktop1_coreclkd_divretimeren_h", ctypes.c_uint32, 1),  # 28 to 28
        ("od_clktop1_coreclkd_bypass", ctypes.c_uint32, 1),  # 29 to 29
        ("reserved_30", ctypes.c_uint32, 2)  # 30 to 31
    ]


class DKLP_CMN_ANA_CMN_ANA_DWORD1_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_CMN_ANA_CMN_ANA_DWORD1_REG),
        ("asUint", ctypes.c_uint32)]
