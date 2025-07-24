import ctypes

'''
Register instance and offset
'''

DKLP_CMN_ANA_CMN_ANA_DWORD28_TC1 = 0x168130
DKLP_CMN_ANA_CMN_ANA_DWORD28_TC2 = 0x169130
DKLP_CMN_ANA_CMN_ANA_DWORD28_TC3 = 0x16A130
DKLP_CMN_ANA_CMN_ANA_DWORD28_TC4 = 0x16B130

'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class DKLP_CMN_ANA_CMN_ANA_DWORD28_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('cfg_clktop1_plldivby2_2dmon_en_h', ctypes.c_uint32, 1),  # 0 to 0
        ('cfg_clktop1_divby2clk_bypass_en', ctypes.c_uint32, 1),  # 1 to 1
        ('cfg_clktop1_vga_clk_sel', ctypes.c_uint32, 1),  # 2 to 2
        ('cfg_clktop1_vga_clk2dl_en', ctypes.c_uint32, 1),  # 3 to 3
        ('cfg_clktop2_plldivby2_2dmon_en_h', ctypes.c_uint32, 1),  # 4 to 4
        ('cfg_clktop2_divby2clk_bypass_en', ctypes.c_uint32, 1),  # 5 to 5
        ('cfg_clktop2_vga_clk_sel', ctypes.c_uint32, 1),  # 6 to 6
        ('cfg_clktop2_vga_clk2dl_en', ctypes.c_uint32, 1),  # 7 to 7
        ('cfg_refclkin1_refclk_dlane_sel', ctypes.c_uint32, 2),  # 8 to 9
        ('cfg_refclkin1_refclk_sel', ctypes.c_uint32, 1),  # 10 to 10
        ('cfg_refclkin1_refclk_dlane_en', ctypes.c_uint32, 1),  # 11 to 11
        ('cfg_refclkin2_refclk_dlane_sel', ctypes.c_uint32, 2),  # 12 to 13
        ('cfg_refclkin2_refclk_sel', ctypes.c_uint32, 1),  # 14 to 14
        ('cfg_refclkin2_refclk_dlane_en', ctypes.c_uint32, 1),  # 15 to 15
        ('cfg_clktop1_id_vga_chpmp_ck_divratio', ctypes.c_uint32, 4),  # 16 to 19
        ('cfg_clktop1_id_vga_chpmp_div_en_h', ctypes.c_uint32, 1),  # 20 to 20
        ('cfg_clktop2_id_vga_chpmp_ck_divratio', ctypes.c_uint32, 4),  # 24 to 27
        ('cfg_clktop2_id_vga_chpmp_div_en_h', ctypes.c_uint32, 1)  # 28 to 28
    ]


class DKLP_CMN_ANA_CMN_ANA_DWORD28_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_CMN_ANA_CMN_ANA_DWORD28_REG),
        ("asUint", ctypes.c_uint32)]
