import ctypes
 
'''
Register instance and offset 
'''
TRANS_DATAN1_A = 0x60034 
TRANS_DATAN1_B = 0x61034 
TRANS_DATAN1_C = 0x62034 
TRANS_DATAN1_D = 0x63034 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DATAN_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("data_n_value",        ctypes.c_uint32,24), # 0 to 23 
        ("reserved_24",         ctypes.c_uint32,8), # 24 to 31 
    ]

 
class DATAN_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DATAN_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
