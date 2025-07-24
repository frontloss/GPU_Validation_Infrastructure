import ctypes

'''
Register instance and offset
'''

DKLP_CMN_ANA_CMN_ANA_DWORD3_TC1 = 0x1680CC
DKLP_CMN_ANA_CMN_ANA_DWORD3_TC2 = 0x1690CC
DKLP_CMN_ANA_CMN_ANA_DWORD3_TC3 = 0x16A0CC
DKLP_CMN_ANA_CMN_ANA_DWORD3_TC4 = 0x16B0CC

'''
Register field expected values
'''

'''
Register bitfield defnition structure
'''


class DKLP_CMN_ANA_CMN_ANA_DWORD3_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reg_value", ctypes.c_uint32, 32)  # 0 to 31
    ]


class DKLP_CMN_ANA_CMN_ANA_DWORD3_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_CMN_ANA_CMN_ANA_DWORD3_REG),
        ("asUint", ctypes.c_uint32)]