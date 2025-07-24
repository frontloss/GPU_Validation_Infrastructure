import ctypes
 
'''
Register instance and offset 
'''
DKLP_PLL0_TDC_COLDST_BIAS_TC1 = 0x168198
DKLP_PLL0_TDC_COLDST_BIAS_TC2 = 0x169198
DKLP_PLL0_TDC_COLDST_BIAS_TC3 = 0x16A198
DKLP_PLL0_TDC_COLDST_BIAS_TC4 = 0x16B198

DKLP_PLL1_TDC_COLDST_BIAS_TC1 = 0x168218
DKLP_PLL1_TDC_COLDST_BIAS_TC2 = 0x169218
DKLP_PLL1_TDC_COLDST_BIAS_TC3 = 0x16A218
DKLP_PLL1_TDC_COLDST_BIAS_TC4 = 0x16B218

'''
Register bitfield defnition structure 
'''
class DKLP_PLL_TDC_COLDST_BIAS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("i_feedfwdgain_7_0",           ctypes.c_uint32,8), # 0 to 7
        ("i_sscstepsize_7_0",           ctypes.c_uint32,8), # 8 to 15
        ("si_dcocoarse_7_0",            ctypes.c_uint32,8), # 16 to 23
        ("i_tribufctrlext_4_0",         ctypes.c_uint32,5), # 24 to 28
        ("i_cloadctrlext_4_2",          ctypes.c_uint32,3) # 29 to 31
    ]

 
class DKLP_PLL_TDC_COLDST_BIAS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DKLP_PLL_TDC_COLDST_BIAS_REG ),
        ("asUint", ctypes.c_uint32 ) ]