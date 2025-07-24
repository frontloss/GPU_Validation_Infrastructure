import ctypes
 
'''
Register instance and offset 
'''
TRANS_DATAM1_A = 0x60030 
TRANS_DATAM1_B = 0x61030 
TRANS_DATAM1_C = 0x62030 
TRANS_DATAM1_D = 0x63030 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DATAM_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("data_m_value"        , ctypes.c_uint32, 24), # 23 to 0 
		("reserved_24",             ctypes.c_uint32,1), # 24 to 24 
        ("tu_or_vcpayload_size" , ctypes.c_uint32, 6), # 30 to 25 
		("reserved_31",             ctypes.c_uint32,1), # 31 to 31 
    ]

 
class DATAM_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DATAM_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
