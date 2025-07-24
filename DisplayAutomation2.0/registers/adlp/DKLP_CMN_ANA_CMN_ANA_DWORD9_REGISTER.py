import ctypes

'''
Register instance and offset
'''

DKLP_CMN_ANA_CMN_ANA_DWORD9_TC1 = 0x1680E4
DKLP_CMN_ANA_CMN_ANA_DWORD9_TC2 = 0x1690E4
DKLP_CMN_ANA_CMN_ANA_DWORD9_TC3 = 0x16A0E4
DKLP_CMN_ANA_CMN_ANA_DWORD9_TC4 = 0x16B0E4

'''
Register field expected values
'''

'''
Register bitfield definition structure
'''

class DKLP_CMN_ANA_CMN_ANA_DWORD9_REG(ctypes.LittleEndianStructure):
    _fields_ = [
        ('value', ctypes.c_uint32)
    ]

class DKLP_CMN_ANA_CMN_ANA_DWORD9_REGISTER(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DKLP_CMN_ANA_CMN_ANA_DWORD9_REG),
        ("asUint", ctypes.c_uint32)]
