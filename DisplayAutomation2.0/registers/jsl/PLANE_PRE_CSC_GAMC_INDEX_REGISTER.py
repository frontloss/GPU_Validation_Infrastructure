import ctypes
 
'''
Register instance and offset 
'''
PLANE_PRE_CSC_GAMC_INDEX_1_A = 0x701D0 
PLANE_PRE_CSC_GAMC_INDEX_1_B = 0x711D0 
PLANE_PRE_CSC_GAMC_INDEX_1_C = 0x721D0
PLANE_PRE_CSC_GAMC_INDEX_1_D = 0x731D0  
PLANE_PRE_CSC_GAMC_INDEX_2_A = 0x702D0 
PLANE_PRE_CSC_GAMC_INDEX_2_B = 0x712D0 
PLANE_PRE_CSC_GAMC_INDEX_2_C = 0x722D0
PLANE_PRE_CSC_GAMC_INDEX_2_D = 0x732D0  
PLANE_PRE_CSC_GAMC_INDEX_3_A = 0x703D0 
PLANE_PRE_CSC_GAMC_INDEX_3_B = 0x713D0 
PLANE_PRE_CSC_GAMC_INDEX_3_C = 0x723D0 
PLANE_PRE_CSC_GAMC_INDEX_3_D = 0x733D0 
PLANE_PRE_CSC_GAMC_INDEX_4_A = 0x704D0 
PLANE_PRE_CSC_GAMC_INDEX_4_B = 0x714D0 
PLANE_PRE_CSC_GAMC_INDEX_4_C = 0x724D0 
PLANE_PRE_CSC_GAMC_INDEX_4_D = 0x734D0
PLANE_PRE_CSC_GAMC_INDEX_5_A = 0x705D0 
PLANE_PRE_CSC_GAMC_INDEX_5_B = 0x715D0 
PLANE_PRE_CSC_GAMC_INDEX_5_C = 0x725D0 
PLANE_PRE_CSC_GAMC_INDEX_5_D = 0x735D0
PLANE_PRE_CSC_GAMC_INDEX_6_A = 0x706D0 
PLANE_PRE_CSC_GAMC_INDEX_6_B = 0x716D0 
PLANE_PRE_CSC_GAMC_INDEX_6_C = 0x726D0 
PLANE_PRE_CSC_GAMC_INDEX_6_D = 0x736D0
PLANE_PRE_CSC_GAMC_INDEX_7_A = 0x707D0 
PLANE_PRE_CSC_GAMC_INDEX_7_B = 0x717D0 
PLANE_PRE_CSC_GAMC_INDEX_7_C = 0x727D0 
PLANE_PRE_CSC_GAMC_INDEX_7_D = 0x737D0 
'''
Register field expected values 
'''
index_auto_increment_AUTO_INCREMENT = 0b1 
index_auto_increment_NO_INCREMENT = 0b0 
index_value_DEFAULT = [0, 34]

 
'''
Register bitfield defnition structure 
'''
class PLANE_PRE_CSC_GAMC_INDEX_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("index_value"         , ctypes.c_uint32, 8), # 0 to 7 
        ("reserved_6"          , ctypes.c_uint32, 2), # 8 to 9 
        ("index_auto_increment" , ctypes.c_uint32, 1), # 10 to 10 
        ("reserved_11"         , ctypes.c_uint32, 21), # 11 to 31 
    ]

 
class PLANE_PRE_CSC_GAMC_INDEX_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_PRE_CSC_GAMC_INDEX_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
