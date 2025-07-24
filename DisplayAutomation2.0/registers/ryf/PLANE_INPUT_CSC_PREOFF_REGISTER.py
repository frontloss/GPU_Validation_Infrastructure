import ctypes
 
'''
Register instance and offset 
'''
PLANE_INPUT_CSC_PREOFF_1_A = 0x701F8 
PLANE_INPUT_CSC_PREOFF_1_B = 0x711F8 
PLANE_INPUT_CSC_PREOFF_1_C = 0x721F8 
PLANE_INPUT_CSC_PREOFF_2_A = 0x702F8 
PLANE_INPUT_CSC_PREOFF_2_B = 0x712F8 
PLANE_INPUT_CSC_PREOFF_2_C = 0x722F8 
PLANE_INPUT_CSC_PREOFF_3_A = 0x703F8 
PLANE_INPUT_CSC_PREOFF_3_B = 0x713F8 
PLANE_INPUT_CSC_PREOFF_3_C = 0x723F8 
PLANE_INPUT_CSC_PREOFF_4_A = 0x704F8 
PLANE_INPUT_CSC_PREOFF_4_B = 0x714F8 
PLANE_INPUT_CSC_PREOFF_4_C = 0x724F8 
 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_INPUT_CSC_PREOFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("precsc_offset" , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"   , ctypes.c_uint32, 19), # 13 to 31 
    ]

 
class PLANE_INPUT_CSC_PREOFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_INPUT_CSC_PREOFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
