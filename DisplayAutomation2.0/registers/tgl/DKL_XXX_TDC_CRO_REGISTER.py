import ctypes

'''
Register instance and offset
'''

DKL_XXX_TDC_CRO_NULL_D = 0x168228
DKL_XXX_TDC_CRO_NULL_E = 0x169228
DKL_XXX_TDC_CRO_NULL_F = 0x16A228
DKL_XXX_TDC_CRO_NULL_G = 0x16B228
DKL_XXX_TDC_CRO_NULL_H = 0x16C228
DKL_XXX_TDC_CRO_NULL_I = 0x16D228

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_XXX_TDC_CRO_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("I_TDCDC_EN_H", ctypes.c_uint32, 1),  # 0 to 0
        ("I_SWCAP_IREFGEN_CLKMODE_1_0", ctypes.c_uint32, 2),  # 1 to 2
        ("I_BBINLOCK_H", ctypes.c_uint32, 1),  # 3 to 3
        ("I_COLDSTART", ctypes.c_uint32, 1),  # 4 to 4
        ("I_IREFBIAS_STARTUP_PULSE_WIDTH_1_0", ctypes.c_uint32, 2),  # 5 to 6
        ("I_IREFBIAS_STARTUP_PULSE_BYPASS", ctypes.c_uint32, 1),  # 7 to 7
        ("I_IREFINT_EN", ctypes.c_uint32, 1),  # 8 to 8
        ("I_VGSBUFEN", ctypes.c_uint32, 1),  # 9 to 9
        ("I_DIGDFTSWEP", ctypes.c_uint32, 1),  # 10 to 10
        ("I_IREFDIGDFTEN", ctypes.c_uint32, 1),  # 11 to 11
        ("I_IREF_REFCLK_INV_EN", ctypes.c_uint32, 1),  # 12 to 12
        ("I_PLLLC_REGEN_H", ctypes.c_uint32, 1),  # 13 to 13
        ("I_PLLLC_EN_MODE_CTRL_1_0", ctypes.c_uint32, 2),  # 14 to 15
        ("I_PLLLC_RO_REGEN_H", ctypes.c_uint32, 1),  # 16 to 16
        ("I_PLLLC_RO_REGDISABLE", ctypes.c_uint32, 1),  # 17 to 17
        ("I_PLLLC_RO_MODE_CTRL", ctypes.c_uint32, 1),  # 18 to 18
        ("I_PLLLC_REG_RESETB_ANA_MODE_CTRL", ctypes.c_uint32, 1),  # 19 to 19
        ("I_PLLLC_REG_ACTIVE_STANDBY", ctypes.c_uint32, 1),  # 20 to 20
        ("I_PLLLC_REG_ACTIVE_STANDBY_MODE_CTRL", ctypes.c_uint32, 1),  # 21 to 21
        ("I_PLLLC_REG_REFCLK_ACK_MODE_CTRL", ctypes.c_uint32, 1),  # 22 to 22
        ("I_PLLLC_REG_REFCLK_ACK_MODE_CTRL", ctypes.c_uint32, 1),  # 23 to 23
        ("I_PLLLC_IREF_CLOCK_OVRD", ctypes.c_uint32, 1),  # 24 to 24
        ("I_PLLLC_IREF_CLOCK_SEL_1_0", ctypes.c_uint32, 2),  # 25 to 26
        ("I_DFX_MDITH_DISABLE", ctypes.c_uint32, 1),  # 27 to 27
        ("I_DFX_MDITH_DISABLE", ctypes.c_uint32, 1),  # 28 to 28
        ("I_DFX_MDFX_ENABLE", ctypes.c_uint32, 1),  # 29 to 29
        ("I_DFX_POSTDIV_DISABLE", ctypes.c_uint32, 1),  # 30 to 30
        ("I_PLLLC_REG_FULLCALRESETB", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DKL_XXX_TDC_CRO_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_XXX_TDC_CRO_REG),
        ("asUint", ctypes.c_uint32)]