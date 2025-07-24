import ctypes
 
'''
Register instance and offset 
'''
CUR_BUF_CFG_A = 0x7017C 
CUR_BUF_CFG_B = 0x7117C 
CUR_BUF_CFG_C = 0x7217C
PLANE_BUF_CFG_1_A = 0x7027C
PLANE_BUF_CFG_1_B = 0x7127C
PLANE_BUF_CFG_1_C = 0x7227C
PLANE_BUF_CFG_2_A = 0x7037C
PLANE_BUF_CFG_2_B = 0x7137C
PLANE_BUF_CFG_2_C = 0x7237C
PLANE_BUF_CFG_3_A = 0x7047C
PLANE_BUF_CFG_3_B = 0x7147C
PLANE_BUF_CFG_3_C = 0x7247C
PLANE_BUF_CFG_4_A = 0x7057C
PLANE_BUF_CFG_4_B = 0x7157C
PLANE_BUF_CFG_4_C = 0x7257C
PLANE_NV12_BUF_CFG_1_A = 0x70278
PLANE_NV12_BUF_CFG_1_B = 0x71278
PLANE_NV12_BUF_CFG_1_C = 0x72278
PLANE_NV12_BUF_CFG_2_A = 0x70378
PLANE_NV12_BUF_CFG_2_B = 0x71378
PLANE_NV12_BUF_CFG_2_C = 0x72378
PLANE_NV12_BUF_CFG_3_A = 0x70478
PLANE_NV12_BUF_CFG_3_B = 0x71478
PLANE_NV12_BUF_CFG_3_C = 0x72478
PLANE_NV12_BUF_CFG_4_A = 0x70578
PLANE_NV12_BUF_CFG_4_B = 0x71578
PLANE_NV12_BUF_CFG_4_C = 0x72578

 
'''
Register field expected values 
'''
buffer_end_DEFAULT = 0x000 
buffer_start_DEFAULT = 0x000 

 
'''
Register bitfield defnition structure 
'''
class PLANE_BUF_CFG_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("buffer_start" , ctypes.c_uint32, 10), # 0 to 9 
        ("reserved_10" , ctypes.c_uint32, 6), # 10 to 15 
        ("buffer_end"  , ctypes.c_uint32, 10), # 16 to 25 
        ("reserved_26" , ctypes.c_uint32, 6), # 26 to 31 
    ]

 
class PLANE_BUF_CFG_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PLANE_BUF_CFG_REG ),
        ("asUint", ctypes.c_uint32 ) ]
 
