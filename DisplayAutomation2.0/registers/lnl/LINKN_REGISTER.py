import ctypes
 
'''
Register instance and offset 
'''
TRANS_LINKN1_A = 0x60044 
TRANS_LINKN1_B = 0x61044 
TRANS_LINKN1_C = 0x62044 
TRANS_LINKN1_D = 0x63044
TRANS_LINKN1_CMTG0 = 0x6F044
TRANS_LINKN1_CMTG1 = 0x6F144

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class LINKN_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("link_n_value" , ctypes.c_uint32, 24), # 0 to 23 
        ("extended_link_n_value" , ctypes.c_uint32, 8), # 24 to 31
    ]

 
class LINKN_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      LINKN_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
