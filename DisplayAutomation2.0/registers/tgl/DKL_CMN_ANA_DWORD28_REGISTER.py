import ctypes

'''
Register instance and offset
'''
DKL_CMN_ANA_DWORD28_D = 0x168130
DKL_CMN_ANA_DWORD28_E = 0x169130
DKL_CMN_ANA_DWORD28_F = 0x16A130
DKL_CMN_ANA_DWORD28_G = 0x16B130
DKL_CMN_ANA_DWORD28_H = 0x16C130
DKL_CMN_ANA_DWORD28_I = 0x16D130

'''
Register field expected values
'''

'''
Register bitfield definition structure
'''


class DKL_CMN_ANA_DWORD28_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("clktop1_plldivby2_2dmon_en_h", ctypes.c_uint32, 1),  # 0 to 0
        ("clktop1_divby2clk_bypass_en", ctypes.c_uint32, 1),  # 1 to 1
        ("clktop1_vga_clk_sel", ctypes.c_uint32, 1),  # 2 to 2
        ("clktop1_vga_clk2dl_en", ctypes.c_uint32, 1),  # 3 to 3
        ("clktop2_plldivby2_2dmon_en_h", ctypes.c_uint32, 1),  # 4 to 4
        ("clktop2_divby2clk_bypass_en", ctypes.c_uint32, 1),  # 5 to 5
        ("clktop2_vga_clk_sel", ctypes.c_uint32, 1),  # 6 to 6
        ("clktop2_vga_clk2dl_en", ctypes.c_uint32, 1),  # 7 to 7
        ("refclkin1_refclk_dlane_sel", ctypes.c_uint32, 2),  # 8 to 9
        ("refclkin1_refclk_sel", ctypes.c_uint32, 1),  # 10 to 10
        ("refclkin1_refclk_dlane_en", ctypes.c_uint32, 1),  # 11 to 11
        ("refclkin2_refclk_dlane_sel", ctypes.c_uint32, 2),  # 12 to 13
        ("refclkin2_refclk_sel", ctypes.c_uint32, 1),  # 14 to 14
        ("refclkin2_refclk_dlane_en", ctypes.c_uint32, 1),  # 15 to 15
        ("clktop1_id_vga_chpmp_ck_divratio", ctypes.c_uint32, 4),  # 16 to 19
        ("clktop1_id_vga_chpmp_div_en_h", ctypes.c_uint32, 1),  # 20 to 20
        ("Reserved", ctypes.c_uint32, 4),  # 21 to 24
        ("clktop2_id_vga_chpmp_ck_divratio", ctypes.c_uint32, 3),  # 25 to 27
        ("clktop2_id_vga_chpmp_div_en_h", ctypes.c_uint32, 1),  # 28 to 28
        ("Reserved", ctypes.c_uint32, 3)  # 30 to 31
    ]


class DKL_CMN_ANA_DWORD28_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_CMN_ANA_DWORD28_REG),
        ("asUint", ctypes.c_uint32)]
