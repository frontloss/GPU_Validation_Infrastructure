import ctypes
 
'''
Register instance and offset 
'''
PLANE_POST_CSC_GAMC_INDEX_1_A = 0x701D8 
PLANE_POST_CSC_GAMC_INDEX_1_B = 0x711D8 
PLANE_POST_CSC_GAMC_INDEX_1_C = 0x721D8
PLANE_POST_CSC_GAMC_INDEX_1_D = 0x731D8  
PLANE_POST_CSC_GAMC_INDEX_2_A = 0x702D8 
PLANE_POST_CSC_GAMC_INDEX_2_B = 0x712D8 
PLANE_POST_CSC_GAMC_INDEX_2_C = 0x722D8
PLANE_POST_CSC_GAMC_INDEX_2_D = 0x732D8 
PLANE_POST_CSC_GAMC_INDEX_3_A = 0x703D8 
PLANE_POST_CSC_GAMC_INDEX_3_B = 0x713D8 
PLANE_POST_CSC_GAMC_INDEX_3_C = 0x723D8 
PLANE_POST_CSC_GAMC_INDEX_3_D = 0x733D8 
PLANE_POST_CSC_GAMC_INDEX_4_A = 0x704D8 
PLANE_POST_CSC_GAMC_INDEX_4_B = 0x714D8 
PLANE_POST_CSC_GAMC_INDEX_4_C = 0x724D8 
PLANE_POST_CSC_GAMC_INDEX_4_D = 0x734D8 
PLANE_POST_CSC_GAMC_INDEX_5_A = 0x705D8 
PLANE_POST_CSC_GAMC_INDEX_5_B = 0x715D8 
PLANE_POST_CSC_GAMC_INDEX_5_C = 0x725D8 
PLANE_POST_CSC_GAMC_INDEX_5_D = 0x735D8
PLANE_POST_CSC_GAMC_INDEX_6_A = 0x706D8 
PLANE_POST_CSC_GAMC_INDEX_6_B = 0x716D8 
PLANE_POST_CSC_GAMC_INDEX_6_C = 0x726D8 
PLANE_POST_CSC_GAMC_INDEX_6_D = 0x736D8
PLANE_POST_CSC_GAMC_INDEX_7_A = 0x707D8 
PLANE_POST_CSC_GAMC_INDEX_7_B = 0x717D8 
PLANE_POST_CSC_GAMC_INDEX_7_C = 0x727D8 
PLANE_POST_CSC_GAMC_INDEX_7_D = 0x737D8
 
'''
Register field expected values 
'''
index_auto_increment_AUTO_INCREMENT = 0b1 
index_auto_increment_NO_INCREMENT = 0b0 
index_value_DEFAULT = [0, 34]

 
'''
Register bitfield defnition structure 
'''
class PLANE_POST_CSC_GAMC_INDEX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("index_value"         , ctypes.c_uint32, 6), # 0 to 5 
        ("reserved_6"          , ctypes.c_uint32, 4), # 6 to 9 
        ("index_auto_increment" , ctypes.c_uint32, 1), # 10 to 10 
        ("reserved_11"         , ctypes.c_uint32, 21), # 11 to 31 
    ]

 
class PLANE_POST_CSC_GAMC_INDEX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_POST_CSC_GAMC_INDEX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
