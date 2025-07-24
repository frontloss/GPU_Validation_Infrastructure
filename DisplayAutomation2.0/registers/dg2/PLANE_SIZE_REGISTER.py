import ctypes

'''
Register instance and offset 
'''
PLANE_SIZE_1_A  = 0x70190   
PLANE_SIZE_1_B  = 0x71190   
PLANE_SIZE_1_C  = 0x72190   
PLANE_SIZE_1_D  = 0x73190   

PLANE_SIZE_2_A  = 0x70290   
PLANE_SIZE_2_B  = 0x71290   
PLANE_SIZE_2_C  = 0x72290   
PLANE_SIZE_2_D  = 0x73290   

PLANE_SIZE_3_A  = 0x70390   
PLANE_SIZE_3_B  = 0x71390   
PLANE_SIZE_3_C  = 0x72390   
PLANE_SIZE_3_D  = 0x73390   

PLANE_SIZE_4_A  = 0x70490   
PLANE_SIZE_4_B  = 0x71490   
PLANE_SIZE_4_C  = 0x72490   
PLANE_SIZE_4_D  = 0x73490   

PLANE_SIZE_5_A  = 0x70590   
PLANE_SIZE_5_B  = 0x71590   
PLANE_SIZE_5_C  = 0x72590   
PLANE_SIZE_5_D  = 0x73590   

PLANE_SIZE_6_A  = 0x70690   
PLANE_SIZE_6_B  = 0x71690   
PLANE_SIZE_6_C  = 0x72690   
PLANE_SIZE_6_D  = 0x73690   

PLANE_SIZE_7_A  = 0x70790   
PLANE_SIZE_7_B  = 0x71790   
PLANE_SIZE_7_C  = 0x72790   
PLANE_SIZE_7_D  = 0x73790   
 
'''
Register bitfield defnition structure 
'''
class PLANE_SIZE_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("width",           ctypes.c_uint32,13), # 0 to 12 
        ("reserved_13",     ctypes.c_uint32,3), # 13 to 15 
        ("height",          ctypes.c_uint32,13), # 16 to 28 
        ("reserved_29",     ctypes.c_uint32,3), # 29 to 31 
    ]

 
class PLANE_SIZE_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_SIZE_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
