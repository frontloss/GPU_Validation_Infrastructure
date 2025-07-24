import ctypes

'''
Register instance and offset
'''

DKL_SSC_L_NULL_D = 0x168210
DKL_SSC_L_NULL_E = 0x169210

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_SSC_L_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_sscstepsize_7_0", ctypes.c_uint32, 8),  # 0 to 7
        ("i_sscstepsize_9_8", ctypes.c_uint32, 2),  # 8 to 9
        ("i_sscstepnum", ctypes.c_uint32, 3),  # 10 to 12
        ("reserved_13", ctypes.c_uint32, 3),  # 13 to 15
        ("i_sscsteplength_7_0", ctypes.c_uint32, 8),  # 16 to 23
        ("i_sscsteplength_9_8", ctypes.c_uint32, 2),  # 24 to 25
        ("i_ssctype", ctypes.c_uint32, 2),  # 26 to 27
        ("i_sscen_h", ctypes.c_uint32, 1),  # 28 to 28
        ("i_rampafc_sscen_h", ctypes.c_uint32, 1),  # 29 to 29
        ("i_ssc_strobe_h", ctypes.c_uint32, 1),  # 30 to 30
        ("i_ssc_openloop_en_h", ctypes.c_uint32, 1)  # 31 to 31
    ]


class DKL_SSC_L_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_SSC_L_REG),
        ("asUint", ctypes.c_uint32)]