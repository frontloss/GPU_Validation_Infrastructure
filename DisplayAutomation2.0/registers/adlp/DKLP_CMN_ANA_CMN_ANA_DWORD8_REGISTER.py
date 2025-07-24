import ctypes

'''
Register instance and offset
'''

DKLP_CMN_ANA_CMN_ANA_DWORD8_TC1 = 0x1680E0
DKLP_CMN_ANA_CMN_ANA_DWORD8_TC2 = 0x1690E0
DKLP_CMN_ANA_CMN_ANA_DWORD8_TC3 = 0x16A0E0
DKLP_CMN_ANA_CMN_ANA_DWORD8_TC4 = 0x16B0E0

'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class DKLP_CMN_ANA_CMN_ANA_DWORD8_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('cfg_od_clktop2_coreclkf_divratio_7_0', ctypes.c_uint32, 8),  # 0 to 7
        ('cfg_reserved536', ctypes.c_uint32, 1),  # 8 to 8
        ('cfg_od_clktop2_coreclkg_divretimeren_h', ctypes.c_uint32, 1),  # 9 to 9
        ('cfg_od_clktop2_coreclkg_bypass', ctypes.c_uint32, 1),  # 10 to 10
        ('cfg_reserved535', ctypes.c_uint32, 1),  # 11 to 11
        ('cfg_od_clktop2_coreclkh_divretimeren_h', ctypes.c_uint32, 1),  # 12 to 12
        ('cfg_od_clktop2_coreclkh_bypass', ctypes.c_uint32, 1),  # 13 to 13
        ('cfg_reserved534', ctypes.c_uint32, 2),  # 14 to 15
        ('cfg_od_clktop2_coreclkg_divratio_7_0', ctypes.c_uint32, 8),  # 16 to 23
        ('cfg_od_clktop2_coreclkh_divratio_7_0', ctypes.c_uint32, 8)  # 24 to 31
    ]


class DKLP_CMN_ANA_CMN_ANA_DWORD8_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_CMN_ANA_CMN_ANA_DWORD8_REG),
        ("asUint", ctypes.c_uint32)]
