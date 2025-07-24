import ctypes
 
'''
Register instance and offset 
'''
TRANS_LINKM1_A = 0x60040 
TRANS_LINKM1_B = 0x61040 
TRANS_LINKM1_C = 0x62040 
TRANS_LINKM1_D = 0x63040
TRANS_LINKM1_CMTG = 0x6F040

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class LINKM_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("link_m_value" , ctypes.c_uint32, 24), # 0 to 23 
        ("reserved_24" , ctypes.c_uint32, 8), # 24 to 31 
    ]

 
class LINKM_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      LINKM_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
