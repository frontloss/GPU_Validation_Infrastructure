import ctypes
 
'''
Register instance and offset 
'''
PRE_CSC_GAMC_DATA_A = 0x4A488 
PRE_CSC_GAMC_DATA_B = 0x4AC88 
PRE_CSC_GAMC_DATA_C = 0x4B488
PRE_CSC_GAMC_DATA_D = 0x4BC88  

 
'''
Register field expected values 
'''
gamma_value_ = 0b0000000000000000000 

 
'''
Register bitfield defnition structure 
'''
class PRE_CSC_GAMC_DATA_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("gamma_value" , ctypes.c_uint32, 19), # 0 to 18 
        ("reserved_19" , ctypes.c_uint32, 13), # 19 to 31 
    ]

 
class PRE_CSC_GAMC_DATA_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PRE_CSC_GAMC_DATA_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
