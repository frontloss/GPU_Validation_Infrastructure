import ctypes
 
'''
Register instance and offset 
'''
PLANE_CSC_PREOFF_1_A = 0x702A8 
PLANE_CSC_PREOFF_1_B = 0x712A8 
PLANE_CSC_PREOFF_1_C = 0x722A8 
PLANE_CSC_PREOFF_2_A = 0x703A8 
PLANE_CSC_PREOFF_2_B = 0x713A8 
PLANE_CSC_PREOFF_2_C = 0x723A8 
PLANE_CSC_PREOFF_3_A = 0x704A8 
PLANE_CSC_PREOFF_3_B = 0x714A8 
PLANE_CSC_PREOFF_3_C = 0x724A8 
PLANE_CSC_PREOFF_4_A = 0x705A8 
PLANE_CSC_PREOFF_4_B = 0x715A8 
PLANE_CSC_PREOFF_4_C = 0x725A8 
 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_CSC_PREOFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("precsc_offset" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"   , ctypes.c_uint32, 19), # 13 to 31
    ]

 
class PLANE_CSC_PREOFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_CSC_PREOFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
