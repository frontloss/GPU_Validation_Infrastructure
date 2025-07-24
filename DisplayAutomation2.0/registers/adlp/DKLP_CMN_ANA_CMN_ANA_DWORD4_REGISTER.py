import ctypes

'''
Register instance and offset
'''

DKLP_CMN_ANA_CMN_ANA_DWORD4_TC1 = 0x1680D0
DKLP_CMN_ANA_CMN_ANA_DWORD4_TC2 = 0x1690D0
DKLP_CMN_ANA_CMN_ANA_DWORD4_TC3 = 0x16A0D0
DKLP_CMN_ANA_CMN_ANA_DWORD4_TC4 = 0x16B0D0

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_CMN_ANA_CMN_ANA_DWORD4_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reg_value", ctypes.c_uint32, 32)  # 0 to 31
    ]


class DKLP_CMN_ANA_CMN_ANA_DWORD4_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_CMN_ANA_CMN_ANA_DWORD4_REG),
        ("asUint", ctypes.c_uint32)]