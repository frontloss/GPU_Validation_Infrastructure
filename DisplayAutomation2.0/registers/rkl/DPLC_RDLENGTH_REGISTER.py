import ctypes
 
'''
Register instance and offset 
'''
DPLC_RDLENGTH_PARTA_A = 0x4943C
DPLC_RDLENGTH_PARTA_B = 0x494BC 
DPLC_RDLENGTH_PARTB_A = 0x49440 
DPLC_RDLENGTH_PARTB_B = 0x494C0 

 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class DPLC_RDLENGTH_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("read_length" , ctypes.c_uint32, 16), # 0 to 15 
        ("reserved_16" , ctypes.c_uint32, 16), # 16 to 31 
    ]

 
class DPLC_RDLENGTH_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      DPLC_RDLENGTH_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
