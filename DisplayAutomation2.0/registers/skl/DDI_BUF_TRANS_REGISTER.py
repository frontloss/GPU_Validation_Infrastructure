import ctypes
 
'''
Register instance and offset 
'''
DDI_BUF_TRANS_A = 0x64E00
DDI_BUF_TRANS_B = 0x64E60
DDI_BUF_TRANS_B_ENTRY9_DWORD0 = 0x64EA8
DDI_BUF_TRANS_B_ENTRY9_DWORD1 = 0x64EAC
DDI_BUF_TRANS_C = 0x64EC0
DDI_BUF_TRANS_C_ENTRY9_DWORD0 = 0x64F08
DDI_BUF_TRANS_C_ENTRY9_DWORD1 = 0x64F0C
DDI_BUF_TRANS_D = 0x64F20
DDI_BUF_TRANS_D_ENTRY9_DWORD0 = 0x64F68
DDI_BUF_TRANS_D_ENTRY9_DWORD1 = 0x64F6C
DDI_BUF_TRANS_E = 0x64F80


 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DDI_BUF_TRANS_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("dword", ctypes.c_uint32, 32), # 0 to 31
    ]

 
class DDI_BUF_TRANS_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DDI_BUF_TRANS_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
