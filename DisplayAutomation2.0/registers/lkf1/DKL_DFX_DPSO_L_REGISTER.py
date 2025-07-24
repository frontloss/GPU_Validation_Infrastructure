import ctypes

'''
Register instance and offset
'''

DKL_DFX_DPSO_L_NULL_D = 0x16822c
DKL_DFX_DPSO_L_NULL_E = 0x16922c

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKL_DFX_DPSO_L_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("i_init_cselafc", ctypes.c_uint32, 8),  # 0 to 7
        ("i_max_cselafc", ctypes.c_uint32, 8),  # 8 to 15
        ("i_fllafc_lockcnt", ctypes.c_uint32, 3),  # 16 to 18
        ("i_fllafc_gain", ctypes.c_uint32, 4),  # 19 to 22
        ("i_fastlock_en_h", ctypes.c_uint32, 1),  # 23 to 23
        ("i_bb_gain1", ctypes.c_uint32, 3),  # 24 to 26
        ("i_bb_gain2", ctypes.c_uint32, 3),  # 27 to 29
        ("i_cml2cmosbonus", ctypes.c_uint32, 2)  # 30 to 31
    ]


class DKL_DFX_DPSO_L_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKL_DFX_DPSO_L_REG),
        ("asUint", ctypes.c_uint32)]