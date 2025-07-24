import ctypes
 
'''
Register instance and offset 
'''
PLANE_COLOR_CTL_1_A = 0x701CC 
PLANE_COLOR_CTL_1_B = 0x711CC 
PLANE_COLOR_CTL_1_C = 0x721CC
PLANE_COLOR_CTL_2_A = 0x702CC 
PLANE_COLOR_CTL_2_B = 0x712CC  
PLANE_COLOR_CTL_2_C = 0x722CC 
PLANE_COLOR_CTL_3_A = 0x703CC 
PLANE_COLOR_CTL_3_B = 0x713CC   
PLANE_COLOR_CTL_3_C = 0x723CC  
PLANE_COLOR_CTL_4_A = 0x704CC 
PLANE_COLOR_CTL_4_B = 0x714CC    
PLANE_COLOR_CTL_4_C = 0x724CC 
PLANE_COLOR_CTL_5_A = 0x705CC 
PLANE_COLOR_CTL_5_B = 0x715CC 
PLANE_COLOR_CTL_5_C = 0x725CC 
PLANE_COLOR_CTL_6_A = 0x706CC 
PLANE_COLOR_CTL_6_B = 0x716CC   
PLANE_COLOR_CTL_6_C = 0x726CC 
PLANE_COLOR_CTL_7_A = 0x707CC 
PLANE_COLOR_CTL_7_B = 0x717CC 
PLANE_COLOR_CTL_7_C = 0x727CC
PLANE_COLOR_CTL_1_D = 0x731CC   
PLANE_COLOR_CTL_2_D = 0x732CC 
PLANE_COLOR_CTL_3_D = 0x733CC 
PLANE_COLOR_CTL_4_D = 0x734CC 
PLANE_COLOR_CTL_5_D = 0x735CC 
PLANE_COLOR_CTL_6_D = 0x736CC   
PLANE_COLOR_CTL_7_D = 0x737CC
 
'''
Register field expected values 
'''

 
'''
Register bitfield defnition structure 
'''
class PLANE_COLOR_CTL_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("reserved_0",                      ctypes.c_uint32,4), # 0 to 3 
        ("alpha_mode",                      ctypes.c_uint32,2), # 4 to 5 
        ("reserved_6",                      ctypes.c_uint32,6), # 6 to 11 
        ("plane_gamma_mode",                ctypes.c_uint32,1), # 12 to 12
        ("plane_gamma_disable",             ctypes.c_uint32,1), # 13 to 13 
        ("plane_pre_csc_gamma_enable",      ctypes.c_uint32,1), # 14 to 14 
        ("reserved_15",                     ctypes.c_uint32,2), # 15 to 16 
        ("plane_csc_mode",                  ctypes.c_uint32,3), # 17 to 19 
        ("plane_input_csc_enable",          ctypes.c_uint32,1), # 20 to 20
        ("plane_csc_enable",                ctypes.c_uint32,1), # 21 to 21
        ("yuv_range_correction_output",     ctypes.c_uint32,1), # 22 to 22 
        ("pipe_csc_enable",                 ctypes.c_uint32,1), # 23 to 23 
        ("reserved_24",                     ctypes.c_uint32,4), # 24 to 27 
        ("yuv_range_correction_disable",    ctypes.c_uint32,1), # 28 to 28 
        ("remove_yuv_offset",               ctypes.c_uint32,1), # 29 to 29 
        ("pipe_gamma_enable",               ctypes.c_uint32,1), # 30 to 30 
        ("reserved_31",                     ctypes.c_uint32,1), # 31 to 31 
    ]

 
class PLANE_COLOR_CTL_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_COLOR_CTL_REG ),
        ("asUint", ctypes.c_uint32 ) ]