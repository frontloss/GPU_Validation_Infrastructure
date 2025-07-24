import ctypes
 
'''
Register instance and offset 
'''
DKL_TDC_COLDST_BIAS_D = 0x168218
DKL_TDC_COLDST_BIAS_E = 0x169218
DKL_TDC_COLDST_BIAS_F = 0x16A218
DKL_TDC_COLDST_BIAS_G= 0x16B218
DKL_TDC_COLDST_BIAS_H = 0x16C218
DKL_TDC_COLDST_BIAS_I = 0x16D218

'''
Register bitfield defnition structure 
'''
class DKL_TDC_COLDST_BIAS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("i_feedfwdgain_7_0",           ctypes.c_uint32,8), # 0 to 7
        ("i_sscstepsize_7_0",           ctypes.c_uint32,8), # 8 to 15
        ("si_dcocoarse_7_0",            ctypes.c_uint32,8), # 16 to 23
        ("i_tribufctrlext_4_0",         ctypes.c_uint32,5), # 24 to 28
        ("i_cloadctrlext_4_2",          ctypes.c_uint32,3) # 29 to 31
    ]

 
class DKL_TDC_COLDST_BIAS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DKL_TDC_COLDST_BIAS_REG ),
        ("asUint", ctypes.c_uint32 ) ]