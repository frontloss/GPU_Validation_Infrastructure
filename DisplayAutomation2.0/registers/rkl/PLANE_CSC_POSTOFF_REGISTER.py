import ctypes
 
'''
Register instance and offset 
'''
PLANE_CSC_POSTOFF_1_A = 0x702B4 
PLANE_CSC_POSTOFF_1_B = 0x712B4 
PLANE_CSC_POSTOFF_1_C = 0x722B4 
PLANE_CSC_POSTOFF_2_A = 0x703B4 
PLANE_CSC_POSTOFF_2_B = 0x713B4 
PLANE_CSC_POSTOFF_2_C = 0x723B4 
PLANE_CSC_POSTOFF_3_A = 0x704B4 
PLANE_CSC_POSTOFF_3_B = 0x714B4 
PLANE_CSC_POSTOFF_3_C = 0x724B4 
PLANE_CSC_POSTOFF_4_A = 0x705B4 
PLANE_CSC_POSTOFF_4_B = 0x715B4 
PLANE_CSC_POSTOFF_4_C = 0x725B4 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_CSC_POSTOFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("postcsc_offset"  , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"     , ctypes.c_uint32, 19), # 13 to 31 
    ]

 
class PLANE_CSC_POSTOFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_CSC_POSTOFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
