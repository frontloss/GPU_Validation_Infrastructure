import ctypes

'''
Register instance and offset
'''

DKLP_CMN_ANA_CMN_ANA_DWORD7_TC1 = 0x1680DC
DKLP_CMN_ANA_CMN_ANA_DWORD7_TC2 = 0x1690DC
DKLP_CMN_ANA_CMN_ANA_DWORD7_TC3 = 0x16A0DC
DKLP_CMN_ANA_CMN_ANA_DWORD7_TC4 = 0x16B0DC

'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class DKLP_CMN_ANA_CMN_ANA_DWORD7_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('cfg_od_clktop2_coreclkc_divratio_7_0', ctypes.c_uint32, 8),  # 0 to 7
        ('cfg_od_clktop2_coreclkd_divratio_7_0', ctypes.c_uint32, 8),  # 8 to 15
        ('cfg_reserved533', ctypes.c_uint32, 1),  # 16 to 16
        ('cfg_od_clktop2_coreclke_divretimeren_h', ctypes.c_uint32, 1),  # 17 to 17
        ('cfg_od_clktop2_coreclke_bypass', ctypes.c_uint32, 1),  # 18 to 18
        ('cfg_reserved532', ctypes.c_uint32, 1),  # 19 to 19
        ('cfg_od_clktop2_coreclkf_divretimeren_h', ctypes.c_uint32, 1),  # 20 to 20
        ('cfg_od_clktop2_coreclkf_bypass', ctypes.c_uint32, 1),  # 21 to 21
        ('cfg_reserved531', ctypes.c_uint32, 2),  # 22 to 23
        ('cfg_od_clktop2_coreclke_divratio_7_0', ctypes.c_uint32, 8)  # 24 to 31
    ]


class DKLP_CMN_ANA_CMN_ANA_DWORD7_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_CMN_ANA_CMN_ANA_DWORD7_REG),
        ("asUint", ctypes.c_uint32)]
