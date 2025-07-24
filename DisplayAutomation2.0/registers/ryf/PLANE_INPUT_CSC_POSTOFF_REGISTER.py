import ctypes
 
'''
Register instance and offset 
'''
PLANE_INPUT_CSC_POSTOFF_1_A = 0x70284 
PLANE_INPUT_CSC_POSTOFF_1_B = 0x71284 
PLANE_INPUT_CSC_POSTOFF_1_C = 0x72284 
PLANE_INPUT_CSC_POSTOFF_2_A = 0x70384 
PLANE_INPUT_CSC_POSTOFF_2_B = 0x71384 
PLANE_INPUT_CSC_POSTOFF_2_C = 0x72384 
PLANE_INPUT_CSC_POSTOFF_3_A = 0x70484 
PLANE_INPUT_CSC_POSTOFF_3_B = 0x71484 
PLANE_INPUT_CSC_POSTOFF_3_C = 0x72484 
PLANE_INPUT_CSC_POSTOFF_4_A = 0x70584 
PLANE_INPUT_CSC_POSTOFF_4_B = 0x71584 
PLANE_INPUT_CSC_POSTOFF_4_C = 0x72584 
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_INPUT_CSC_POSTOFF_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("postcsc_offset"  , ctypes.c_uint32, 13), # 0 to 12 
        ("reserved_13"     , ctypes.c_uint32, 19), # 13 to 31 
    ]

 
class PLANE_INPUT_CSC_POSTOFF_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_INPUT_CSC_POSTOFF_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
