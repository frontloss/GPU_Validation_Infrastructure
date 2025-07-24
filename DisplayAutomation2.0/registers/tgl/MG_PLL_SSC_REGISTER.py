import ctypes

'''
Register instance and offset
'''
MG_PLL1_SSC_PORT1 = 0x168A10
MG_PLL1_SSC_PORT2 = 0x169A10
MG_PLL1_SSC_PORT3 = 0x16AA10
MG_PLL1_SSC_PORT4 = 0x16BA10

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class MG_PLL_SSC_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_sscstepsize", ctypes.c_uint32, 8),  # 0 to 7
        ("i_afc_startup2", ctypes.c_uint32, 1),  # 8 to 8
        ("i_s_sscfll_en_h", ctypes.c_uint32, 1),  # 9 to 9
        ("i_sscstepnum", ctypes.c_uint32, 3),  # 10 to 12
        ("reserved_13", ctypes.c_uint32, 3),  # 13 to 15
        ("i_sscsteplength", ctypes.c_uint32, 10),  # 16 to 25
        ("i_ssctype", ctypes.c_uint32, 2),  # 26 to 27
        ("i_sscen_h", ctypes.c_uint32, 1),  # 28 to 28
        ("i_rampafc_sscen_h", ctypes.c_uint32, 1),  # 29 to 29
        ("i_ssc_strobe_h", ctypes.c_uint32, 1),  # 30 to 30
        ("i_ssc_openloop_en_h", ctypes.c_uint32, 1)  # 31 to 31
    ]


class MG_PLL_SSC_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", MG_PLL_SSC_REG),
        ("asUint", ctypes.c_uint32)]